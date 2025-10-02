import importlib
import sys

from flywheel.repocrawler import RepoInfo


def test_repo_feature_summary_has_pattern_table(monkeypatch, tmp_path):
    module = importlib.import_module("scripts.update_repo_feature_summary")

    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("owner/repo\n")
    out_path = tmp_path / "summary.md"

    info = RepoInfo(
        name="owner/repo",
        branch="main",
        coverage="88%",
        patch_percent=95.0,
        uses_codecov=True,
        has_license=True,
        has_ci=True,
        has_agents=True,
        has_coc=False,
        has_contributing=False,
        has_precommit=False,
        installer="uv",
        latest_commit="deadbee",
        workflow_count=3,
        trunk_green=True,
        stars=5,
        open_issues=1,
        commit_date="2024-01-01",
        dark_pattern_count=2,
        bright_pattern_count=4,
    )

    class DummyCrawler:
        def __init__(self, repos, token=None):
            self.repos = list(repos)

        def crawl(self):
            return [info]

    monkeypatch.setattr(module, "RepoCrawler", DummyCrawler)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_repo_feature_summary",
            "--repos-from",
            str(repo_file),
            "--out",
            str(out_path),
        ],
    )

    module.main()

    content = out_path.read_text()
    assert "## Dark & Bright Pattern Scan" in content
    assert "Dark Patterns" in content and "Bright Patterns" in content
    assert "Dark Patterns counts potential UX anti-patterns" in content
