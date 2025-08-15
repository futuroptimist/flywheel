import runpy
import subprocess
from pathlib import Path

import flywheel.agents.scanner as scanner


def test_clone_repo(monkeypatch, tmp_path):
    (tmp_path / "dest").mkdir()
    calls = []

    def fake_run(cmd, check):
        calls.append(cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    scanner.clone_repo("foo/bar", tmp_path / "dest")
    assert calls[0][:4] == ["git", "clone", "--depth", "1"]


def test_clone_repo_overwrites_file(monkeypatch, tmp_path):
    dest = tmp_path / "dest"
    dest.write_text("x")
    calls = []

    def fake_run(cmd, check):
        calls.append(cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    scanner.clone_repo("foo/bar", dest)
    assert calls[0][:4] == ["git", "clone", "--depth", "1"]
    assert not dest.exists()


def test_analyze_repo(tmp_path):
    (tmp_path / "a.txt").write_text("hi")
    (tmp_path / "b.md").write_text("yo")
    report = scanner.analyze_repo(tmp_path)
    assert "- a.txt" in report
    assert "- b.md" in report


def test_analyze_repo_skips_directories(tmp_path):
    (tmp_path / "a.txt").write_text("hi")
    (tmp_path / "sub").mkdir()
    report = scanner.analyze_repo(tmp_path)
    assert "- sub" not in report


def test_analyze_repo_skips_hidden_files(tmp_path):
    (tmp_path / "a.txt").write_text("hi")
    (tmp_path / ".secret").write_text("nope")
    report = scanner.analyze_repo(tmp_path)
    assert "- a.txt" in report
    assert "- .secret" not in report


def test_analyze_repo_skips_symlinks(tmp_path):
    target = tmp_path / "real.txt"
    target.write_text("hi")
    (tmp_path / "link.txt").symlink_to(target)
    report = scanner.analyze_repo(tmp_path)
    assert "- real.txt" in report
    assert "- link.txt" not in report


def test_main(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    def fake_clone(repo, dest):
        dest.mkdir()

    def fake_analyze(path):
        return f"report for {path.name}"

    monkeypatch.setattr(scanner, "REPOS", ["foo/bar"])
    monkeypatch.setattr(scanner, "clone_repo", fake_clone)
    monkeypatch.setattr(scanner, "analyze_repo", fake_analyze)

    scanner.main()
    out = Path("reports/foo_bar.md")
    assert out.read_text() == "report for foo_bar"


def test_run_module(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(scanner, "REPOS", [])
    runpy.run_module("flywheel.agents.scanner", run_name="__main__")
