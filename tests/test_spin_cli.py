from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Collection
from pathlib import Path

import pytest

from flywheel import __main__ as main_module
from flywheel.__main__ import (
    LINT_VALIDATION_COMMANDS,
    SPIN_ANALYZERS,
    _analyze_repository,
    _detect_lint_config,
    _detect_tests,
    _format_stats_lines,
    _has_ci_workflows,
    _has_docs_directory,
    _iter_project_files,
    _package_json_configures_lint,
    _parse_analyzers,
    _pyproject_configures_lint,
    _render_spin_markdown,
    _render_spin_table,
    _setup_cfg_configures_lint,
    _spin_cache_filename,
    _write_spin_cache,
    spin,
)

CaptureFixtureStr = pytest.CaptureFixture[str]


def run_spin_dry_run(
    path: Path, *extra: str, env: dict[str, str] | None = None
) -> dict:
    cmd = [
        sys.executable,
        "-m",
        "flywheel",
        "spin",
        str(path),
        "--dry-run",
        *extra,
    ]
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    completed = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
        env=run_env,
    )
    return json.loads(completed.stdout)


def run_spin_dry_run_text(
    path: Path, *extra: str, env: dict[str, str] | None = None
) -> str:
    cmd = [
        sys.executable,
        "-m",
        "flywheel",
        "spin",
        str(path),
        "--dry-run",
        *extra,
    ]
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    completed = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
        env=run_env,
    )
    return completed.stdout


def test_parse_analyzers_defaults_when_blank() -> None:
    assert _parse_analyzers(",") == set(SPIN_ANALYZERS)


def test_parse_analyzers_allows_explicit_subset() -> None:
    assert _parse_analyzers("docs") == {"docs"}


def test_parse_analyzers_allows_none_then_add() -> None:
    assert _parse_analyzers("none,docs") == {"docs"}


def test_parse_analyzers_allows_all_then_disable() -> None:
    expected = set(SPIN_ANALYZERS) - {"tests"}
    assert _parse_analyzers("all,-tests") == expected


def test_spin_dry_run_flags_missing_assets(tmp_path: Path) -> None:
    repo = tmp_path / "sample"
    repo.mkdir()

    result = run_spin_dry_run(repo)

    assert result["mode"] == "dry-run"
    stats = result["stats"]
    assert stats["has_readme"] is False
    assert stats["has_docs"] is False
    assert stats["has_ci_workflows"] is False
    assert stats["has_tests"] is False
    assert stats["has_lint_config"] is False
    assert stats["has_lint_config"] is False

    suggestion_ids = {entry["id"] for entry in result["suggestions"]}
    assert suggestion_ids == {
        "add-docs",
        "add-readme",
        "add-tests",
        "add-linting",
        "configure-ci",
    }

    categories: dict[str, str] = {}
    validations: dict[str, list[str]] = {}
    for entry in result["suggestions"]:
        categories[entry["id"]] = entry["category"]
        assert 0.0 <= entry["confidence"] <= 1.0
        validations[entry["id"]] = entry["validation"]
        assert entry["dependencies"] == []
        assert entry["rationale"] == entry["description"]
        assert entry["diffPreview"] == ""
    assert categories == {
        "add-docs": "docs",
        "add-readme": "docs",
        "add-tests": "fix",
        "add-linting": "chore",
        "configure-ci": "chore",
    }
    assert validations["add-docs"] == ["test -d docs"]
    assert validations["add-readme"] == ["test -f README.md"]
    assert validations["configure-ci"] == ["test -d .github/workflows"]
    assert validations["add-tests"] == [
        "npm run test:ci || npm test || pytest -q",
    ]
    lint_validation_commands = list(LINT_VALIDATION_COMMANDS)
    assert validations["add-linting"] == lint_validation_commands


def test_spin_dry_run_detects_existing_assets(tmp_path: Path) -> None:
    repo = tmp_path / "project"
    workflows = repo / ".github" / "workflows"
    tests_dir = repo / "tests"
    workflows.mkdir(parents=True)
    tests_dir.mkdir(parents=True)
    repo.mkdir(exist_ok=True)

    (repo / "README.md").write_text("Hello world\n")
    docs_dir = repo / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Overview\n")
    test_code = "def test_sample():\n    assert True\n"
    (tests_dir / "test_sample.py").write_text(test_code)
    (workflows / "ci.yml").write_text("name: CI\n")
    (repo / ".pre-commit-config.yaml").write_text("repos: []\n")

    result = run_spin_dry_run(repo)

    stats = result["stats"]
    assert stats["has_readme"] is True
    assert stats["has_docs"] is True
    assert stats["has_ci_workflows"] is True
    assert stats["has_tests"] is True
    assert stats["has_lint_config"] is True

    assert result["suggestions"] == []


def test_spin_analyzers_subset(tmp_path: Path) -> None:
    repo = tmp_path / "subset"
    repo.mkdir()
    (repo / "package.json").write_text("{}\n")

    result = run_spin_dry_run(
        repo,
        "--analyzers",
        "docs,dependencies",
    )

    stats = result["stats"]
    assert stats["has_docs"] is False
    assert stats["has_readme"] is None
    assert stats["has_ci_workflows"] is None
    assert stats["has_tests"] is None
    assert stats["has_lint_config"] is None
    dependency = stats["dependency_health"]
    assert dependency["status"] == "lockfile-missing"

    suggestion_ids = {entry["id"] for entry in result["suggestions"]}
    assert suggestion_ids == {"add-docs", "commit-lockfiles"}
    for entry in result["suggestions"]:
        assert entry["validation"], entry["id"]
        assert entry["dependencies"] == []


