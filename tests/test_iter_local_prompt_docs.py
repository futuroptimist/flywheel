import importlib
import sys

from scripts.update_prompt_docs_summary import (
    is_canonical_prompt_path,
    iter_local_prompt_docs,
)


def test_iter_local_prompt_docs_includes_top_level(tmp_path):

    docs_root = tmp_path / "docs"
    codex_dir = docs_root / "prompts" / "codex"
    codex_dir.mkdir(parents=True)
    (codex_dir / "a.md").write_text("# A\n")
    (docs_root / "prompts-extra.md").write_text("# Extra\n")

    files = list(iter_local_prompt_docs(docs_root))
    names = sorted(p.name for p in files)
    assert names == ["a.md", "prompts-extra.md"]


def test_import_without_tabulate(monkeypatch, tmp_path):
    monkeypatch.delitem(sys.modules, "tabulate", raising=False)
    module = importlib.reload(
        importlib.import_module("scripts.update_prompt_docs_summary")
    )

    docs_root = tmp_path / "docs"
    codex_dir = docs_root / "prompts" / "codex"
    codex_dir.mkdir(parents=True)
    (codex_dir / "a.md").write_text("# A\n")

    files = list(module.iter_local_prompt_docs(docs_root))
    names = sorted(p.name for p in files)
    assert names == ["a.md"]


def test_is_canonical_prompt_path_accepts_docs_prompts_root():
    assert is_canonical_prompt_path("docs/prompts/automation.md")


def test_is_canonical_prompt_path_rejects_external_locations():
    assert not is_canonical_prompt_path("frontend/docs/prompts/automation.md")
