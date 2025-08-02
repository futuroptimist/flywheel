import sys
from pathlib import Path

import pytest

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
    out = capsys.readouterr().out.strip()
    assert out == "All dev tooling files present."


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


def test_main_crawl_no_repos(tmp_path):
    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("")
    out = tmp_path / "sum.md"
    with pytest.raises(SystemExit):
        fm.main(
            [
                "crawl",
                "--repos-file",
                str(repo_file),
                "--output",
                str(out),
            ]
        )


def test_main_crawl_repos_file(monkeypatch, tmp_path):
    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("a/b\nc/d\n")
    out = tmp_path / "sum.md"
    captured = {}

    class DummyCrawler:
        def __init__(self, repos, token=None):
            captured["repos"] = repos

        def generate_summary(self):
            return "report"

    monkeypatch.setattr(fm, "RepoCrawler", DummyCrawler)
    fm.main(
        [
            "crawl",
            "e/f",
            "--repos-file",
            str(repo_file),
            "--output",
            str(out),
        ]
    )
    assert captured["repos"] == ["a/b", "c/d", "e/f"]
