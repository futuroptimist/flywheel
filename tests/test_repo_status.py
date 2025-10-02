import re

import pytest

import src.repo_status as rs


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
            return {"workflow_runs": [{"conclusion": self._conclusion}]}

    def fake_get(url, headers, timeout):
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
            return {"workflow_runs": [{"conclusion": self._conclusion}]}

    def fake_get(url, headers, timeout):
        return Resp(next(conclusions))

    monkeypatch.setattr(rs.requests, "get", fake_get)
    with pytest.raises(RuntimeError):
        rs.fetch_repo_status("owner/repo", attempts=2)


def test_fetch_repo_status_attempts_zero():
    with pytest.raises(ValueError):
        rs.fetch_repo_status("owner/repo", attempts=0)


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
