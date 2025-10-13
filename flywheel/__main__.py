import argparse
import json
import math
import os
import shutil
import sys
import textwrap
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

import yaml

from . import status_helper as repo_status
from .repocrawler import RepoCrawler

ROOT = Path(__file__).resolve().parent.parent

CONFIG_ENV_VAR = "FLYWHEEL_CONFIG_DIR"
CONFIG_FILENAME = "config.json"
DEFAULT_CONFIG_DIR = Path.home() / ".config" / "flywheel"
TELEMETRY_REMINDER = (
    "Telemetry preference not set; run `flywheel config telemetry "
    "--set off|on|full` to choose."
)

HELP_EPILOG = textwrap.dedent(
    """\
    Examples:
      flywheel init ./project --language python --save-dev --yes
      flywheel spin --dry-run path/to/repo --format table
    """
)


def _config_dir() -> Path:
    override = os.environ.get(CONFIG_ENV_VAR)
    if override:
        return Path(override).expanduser()
    return DEFAULT_CONFIG_DIR


def _config_path() -> Path:
    return _config_dir() / CONFIG_FILENAME


def load_config() -> dict[str, object]:
    path = _config_path()
    if not path.exists():
        return {}
    try:
        text = path.read_text()
    except OSError:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    if isinstance(data, dict):
        return data
    return {}


def save_config(data: dict[str, object]) -> Path:
    path = _config_path()
    directory = path.parent
    directory.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return path


def update_related_status(args: argparse.Namespace) -> None:
    attempts = getattr(args, "attempts", 2)
    if attempts < 1:
        raise SystemExit("--attempts must be >= 1")
    readme = Path(args.readme)
    token = args.token or os.environ.get("GITHUB_TOKEN")
    repo_status.update_readme(readme, token=token, attempts=attempts)


def telemetry_config(args: argparse.Namespace) -> None:
    config = load_config()
    mode = args.set
    if mode:
        config["telemetry"] = mode
        save_config(config)
        print(f"Telemetry preference set to {mode}.")
        return
    current = str(config.get("telemetry", "ask"))
    print(f"Telemetry preference: {current}")


def _automation_context() -> bool:
    """Return ``True`` when running in a known non-interactive environment."""

    for name in ("CI", "GITHUB_ACTIONS"):
        raw = os.environ.get(name)
        if not raw:
            continue
        if raw.lower() in {"0", "false", "no"}:
            continue
        return True
    return False


def _is_interactive() -> bool:
    """Return ``True`` when stdin/stdout are attached to a TTY."""

    try:
        stdin_tty = sys.stdin.isatty()
        stdout_tty = sys.stdout.isatty()
    except Exception:  # pragma: no cover - extremely unlikely
        return False
    return bool(stdin_tty and stdout_tty)


def _prompt_for_telemetry() -> None:
    """Prompt once for telemetry opt-in and persist the choice."""

    config = load_config()
    if "telemetry" in config:
        return
    if _automation_context() or not _is_interactive():
        print(TELEMETRY_REMINDER, file=sys.stderr)
        return

    prompt = (
        "Share anonymized telemetry (command usage and exit codes) to help "
        "improve flywheel? [y/N]: "
    )
    while True:
        try:
            response = input(prompt)
        except EOFError:
            print(TELEMETRY_REMINDER, file=sys.stderr)
            return
        response = response.strip().lower()
        if response in {"y", "yes"}:
            choice = "on"
            break
        if response in {"n", "no", ""}:
            choice = "off"
            break
        print("Please respond with 'y' or 'n'.")

    config["telemetry"] = choice
    save_config(config)
    if choice == "on":
        confirmation = (
            "Telemetry enabled. Run `flywheel config telemetry "
            "--set off|full` to update the preference."
        )
    else:
        confirmation = (
            "Telemetry disabled. Run `flywheel config telemetry "
            "--set on|full` to enable it later."
        )
    print(confirmation)


