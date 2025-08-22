from pathlib import Path

DOC = Path("docs/prompt-docs-todos.md")


def test_prompt_docs_todos_has_table_header():
    lines = DOC.read_text().splitlines()
    assert lines, "docs/prompt-docs-todos.md should not be empty"
    assert any(
        line.startswith("| Repo |") for line in lines
    ), "missing table header"  # noqa: E501