def test_spin_analyzers_disable_with_minus(tmp_path: Path) -> None:
    repo = tmp_path / "minus"
    repo.mkdir()

    result = run_spin_dry_run(
        repo,
        "--analyzers",
        "all,-tests",
    )

    stats = result["stats"]
    assert stats["has_tests"] is None
    assert stats["has_lint_config"] is False

    suggestion_ids = {entry["id"] for entry in result["suggestions"]}
    assert "add-tests" not in suggestion_ids
    assert {
        "add-docs",
        "add-readme",
        "add-linting",
        "configure-ci",
    }.issubset(suggestion_ids)
    for entry in result["suggestions"]:
        assert entry["validation"], entry["id"]
        assert entry["dependencies"] == []


def test_spin_invalid_analyzer_errors(tmp_path: Path) -> None:
    repo = tmp_path / "invalid"
    repo.mkdir()

    args = argparse.Namespace(
        path=str(repo),
        dry_run=True,
        format="json",
        analyzers="bogus",
    )

    with pytest.raises(SystemExit):
        spin(args)


def test_has_docs_directory_ignores_hidden_files(tmp_path: Path) -> None:
    repo = tmp_path / "hidden-docs"
    repo.mkdir()

    docs_dir = repo / "docs"
    docs_dir.mkdir()
    (docs_dir / ".placeholder").write_text("hidden\n")

    assert _has_docs_directory(repo) is False


def test_has_docs_directory_handles_os_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    repo = tmp_path / "docs-error"
    repo.mkdir()

    docs_dir = repo / "docs"
    docs_dir.mkdir()

    original_rglob = Path.rglob

    def raising_rglob(self: Path, pattern: str):
        if self == docs_dir:
            raise OSError("permission denied")
        return original_rglob(self, pattern)

    monkeypatch.setattr(Path, "rglob", raising_rglob)

    assert _has_docs_directory(repo) is False


def test_spin_reports_missing_lockfile(tmp_path: Path) -> None:
    repo = tmp_path / "pkg"
    repo.mkdir()
    (repo / "package.json").write_text("{}\n")

    result = run_spin_dry_run(repo)

    dep = result["stats"]["dependency_health"]
    assert dep["status"] == "lockfile-missing"
    assert dep["manifests"] == ["package.json"]
    assert dep["missing_lockfiles"] == ["package.json"]

    suggestion_ids = {entry["id"] for entry in result["suggestions"]}
    assert "commit-lockfiles" in suggestion_ids
    for entry in result["suggestions"]:
        if entry["id"] == "commit-lockfiles":
            lock_suggestion = entry
            break
    else:  # pragma: no cover - defensive fallback
        raise AssertionError("commit-lockfiles suggestion missing")
    assert "package.json" in lock_suggestion["files"]
    assert 0.0 <= lock_suggestion["confidence"] <= 1.0
    assert lock_suggestion["dependencies"] == []
    lock_commands = [
        command
        for command in lock_suggestion["validation"]
        if "package-lock.json" in command
    ]
    assert lock_commands


def test_spin_lockfile_validation_handles_pipfile(tmp_path: Path) -> None:
    repo = tmp_path / "pip"
    repo.mkdir()
    (repo / "Pipfile").write_text("[packages]\n")

    result = run_spin_dry_run(repo)

    for entry in result["suggestions"]:
        if entry["id"] == "commit-lockfiles":
            lock = entry
            break
    else:  # pragma: no cover - defensive fallback
        raise AssertionError("commit-lockfiles suggestion missing")
    pip_commands = [
        command for command in lock["validation"] if "Pipfile.lock" in command
    ]
    assert pip_commands
    assert lock["dependencies"] == []


def test_suggestions_sorted_by_category_and_impact(tmp_path: Path) -> None:
    repo = tmp_path / "prioritized"
    repo.mkdir()
    (repo / "package.json").write_text("{}\n")

    stats, suggestions = main_module._analyze_repository(repo)

    assert stats["has_readme"] is False
    assert stats["has_docs"] is False
    assert stats["has_ci_workflows"] is False
    assert stats["has_tests"] is False

    assert [entry["id"] for entry in suggestions] == [
        "add-tests",
        "configure-ci",
        "add-linting",
        "commit-lockfiles",
        "add-docs",
        "add-readme",
    ]
    for entry in suggestions:
        assert 0.0 <= entry["confidence"] <= 1.0
        assert entry["validation"], entry["id"]


def test_spin_ignores_present_lockfile(tmp_path: Path) -> None:
    repo = tmp_path / "pkg"
    repo.mkdir()
    (repo / "package.json").write_text("{}\n")
    (repo / "package-lock.json").write_text("{}\n")

    result = run_spin_dry_run(repo)

    dep = result["stats"]["dependency_health"]
    assert dep["status"] == "ok"
    assert dep["missing_lockfiles"] == []
    suggestion_ids = {entry["id"] for entry in result["suggestions"]}
    assert "commit-lockfiles" not in suggestion_ids