def maybe_prompt_for_telemetry(args: argparse.Namespace) -> None:
    """Prompt for telemetry opt-in on the first CLI run."""

    command = getattr(args, "command", None)
    if command == "config":
        return
    if getattr(args, "yes", False):
        # Commands executed with ``--yes`` are explicitly non-interactive, so
        # skip the telemetry prompt to avoid blocking automation (for example
        # during CI test runs).
        return
    _prompt_for_telemetry()


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
SPIN_ANALYZERS = {
    "ci",
    "dependencies",
    "docs",
    "lint",
    "readme",
    "tests",
}
SPIN_ANALYZER_HELP = (
    "comma-separated analyzers to enable/disable (use -name to disable)"
)
LANGUAGE_BY_SUFFIX = {
    ".bash": "Shell",
    ".c": "C",
    ".cc": "C++",
    ".cjs": "JavaScript",
    ".cpp": "C++",
    ".cs": "C#",
    ".css": "CSS",
    ".cxx": "C++",
    ".dart": "Dart",
    ".go": "Go",
    ".h": "C",
    ".hh": "C++",
    ".hpp": "C++",
    ".htm": "HTML",
    ".html": "HTML",
    ".ini": "INI",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".kts": "Kotlin",
    ".kt": "Kotlin",
    ".less": "Less",
    ".lua": "Lua",
    ".m": "Objective-C",
    ".md": "Markdown",
    ".mm": "Objective-C++",
    ".mjs": "JavaScript",
    ".php": "PHP",
    ".pl": "Perl",
    ".ps1": "PowerShell",
    ".psm1": "PowerShell",
    ".py": "Python",
    ".pyi": "Python",
    ".r": "R",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scala": "Scala",
    ".scss": "Sass",
    ".sh": "Shell",
    ".swift": "Swift",
    ".toml": "TOML",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".vue": "Vue",
    ".yaml": "YAML",
    ".yml": "YAML",
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

IMPACT_CONFIDENCE = {
    "high": 0.9,
    "medium": 0.8,
    "low": 0.7,
}


def _merge_repo_specs(specs: Sequence[str]) -> list[str]:
    """Return deduplicated repo specs preserving latest branch overrides."""

    order: list[str] = []
    branches: dict[str, str | None] = {}
    for raw in specs:
        spec = raw.strip()
        if not spec:
            continue
        if "@" in spec:
            name, branch = spec.split("@", 1)
            name = name.strip()
            branch = branch.strip()
        else:
            name = spec
            branch = ""
        if not name:
            continue
        if name not in order:
            order.append(name)
        if branch:
            branches[name] = branch
        else:
            branches.setdefault(name, None)

    merged: list[str] = []
    for name in order:
        branch = branches.get(name)
        merged.append(f"{name}@{branch}" if branch else name)
    return merged


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
    if save_dev is None:
        if args.yes:
            save_dev = False
        else:
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
    try:
        entries = list(workflows.iterdir())
    except OSError:
        return False

    keywords = getattr(RepoCrawler, "CI_KEYWORDS", ())
    for path in entries:
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".yml", ".yaml"}:
            continue
        name = path.name.lower()
        if any(keyword in name for keyword in keywords):
            return True
    return False


def _has_docs_directory(root: Path) -> bool:
    docs_dir = root / "docs"
    if not docs_dir.exists():
        return False
    try:
        for path in docs_dir.rglob("*"):
            if path.is_file() and not path.name.startswith("."):
                return True
    except OSError:
        return False
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


LINT_CONFIG_PATHS = [
    ".pre-commit-config.yaml",
    ".pre-commit-config.yml",
    ".flake8",
    "pylintrc",
    "eslint.config.js",
    "eslint.config.mjs",
    "eslint.config.cjs",
    ".eslintrc",
    ".eslintrc.json",
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.yaml",
    ".eslintrc.yml",
    ".stylelintrc",
    ".stylelintrc.json",
    ".stylelintrc.yaml",
    ".stylelintrc.yml",
]

PYPROJECT_LINT_MARKERS = (
    "[tool.black]",
    "[tool.ruff]",
    "[tool.flake8]",
    "[tool.isort]",
)

SETUP_CFG_LINT_MARKERS = (
    "[flake8]",
    "[pylint]",
    "[isort]",
)

PACKAGE_JSON_LINT_TOKENS = (
    "eslint",
    "prettier",
    "flake8",
    "ruff",
    "pylint",
)


LINT_VALIDATION_COMMANDS = (
    "pre-commit run --all-files"
    " || npm run lint -- --max-warnings=0"
    " || npm run lint"
    " || ruff check ."
    " || flake8 .",
)


def _pyproject_configures_lint(pyproject: Path) -> bool:
    if not pyproject.exists():
        return False
    try:
        text = pyproject.read_text()
    except OSError:
        return False
    lowered = text.lower()
    return any(marker in lowered for marker in PYPROJECT_LINT_MARKERS)


