import importlib.util
import sys
import textwrap
import types
from pathlib import Path


def load_module():
    dummy = types.ModuleType("tabulate")
    dummy.tabulate = lambda *a, **k: ""
    sys.modules.setdefault("tabulate", dummy)
    spec = importlib.util.spec_from_file_location(
        "update_prompt_docs_summary",
        Path("scripts/update_prompt_docs_summary.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extract_prompts_skips_meta_sections():
    uds = load_module()
    text = textwrap.dedent(
        """
        ## Implementation prompts

        ### How to choose a prompt

        Some instructions.

        ### Notes for human contributors

        More text.

        ## Upgrade Prompt
        Type: evergreen
        Real prompt content.
        """
    )
    prompts = uds.extract_prompts(text, "https://example.com")
    assert len(prompts) == 1
    assert prompts[0][1] == "evergreen"
