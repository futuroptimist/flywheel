from pathlib import Path

from flywheel.agents.scanner import analyze_repo


def test_analyze_repo_trailing_newline(tmp_path: Path) -> None:
    """Report ends with newline and skips hidden files and directories."""
    (tmp_path / "B.txt").write_text("b")
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / ".hidden").write_text("secret")
    (tmp_path / "dir").mkdir()

    report = analyze_repo(tmp_path)

    assert report.endswith("\n")
    lines = report.splitlines()
    assert "- a.txt" in lines
    assert "- B.txt" in lines
    assert "- .hidden" not in lines
    assert "- dir" not in lines
