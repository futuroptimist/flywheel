import importlib
import runpy
import sys
from pathlib import Path

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


def test_update_repo_feature_summary_cli_execution(monkeypatch, tmp_path):
    root = Path(__file__).resolve().parents[1]
    stripped_path = list(
        filter(
            lambda entry: Path(entry).resolve() != root,
            sys.path,
        )
    )
    monkeypatch.setattr(sys, "path", stripped_path)
    for name in [
        "flywheel",
        "flywheel.repocrawler",
        "scripts.update_repo_feature_summary",
    ]:
        sys.modules.pop(name, None)

    namespace = runpy.run_path(
        str(root / "scripts" / "update_repo_feature_summary.py"),
        run_name="not_main",
    )

    class DummyInfo:
        def __init__(self):
            self.name = "owner/repo"
            self.branch = "main"
            self.coverage = "100%"
            self.patch_percent = 95.0
            self.uses_codecov = True
            self.has_license = True
            self.has_ci = True
            self.has_agents = True
            self.has_coc = True
            self.has_contributing = True
            self.has_precommit = True
            self.installer = "uv"
            self.latest_commit = "deadbee"
            self.workflow_count = 3
            self.trunk_green = True
            self.stars = 5
            self.open_issues = 1
            self.commit_date = "2024-01-01"
            self.dark_pattern_count = 0
            self.bright_pattern_count = 1

    class DummyCrawler:
        def __init__(self, repos, token=None):
            self.repos = list(repos)

        def crawl(self):
            return [DummyInfo()]

    namespace["RepoCrawler"] = DummyCrawler

    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("owner/repo\n")
    out_path = tmp_path / "summary.md"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_repo_feature_summary.py",
            "--repos-from",
            str(repo_file),
            "--out",
            str(out_path),
        ],
    )

    namespace["main"]()

    assert out_path.exists()
    content = out_path.read_text()
    assert "Dark Patterns" in content
