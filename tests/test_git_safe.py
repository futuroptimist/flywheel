import os
import subprocess
from pathlib import Path


def test_git_safe_block(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True)
    logfile = Path.home() / ".flywheel" / "unsafe.log"
    if logfile.exists():
        logfile.unlink()
    env = os.environ.copy()
    env["PATH"] = f"{Path.cwd()}/bin:" + env.get("PATH", "")
    result = subprocess.run(
        [
            "git-safe",
            "commit",
            "--no-verify",
            "-m",
            "msg",
        ],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "Refusing" in result.stderr
    assert not logfile.exists()


def test_git_safe_allow(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True)
    logfile = Path.home() / ".flywheel" / "unsafe.log"
    if logfile.exists():
        logfile.unlink()
    env = os.environ.copy()
    env["PATH"] = f"{Path.cwd()}/bin:" + env.get("PATH", "")
    env["FLYWHEEL_ALLOW_NO_VERIFY"] = "1"
    subprocess.run(
        [
            "git-safe",
            "init",
        ],
        cwd=repo,
        env=env,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git-safe",
            "commit",
            "--no-verify",
            "-m",
            "msg",
            "--allow-empty",
        ],
        cwd=repo,
        env=env,
    )
    assert logfile.exists()
