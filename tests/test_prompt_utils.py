import argparse
import builtins

import flywheel.__main__ as fm
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


def test_prompt_truncates_long_readme(tmp_path, capsys):
    readme = tmp_path / "README.md"
    readme.write_text("\n".join(f"line{i}" for i in range(30)))
    args = argparse.Namespace(path=str(tmp_path))
    fm.prompt(args)
    out = capsys.readouterr().out
    assert "line19" in out
    assert "line20" not in out
