import builtins

from flywheel.__main__ import inject_dev, prompt_bool


def test_prompt_bool_default_true(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "")
    assert prompt_bool("continue?", True) is True


def test_prompt_bool_default_false(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "")
    assert prompt_bool("continue?", False) is False


def test_prompt_bool_yes(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "y")
    assert prompt_bool("continue?", False) is True


def test_prompt_bool_no(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    assert prompt_bool("continue?", True) is False


def test_inject_dev(tmp_path):
    target = tmp_path / "repo"
    inject_dev(target)
    assert (target / ".github" / "workflows" / "01-lint-format.yml").exists()
