from flywheel.repocrawler import RepoCrawler


class Dummy404:
    def __init__(self):
        self.headers = {}

    def get(self, url, **kw):
        class Resp:
            status_code = 404
            text = ""

            def json(self):
                raise ValueError("no json")

        return Resp()


def test_default_branch_404():
    crawler = RepoCrawler([], session=Dummy404())
    assert crawler._default_branch("demo/repo") == "main"


class DummyBadJSON:
    def __init__(self):
        self.headers = {}

    def get(self, url, **kw):
        class Resp:
            status_code = 200
            text = "not json"

            def json(self):
                raise ValueError("bad")

        return Resp()


def test_default_branch_bad_json():
    crawler = RepoCrawler([], session=DummyBadJSON())
    assert crawler._default_branch("demo/repo") == "main"


class DummyTimeout:
    def __init__(self):
        self.headers = {}

    def get(self, url, **kw):
        assert "timeout" in kw

        class Resp:
            status_code = 200

            def json(self):
                return {"default_branch": "dev"}

        return Resp()


def test_default_branch_uses_timeout():
    crawler = RepoCrawler([], session=DummyTimeout())
    assert crawler._default_branch("demo/repo") == "dev"


class DummyMissingStatuses:
    def __init__(self):
        self.headers = {}

    def get(self, url, **kw):
        class Resp:
            def __init__(self, status_code: int, body: str):
                self.status_code = status_code
                self._body = body

            def json(self):
                import json

                if not self._body:
                    raise ValueError("no json")
                return json.loads(self._body)

        if "/actions/runs" in url:
            return Resp(200, '{"workflow_runs": []}')
        if "/commits/" in url and url.endswith("/status"):
            return Resp(404, "")
        return Resp(200, "{}")


def test_branch_green_missing_status_returns_none():
    crawler = RepoCrawler([], session=DummyMissingStatuses())
    assert crawler._branch_green("demo/repo", "main", "abcdef0") is None
