"""Utilities to crawl GitHub repositories for flywheel features."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional
from urllib.parse import urlparse

import requests
from requests import RequestException

try:  # pragma: no cover - optional dependency
    import requests_cache
except Exception:  # pragma: no cover - fallback when cache not installed
    requests_cache = None

PATCH_THRESHOLD = 90.0
BADGE_PATCH = "https://img.shields.io/codecov/patch/github/{repo}/{branch}.svg"
BADGE_TOTAL = "https://codecov.io/gh/{repo}/branch/{branch}/graph/badge.svg"


@dataclass
class RepoInfo:
    name: str
    branch: str
    coverage: Optional[str]
    patch_percent: Optional[float]
    uses_codecov: bool
    has_license: bool
    has_ci: bool
    has_agents: bool
    has_coc: bool
    has_contributing: bool
    has_precommit: bool
    installer: str
    latest_commit: Optional[str]
    workflow_count: int
    trunk_green: Optional[bool]
    commit_date: Optional[str] = None
    dark_pattern_count: int = 0
    bright_pattern_count: int = 0


class RepoCrawler:
    """Check remote GitHub repos for standard flywheel features."""

    # Filenames whose presence in `.github/workflows/` signals that the repo
    # runs some form of continuous integration. This keeps the heuristic broad
    # so repos with custom workflow names still count.
    CI_KEYWORDS = ("ci", "test", "lint", "build", "docs", "qa")

    _UV = re.compile(r"setup-uv|uv venv", re.I)
    _PIP = re.compile(r"pip install", re.I)
    _POETRY = re.compile(r"poetry\s+install", re.I)
    DARK_PATTERNS = [
        re.compile(r"onbeforeunload", re.I),
        re.compile(r"navigator\.clipboard\.writeText", re.I),
        re.compile(r"auto\s*play", re.I),
        re.compile(r"confirmshame", re.I),
    ]
    BRIGHT_PATTERNS = [
        re.compile(r"delete\s+account", re.I),
        re.compile(r"unsubscribe", re.I),
        re.compile(r"opt[-_ ]?out", re.I),
        re.compile(r"privacy", re.I),
        re.compile(r"no[-_ ]?tracking", re.I),
    ]

    DOCKER_FILES = (
        "Dockerfile",
        "Dockerfile.dev",
        "Dockerfile.prod",
        "docker/Dockerfile",
        "frontend/Dockerfile",
    )

    def _list_files(self, repo: str, branch: str) -> list[str]:
        base = "https://api.github.com/repos/"
        url = f"{base}{repo}/git/trees/{branch}?recursive=1"
        try:
            resp = self.session.get(
                url,
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
        except RequestException:
            return []
        if resp.status_code == 200:
            try:
                data = resp.json()
                return [
                    item.get("path", "")
                    for item in data.get("tree", [])
                    if item.get("type") == "blob"
                ]
            except Exception:
                return []
        return []

    def _detect_dark_patterns(self, repo: str, branch: str) -> int:
        count = 0
        files = self._list_files(repo, branch)[:50]
        for path in files:
            if not path.endswith(
                (
                    ".js",
                    ".ts",
                    ".tsx",
                    ".py",
                    ".html",
                    ".md",
                    ".json",
                )
            ):
                continue
            text = self._fetch_file(repo, path, branch)
            if not text:
                continue
            for pat in self.DARK_PATTERNS:
                if pat.search(text):
                    count += 1
                    break
        return count

    def _detect_bright_patterns(self, repo: str, branch: str) -> int:
        count = 0
        files = self._list_files(repo, branch)[:50]
        for path in files:
            if not path.endswith(
                (
                    ".js",
                    ".ts",
                    ".tsx",
                    ".py",
                    ".html",
                    ".md",
                    ".json",
                )
            ):
                continue
            text = self._fetch_file(repo, path, branch)
            if not text:
                continue
            for pat in self.BRIGHT_PATTERNS:
                if pat.search(text):
                    count += 1
                    break
        return count

    def _badge_patch_percent(self, repo: str, branch: str) -> Optional[float]:
        """Return patch coverage parsed from the public badge."""
        url = BADGE_PATCH.format(repo=repo, branch=branch)
        try:
            resp = self.session.get(url, timeout=10)
        except RequestException:
            return None
        if resp.status_code == 200:
            m = re.search(r">(\d{1,3})%<", resp.text)
            if m:
                return float(m.group(1))
        return None

    def _badge_total_percent(self, repo: str, branch: str) -> Optional[str]:
        """Return total coverage parsed from the public badge."""
        url = BADGE_TOTAL.format(repo=repo, branch=branch)
        try:
            resp = self.session.get(url, timeout=10)
        except RequestException:
            return None
        if resp.status_code == 200:
            m = re.search(r">(\d{1,3})%<", resp.text)
            if m:
                return f"{m.group(1)}%"
        return None

    def __init__(
        self,
        repos: Iterable[str],
        session: Optional[requests.Session] = None,
        token: Optional[str] = None,
    ) -> None:
        """Initialize with an optional list of ``owner/name@branch`` specs."""

        self.repos: list[str] = []
        self._branch_overrides: dict[str, str] = {}
        for r in repos:
            if "@" in r:
                name, branch = r.split("@", 1)
                self.repos.append(name)
                self._branch_overrides[name] = branch
            else:
                self.repos.append(r)
        if session is not None:
            self.session = session
        elif requests_cache:
            cache_dir = Path(".cache")
            cache_dir.mkdir(exist_ok=True)
            self.session = requests_cache.CachedSession(
                cache_dir / "github-cache"
            )  # noqa: E501
        else:  # pragma: no cover - requests_cache not installed
            self.session = requests.Session()
        tok = token or os.environ.get("GITHUB_TOKEN")
        if tok:
            self.session.headers.update({"Authorization": f"Bearer {tok}"})

    def _fetch_file(
        self,
        repo: str,
        path: str,
        branch: Optional[str],
    ) -> Optional[str]:
        branches = [b for b in (branch, "main", "master") if b]
        for br in branches:
            url = f"https://raw.githubusercontent.com/{repo}/{br}/{path}"
            try:
                resp = self.session.get(url, timeout=10)
            except RequestException:
                continue
            if resp.status_code == 200:
                return resp.text
        return None

    def _default_branch(self, repo: str) -> str:
        url = f"https://api.github.com/repos/{repo}"
        try:
            resp = self.session.get(
                url,
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
        except RequestException:
            return "main"
        if resp.status_code == 200:
            try:
                return resp.json().get("default_branch", "main")
            except Exception:
                return "main"
        return "main"

    def _latest_commit(
        self, repo: str, branch: str
    ) -> tuple[Optional[str], Optional[str]]:
        owner, name = repo.split("/", 1)
        url = (
            "https://api.github.com/repos/"
            f"{owner}/{name}/commits?per_page=1&sha={branch}"
        )
        try:
            resp = self.session.get(
                url,
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and data:
                    sha = data[0].get("sha", "")
                    date_str = (
                        data[0].get("commit", {}).get("author", {}).get("date")
                    )  # noqa: E501
                    if date_str:
                        try:
                            dt = datetime.fromisoformat(
                                date_str.replace("Z", "+00:00")
                            )  # noqa: E501
                            date = dt.date().isoformat()
                        except Exception:  # pragma: no cover - parsing errors
                            date = None
                    else:
                        date = None  # pragma: no cover - missing date
                    return sha[:7] if sha else None, date
        except RequestException:
            return None, None
        except Exception:  # pragma: no cover - unexpected JSON
            return None, None
        return None, None

    PASS_CONCLUSIONS = {"success", "neutral", "skipped", "no_status"}

    def _branch_green(
        self,
        repo: str,
        branch: str,
        sha: str,
    ) -> Optional[bool]:
        """Return True when the HEAD of ``branch`` is considered passing."""

        if not sha:
            return None

        owner, name = repo.split("/", 1)
        base = "https://api.github.com/repos"

        # First check workflow runs for the specific commit
        runs_url = (
            f"{base}/{owner}/{name}/actions/runs"
            f"?branch={branch}&status=completed&per_page=20"
        )
        try:
            resp = self.session.get(
                runs_url,
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
        except RequestException:
            resp = None

        if resp and resp.status_code == 200:
            try:
                runs = resp.json().get("workflow_runs", [])
            except Exception:
                runs = []
            for run in runs:
                if run.get("head_sha", "").startswith(sha):
                    conclusion = run.get("conclusion")
                    if conclusion:
                        return conclusion in self.PASS_CONCLUSIONS
                    break

        # Fallback to the combined commit status API
        url = f"{base}/{owner}/{name}/commits/{sha}/status"
        try:
            resp = self.session.get(
                url,
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
        except RequestException:
            return None

        # ----- New, more robust evaluation ---------------------------------
        if resp.status_code != 200:
            return None

        try:
            body = resp.json()
        except Exception:
            return None

        # 1. Fast-path: combined status already success
        if body.get("state") == "success":
            return True

        statuses = body.get("statuses", [])

        _COVERAGE_CONTEXTS = {"codecov/patch", "codecov/project"}

        hard_failure = False
        has_success = False
        for st in statuses:
            ctx = st.get("context", "")
            state = st.get("state")
            if ctx in _COVERAGE_CONTEXTS:
                continue
            if state == "success":
                has_success = True
            elif state in {"failure", "error"}:
                hard_failure = True

        if hard_failure:
            return False
        if has_success:
            return True

        # 2. Fallback to the Checks API (used by GitHub Actions)
        checks_url = (
            "https://api.github.com/repos/" f"{repo}/commits/{sha}/check-runs"
        )  # noqa: E501
        try:
            r = self.session.get(
                checks_url,
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
            if r.status_code == 200:
                runs = r.json().get("check_runs", [])
                if runs:
                    conclusions = {run.get("conclusion") for run in runs}
                    if conclusions <= {"success", "neutral", "skipped"}:
                        return True
                    if {"failure", "cancelled", "timed_out"} & conclusions:
                        return False
        except RequestException:  # pragma: no cover - network error handling
            pass

        # 3. Last resort: no CI contexts present → treat as green
        return True

    def _recent_commits(
        self,
        repo: str,
        branch: str,
        count: int = 2,
    ) -> list[str]:
        """Return the most recent commit SHAs for the branch."""
        url = (
            "https://api.github.com/repos/"
            f"{repo}/commits?per_page={count}&sha={branch}"
        )
        try:
            resp = self.session.get(
                url,
                headers={"Accept": "application/vnd.github+json"},
            )
        except RequestException:
            return []
        if resp.status_code == 200:
            try:
                return [c["sha"] for c in resp.json()][:count]
            except Exception:
                return []
        return []

    def _has_file(self, repo: str, path: str, branch: str) -> bool:
        return self._fetch_file(repo, path, branch) is not None

    def _list_workflows(self, repo: str, branch: str) -> set[str]:
        """Return workflow filenames under `.github/workflows` for the repo."""
        url = (
            "https://api.github.com/repos/"
            f"{repo}/contents/.github/workflows?ref={branch}"
        )
        try:
            resp = self.session.get(
                url,
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
        except RequestException:
            return set()
        if resp.status_code == 200:
            try:
                return {
                    item.get("name", "")
                    for item in resp.json()
                    if item.get("name", "").endswith((".yml", ".yaml"))
                }
            except Exception:
                return set()
        return set()

    def _has_ci(self, workflow_files: set[str]) -> bool:
        """Return True if workflow names suggest continuous integration."""
        for name in workflow_files:
            lower = name.lower()
            if any(key in lower for key in self.CI_KEYWORDS):
                return True
        return False

    def _detect_installer(self, text: str) -> str:
        """Return installer hint based on workflow snippets."""
        if self._UV.search(text):
            return "uv"
        if self._PIP.search(text):
            return "pip"
        if self._POETRY.search(text):
            return "poetry"
        return "partial"

    # ------------------------ Coverage helpers ------------------------ #
    def _project_coverage_from_codecov(
        self,
        repo: str,
        branch: str,
    ) -> Optional[str]:
        """Retrieve project coverage percentage via Codecov API."""
        owner, name = repo.split("/", 1)
        url = f"https://codecov.io/api/gh/{owner}/{name}"
        try:
            resp = self.session.get(url, timeout=10)
        except RequestException:
            resp = None
        if resp and resp.status_code == 200:
            try:
                body = resp.json()
                cov = body.get("commit", {}).get("totals", {}).get("coverage")
                if cov is not None:
                    return f"{cov}%"
            except Exception:
                pass
        # Fallback to parsing the public badge if the API fails
        try:
            return self._badge_total_percent(repo, branch)
        except Exception:
            return None

    def _patch_coverage_from_codecov(
        self,
        repo: str,
        branch: str,
    ) -> Optional[float]:
        """Retrieve patch coverage percentage via Codecov REST API."""
        owner, name = repo.split("/", 1)
        headers = {}
        token = os.environ.get("CODECOV_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            resp = self.session.get(
                f"https://codecov.io/api/gh/{owner}/{name}",
                headers=headers,
                timeout=10,
            )
        except RequestException:
            resp = None
        if resp and resp.status_code == 200:
            try:
                body = resp.json()
                diff = (
                    body.get("commit", {})
                    .get("totals", {})
                    .get("coverage_diff")  # noqa: E501
                )
                if diff is not None and diff >= 90:
                    return float(diff)
            except Exception:
                pass
        # Fallback to parsing the badge
        try:
            return self._badge_patch_percent(repo, branch)
        except Exception:
            return None

    def _parse_coverage(
        self, readme: Optional[str], repo: str, branch: str
    ) -> Optional[str]:
        if not readme:
            return None

        if not re.search(r"codecov.io/.+?/badge.svg", readme):
            return None

        pct = self._project_coverage_from_codecov(repo, branch)
        if pct:
            return pct
        return None

    def _uses_codecov(
        self,
        repo: str,
        branch: str,
        readme: Optional[str],
    ) -> bool:
        """Return True if Codecov appears to be configured."""
        if readme:
            # Find URLs in the README and examine their hostnames for Codecov
            urls = re.findall(r"https?://[^\s)\]]+", readme)
            for url in urls:
                host = urlparse(url).hostname
                is_codecov = host == "codecov.io" or (
                    host and host.endswith(".codecov.io")
                )
                if is_codecov:
                    return True
        for name in (
            "codecov.yml",
            "codecov.yaml",
            ".codecov.yml",
            ".codecov.yaml",
        ):
            if self._has_file(repo, name, branch):
                return True
        return False

    # ---------------------------- Crawl helpers ---------------------------- #
    def _basic_repo(self, repo: str) -> RepoInfo:
        """Fetch branch and commit info with minimal requests."""

        branch = self._branch_overrides.get(repo) or self._default_branch(repo)
        latest_commit, commit_date = self._latest_commit(repo, branch)
        if latest_commit:
            trunk_green = self._branch_green(repo, branch, latest_commit)
        else:
            trunk_green = None
        return RepoInfo(
            name=repo,
            branch=branch,
            coverage=None,
            patch_percent=None,
            uses_codecov=False,
            has_license=False,
            has_ci=False,
            has_agents=False,
            has_coc=False,
            has_contributing=False,
            has_precommit=False,
            installer="",
            latest_commit=latest_commit,
            workflow_count=0,
            trunk_green=trunk_green,
            commit_date=commit_date,
        )

    def _augment_repo(self, info: RepoInfo) -> None:
        """Populate remaining fields for ``info`` in-place."""

        repo = info.name
        branch = info.branch
        readme = self._fetch_file(repo, "README.md", branch)
        info.coverage = self._parse_coverage(readme, repo, branch)
        info.uses_codecov = self._uses_codecov(repo, branch, readme)
        info.patch_percent = self._patch_coverage_from_codecov(repo, branch)
        workflow_files = self._list_workflows(repo, branch)
        info.workflow_count = len(workflow_files)
        workflows_txt = "".join(
            [
                self._fetch_file(
                    repo,
                    f".github/workflows/{name}",
                    branch,
                )
                or ""
                for name in workflow_files
            ]
        )
        docker_txt = "".join(
            filter(
                None,
                [self._fetch_file(repo, p, branch) for p in self.DOCKER_FILES],
            )
        )
        pkg_txt = self._fetch_file(repo, "package.json", branch) or ""
        frontend_txt = (
            self._fetch_file(
                repo,
                "frontend/package.json",
                branch,
            )
            or ""
        )
        npm_scripts_txt = pkg_txt + frontend_txt
        info.installer = self._detect_installer(
            workflows_txt + docker_txt + npm_scripts_txt
        )  # noqa: E501
        info.has_license = self._has_file(repo, "LICENSE", branch)
        info.has_ci = self._has_ci(workflow_files)
        info.has_agents = self._has_file(repo, "AGENTS.md", branch)
        info.has_coc = self._has_file(repo, "CODE_OF_CONDUCT.md", branch)
        info.has_contributing = self._has_file(repo, "CONTRIBUTING.md", branch)
        info.has_precommit = self._has_file(
            repo,
            ".pre-commit-config.yaml",
            branch,
        )
        info.dark_pattern_count = self._detect_dark_patterns(repo, branch)
        info.bright_pattern_count = self._detect_bright_patterns(repo, branch)

    def crawl(self) -> List[RepoInfo]:
        infos = [self._basic_repo(r) for r in self.repos]
        for info in infos:
            self._augment_repo(info)
        return infos

    def generate_summary(self) -> str:
        repos = self.crawl()
        missing = []
        for r in repos:
            if not r.latest_commit or not r.commit_date:
                missing.append(r.name)
        if missing:
            raise RuntimeError(
                "Missing commit data for: {}. Pass a GitHub token via "
                "GITHUB_TOKEN to avoid rate limits.".format(", ".join(missing))
            )
        lines = [
            "# Repo Feature Summary",
            "",
            (
                "This table tracks which flywheel features each related "
                "repository has adopted."
            ),
            "",
            "<!-- spellchecker: disable -->",
        ]

        basics_header = (
            "| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |"  # noqa: E501
        )
        basics_sep = "| ---- | ------ | ------ | ----- | ----------------- |"
        lines.extend(["## Basics", basics_header, basics_sep])
        basics_rows = []

        coverage_header = "| Repo | Coverage | Patch | Codecov | Installer | Last-Updated (UTC) |"  # noqa: E501
        coverage_sep = "| ---- | -------- | ----- | ------- | --------- | ----------------- |"  # noqa: E501
        coverage_rows = []

        policy_header = "| Repo | License | CI | Workflows | AGENTS.md | Code of Conduct | Contributing | Pre-commit | Last-Updated (UTC) |"  # noqa: E501
        policy_sep = "| ---- | ------- | -- | --------- | --------- | --------------- | ------------ | ---------- | ----------------- |"  # noqa: E501
        policy_rows = []

        pattern_header = (
            "| Repo | Dark Patterns | Bright Patterns | Last-Updated (UTC) |"
        )
        pattern_sep = "| ---- | ------------- | --------------- | ----------------- |"  # noqa: E501
        pattern_rows = []

        for idx, info in enumerate(repos):
            coverage = "❌"
            if info.coverage:
                coverage = f"✅ ({info.coverage})"
            if info.patch_percent is None:
                patch = "—"
            else:
                passed = info.patch_percent >= PATCH_THRESHOLD
                emoji = "✅" if passed else "❌"
                patch = f"{emoji} ({info.patch_percent:.0f}%)"
            repo_link = f"[{info.name}](https://github.com/{info.name})"
            if idx == 0:
                repo_link = f"**{repo_link}**"
            commit = f"`{info.latest_commit}`" if info.latest_commit else "n/a"
            if info.installer == "uv":
                inst = "🚀 uv"
            elif info.installer == "partial":
                inst = "🔶 partial"
            else:
                inst = info.installer

            trunk = "n/a"
            if info.trunk_green is True:
                trunk = "✅"
            elif info.trunk_green is False:
                trunk = "❌"
            updated = info.commit_date or "n/a"
            basics_rows.append(
                f"| {repo_link} | {info.branch} | {commit} | {trunk} | {updated} |"  # noqa: E501
            )
            codecov = "✅" if info.uses_codecov else "❌"
            coverage_rows.append(
                "| {} | {} | {} | {} | {} | {} |".format(
                    repo_link,
                    coverage,
                    patch,
                    codecov,
                    inst,
                    updated,
                )
            )
            policy_rows.append(
                (
                    "| {repo} | {lic} | {ci} | {count} | {agents} | {coc} | "
                    "{cont} | {pre} | {updated} |"
                ).format(
                    repo=repo_link,
                    lic="✅" if info.has_license else "❌",
                    ci="✅" if info.has_ci else "❌",
                    count=info.workflow_count,
                    agents="✅" if info.has_agents else "❌",
                    coc="✅" if info.has_coc else "❌",
                    cont="✅" if info.has_contributing else "❌",
                    pre="✅" if info.has_precommit else "❌",
                    updated=updated,
                )
            )
            pattern_rows.append(
                (
                    f"| {repo_link} | {info.dark_pattern_count} | {info.bright_pattern_count} | {updated} |"  # noqa: E501
                )
            )

        lines.extend(basics_rows)
        lines.extend(
            [
                "",
                "## Coverage & Installer",
                coverage_header,
                coverage_sep,
            ]
        )
        lines.extend(coverage_rows)
        lines.extend(
            ["", "## Policies & Automation", policy_header, policy_sep]
        )  # noqa: E501
        lines.extend(policy_rows)
        lines.extend(
            [
                "",
                "## Dark & Bright Pattern Scan",
                pattern_header,
                pattern_sep,
            ]
        )
        lines.extend(pattern_rows)
        lines.append("")
        lines.append(
            "Legend: ✅ indicates the repo has adopted that feature from flywheel. 🚀 uv means only uv was found. "  # noqa: E501
            "🔶 partial signals a mix of uv and pip.\n"
            "Coverage percentages are parsed from their badges where available. Codecov shows ✅ when a Codecov config or badge is present. "  # noqa: E501
            "Patch shows ✅ when diff coverage is at least 90% and ❌ otherwise, with the percentage in parentheses.\n"  # noqa: E501
            "The commit column shows the short SHA of the latest default branch commit at crawl time. The Trunk column indicates whether CI is green for that commit. "  # noqa: E501
            "Dark Patterns and Bright Patterns list counts of suspicious or positive code snippets detected.\n"  # noqa: E501
            "Last-Updated (UTC) records the date of the commit used for each row."  # noqa: E501
        )
        return "\n".join(lines)
