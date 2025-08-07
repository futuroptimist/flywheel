import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402
import flywheel.repocrawler as rc  # noqa: E402


class DummySession:
    def __init__(self, files):
        self.files = files
        self.headers = {}

    def get(self, url, **kwargs):
        class Resp:
            def __init__(self, text, status):
                self.text = text
                self.status_code = status

            def json(self):
                import json

                return json.loads(self.text)

        if url.startswith("https://api.github.com/repos/"):
            if url.endswith("/commits?per_page=1&sha=main"):
                return Resp(
                    '[{"sha": "deadbeef", "commit": {"author": {"date": '
                    '"2024-01-01T00:00:00Z"}}}]',
                    200,
                )
            if url.endswith("/commits?per_page=2&sha=main"):
                return Resp(
                    '[{"sha": "cafecafe", "commit": {"author": {"date": '
                    '"2024-01-02T00:00:00Z"}}},'
                    '{"sha": "deadbeef", "commit": {"author": {"date": '
                    '"2024-01-01T00:00:00Z"}}}]',
                    200,
                )
            if "/contents/.github/workflows" in url:
                import json

                repo = url.split("repos/")[1].split("/contents")[0]
                branch = url.split("ref=")[-1]
                prefix = f"{repo}/{branch}/.github/workflows/"
                names = [
                    p.split("/")[-1]
                    for p in self.files
                    if p.startswith(prefix)  # noqa: E501
                ]  # noqa: E501
                return Resp(json.dumps([{"name": n} for n in names]), 200)
            return Resp('{"default_branch": "main"}', 200)

        path = url.split("raw.githubusercontent.com/")[-1]
        if path in self.files:
            return Resp(self.files[path], 200)
        if url.startswith("https://codecov.io/api/gh/"):
            return Resp(
                '{"commit": {"totals": {"coverage": 95, "coverage_diff": 73}}}',  # noqa: E501
                200,
            )
        if url.startswith("https://api.codecov.io/api/v2/github/"):
            if "totals" in url or "compare" in url:
                return Resp('{"totals": {"patch": {"coverage": 73}}}', 200)
        if url.startswith("https://img.shields.io/codecov"):
            return Resp("<svg>95%</svg>", 200)
        return Resp("", 404)


def test_generate_summary():
    files = {
        "foo/bar/main/README.md": "100% coverage",
        "foo/bar/main/LICENSE": "",
        "foo/bar/main/.github/workflows/01-lint-format.yml": "",
        "foo/bar/main/AGENTS.md": "",
        "foo/bar/main/CODE_OF_CONDUCT.md": "",
        "foo/bar/main/CONTRIBUTING.md": "",
        "foo/bar/main/.pre-commit-config.yaml": "",
    }
    session = DummySession(files)
    crawler = rc.RepoCrawler(["foo/bar"], session=session)
    out = crawler.generate_summary()
    assert "100%" not in out
    assert "**[foo/bar](https://github.com/foo/bar)**" in out
    assert "main" in out
    assert "pip" in out
    assert "deadbee" in out
    assert (
        "| Repo | Dark Patterns | Bright Patterns | Last-Updated (UTC) |"
        in out  # noqa: E501
    )


def test_parse_coverage_none():
    crawler = rc.RepoCrawler([])
    assert crawler._parse_coverage(None, "foo/bar", "main") is None


def test_parse_coverage_unknown():
    crawler = rc.RepoCrawler([])
    result = crawler._parse_coverage(
        "partial coverage info",
        "foo/bar",
        "main",
    )
    assert result is None


def test_parse_coverage_no_match():
    crawler = rc.RepoCrawler([])
    result = crawler._parse_coverage("nothing here", "foo/bar", "main")
    assert result is None


def test_parse_coverage_codecov():
    crawler = rc.RepoCrawler([], session=DummySession({}))
    # fmt: off
    readme = (
        "![Coverage](" "https://codecov.io/gh/foo/bar/branch/main/" "graph/badge.svg)"  # noqa: E501
    )
    # fmt: on
    result = crawler._parse_coverage(readme, "foo/bar", "main")
    assert result == "95%"


def test_uses_codecov_from_readme():
    sess = DummySession({})
    crawler = rc.RepoCrawler([], session=sess)
    readme = "See https://codecov.io/gh/foo/bar for coverage"
    assert crawler._uses_codecov("foo/bar", "main", readme) is True


def test_uses_codecov_false():
    sess = DummySession({})
    crawler = rc.RepoCrawler([], session=sess)
    assert crawler._uses_codecov("foo/bar", "main", "no badge") is False


def test_uses_codecov_from_config(monkeypatch):
    sess = DummySession({})
    crawler = rc.RepoCrawler([], session=sess)
    monkeypatch.setattr(
        crawler,
        "_has_file",
        lambda r, n, b: n == "codecov.yml",
    )
    assert crawler._uses_codecov("foo/bar", "main", None) is True