def test_spin_reports_language_mix(tmp_path: Path) -> None:
    repo = tmp_path / "polyglot"
    repo.mkdir()

    scripts = repo / "scripts"
    scripts.mkdir()
    (scripts / "build.py").write_text("print('hi')\n")

    services = repo / "services"
    services.mkdir()
    (services / "worker.py").write_text("print('hello')\n")

    frontend = repo / "frontend"
    frontend.mkdir()
    (frontend / "main.ts").write_text("export const foo = 1;\n")

    ui = repo / "ui"
    ui.mkdir()
    (ui / "App.jsx").write_text("export default () => null;\n")

    result = run_spin_dry_run(repo)

    mix = result["stats"]["language_mix"]
    assert mix == [
        {"language": "Python", "count": 2},
        {"language": "JavaScript", "count": 1},
        {"language": "TypeScript", "count": 1},
    ]


def test_language_mix_recognizes_more_languages(tmp_path: Path) -> None:
    repo = tmp_path / "polyglot2"
    repo.mkdir()

    (repo / "backend").mkdir()
    (repo / "backend" / "main.rs").write_text("fn main() {}\n")
    (repo / "service").mkdir()
    (repo / "service" / "handler.go").write_text("package main\n")
    (repo / "app").mkdir()
    (repo / "app" / "Main.java").write_text("class Main {}\n")
    (repo / "scripts").mkdir()
    (repo / "scripts" / "deploy.sh").write_text("#!/bin/bash\n")

    stats, _ = main_module._analyze_repository(repo)
    mix = stats["language_mix"]
    languages = {entry["language"] for entry in mix}
    assert {"Rust", "Go", "Java", "Shell"}.issubset(languages)


