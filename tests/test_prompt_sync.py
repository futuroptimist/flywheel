from argparse import Namespace
from pathlib import Path

import pytest

from flywheel.__main__ import (
    PROMPT_DOCS,
    ROOT,
    sync_prompt_docs,
    sync_prompts_cli,
)


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


def test_sync_prompts_cli_reports_updates(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    target = tmp_path / "sugarkube"

    args = Namespace(target=str(target), files=None)
    sync_prompts_cli(args)

    captured = capsys.readouterr().out.strip().splitlines()
    expected_paths = [target.resolve() / rel for rel in PROMPT_DOCS]
    expected_lines = [f"Updated {path}" for path in expected_paths]
    assert captured == expected_lines


def test_sync_prompts_cli_handles_files_arg(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    target = tmp_path / "sugarkube"
    path = Path("docs/prompts/codex/automation.md")

    args = Namespace(target=str(target), files=[path])
    sync_prompts_cli(args)
    first_out = capsys.readouterr().out.strip()
    assert f"Updated {target.resolve() / path}" in first_out

    sync_prompts_cli(args)
    second_out = capsys.readouterr().out.strip()
    assert second_out == "Prompt docs already up to date."
