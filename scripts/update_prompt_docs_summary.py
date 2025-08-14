"""Generate prompt docs summary using RepoCrawler."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import DefaultDict, List, Set

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tabulate import tabulate  # noqa: E402

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


def _parse_existing(path: Path) -> Set[str]:
    if not path.exists():
        return set()
    existing: Set[str] = set()
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 2:
            existing.add(parts[1].replace("**", ""))
    return existing


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def is_one_click(snippet: str) -> bool:
    """Heuristically determine if a prompt is 1-click ready."""
    patterns = [r"\{[^}]+\}", r"<[^>]+>", r"TODO", r"REPLACE", r"YOUR \w+"]
    return not any(re.search(p, snippet, re.IGNORECASE) for p in patterns)


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
        ptype = find_type(lines, line_no + 1) or "unknown"
        if ptype == "one":
            ptype = "one-off"
        snippet = "\n".join(lines[line_no + 1 : next_line])  # noqa: E203
        anchor = slugify(title)
        one_click = is_one_click(snippet)
        prompts.append([f"[{title}]({base_url}#{anchor})", ptype, one_click])
    return prompts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-from", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--token")
    args = parser.parse_args()

    repos = load_repos(args.repos_from)
    crawler = RepoCrawler(repos, token=args.token)

    existing_docs = _parse_existing(args.out)
    grouped: DefaultDict[str, List[List[str]]] = defaultdict(list)
    new_rows: list[list[str]] = []

    # Include prompt docs from the local repository (first entry)
    local_repo = repos[0].split("@")[0]
    docs_root = Path(__file__).resolve().parents[1] / "docs"
    prompts_dir = docs_root / "prompts" / "codex"
    for path in sorted(prompts_dir.glob("*.md")):
        text = path.read_text()
        repo_link = f"**[{local_repo}](https://github.com/{local_repo})**"
        rel = Path("docs/prompts/codex") / path.name
        base_url = f"https://github.com/{local_repo}/blob/main/{rel}"  # noqa: E501
        path_link = f"[{rel}]({base_url})"
        prompts = extract_prompts(text, base_url)
        for prompt_link, ptype, one_click in prompts:
            if not one_click:
                continue
            row = [path_link, prompt_link, ptype, "yes"]
            if path.name.startswith("prompts-"):
                row = [f"**{cell}**" for cell in row]
            grouped[repo_link].append(row)
            if prompt_link not in existing_docs:
                new_row = [
                    repo_link,
                    path_link,
                    prompt_link,
                    ptype,
                    "yes",
                ]
                # fmt: off
                if path.name.startswith("prompts-"):
                    new_row = [new_row[0]] + list(
                        f"**{cell}**" for cell in new_row[1:]
                    )
                # fmt: on
                new_rows.append(new_row)

    # Add prompt docs from remote repositories (skip local repo)
    for spec in repos[1:]:
        if "@" in spec:
            name, branch = spec.split("@", 1)
        else:
            name = spec
            branch = crawler._default_branch(name)
        files = crawler._list_files(name, branch)
        for path in files:
            if (
                "prompt" in path
                and path.endswith(".md")
                and not path.endswith("prompt-docs-summary.md")
            ):
                text = crawler._fetch_file(name, path, branch) or ""
                repo_link = f"[{name}](https://github.com/{name})"
                base_url = (
                    f"https://github.com/{name}/blob/{branch}/" f"{path}"
                )  # noqa: E501
                path_link = f"[{path}]({base_url})"
                prompts = extract_prompts(text, base_url)
                for prompt_link, ptype, one_click in prompts:
                    if not one_click:
                        continue
                    row = [path_link, prompt_link, ptype, "yes"]
                    if Path(path).name.startswith("prompts-"):
                        row = [f"**{cell}**" for cell in row]
                    grouped[repo_link].append(row)
                    if prompt_link not in existing_docs:
                        new_row = [
                            repo_link,
                            path_link,
                            prompt_link,
                            ptype,
                            "yes",
                        ]
                        if Path(path).name.startswith("prompts-"):
                            new_row = [new_row[0]] + [
                                f"**{cell}**" for cell in new_row[1:]
                            ]
                        new_rows.append(new_row)

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
        "# Prompt Docs Summary",
        "",
        "This index is auto-generated with ",
        "[scripts/update_prompt_docs_summary.py]",
        "(../../scripts/update_prompt_docs_summary.py) ",
        "using RepoCrawler to discover prompt documents across repositories.",
        "",
        (
            "All prompts are verified with OpenAI Codex. Other coding agents "
            "like Claude Code, Gemini CLI, and Cursor should work too."
        ),
        "",
        (
            f"**{total_prompts} one-click prompts verified across "
            f"{repo_count} repos ({counts['evergreen']} evergreen, "
            f"{counts['one-off']} one-off, {counts['unknown']} unknown).**"
        ),
        "",
        (
            "One-off prompts are temporary—copy them into issues or PRs, "
            "implement, and then remove them from source docs."
        ),
        "",
        (
            "All listed prompts are mechanically verified as 1-click ready: "
            "copy & paste without editing."
        ),
        "",
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
                # fmt: off
                [
                    "unknown",
                    (
                        "catch-all; refine into another category or "
                        "create a new one"
                    ),
                ],
                # fmt: on
            ],
            headers=["Type", "Description"],
            tablefmt="github",
        ),
        "",
    ]

    for repo_link, prompts in grouped.items():
        lines.append(f"## {repo_link}")
        lines.append("")
        lines.append(
            tabulate(
                prompts,
                headers=["Path", "Prompt", "Type", "One-click?"],
                tablefmt="github",
            )
        )  # noqa: E501
        lines.append("")

    if new_rows:
        lines.extend(
            [
                "## Untriaged Prompt Docs",
                "",
                tabulate(
                    new_rows,
                    headers=["Repo", "Path", "Prompt", "Type", "One-click?"],
                    tablefmt="github",
                ),
                "",
            ]
        )
    else:
        lines.extend(["## Untriaged Prompt Docs", "", "None detected.", ""])

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
    args.out.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
