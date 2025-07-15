"""Utilities to crawl GitHub repositories for flywheel features."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests
from requests import RequestException

PATCH_THRESHOLD = 90.0
BADGE_PATCH = "https://img.shields.io/codecov/patch/github/{repo}/{branch}.svg"


@dataclass
class RepoInfo:
    name: str
    branch: str
    coverage: Optional[str]
    patch_percent: Optional[float]
    has_license: bool
    has_ci: bool
    has_agents: bool
    has_coc: bool
    has_contributing: bool
    has_precommit: bool
    installer: str
    latest_commit: Optional[str]
    workflow_count: int


class RepoCrawler:
    """Check remote GitHub repos for standard flywheel features."""

    # Filenames whose presence in `.github/workflows/` signals that the repo
    # runs some form of continuous integration. This keeps the heuristic broad
    # so repos with custom workflow names still count.
    CI_KEYWORDS = ("ci", "test", "lint", "build", "docs")

    _UV_OK = re.compile(r"\buv\s+pip\b", re.I)
    _PIP_BAD = re.compile(
        r"""
        (?<!\buv\s)(?<!\w)(?:pip3?|python\s+-m\s+pip)\s+install
        |pip\s+compile
        |apt[\w\- ]+python3?-pip
        """,
        re.I | re.X,
    )

    DOCKER_FILES = (
        "Dockerfile",
        "Dockerfile.dev",
        "Dockerfile.prod",
        "docker/Dockerfile",
        "frontend/Dockerfile",
    )

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
        self.session = session or requests.Session()
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
                resp = self.session.get(url)
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
            )
        except RequestException:
            return "main"
        if resp.status_code == 200:
            try:
                return resp.json().get("default_branch", "main")
            except Exception:
                return "main"
        return "main"

    def _latest_commit(self, repo: str, branch: str) -> Optional[str]:
        url = "https://api.github.com/repos/%s/commits?per_page=1&sha=%s" % (
            repo,
            branch,
        )
        try:
            resp = self.session.get(
                url,
                headers={"Accept": "application/vnd.github+json"},
            )
        except RequestException:
            return None
        if resp.status_code == 200:
            try:
                return resp.json()[0]["sha"][:7]
            except Exception:
                return None
        return None

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
            )
        except RequestException:
            return set()
        if resp.status_code == 200:
            try:
                return {item.get("name", "") for item in resp.json()}
            except Exception:
                return set()
        return set()

    def _has_ci(self, workflow_files: set[str]) -> bool:
        """Return True if any workflow filename hints at CI presence."""
        return any(
            any(k in wf.lower() for k in self.CI_KEYWORDS)
            for wf in workflow_files  # noqa: E501
        )

    def _detect_installer(self, text: str) -> str:
        """Return 'uv', 'partial', or 'pip' based on shell snippets."""
        has_uv = bool(self._UV_OK.search(text))
        has_pip = bool(self._PIP_BAD.search(text))
        if has_uv and not has_pip:
            return "uv"
        if has_uv and has_pip:
            return "partial"
        return "pip"

    # ------------------------ Coverage helpers ------------------------ #
    def _project_coverage_from_codecov(
        self,
        repo: str,
        branch: str,
    ) -> Optional[str]:
        """Retrieve project coverage percentage via shields.io."""
        url = f"https://img.shields.io/codecov/c/github/{repo}/{branch}.svg"
        try:
            resp = self.session.get(url, timeout=10)
        except RequestException:
            return None
        if resp.status_code == 200:
            m = re.search(r">(\d{1,3})%<", resp.text)
            if m:
                return f"{m.group(1)}%"
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
        totals = (
            "https://api.codecov.io/api/v2/github/"
            f"{owner}/repos/{name}/totals/?branch={branch}"
        )
        try:
            resp = self.session.get(totals, headers=headers, timeout=10)
            if resp.status_code == 200:
                body = resp.json()
                # fmt: off
                pct = (
                    body.get("totals", {})
                    .get("patch", {})
                    .get("coverage")
                )
                # fmt: on
                if pct is not None:
                    return float(pct)
        except RequestException:
            pass
        except Exception:
            pass

        commits = self._recent_commits(repo, branch, 2)
        if len(commits) == 2:
            base, head = commits[1], commits[0]
        else:
            base, head = "HEAD~1", "HEAD"
        compare = (
            "https://api.codecov.io/api/v2/github/"
            f"{owner}/repos/{name}/compare/?base={base}&head={head}"
        )
        try:
            resp = self.session.get(compare, headers=headers, timeout=10)
            if resp.status_code == 200:
                body = resp.json()
                # fmt: off
                pct = (
                    body.get("totals", {})
                    .get("patch", {})
                    .get("coverage")
                )
                # fmt: on
                if pct is not None:
                    return float(pct)
        except RequestException:
            pass
        except Exception:
            pass

        return self._badge_patch_percent(repo, branch)

    def _parse_coverage(
        self, readme: Optional[str], repo: str, branch: str
    ) -> Optional[str]:
        if not readme:
            return None

        # 1. Fast path – percentage already in the README (shields badge, etc.)
        coverage_match = (
            re.search(r"coverage-(\d+)%25", readme)
            or re.search(r"codecov.*?(\d+)%", readme)
            or re.search(r"(\d{1,3})%", readme)
        )
        if coverage_match:
            return f"{coverage_match.group(1)}%"

        # 2. README mentions Codecov → query shields proxy.
        if "codecov.io" in readme:
            pct = self._project_coverage_from_codecov(repo, branch)
            if pct:
                return pct

        # 3. We spoke about coverage but still no number.
        if "coverage" in readme.lower():
            return "unknown"
        return None

    def _check_repo(self, repo: str) -> RepoInfo:
        branch = self._branch_overrides.get(repo) or self._default_branch(repo)
        readme = self._fetch_file(repo, "README.md", branch)
        coverage = self._parse_coverage(readme, repo, branch)
        patch_cov = self._patch_coverage_from_codecov(repo, branch)
        workflow_files = self._list_workflows(repo, branch)
        workflow_count = len(workflow_files)
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

        installer = self._detect_installer(
            workflows_txt + docker_txt + npm_scripts_txt
        )  # noqa: E501
        latest_commit = self._latest_commit(repo, branch)
        return RepoInfo(
            name=repo,
            branch=branch,
            coverage=coverage,
            patch_percent=patch_cov,
            has_license=self._has_file(repo, "LICENSE", branch),
            has_ci=self._has_ci(workflow_files),
            has_agents=self._has_file(repo, "AGENTS.md", branch),
            has_coc=self._has_file(repo, "CODE_OF_CONDUCT.md", branch),
            has_contributing=self._has_file(repo, "CONTRIBUTING.md", branch),
            has_precommit=self._has_file(
                repo,
                ".pre-commit-config.yaml",
                branch,
            ),
            installer=installer,
            latest_commit=latest_commit,
            workflow_count=workflow_count,
        )

    def crawl(self) -> List[RepoInfo]:
        return [self._check_repo(r) for r in self.repos]

    def generate_summary(self) -> str:
        repos = self.crawl()
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

        basics_header = "| Repo | Branch | Commit |"
        basics_sep = "| ---- | ------ | ------ |"
        lines.extend(["## Basics", basics_header, basics_sep])
        basics_rows = []

        coverage_header = "| Repo | Coverage | Patch | Installer |"
        coverage_sep = "| ---- | -------- | ----- | --------- |"
        coverage_rows = []

        policy_header = (
            "| Repo | License | CI | Workflows | AGENTS.md |"
            " Code of Conduct | Contributing | Pre-commit |"
        )
        policy_sep = (
            "| ---- | ------- | -- | --------- | --------- |"
            " --------------- | ------------ | ---------- |"
        )
        policy_rows = []

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
                inst = "pip"

            basics_rows.append(f"| {repo_link} | {info.branch} | {commit} |")
            coverage_rows.append(
                "| {} | {} | {} | {} |".format(
                    repo_link,
                    coverage,
                    patch,
                    inst,
                )
            )
            policy_rows.append(
                (
                    "| {repo} | {lic} | {ci} | {count} | {agents} | {coc} | "
                    "{cont} | {pre} |"
                ).format(
                    repo=repo_link,
                    lic="✅" if info.has_license else "❌",
                    ci="✅" if info.has_ci else "❌",
                    count=info.workflow_count,
                    agents="✅" if info.has_agents else "❌",
                    coc="✅" if info.has_coc else "❌",
                    cont="✅" if info.has_contributing else "❌",
                    pre="✅" if info.has_precommit else "❌",
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
        lines.append("")
        lines.append(
            "Legend: ✅ indicates the repo has adopted that feature from "
            "flywheel. 🚀 uv means only uv was found. "
            "🔶 partial signals a mix of uv and pip. "
            "Coverage percentages are parsed from their badges where "
            "available. Patch shows ✅ when diff coverage is at least 90% "
            "and ❌ otherwise, with the percentage in parentheses. "
            "The commit column shows the short SHA of the latest default "
            "branch commit at crawl time."
        )
        return "\n".join(lines)
