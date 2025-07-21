import importlib
from pathlib import Path

import pytest

import flywheel.__main__ as fm


def test_audit_ci_failure(tmp_path):
    with pytest.raises(SystemExit):
        fm.audit_repo(tmp_path, ci=True)


def test_command_key():
    argv = ["init", "repo", "--mode", "jsonl", "--save-dev"]
    assert fm._command_key(argv) == "init repo --save-dev"
    argv2 = ["prompt", "--mode=jsonl"]
    assert fm._command_key(argv2) == "prompt"


def test_sdk_env_generation(monkeypatch):
    monkeypatch.setenv("FLYWHEEL_BUILD", "1")
    mod = importlib.reload(importlib.import_module("flywheel.agent.sdk"))
    path = Path("flywheel/agent_manifest.json")
    assert path.exists()
    _ = mod
    data = path.read_text()
    _ = data
    path.unlink()