def _setup_cfg_configures_lint(setup_cfg: Path) -> bool:
    if not setup_cfg.exists():
        return False
    try:
        text = setup_cfg.read_text()
    except OSError:
        return False
    lowered = text.lower()
    return any(marker in lowered for marker in SETUP_CFG_LINT_MARKERS)


def _package_json_configures_lint(package_json: Path) -> bool:
    if not package_json.exists():
        return False
    try:
        payload: object = json.loads(package_json.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(payload, dict):
        return False
    scripts = payload.get("scripts")
    if not isinstance(scripts, dict):
        return False
    for key, command in scripts.items():
        if not isinstance(key, str) or not isinstance(command, str):
            continue
        lower_key = key.lower()
        lower_cmd = command.lower()
        if "lint" in lower_key:
            return True
        if any(token in lower_cmd for token in PACKAGE_JSON_LINT_TOKENS):
            return True
    return False


def _detect_lint_config(root: Path, files: Sequence[Path]) -> bool:
    """Return True when lint tooling is configured for the project."""

    if any((root / name).exists() for name in LINT_CONFIG_PATHS):
        return True
    if _pyproject_configures_lint(root / "pyproject.toml"):
        return True
    if _setup_cfg_configures_lint(root / "setup.cfg"):
        return True
    if _package_json_configures_lint(root / "package.json"):
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


def _lockfile_validation_commands(missing: Sequence[str]) -> list[str]:
    """Return shell commands that confirm expected lockfiles exist."""

    commands: list[str] = []
    for manifest in missing:
        manifest_path = Path(manifest)
        parent = manifest_path.parent
        prefix = parent.as_posix()
        if prefix in {"", "."}:
            prefix = ""
        else:
            prefix = f"{prefix}/"
        name = manifest_path.name.lower()
        if name == "package.json":
            checks: list[str] = []
            for candidate in NODE_LOCKFILES:
                candidate_path = f"{prefix}{candidate}"
                checks.append(f"test -f {candidate_path}")
            if checks:
                commands.append(" || ".join(checks))
        elif name == "pipfile":
            lock_path = f"{prefix}{PIPFILE_LOCK}"
            commands.append(f"test -f {lock_path}")
    return commands


def _parse_analyzers(value: str | None) -> set[str]:
    """Return enabled analyzers parsed from ``value``.

    ``value`` accepts a comma-separated list of analyzer names.
    Entries starting with ``-`` disable an analyzer, ``all`` resets to the
    ``none`` clears the list entirely. Analyzer names are case-insensitive.
    """

    enabled = set(SPIN_ANALYZERS)
    explicit_selection = False
    if not value:
        return enabled

    tokens = [token.strip() for token in value.split(",") if token.strip()]
    if not tokens:
        return enabled

    for token in tokens:
        lowered = token.lower()
        if lowered == "all":
            enabled = set(SPIN_ANALYZERS)
            explicit_selection = True
            continue
        if lowered == "none":
            enabled = set()
            explicit_selection = True
            continue
        negate = lowered.startswith("-")
        name = lowered[1:] if negate else lowered
        if name not in SPIN_ANALYZERS:
            valid = ", ".join(sorted(SPIN_ANALYZERS))
            message = f"Unknown analyzer '{name}'. " f"Valid options: {valid}."
            raise SystemExit(message)
        if negate:
            enabled.discard(name)
        else:
            if not explicit_selection:
                enabled = set()
                explicit_selection = True
            enabled.add(name)
    return enabled


def _analyze_repository(
    root: Path,
    analyzers: set[str] | None = None,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    enabled = analyzers if analyzers is not None else set(SPIN_ANALYZERS)
    include_docs = "docs" in enabled
    include_readme = "readme" in enabled
    include_ci = "ci" in enabled
    include_lint = "lint" in enabled
    include_tests = "tests" in enabled
    include_dependencies = "dependencies" in enabled
    files = _iter_project_files(root)
    ext_counts = Counter((path.suffix.lower() or "<none>") for path in files)
    top_extensions = [
        {"extension": ext, "count": count}
        for ext, count in sorted(
            ext_counts.items(), key=lambda item: (-item[1], item[0])
        )[:5]
    ]
    has_readme = (root / "README.md").exists() if include_readme else None
    has_ci = _has_ci_workflows(root) if include_ci else None
    has_docs = _has_docs_directory(root) if include_docs else None
    has_tests = _detect_tests(root, files) if include_tests else None
    has_lint = _detect_lint_config(root, files) if include_lint else None
    language_mix = _summarize_language_mix(files)
    if include_dependencies:
        dependency_health = _analyze_dependency_health(root, files)
    else:
        dependency_health = None
    stats: dict[str, object] = {
        "total_files": len(files),
        "top_extensions": top_extensions,
        "has_readme": has_readme,
        "has_docs": has_docs,
        "has_lint_config": has_lint,
        "has_tests": has_tests,
        "has_ci_workflows": has_ci,
        "language_mix": language_mix,
        "dependency_health": dependency_health,
    }
    suggestions: list[dict[str, object]] = []
    if include_docs and not has_docs:
        suggestions.append(
            {
                "id": "add-docs",
                "category": "docs",
                "title": "Create docs/ with onboarding guides",
                "description": (
                    "Set up a docs/ directory with project guides and "
                    "contributor onboarding notes so new collaborators ramp "
                    "up quickly."
                ),
                "impact": "medium",
                "confidence": IMPACT_CONFIDENCE["medium"],
                "files": ["docs/"],
                "dependencies": [],
                "validation": ["test -d docs"],
            }
        )
    if include_readme and not has_readme:
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
                "confidence": IMPACT_CONFIDENCE["medium"],
                "files": ["README.md"],
                "dependencies": [],
                "validation": ["test -f README.md"],
            }
        )
    if include_ci and not has_ci:
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
                "confidence": IMPACT_CONFIDENCE["high"],
                "files": [".github/workflows/"],
                "dependencies": [],
                "validation": ["test -d .github/workflows"],
            }
        )
    if include_lint and not has_lint:
        suggestions.append(
            {
                "id": "add-linting",
                "category": "chore",
                "title": "Add lint configuration",
                "description": (
                    "Set up lint tooling (for example pre-commit, "
                    "ESLint, or Ruff) so contributors catch style "
                    "issues before they reach CI."
                ),
                "impact": "medium",
                "confidence": IMPACT_CONFIDENCE["medium"],
                "files": [".pre-commit-config.yaml"],
                "dependencies": [],
                "validation": list(LINT_VALIDATION_COMMANDS),
            }
        )
    if include_tests and not has_tests:
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
                "confidence": IMPACT_CONFIDENCE["high"],
                "files": ["tests/"],
                "dependencies": [],
                "validation": [
                    "npm run test:ci || npm test || pytest -q",
                ],
            }
        )
    if (
        include_dependencies
        and dependency_health
        and dependency_health["missing_lockfiles"]
    ):
        validations = _lockfile_validation_commands(
            dependency_health["missing_lockfiles"]
        )
        if not validations:
            validations = ["git status --short"]
        suggestions.append(
            {
                "id": "commit-lockfiles",
                "category": "chore",
                "title": "Commit dependency lockfiles",
                "description": (
                    "Generate and commit dependency lockfiles (for example, "
                    "package-lock.json or Pipfile.lock) so installs stay "
                    "reproducible across environments."
                ),
                "impact": "medium",
                "confidence": IMPACT_CONFIDENCE["medium"],
                "files": dependency_health["missing_lockfiles"],
                "dependencies": [],
                "validation": validations,
            }
        )
    suggestions = _sort_suggestions(suggestions)
    return stats, suggestions


