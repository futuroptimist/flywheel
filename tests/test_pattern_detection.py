import flywheel.repocrawler as rc


def test_dark_bright_detection(monkeypatch):
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(
        crawler,
        "_list_files",
        lambda repo, branch: ["index.js", "README.md"],
    )
    monkeypatch.setattr(
        crawler,
        "_fetch_file",
        lambda repo, path, branch: (
            "onbeforeunload" if path == "index.js" else "delete account"
        ),
    )
    assert crawler._detect_dark_patterns("foo/bar", "main") == 1
    assert crawler._detect_bright_patterns("foo/bar", "main") == 1


def test_pattern_detection_skips(monkeypatch):
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(
        crawler,
        "_list_files",
        lambda repo, branch: ["image.png", "script.js"],
    )

    def fetch(repo, path, branch):
        if path == "script.js":
            return "unsubscribe"
        return None

    monkeypatch.setattr(crawler, "_fetch_file", fetch)
    assert crawler._detect_dark_patterns("foo/bar", "main") == 0
    assert crawler._detect_bright_patterns("foo/bar", "main") == 1


def test_pattern_detection_case_insensitive_extensions(monkeypatch):
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(
        crawler,
        "_list_files",
        lambda repo, branch: ["INDEX.JS", "README.MD"],
    )

    def fetch(repo, path, branch):
        return "onbeforeunload" if path == "INDEX.JS" else "delete account"

    monkeypatch.setattr(crawler, "_fetch_file", fetch)
    assert crawler._detect_dark_patterns("foo/bar", "main") == 1
    assert crawler._detect_bright_patterns("foo/bar", "main") == 1


def test_list_files_errors(monkeypatch):
    crawler = rc.RepoCrawler([])

    class DummySession:
        def get(self, url, **kwargs):
            raise rc.requests.RequestException

    crawler.session = DummySession()
    assert crawler._list_files("foo/bar", "main") == []

    class Resp:
        status_code = 200

        @staticmethod
        def json():
            raise ValueError

    class BadSession:
        def get(self, url, **kwargs):
            return Resp()

    crawler.session = BadSession()
    assert crawler._list_files("foo/bar", "main") == []


def test_continue_on_empty(monkeypatch):
    crawler = rc.RepoCrawler([])
    monkeypatch.setattr(crawler, "_list_files", lambda r, b: ["script.js"])
    monkeypatch.setattr(crawler, "_fetch_file", lambda r, p, b: None)
    assert crawler._detect_dark_patterns("foo/bar", "main") == 0
    assert crawler._detect_bright_patterns("foo/bar", "main") == 0


def test_pattern_detection_reuses_file_list(monkeypatch):
    crawler = rc.RepoCrawler([])
    calls = {"count": 0}

    def list_files(repo, branch):
        calls["count"] += 1
        return ["index.js", "README.md"]

    monkeypatch.setattr(crawler, "_list_files", list_files)
    monkeypatch.setattr(crawler, "_fetch_file", lambda r, p, b: "unsubscribe")
    files = crawler._list_files("foo/bar", "main")
    crawler._detect_dark_patterns("foo/bar", "main", files)
    crawler._detect_bright_patterns("foo/bar", "main", files)
    assert calls["count"] == 1
