from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


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
