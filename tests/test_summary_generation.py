from flywheel.repocrawler import RepoCrawler


def test_summary_generation(monkeypatch):
    crawler = RepoCrawler(["foo/bar"])
    monkeypatch.setattr(crawler, "_parse_coverage", lambda *a, **kw: "88%")
    monkeypatch.setattr(
        crawler,
        "_patch_coverage_from_codecov",
        lambda *a, **kw: 95.0,
    )
    monkeypatch.setattr(crawler, "_default_branch", lambda *a, **kw: "main")
    monkeypatch.setattr(crawler, "_fetch_file", lambda *a, **kw: "")
    monkeypatch.setattr(crawler, "_list_workflows", lambda *a, **kw: set())
    monkeypatch.setattr(crawler, "_latest_commit", lambda *a, **kw: "deadbee")
    monkeypatch.setattr(crawler, "_branch_green", lambda *a, **kw: True)
    monkeypatch.setattr(crawler, "_detect_installer", lambda *a, **kw: "uv")
    monkeypatch.setattr(crawler, "_has_file", lambda *a, **kw: True)

    summary = crawler.generate_summary()
    assert "| Repo | Coverage | Patch | Codecov | Installer |" in summary
    assert "(95%)" in summary
    assert "—" not in summary
    assert "| Repo | Dark Patterns | Bright Patterns |" in summary
