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


def test_main_crawl_creates_parent_dirs(monkeypatch, tmp_path):
    out = tmp_path / "nested" / "sum.md"

    class DummyCrawler:
        def __init__(self, repos, token=None):
            self.repos = repos

        def generate_summary(self):
            return "report"

    monkeypatch.setattr(fm, "RepoCrawler", DummyCrawler)
    fm.main(["crawl", "foo/bar", "--output", str(out)])
    assert out.read_text() == "report"


def test_main_crawl_deduplicates_repos(monkeypatch, tmp_path):
    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("foo/bar\nbaz/qux\n")
    out = tmp_path / "sum.md"
    seen = {}

    class DummyCrawler:
        def __init__(self, repos, token=None):
            seen["repos"] = list(repos)

        def generate_summary(self):
            return "report"

    monkeypatch.setattr(fm, "RepoCrawler", DummyCrawler)
    fm.main(
        [
            "crawl",
            "baz/qux",
            "foo/bar",
            "extra/repo",
            "--repos-file",
            str(repo_file),
            "--output",
            str(out),
        ]
    )
    assert out.read_text() == "report"
    assert seen["repos"] == ["foo/bar", "baz/qux", "extra/repo"]


def test_main_crawl_branch_override_prefers_latest(monkeypatch, tmp_path):
    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("foo/bar@alpha\nfoo/bar\nfoo/bar@main\n")
    out = tmp_path / "sum.md"
    seen: dict[str, list[str]] = {}

    class DummyCrawler:
        def __init__(self, repos, token=None):
            seen["repos"] = list(repos)

        def generate_summary(self):
            return "report"

    monkeypatch.setattr(fm, "RepoCrawler", DummyCrawler)
    fm.main(
        [
            "crawl",
            "foo/bar@beta",
            "--repos-file",
            str(repo_file),
            "--output",
            str(out),
        ]
    )
    assert out.read_text() == "report"
    assert seen["repos"] == ["foo/bar@beta"]


def test_main_crawl_skips_blank_and_branch_only_specs(monkeypatch, tmp_path):
    out = tmp_path / "summary.md"
    seen: dict[str, list[str]] = {}

    class DummyCrawler:
        def __init__(self, repos, token=None):
            seen["repos"] = list(repos)

        def generate_summary(self):
            return "report"

    monkeypatch.setattr(fm, "RepoCrawler", DummyCrawler)
    missing_list = tmp_path / "missing.txt"
    fm.main(
        [
            "crawl",
            "   ",
            "@dev",
            "foo/bar",
            "--repos-file",
            str(missing_list),
            "--output",
            str(out),
        ]
    )

    assert out.read_text() == "report"
    assert seen["repos"] == ["foo/bar"]


def test_merge_repo_specs_skips_blank_entries():
    merged = fm._merge_repo_specs(
        [
            "   ",
            "@main",
            "foo/bar",
            "foo/bar@beta",
        ]
    )
    assert merged == ["foo/bar@beta"]


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
