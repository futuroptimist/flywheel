import subprocess
from pathlib import Path


def test_prompt_docs_summary_links_not_wrapped():
    text = Path("docs/prompt-docs-summary.md").read_text()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("|"):
            assert line.endswith("|"), f"Table row not terminated: {line}"
            cells = [c.strip() for c in line.split("|")[1:-1]]
            assert all(cells), f"Empty cell: {line}"
        if "](" in line:
            before, after = line.split("](", 1)
            link_text = before.split("[", 1)[-1]
            assert link_text.strip(), f"Empty link text: {line}"
            assert ")" in after, f"Link appears to be wrapped: {line}"
        if i < len(lines) - 1:
            nxt = lines[i + 1]
            if line and line[-1].isalpha() and nxt and nxt[0].islower():
                raise AssertionError(
                    f"Word broken across lines: '{line}' / '{nxt}'"  # noqa: E501
                )


def test_update_prompt_docs_summary_produces_unwrapped_links(tmp_path):
    repo_list = tmp_path / "repos.txt"
    repo_list.write_text("futuroptimist/flywheel\n")
    out = tmp_path / "summary.md"
    subprocess.run(
        [
            "python",
            "scripts/update_prompt_docs_summary.py",
            "--repos-from",
            str(repo_list),
            "--out",
            str(out),
        ],
        check=True,
    )
    text = out.read_text()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("|"):
            assert line.endswith(
                "|"
            ), f"Generated table row not terminated: {line}"  # noqa: E501
            cells = [c.strip() for c in line.split("|")[1:-1]]
            assert all(cells), f"Generated empty cell: {line}"
        if "](" in line:
            before, after = line.split("](", 1)
            link_text = before.split("[", 1)[-1]
            assert link_text.strip(), f"Generated empty link text: {line}"  # noqa: E501
            assert ")" in after, f"Generated link appears wrapped: {line}"  # noqa: E501
        if i < len(lines) - 1:
            nxt = lines[i + 1]
            if line and line[-1].isalpha() and nxt and nxt[0].islower():
                raise AssertionError(
                    f"Generated word broken across lines: '{line}' / '{nxt}'"
                )
