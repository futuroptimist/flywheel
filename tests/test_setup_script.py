from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SETUP_SCRIPT = REPO_ROOT / "scripts" / "setup.sh"


@pytest.mark.skipif(not SETUP_SCRIPT.exists(), reason="setup script missing")
def test_setup_script_scaffolds_local_directory(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()

    scripts_dir = repo / "scripts"
    scripts_dir.mkdir()

    # Copy the setup script into the temporary repo.
    shutil.copy2(SETUP_SCRIPT, scripts_dir / "setup.sh")

    # Provide a minimal .gitignore and README so the script has files to touch.
    gitignore = repo / ".gitignore"
    gitignore.write_text("node_modules/\n")
    readme = repo / "README.md"
    readme.write_text("Welcome to __OWNER__/__REPO__\n")

    subprocess.run(
        ["bash", "scripts/setup.sh", "alice", "demo"],
        cwd=repo,
        check=True,
    )

    local_dir = repo / ".local"
    assert local_dir.is_dir(), "setup script should create .local directory"

    readme_template = local_dir / "README.md"
    readme_message = "setup script should create local README template"
    assert readme_template.is_file(), readme_message

    env_example = local_dir / "settings.env.example"
    env_message = "setup script should create env example template"
    assert env_example.is_file(), env_message

    gitignore_lines = gitignore.read_text().splitlines()
    gitignore_message = ".local directory should be gitignored"
    assert ".local/" in gitignore_lines, gitignore_message
