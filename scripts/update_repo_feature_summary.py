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

    basics = [
        [
            "Repo",
            "Branch",
            "Commit",
            "Trunk",
            "Stars",
            "Open Issues",
            "Last-Updated (UTC)",
        ]
    ]
    coverage = [
        [
            "Repo",
            "Coverage",
            "Patch",
            "Codecov",
            "Installer",
            "Last-Updated (UTC)",
        ]
    ]
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
            "Last-Updated (UTC)",
        ]
    ]
    pattern = [
        [
            "Repo",
            "Dark Patterns",
            "Bright Patterns",
            "Last-Updated (UTC)",
        ]
    ]

    for idx, info in enumerate(infos):
        link = f"[{info.name}](https://github.com/{info.name})"
        if idx == 0:
            link = f"**{link}**"
        commit = f"`{info.latest_commit}`" if info.latest_commit else "n/a"
        updated = info.commit_date or "n/a"
        trunk = "n/a"
        if info.trunk_green is True:
            trunk = "✅"
        elif info.trunk_green is False:
            trunk = "❌"
        basics.append(
            [
                link,
                info.branch,
                commit,
                trunk,
                str(info.stars),
                str(info.open_issues),
                updated,
            ]
        )

        cov = "❌"
        if info.coverage:
            if info.coverage == "100%":
                cov = "✔️"
            else:
                cov = info.coverage

        if info.patch_percent is None:
            patch = "—"
        else:
            emoji = "✅" if info.patch_percent >= 90 else "❌"
            patch = f"{emoji} ({info.patch_percent:.0f}%)"

        inst_map = {"uv": "🚀 uv", "partial": "🔶 partial"}
        inst = inst_map.get(info.installer, info.installer)
        codecov = "✅" if info.uses_codecov else "❌"
        coverage.append([link, cov, patch, codecov, inst, updated])

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
                updated,
            ]
        )

        pattern.append(
            [
                link,
                str(info.dark_pattern_count),
                str(info.bright_pattern_count),
                updated,
            ]
        )

    lines = [
        "## Basics",
        tabulate(basics[1:], headers=basics[0], tablefmt="github"),
    ]
    lines.extend(
        [
            "",
            "## Coverage & Installer",
            tabulate(coverage[1:], headers=coverage[0], tablefmt="github"),
        ]
    )
    lines.extend(
        [
            "",
            "## Policies & Automation",
            tabulate(policy[1:], headers=policy[0], tablefmt="github"),
        ]
    )
    lines.extend(
        [
            "",
            "## Dark & Bright Pattern Scan",
            tabulate(pattern[1:], headers=pattern[0], tablefmt="github"),
        ]
    )
    lines.append("")
    lines.append(
        "Legend: ✅ indicates the repo has adopted that feature from flywheel. 🚀 uv means only uv was found. "  # noqa: E501
        "🔶 partial signals a mix of uv and pip.\n"  # noqa: E501
        "Coverage percentages are parsed from Codecov when available. Codecov shows ✅ when a Codecov config or badge is present. "  # noqa: E501
        "Patch shows ✅ when diff coverage is at least 90% and ❌ otherwise. The commit column shows the short SHA of the latest default branch commit at crawl time.\n"  # noqa: E501
        "Last-Updated (UTC) records the date of that commit.\n"
        "Dark Patterns counts potential UX anti-patterns while Bright Patterns counts pro-user cues detected in code and docs."  # noqa: E501
    )
    lines.append(
        f"_Updated automatically: {date.today()}_",
    )

    content = "\n".join(["# Repo Feature Summary", "", *lines])
    if not content.endswith("\n"):
        content += "\n"
    args.out.write_text(content)


if __name__ == "__main__":
    main()
