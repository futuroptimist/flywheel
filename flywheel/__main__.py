import argparse
import json
import os
import shutil
from collections import Counter
from pathlib import Path
from typing import Sequence

import yaml

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
    "eslint.config.mjs",
    ".prettierrc",
    ".pre-commit-config.yaml",
    "scripts/checks.sh",
]

PY_FILES = [
    "templates/python/pyproject.toml",
    "templates/python/requirements.txt",
]

JS_FILES = ["templates/javascript/package.json"]

PROMPT_DOCS = [Path("docs/prompts/codex/automation.md")]

SPIN_SKIP_DIRECTORIES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".svn",
    ".tox",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
    ".venv",
}
SPIN_ALLOWED_HIDDEN = {".github"}
CODE_FILE_SUFFIXES = {
    ".cjs",
    ".js",
    ".jsx",
    ".mjs",
    ".py",
    ".ts",
    ".tsx",
}
LANGUAGE_BY_SUFFIX = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".cjs": "JavaScript",
    ".mjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
}
TEST_FILENAME_SUFFIXES = (
    "_test.py",
    "_test.ts",
    "_test.tsx",
    "_test.js",
    "_test.jsx",
    ".test.py",
    ".test.ts",
    ".test.tsx",
    ".test.js",
    ".test.jsx",
    ".spec.py",
    ".spec.ts",
    ".spec.tsx",
    ".spec.js",
    ".spec.jsx",
)

NODE_LOCKFILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "bun.lockb",
}
PIPFILE_LOCK = "Pipfile.lock"


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.read_bytes() == src.read_bytes():
        return
    shutil.copy2(src, dest)


