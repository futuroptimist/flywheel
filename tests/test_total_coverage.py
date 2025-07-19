import requests
import responses

from flywheel.repocrawler import RepoCrawler


@responses.activate
def test_badge_total_success():
    svg = "<svg>98%</svg>"
    responses.add(
        responses.GET,
        "https://codecov.io/gh/foo/bar/branch/main/graph/badge.svg",
        body=svg,
        status=200,
    )
    c = RepoCrawler([])
    assert c._badge_total_percent("foo/bar", "main") == "98%"


@responses.activate
def test_project_coverage_badge_fallback():
    responses.add(
        responses.GET,
        "https://codecov.io/api/gh/foo/bar",
        status=404,
    )
    responses.add(
        responses.GET,
        "https://codecov.io/gh/foo/bar/branch/main/graph/badge.svg",
        body="<svg>88%</svg>",
        status=200,
    )
    c = RepoCrawler([])
    assert c._project_coverage_from_codecov("foo/bar", "main") == "88%"


def test_project_coverage_badge_error(monkeypatch):
    c = RepoCrawler([])

    def boom(*a, **kw):
        raise ValueError("fail")

    monkeypatch.setattr(c, "_badge_total_percent", boom)

    class Sess:
        def __init__(self):
            self.headers = {}

        def get(self, *a, **kw):
            raise requests.RequestException("err")

    c.session = Sess()
    assert c._project_coverage_from_codecov("foo/bar", "main") is None
