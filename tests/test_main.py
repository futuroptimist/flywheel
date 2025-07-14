import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402
import flywheel.__main__ as fm  # noqa: E402


def test_build_parser_commands():
    parser = fm.build_parser()
    sub = parser._subparsers._group_actions[0]
    cmds = set(sub.choices.keys())
    assert {"init", "update", "audit", "prompt", "crawl"} <= cmds


def test_main_audit(capsys, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    fm.main(["audit", str(repo)])
    out = capsys.readouterr().out
    assert "Missing dev tooling files" in out


def test_main_audit_all_present(capsys, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    fm.inject_dev(repo)
    fm.main(["audit", str(repo)])
    out = capsys.readouterr().out
    assert "All dev tooling files present." in out


def test_main_crawl(monkeypatch, tmp_path):
    out = tmp_path / "sum.md"

    class DummyCrawler:
        def __init__(self, repos, token=None):
            self.repos = repos

        def generate_summary(self):
            return "report"

    monkeypatch.setattr(fm, "RepoCrawler", DummyCrawler)
    fm.main(["crawl", "foo/bar", "--output", str(out)])
    assert out.read_text() == "report"
