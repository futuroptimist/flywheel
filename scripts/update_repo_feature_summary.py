#!/usr/bin/env python
"""Generate the repo feature summary from a list of repos."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import List

from tabulate import tabulate

from flywheel.repocrawler import RepoCrawler


def load_repos(path: Path) -> List[str]:
    lines = path.read_text().splitlines()
    return [line.strip() for line in lines if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-from", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--token")
    args = parser.parse_args()

    repos = load_repos(args.repos_from)
    crawler = RepoCrawler(repos, token=args.token)
    infos = crawler.crawl()

    basics = [["Repo", "Branch", "Commit"]]
    coverage = [["Repo", "Coverage", "Patch", "Installer", "Codecov"]]
    policy = [
        [
            "Repo",
            "License",
            "CI",
            "Workflows",
            "AGENTS.md",
            "Code of Conduct",
            "Contributing",
            "Pre-commit",
        ]
    ]

    for idx, info in enumerate(infos):
        link = f"[{info.name}](https://github.com/{info.name})"
        if idx == 0:
            link = f"**{link}**"
        commit = f"`{info.latest_commit}`" if info.latest_commit else "n/a"
        basics.append([link, info.branch, commit])

        cov = "❌"
        if info.coverage:
            cov = f"✅ ({info.coverage})"

        if info.patch_percent is None:
            patch = "—"
        else:
            emoji = "✅" if info.patch_percent >= 90 else "❌"
            patch = f"{emoji} ({info.patch_percent:.0f}%)"

        inst_map = {"uv": "🚀 uv", "partial": "🔶 partial"}
        inst = inst_map.get(info.installer, info.installer)
        coverage.append(
            [
                link,
                cov,
                patch,
                inst,
                "✅" if info.uses_codecov else "❌",
            ]
        )

        policy.append(
            [
                link,
                "✅" if info.has_license else "❌",
                "✅" if info.workflow_count > 0 else "❌",
                str(info.workflow_count),
                "✅" if info.has_agents else "❌",
                "✅" if info.has_coc else "❌",
                "✅" if info.has_contributing else "❌",
                "✅" if info.has_precommit else "❌",
            ]
        )

    lines = [
        "## Basics",
        tabulate(
            basics[1:],
            headers=basics[0],
            tablefmt="github",
            maxcolwidths=[None] * len(basics[0]),
        ),
    ]
    lines.extend(
        [
            "",
            "## Coverage & Installer",
            tabulate(
                coverage[1:],
                headers=coverage[0],
                tablefmt="github",
                maxcolwidths=[None] * len(coverage[0]),
            ),
        ]
    )
    lines.extend(
        [
            "",
            "## Policies & Automation",
            tabulate(
                policy[1:],
                headers=policy[0],
                tablefmt="github",
                maxcolwidths=[None] * len(policy[0]),
            ),
        ]
    )
    lines.append("")
    lines.append(
        "Legend: ✅ indicates the repo has adopted that feature from flywheel. "
        "🚀 uv means only uv was found. 🔶 partial signals a mix of uv and pip. "
        "Coverage percentages are parsed from Codecov when available. The "
        "Codecov column marks repos using Codecov for reporting. Patch shows "
        "✅ when diff coverage is at least 90% and ❌ otherwise. The commit "
        "column shows the short SHA of the latest default branch commit at "
        "crawl time."
    )
    lines.append(
        f"_Updated automatically: {date.today()}_",
    )

    content = "\n".join(["# Repo Feature Summary", "", *lines])
    args.out.write_text(content)


if __name__ == "__main__":
    main()
