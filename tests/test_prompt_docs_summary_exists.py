from pathlib import Path

TITLE = "# Prompt Docs Summary"


def test_prompt_docs_summary_exists_and_titled():
    doc = Path("docs/prompt-docs-summary.md")
    assert doc.exists(), "docs/prompt-docs-summary.md missing"
    lines = doc.read_text().splitlines()
    assert lines[1].strip() == TITLE, "unexpected document title"
