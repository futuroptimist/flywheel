from __future__ import annotations

import os


def get_github_token() -> str:
    """Return GITHUB_TOKEN or raise RuntimeError if unset."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable not set")
    return token
