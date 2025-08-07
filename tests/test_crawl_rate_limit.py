from flywheel.repocrawler import RepoCrawler


class DummyResp:
    def __init__(self, status, text="", json_data=None):
        self.status_code = status
        self.text = text
        self._json = json_data or {}

    def json(self):
        return self._json


class RateLimitSession:
    def __init__(self, limit):
        self.limit = limit
        self.count = 0
        self.headers = {}

    def get(self, url, *_, **__):
        self.count += 1
        if self.count > self.limit:
            return DummyResp(403)
        if "commits?per_page=1" in url:
            data = [
                {
                    "sha": "deadbeef",
                    "commit": {"author": {"date": "2024-01-02T03:04:05Z"}},
                }
            ]
            return DummyResp(200, json_data=data)
        if "/repos/" in url:
            return DummyResp(200, json_data={"default_branch": "main"})
        return DummyResp(200, json_data={})


def test_crawl_fetches_commits_before_limit(monkeypatch):
    sess = RateLimitSession(limit=10)
    crawler = RepoCrawler(["foo/one", "foo/two"], session=sess)
    monkeypatch.setattr(crawler, "_list_workflows", lambda *a, **k: set())
    monkeypatch.setattr(crawler, "_parse_coverage", lambda *a, **k: "100%")
    monkeypatch.setattr(crawler, "_uses_codecov", lambda *a, **k: True)
    monkeypatch.setattr(
        crawler,
        "_patch_coverage_from_codecov",
        lambda *a, **k: 95.0,
    )
    monkeypatch.setattr(crawler, "_detect_installer", lambda *a, **k: "uv")
    monkeypatch.setattr(crawler, "_detect_dark_patterns", lambda *a, **k: 0)
    monkeypatch.setattr(crawler, "_detect_bright_patterns", lambda *a, **k: 0)
    monkeypatch.setattr(crawler, "_has_file", lambda *a, **k: False)
    monkeypatch.setattr(crawler, "_has_ci", lambda *a, **k: False)
    monkeypatch.setattr(crawler, "_branch_green", lambda *a, **k: True)

    def fake_fetch(repo, path, branch):
        sess.get(f"https://example.com/{repo}/{path}")
        return ""

    monkeypatch.setattr(crawler, "_fetch_file", fake_fetch)

    infos = crawler.crawl()
    assert infos[0].latest_commit == "deadbee"
    assert infos[1].latest_commit == "deadbee"
