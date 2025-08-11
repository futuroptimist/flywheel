import os
import subprocess
from pathlib import Path


def test_checks_script_skips_missing_security_tools(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts" / "checks.sh"
    env = os.environ.copy()
    env["RUN_SECURITY_ONLY"] = "1"
    env["PATH"] = "/usr/bin:/bin"
    # ensure bandit and safety are absent
    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert "bandit not installed" in result.stdout
    assert "safety not installed" in result.stdout


def test_checks_script_skips_missing_linkchecker(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts" / "checks.sh"
    env = os.environ.copy()
    env["RUN_DOCS_ONLY"] = "1"
    env["PATH"] = "/usr/bin:/bin"
    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert "linkchecker not installed" in result.stdout
