import flywheel.agents.scanner as scanner


def test_analyze_repo_sorts_case_insensitive(tmp_path):
    (tmp_path / "a.txt").write_text("hi")
    (tmp_path / "B.txt").write_text("yo")
    report = scanner.analyze_repo(tmp_path)
    lines = [line for line in report.splitlines() if line.startswith("- ")]
    assert lines == ["- a.txt", "- B.txt"]
