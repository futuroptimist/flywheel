import argparse
import builtins
from pathlib import Path

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


def test_summarize_repo_root_missing_dir(tmp_path):
    missing = tmp_path / "missing"
    assert fm.summarize_repo_root(missing) == "(directory not found)"


def test_summarize_repo_root_not_directory(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("data")
    assert fm.summarize_repo_root(file_path) == "(path is not a directory)"


def test_summarize_repo_root_iter_error(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()

    def boom(_: Path):
        raise OSError("cannot list")

    monkeypatch.setattr(Path, "iterdir", boom)
    assert fm.summarize_repo_root(repo) == "(unable to list repository contents)"


def test_summarize_repo_root_formats_entries(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".hidden").mkdir()
    (repo / "docs").mkdir()
    (repo / "README.md").write_text("hi")
    target = repo / "mystery"
    target.write_text("data")
    file_target = repo / "notes.txt"
    file_target.write_text("info")
    (repo / "notes-link").symlink_to(file_target)

    original_is_dir = Path.is_dir

    def flaky_is_dir(self: Path) -> bool:
        if self == target:
            raise OSError("stat failure")
        return original_is_dir(self)

    monkeypatch.setattr(Path, "is_dir", flaky_is_dir)

    snapshot = fm.summarize_repo_root(repo)
    assert "docs/" in snapshot
    assert "README.md" in snapshot
    assert "notes-link@" in snapshot
    assert "mystery" in snapshot
    assert ".hidden" not in snapshot


def test_summarize_repo_root_limits_entries(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    for idx in range(12):
        (repo / f"item{idx}").write_text("data")

    snapshot = fm.summarize_repo_root(repo, limit=5)
    assert snapshot.count(",") == 5  # five commas == six entries listed
    assert snapshot.endswith("… (+7 more)")


def test_summarize_repo_root_empty_dir(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    assert fm.summarize_repo_root(repo) == "(no non-hidden files found)"


def test_summarize_repo_root_unknown_type(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    special = repo / "mystery"
    special.write_text("data")

    original_is_dir = Path.is_dir
    original_is_symlink = Path.is_symlink
    original_is_file = Path.is_file

    def always_false(self: Path) -> bool:
        if self == special:
            return False
        return original_is_dir(self)

    def always_false_symlink(self: Path) -> bool:
        if self == special:
            return False
        return original_is_symlink(self)

    def always_false_file(self: Path) -> bool:
        if self == special:
            return False
        return original_is_file(self)

    monkeypatch.setattr(Path, "is_dir", always_false)
    monkeypatch.setattr(Path, "is_symlink", always_false_symlink)
    monkeypatch.setattr(Path, "is_file", always_false_file)

    snapshot = fm.summarize_repo_root(repo)
    assert snapshot == "mystery"
