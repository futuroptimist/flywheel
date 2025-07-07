import requests

from flywheel.repocrawler import RepoCrawler


def test_handles_shields_timeout(monkeypatch):
    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, *a, **kw):
            raise requests.Timeout

    crawler = RepoCrawler([], session=Sess())
    pct = crawler._parse_coverage(
        "![Coverage](https://codecov.io/gh/foo/bar/branch/main/badge.svg)",
        "foo/bar",
        "main",
    )
    assert pct == "unknown"