def test_uses_codecov_ignores_similar_domains():
    sess = DummySession({})
    crawler = rc.RepoCrawler([], session=sess)
    readme = "See https://not-codecov.io/gh/foo/bar for coverage"
    assert crawler._uses_codecov("foo/bar", "main", readme) is False


def test_init_with_token():
    session = DummySession({})
    rc.RepoCrawler(["foo/bar"], session=session, token="abc123")
    assert session.headers.get("Authorization") == "Bearer abc123"


def test_ci_detection_single_file():
    crawler = rc.RepoCrawler([])
    assert crawler._has_ci({"ci.yml"}) is True


def test_branch_override():
    files = {
        "foo/bar/dev/README.md": "100% coverage",
        "foo/bar/dev/LICENSE": "",
        "foo/bar/dev/.github/workflows/ci.yml": "",
    }
    session = DummySession(files)
    crawler = rc.RepoCrawler(["foo/bar@dev"], session=session)
    info = crawler.crawl()[0]
    assert info.branch == "dev"


def test_generate_summary_installer_variants(monkeypatch):
    info_uv = rc.RepoInfo(
        name="demo/uv",
        branch="main",
        coverage="100%",
        patch_percent=None,
        uses_codecov=True,
        has_license=True,
        has_ci=True,
        has_agents=False,
        has_coc=True,
        has_contributing=True,
        has_precommit=True,
        installer="uv",
        latest_commit="cafec0d",
        workflow_count=1,
        trunk_green=True,
        commit_date="2024-01-01",
    )
    info_partial = info_uv.__class__(
        **{**info_uv.__dict__, "name": "demo/partial", "installer": "partial"}
    )
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(crawler, "crawl", lambda: [info_uv, info_partial])
    summary = crawler.generate_summary()
    assert "🚀 uv" in summary
    assert "🔶 partial" in summary


def test_generate_summary_other_installer(monkeypatch):
    info = rc.RepoInfo(
        name="demo/poetry",
        branch="main",
        coverage="80%",
        patch_percent=None,
        uses_codecov=True,
        has_license=True,
        has_ci=True,
        has_agents=True,
        has_coc=True,
        has_contributing=True,
        has_precommit=True,
        installer="poetry",
        latest_commit="1234567",
        workflow_count=1,
        trunk_green=True,
        commit_date="2024-01-01",
    )
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(crawler, "crawl", lambda: [info])
    summary = crawler.generate_summary()
    assert "poetry" in summary


def test_summary_column_order(monkeypatch):
    info = rc.RepoInfo(
        name="demo/uv",
        branch="main",
        coverage="100%",
        patch_percent=None,
        uses_codecov=True,
        has_license=True,
        has_ci=True,
        has_agents=True,
        has_coc=True,
        has_contributing=True,
        has_precommit=True,
        installer="uv",
        latest_commit="abcdef0",
        workflow_count=1,
        trunk_green=True,
        commit_date="2024-01-01",
    )
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(crawler, "crawl", lambda: [info])
    summary = crawler.generate_summary()
    assert (
        "| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |" in summary
    )  # noqa: E501
    assert (
        "| Repo | Coverage | Patch | Codecov | Installer | Last-Updated (UTC) |"  # noqa: E501
        in summary
    )
    assert (
        "| Repo | License | CI | Workflows | AGENTS.md | Code of Conduct | Contributing | Pre-commit | Last-Updated (UTC) |"  # noqa: E501
        in summary
    )
    assert (
        "| Repo | Dark Patterns | Bright Patterns | Last-Updated (UTC) |"  # noqa: E501
        in summary
    )
    lines = summary.splitlines()
    idx = lines.index(
        "| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |"
    )  # noqa: E501
    row = lines[idx + 2]
    assert "`abcdef0`" in row


def test_patch_coverage_svg():
    crawler = rc.RepoCrawler([], session=DummySession({}))
    pct = crawler._patch_coverage_from_codecov("foo/bar", "main")
    assert pct == 95.0


def test_generate_summary_with_patch(monkeypatch):
    """Row should show ✅ and percentage when patch coverage is known."""

    info = rc.RepoInfo(
        name="demo/repo",
        branch="main",
        coverage="100%",
        patch_percent=73.0,
        uses_codecov=True,
        has_license=True,
        has_ci=True,
        has_agents=False,
        has_coc=True,
        has_contributing=True,
        has_precommit=True,
        installer="uv",
        latest_commit="abcdef1",
        workflow_count=1,
        trunk_green=False,
        commit_date="2024-01-01",
    )
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(crawler, "crawl", lambda: [info])
    lines = crawler.generate_summary().splitlines()
    idx = lines.index(
        "| Repo | Coverage | Patch | Codecov | Installer | Last-Updated (UTC) |"  # noqa: E501
    )
    row = lines[idx + 2]
    assert "❌ (73%)" in row
    assert "(73%)" in row
