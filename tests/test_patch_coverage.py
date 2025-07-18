import textwrap

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


@responses.activate
def test_badge_non_200():
    responses.add(
        responses.GET,
        "https://img.shields.io/codecov/patch/github/foo/bar/main.svg",
        status=404,
    )
    crawler = RepoCrawler([])
    assert crawler._badge_patch_percent("foo/bar", "main") is None


@responses.activate
def test_patch_coverage_success():
    responses.add(
        responses.GET,
        "https://codecov.io/api/gh/foo/bar",
        json={"commit": {"totals": {"coverage_diff": 95}}},
        status=200,
    )
    crawler = RepoCrawler([])
    assert crawler._patch_coverage_from_codecov("foo/bar", "main") == 95.0