def _sort_suggestions(
    items: Sequence[dict[str, object]],
) -> list[dict[str, object]]:
    """Return suggestions sorted by category priority and impact severity."""

    category_order = {
        "fix": 0,
        "chore": 1,
        "docs": 2,
        "feature": 3,
        "refactor": 4,
    }
    impact_order = {"high": 0, "medium": 1, "low": 2}

    def sort_key(item: dict[str, object]) -> tuple[int, int, str]:
        category = str(item.get("category", ""))
        impact = str(item.get("impact", ""))
        cat_rank = category_order.get(category, len(category_order))
        impact_rank = impact_order.get(impact, len(impact_order))
        identifier = str(item.get("id", ""))
        return (cat_rank, impact_rank, identifier)

    return sorted(items, key=sort_key)


def _format_bool(value: bool | None) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "skipped"


def _format_language_mix(entries: Sequence[dict[str, object]]) -> str:
    if not entries:
        return "none detected"
    parts: list[str] = []
    for entry in entries:
        language = str(entry.get("language", ""))
        count = entry.get("count")
        parts.append(f"{language} ({count})")
    return ", ".join(parts)


def _format_confidence(value: object) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "-"
    if math.isnan(number) or math.isinf(number):
        return "-"
    return f"{number:.2f}"


def _format_stats_lines(stats: dict[str, object]) -> list[str]:
    dependency = stats.get("dependency_health")
    language_mix = stats.get("language_mix", [])
    lines = [f"  - total_files: {stats.get('total_files', 0)}"]
    readme_flag = _format_bool(stats.get("has_readme"))
    docs_flag = _format_bool(stats.get("has_docs"))
    ci_flag = _format_bool(stats.get("has_ci_workflows"))
    tests_flag = _format_bool(stats.get("has_tests"))
    lint_flag = _format_bool(stats.get("has_lint_config"))
    lines.append(f"  - has_readme: {readme_flag}")
    lines.append(f"  - has_docs: {docs_flag}")
    lines.append(f"  - has_ci_workflows: {ci_flag}")
    lines.append(f"  - has_tests: {tests_flag}")
    lines.append(f"  - has_lint_config: {lint_flag}")
    if isinstance(dependency, dict):
        dep_status = dependency.get("status", "unknown")
    elif dependency is None:
        dep_status = "skipped"
    else:
        dep_status = str(dependency)
    lines.append(f"  - dependency_health: {dep_status}")
    mix_text = _format_language_mix(language_mix)
    lines.append(f"  - language_mix: {mix_text}")
    return lines


