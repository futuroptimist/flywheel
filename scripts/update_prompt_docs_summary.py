"""Generate prompt docs summary using RepoCrawler."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from itertools import count
from pathlib import Path
from textwrap import fill
from typing import DefaultDict, Dict, Iterable, Iterator, List, Tuple

sys.path.append(str(Path(__file__).resolve().parents[1]))
from flywheel.repocrawler import RepoCrawler  # noqa: E402


def load_repos(path: Path) -> List[str]:
    lines = path.read_text().splitlines()
    return [line.strip() for line in lines if line.strip()]


def extract_title(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.lower().startswith("title:"):
                return line.split(":", 1)[1].strip().strip("'\"")
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


PLACEHOLDER_PATTERNS = [
    re.compile(r"{[A-Z][^}]+}"),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bREPLACE\b", re.IGNORECASE),
    # Match placeholder-style "YOUR" tokens (e.g., "YOURNAME", "YOUR TOKEN").
    # This intentionally remains case-sensitive so natural language like
    # "your project" does not trip the heuristic.
    re.compile(r"\bYOUR(?:\s+[A-Z][A-Z0-9_-]*|[A-Z0-9_-]+)\b"),
]

TABLE_COLUMN_WIDTHS = [38, 38, 12, 10]
LEGEND_COLUMN_WIDTHS = [12, 74]
NOTE_WRAP_WIDTH = 88


def is_one_click(snippet: str) -> bool:
    """Heuristically determine if a prompt is 1-click ready."""

    return not any(pattern.search(snippet) for pattern in PLACEHOLDER_PATTERNS)


def find_type(lines: List[str], start: int) -> str:
    for idx in range(start, min(start + 5, len(lines))):
        match = re.search(r"Type:\s*([\w-]+)", lines[idx], re.IGNORECASE)
        if match:
            return match.group(1).lower()
    return ""


def is_prompt_heading(title: str) -> bool:
    return "prompt" in title.lower() or title[:1].isdigit()


def extract_prompts(
    text: str, base_url: str
) -> List[Tuple[str, str, str, bool]]:
    lines = text.splitlines()
    prompts: List[Tuple[str, str, str, bool]] = []
    headings: List[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("##"):
            headings.append((i, line[2:].strip()))
        elif line.startswith("## ") or line.startswith("### "):
            title = line.lstrip("#").strip()
            if is_prompt_heading(title):
                headings.append((i, title))
    if not headings:
        title = extract_title(text) or base_url.split("/")[-1]
        snippet = text
        one_click = is_one_click(snippet)
        prompts.append((title, base_url, "unknown", one_click))
        return prompts

    for idx, (line_no, title) in enumerate(headings):
        if idx + 1 < len(headings):
            next_line = headings[idx + 1][0]
        else:
            next_line = len(lines)
        ptype = find_type(lines, line_no + 1)
        if not ptype:
            title_lower = title.lower()
            if re.match(r"\d", title_lower):
                ptype = "one-off"
            elif "prompt" in title_lower:
                ptype = "evergreen"
            else:
                ptype = "unknown"
        elif ptype == "one":
            ptype = "one-off"
        snippet = "\n".join(lines[line_no + 1 : next_line])  # noqa: E203
        anchor = slugify(title)
        one_click = is_one_click(snippet)
        prompts.append((title, f"{base_url}#{anchor}", ptype, one_click))
    return prompts


def iter_local_prompt_docs(docs_root: Path) -> Iterable[Path]:
    """Yield markdown prompt docs bundled with the local repository."""
    for path in sorted(docs_root.rglob("*.md")):
        rel = path.relative_to(docs_root)
        pl = str(rel).lower()
        if (
            "prompt" in pl
            and not pl.endswith("prompt-docs-summary.md")
            and not pl.endswith("prompt-docs-todos.md")
        ):
            yield path


def is_canonical_prompt_path(path: str) -> bool:
    """Return True if the prompt doc lives under docs/prompts/codex/."""

    normalized = path.replace("\\", "/")
    return normalized.startswith("docs/prompts/codex/")


def describe_noncanonical_location(path: str) -> str:
    normalized = path.replace("\\", "/")
    parent = Path(normalized).parent
    normalized_path = Path(normalized)
    if not parent or parent in {Path(""), Path(".")}:
        return normalized_path.as_posix()
    parent_str = parent.as_posix()
    if parent_str == "docs":
        return normalized_path.as_posix()
    return parent_str


def wrap_noncanonical_note(locations: Iterable[str]) -> List[str]:
    note = (
        "_Note: Prompt docs also found outside `docs/prompts/codex/`: "
        f"{', '.join(sorted(f'`{loc}`' for loc in locations))}._"
    )
    return fill(
        note,
        width=NOTE_WRAP_WIDTH,
        break_long_words=False,
        break_on_hyphens=False,
    ).splitlines()


def wrap_paragraph(text: str) -> List[str]:
    return fill(
        text,
        width=NOTE_WRAP_WIDTH,
        break_long_words=False,
        break_on_hyphens=False,
    ).splitlines()


def wrap_url_lines(url: str) -> List[str]:
    wrapped = fill(
        url.replace("/", "/ "),
        width=NOTE_WRAP_WIDTH,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return [line.replace("/ ", "/") for line in wrapped.splitlines()]


def wrap_table_cell(text: str, width: int) -> List[str]:
    bold = text.startswith("**") and text.endswith("**")
    inner = text[2:-2] if bold else text
    prepared = inner.replace("][", "] [").replace("/", "/ ")
    wrapped = fill(
        prepared,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ).splitlines() or [""]
    cleaned = [line.replace("/ ", "/") for line in wrapped]
    if bold:
        cleaned[0] = f"**{cleaned[0]}"
        cleaned[-1] = f"{cleaned[-1]}**"
    return cleaned


def render_table_row(
    cells: List[List[str]], col_widths: List[int]
) -> List[str]:
    max_height = max(len(cell) for cell in cells)
    rows: List[str] = []
    for idx in range(max_height):
        parts = []
        for col, width in enumerate(col_widths):
            cell_lines = cells[col]
            value = cell_lines[idx] if idx < len(cell_lines) else ""
            parts.append(value.ljust(width))
        rows.append("| " + " | ".join(parts) + " |")
    return rows


def format_markdown_table(
    rows: List[List[str]], headers: List[str], column_widths: List[int]
) -> List[str]:
    structured = [
        [
            wrap_table_cell(cell, column_widths[col])
            for col, cell in enumerate(row)
        ]
        for row in [headers, *rows]
    ]
    col_widths = [
        min(
            column_widths[col],
            max(len(line) for row in structured for line in row[col]),
        )
        for col in range(len(headers))
    ]
    lines: List[str] = []
    lines.extend(render_table_row(structured[0], col_widths))
    separator_parts = ["-" * max(3, width) for width in col_widths]
    separator = "| " + " | ".join(separator_parts) + " |"
    lines.append(separator)
    for row_cells in structured[1:]:
        lines.extend(render_table_row(row_cells, col_widths))
    return lines


def format_reference_definition(name: str, url: str) -> List[str]:
    url_lines = wrap_url_lines(url)
    if not url_lines:
        return [f"[{name}]: {url}"]
    first, *rest = url_lines
    lines = [f"[{name}]: {first}"]
    lines.extend(f"    {line}" for line in rest)
    return lines


def register_reference(
    url: str,
    prefix: str,
    counter: Iterator[int],
    lookup: Dict[str, str],
    order: List[Tuple[str, str]],
) -> str:
    if url in lookup:
        return lookup[url]
    ref = f"{prefix}-{next(counter)}"
    lookup[url] = ref
    order.append((ref, url))
    return ref


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-from", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--token")
    args = parser.parse_args()

    repos = load_repos(args.repos_from)
    crawler = RepoCrawler(repos, token=args.token)

    grouped: DefaultDict[str, List[List[str]]] = defaultdict(list)
    noncanonical_paths: DefaultDict[str, set[str]] = defaultdict(set)
    reference_counter = count(1)
    reference_lookup: Dict[str, str] = {}
    reference_order: List[Tuple[str, str]] = []

    # Include prompt docs from the local repository (first entry)
    local_repo = repos[0].split("@")[0]
    docs_root = Path(__file__).resolve().parents[1] / "docs"
    for path in iter_local_prompt_docs(docs_root):
        text = path.read_text()
        repo_link = f"**[{local_repo}](https://github.com/{local_repo})**"
        rel = Path("docs") / path.relative_to(docs_root)
        rel_str = rel.as_posix()
        base_url = (
            f"https://github.com/{local_repo}/blob/main/{rel_str}"
        )
        path_ref = register_reference(
            base_url,
            "path",
            reference_counter,
            reference_lookup,
            reference_order,
        )
        path_cell = f"[{rel_str}][{path_ref}]"
        prompts = extract_prompts(text, base_url)
        for prompt_title, prompt_url, ptype, one_click in prompts:
            if not one_click:
                continue
            prompt_ref = register_reference(
                prompt_url,
                "prompt",
                reference_counter,
                reference_lookup,
                reference_order,
            )
            prompt_cell = f"[{prompt_title}][{prompt_ref}]"
            row = [path_cell, prompt_cell, ptype, "yes"]
            if path.name.startswith("prompts-"):
                row = [f"**{cell}**" for cell in row]
            grouped[repo_link].append(row)
        if not is_canonical_prompt_path(rel_str):
            noncanonical_paths[repo_link].add(
                describe_noncanonical_location(rel_str)
            )

    # Add prompt docs from remote repositories (skip local repo)
    for spec in repos[1:]:
        if "@" in spec:
            name, branch = spec.split("@", 1)
        else:
            name = spec
            branch = crawler._default_branch(name)
        files = crawler._list_files(name, branch)
        for path in files:
            pl = path.lower()
            if (
                "prompt" in pl
                and pl.endswith(".md")
                and not pl.endswith("prompt-docs-summary.md")
                and not pl.endswith("prompt-docs-todos.md")
            ):
                text = crawler._fetch_file(name, path, branch) or ""
                repo_link = f"[{name}](https://github.com/{name})"
                base_url = f"https://github.com/{name}/blob/{branch}/{path}"
                path_ref = register_reference(
                    base_url,
                    "path",
                    reference_counter,
                    reference_lookup,
                    reference_order,
                )
                path_cell = f"[{path}][{path_ref}]"
                prompts = extract_prompts(text, base_url)
                for prompt_title, prompt_url, ptype, one_click in prompts:
                    if not one_click:
                        continue
                    prompt_ref = register_reference(
                        prompt_url,
                        "prompt",
                        reference_counter,
                        reference_lookup,
                        reference_order,
                    )
                    prompt_cell = f"[{prompt_title}][{prompt_ref}]"
                    row = [path_cell, prompt_cell, ptype, "yes"]
                    if Path(path).name.startswith("prompts-"):
                        row = [f"**{cell}**" for cell in row]
                    grouped[repo_link].append(row)
                    if not is_canonical_prompt_path(path):
                        noncanonical_paths[repo_link].add(
                            describe_noncanonical_location(path)
                        )

    type_order = {"evergreen": 0, "unknown": 1, "one-off": 2}
    for repo_prompts in grouped.values():
        repo_prompts.sort(key=lambda row: type_order.get(row[2], 1))

    counts = {"evergreen": 0, "one-off": 0, "unknown": 0}
    for repo_prompts in grouped.values():
        for _, _, ptype, _ in repo_prompts:
            counts[ptype] = counts.get(ptype, 0) + 1
    total_prompts = sum(counts.values())
    repo_count = len(grouped)

    lines = [
        "<!-- spellchecker: disable -->",
        "# Prompt Docs Summary",
        "",
        "This index is auto-generated with ",
        "[scripts/update_prompt_docs_summary.py]",
        "(../../scripts/update_prompt_docs_summary.py) ",
        "using RepoCrawler to discover prompt documents across repositories.",
        "",
        "RepoCrawler powers other reports like repo-feature summaries; ",
        "use it as a model for deep dives.",
        "",
    ]

    lines.extend(
        wrap_paragraph(
            "Think of each listed repository as a small flywheel belted "
            "to this codebase. The list in dict/prompt-doc-repos.txt "
            "mirrors docs/repo_list.txt; if a repo drops from the output, "
            "fix that integration rather than deleting it."
        )
    )
    lines.append("")
    lines.extend(
        wrap_paragraph(
            "All prompts are verified with OpenAI Codex. Other coding agents "
            "like Claude Code, Gemini CLI, and Cursor should work too."
        )
    )
    lines.append("")
    lines.append(
        f"**{total_prompts} one-click prompts verified across "
        f"{repo_count} repos ({counts['evergreen']} evergreen, "
        f"{counts['one-off']} one-off, {counts['unknown']} unknown).**"
    )
    lines.append("")
    lines.extend(
        wrap_paragraph(
            "One-off prompts are temporary—copy them into issues or PRs, "
            "implement, and then remove them from source docs."
        )
    )
    lines.append("")
    lines.extend(
        wrap_paragraph(
            "All listed prompts are mechanically verified as 1-click ready: "
            "copy & paste without editing."
        )
    )
    lines.append("")
    lines.extend(
        [
            "Run this script to regenerate the table:",
            "",
            "```bash",
            (
                "python scripts/update_prompt_docs_summary.py "
                "--repos-from docs/repo_list.txt "
                "--out docs/prompt-docs-summary.md"
            ),
            "```",
            "",
        ]
    )

    lines.extend(
        [
            "## Legend",
            "",
            *format_markdown_table(
                [
                    [
                        "evergreen",
                        (
                            "prompts that can be reused to hillclimb toward "
                            "goals like feature completeness or test coverage"
                        ),
                    ],
                    [
                        "one-off",
                        (
                            "prompts to implement features or make "
                            "recommended changes "
                            "(glorified TODO; remove after cleanup)"
                        ),
                    ],
                    [
                        "unknown",
                        (
                            "catch-all; refine into another category or "
                            "create a new one"
                        ),
                    ],
                ],
                headers=["Type", "Description"],
                column_widths=LEGEND_COLUMN_WIDTHS,
            ),
            "",
        ]
    )

    for repo_link, repo_prompts in grouped.items():
        lines.append(f"## {repo_link}")
        lines.append("")
        lines.extend(
            format_markdown_table(
                repo_prompts,
                headers=["Path", "Prompt", "Type", "One-click?"],
                column_widths=TABLE_COLUMN_WIDTHS,
            )
        )
        lines.append("")
        if noncanonical_paths.get(repo_link):
            lines.extend(
                wrap_noncanonical_note(noncanonical_paths[repo_link]) + [""]
            )

    todo_file = docs_root / "prompt-docs-todos.md"
    if todo_file.exists() and todo_file.read_text().strip():
        todo_lines = [
            line.rstrip() for line in todo_file.read_text().splitlines()
        ]
        heading = todo_lines[0].strip()
        description = todo_lines[2].strip() if len(todo_lines) > 2 else ""
        table_lines = [
            line for line in todo_lines if line.strip().startswith("|")
        ]

        lines.extend(["## TODO Prompts for Other Repos", "", heading, ""])
        if description:
            lines.extend(wrap_paragraph(description))
            lines.append("")

        if table_lines:
            header_cells = [
                cell.strip()
                for cell in table_lines[0].strip().strip("|").split("|")
            ]
            data_lines = [
                [
                    cell.strip() for cell in row.strip().strip("|").split("|")
                ]
                for row in table_lines[2:]
                if row.strip()
            ]
            todo_rows: List[List[str]] = []
            for repo, prompt_cell, prompt_type, notes in data_lines:
                match = re.match(r"\[(.+?)\]\((.+)\)", prompt_cell)
                if match:
                    label, url = match.groups()
                    prompt_ref = register_reference(
                        url,
                        "todo",
                        reference_counter,
                        reference_lookup,
                        reference_order,
                    )
                    formatted_prompt = f"[{label}][{prompt_ref}]"
                else:
                    formatted_prompt = prompt_cell
                todo_rows.append([repo, formatted_prompt, prompt_type, notes])

            lines.extend(
                format_markdown_table(
                    todo_rows,
                    headers=header_cells,
                    column_widths=[24, 52, 10, 16],
                )
            )
            lines.append("")

    if reference_order:
        lines.append("")
        for name, url in reference_order:
            lines.extend(format_reference_definition(name, url))
        lines.append("")

    lines.extend([f"_Updated automatically: {date.today()}_", ""])
    args.out.write_text("\n".join(line.rstrip() for line in lines))


if __name__ == "__main__":
    main()
