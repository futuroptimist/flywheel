import hashlib
import os
import subprocess
import sys
from pathlib import Path


def hash_dir(path: Path) -> dict:
    result = {}
    for file in path.rglob("*"):
        if file.is_file():
            data = file.read_bytes()
            result[file.relative_to(path)] = hashlib.md5(data).hexdigest()
    return result


def test_init_idempotent(tmp_path):
    target = tmp_path / "repo"
    cmd = [
        sys.executable,
        "-m",
        "flywheel",
        "init",
        str(target),
        "--language",
        "python",
        "--save-dev",
        "--yes",
    ]
    subprocess.run(cmd, check=True)
    first = hash_dir(target)
    subprocess.run(cmd, check=True)
    second = hash_dir(target)
    assert first == second
    assert (target / "pyproject.toml").exists()
    wf = target / ".github" / "workflows" / "01-lint-format.yml"
    assert wf.exists()


def test_init_copies_dev_tooling(tmp_path):
    target = tmp_path / "repo"
    cmd = [
        sys.executable,
        "-m",
        "flywheel",
        "init",
        str(target),
        "--language",
        "python",
        "--save-dev",
        "--yes",
    ]
    subprocess.run(cmd, check=True)

    precommit = target / ".pre-commit-config.yaml"
    checks = target / "scripts" / "checks.sh"

    assert precommit.exists()
    assert checks.exists()
    assert os.access(checks, os.X_OK)


def test_prompt(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("Hello")
    (tmp_path / "docs").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "pyproject.toml").write_text("[tool]")
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "prompt", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "# Purpose" in result.stdout
    assert "# Repo Snapshot" in result.stdout
    lines = result.stdout.splitlines()
    snapshot_line = next(
        line for line in lines if line.startswith("Top-level entries:")
    )
    for expected in ("README.md", "docs/", "pyproject.toml", "src/"):
        assert expected in snapshot_line


def test_prompt_no_readme(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "prompt", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "No README found." in result.stdout
    snapshot_line = next(
        line
        for line in result.stdout.splitlines()
        if line.startswith("Top-level entries:")
    )
    assert "(no non-hidden files found)" in snapshot_line


def test_prompt_handles_braces(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("Hello {braced} world")
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "prompt", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "{braced}" in result.stdout


def test_prompt_snapshot_truncates(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("Intro")
    for idx in range(12):
        (tmp_path / f"file{idx}.txt").write_text("data")
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "prompt", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    snapshot_line = next(
        line
        for line in result.stdout.splitlines()
        if line.startswith("Top-level entries:")
    )
    assert "… (+" in snapshot_line


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "init" in result.stdout
    assert "crawl" in result.stdout


def test_runbook_cli():
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "runbook"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Stage: bootstrap" in result.stdout
    expected = "- clone: Use the GitHub template and run ./scripts/setup.sh"
    assert expected in result.stdout
