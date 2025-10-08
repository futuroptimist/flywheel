from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from flywheel.promptsync import (
    compare_prompt_sets,
    format_prompt_sync_report,
    main,
    parse_prompt_summary,
)


@pytest.fixture()
def sample_summary() -> str:
    return (
        textwrap.dedent(
            """
        ## **futuroptimist/flywheel**

        | Path | Prompt | Type | One-click? |
        | ---- | ------ | ---- | ---------- |
        | [docs/prompts/codex/automation.md](https://a/auto) |
        | [docs/prompts/codex/cleanup.md](https://a/cleanup) |

        ## futuroptimist/sugarkube

        | Path | Prompt | Type | One-click? |
        | ---- | ------ | ---- | ---------- |
        | [docs/prompts/codex/automation.md](https://b/auto) |
        | [docs/prompts/codex/docs.md](https://b/docs) |
        """
        ).strip()
        + "\n"
    )


def test_compare_prompt_sets_reports_missing_and_extra(
    sample_summary: str,
) -> None:
    missing, extra = compare_prompt_sets(
        sample_summary,
        source_repo="futuroptimist/flywheel",
        target_repo="futuroptimist/sugarkube",
    )

    assert missing == {"docs/prompts/codex/cleanup.md"}
    assert extra == {"docs/prompts/codex/docs.md"}


def test_format_prompt_sync_report_lists_paths(
    sample_summary: str,
) -> None:
    missing, extra = compare_prompt_sets(
        sample_summary,
        source_repo="futuroptimist/flywheel",
        target_repo="futuroptimist/sugarkube",
    )

    report = format_prompt_sync_report(
        missing,
        extra,
        source_repo="futuroptimist/flywheel",
        target_repo="futuroptimist/sugarkube",
    )

    assert "docs/prompts/codex/cleanup.md" in report
    assert "docs/prompts/codex/docs.md" in report
    assert "No prompt differences" not in report


def test_parse_prompt_summary_extracts_rows(sample_summary: str) -> None:
    summary = parse_prompt_summary(sample_summary)

    assert summary["futuroptimist/flywheel"] == {
        "docs/prompts/codex/automation.md",
        "docs/prompts/codex/cleanup.md",
    }
    assert summary["futuroptimist/sugarkube"] == {
        "docs/prompts/codex/automation.md",
        "docs/prompts/codex/docs.md",
    }


def test_format_prompt_sync_report_when_no_differences() -> None:
    report = format_prompt_sync_report(
        set(),
        set(),
        source_repo="source/repo",
        target_repo="target/repo",
    )

    assert report == "No prompt differences between source/repo and target/repo."


def test_main_returns_zero_when_no_differences(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    summary = tmp_path / "summary.md"
    summary.write_text(
        textwrap.dedent(
            """
        ## repo-a

        | Path | Prompt |
        | ---- | ------ |
        | [alpha](https://example.com/a) |

        ## repo-b

        | Path | Prompt |
        | ---- | ------ |
        | [alpha](https://example.com/a) |
        """
        ).strip()
        + "\n"
    )

    exit_code = main(
        [
            "--summary",
            str(summary),
            "--source-repo",
            "repo-a",
            "--target-repo",
            "repo-b",
            "--fail-on-diff",
        ]
    )

    captured = capsys.readouterr()
    assert "No prompt differences" in captured.out
    assert exit_code == 0


def test_main_returns_one_when_differences_detected(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    summary = tmp_path / "summary.md"
    summary.write_text(
        textwrap.dedent(
            """
        ## repo-a

        | Path | Prompt |
        | ---- | ------ |
        | [alpha](https://example.com/a) |

        ## repo-b

        | Path | Prompt |
        | ---- | ------ |
        | [beta](https://example.com/b) |
        """
        ).strip()
        + "\n"
    )

    exit_code = main(
        [
            "--summary",
            str(summary),
            "--source-repo",
            "repo-a",
            "--target-repo",
            "repo-b",
            "--fail-on-diff",
        ]
    )

    captured = capsys.readouterr()
    assert "Prompts present in repo-a but missing from repo-b" in captured.out
    assert exit_code == 1
