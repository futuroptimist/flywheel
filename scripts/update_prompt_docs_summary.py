"""Generate prompt docs summary using RepoCrawler."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tabulate import tabulate  # noqa: E402

from flywheel.repocrawler import RepoCrawler  # noqa: E402

# Suggested prompt docs for repositories that currently lack them.
SUGGESTED_DOCS = {
    "futuroptimist/axel": (
        "prompts-synergy.md",
        "Centralize prompts for cross-repo coordination via the Synergy Bot",
    ),
    "futuroptimist/gabriel": (
        "prompts-gabriel.md",
        "Document prompts guiding Gabriel integrations",
    ),
    "futuroptimist/futuroptimist": (
        "prompts-organization.md",
        "Capture prompts for organizational workflows and profile updates",
    ),
    "futuroptimist/token.place": (
        "prompts-market.md",
        "Outline prompts for token marketplace operations",
    ),
    "futuroptimist/f2clipboard": (
        "prompts-clipboard.md",
        "Describe prompts for clipboard automation and sharing",
    ),
    "futuroptimist/sigma": (
        "prompts-design.md",
        "Collect prompts for collaborative design sessions",
    ),
    "futuroptimist/wove": (
        "prompts-weaving.md",
        "Detail prompts for weaving simulations and planning",
    ),
    "futuroptimist/sugarkube": (
        "prompts-devops.md",
        "Provide prompts for deployment and infrastructure tasks",
    ),
}


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-from", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--token")
    args = parser.parse_args()

    repos = load_repos(args.repos_from)
    crawler = RepoCrawler(repos, token=args.token)
    infos = crawler.crawl()

    rows: list[list[str]] = []
    repos_with_docs: set[str] = set()

    # Include prompt docs from the local repository (first entry)
    local_repo = repos[0].split("@")[0]
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    for path in sorted(docs_dir.glob("prompts-*.md")):
        text = path.read_text()
        title = extract_title(text)
        repo_link = f"**[{local_repo}](https://github.com/{local_repo})**"
        file_name = path.name
        doc_link = (
            f"[{file_name}](https://github.com/{local_repo}/blob/main/docs/"
            f"{file_name})"
        )
        rows.append([repo_link, doc_link, title])
        repos_with_docs.add(local_repo)

    # Add prompt docs from remote repositories (skip local repo)
    for info in infos[1:]:
        files = crawler._list_files(info.name, info.branch)
        for path in files:
            if "prompts-" in path and path.endswith(".md"):
                text = crawler._fetch_file(info.name, path, info.branch) or ""
                title = extract_title(text)
                repo_link = f"[{info.name}](https://github.com/{info.name})"
                file_name = path.split("/")[-1]
                doc_link = (
                    f"[{file_name}](https://github.com/{info.name}/blob/"
                    f"{info.branch}/{path})"
                )
                rows.append([repo_link, doc_link, title])
                repos_with_docs.add(info.name)

    table = tabulate(
        rows,
        headers=["Repo", "Document", "Title"],
        tablefmt="github",
    )

    suggestions: list[list[str]] = []
    for repo in (r.split("@")[0] for r in repos):
        if repo in repos_with_docs:
            continue
        doc_info = SUGGESTED_DOCS.get(repo)
        if doc_info:
            doc_name, purpose = doc_info
            repo_link = f"[{repo}](https://github.com/{repo})"
            suggestions.append([repo_link, doc_name, purpose])

    lines = [
        "# Prompt Docs Summary",
        "",
        "This index is auto-generated with ",
        "[scripts/update_prompt_docs_summary.py]",
        "(../scripts/update_prompt_docs_summary.py)",
        "using RepoCrawler to discover prompt documents across repositories.",
        "",
        table,
    ]

    if suggestions:
        suggestion_table = tabulate(
            suggestions,
            headers=["Repo", "Suggested Doc", "Purpose"],
            tablefmt="github",
        )
        lines.extend(["", "## Suggested Prompt Docs", "", suggestion_table])

    lines.extend(["", f"_Updated automatically: {date.today()}_", ""])

    args.out.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
