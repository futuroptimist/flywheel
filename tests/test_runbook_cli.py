import argparse
from pathlib import Path

import pytest

from flywheel.__main__ import runbook


class DummyArgs(argparse.Namespace):
    def __init__(self, file: Path):
        super().__init__(file=file)


def test_runbook_renders_tasks(tmp_path, capsys):
    runbook_path = tmp_path / "custom.yml"
    runbook_path.write_text("""
workflow:
  - stage: alpha
    tasks:
      - id: alpha-1
        description: first task
      - id: alpha-2
      - description: lonely description
      - string task
  - beta stage
""".strip())

    runbook(DummyArgs(runbook_path))

    captured = capsys.readouterr().out.splitlines()
    assert captured[0] == "Stage: alpha"
    assert "- alpha-1: first task" in captured
    assert "- alpha-2" in captured
    assert "- lonely description" in captured
    assert "- string task" in captured
    assert "Stage: beta stage" in captured


def test_runbook_missing_file(tmp_path):
    missing = tmp_path / "missing.yml"

    with pytest.raises(SystemExit) as exc:
        runbook(DummyArgs(missing))

    assert str(exc.value) == f"Runbook file not found: {missing}"
