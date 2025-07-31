from __future__ import annotations

from .ci_status import ci_state


def trunk_cell(owner: str, repo: str, sha: str) -> str:
    """Return emoji for Trunk column."""
    if not sha:
        return "n/a"
    state = ci_state(owner, repo, sha)
    return "✅" if state == "green" else "❌"
