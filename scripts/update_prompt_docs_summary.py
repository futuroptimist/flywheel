"""Generate prompt docs summary using RepoCrawler."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import List, Set

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
            existing.add(parts[1])
    return existing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-from", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--token")
    args = parser.parse_args()

    repos = load_repos(args.repos_from)
    crawler = RepoCrawler(repos, token=args.token)

    existing_docs = _parse_existing(args.out)
    rows: list[list[str]] = []
    new_rows: list[list[str]] = []

    # Include prompt docs from the local repository (first entry)
    local_repo = repos[0].split("@")[0]
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    for path in sorted(docs_dir.glob("*prompt*.md")):
        if path.name == "prompt-docs-summary.md":
            continue
        text = path.read_text()
        title = extract_title(text)
        repo_link = f"**[{local_repo}](https://github.com/{local_repo})**"
        file_name = path.name
        doc_link = (
            f"[{file_name}](https://github.com/{local_repo}/blob/main/docs/"
            f"{file_name})"
        )
        row = [repo_link, doc_link, title]
        rows.append(row)
        if doc_link not in existing_docs:
            new_rows.append(row)

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
                title = extract_title(text)
                repo_link = f"[{name}](https://github.com/{name})"
                file_name = path.split("/")[-1]
                doc_link = "[{0}](https://github.com/{1}/blob/{2}/{3})".format(
                    file_name,
                    name,
                    branch,
                    path,
                )
                row = [repo_link, doc_link, title]
                rows.append(row)
                if doc_link not in existing_docs:
                    new_rows.append(row)

    table = tabulate(
        rows,
        headers=["Repo", "Document", "Title"],
        tablefmt="github",
    )
    lines = [
        "# Prompt Docs Summary",
        "",
        "This index is auto-generated with "
        "[scripts/update_prompt_docs_summary.py]"
        "(../scripts/update_prompt_docs_summary.py) "
        "using RepoCrawler to discover prompt documents across repositories.",
        "",
        table,
    ]

    if new_rows:
        lines.extend(
            [
                "",
                "## Untriaged Prompt Docs",
                "",
                tabulate(
                    new_rows,
                    headers=["Repo", "Document", "Title"],
                    tablefmt="github",
                ),
            ]
        )
    else:
        lines.extend(["", "## Untriaged Prompt Docs", "", "None detected."])

    lines.extend(["", f"_Updated automatically: {date.today()}_", ""])
    args.out.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
