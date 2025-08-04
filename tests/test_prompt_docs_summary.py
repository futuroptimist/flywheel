import re
from pathlib import Path


def test_update_script_link_exists():
    doc = Path("docs/prompt-docs-summary.md")
    text = doc.read_text()
    pattern = r"\[scripts/update_prompt_docs_summary.py\]\((.+?)\)"
    match = re.search(pattern, text)
    assert match, "missing link to update_prompt_docs_summary.py"
    target = (doc.parent / match.group(1)).resolve()
    assert target.exists(), f"link target {target} does not exist"
