import re
import sys

import pytest

import src.repo_status as rs
from flywheel import status_helper


def test_status_to_emoji():
    assert rs.status_to_emoji("success") == "✅"
    assert rs.status_to_emoji("neutral") == "✅"
    assert rs.status_to_emoji("skipped") == "✅"
    assert rs.status_to_emoji("failure") == "❌"
    assert rs.status_to_emoji(None) == "❓"
    assert rs.status_to_emoji("Success") == "✅"
    assert rs.status_to_emoji("FAILURE") == "❌"


def test_status_to_emoji_non_string():
    assert rs.status_to_emoji(42) == "❌"


def test_fetch_repo_status_success(monkeypatch):
    class Resp:
        def __init__(self, conclusion):
            self._conclusion = conclusion

        def raise_for_status(self):
            pass

        def json(self):
            if self._conclusion is None:
                return {"default_branch": "main"}
            return {"workflow_runs": [{"conclusion": self._conclusion}]}

    def fake_get(url, headers, timeout, params=None):
        if url == "https://api.github.com/repos/owner/repo":
            return Resp(None)
        assert params == {
            "per_page": 1,
            "status": "completed",
            "branch": "main",
        }
        return Resp("success")

    monkeypatch.setattr(rs.requests, "get", fake_get)
    assert rs.fetch_repo_status("owner/repo") == "✅"


def test_fetch_repo_status_inconsistent(monkeypatch):
    conclusions = iter(["success", "failure"])

    class Resp:
        def __init__(self, conclusion):
            self._conclusion = conclusion

        def raise_for_status(self):
            pass

        def json(self):
            if self._conclusion is None:
                return {"default_branch": "main"}
            return {"workflow_runs": [{"conclusion": self._conclusion}]}

    def fake_get(url, headers, timeout, params=None):
        if url == "https://api.github.com/repos/owner/repo":
            return Resp(None)
        return Resp(next(conclusions))

    monkeypatch.setattr(rs.requests, "get", fake_get)
    with pytest.raises(RuntimeError):
        rs.fetch_repo_status("owner/repo", attempts=2)


def test_fetch_repo_status_uses_default_branch(monkeypatch):
    requests_made = []

    class Resp:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    def fake_get(url, headers, timeout, params=None):
        requests_made.append((url, params))
        if url == "https://api.github.com/repos/owner/repo":
            return Resp({"default_branch": "stable"})
        # A failed pull-request run may be newer than this run, but must not
        # affect a repository's default-branch health marker.
        return Resp({"workflow_runs": [{"conclusion": "success"}]})

    monkeypatch.setattr(rs.requests, "get", fake_get)

    assert rs.fetch_repo_status("owner/repo", attempts=1) == "✅"
    assert requests_made == [
        ("https://api.github.com/repos/owner/repo", None),
        (
            "https://api.github.com/repos/owner/repo/actions/runs",
            {
                "per_page": 1,
                "status": "completed",
                "branch": "stable",
            },
        ),
    ]


@pytest.mark.parametrize("default_branch", [None, ""])
def test_fetch_requires_default_branch(monkeypatch, default_branch):
    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"default_branch": default_branch}

    monkeypatch.setattr(rs.requests, "get", lambda *args, **kwargs: Resp())

    message = "Could not resolve the default branch"
    with pytest.raises(RuntimeError, match=message):
        rs.fetch_repo_status("owner/repo")


def test_fetch_repo_status_attempts_zero():
    with pytest.raises(ValueError):
        rs.fetch_repo_status("owner/repo", attempts=0)


def test_fetch_repo_status_with_token_and_branch(monkeypatch):
    captured = {}

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"workflow_runs": []}

    def fake_get(url, headers, timeout, params=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["params"] = params
        return Resp()

    monkeypatch.setattr(rs.requests, "get", fake_get)

    emoji = rs.fetch_repo_status(
        "owner/repo", token="abc123", branch="release#1&hot+fix"
    )

    assert emoji == "❓"
    assert captured["headers"]["Authorization"] == "Bearer abc123"
    assert captured["params"] == {
        "per_page": 1,
        "status": "completed",
        "branch": "release#1&hot+fix",
    }


def test_update_readme(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    readme.write_text("## Related Projects\n- https://github.com/a/b\n")

    monkeypatch.setattr(rs, "fetch_repo_status", lambda *args, **kwargs: "✅")

    rs.update_readme(readme)
    data = readme.read_text().splitlines()
    assert data[1].startswith("- ✅ ")
    assert re.search(r"https://github.com/a/b", data[1])


def test_cli_updates_readme(monkeypatch, tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# Title",
                "",
                "## Related Projects",
                "- https://github.com/example/repo",
                "",
            ]
        )
    )

    captured = {}

    def fake_fetch(repo, token=None, branch=None, attempts=2):
        captured["params"] = {
            "repo": repo,
            "token": token,
            "branch": branch,
            "attempts": attempts,
        }
        return "✅"

    monkeypatch.setattr(rs, "fetch_repo_status", fake_fetch)

    rs.main(["--readme", str(readme), "--attempts", "3"])

    assert captured["params"] == {
        "repo": "example/repo",
        "token": None,
        "branch": None,
        "attempts": 3,
    }
    lines = readme.read_text().splitlines()
    assert lines[3] == "- ✅ https://github.com/example/repo"


def test_cli_attempt_validation(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("## Related Projects\n")

    with pytest.raises(SystemExit):
        rs.main(["--readme", str(readme), "--attempts", "0"])


def test_get_fetch_repo_status_without_shim(monkeypatch):
    monkeypatch.delitem(sys.modules, "src.repo_status", raising=False)

    fetch = status_helper._get_fetch_repo_status()

    assert fetch is status_helper.fetch_repo_status


def test_update_readme_stops_at_next_section(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    readme.write_text(
        "\n".join(
            [
                "## Related Projects",
                "- https://github.com/example/repo",
                "## Another Section",
                "- untouched",
            ]
        )
    )

    calls = []

    def fake_fetch(repo, token=None, branch=None, attempts=2):
        calls.append(repo)
        return "✅"

    monkeypatch.setattr(rs, "fetch_repo_status", fake_fetch)

    rs.update_readme(readme)

    lines = readme.read_text().splitlines()
    assert lines[1] == "- ✅ https://github.com/example/repo"
    assert lines[2] == "## Another Section"
    assert calls == ["example/repo"]
