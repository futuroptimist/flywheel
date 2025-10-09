from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import pytest

import flywheel.__main__ as main_module
from flywheel.__main__ import (
    _analyze_repository,
    _detect_tests,
    _has_ci_workflows,
    _iter_project_files,
    spin,
)


def run_spin_dry_run(path: Path) -> dict:
    cmd = [
        sys.executable,
        "-m",
        "flywheel",
        "spin",
        str(path),
        "--dry-run",
    ]
    completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def test_spin_dry_run_flags_missing_assets(tmp_path: Path) -> None:
    repo = tmp_path / "sample"
    repo.mkdir()

    result = run_spin_dry_run(repo)

    assert result["mode"] == "dry-run"
    stats = result["stats"]
    assert stats["has_readme"] is False
    assert stats["has_ci_workflows"] is False
    assert stats["has_tests"] is False

    suggestion_ids = {entry["id"] for entry in result["suggestions"]}
    assert suggestion_ids == {"add-readme", "add-tests", "configure-ci"}
    categories: dict[str, str] = {}
    for entry in result["suggestions"]:
        categories[entry["id"]] = entry["category"]
    assert categories == {
        "add-readme": "docs",
        "add-tests": "fix",
        "configure-ci": "chore",
    }


def test_spin_dry_run_detects_existing_assets(tmp_path: Path) -> None:
    repo = tmp_path / "project"
    workflows = repo / ".github" / "workflows"
    tests_dir = repo / "tests"
    workflows.mkdir(parents=True)
    tests_dir.mkdir(parents=True)
    repo.mkdir(exist_ok=True)

    (repo / "README.md").write_text("Hello world\n")
    test_code = "def test_sample():\n    assert True\n"
    (tests_dir / "test_sample.py").write_text(test_code)
    (workflows / "ci.yml").write_text("name: CI\n")

    result = run_spin_dry_run(repo)

    stats = result["stats"]
    assert stats["has_readme"] is True
    assert stats["has_ci_workflows"] is True
    assert stats["has_tests"] is True

    assert result["suggestions"] == []


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
    assert any(entry["id"] == "commit-lockfiles" for entry in suggestions)


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


def test_has_ci_workflows_detects_yaml_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    assert _has_ci_workflows(repo) is False

    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "README.txt").write_text("nope\n")

    assert _has_ci_workflows(repo) is False

    (workflows / "ci.yaml").write_text("name: CI\n")

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


def test_analyze_repository_returns_sorted_extensions(tmp_path: Path) -> None:
    repo = tmp_path / "analysis"
    repo.mkdir()

    (repo / "README.md").write_text("Hi\n")
    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: CI\n")

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

    stats, suggestions = _analyze_repository(repo)

    assert stats["total_files"] >= 4
    assert stats["has_readme"] is True
    assert stats["has_tests"] is True
    assert stats["has_ci_workflows"] is True

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
    assert stats["has_ci_workflows"] is False
    assert stats["has_tests"] is False

    assert [entry["id"] for entry in suggestions] == [
        "add-readme",
        "add-tests",
        "configure-ci",
    ]
    category_map: dict[str, str] = {}
    for entry in suggestions:
        category_map[entry["id"]] = entry["category"]
    assert category_map == {
        "add-readme": "docs",
        "add-tests": "fix",
        "configure-ci": "chore",
    }


def test_spin_dry_run_outputs_json_inline(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "inline"
    repo.mkdir()

    args = argparse.Namespace(path=str(repo), dry_run=True)

    spin(args)

    captured = capsys.readouterr().out
    payload = json.loads(captured)

    assert payload["mode"] == "dry-run"
    assert payload["target"] == str(repo.resolve())
    assert payload["stats"]["has_readme"] is False
    snapshot_categories: dict[str, str] = {}
    for item in payload["suggestions"]:
        snapshot_categories[item["id"]] = item["category"]
    assert snapshot_categories == {
        "add-readme": "docs",
        "add-tests": "fix",
        "configure-ci": "chore",
    }
