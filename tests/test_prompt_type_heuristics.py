"""Tests for prompt type inference heuristics."""

import sys
import types

tabulate_module = types.ModuleType("tabulate")
tabulate_module.tabulate = lambda *a, **kw: ""
sys.modules["tabulate"] = tabulate_module

from scripts.update_prompt_docs_summary import extract_prompts  # noqa: E402


def test_heading_type_inference():
    text = """## 1 - Fix issue
Details

## Codex Spellcheck Prompt
Content"""
    base_url = "https://example.com/doc.md"
    prompts = extract_prompts(text, base_url)
    assert prompts[0][1] == "one-off"
    assert prompts[1][1] == "evergreen"
