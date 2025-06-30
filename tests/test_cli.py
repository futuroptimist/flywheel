import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI = PROJECT_ROOT / "flywheel.py"


def run_cmd(*args, cwd):
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_init_idempotent(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run_cmd("init", str(repo), "--save-dev", cwd=PROJECT_ROOT)
    assert (repo / ".eslintrc.json").exists()
    # second run should not fail and files remain
    run_cmd("init", str(repo), "--save-dev", cwd=PROJECT_ROOT)
    assert (repo / ".eslintrc.json").exists()


def test_prompt(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("Hello flywheel")
    output = run_cmd("prompt", str(repo), cwd=PROJECT_ROOT)
    assert "Repo Prompt" in output
