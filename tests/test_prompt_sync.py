from pathlib import Path

import pytest

from flywheel.__main__ import PROMPT_DOCS, ROOT, sync_prompt_docs


def test_sync_prompt_docs_copies_missing_prompts(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    updated = sync_prompt_docs(target)

    expected = [target / rel for rel in PROMPT_DOCS]
    assert updated == expected
    for rel in PROMPT_DOCS:
        src = ROOT / rel
        dest = target / rel
        assert dest.read_text() == src.read_text()


def test_sync_prompt_docs_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    sync_prompt_docs(target)
    second = sync_prompt_docs(target)

    assert second == []


def test_sync_prompt_docs_missing_source(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    with pytest.raises(FileNotFoundError):
        sync_prompt_docs(
            target,
            prompt_paths=[Path("docs/prompts/codex/missing.md")],
        )
