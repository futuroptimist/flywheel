from __future__ import annotations

import textwrap

import pytest

from flywheel.promptsync import compare_prompt_sets, format_prompt_sync_report


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
