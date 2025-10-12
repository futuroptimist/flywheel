"""Minimal example showing how to call the flywheel CLI from Python."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def generate_prompt(argv: Sequence[str] | None = None) -> str:
    """Return the Codex automation prompt for the target repository."""

    from flywheel.__main__ import build_parser

    parser = build_parser()
    cli_args = list(argv) if argv is not None else ["prompt", "."]
    parsed = parser.parse_args(cli_args)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        parsed.func(parsed)
    return buffer.getvalue()


def main(argv: Sequence[str] | None = None) -> None:
    """Print the automation prompt for ``repo`` (defaults to repo root)."""

    args = list(argv) if argv is not None else sys.argv[1:]
    if args:
        repo_path = Path(args[0]).resolve()
    else:
        repo_path = REPO_ROOT
    prompt = generate_prompt(["prompt", str(repo_path)])
    # ``prompt`` already ends with a newline; avoid double spacing when
    # printing the result.
    print(prompt, end="" if prompt.endswith("\n") else "\n")


if __name__ == "__main__":  # pragma: no cover - exercised via tests
    main()
