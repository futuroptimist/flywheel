from pathlib import Path


def _read_repo_list(path: str) -> list[str]:
    """Return non-empty, stripped entries from ``path``."""

    lines = Path(path).read_text().splitlines()
    return [line.strip() for line in lines if line.strip()]


def test_prompt_repo_lists_match():
    """Ensure prompt-doc and crawl repo manifests stay in sync."""

    repo_list = _read_repo_list("docs/repo_list.txt")
    prompt_repo_list = _read_repo_list("dict/prompt-doc-repos.txt")
    assert (
        repo_list == prompt_repo_list
    ), "prompt repo manifest must match docs/repo_list.txt"