def test_dependency_health_tracks_manifests_and_lockfiles(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "deps"
    repo.mkdir()

    node_dir = repo / "web"
    node_dir.mkdir()
    (node_dir / "package.json").write_text("{}\n")
    (node_dir / "pnpm-lock.yaml").write_text("lock\n")

    python_dir = repo / "api"
    python_dir.mkdir()
    (python_dir / "Pipfile").write_text("[packages]\n")

    files = [
        node_dir / "package.json",
        node_dir / "pnpm-lock.yaml",
        python_dir / "Pipfile",
        Path("outside/package.json"),
    ]

    health = main_module._analyze_dependency_health(repo, files)

    assert health["manifests"] == [
        "api/Pipfile",
        "outside/package.json",
        "web/package.json",
    ]
    assert health["lockfiles"] == ["web/pnpm-lock.yaml"]
    assert health["missing_lockfiles"] == [
        "api/Pipfile",
        "outside/package.json",
    ]
    assert health["status"] == "lockfile-missing"


def test_dependency_health_handles_pipfile_lock(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "pipenv"
    repo.mkdir()

    (repo / "Pipfile").write_text("[packages]\n")
    (repo / "Pipfile.lock").write_text("{}\n")

    files = [repo / "Pipfile", repo / "Pipfile.lock"]

    health = main_module._analyze_dependency_health(repo, files)

    assert health["manifests"] == ["Pipfile"]
    assert health["lockfiles"] == ["Pipfile.lock"]
    assert health["missing_lockfiles"] == []
    assert health["status"] == "ok"


def test_analyze_repository_emits_lockfile_suggestion(tmp_path: Path) -> None:
    repo = tmp_path / "service"
    repo.mkdir()
    (repo / "package.json").write_text("{}\n")

    stats, suggestions = main_module._analyze_repository(repo)

    dependency_health = stats["dependency_health"]
    assert dependency_health["missing_lockfiles"] == ["package.json"]
    lockfile_suggestion = next(
        entry for entry in suggestions if entry["id"] == "commit-lockfiles"
    )
    assert lockfile_suggestion["category"] == "chore"
    assert 0.0 <= lockfile_suggestion["confidence"] <= 1.0
    rationale = lockfile_suggestion["rationale"]
    description = lockfile_suggestion["description"]
    assert rationale == description
    assert lockfile_suggestion["diffPreview"] == ""


def test_lockfile_validation_commands_cover_known_manifests() -> None:
    missing = [
        "package.json",
        "app/package.json",
        "api/Pipfile",
    ]

    commands = main_module._lockfile_validation_commands(missing)

    assert "package-lock.json" in commands[0]
    assert "app/package-lock.json" in commands[1]
    assert "app/pnpm-lock.yaml" in commands[1]
    assert commands[2] == "test -f api/Pipfile.lock"


def test_lockfile_suggestion_falls_back_to_git_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "service"
    repo.mkdir()
    (repo / "package.json").write_text("{}\n")

    monkeypatch.setattr(
        main_module,
        "_lockfile_validation_commands",
        lambda missing: [],
    )

    _, suggestions = main_module._analyze_repository(repo)

    lockfile_suggestion = next(
        entry for entry in suggestions if entry["id"] == "commit-lockfiles"
    )

    assert lockfile_suggestion["validation"] == ["git status --short"]


def test_spin_requires_existing_directory(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist"
    args = argparse.Namespace(path=str(missing), dry_run=True)

    with pytest.raises(SystemExit) as exc:
        spin(args)

    assert "Target path not found" in str(exc.value)


def test_spin_rejects_file_targets(tmp_path: Path) -> None:
    file_path = tmp_path / "README.md"
    file_path.write_text("hello\n")
    args = argparse.Namespace(path=str(file_path), dry_run=True)

    with pytest.raises(SystemExit) as exc:
        spin(args)

    assert "Target path is not a directory" in str(exc.value)


def test_spin_requires_dry_run_flag(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    args = argparse.Namespace(path=str(repo), dry_run=False)

    with pytest.raises(SystemExit) as exc:
        spin(args)

    assert "Only --dry-run mode is supported" in str(exc.value)


def test_spin_writes_cache_file(tmp_path: Path) -> None:
    repo = tmp_path / "cacheable"
    repo.mkdir()
    cache_dir = tmp_path / "cache"

    result = run_spin_dry_run(repo, "--cache-dir", str(cache_dir))

    files = list(cache_dir.glob("*.json"))
    assert len(files) == 1
    cached = json.loads(files[0].read_text())
    assert cached == result


def test_spin_reuses_existing_cache(
    tmp_path: Path,
    capsys: CaptureFixtureStr,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = tmp_path / "cached"
    repo.mkdir()
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    cached_payload = {
        "target": str(repo.resolve()),
        "mode": "dry-run",
        "stats": {"cached": True},
        "suggestions": [
            {
                "id": "cached",
                "category": "chore",
                "impact": "low",
                "confidence": 0.5,
                "title": "Use cached result",
                "files": [],
                "dependencies": [],
            }
        ],
    }
    cache_path = cache_dir / _spin_cache_filename(repo)
    cache_path.write_text(json.dumps(cached_payload) + "\n")

    def fail_analyze(*_args: object, **_kwargs: object) -> None:
        message = "analysis should be skipped when cache exists"
        raise AssertionError(message)

    monkeypatch.setattr(main_module, "_analyze_repository", fail_analyze)

    def fail_write(*_args: object, **_kwargs: object) -> None:
        message = "cache writer should not be invoked for cached result"
        raise AssertionError(message)

    monkeypatch.setattr(main_module, "_write_spin_cache", fail_write)

    args = argparse.Namespace(
        path=str(repo),
        dry_run=True,
        cache_dir=str(cache_dir),
        analyzers=None,
        format="json",
    )

    spin(args)

    output = json.loads(capsys.readouterr().out)
    assert output["analyzers"] == sorted(SPIN_ANALYZERS)
    for key, value in cached_payload.items():
        assert output[key] == value


def test_spin_ignores_cache_with_different_analyzers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "subset"
    repo.mkdir()
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    default_payload = {
        "target": str(repo.resolve()),
        "mode": "dry-run",
        "stats": {"cached": True},
        "suggestions": [],
    }
    default_path = cache_dir / _spin_cache_filename(repo)
    default_path.write_text(json.dumps(default_payload) + "\n")

    calls: list[tuple[dict[str, bool], list[dict[str, object]]]] = []

    def fake_analyze(
        *_args: object, **_kwargs: object
    ) -> tuple[dict[str, bool], list[dict[str, object]]]:
        result_stats = {"fresh": True}
        result_suggestions: list[dict[str, object]] = []
        calls.append((result_stats, result_suggestions))
        return result_stats, result_suggestions

    monkeypatch.setattr(main_module, "_analyze_repository", fake_analyze)

    args = argparse.Namespace(
        path=str(repo),
        dry_run=True,
        cache_dir=str(cache_dir),
        analyzers="docs",
        format="json",
    )

    spin(args)

    assert calls, "analyze should run when analyzers differ from cached payload"
    cached_files = list(cache_dir.glob("*.json"))
    assert any(path != default_path for path in cached_files)


def test_spin_hydrates_analyzers_for_legacy_cache(
    tmp_path: Path, capsys: CaptureFixtureStr, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "legacy"
    repo.mkdir()
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    cached_payload = {
        "target": str(repo.resolve()),
        "mode": "dry-run",
        "stats": {"cached": True},
        "suggestions": [],
    }
    cache_path = cache_dir / _spin_cache_filename(repo)
    cache_path.write_text(json.dumps(cached_payload) + "\n")

    def fail_analyze(*_args: object, **_kwargs: object) -> None:
        message = "legacy caches should skip repository analysis"
        raise AssertionError(message)

    monkeypatch.setattr(main_module, "_analyze_repository", fail_analyze)

    args = argparse.Namespace(
        path=str(repo),
        dry_run=True,
        cache_dir=str(cache_dir),
        analyzers=None,
        format="json",
    )

    spin(args)

    output = json.loads(capsys.readouterr().out)
    assert output["analyzers"] == sorted(SPIN_ANALYZERS)


def test_spin_cache_filename_is_stable_and_sanitized(tmp_path: Path) -> None:
    project = tmp_path / "My Repo !"
    project.mkdir()

    filename = _spin_cache_filename(project)

    assert filename.endswith(".json")
    assert " " not in filename
    assert "!" not in filename
    assert filename == _spin_cache_filename(project)


def test_spin_cache_filename_handles_root_anchor(tmp_path: Path) -> None:
    # Passing the filesystem root exercises the fallback stem branch.
    root_target = Path(tmp_path.anchor)

    filename = _spin_cache_filename(root_target)

    assert filename.startswith("target-")
    assert filename.endswith(".json")


def test_write_spin_cache_skips_rewrites_when_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache_dir = tmp_path / "cache"
    target = tmp_path / "project"
    target.mkdir()

    writes: list[str] = []
    original_write_text = Path.write_text

    def tracking_write(self: Path, text: str, *args, **kwargs):
        writes.append(text)
        return original_write_text(self, text, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", tracking_write, raising=False)

    initial = {"value": 1}
    cache_path = _write_spin_cache(cache_dir, target, initial)
    assert cache_path.exists()
    assert json.loads(cache_path.read_text()) == initial

    _write_spin_cache(cache_dir, target, initial)
    assert len(writes) == 1

    updated = {"value": 2}
    _write_spin_cache(cache_dir, target, updated)
    assert len(writes) == 2
    assert json.loads(cache_path.read_text()) == updated


def test_write_spin_cache_handles_read_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache_dir = tmp_path / "cache"
    target = tmp_path / "project"
    target.mkdir()

    existing_path = cache_dir / _spin_cache_filename(target)
    cache_dir.mkdir()
    existing_path.write_text(json.dumps({"value": 1}) + "\n")

    original_read = Path.read_text

    def flaky_read(self: Path, *args, **kwargs):
        if self == existing_path:
            raise OSError("temporary failure")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", flaky_read, raising=False)

    updated = {"value": 2}
    cache_path = _write_spin_cache(cache_dir, target, updated)
    assert cache_path == existing_path
    assert json.loads(original_read(existing_path)) == updated


def test_spin_invokes_cache_writer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    cache_dir = tmp_path / "cache"

    fake_stats = {"ok": True}
    fake_suggestions = [{"id": "demo"}]

    def fake_analyze(
        *_args: object, **_kwargs: object
    ) -> tuple[dict[str, bool], list[dict[str, str]]]:
        return fake_stats, fake_suggestions

    monkeypatch.setattr(main_module, "_analyze_repository", fake_analyze)

    writes: list[tuple[Path, Path, dict[str, object]]] = []

    def fake_write(
        cache_path: Path,
        target: Path,
        payload: dict[str, object],
        analyzers: Collection[str] | None = None,
    ) -> Path:
        writes.append((cache_path, target, payload, analyzers))
        expected = cache_path / "result.json"
        expected.parent.mkdir(parents=True, exist_ok=True)
        expected.write_text("{}")
        return expected

    monkeypatch.setattr(main_module, "_write_spin_cache", fake_write)

    args = argparse.Namespace(
        path=str(repo),
        dry_run=True,
        cache_dir=str(cache_dir),
        format="json",
    )

    spin(args)

    assert writes
    cache_path, target_path, payload, analyzers = writes[0]
    assert cache_path == cache_dir
    assert target_path == repo
    assert payload["mode"] == "dry-run"
    assert payload["analyzers"] == sorted(SPIN_ANALYZERS)
    assert analyzers is None


def test_spin_telemetry_override_updates_config(tmp_path: Path) -> None:
    repo = tmp_path / "telemetry"
    repo.mkdir()
    config_dir = tmp_path / "cfg"
    env = {"FLYWHEEL_CONFIG_DIR": str(config_dir)}

    run_spin_dry_run(repo, "--telemetry", "off", env=env)

    config_path = config_dir / "config.json"
    assert config_path.exists()
    data = json.loads(config_path.read_text())
    assert data["telemetry"] == "off"

    run_spin_dry_run(repo, "--telemetry", "full", env=env)
    updated = json.loads(config_path.read_text())
    assert updated["telemetry"] == "full"


def test_iter_project_files_skips_unwanted_entries(tmp_path: Path) -> None:
    repo = tmp_path / "project"
    repo.mkdir()

    hidden_dir = repo / ".git"
    hidden_dir.mkdir()
    (hidden_dir / "config").write_text("noop\n")

    allowed_hidden = repo / ".github" / "workflows"
    allowed_hidden.mkdir(parents=True)
    (allowed_hidden / "ci.yml").write_text("name: CI\n")

    dotted_dir = repo / ".cache"
    dotted_dir.mkdir()

    (repo / "node_modules").mkdir()
    (repo / "node_modules" / "index.js").write_text("module.exports = {}\n")

    src = repo / "src"
    src.mkdir()
    (src / "main.py").write_text("print('hi')\n")

    (repo / ".env").write_text("SECRET=1\n")

    files = _iter_project_files(repo)
    relative = {path.relative_to(repo).as_posix() for path in files}

    assert "src/main.py" in relative
    assert ".github/workflows/ci.yml" in relative
    assert ".env" not in relative
    assert "node_modules/index.js" not in relative
    assert ".git/config" not in relative
    assert ".cache" not in relative


def test_iter_project_files_guard_skipped_dirs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    repo = tmp_path / "synthetic"
    repo.mkdir()

    node_modules = repo / "node_modules"
    package_dir = node_modules / "pkg"
    package_dir.mkdir(parents=True)
    (package_dir / "index.js").write_text("module.exports = {}\n")

    walk_sequence = [
        (str(repo), ["node_modules"], []),
        (str(node_modules), ["pkg"], []),
        (str(package_dir), [], ["index.js"]),
    ]

    def fake_walk(path: Path):
        for dirpath, dirnames, filenames in walk_sequence:
            yield dirpath, list(dirnames), list(filenames)

    monkeypatch.setattr(main_module.os, "walk", fake_walk)

    files = _iter_project_files(repo)

    assert files == []


def test_has_ci_workflows_requires_ci_keywords(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    assert _has_ci_workflows(repo) is False

    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "README.txt").write_text("nope\n")

    assert _has_ci_workflows(repo) is False

    (workflows / "deploy.yaml").write_text("name: Deploy\n")

    assert _has_ci_workflows(repo) is False

    (workflows / "lint.yml").write_text("name: Lint\n")

    assert _has_ci_workflows(repo) is True


def test_has_ci_workflows_handles_iterdir_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    repo = tmp_path / "repo"
    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True)

    original_iterdir = Path.iterdir

    def fake_iterdir(self: Path):
        if self == workflows:
            raise OSError("permission denied")
        return original_iterdir(self)

    monkeypatch.setattr(Path, "iterdir", fake_iterdir)

    assert _has_ci_workflows(repo) is False


def test_has_ci_workflows_ignores_directories(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True)

    (workflows / "nested").mkdir()

    assert _has_ci_workflows(repo) is False

    (workflows / "lint.yml").write_text("name: Lint\n")

    assert _has_ci_workflows(repo) is True


def test_detect_tests_handles_multiple_patterns(tmp_path: Path) -> None:
    repo = tmp_path / "project"
    repo.mkdir()

    assert _detect_tests(repo, []) is False

    (repo / "tests").mkdir()
    (repo / "tests" / "sample.txt").write_text("artifact\n")

    assert _detect_tests(repo, []) is True

    src = repo / "src"
    src.mkdir()
    code_files = [src / "utils_test.py", src / "component.spec.ts"]
    for path in code_files:
        path.write_text("pass\n")

    other_files = [src / "helpers.py", repo / "README.md"]
    for path in other_files:
        path.write_text("print('ok')\n")

    files = _iter_project_files(repo)
    assert _detect_tests(repo, files) is True


def test_detect_tests_scans_code_paths_without_tests_dir(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "codebase"
    repo.mkdir()

    test_like_paths = [
        repo / "src" / "module_test.py",
        repo / "src" / "component.test.tsx",
        repo / "pkg" / "__tests__" / "index.js",
        repo / "examples" / "tests" / "helper.ts",
    ]
    for path in test_like_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("pass\n")

    noise = repo / "README.md"
    noise.write_text("# Sample\n")

    assert _detect_tests(repo, test_like_paths + [noise]) is True


def test_detect_tests_honors_test_prefix(tmp_path: Path) -> None:
    repo = tmp_path / "prefix"
    repo.mkdir()

    readme = repo / "README.md"
    readme.write_text("# project\n")

    test_file = repo / "src" / "test_example.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("def test_example():\n    assert True\n")

    assert _detect_tests(repo, [readme, test_file]) is True


def test_detect_tests_checks_parent_directories(tmp_path: Path) -> None:
    repo = tmp_path / "parent"
    repo.mkdir()

    helper = repo / "pkg" / "tests" / "helper.js"
    helper.parent.mkdir(parents=True, exist_ok=True)
    helper.write_text("module.exports = {}\n")

    assert _detect_tests(repo, [helper]) is True


def test_detect_lint_config_detects_pre_commit(tmp_path: Path) -> None:
    repo = tmp_path / "lint"
    repo.mkdir()
    (repo / ".pre-commit-config.yaml").write_text("repos: []\n")

    assert _detect_lint_config(repo, []) is True


def test_detect_lint_config_detects_package_json_script(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "package"
    repo.mkdir()
    package_json = repo / "package.json"
    payload = {"scripts": {"lint": "eslint src"}}
    package_json.write_text(json.dumps(payload) + "\n")

    assert _detect_lint_config(repo, []) is True


def test_detect_lint_config_detects_pyproject(tmp_path: Path) -> None:
    repo = tmp_path / "pyproject"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[tool.ruff]\nline-length = 100\n")

    assert _detect_lint_config(repo, []) is True


def test_detect_lint_config_returns_false_without_signals(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "nolint"
    repo.mkdir()

    assert _detect_lint_config(repo, []) is False


def test_detect_lint_config_detects_setup_cfg(tmp_path: Path) -> None:
    repo = tmp_path / "setup"
    repo.mkdir()
    (repo / "setup.cfg").write_text("[isort]\nprofile = black\n")

    assert _detect_lint_config(repo, []) is True


def test_pyproject_configures_lint_detects_markers(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[tool.isort]\nprofile = 'black'\n")

    assert _pyproject_configures_lint(pyproject) is True


def test_pyproject_configures_lint_handles_read_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[tool.ruff]\n")

    def boom(_: Path) -> str:
        raise OSError("unreadable")

    monkeypatch.setattr(Path, "read_text", boom)

    assert _pyproject_configures_lint(pyproject) is False


def test_setup_cfg_configures_lint_detects_markers(tmp_path: Path) -> None:
    setup_cfg = tmp_path / "setup.cfg"
    setup_cfg.write_text("[flake8]\nmax-line-length = 100\n")

    assert _setup_cfg_configures_lint(setup_cfg) is True


def test_setup_cfg_configures_lint_handles_read_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    setup_cfg = tmp_path / "setup.cfg"
    setup_cfg.write_text("[pylint]\ndisable = missing-docstring\n")

    def boom(_: Path) -> str:
        raise OSError("unreadable")

    monkeypatch.setattr(Path, "read_text", boom)

    assert _setup_cfg_configures_lint(setup_cfg) is False


def test_package_json_configures_lint_detects_tokens(tmp_path: Path) -> None:
    package_json = tmp_path / "package.json"
    package_json.write_text(
        json.dumps(
            {
                "scripts": {
                    "check": "prettier --check src",
                }
            }
        )
    )

    assert _package_json_configures_lint(package_json) is True


def test_package_json_configures_lint_skips_non_string_entries(
    tmp_path: Path,
) -> None:
    package_json = tmp_path / "package.json"
    package_json.write_text(
        json.dumps(
            {
                "scripts": {
                    "lint": ["eslint"],
                }
            }
        )
    )

    assert _package_json_configures_lint(package_json) is False


def test_package_json_configures_lint_handles_invalid_json(
    tmp_path: Path,
) -> None:
    package_json = tmp_path / "package.json"
    package_json.write_text("{invalid")

    assert _package_json_configures_lint(package_json) is False


def test_package_json_configures_lint_handles_read_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    package_json = tmp_path / "package.json"
    package_json.write_text(
        json.dumps(
            {
                "scripts": {
                    "lint": "eslint src",
                }
            }
        )
    )

    def boom(_: Path) -> str:
        raise OSError("unreadable")

    monkeypatch.setattr(Path, "read_text", boom)

    assert _package_json_configures_lint(package_json) is False


def test_package_json_configures_lint_handles_non_mapping_payload(
    tmp_path: Path,
) -> None:
    package_json = tmp_path / "package.json"
    package_json.write_text(json.dumps(["lint"]))

    assert _package_json_configures_lint(package_json) is False


def test_analyze_repository_returns_sorted_extensions(tmp_path: Path) -> None:
    repo = tmp_path / "analysis"
    repo.mkdir()

    (repo / "README.md").write_text("Hi\n")
    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: CI\n")

    docs_dir = repo / "docs"
    docs_dir.mkdir()
    (docs_dir / "overview.md").write_text("# Docs\n")

    src = repo / "src"
    src.mkdir()
    (src / "main.py").write_text("print('hi')\n")
    (src / "helper.py").write_text("print('hi again')\n")
    (src / "widget.ts").write_text("export {}\n")

    tests_dir = repo / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_widget.py").write_text(
        "def test_widget():\n" "    assert True\n"
    )
    (repo / ".pre-commit-config.yaml").write_text("repos: []\n")

    stats, suggestions = _analyze_repository(repo)

    assert stats["total_files"] >= 4
    assert stats["has_readme"] is True
    assert stats["has_docs"] is True
    assert stats["has_tests"] is True
    assert stats["has_ci_workflows"] is True
    assert stats["has_lint_config"] is True

    extensions = stats["top_extensions"]
    counts = [entry["count"] for entry in extensions]
    assert counts == sorted(counts, reverse=True)
    assert suggestions == []


def test_analyze_repository_reports_missing_assets(tmp_path: Path) -> None:
    repo = tmp_path / "needs-help"
    repo.mkdir()

    src = repo / "src"
    src.mkdir()
    (src / "main.py").write_text("print('hi')\n")

    stats, suggestions = _analyze_repository(repo)

    assert stats["has_readme"] is False
    assert stats["has_docs"] is False
    assert stats["has_ci_workflows"] is False
    assert stats["has_tests"] is False
    assert stats["has_lint_config"] is False

    assert [entry["id"] for entry in suggestions] == [
        "add-tests",
        "configure-ci",
        "add-linting",
        "add-docs",
        "add-readme",
    ]
    category_map: dict[str, str] = {}
    for entry in suggestions:
        category_map[entry["id"]] = entry["category"]
    assert category_map == {
        "add-docs": "docs",
        "add-readme": "docs",
        "add-tests": "fix",
        "add-linting": "chore",
        "configure-ci": "chore",
    }


def test_spin_dry_run_outputs_json_inline(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "inline"
    repo.mkdir()

    args = argparse.Namespace(path=str(repo), dry_run=True, format="json")

    spin(args)

    captured = capsys.readouterr().out
    payload = json.loads(captured)

    assert payload["mode"] == "dry-run"
    assert payload["target"] == str(repo.resolve())
    assert payload["stats"]["has_readme"] is False
    assert payload["stats"]["has_docs"] is False
    assert payload["stats"]["has_lint_config"] is False

    snapshot_categories: dict[str, str] = {}
    snapshot_validations: dict[str, list[str]] = {}
    for item in payload["suggestions"]:
        snapshot_categories[item["id"]] = item["category"]
        snapshot_validations[item["id"]] = item["validation"]
    assert snapshot_categories == {
        "add-docs": "docs",
        "add-readme": "docs",
        "add-tests": "fix",
        "add-linting": "chore",
        "configure-ci": "chore",
    }
    for commands in snapshot_validations.values():
        assert commands
    lint_validation_commands = list(LINT_VALIDATION_COMMANDS)
    assert snapshot_validations["add-linting"] == lint_validation_commands


def test_spin_reports_lockfile_category(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "missing-lockfile"
    repo.mkdir()
    (repo / "package.json").write_text("{}\n")

    args = argparse.Namespace(path=str(repo), dry_run=True, format="json")

    spin(args)

    payload = json.loads(capsys.readouterr().out)
    suggestions = payload["suggestions"]
    lockfile_entry = next(
        item for item in suggestions if item["id"] == "commit-lockfiles"
    )
    assert lockfile_entry["category"] == "chore"


def test_spin_table_format(
    tmp_path: Path,
    capsys: CaptureFixtureStr,
) -> None:
    repo = tmp_path / "table"
    repo.mkdir()

    args = argparse.Namespace(path=str(repo), dry_run=True, format="table")

    spin(args)

    output = capsys.readouterr().out
    assert "Target:" in output
    assert "Stats:" in output
    assert "Index" in output
    assert "add-docs" in output


def test_spin_table_marks_skipped_analyzers(
    tmp_path: Path,
    capsys: CaptureFixtureStr,
) -> None:
    repo = tmp_path / "skipped"
    repo.mkdir()

    args = argparse.Namespace(
        path=str(repo), dry_run=True, format="table", analyzers="none"
    )

    spin(args)

    output = capsys.readouterr().out
    assert "has_readme: skipped" in output
    assert "has_tests: skipped" in output
    assert "has_lint_config: skipped" in output


def test_format_stats_lines_handles_literal_dependency() -> None:
    stats = {
        "total_files": 1,
        "has_readme": True,
        "has_docs": True,
        "has_ci_workflows": True,
        "has_tests": True,
        "dependency_health": "warn",
        "language_mix": [],
    }

    lines = _format_stats_lines(stats)

    assert "dependency_health: warn" in lines[-2]


def test_spin_markdown_format(
    tmp_path: Path,
    capsys: CaptureFixtureStr,
) -> None:
    repo = tmp_path / "markdown"
    repo.mkdir()

    args = argparse.Namespace(path=str(repo), dry_run=True, format="markdown")

    spin(args)

    output = capsys.readouterr().out
    assert "# flywheel spin dry-run" in output
    assert "| Confidence |" in output
    assert "add-docs" in output


@pytest.mark.parametrize("value", [None, "unknown", object()])
def test_format_confidence_handles_non_numeric(value: object) -> None:
    assert main_module._format_confidence(value) == "-"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_format_confidence_handles_non_finite(value: float) -> None:
    assert main_module._format_confidence(value) == "-"


def test_spin_markdown_without_suggestions() -> None:
    stats = {
        "total_files": 4,
        "has_readme": True,
        "has_docs": False,
        "has_ci_workflows": True,
        "has_tests": False,
        "has_lint_config": True,
        "dependency_health": {"status": "ok"},
        "language_mix": [
            {"language": "Python", "count": 3},
            {"language": "TypeScript", "count": 1},
        ],
    }
    result = {
        "target": "demo",
        "mode": "dry-run",
        "stats": stats,
        "suggestions": [],
    }

    markdown = _render_spin_markdown(result)

    assert "language_mix: Python (3), TypeScript (1)" in markdown
    assert "_No suggestions found._" in markdown


def test_spin_table_without_suggestions() -> None:
    stats = {
        "total_files": 2,
        "has_readme": False,
        "has_docs": True,
        "has_ci_workflows": False,
        "has_tests": True,
        "has_lint_config": False,
        "dependency_health": {"status": "warn"},
        "language_mix": [
            {"language": "Python", "count": 1},
            {"language": "JavaScript", "count": 1},
        ],
    }
    result = {
        "target": "demo",
        "mode": "dry-run",
        "stats": stats,
        "suggestions": [],
    }

    table_text = _render_spin_table(result)

    stats_lines = _format_stats_lines(stats)
    for line in stats_lines:
        assert line in table_text
    assert "Suggestions: none found." in table_text


def test_spin_cli_accepts_table_format(tmp_path: Path) -> None:
    repo = tmp_path / "cli-table"
    repo.mkdir()

    output = run_spin_dry_run_text(
        repo,
        "--format",
        "table",
    )

    assert "Index" in output
    assert "Confidence" in output
    assert "add-docs" in output
    assert "0.80" in output or "0.8" in output


def test_spin_cli_accepts_markdown_format(tmp_path: Path) -> None:
    repo = tmp_path / "cli-md"
    repo.mkdir()

    output = run_spin_dry_run_text(
        repo,
        "--format",
        "markdown",
    )

    assert "# flywheel spin dry-run" in output
    assert "| Confidence |" in output


def test_spin_rejects_unknown_format(tmp_path: Path) -> None:
    repo = tmp_path / "cli-invalid"
    repo.mkdir()

    args = argparse.Namespace(
        path=str(repo),
        dry_run=True,
        format="markdownish",
    )

    with pytest.raises(SystemExit) as excinfo:
        spin(args)

    assert "Unsupported format" in str(excinfo.value)
