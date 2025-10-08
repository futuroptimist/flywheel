"""Utilities to compare prompt docs between repositories."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, Sequence, Set, Tuple

REPO_HEADER_PATTERN = re.compile(r"\**\[([^\]]+)\]\([^)]*\)\**")
TABLE_ROW_PATTERN = re.compile(r"^\|.*\|")


def _normalize_repo(header_line: str) -> str:
    match = REPO_HEADER_PATTERN.search(header_line)
    if match:
        return match.group(1).strip()
    return header_line.strip().strip("*")


def _extract_table_rows(lines: Iterable[str]) -> Set[str]:
    rows: Set[str] = set()
    for line in lines:
        if not TABLE_ROW_PATTERN.match(line):
            break
        parts = [cell.strip() for cell in line.split("|")[1:-1]]
        if not parts or parts[0] in {"", "Path"}:
            continue
        if all(set(cell) <= {"-", ":"} for cell in parts):
            continue
        link = parts[0]
        rel = link.split("](")[0].lstrip("[")
        rows.add(rel)
    return rows


def _iter_sections(text: str) -> Iterable[tuple[str, list[str]]]:
    lines = text.splitlines()
    current_repo: str | None = None
    current_lines: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if current_repo is not None:
                yield current_repo, current_lines
            current_repo = _normalize_repo(line[3:].strip())
            current_lines = []
        elif current_repo is not None:
            current_lines.append(line)
    if current_repo is not None:
        yield current_repo, current_lines


def parse_prompt_summary(text: str) -> Dict[str, Set[str]]:
    summary: Dict[str, Set[str]] = {}
    for repo, lines in _iter_sections(text):
        table_started = False
        table_lines: list[str] = []
        for line in lines:
            if line.startswith("| "):
                table_started = True
                table_lines.append(line)
            elif table_started:
                break
        if table_lines:
            rows = _extract_table_rows(table_lines[2:])
            summary[repo] = rows
    return summary


def compare_prompt_sets(
    text: str,
    *,
    source_repo: str,
    target_repo: str,
) -> Tuple[Set[str], Set[str]]:
    summary = parse_prompt_summary(text)
    source = summary.get(source_repo, set())
    target = summary.get(target_repo, set())
    missing = source - target
    extra = target - source
    return missing, extra


def format_prompt_sync_report(
    missing: Set[str],
    extra: Set[str],
    *,
    source_repo: str,
    target_repo: str,
) -> str:
    lines: list[str] = []
    if not missing and not extra:
        lines.append(
            "No prompt differences between {} and {}.".format(
                source_repo,
                target_repo,
            )
        )
        return "\n".join(lines)
    if missing:
        lines.append(
            f"Prompts present in {source_repo} but missing from {target_repo}:"
        )
        for path in sorted(missing):
            lines.append(f"- {path}")
    if extra:
        lines.append(
            "Prompts present in {} but not in {}:".format(
                target_repo,
                source_repo,
            )
        )
        for path in sorted(extra):
            lines.append(f"- {path}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare prompt docs between repos.",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("docs/prompt-docs-summary.md"),
        help="Path to the generated prompt docs summary.",
    )
    parser.add_argument(
        "--source-repo",
        default="futuroptimist/flywheel",
        help="Repository treated as the source of truth.",
    )
    parser.add_argument(
        "--target-repo",
        default="futuroptimist/sugarkube",
        help="Repository checked for parity with the source.",
    )
    parser.add_argument(
        "--fail-on-diff",
        action="store_true",
        help="Exit with status 1 when differences are detected.",
    )
    args = parser.parse_args(argv)

    text = args.summary.read_text()
    missing, extra = compare_prompt_sets(
        text,
        source_repo=args.source_repo,
        target_repo=args.target_repo,
    )
    report = format_prompt_sync_report(
        missing,
        extra,
        source_repo=args.source_repo,
        target_repo=args.target_repo,
    )
    print(report)
    if args.fail_on_diff and (missing or extra):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
