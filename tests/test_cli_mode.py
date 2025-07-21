import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


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


def test_main_direct(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    import io

    from flywheel.__main__ import main

    monkeypatch.chdir(repo)
    monkeypatch.setattr(
        sys, "argv", ["flywheel", "prompt", str(repo), "--mode", "human"]
    )
    buf = io.StringIO()
    from contextlib import redirect_stdout

    with redirect_stdout(buf):
        main()
    out = buf.getvalue()
    assert "No README found." in out


def test_command_key():
    from flywheel.__main__ import _command_key

    assert _command_key(["prompt", "--mode", "jsonl"]) == "prompt"
    assert _command_key(["prompt", "--mode=jsonl"]) == "prompt"
    assert _command_key(["prompt", "--other", "x"]) == "prompt --other x"


def test_audit_repo_ci_exit(tmp_path):
    from flywheel.__main__ import audit_repo

    target = tmp_path / "repo"
    target.mkdir()
    with pytest.raises(SystemExit):
        audit_repo(target, ci=True)
