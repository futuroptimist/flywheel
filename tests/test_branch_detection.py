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
