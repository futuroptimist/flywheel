import argparse
import shutil
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


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.read_bytes() == src.read_bytes():
        return
    shutil.copy2(src, dest)


def inject_dev(target: Path) -> None:
    for rel in WORKFLOW_FILES + OTHER_FILES:
        copy_file(ROOT / rel, target / rel)


def audit_repo(target: Path) -> None:
    missing = []
    for rel in WORKFLOW_FILES + OTHER_FILES:
        if not (target / rel).exists():
            missing.append(rel)
    if missing:
        print("Missing dev tooling files:")
        for rel in missing:
            print(f" - {rel}")
    else:
        print("All dev tooling files present.")


def prompt_bool(question: str, default: bool) -> bool:
    suffix = "Y/n" if default else "y/N"
    resp = input(f"{question} [{suffix}]: ").strip().lower()
    if not resp:
        return default
    return resp.startswith("y")


def init_repo(args: argparse.Namespace) -> None:
    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)

    language = args.language
    if not args.yes:
        resp = input(f"Language [python/javascript] ({language}): ").strip()
        if resp:
            language = resp

    if language == "python":
        for rel in PY_FILES:  # pragma: no cover
            copy_file(ROOT / rel, target / Path(rel).name)  # pragma: no cover
    elif language == "javascript":
        for rel in JS_FILES:  # pragma: no cover
            copy_file(ROOT / rel, target / Path(rel).name)  # pragma: no cover

    save_dev = args.save_dev
    if not args.yes and not save_dev:
        save_dev = prompt_bool("Inject dev tooling?", False)

    if save_dev:
        inject_dev(target)


PROMPT_TMPL = """# Purpose
Assist developers working on this repository.

# Context
{snippet}

# Request
Provide high level guidance or next steps.
"""


def prompt(args: argparse.Namespace) -> None:
    repo = Path(args.path).resolve()
    readme = repo / "README.md"
    if readme.exists():
        snippet = "\n".join(readme.read_text().splitlines()[:20])
    else:
        snippet = "No README found."  # pragma: no cover
    print(PROMPT_TMPL.format(snippet=snippet))


def crawl(args: argparse.Namespace) -> None:
    crawler = RepoCrawler(args.repos, token=args.token)
    md = crawler.generate_summary()
    Path(args.output).write_text(md)


def build_parser() -> argparse.ArgumentParser:
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
    p_init.set_defaults(func=init_repo)

    p_update = sub.add_parser("update", help="update dev tooling")
    p_update.add_argument("path", help="target repository path")
    p_update.add_argument("--save-dev", action="store_true", default=True)
    p_update.set_defaults(func=lambda a: inject_dev(Path(a.path)))

    p_audit = sub.add_parser("audit", help="check for missing tooling")
    p_audit.add_argument("path", help="repository path")
    p_audit.set_defaults(func=lambda a: audit_repo(Path(a.path)))

    p_prompt = sub.add_parser("prompt", help="generate Codex prompt")
    p_prompt.add_argument(
        "path",
        nargs="?",
        default=".",
        help="repository path",
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
    p_crawl.set_defaults(func=crawl)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
