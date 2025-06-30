#!/usr/bin/env python3
"""Flywheel CLI for initializing repos and generating prompts."""
import argparse
import shutil
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent


def copy_template(target: Path, template_dir: Path) -> None:
    for src in template_dir.rglob("*"):
        rel = src.relative_to(template_dir)
        dst = target / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy2(src, dst)


def init_repo(args) -> None:
    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)
    template_dir = REPO_ROOT / "templates" / args.template
    copy_template(target, template_dir)

    if args.save_dev:
        copy_template(target, REPO_ROOT / "templates" / "dev")


def update_repo(args) -> None:
    init_repo(args)


def audit_repo(args) -> None:
    required = [
        ".github/workflows/ci.yml",
        "dependabot.yml",
    ]
    missing = [r for r in required if not (Path(args.path) / r).exists()]
    if missing:
        print("Missing files: " + ", ".join(missing))
    else:
        print("All required files present")


def generate_prompt(args) -> None:
    repo = Path(args.path)
    readme = repo / "README.md"
    snippet = readme.read_text()[:200] if readme.exists() else ""
    prompt = textwrap.dedent(
        f"""
        ## Repo Prompt

        Repository path: {repo.resolve()}

        README Preview:\n{snippet}
        """
    )
    print(prompt.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="flywheel template manager")
    sub = parser.add_subparsers(dest="cmd")
    base = argparse.ArgumentParser(add_help=False)
    base.add_argument("path", nargs="?", default=".", help="target repo path")
    base.add_argument(
        "--save-dev",
        action="store_true",
        help="include ESLint, CI, tests, and release helpers",
    )

    p_init = sub.add_parser("init", parents=[base], help="initialize repo")
    p_init.set_defaults(func=init_repo)

    p_update = sub.add_parser("update", parents=[base], help="update repo")
    p_update.set_defaults(func=update_repo)

    p_audit = sub.add_parser("audit", parents=[base], help="check repo state")
    p_audit.set_defaults(func=audit_repo)

    p_prompt = sub.add_parser(
        "prompt", parents=[base], help="generate Codex-friendly repo prompt"
    )
    p_prompt.set_defaults(func=generate_prompt)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return

    # fmt: off
    if (
        sys.stdin.isatty()
        and not args.save_dev
        and args.cmd in {"init", "update"}
    ):
        ans = input("Include dev tooling (ESLint/CI etc)? [y/N] ")
        if ans.lower().startswith("y"):
            args.save_dev = True
    # fmt: on

    if (Path(args.path) / "package.json").exists():
        args.template = "javascript"
    else:
        args.template = "python"
    args.func(args)


if __name__ == "__main__":
    main()
