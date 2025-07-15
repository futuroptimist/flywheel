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


def test_badge_patch_percent_request_error(monkeypatch):
    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, *a, **kw):
            raise requests.RequestException("boom")

    crawler = RepoCrawler([], session=Sess())
    assert crawler._badge_patch_percent("foo/bar", "main") is None


def test_patch_coverage_token_and_errors(monkeypatch):
    class Sess:
        def __init__(self):
            self.headers = {}
            self.calls = []

        def get(self, url, **kw):
            self.calls.append((url, kw.get("headers")))
            if "totals" in url:
                raise requests.RequestException("fail")
            if "compare" in url:
                raise ValueError("bad")

    sess = Sess()
    crawler = RepoCrawler([], session=sess)
    monkeypatch.setattr(
        crawler,
        "_recent_commits",
        lambda *a, **kw: ["h", "b"],
    )
    monkeypatch.setenv("CODECOV_TOKEN", "abc")
    monkeypatch.setattr(crawler, "_badge_patch_percent", lambda *a, **kw: 42.0)
    pct = crawler._patch_coverage_from_codecov("foo/bar", "main")
    assert pct == 42.0
    assert sess.calls[0][1]["Authorization"] == "Bearer abc"


def test_patch_coverage_compare_on_error(monkeypatch):
    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, url, **kw):
            if "totals" in url:
                raise ValueError("bad json")
            if "compare" in url:

                class Resp:
                    status_code = 200

                    def json(self):
                        return {"totals": {"patch": {"coverage": 77}}}

                return Resp()

    crawler = RepoCrawler([], session=Sess())
    monkeypatch.setattr(
        crawler,
        "_recent_commits",
        lambda *a, **kw: ["h", "b"],
    )
    pct = crawler._patch_coverage_from_codecov("foo/bar", "main")
    assert pct == 77.0


def test_patch_coverage_compare_request_exception(monkeypatch):
    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, url, **kw):
            if "totals" in url:

                class Resp:
                    status_code = 404

                    def json(self):
                        return {}

                return Resp()
            if "compare" in url:
                raise requests.RequestException("boom")

    crawler = RepoCrawler([], session=Sess())
    monkeypatch.setattr(crawler, "_badge_patch_percent", lambda *a, **kw: None)
    monkeypatch.setattr(
        crawler,
        "_recent_commits",
        lambda *a, **kw: [],
    )
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") is None
