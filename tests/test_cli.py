import hashlib
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


def test_prompt(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("Hello")
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "prompt", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "# Purpose" in result.stdout


def test_prompt_no_readme(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "prompt", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "No README found." in result.stdout


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "flywheel", "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "init" in result.stdout
    assert "crawl" in result.stdout
