import importlib
import sys


def test_iter_local_prompt_docs_includes_top_level(tmp_path):
    from scripts.update_prompt_docs_summary import iter_local_prompt_docs

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
