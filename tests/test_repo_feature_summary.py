from pathlib import Path


def test_repo_feature_summary_trunk_legend_mentions_na():
    text = Path("docs/repo-feature-summary.md").read_text()
    expected = (
        "The Trunk column shows ✅ when CI succeeded, ❌ when it failed, "
        "and n/a when CI is missing or still running."
    )
    assert expected in text
