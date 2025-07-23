from pathlib import Path

import flywheel.agents.scanner as scanner


def test_analyze_repo(tmp_path):
    (tmp_path / "a.txt").write_text("1")
    (tmp_path / "b.txt").write_text("2")
    report = scanner.analyze_repo(tmp_path)
    assert "# Report for" in report
    assert "- a.txt" in report
    assert "- b.txt" in report


def test_clone_repo(monkeypatch, tmp_path):
    calls = []
    removed = []

    def fake_run(cmd, check):
        calls.append(cmd)

    def fake_rmtree(path):
        removed.append(path)

    (tmp_path / "old").write_text("1")
    monkeypatch.setattr(scanner.subprocess, "run", fake_run)
    monkeypatch.setattr(scanner.shutil, "rmtree", fake_rmtree)
    scanner.clone_repo("foo/bar", tmp_path)
    assert calls[0][:4] == ["git", "clone", "--depth", "1"]
    assert "foo/bar" in calls[0][4]
    assert removed and removed[0] == tmp_path


def test_main(monkeypatch, tmp_path):
    def fake_clone(repo, dest):
        dest.mkdir()

    def fake_analyze(path):
        return f"report for {path.name}"

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(scanner, "REPOS", ["a/b"])
    monkeypatch.setattr(scanner, "clone_repo", fake_clone)
    monkeypatch.setattr(scanner, "analyze_repo", fake_analyze)
    scanner.main()
    out = Path("reports/a_b.md").read_text()
    assert out == "report for a_b"
