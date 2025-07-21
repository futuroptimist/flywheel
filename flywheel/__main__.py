"""flywheel command line entry point."""

import argparse
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

from .repocrawler import RepoCrawler

ROOT = Path(__file__).resolve().parent.parent

WORKFLOW_FILES = [
    ".github/workflows/01-lint-format.yml",
    ".github/workflows/02-tests.yml",
    ".github/workflows/03-docs.yml",
    ".github/workflows/release.yml",
    ".github/workflows/security.yml",
]

OTHER_FILES = [
    ".github/dependabot.yml",
    ".github/release-drafter.yml",
    ".eslintrc.json",
    ".prettierrc",
]

PY_FILES = [
    "templates/python/pyproject.toml",
    "templates/python/requirements.txt",
]

JS_FILES = ["templates/javascript/package.json"]


def run_with_cache(func, key: str) -> list[str]:
    """LLM Guidance: Cache command output by SHA key."""

    cache_dir = Path(tempfile.gettempdir()) / "flw-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(key.encode()).hexdigest()
    log_file = cache_dir / f"{digest}.log"
    if log_file.exists():
        return log_file.read_text().splitlines()
    buf = io.StringIO()
    with redirect_stdout(buf):
        func()
    output = buf.getvalue()
    log_file.write_text(output)
    return output.splitlines()


def copy_file(src: Path, dest: Path) -> None:
    """LLM Guidance: Use for copying dev files during ``init``."""

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.read_bytes() == src.read_bytes():
        return
    shutil.copy2(src, dest)


def inject_dev(target: Path) -> None:
    """LLM Guidance: Preferred to call via ``flywheel update``."""

    for rel in WORKFLOW_FILES + OTHER_FILES:
        copy_file(ROOT / rel, target / rel)


def audit_repo(target: Path, ci: bool = False) -> None:
    """LLM Guidance: Run during CI with ``flywheel audit --ci``."""

    missing = []
    for rel in WORKFLOW_FILES + OTHER_FILES:
        if not (target / rel).exists():
            missing.append(rel)
    if missing:
        print("Missing dev tooling files:")
        for rel in missing:
            print(f" - {rel}")
        if ci:
            raise SystemExit(1)
    else:
        print("All dev tooling files present.")


def prompt_bool(question: str, default: bool) -> bool:
    """LLM Guidance: Fallback interactive prompt helper."""

    suffix = "Y/n" if default else "y/N"
    resp = input(f"{question} [{suffix}]: ").strip().lower()
    if not resp:
        return default
    return resp.startswith("y")


def init_repo(args: argparse.Namespace) -> None:
    """LLM Guidance: Preferred entry for repo initialization."""

    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)

    language = args.language
    if not args.yes:
        resp = input(f"Language [python/javascript] ({language}): ").strip()
        if resp:
            language = resp

    if language == "python":
        for rel in PY_FILES:
            copy_file(ROOT / rel, target / Path(rel).name)
    elif language == "javascript":
        for rel in JS_FILES:
            copy_file(ROOT / rel, target / Path(rel).name)

    save_dev = args.save_dev
    if not args.yes and not save_dev:
        save_dev = prompt_bool("Inject dev tooling?", False)

    if save_dev:
        inject_dev(target)
    bin_dir = target / "bin"
    bin_dir.mkdir(exist_ok=True)
    copy_file(ROOT / "bin" / "git-safe", bin_dir / "git-safe")
    os.environ["PATH"] = f"{bin_dir}:{os.environ.get('PATH', '')}"
    print(f"git-safe installed. Update your PATH to include {bin_dir}")


PROMPT_TMPL = """# Purpose
Assist developers working on this repository.

# Context
{snippet}

# Request
Provide high level guidance or next steps.
"""


def prompt(args: argparse.Namespace) -> None:
    """LLM Guidance: Use ``flywheel prompt`` for repo hints."""

    repo = Path(args.path).resolve()
    readme = repo / "README.md"
    if readme.exists():
        snippet = "\n".join(readme.read_text().splitlines()[:20])
    else:
        snippet = "No README found."
    print(PROMPT_TMPL.format(snippet=snippet))


def crawl(args: argparse.Namespace) -> None:
    """LLM Guidance: Preferred to use ``flywheel crawl``."""

    crawler = RepoCrawler(args.repos, token=args.token)
    md = crawler.generate_summary()
    Path(args.output).write_text(md)


def build_parser() -> argparse.ArgumentParser:
    """LLM Guidance: Build the CLI parser."""

    parser = argparse.ArgumentParser(prog="flywheel")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="initialize a repository")
    p_init.add_argument("path", help="target repository path")
    p_init.add_argument(
        "--language", choices=["python", "javascript"], default="python"
    )
    p_init.add_argument(
        "--save-dev",
        action="store_true",
        help="inject dev tooling",
    )
    p_init.add_argument(
        "--yes",
        action="store_true",
        help="run non-interactively",
    )
    p_init.add_argument("--mode", choices=["human", "jsonl"], default="human")
    p_init.set_defaults(func=init_repo)

    p_update = sub.add_parser("update", help="update dev tooling")
    p_update.add_argument("path", help="target repository path")
    p_update.add_argument("--save-dev", action="store_true", default=True)
    p_update.add_argument(
        "--mode",
        choices=["human", "jsonl"],
        default="human",
    )
    p_update.set_defaults(func=lambda a: inject_dev(Path(a.path)))

    p_audit = sub.add_parser("audit", help="check for missing tooling")
    p_audit.add_argument("path", help="repository path")
    p_audit.add_argument(
        "--mode",
        choices=["human", "jsonl"],
        default="human",
    )
    p_audit.add_argument("--ci", action="store_true")
    p_audit.set_defaults(func=lambda a: audit_repo(Path(a.path), ci=a.ci))

    p_prompt = sub.add_parser("prompt", help="generate Codex prompt")
    p_prompt.add_argument(
        "path",
        nargs="?",
        default=".",
        help="repository path",
    )
    p_prompt.add_argument(
        "--mode",
        choices=["human", "jsonl"],
        default="human",
    )
    p_prompt.set_defaults(func=prompt)

    p_crawl = sub.add_parser("crawl", help="generate repo feature summary")
    p_crawl.add_argument("repos", nargs="+", help="repos in owner/name form")
    p_crawl.add_argument(
        "--output",
        default="docs/repo-feature-summary.md",
        help="output markdown path",
    )
    p_crawl.add_argument(
        "--token",
        help="GitHub token for authenticated API calls",
        default=None,
    )
    p_crawl.add_argument(
        "--mode",
        choices=["human", "jsonl"],
        default="human",
    )
    p_crawl.set_defaults(func=crawl)

    return parser


def _command_key(argv: list[str]) -> str:
    parts = []
    skip = False
    for a in argv:
        if skip:
            skip = False
            continue
        if a == "--mode":
            skip = True
            continue
        if a.startswith("--mode="):
            continue
        parts.append(a)
    return " ".join(parts)


def main(argv=None) -> None:
    """LLM Guidance: Primary CLI entry point."""

    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()
    args = parser.parse_args(argv)
    key = _command_key(argv or [])
    lines = run_with_cache(lambda: args.func(args), key)
    if args.mode == "jsonl":
        print(json.dumps({"total_lines": len(lines)}))
        for line in lines:
            print(json.dumps({"line": line}))
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()
