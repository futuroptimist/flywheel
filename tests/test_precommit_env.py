import os
import subprocess


def test_checks_sh_skips_e2e_when_pre_commit(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for cmd in [
        "npm",
        "npx",
        "flake8",
        "isort",
        "black",
        "pytest",
        "bandit",
        "safety",
        "pyspelling",
        "linkchecker",
    ]:
        script_path = bin_dir / cmd
        script_path.write_text("#!/bin/sh\nexit 0\n")
        script_path.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["PRE_COMMIT"] = "1"

    result = subprocess.run(
        ["bash", "scripts/checks.sh"], capture_output=True, text=True, env=env
    )
    assert "Skipping Playwright installation and e2e tests" in result.stderr
    assert result.returncode == 0
