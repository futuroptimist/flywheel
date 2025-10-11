import argparse
import builtins
import shutil

import flywheel.__main__ as fm


def test_copy_file_skip(monkeypatch, tmp_path):
    src = tmp_path / "src.txt"
    dest = tmp_path / "dest.txt"
    src.write_text("data")
    dest.write_text("data")

    called = False

    def fake_copy(s, d):
        nonlocal called
        called = True

    monkeypatch.setattr(shutil, "copy2", fake_copy)
    fm.copy_file(src, dest)
    assert dest.read_text() == "data"
    assert not called


def test_prompt_bool(monkeypatch):
    inputs = iter(["", "n", "y"])

    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    # empty returns default
    assert fm.prompt_bool("Q", True) is True
    # explicit no
    assert fm.prompt_bool("Q", True) is False
    # explicit yes
    assert fm.prompt_bool("Q", False) is True


def test_init_repo_interactive(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    inputs = iter(["javascript", "y"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    args = argparse.Namespace(
        path=str(repo), language="python", save_dev=None, yes=False
    )
    fm.init_repo(args)

    assert (repo / "package.json").exists()
    assert (repo / "eslint.config.mjs").exists()
    assert (repo / ".github" / "workflows" / "01-lint-format.yml").exists()


def test_update_repo_interactive_accept(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    inputs = iter([""])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    args = argparse.Namespace(path=str(repo), save_dev=None, yes=False)
    fm.update_repo(args)

    wf = repo / ".github" / "workflows" / "01-lint-format.yml"
    eslint_config = repo / "eslint.config.mjs"
    assert wf.exists()
    assert eslint_config.exists()


def test_update_repo_interactive_decline(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    inputs = iter(["n"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    args = argparse.Namespace(path=str(repo), save_dev=None, yes=False)
    fm.update_repo(args)

    wf = repo / ".github" / "workflows" / "01-lint-format.yml"
    eslint_config = repo / "eslint.config.mjs"
    assert not wf.exists()
    assert not eslint_config.exists()


def test_update_repo_yes_flag(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()

    args = argparse.Namespace(path=str(repo), save_dev=None, yes=True)
    fm.update_repo(args)

    wf = repo / ".github" / "workflows" / "01-lint-format.yml"
    eslint_config = repo / "eslint.config.mjs"
    assert wf.exists()
    assert eslint_config.exists()
