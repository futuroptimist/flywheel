from flywheel.repocrawler import format_coverage


def test_format_coverage_variants():
    assert format_coverage("100%") == "✔️"
    assert format_coverage("(100%)") == "✔️"
    assert format_coverage("57%") == "57 %"
    assert format_coverage("(57%)") == "57 %"
    assert format_coverage(None) == "❌"
