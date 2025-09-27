"""Generate prompt docs summary using RepoCrawler."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import DefaultDict, Iterable, List

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
    # Treat TODO markers as placeholders only when they open a line or bullet.
    re.compile(
        r"^\s*(?:[-*]|//|#|<!--)?\s*TODO\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(r"\bREPLACE\b", re.IGNORECASE),
    # Match placeholder-style "YOUR" tokens (e.g., "YOURNAME", "YOUR TOKEN").
    # This intentionally remains case-sensitive so natural language like
    # "your project" does not trip the heuristic.
    re.compile(r"\bYOUR(?:\s+[A-Z][A-Z0-9_-]*|[A-Z0-9_-]+)\b"),
]


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


def extract_prompts(text: str, base_url: str) -> List[List[str]]:
    lines = text.splitlines()
    prompts: List[List[str]] = []
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
        prompts.append([f"[{title}]({base_url})", "unknown", one_click])
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
        prompts.append([f"[{title}]({base_url}#{anchor})", ptype, one_click])
    return prompts


PROMPT_KEYWORDS = ("prompt", "implement")
PROMPT_DOC_SKIP_SUFFIXES = ("prompt-docs-summary.md", "prompt-docs-todos.md")

# Exclude archival folders such as legacy postmortems that happen
# to include the word "prompt" in their filenames (e.g., historical
# docs/pms/2025-08-09-spellcheck-prompt-summary.md).
PROMPT_DOC_EXCLUDE_PATTERNS = (
    re.compile(r"(?:^|/)pms/"),
    re.compile(r"/postmortem"),
    re.compile(r"/post-mortem"),
)


def looks_like_prompt_doc(path: str) -> bool:
    """Return True when the path suggests a prompt/implementation doc."""

    pl = path.lower()
    if any(pl.endswith(suffix) for suffix in PROMPT_DOC_SKIP_SUFFIXES):
        return False
    if any(pattern.search(pl) for pattern in PROMPT_DOC_EXCLUDE_PATTERNS):
        return False
    return any(keyword in pl for keyword in PROMPT_KEYWORDS)


def iter_local_prompt_docs(docs_root: Path) -> Iterable[Path]:
    """Yield markdown prompt docs bundled with the local repository."""
    for path in sorted(docs_root.rglob("*.md")):
        rel = path.relative_to(docs_root)
        if looks_like_prompt_doc(str(rel)):
            yield path


def is_canonical_prompt_path(path: str) -> bool:
    """Return True if the prompt doc lives under docs/prompts/codex/."""

    normalized = path.replace("\\", "/")
    return normalized.startswith("docs/prompts/codex/")


def describe_noncanonical_location(path: str) -> str:
    normalized = path.replace("\\", "/")
    parts = normalized.split("/")

    if normalized.startswith("docs/"):
        if len(parts) <= 2:
            return "docs/"
        if parts[1] == "prompts" and len(parts) > 2:
            return "docs/prompts"
        return "/".join(parts[:2])

    parent = Path(normalized).parent
    if parent in {Path(""), Path(".")}:
        return normalized
    return parent.as_posix()


def format_locations(locations: Iterable[str]) -> List[str]:
    return [f"`{loc}`" for loc in locations]


def format_markdown(path: Path) -> None:
    """Format the generated Markdown file with Prettier."""

    try:
        subprocess.run(
            [
                "npx",
                "--yes",
                "prettier@latest",
                "--log-level",
                "warn",
                "--write",
                str(path),
            ],
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(
            "warning: failed to run `npx prettier --write` on"
            f" {path}. Generated file may require manual formatting.",
            file=sys.stderr,
        )


def normalize_heading_spacing(path: Path) -> None:
    """Ensure the title immediately follows the spellchecker comment."""

    lines = path.read_text().splitlines()
    if (
        len(lines) >= 3
        and lines[0].startswith("<!-- spellchecker:")
        and not lines[1].strip()
        and lines[2].startswith("# ")
    ):
        normalized = "\n".join([lines[0], lines[2], *lines[3:]])
        newline = "" if normalized.endswith("\n") else "\n"
        path.write_text(normalized + newline)


def main() -> None:
    from tabulate import tabulate

    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-from", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--token")
    args = parser.parse_args()

    repos = load_repos(args.repos_from)
    crawler = RepoCrawler(repos, token=args.token)

    grouped: DefaultDict[str, List[List[str]]] = defaultdict(list)
    noncanonical_paths: DefaultDict[str, set[str]] = defaultdict(set)

    # Include prompt docs from the local repository (first entry)
    local_repo = repos[0].split("@")[0]
    docs_root = Path(__file__).resolve().parents[1] / "docs"
    for path in iter_local_prompt_docs(docs_root):
        text = path.read_text()
        repo_link = f"**[{local_repo}](https://github.com/{local_repo})**"
        rel = Path("docs") / path.relative_to(docs_root)
        rel_str = rel.as_posix()
        base_url = f"https://github.com/{local_repo}/blob/main/{rel_str}"
        path_link = f"[{rel_str}]({base_url})"
        prompts = extract_prompts(text, base_url)
        for prompt_link, ptype, one_click in prompts:
            if not one_click:
                continue
            row = [path_link, prompt_link, ptype, "yes"]
            if path.name.startswith("prompts-"):
                row = [f"**{cell}**" for cell in row]
            grouped[repo_link].append(row)
        if not is_canonical_prompt_path(rel_str):
            location = describe_noncanonical_location(rel_str)
            noncanonical_paths[repo_link].add(location)

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
            if pl.endswith(".md") and looks_like_prompt_doc(pl):
                text = crawler._fetch_file(name, path, branch) or ""
                repo_link = f"[{name}](https://github.com/{name})"
                base_url = f"https://github.com/{name}/blob/{branch}/{path}"
                path_link = f"[{path}]({base_url})"
                prompts = extract_prompts(text, base_url)
                for prompt_link, ptype, one_click in prompts:
                    if not one_click:
                        continue
                    row = [path_link, prompt_link, ptype, "yes"]
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

    repo_root = Path(__file__).resolve().parents[1]
    scripts_path = repo_root / "scripts" / "update_prompt_docs_summary.py"
    script_display = scripts_path.relative_to(repo_root).as_posix()
    script_relpath = os.path.relpath(scripts_path, args.out.parent)
    script_href = Path(script_relpath).as_posix()

    lines = [
        "<!-- spellchecker: disable -->",
        "# Prompt Docs Summary",
        "",
        (
            "This index is auto-generated with "
            f"[{script_display}]"
            f"({script_href}) "
            "using RepoCrawler to discover prompt documents "
            "across repositories."
        ),
        "",
        (
            "RepoCrawler powers other reports like repo-feature summaries; "
            "use it as a model for deep dives."
        ),
        "",
        (
            "Think of each listed repository as a small flywheel belted "
            "to this codebase. The list in dict/prompt-doc-repos.txt "
            "mirrors docs/repo_list.txt; if a repo drops from the "
            "output, "
            "fix that integration rather than deleting it."
        ),
        "",
        (
            "All prompts are verified with OpenAI Codex. Other coding "
            "agents like Claude Code, Gemini CLI, and Cursor should work "
            "too."
        ),
        "",
        (
            f"**{total_prompts} one-click prompts verified across "
            f"{repo_count} repos ({counts['evergreen']} evergreen, "
            f"{counts['one-off']} one-off, {counts['unknown']} unknown).**"
        ),
        "",
        (
            "One-off prompts are temporary—copy them into issues or "
            "PRs, implement, and then remove them from source docs."
        ),
        "",
        (
            "All listed prompts are mechanically verified as 1-click "
            "ready: copy & paste without editing."
        ),
        "",
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

    lines.extend(
        [
            "## Legend",
            "",
            tabulate(
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
                tablefmt="github",
            ),
            "",
        ]
    )

    for repo_link, repo_prompts in grouped.items():
        lines.append(f"## {repo_link}")
        lines.append("")
        lines.append(
            tabulate(
                repo_prompts,
                headers=["Path", "Prompt", "Type", "One-click?"],
                tablefmt="github",
            )
        )
        lines.append("")
        if noncanonical_paths.get(repo_link):
            noncanonical = noncanonical_paths[repo_link]
            formatted_locations = format_locations(noncanonical)
            locations = ", ".join(sorted(formatted_locations))
            lines.append(
                (
                    "_❌ Note: Prompt docs also found outside "
                    "`docs/prompts/codex/`: "
                    f"{locations}._"
                )
            )
            lines.append("")

    todo_file = docs_root / "prompt-docs-todos.md"
    if todo_file.exists() and todo_file.read_text().strip():
        todo_content = todo_file.read_text().strip()
        lines.extend(
            [
                "## TODO Prompts for Other Repos",
                "",
                todo_content,
                "",
            ]
        )

    lines.extend([f"_Updated automatically: {date.today()}_", ""])
    args.out.write_text("\n".join(line.rstrip() for line in lines))
    format_markdown(args.out)
    normalize_heading_spacing(args.out)


if __name__ == "__main__":
    main()
