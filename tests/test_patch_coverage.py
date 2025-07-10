import textwrap

import requests
import responses

from flywheel.repocrawler import RepoCrawler


@responses.activate
def test_badge_fallback():
    svg = textwrap.dedent(
        """
        <svg><text x='0' y='15'>95%</text></svg>
        """
    )
    responses.add(
        responses.GET,
        "https://img.shields.io/codecov/patch/github/foo/bar/main.svg",
        body=svg,
        status=200,
    )
    crawler = RepoCrawler([])
    pct = crawler._badge_patch_percent("foo/bar", "main")
    assert pct == 95.0


def test_badge_patch_network_error(monkeypatch):
    class ErrSession:
        def __init__(self):
            self.headers = {}

        def get(self, *a, **kw):
            raise requests.RequestException("boom")

    crawler = RepoCrawler([], session=ErrSession())
    assert crawler._badge_patch_percent("foo/bar", "main") is None


def test_patch_coverage_network_fallback(monkeypatch):
    class ErrSession:
        def __init__(self):
            self.headers = {}

        def get(self, *a, **kw):
            raise requests.RequestException("fail")

    crawler = RepoCrawler([], session=ErrSession())
    monkeypatch.setattr(crawler, "_badge_patch_percent", lambda *a: 88.0)
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") == 88.0


def test_patch_coverage_json_error(monkeypatch):
    class BadResp:
        status_code = 200

        def json(self):
            raise ValueError("bad")

    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, *a, **kw):
            return BadResp()

    crawler = RepoCrawler([], session=Sess())
    monkeypatch.setattr(crawler, "_badge_patch_percent", lambda *a: 77.0)
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") == 77.0


def test_patch_coverage_with_token(monkeypatch):
    data = {"totals": {"patch": {"coverage": 99}}}

    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, url, headers=None, timeout=10):
            assert headers.get("Authorization") == "Bearer token123"

            class Resp:
                status_code = 200

                def json(self_inner):
                    return data

            return Resp()

    monkeypatch.setenv("CODECOV_TOKEN", "token123")
    crawler = RepoCrawler([], session=Sess())
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") == 99.0


def test_patch_coverage_compare_success():
    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, url, headers=None, timeout=10):
            class Resp:
                def __init__(self, status, data=None):
                    self.status_code = status
                    self._data = data

                def json(self):
                    return self._data or {}

            if "totals" in url:
                return Resp(500)
            return Resp(200, {"totals": {"patch": {"coverage": 66}}})

    crawler = RepoCrawler([], session=Sess())
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") == 66.0
