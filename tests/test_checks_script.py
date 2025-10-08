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


def test_checks_script_runs_codespell(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts" / "checks.sh"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log_file = tmp_path / "codespell.log"

    def stub(name: str, body: str = "exit 0") -> None:
        path = bin_dir / name
        path.write_text(f"#!/usr/bin/env bash\n{body}\n")
        path.chmod(0o755)

    stub(
        "codespell",
        f'echo codespell "$@" >> "{log_file}"\nexit 0',
    )
    link_log = tmp_path / "linkchecker.log"

    stub(
        "linkchecker",
        f'echo linkchecker "$@" >> "{link_log}"\nexit 0',
    )

    for cmd in [
        "flake8",
        "isort",
        "black",
        "npm",
        "pytest",
        "bandit",
        "safety",
        "pyspelling",
    ]:
        stub(cmd)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env.get('PATH', '')}"
    env["SKIP_E2E"] = "1"

    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        env=env,
        cwd=script.parent.parent,
    )

    assert result.returncode == 0
    assert log_file.exists()
    logged = log_file.read_text().strip()
    assert logged.startswith("codespell ")
    assert "--ignore-words" in logged

    assert link_log.exists()
    link_logged = link_log.read_text().strip()
    assert link_logged.startswith("linkchecker ")
    assert "--no-warnings" in link_logged
