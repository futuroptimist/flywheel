from argparse import Namespace
from pathlib import Path

import pytest

# fmt: off
# isort: off
import flywheel.__main__ as cli
# isort: on
# fmt: on


def test_sync_prompt_docs_copies_missing_prompts(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    updated = cli.sync_prompt_docs(target)

    expected = [target / rel for rel in cli.PROMPT_DOCS]
    assert updated == expected
    for rel in cli.PROMPT_DOCS:
        src = cli.ROOT / rel
        dest = target / rel
        assert dest.read_text() == src.read_text()


def test_sync_prompt_docs_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    cli.sync_prompt_docs(target)
    second = cli.sync_prompt_docs(target)

    assert second == []


def test_sync_prompt_docs_missing_source(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    with pytest.raises(FileNotFoundError):
        cli.sync_prompt_docs(
            target,
            prompt_paths=[Path("docs/prompts/codex/missing.md")],
        )


def test_sync_prompts_cli_reports_updates(tmp_path: Path) -> None:
    target = tmp_path / "axel"
    args = Namespace(target=str(target), files=None)
    cli.sync_prompts_cli(args)

    for rel in cli.PROMPT_DOCS:
        assert (target / rel).exists()


def test_sync_prompts_cli_handles_files_arg(tmp_path: Path) -> None:
    target = tmp_path / "axel"
    args = Namespace(
        target=str(target), files=[Path("docs/prompts/codex/automation.md")]
    )
    cli.sync_prompts_cli(args)
    cli.sync_prompts_cli(args)

    doc = target / "docs/prompts/codex/automation.md"
    assert doc.exists()
