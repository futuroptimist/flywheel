#!/usr/bin/env python3
"""Simple heuristic scanner for credential-like strings in Git diffs.

Usage:
    git diff --cached | ./scripts/scan-secrets.py

The script examines added lines in the diff and looks for common patterns such
as GitHub tokens, AWS access keys, Stripe secrets, Slack tokens, or private key
headers. Matches are masked in the output so that potential secrets are not
re-emitted verbatim. The process exits with status code ``1`` when a secret is
suspected so that calling workflows can block the commit.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Sequence

HUNK_RE = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")

# Patterns adapted from common secret scanners (GitHub, TruffleHog,
# detect-secrets) and tailored for Flywheel repos.
PATTERNS: Sequence[tuple[re.Pattern[str], str]] = (
    (re.compile(r"AKIA[0-9A-Z]{16}"), "Potential AWS access key"),
    (re.compile(r"ASIA[0-9A-Z]{16}"), "Potential temporary AWS access key"),
    (
        re.compile(
            r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}"  # noqa: E501
        ),
        "AWS secret key assignment",
    ),
    (
        re.compile(r"gh[pousr]_[A-Za-z0-9]{36}"),
        "Potential GitHub access token",
    ),
    (
        re.compile(r"sk_(?:live|test)_[A-Za-z0-9]{24,}"),
        "Potential Stripe secret key",
    ),
    (
        re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
        "Potential Slack token",
    ),
    (
        re.compile(r"-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----"),
        "Private key material",
    ),
    (
        re.compile(r"(?i)api_key\s*[:=]\s*['\"]?[A-Za-z0-9]{20,}"),
        "Generic API key assignment",
    ),
)


@dataclass
class Finding:
    path: str
    line: int
    match: str
    description: str

    @property
    def masked(self) -> str:
        token = self.match.strip()
        if len(token) <= 8:
            return token
        return f"{token[:4]}…{token[-4:]}"


def _normalize_path(raw: str) -> str:
    path = raw.strip()
    if path.startswith("b/"):
        path = path[2:]
    return path


def iter_added_lines(diff: str) -> Iterator[tuple[str, int, str]]:
    """Yield (path, line_number, text) triples for added lines in a diff."""

    current_path = ""
    current_line = 0
    for raw_line in diff.splitlines():
        if raw_line.startswith("+++ "):
            path = raw_line[4:]
            if path == "/dev/null":
                current_path = ""
            else:
                current_path = _normalize_path(path)
            current_line = 0
        elif raw_line.startswith("@@"):
            match = HUNK_RE.match(raw_line)
            if match:
                current_line = int(match.group(1))
        elif raw_line.startswith("+") and not raw_line.startswith("+++"):
            if current_path and current_line:
                yield current_path, current_line, raw_line[1:]
            current_line += 1
        elif raw_line.startswith(" ") and current_line:
            current_line += 1
        elif raw_line.startswith("-"):
            continue


def scan_lines(lines: Iterable[tuple[str, int, str]]) -> List[Finding]:
    findings: List[Finding] = []
    for path, lineno, text in lines:
        for pattern, description in PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append(
                    Finding(
                        path=path,
                        line=lineno,
                        match=match.group(0),
                        description=description,
                    )
                )
                break
    return findings


def scan_diff(diff: str) -> List[Finding]:
    return scan_lines(iter_added_lines(diff))


def _format_findings(findings: Sequence[Finding]) -> str:
    lines = ["Potential secrets detected:"]
    for finding in findings:
        lines.append(
            f" - {finding.path}:{finding.line}: {finding.description}"
            f" ({finding.masked})"
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    diff = sys.stdin.read()
    if not diff.strip():
        print("No input provided on stdin; pipe a git diff into this script.")
        return 0
    findings = scan_diff(diff)
    if not findings:
        print("No secrets detected.")
        return 0
    print(_format_findings(findings))
    return 1


if __name__ == "__main__":  # pragma: no cover - exercised via CLI
    sys.exit(main())
