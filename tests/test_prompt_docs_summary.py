from pathlib import Path

SUMMARY_FILE = Path(__file__).parent.parent / "docs" / "prompt-docs-summary.md"


def test_prompt_docs_summary_has_spellcheck_disabled():
    first_line = SUMMARY_FILE.read_text().splitlines()[0].strip()
    assert first_line == "<!-- spellchecker: disable -->"
