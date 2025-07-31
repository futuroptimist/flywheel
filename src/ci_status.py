from __future__ import annotations

import requests

from .github_auth import get_github_token

_ACCEPTABLE_REST_CONCLUSIONS = {
    "success",
    "neutral",
    "skipped",
    "completed",  # legacy status API
}


def _query_graphql(owner: str, repo: str, sha: str) -> str | None:
    """Return GraphQL `statusCheckRollup.state` or None on error."""
    token = get_github_token()
    qry = """
    query($o:String!,$r:String!,$s:String!) {
      repository(owner:$o, name:$r) {
        object(oid:$s) {
          ... on Commit { statusCheckRollup { state } }
        }
      }
    }"""
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": qry, "variables": {"o": owner, "r": repo, "s": sha}},
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    if resp.ok:
        rollup = (
            resp.json()
            .get("data", {})
            .get("repository", {})
            .get("object", {})
            .get("statusCheckRollup")
        )
        return None if rollup is None else rollup["state"]
    return None


def _query_rest(owner: str, repo: str, sha: str) -> str | None:
    """Return best-effort status via the Checks REST API."""
    token = get_github_token()
    base = "https://api.github.com/repos/"
    url = f"{base}{owner}/{repo}/commits/{sha}/check-runs"
    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    if not r.ok:
        return None
    runs = r.json().get("check_runs", [])
    if not runs:  # no CI
        return "NO_CI"
    for run in runs:
        concl = (run.get("conclusion") or "").lower()
        if concl not in _ACCEPTABLE_REST_CONCLUSIONS:
            return "FAILURE"
    return "SUCCESS"


def ci_state(owner: str, repo: str, sha: str) -> str:
    """
    Return 'green' or 'red' for the dashboard.
    Logic order:
      1. GraphQL rollup
      2. REST checks fall-back
    """
    state = _query_graphql(owner, repo, sha)
    if state is None:
        state = _query_rest(owner, repo, sha)

    if state in ("SUCCESS", "PENDING", "NO_CI"):
        return "green"
    return "red"
