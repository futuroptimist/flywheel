"""Generate prompt docs summary using RepoCrawler."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse

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


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def find_type(lines: List[str], start: int) -> str:
    for idx in range(start, min(start + 5, len(lines))):
        match = re.search(r"Type:\s*(\w+)", lines[idx], re.IGNORECASE)
        if match:
            return match.group(1).lower()
    return ""


def is_prompt_heading(title: str) -> bool:
    return "prompt" in title.lower() or title[:1].isdigit()


def extract_prompts(text: str, base_url: str) -> List[List[str]]:
    lines = text.splitlines()
    prompts: List[List[str]] = []
    for i, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("##"):
            title = line[2:].strip()
            ptype = find_type(lines, i + 1) or "unknown"
            anchor = slugify(title)
            prompts.append([f"[{title}]({base_url}#{anchor})", ptype])
        elif line.startswith("## ") or line.startswith("### "):
            title = line.lstrip("#").strip()
            if is_prompt_heading(title):
                ptype = find_type(lines, i + 1) or "unknown"
                anchor = slugify(title)
                prompts.append([f"[{title}]({base_url}#{anchor})", ptype])
    if not prompts:
        title = extract_title(text) or Path(urlparse(base_url).path).name
        prompts.append([f"[{title}]({base_url})", "unknown"])
    return prompts


def extract_first_codeblock(text: str) -> str:
    match = re.search(r"```(?:[\w+-]*)\n(.*?)\n```", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def render_table(headers: List[str], rows: List[List[str]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    lines = [header, separator]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-from", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--token")
    args = parser.parse_args()

    repos = load_repos(args.repos_from)
    crawler = RepoCrawler(repos, token=args.token)

    existing_docs = _parse_existing(args.out)
    grouped: Dict[str, Dict[str, List[List[str]]]] = {}
    new_rows: list[list[str]] = []

    # Include prompt docs from the local repository (first entry)
    local_repo = repos[0].split("@")[0]
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    template_prompts: List[Tuple[str, str, Path]] = []
    for path in sorted(docs_dir.glob("prompts-*.md")):
        text = path.read_text()
        title = extract_title(text) or path.stem.replace("-", " ").title()
        codeblock = extract_first_codeblock(text)
        template_prompts.append((title, codeblock, path))

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
                prompts = extract_prompts(text, base_url)
                if name not in grouped:
                    grouped[name] = {"link": repo_link, "prompts": []}
                for prompt_link, ptype in prompts:
                    grouped[name]["prompts"].append([prompt_link, ptype])
                    if prompt_link not in existing_docs:
                        new_rows.append([repo_link, prompt_link, ptype])

    lines = [
        "# Prompt Docs Summary",
        "",
        (
            "This index is auto-generated with "
            "[scripts/update_prompt_docs_summary.py]"
            "(../scripts/update_prompt_docs_summary.py) "
            "using RepoCrawler to discover prompt documents across "
            "repositories."
        ),
        "",
        f"## Template Prompts ({local_repo})",
        "",
    ]

    for title, codeblock, path in template_prompts:
        url = f"https://github.com/{local_repo}/blob/main/docs/{path.name}"
        lines.append(f"### [{title}]({url})")
        lines.append("")
        lines.append("```")
        lines.append(codeblock)
        lines.append("```")
        lines.append("")

    for name, info in grouped.items():
        repo_link = info["link"]
        prompts = info["prompts"]
        lines.append(f"## {repo_link}")
        lines.append("")
        lines.append("```")
        lines.append(
            f"Use https://github.com/{local_repo} prompt docs as templates. "
            f"Align {name}'s prompts in docs/prompts-*.md."
        )
        lines.append("```")
        lines.append("")
        lines.append(render_table(["Prompt", "Type"], prompts))
        lines.append("")

    if new_rows:
        lines.extend(
            [
                "## Untriaged Prompt Docs",
                "",
                render_table(["Repo", "Prompt", "Type"], new_rows),
                "",
            ]
        )
    else:
        lines.extend(["## Untriaged Prompt Docs", "", "None detected.", ""])

    todo_file = docs_dir / "prompt-docs-todos.md"
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
