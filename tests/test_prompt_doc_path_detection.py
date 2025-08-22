import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import SimpleNamespace

module_path = Path("scripts/update_prompt_docs_summary.py")

# Stub dependencies so the module can be imported without extras.
sys.modules.setdefault(
    "tabulate",
    SimpleNamespace(tabulate=lambda *args, **kwargs: ""),
)

module = SourceFileLoader("upd", str(module_path)).load_module()

is_prompt_doc_path = module.is_prompt_doc_path


def test_is_prompt_doc_path_case_insensitive():
    assert is_prompt_doc_path("Docs/Prompts/Foo.MD")
    assert is_prompt_doc_path("prompt/Bar.md")
    assert not is_prompt_doc_path("README.md")
    assert not is_prompt_doc_path("docs/prompt-docs-summary.md")
