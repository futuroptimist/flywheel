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
