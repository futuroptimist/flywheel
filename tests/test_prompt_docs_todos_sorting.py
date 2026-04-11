from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from scripts.update_prompt_docs_summary import normalize_prompt_todo_table


@pytest.mark.parametrize(
    "rows",
    [
        [
            ("zeta/repo", "[zeta](https://example.com/zeta)", "unknown"),
            ("alpha/repo", "[alpha](https://example.com/alpha)", "evergreen"),
            ("beta/repo", "[beta](https://example.com/beta)", "one-off"),
        ],
        [
            ("beta/repo", "[beta](https://example.com/beta)", "one-off"),
            ("alpha/repo", "[alpha](https://example.com/alpha)", "evergreen"),
        ],
    ],
)
def test_todos_sorted_by_type_and_repo(tmp_path: Path, rows):
    todo = tmp_path / "prompt-docs-todos.md"
    body = "\n".join(
        f"| {repo} | {prompt} | {ptype} | |" for repo, prompt, ptype in rows
    )
    todo.write_text(
        textwrap.dedent(
            f"""\
            # Prompt Docs TODOs

            | Repo | Suggested Prompt | Type | Notes |
            |------|-----------------|------|-------|
            {body}
            """
        ).strip()
        + "\n"
    )

    normalized = normalize_prompt_todo_table(todo)
    assert normalized.endswith("\n")
    persisted = todo.read_text()
    assert persisted == normalized

    lines = [line for line in normalized.splitlines() if line.startswith("|")]
    data_rows = lines[2:]
    parsed = [
        (
            parts[1].strip(),
            parts[2].strip(),
            parts[3].strip(),
        )
        for parts in (row.split("|") for row in data_rows)
    ]
    assert (
        parsed
        == [
            (
                "alpha/repo",
                "[alpha](https://example.com/alpha)",
                "evergreen",
            ),
            (
                "beta/repo",
                "[beta](https://example.com/beta)",
                "one-off",
            ),
            (
                "zeta/repo",
                "[zeta](https://example.com/zeta)",
                "unknown",
            ),
        ][: len(data_rows)]
    )
