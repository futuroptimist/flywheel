import re
from pathlib import Path

SUMMARY_FILE = Path(__file__).parent.parent / "docs" / "prompt-docs-summary.md"


def test_prompt_docs_summary_has_spellcheck_disabled():
    first_line = SUMMARY_FILE.read_text().splitlines()[0].strip()
    assert first_line == "<!-- spellchecker: disable -->"


def test_prompt_docs_summary_has_no_whitespace_broken_links():
    text = SUMMARY_FILE.read_text()
    broken_link_match = re.search(
        r"(?<!!)\[[^\]]+\]\s+\(",
        text,
    )
    error_message = (
        "prompt-docs-summary.md contains links with whitespace "
        "between [] and ()"
    )
    assert broken_link_match is None, error_message
