from pathlib import Path
from types import SimpleNamespace

import pytest
import requests

import flywheel.repocrawler as rc
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


def test_repo_stats_request_exception():
    class ErrSession:
        def __init__(self):
            self.headers = {}

        def get(self, *_, **__):
            raise requests.RequestException("boom")

    crawler = RepoCrawler([], session=ErrSession())
    assert crawler._repo_stats("demo/repo") == (0, 0)


def test_repo_stats_bad_json():
    sess = make_session(
        {"/repos/demo/repo": DummyResp(200, json_data=ValueError("bad"))}
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._repo_stats("demo/repo") == (0, 0)


def test_init_uses_requests_cache(tmp_path, monkeypatch):
    class FakeSession:
        def __init__(self, path, expire_after):
            self.path = path
            self.expire_after = expire_after
            self.headers = {}

    fake_rc = SimpleNamespace(CachedSession=FakeSession)
    monkeypatch.setattr(rc, "requests_cache", fake_rc)
    monkeypatch.chdir(tmp_path)
    crawler = RepoCrawler([])
    assert isinstance(crawler.session, FakeSession)
    assert crawler.session.path == Path(".cache") / "github-cache"
    assert crawler.session.expire_after == 3600


def test_latest_commit_error():
    sess = make_session({"/commits?per_page=1": DummyResp(200, json_data={})})
    crawler = RepoCrawler([], session=sess)
    assert crawler._latest_commit("demo/repo", "main") == (None, None)


def test_latest_commit_invalid_json():
    sess = make_session(
        {"/commits?per_page=1": DummyResp(200, json_data=ValueError("bad"))}
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._latest_commit("demo/repo", "main") == (None, None)


def test_latest_commit_non_200():
    sess = make_session({"/commits?per_page=1": DummyResp(404)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._latest_commit("demo/repo", "main") == (None, None)


def test_latest_commit_parses_date():
    mapping = {
        "/commits?per_page=1": DummyResp(
            200,
            json_data=[
                {
                    "sha": "deadbeef",
                    "commit": {"author": {"date": "2024-01-02T03:04:05Z"}},
                }
            ],
        )
    }
    sess = make_session(mapping)
    crawler = RepoCrawler([], session=sess)
    sha, date = crawler._latest_commit("demo/repo", "main")
    assert sha == "deadbee"
    assert date == "2024-01-02"


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


def test_coverage_from_codecov_bad_json():
    sess = make_session(
        {
            "codecov": DummyResp(200, json_data=ValueError("boom")),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._project_coverage_from_codecov("demo/repo", "main") is None


def test_coverage_from_codecov_non_200():
    sess = make_session({"codecov": DummyResp(404)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._project_coverage_from_codecov("demo/repo", "main") is None


def test_has_ci_only_deploy_returns_false():
    crawler = RepoCrawler([])
    assert crawler._has_ci({"deploy.yml"}) is False


@pytest.mark.parametrize(
    "snippet,expected",
    [
        ("uv pip install -r req.txt", "uv"),
        ("uv pip install && pip install black", "partial"),
        ("python -m pip install -r requirements.txt", "pip"),
        ("RUN pip3 install uv && uv pip install .", "partial"),
        ("pip3 install -r requirements.txt", "pip"),
    ],
)
def test_installer_strict(snippet, expected):
    c = RepoCrawler([])
    assert c._detect_installer(snippet) == expected


def test_installer_additional():
    c = RepoCrawler([])
    assert c._detect_installer("setup-uv") == "uv"
    assert c._detect_installer("poetry install") == "poetry"
    assert c._detect_installer("pipx install flywheel") == "pipx"
    assert c._detect_installer("echo nothing") == "none"


def test_installer_partial_mix():
    c = RepoCrawler([])
    snippet = """
    uv venv project
    pip install -r requirements.txt
    """
    assert c._detect_installer(snippet) == "partial"


def test_installer_setup_uv_then_pip_is_partial():
    c = RepoCrawler([])
    snippet = """
    uses: astral-sh/setup-uv@v4
    run: pip install -r requirements.txt
    """
    assert c._detect_installer(snippet) == "partial"


def test_network_exceptions_handled():
    class ErrSession:
        def __init__(self):
            self.headers = {}

        def get(self, *_, **__):
            raise requests.RequestException("boom")

    c = RepoCrawler([], session=ErrSession())
    assert c._fetch_file("demo/repo", "README.md", "main") is None
    assert c._default_branch("demo/repo") == "main"
    assert c._latest_commit("demo/repo", "main") == (None, None)
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
    assert result is None


def test_patch_coverage_not_found():
    """404 or bad response returns None."""

    sess = make_session({"/totals/": DummyResp(404)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") is None


def test_patch_coverage_bad_json():
    sess = make_session(
        {
            "codecov": DummyResp(200, json_data=ValueError("boom")),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") is None


def test_generate_summary_no_patch(monkeypatch):
    """patch=None should render the ❌ symbol (covers else-branch)."""

    info = RepoInfo(
        name="demo/repo",
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
        latest_commit="123cafe",
        workflow_count=1,
        trunk_green=None,
        stars=0,
        open_issues=0,
        commit_date="2024-01-01",
    )
    crawler = RepoCrawler([])
    monkeypatch.setattr(crawler, "crawl", lambda: [info])
    lines = crawler.generate_summary().splitlines()
    idx = lines.index(
        "| Repo | Coverage | Patch | Codecov | Installer | Last-Updated (UTC) |"  # noqa: E501
    )
    row = lines[idx + 2]
    assert "| — |" in row


def test_recent_commits_success():
    sess = make_session(
        {
            "/commits?per_page=2&sha=main": DummyResp(
                200,
                json_data=[{"sha": "aa"}, {"sha": "bb"}],
            )
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._recent_commits("demo/repo", "main") == ["aa", "bb"]


def test_recent_commits_invalid_json():
    sess = make_session(
        {"/commits?per_page=2": DummyResp(200, json_data=ValueError("bad"))}
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._recent_commits("demo/repo", "main") == []


def test_recent_commits_non_200():
    sess = make_session({"/commits?per_page=2": DummyResp(500)})
    crawler = RepoCrawler([], session=sess)
    assert crawler._recent_commits("demo/repo", "main") == []


def test_recent_commits_request_exception():
    class ErrSession:
        def __init__(self):
            self.headers = {}

        def get(self, *_, **__):
            raise requests.RequestException("boom")

    crawler = RepoCrawler([], session=ErrSession())
    assert crawler._recent_commits("demo/repo", "main") == []


def test_recent_commits_uses_timeout():
    captured = {}

    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, url, **kwargs):
            captured.update(kwargs)
            return DummyResp(200, json_data=[{"sha": "aa"}])

    crawler = RepoCrawler([], session=Sess())
    assert crawler._recent_commits("demo/repo", "main") == ["aa"]
    assert captured.get("timeout") == 10


@pytest.mark.parametrize("conclusion", ["success", "neutral", "skipped"])
def test_branch_green_actions_pass(conclusion):
    sess = make_session(
        {
            "/actions/runs": DummyResp(
                200,
                json_data={
                    "workflow_runs": [
                        {
                            "conclusion": conclusion,
                            "head_sha": "dead",
                        }
                    ]
                },
            )
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "dead") is True


@pytest.mark.parametrize("conclusion", ["failure", "timed_out", "cancelled"])
def test_branch_green_actions_fail(conclusion):
    sess = make_session(
        {
            "/actions/runs": DummyResp(
                200,
                json_data={
                    "workflow_runs": [
                        {
                            "conclusion": conclusion,
                            "head_sha": "dead",
                        }
                    ]
                },
            )
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "dead") is False


def test_branch_green_actions_incomplete_returns_none():
    sess = make_session(
        {
            "/actions/runs": DummyResp(
                200,
                json_data={
                    "workflow_runs": [
                        {
                            "status": "in_progress",
                            "head_sha": "dead",
                        }
                    ]
                },
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "dead") is None


def test_branch_green_fallback_success():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/cafe/status": DummyResp(
                200,
                json_data={"state": "success"},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "cafe") is True


def test_branch_green_no_status_returns_none():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/nosh/status": DummyResp(
                200,
                json_data={"state": "no_status"},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "nosh") is None


def test_branch_green_pending_status():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/pend/status": DummyResp(
                200,
                json_data={"state": "pending"},
            ),
            "/commits/pend/check-runs": DummyResp(
                200,
                json_data={"check_runs": []},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "pend") is None


def test_branch_green_pending_check_run_returns_none():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/spin/status": DummyResp(
                200,
                json_data={"state": "pending"},
            ),
            "/commits/spin/check-runs": DummyResp(
                200,
                json_data={
                    "check_runs": [
                        {"status": "in_progress", "conclusion": None},
                    ]
                },
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "spin") is None


def test_branch_green_status_incomplete_context_returns_none():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/queue/status": DummyResp(
                200,
                json_data={
                    "state": "failure",
                    "statuses": [
                        {
                            "state": "queued",
                            "context": "build",
                        }
                    ],
                },
            ),
            "/commits/queue/check-runs": DummyResp(200, json_data={"check_runs": []}),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "queue") is None


def test_branch_green_actions_bad_json_fallback():
    """Invalid workflow run JSON should fall back to commit status."""
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data=ValueError("boom")),
            "/commits/cafe/status": DummyResp(
                200,
                json_data={"state": "success"},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "cafe") is True


def test_branch_green_run_sha_mismatch_fallback():
    sess = make_session(
        {
            "/actions/runs": DummyResp(
                200,
                json_data={
                    "workflow_runs": [
                        {
                            "conclusion": "success",
                            "head_sha": "other",
                        }
                    ]
                },
            ),
            "/commits/dead/status": DummyResp(
                200,
                json_data={"state": "success"},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "dead") is True


def test_branch_green_run_no_conclusion_fallback():
    sess = make_session(
        {
            "/actions/runs": DummyResp(
                200,
                json_data={"workflow_runs": [{"head_sha": "dead"}]},
            ),
            "/commits/dead/status": DummyResp(
                200,
                json_data={"state": "success"},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "dead") is True


def test_branch_green_failure_fallback():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/dead/status": DummyResp(
                200,
                json_data={
                    "state": "failure",
                    "statuses": [{"state": "failure", "context": "build"}],
                },
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "dead") is False


def test_branch_green_ignore_coverage_context_success():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/cc/status": DummyResp(
                200,
                json_data={
                    "state": "failure",
                    "statuses": [
                        {"state": "success", "context": "build"},
                        {"state": "failure", "context": "codecov/project"},
                    ],
                },
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "cc") is True


def test_branch_green_checks_api_success():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/chk/status": DummyResp(
                200,
                json_data={"state": "failure"},
            ),
            "/commits/chk/check-runs": DummyResp(
                200,
                json_data={"check_runs": [{"conclusion": "success"}]},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "chk") is True


def test_branch_green_checks_api_failure():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/badchk/status": DummyResp(
                200,
                json_data={"state": "failure"},
            ),
            "/commits/badchk/check-runs": DummyResp(
                200,
                json_data={"check_runs": [{"conclusion": "failure"}]},
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "badchk") is False


def test_branch_green_checks_api_mixed_pending_returns_none():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/mixed/status": DummyResp(
                200,
                json_data={
                    "state": "failure",
                    "statuses": [],
                },
            ),
            "/commits/mixed/check-runs": DummyResp(
                200,
                json_data={
                    "check_runs": [
                        {
                            "status": "completed",
                            "conclusion": "success",
                        },
                        {
                            "status": "in_progress",
                            "conclusion": None,
                        },
                    ]
                },
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "mixed") is None


def test_branch_green_checks_api_pending_returns_none():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/wait/status": DummyResp(
                200,
                json_data={
                    "state": "failure",
                    "statuses": [],
                },
            ),
            "/commits/wait/check-runs": DummyResp(
                200,
                json_data={
                    "check_runs": [
                        {
                            "status": "queued",
                            "conclusion": None,
                        }
                    ]
                },
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "wait") is None


def test_branch_green_status_bad_json():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/bad/status": DummyResp(
                200,
                json_data=ValueError("boom"),
            ),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "bad") is False


def test_branch_green_status_non_200():
    sess = make_session(
        {
            "/actions/runs": DummyResp(200, json_data={"workflow_runs": []}),
            "/commits/miss/status": DummyResp(404),
        }
    )
    crawler = RepoCrawler([], session=sess)
    assert crawler._branch_green("demo/repo", "main", "miss") is False


def test_branch_green_request_exception():
    class ErrSession:
        def __init__(self):
            self.headers = {}

        def get(self, *_, **__):
            raise requests.RequestException("boom")

    crawler = RepoCrawler([], session=ErrSession())
    assert crawler._branch_green("demo/repo", "main", "dead") is False


def test_branch_green_no_sha():
    crawler = RepoCrawler([])
    assert crawler._branch_green("demo/repo", "main", "") is None
