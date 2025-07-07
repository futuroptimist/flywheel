import subprocess
import sys


def test_update_cli(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    cmd = [sys.executable, "-m", "flywheel", "update", str(repo)]
    subprocess.run(cmd, check=True)
    subprocess.run(cmd, check=True)
    wf = repo / ".github" / "workflows" / "01-lint-format.yml"
    assert wf.exists()
