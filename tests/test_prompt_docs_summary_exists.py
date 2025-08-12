from pathlib import Path


def test_prompt_docs_summary_exists_and_titled():
    doc = Path("docs/prompt-docs-summary.md")
    assert doc.exists(), "docs/prompt-docs-summary.md missing"
    first_line = doc.read_text().splitlines()[0].strip()
    assert first_line == "# Prompt Docs Summary", "unexpected document title"
