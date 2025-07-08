import pytest
import requests

from flywheel.repocrawler import RepoCrawler, RepoInfo


class DummyResp:
    def __init__(self, status, text="", json_data=None):
        self.status_code = status
        self.text = text
        self._json = json_data

    def json(self):
        if isinstance(self._json, Exception):
            raise self._json
        return self._json


def make_session(mapping):
    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, url, *_, **__):
            for key, resp in mapping.items():
                if key in url:
                    return resp() if callable(resp) else resp
            return DummyResp(404)

    return Sess()


def test_fetch_file_branch_fallback():
    sess = make_session({"main/file.txt": DummyResp(200, "hello")})
    crawler = RepoCrawler([], session=sess)
    assert crawler._fetch_file("demo/repo", "file.txt", "dev") == "hello"


def test_default_branch_errors():
    sess = make_session({"/repos/demo/repo": DummyResp(500)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._default_branch("demo/repo") == "main"

    sess = make_session(
        {
            "/repos/demo/repo": DummyResp(200, json_data=ValueError("boom")),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._default_branch("demo/repo") == "main"


def test_latest_commit_error():
    sess = make_session({"/commits?per_page=1": DummyResp(200, json_data={})})
    crawler = RepoCrawler([], session=sess)
    assert crawler._latest_commit("demo/repo", "main") is None


def test_latest_commit_non_200():
    sess = make_session({"/commits?per_page=1": DummyResp(404)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._latest_commit("demo/repo", "main") is None


def test_list_workflows_error():
    sess = make_session(
        {
            "/contents/.github/workflows": DummyResp(
                200,
                json_data=ValueError("bad"),
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._list_workflows("demo/repo", "main") == set()


def test_list_workflows_non_200():
    sess = make_session({"/contents/.github/workflows": DummyResp(404)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._list_workflows("demo/repo", "main") == set()


def test_coverage_from_codecov_no_match():
    sess = make_session({"codecov": DummyResp(200, "<svg></svg>")})
    crawler = RepoCrawler([], session=sess)
    assert crawler._project_coverage_from_codecov("demo/repo", "main") is None


def test_has_ci_false():
    crawler = RepoCrawler([])
    assert crawler._has_ci({"deploy.yml"}) is False


@pytest.mark.parametrize(
    "snippet,expected",
    [
        ("uv pip install -r req.txt", "uv"),
        ("uv pip install && pip install black", "partial"),
        ("python -m pip install -r requirements.txt", "pip"),
        ("RUN pip3 install uv && uv pip install .", "partial"),
    ],
)
def test_installer_strict(snippet, expected):
    c = RepoCrawler([])
    assert c._detect_installer(snippet) == expected


def test_network_exceptions_handled():
    class ErrSession:
        def __init__(self):
            self.headers = {}

        def get(self, *_, **__):
            raise requests.RequestException("boom")

    c = RepoCrawler([], session=ErrSession())
    assert c._fetch_file("demo/repo", "README.md", "main") is None
    assert c._default_branch("demo/repo") == "main"
    assert c._latest_commit("demo/repo", "main") is None
    assert c._list_workflows("demo/repo", "main") == set()
    assert c._project_coverage_from_codecov("demo/repo", "main") is None


def test_parse_coverage_codecov_fallback(monkeypatch):
    crawler = RepoCrawler([])

    monkeypatch.setattr(
        crawler,
        "_project_coverage_from_codecov",
        lambda *a: None,
    )

    readme = "![Coverage](https://codecov.io/gh/foo/bar/branch/main/badge.svg)"
    result = crawler._parse_coverage(readme, "foo/bar", "main")
    assert result == "unknown"


def test_patch_coverage_not_found():
    """404 or bad response returns None."""

    sess = make_session({"/totals/": DummyResp(404)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") is None


def test_generate_summary_no_patch(monkeypatch):
    """patch=None should render the ❌ symbol (covers else-branch)."""

    info = RepoInfo(
        name="demo/repo",
        branch="main",
        coverage="100%",
        patch_percent=None,
        has_license=True,
        has_ci=True,
        has_agents=False,
        has_coc=True,
        has_contributing=True,
        has_precommit=True,
        installer="uv",
        latest_commit="123cafe",
    )
    crawler = RepoCrawler([])
    monkeypatch.setattr(crawler, "crawl", lambda: [info])
    table = crawler.generate_summary().splitlines()[7]
    assert "| — |" in table
