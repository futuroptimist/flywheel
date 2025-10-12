"""Shared helpers for computing README status emojis."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Callable, Sequence

import requests

GITHUB_RE = re.compile(
    r"https://github.com/([\w-]+)/([\w.-]+)" r"(?:/tree/([\w./-]+))?"
)


def status_to_emoji(conclusion: str | None) -> str:
    """Return an emoji representing the workflow conclusion."""

    if conclusion is not None:
        conclusion = str(conclusion).lower()
    if conclusion in {"success", "neutral", "skipped"}:
        return "✅"
    if conclusion is None:
        return "❓"
    return "❌"


def fetch_repo_status(
    repo: str,
    token: str | None = None,
    branch: str | None = None,
    attempts: int = 2,
) -> str:
    """Return an emoji for the latest workflow run conclusion for ``repo``."""

    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = (
        "https://api.github.com/repos/{repo}/actions/runs"
        "?per_page=1&status=completed".format(repo=repo)
    )
    if branch:
        url += f"&branch={branch}"

    def _fetch() -> str | None:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        runs = resp.json().get("workflow_runs", [])
        return runs[0].get("conclusion") if runs else None

    conclusions = [_fetch() for _ in range(attempts)]
    if len(set(conclusions)) > 1:
        raise RuntimeError(
            f"Non-deterministic workflow conclusion for {repo}: {conclusions}"
        )
    return status_to_emoji(conclusions[0])


def _get_fetch_repo_status() -> Callable[..., str]:
    module = sys.modules.get("src.repo_status")
    if module is not None and hasattr(module, "fetch_repo_status"):
        return module.fetch_repo_status  # type: ignore[attr-defined]
    return fetch_repo_status


def update_readme(
    readme_path: Path,
    token: str | None = None,
    attempts: int = 2,
) -> None:
    """Update README with status emojis for related project repos."""

    lines = readme_path.read_text().splitlines()
    fetch = _get_fetch_repo_status()
    in_section = False
    for i, line in enumerate(lines):
        if line.strip() == "## Related Projects":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- "):
            match = GITHUB_RE.search(line)
            if match:
                repo = f"{match.group(1)}/{match.group(2)}"
                branch = match.group(3)
                emoji = fetch(repo, token, branch, attempts)
                lines[i] = re.sub(r"^(\-\s*)(?:[✅❌❓]\s*)*", r"\1", line)
                lines[i] = f"- {emoji} {lines[i][2:].lstrip()}"
    readme_path.write_text("\n".join(lines) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update README Related Projects status badges."
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path("README.md"),
        help="Path to README file to update.",
    )
    parser.add_argument(
        "--token",
        help="GitHub token. Defaults to GITHUB_TOKEN environment variable.",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=2,
        help="Number of API reads used to confirm workflow conclusions.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.attempts < 1:
        parser.error("--attempts must be >= 1")
    token = args.token or os.environ.get("GITHUB_TOKEN")
    update_readme(args.readme, token=token, attempts=args.attempts)


__all__ = [
    "build_parser",
    "fetch_repo_status",
    "main",
    "status_to_emoji",
    "update_readme",
]
