import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402
import flywheel.__main__ as fm  # noqa: E402


def test_build_parser_commands():
    parser = fm.build_parser()
    sub = parser._subparsers._group_actions[0]
    cmds = set(sub.choices.keys())
    assert {"init", "update", "audit", "prompt"} <= cmds


def test_main_audit(capsys, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    fm.main(["audit", str(repo)])
    out = capsys.readouterr().out
    assert "TODO" in out
