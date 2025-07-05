import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402
import flywheel.repocrawler as rc  # noqa: E402


class DummySession:
    def __init__(self, files):
        self.files = files

    def get(self, url):
        class Resp:
            def __init__(self, text, status):
                self.text = text
                self.status_code = status

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
    assert "pip" in out