def _render_spin_table(result: dict[str, object]) -> str:
    stats_lines = _format_stats_lines(result.get("stats", {}))
    suggestions = result.get("suggestions", [])
    lines = [
        f"Target: {result.get('target', '')}",
        f"Mode: {result.get('mode', '')}",
        "",
        "Stats:",
        *stats_lines,
        "",
    ]
    if suggestions:
        headers = [
            "Index",
            "Id",
            "Category",
            "Impact",
            "Confidence",
            "Title",
            "Files",
        ]
        rows: list[dict[str, str]] = []
        for idx, suggestion in enumerate(suggestions, start=1):
            files = ", ".join(suggestion.get("files", [])) or "-"
            confidence_value = _format_confidence(suggestion.get("confidence"))
            rows.append(
                {
                    "Index": str(idx),
                    "Id": str(suggestion.get("id", "")),
                    "Category": str(suggestion.get("category", "")),
                    "Impact": str(suggestion.get("impact", "")),
                    "Confidence": confidence_value,
                    "Title": str(suggestion.get("title", "")),
                    "Files": files,
                }
            )
        widths: dict[str, int] = {}
        for header in headers:
            max_cell = max((len(row[header]) for row in rows), default=0)
            widths[header] = max(len(header), max_cell)
        header_cells: list[str] = []
        for header in headers:
            header_cells.append(header.ljust(widths[header]))
        header_line = " | ".join(header_cells)
        sep_cells = ["-" * widths[header] for header in headers]
        separator = "-+-".join(sep_cells)
        lines.append("Suggestions:")
        lines.append(header_line)
        lines.append(separator)
        for row in rows:
            row_cells: list[str] = []
            for header in headers:
                row_cells.append(row[header].ljust(widths[header]))
            line = " | ".join(row_cells)
            lines.append(line)
    else:
        lines.append("Suggestions: none found.")
    return "\n".join(lines)


def _escape_markdown(text: str) -> str:
    escaped = text.replace("|", "\\|")
    return escaped.replace("\n", " ")


