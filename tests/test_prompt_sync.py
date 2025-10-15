from argparse import Namespace
from pathlib import Path

import pytest

# fmt: off
# isort: off
from flywheel import __main__ as flywheel_main
# isort: on
# fmt: on


def test_sync_prompt_docs_copies_missing_prompts(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    updated = flywheel_main.sync_prompt_docs(target)

    expected = [target / rel for rel in flywheel_main.PROMPT_DOCS]
    assert updated == expected
    for rel in flywheel_main.PROMPT_DOCS:
        src = flywheel_main.ROOT / rel
        dest = target / rel
        assert dest.read_text() == src.read_text()


def test_sync_prompt_docs_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    flywheel_main.sync_prompt_docs(target)
    second = flywheel_main.sync_prompt_docs(target)

    assert second == []


def test_sync_prompt_docs_missing_source(tmp_path: Path) -> None:
    target = tmp_path / "sugarkube"

    with pytest.raises(FileNotFoundError):
        flywheel_main.sync_prompt_docs(
            target,
            prompt_paths=[Path("docs/prompts/codex/missing.md")],
        )


def test_sync_prompts_cli_reports_updates(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    target = tmp_path / "axel"
    args = Namespace(target=str(target), files=None)
    flywheel_main.sync_prompts_cli(args)

    captured = capsys.readouterr().out.strip().splitlines()
    root_path = target.resolve()
    expected_paths = [root_path / rel for rel in flywheel_main.PROMPT_DOCS]
    expected_lines = [f"Updated {path}" for path in expected_paths]
    assert captured == expected_lines


def test_sync_prompts_cli_handles_files_arg(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    target = tmp_path / "sugarkube"
    path = Path("docs/prompts/codex/automation.md")

    args = Namespace(target=str(target), files=[path])
    flywheel_main.sync_prompts_cli(args)
    first_out = capsys.readouterr().out.strip()
    assert f"Updated {target.resolve() / path}" in first_out

    flywheel_main.sync_prompts_cli(args)
    second_out = capsys.readouterr().out.strip()
    assert second_out == "Prompt docs already up to date."
