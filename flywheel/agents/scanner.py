"""Clone a set of repos and generate scan reports."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPOS = [
    "futuroptimist/token.place",
    "democratizedspace/dspace",
    "futuroptimist/gabriel",
]


def clone_repo(repo: str, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    url = f"https://github.com/{repo}.git"
    subprocess.run(
        ["git", "clone", "--depth", "1", url, str(dest)],
        check=True,
    )


def analyze_repo(path: Path) -> str:
    files = sorted(p.name for p in path.iterdir())
    report_lines = [
        f"# Report for {path.name}",
        "",
        "## Top-level files",
        "",
    ]
    report_lines.extend(f"- {name}" for name in files)
    report_lines.append("")
    report_lines.append("*(OpenAI analysis would go here)*")
    return "\n".join(report_lines)


def main() -> None:
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    work_dir = Path(".scan-tmp")
    work_dir.mkdir(exist_ok=True)

    for repo in REPOS:
        dest = work_dir / repo.replace("/", "_")
        clone_repo(repo, dest)
        md = analyze_repo(dest)
        out = reports_dir / f"{repo.replace('/', '_')}.md"
        out.write_text(md)


if __name__ == "__main__":
    main()
