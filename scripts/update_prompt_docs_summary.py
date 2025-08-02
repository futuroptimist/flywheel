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
    for idx, info in enumerate(infos):
        files = crawler._list_files(info.name, info.branch)
        for path in files:
            if "prompts-" in path and path.endswith(".md"):
                text = crawler._fetch_file(info.name, path, info.branch) or ""
                title = extract_title(text)
                repo_link = f"[{info.name}](https://github.com/{info.name})"
                if idx == 0:
                    repo_link = f"**{repo_link}**"
                file_name = path.split("/")[-1]
                doc_link = (
                    f"[{file_name}](https://github.com/{info.name}/blob/"
                    f"{info.branch}/{path})"
                )
                rows.append([repo_link, doc_link, title])

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
        "(../scripts/update_prompt_docs_summary.py)",
        "using RepoCrawler to discover prompt documents across repositories.",
        "",
        table,
        "",
        f"_Updated automatically: {date.today()}_",
        "",
    ]
    args.out.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
