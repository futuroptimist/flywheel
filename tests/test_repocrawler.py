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
                return Resp('[{"sha": "deadbeef"}]', 200)
            return Resp('{"default_branch": "main"}', 200)

        path = url.split("raw.githubusercontent.com/")[-1]
        if path in self.files:
            return Resp(self.files[path], 200)
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
    assert "100%" in out
    assert "**[foo/bar](https://github.com/foo/bar)**" in out
    assert "main" in out
    assert "pip" in out
    assert "deadbee" in out


def test_parse_coverage_none():
    crawler = rc.RepoCrawler([])
    assert crawler._parse_coverage(None) is None


def test_parse_coverage_unknown():
    crawler = rc.RepoCrawler([])
    result = crawler._parse_coverage("partial coverage info")
    assert result == "unknown"


def test_parse_coverage_no_match():
    crawler = rc.RepoCrawler([])
    result = crawler._parse_coverage("nothing here")
    assert result is None


def test_init_with_token():
    session = DummySession({})
    rc.RepoCrawler(["foo/bar"], session=session, token="abc123")
    assert session.headers.get("Authorization") == "Bearer abc123"
