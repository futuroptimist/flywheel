from __future__ import annotations

from pathlib import Path

import pytest

ALLOWLIST_PATH = Path(__file__).resolve().parent.parent / "dict" / "allow.txt"


@pytest.fixture(scope="module")
def allowlist_words() -> set[str]:
    contents = ALLOWLIST_PATH.read_text().splitlines()
    return {line.strip() for line in contents if line.strip()}


@pytest.mark.parametrize(
    "word",
    [
        "AST",
        "DevOps",
        "Embeddings",
        "FIXME",
        "Mitigations",
        "Observability",
        "Orchestrator",
        "Semver",
        "TypeScript",
        "UX",
        "WIP",
        "APIs",
        "SaaS",
        "anonymization",
        "anonymized",
        "assimp",
        "backoff",
        "backports",
        "danielsmith",
        "dedupe",
        "deduping",
        "diffPreview",
        "entrypoint",
        "embeddings",
        "integrations",
        "monorepo",
        "oversized",
        "pgvector",
        "pluggable",
        "quickstart",
        "revalidate",
        "repo's",
        "ripgrep",
        "rollout",
        "runnable",
        "sugarkube's",
        "summarization",
        "untrusted",
        "floorplan",
        "hud",
        "webapp",
        "Workstream",
        "Workstreams",
    ],
)
def test_spellcheck_allowlist_contains_required_vocabulary(
    word: str, allowlist_words: set[str]
) -> None:
    assert word in allowlist_words
