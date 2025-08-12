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


def test_dspace_rows_present():
    doc = Path("docs/prompt-docs-summary.md").read_text()
    msg = "dspace prompt docs missing"
    assert doc.count("democratizedspace/dspace") >= 2, msg


def test_no_blank_cells():
    doc = Path("docs/prompt-docs-summary.md")
    for line in doc.read_text().splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            assert all(cells), f"blank cell in line: {line}"