def _render_spin_markdown(result: dict[str, object]) -> str:
    stats = result.get("stats", {})
    stats_lines = _format_stats_lines(stats)
    summary = [
        "# flywheel spin dry-run",
        "",
        f"- Target: `{result.get('target', '')}`",
        f"- Mode: `{result.get('mode', '')}`",
    ]
    # Convert leading bullet prefix in stats lines to markdown list items.
    converted_stats: list[str] = []
    for line in stats_lines:
        converted_stats.append(line.replace("  -", "-", 1))
    summary.extend(converted_stats)
    summary.append("")
    suggestions = result.get("suggestions", [])
    if suggestions:
        headers = [
            "#",
            "Id",
            "Category",
            "Impact",
            "Confidence",
            "Title",
            "Files",
        ]
        summary.append("| " + " | ".join(headers) + " |")
        summary.append("| " + " | ".join("---" for _ in headers) + " |")
        for idx, suggestion in enumerate(suggestions, start=1):
            files = ", ".join(suggestion.get("files", [])) or "-"
            suggestion_id = _escape_markdown(str(suggestion.get("id", "")))
            category = _escape_markdown(str(suggestion.get("category", "")))
            impact = _escape_markdown(str(suggestion.get("impact", "")))
            title = _escape_markdown(str(suggestion.get("title", "")))
            files_cell = _escape_markdown(files)
            confidence = _format_confidence(suggestion.get("confidence"))
            cells = [
                str(idx),
                suggestion_id or "-",
                category or "-",
                impact or "-",
                confidence,
                title or "-",
                files_cell or "-",
            ]
            summary.append("| " + " | ".join(cells) + " |")
    else:
        summary.append("_No suggestions found._")
    return "\n".join(summary)


def spin(args: argparse.Namespace) -> None:
    target = Path(args.path or ".").resolve()
    if not target.exists():
        raise SystemExit(f"Target path not found: {target}")
    if not target.is_dir():
        raise SystemExit(f"Target path is not a directory: {target}")
    if not args.dry_run:
        msg = "Only --dry-run mode is supported; re-run with --dry-run."
        raise SystemExit(msg)
    analyzers = _parse_analyzers(getattr(args, "analyzers", None))
    stats, suggestions = _analyze_repository(target, analyzers=analyzers)
    result = {
        "target": str(target),
        "mode": "dry-run",
        "stats": stats,
        "suggestions": suggestions,
    }
    fmt = getattr(args, "format", "json") or "json"
    if fmt == "json":
        output = json.dumps(result, indent=2, sort_keys=True)
    elif fmt == "table":
        output = _render_spin_table(result)
    elif fmt == "markdown":
        output = _render_spin_markdown(result)
    else:
        raise SystemExit(f"Unsupported format: {fmt}")
    print(output)


def crawl(args: argparse.Namespace) -> None:
    cli_repos = list(args.repos)
    repo_file = Path(args.repos_file)
    combined: list[str] = []
    if repo_file.exists():
        lines = repo_file.read_text().splitlines()
        file_repos = [line.strip() for line in lines if line.strip()]
        combined.extend(file_repos)
    combined.extend(cli_repos)

    # Merge repository specs while ensuring the latest branch override wins
    repos: list[str] = _merge_repo_specs(combined)

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
    parser = argparse.ArgumentParser(
        prog="flywheel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_EPILOG,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="initialize a repository")
    p_init.add_argument("path", help="target repository path")
    p_init.add_argument(
        "--language", choices=["python", "javascript"], default="python"
    )
    p_init.add_argument(
        "--save-dev",
        action="store_true",
        dest="save_dev",
        help="inject dev tooling",
    )
    p_init.add_argument(
        "--no-save-dev",
        action="store_false",
        dest="save_dev",
        help="skip dev tooling",
    )
    p_init.add_argument(
        "--yes",
        action="store_true",
        help="run non-interactively",
    )
    p_init.set_defaults(func=init_repo, save_dev=None)

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
    p_spin.add_argument(
        "--format",
        choices=["json", "table", "markdown"],
        default="json",
        help="output format for dry-run results",
    )
    p_spin.add_argument("--analyzers", help=SPIN_ANALYZER_HELP)
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

    p_status = sub.add_parser(
        "status",
        help="update README related project statuses",
    )
    p_status.add_argument(
        "--readme",
        type=Path,
        default=Path("README.md"),
        help="path to README file",
    )
    p_status.add_argument(
        "--token",
        help="GitHub token (defaults to GITHUB_TOKEN env variable)",
    )
    p_status.add_argument(
        "--attempts",
        type=int,
        default=2,
        help="number of API reads to confirm workflow conclusions",
    )
    p_status.set_defaults(func=update_related_status)

    p_config = sub.add_parser("config", help="manage CLI configuration")
    config_sub = p_config.add_subparsers(dest="config_command", required=True)

    p_config_telemetry = config_sub.add_parser(
        "telemetry",
        help="manage telemetry preferences",
    )
    p_config_telemetry.add_argument(
        "--set",
        choices=["off", "on", "full"],
        help="set telemetry preference (default shows current value)",
    )
    p_config_telemetry.set_defaults(func=telemetry_config)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    maybe_prompt_for_telemetry(args)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
