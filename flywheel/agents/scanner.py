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
    """Clone ``repo`` into ``dest``, overwriting existing paths.

    Symlinks are removed without touching their targets.
    Missing parent directories are created automatically.
    """

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    url = f"https://github.com/{repo}.git"
    subprocess.run(
        ["git", "clone", "--depth", "1", url, str(dest)],
        check=True,
    )


def analyze_repo(path: Path) -> str:
    """Return a simple report listing top-level files.

    Only regular, non-hidden files in ``path`` are included. Directories and
    symlinks are ignored. Filenames are sorted case-insensitively. The returned
    Markdown string ends with a trailing newline so that writing it directly to
    disk produces a POSIX-compliant file.
    """

    names = [
        p.name
        for p in path.iterdir()
        if p.is_file() and not p.is_symlink() and not p.name.startswith(".")
    ]
    files = sorted(names, key=str.lower)
    report_lines = [
        f"# Report for {path.name}",
        "",
        "## Top-level files",
        "",
    ]
    report_lines.extend(f"- {name}" for name in files)
    report_lines.append("")
    report_lines.append("*(OpenAI analysis would go here)*")
    return "\n".join(report_lines) + "\n"


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
