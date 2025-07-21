import json
import subprocess
import sys
import tempfile
from pathlib import Path


def test_jsonl_mode_and_cache(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("hello")
    cmd = [
        sys.executable,
        "-m",
        "flywheel",
        "prompt",
        str(repo),
        "--mode",
        "jsonl",
    ]
    out1 = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    cache_dir = Path(tempfile.gettempdir()) / "flw-cache"
    logs = list(cache_dir.glob("*.log"))
    assert logs
    (repo / "README.md").write_text("changed")
    out2 = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert out1 == out2
    first = out1.splitlines()[0]
    data = json.loads(first)
    assert "total_lines" in data


def test_human_mode(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "flywheel",
            "prompt",
            str(repo),
            "--mode",
            "human",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "No README found." in result.stdout
