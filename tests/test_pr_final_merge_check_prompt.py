import re
from pathlib import Path

import pytest

PROMPT_FILE = (
    Path(__file__).parent.parent
    / "docs"
    / "prompts"
    / "llm"
    / "pr-final-merge-check.md"
)
LIST_LABEL = "Canonical allowed final response forms (exactly four):"
LIST_END = "End canonical allowed final response forms."
CONDITIONAL_SUCCESS = (
    "yes, it can be merged assuming the pending CI checks succeed"  # noqa: E501
)
UNCONDITIONAL_SUCCESS = "yes, it can be merged"


def prompt_sections(document: str) -> dict[str, str]:
    main_start = document.index("## Main Prompt")
    upgrade_start = document.index("## Upgrade Prompt")
    table_start = document.index("## Decision-table validation")
    return {
        "main": document[main_start:upgrade_start],
        "upgrade": document[upgrade_start:table_start],
    }


def canonical_forms(section: str) -> list[str]:
    assert section.count(LIST_LABEL) == 1
    assert section.count(LIST_END) == 1
    after_label = section.split(LIST_LABEL, 1)[1].split(LIST_END, 1)[0]
    entries: list[tuple[int, list[str]]] = []

    for line in after_label.splitlines()[1:]:
        match = re.match(r"^\s{0,2}(\d+)\.\s+(.*)$", line)
        if match:
            entries.append((int(match.group(1)), [match.group(2)]))
        elif entries and line.strip():
            entries[-1][1].append(line.strip())

    numbers = [number for number, _ in entries]
    assert numbers == [1, 2, 3, 4]
    return [" ".join(" ".join(lines).split()) for _, lines in entries]


def validate_contract(document: str) -> None:
    sections = prompt_sections(document)
    forms = {
        name: canonical_forms(section) for name, section in sections.items()
    }  # noqa: E501

    assert forms["main"] == forms["upgrade"]
    assert re.search(
        r"`text`.*complete generated `@codex` comment", forms["main"][0]
    )  # noqa: E501
    assert re.search(
        r"`markdown`.*complete replacement PR description", forms["main"][1]
    )
    assert (
        forms["main"][2] == f"Exactly `{CONDITIONAL_SUCCESS}`."
    ), "conditional success sentence changed"
    assert (
        forms["main"][3] == f"Exactly `{UNCONDITIONAL_SUCCESS}`."
    ), "unconditional success sentence changed"

    for section in sections.values():
        assert not re.search(
            r"\b(?:Category|category) 4\b", section
        ), "Category 4 routing found"
        assert re.search(
            r"no introductory (?:text|or concluding prose).*"
            r"(?:fenced deliverable|selected form)",
            section,
            re.DOTALL,
        )
        assert "new codex task, not a r/e/v/i/e/w task" in section
        assert re.search(
            r"(?:Do not include|contain no)[^\n]*`@codex`[^\n]*"
            r"(?:sentinel|new codex task)",
            section,
        )
        assert re.search(
            r"(?:title, body, or enough of the diff|title, body, or enough "
            r"of the diff is) unreadable.*access-limitation report.*"
            r"(?:(?:preserve|preserved|preserving|preservation) "
            r"(?:of )?the existing description|the existing description.*"
            r"(?:preserve|preserved|preserving|preservation)).*"
            r"(?:restore|restored) access.*rerun",
            section,
            re.DOTALL,
        ), "unreadable-content fallback changed"


def test_prompt_has_exactly_four_allowed_final_response_forms():
    validate_contract(PROMPT_FILE.read_text())


@pytest.mark.parametrize(
    ("mutation", "expected_message"),
    [
        (
            lambda text: text.replace(
                "4. Exactly `yes, it can be merged`.",
                "4. Exactly `yes, it can be merged`.\n"
                "5. A diagnostic paragraph.",  # noqa: E501
                1,
            ),
            "[1, 2, 3, 4]",
        ),
        (
            lambda text: text.replace(
                "4. Exactly `yes, it can be merged`.",
                "4. Exactly `yes, it can be merged`.\n\n"
                "5. A separated diagnostic paragraph.",
                1,
            ),
            "[1, 2, 3, 4]",
        ),
        (
            lambda text: text.replace(
                "3. Exactly `yes, it can be merged assuming the pending "
                "CI checks succeed`.",
                "2. Exactly `yes, it can be merged assuming the pending "
                "CI checks succeed`.",
                1,
            ),
            "[1, 2, 3, 4]",
        ),
        (
            lambda text: text.replace(
                CONDITIONAL_SUCCESS, "yes, merge after CI"
            ),  # noqa: E501
            "conditional",
        ),
        (
            lambda text: text.replace(
                "Use three decision categories",
                "Route Category 4 before three categories",
                1,
            ),
            "Category 4",
        ),
    ],
    ids=[
        "fifth-form",
        "separated-fifth-form",
        "missing-duplicate",
        "altered-success",
        "category-4",
    ],
)
def test_contract_validator_rejects_regressions(mutation, expected_message):
    mutated = mutation(PROMPT_FILE.read_text())

    with pytest.raises(AssertionError) as error:
        validate_contract(mutated)

    assert expected_message.lower() in str(error.value).lower()
