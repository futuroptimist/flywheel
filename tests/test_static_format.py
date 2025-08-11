from pathlib import Path

import pytest

FILES = [
    Path("docs/prompt-docs-todos.md"),
    Path("webapp/static/models/examples/spool_core_sleeve_example.obj"),
]


@pytest.mark.parametrize("path", FILES)
def test_no_trailing_whitespace_and_eof(path: Path) -> None:
    data = path.read_text()
    # ensure no line has trailing whitespace
    for i, line in enumerate(data.splitlines()):
        assert line == line.rstrip(), f"{path}:{i+1} has trailing whitespace"
    # ensure file ends with a newline
    assert data.endswith("\n"), f"{path} missing trailing newline"