def summarize_repo_root(repo: Path, limit: int = 10) -> str:
    """Return a comma-separated snapshot of top-level entries in ``repo``."""

    if not repo.exists():
        return "(directory not found)"
    if not repo.is_dir():
        return "(path is not a directory)"

    try:
        children = sorted(repo.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        return "(unable to list repository contents)"

    entries: list[str] = []
    for child in children:
        name = child.name
        if name.startswith("."):
            continue
        try:
            if child.is_dir():
                entries.append(f"{name}/")
            elif child.is_symlink():
                entries.append(f"{name}@")
            elif child.is_file():
                entries.append(name)
            else:
                entries.append(name)
        except OSError:
            entries.append(name)

    if not entries:
        return "(no non-hidden files found)"

    if len(entries) > limit:
        remaining = len(entries) - limit
        entries = entries[:limit] + [f"… (+{remaining} more)"]

    return ", ".join(entries)


def inject_dev(target: Path) -> None:
    for rel in WORKFLOW_FILES + OTHER_FILES:
        copy_file(ROOT / rel, target / rel)


def sync_prompt_docs(
    target: Path, prompt_paths: Sequence[Path] | None = None
) -> list[Path]:
    """Copy prompt docs into ``target`` and return updated paths."""

    resolved_target = target.resolve()
    resolved_target.mkdir(parents=True, exist_ok=True)
    prompts = [Path(rel) for rel in (prompt_paths or PROMPT_DOCS)]
    updated: list[Path] = []
    for rel in prompts:
        src = ROOT / rel
        if not src.exists():
            raise FileNotFoundError(f"Prompt file not found: {src}")
        dest = resolved_target / rel
        src_bytes = src.read_bytes()
        dest_bytes = dest.read_bytes() if dest.exists() else None
        should_copy = dest_bytes != src_bytes
        copy_file(src, dest)
        if should_copy:
            updated.append(dest)
    return updated


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
        resp = input(
            f"Language [python/javascript] ({language}): "
        ).strip()  # pragma: no cover
        if resp:  # pragma: no cover
            language = resp  # pragma: no cover

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


def update_repo(args: argparse.Namespace) -> None:
    target = Path(args.path).resolve()

    save_dev = args.save_dev
    if save_dev is None:
        if args.yes:
            save_dev = True
        else:
            save_dev = prompt_bool("Inject dev tooling?", True)

    if save_dev:
        inject_dev(target)


PROMPT_TMPL = """# Purpose
Assist developers working on this repository.

# Context
{snippet}

# Repo Snapshot
Top-level entries: {snapshot}

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
    snapshot = summarize_repo_root(repo)
    # Avoid ``str.format`` so braces in README snippets don't break formatting
    prompt_text = PROMPT_TMPL.replace("{snippet}", snippet).replace(
        "{snapshot}", snapshot
    )
    print(prompt_text)


def _iter_project_files(root: Path) -> list[Path]:
    files: list[Path] = []
    allowed_hidden = SPIN_ALLOWED_HIDDEN
    skip_dirs = SPIN_SKIP_DIRECTORIES
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_parts = current.relative_to(root).parts if current != root else ()
        if any(part in skip_dirs for part in rel_parts):
            dirnames[:] = []
            continue
        pruned: list[str] = []
        for name in dirnames:
            if name in skip_dirs:
                continue
            if name.startswith(".") and name not in allowed_hidden:
                continue
            pruned.append(name)
        dirnames[:] = pruned
        for filename in filenames:
            if filename.startswith(".") and current.name not in allowed_hidden:
                continue
            files.append(current / filename)
    return files


def _has_ci_workflows(root: Path) -> bool:
    workflows = root / ".github" / "workflows"
    if not workflows.exists():
        return False
    for path in workflows.iterdir():
        if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}:
            return True
    return False


def _detect_tests(root: Path, files: Sequence[Path]) -> bool:
    tests_dir = root / "tests"
    if tests_dir.exists():
        for path in tests_dir.rglob("*"):
            if path.is_file():
                return True
    for path in files:
        suffix = path.suffix.lower()
        if suffix not in CODE_FILE_SUFFIXES:
            continue
        name = path.name.lower()
        if name.startswith("test_"):
            return True
        if any(name.endswith(sfx) for sfx in TEST_FILENAME_SUFFIXES):
            return True
        parent_parts = [part.lower() for part in path.parts[:-1]]
        if any(part in {"tests", "__tests__"} for part in parent_parts):
            return True
    return False


def _summarize_language_mix(files: Sequence[Path]) -> list[dict[str, object]]:
    counts: Counter[str] = Counter()
    for path in files:
        language = LANGUAGE_BY_SUFFIX.get(path.suffix.lower())
        if language:
            counts[language] += 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    top_languages: list[dict[str, object]] = []
    for language, count in ordered[:5]:
        top_languages.append({"language": language, "count": count})
    return top_languages


def _analyze_dependency_health(
    root: Path,
    files: Sequence[Path],
) -> dict[str, object]:
    manifests: list[str] = []
    lockfiles: list[str] = []
    missing: list[str] = []

    files_by_dir: dict[Path, set[str]] = {}
    for path in files:
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path
        directory = rel.parent
        entries = files_by_dir.setdefault(directory, set())
        entries.add(rel.name)

    for directory, names in files_by_dir.items():
        if "package.json" in names:
            manifest_path = (directory / "package.json").as_posix()
            manifests.append(manifest_path)
            lock_found = False
            for candidate in NODE_LOCKFILES:
                if candidate in names:
                    lock_found = True
                    lockfiles.append((directory / candidate).as_posix())
            if not lock_found:
                missing.append(manifest_path)
        if "Pipfile" in names:
            manifest_path = (directory / "Pipfile").as_posix()
            manifests.append(manifest_path)
            lock_path = (directory / PIPFILE_LOCK).as_posix()
            if PIPFILE_LOCK in names:
                lockfiles.append(lock_path)
            else:
                missing.append(manifest_path)

    manifests = sorted(set(manifests))
    lockfiles = sorted(set(lockfiles))
    missing = sorted(set(missing))
    status = "ok" if not missing else "lockfile-missing"
    return {
        "manifests": manifests,
        "lockfiles": lockfiles,
        "missing_lockfiles": missing,
        "status": status,
    }


def _analyze_repository(
    root: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    files = _iter_project_files(root)
    ext_counts = Counter((path.suffix.lower() or "<none>") for path in files)
    top_extensions = [
        {"extension": ext, "count": count}
        for ext, count in sorted(
            ext_counts.items(), key=lambda item: (-item[1], item[0])
        )[:5]
    ]
    has_readme = (root / "README.md").exists()
    has_ci = _has_ci_workflows(root)
    has_tests = _detect_tests(root, files)
    language_mix = _summarize_language_mix(files)
    dependency_health = _analyze_dependency_health(root, files)
    stats: dict[str, object] = {
        "total_files": len(files),
        "top_extensions": top_extensions,
        "has_readme": has_readme,
        "has_tests": has_tests,
        "has_ci_workflows": has_ci,
        "language_mix": language_mix,
        "dependency_health": dependency_health,
    }
    suggestions: list[dict[str, object]] = []
    if not has_readme:
        suggestions.append(
            {
                "id": "add-readme",
                "category": "docs",
                "title": "Add README.md",
                "description": (
                    "Document the project purpose, setup instructions, and"
                    " test commands so new contributors ramp up quickly."
                ),
                "impact": "medium",
                "files": ["README.md"],
            }
        )
    if not has_ci:
        suggestions.append(
            {
                "id": "configure-ci",
                "category": "chore",
                "title": "Add CI workflows",
                "description": (
                    "Add GitHub Actions workflows "
                    "under .github/workflows "
                    "so lint, test, and docs jobs run on every push."
                ),
                "impact": "high",
                "files": [".github/workflows/"],
            }
        )
    if not has_tests:
        suggestions.append(
            {
                "id": "add-tests",
                "category": "fix",
                "title": "Bootstrap an automated test suite",
                "description": (
                    "Create a tests/ directory or add language-appropriate"
                    " test files to prevent regressions."
                ),
                "impact": "high",
                "files": ["tests/"],
            }
        )
    if dependency_health["missing_lockfiles"]:
        suggestions.append(
            {
                "id": "commit-lockfiles",
                "title": "Commit dependency lockfiles",
                "description": (
                    "Generate and commit dependency lockfiles (for example, "
                    "package-lock.json or Pipfile.lock) so installs stay "
                    "reproducible across environments."
                ),
                "impact": "medium",
                "files": dependency_health["missing_lockfiles"],
            }
        )
    suggestions.sort(key=lambda item: item["id"])
    return stats, suggestions


def spin(args: argparse.Namespace) -> None:
    target = Path(args.path or ".").resolve()
    if not target.exists():
        raise SystemExit(f"Target path not found: {target}")
    if not target.is_dir():
        raise SystemExit(f"Target path is not a directory: {target}")
    if not args.dry_run:
        msg = "Only --dry-run mode is supported; re-run with --dry-run."
        raise SystemExit(msg)
    stats, suggestions = _analyze_repository(target)
    result = {
        "target": str(target),
        "mode": "dry-run",
        "stats": stats,
        "suggestions": suggestions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


def crawl(args: argparse.Namespace) -> None:
    cli_repos = list(args.repos)
    repo_file = Path(args.repos_file)
    combined: list[str] = []
    if repo_file.exists():
        lines = repo_file.read_text().splitlines()
        file_repos = [line.strip() for line in lines if line.strip()]
        combined.extend(file_repos)
    combined.extend(cli_repos)
    repos: list[str] = []
    index_by_repo: dict[str, int] = {}
    for raw_spec in combined:
        spec = raw_spec.strip()
        if not spec:
            continue
        base = spec.split("@", 1)[0].strip()
        if not base:
            continue
        if base in index_by_repo:
            repos[index_by_repo[base]] = spec
        else:
            index_by_repo[base] = len(repos)
            repos.append(spec)
    if not repos:
        raise SystemExit("No repositories provided")
    crawler = RepoCrawler(repos, token=args.token)
    md = crawler.generate_summary()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)


def runbook(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"Runbook file not found: {path}")
    data = yaml.safe_load(path.read_text()) or {}
    workflow = data.get("workflow", [])
    for stage in workflow:
        if isinstance(stage, dict):
            name = stage.get("stage", "")
            tasks = stage.get("tasks", [])
        else:
            name = str(stage)
            tasks = []
        if name:
            print(f"Stage: {name}")
        for task in tasks:
            if isinstance(task, dict):
                task_id = task.get("id")
                desc = task.get("description", "")
                if task_id and desc:
                    print(f"- {task_id}: {desc}")
                elif task_id:
                    print(f"- {task_id}")
                elif desc:
                    print(f"- {desc}")
            else:
                print(f"- {task}")
        print()


def sync_prompts_cli(args: argparse.Namespace) -> None:
    target = Path(args.target).resolve()
    prompt_paths = None
    if args.files:
        prompt_paths = [Path(rel) for rel in args.files]
    updated = sync_prompt_docs(target, prompt_paths=prompt_paths)
    if updated:
        for path in updated:
            print(f"Updated {path}")
    else:
        print("Prompt docs already up to date.")


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
    p_update.add_argument(
        "--save-dev",
        action="store_true",
        dest="save_dev",
        help="inject dev tooling",
    )
    p_update.add_argument(
        "--no-save-dev",
        action="store_false",
        dest="save_dev",
        help="skip dev tooling",
    )
    p_update.add_argument(
        "--yes",
        action="store_true",
        help="run non-interactively",
    )
    p_update.set_defaults(save_dev=None, func=update_repo)

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

    p_spin = sub.add_parser(
        "spin",
        help="analyze a repository and suggest improvements",
    )
    p_spin.add_argument(
        "path",
        nargs="?",
        default=".",
        help="repository path to analyze",
    )
    p_spin.add_argument(
        "--dry-run",
        action="store_true",
        help="generate heuristic suggestions without applying changes",
    )
    p_spin.set_defaults(func=spin)

    p_crawl = sub.add_parser("crawl", help="generate repo feature summary")
    p_crawl.add_argument("repos", nargs="*", help="repos in owner/name form")
    p_crawl.add_argument(
        "--repos-file",
        default="docs/repo_list.txt",
        help="path to file listing repos",
    )
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

    p_runbook = sub.add_parser("runbook", help="print runbook checklist")
    p_runbook.add_argument(
        "--file",
        default=ROOT / "runbook.yml",
        type=Path,
        help="path to runbook YAML file",
    )
    p_runbook.set_defaults(func=runbook)

    p_sync = sub.add_parser(
        "sync-prompts",
        help="sync prompt docs to target repo",
    )
    p_sync.add_argument("target", help="target repository path")
    p_sync.add_argument(
        "--files",
        nargs="+",
        type=Path,
        help="prompt doc paths relative to the repository root",
    )
    p_sync.set_defaults(func=sync_prompts_cli, files=None)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
