from pathlib import Path


def test_repo_feature_summary_has_no_na():
    text = Path("docs/repo-feature-summary.md").read_text().lower()
    assert "n/a" not in text
