"""Utilities to crawl GitHub repositories for flywheel features."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests


@dataclass
class RepoInfo:
    name: str
    branch: str
    coverage: Optional[str]
    has_license: bool
    has_ci: bool
    has_agents: bool
    has_coc: bool
    has_contributing: bool
    has_precommit: bool
    installer: str
    latest_commit: Optional[str]


class RepoCrawler:
    """Check remote GitHub repos for standard flywheel features."""

    # Filenames whose presence in `.github/workflows/` signals that the repo
    # runs some form of continuous integration. This keeps the heuristic broad
    # so repos with custom workflow names still count.
    CI_KEYWORDS = ("ci", "test", "lint", "build", "docs")

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
            resp = self.session.get(url)
            if resp.status_code == 200:
                return resp.text
        return None

    def _default_branch(self, repo: str) -> str:
        url = f"https://api.github.com/repos/{repo}"
        resp = self.session.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
        )
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
        resp = self.session.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
        )
        if resp.status_code == 200:
            try:
                return resp.json()[0]["sha"][:7]
            except Exception:
                return None
        return None

    def _has_file(self, repo: str, path: str, branch: str) -> bool:
        return self._fetch_file(repo, path, branch) is not None

    def _list_workflows(self, repo: str, branch: str) -> set[str]:
        """Return workflow filenames under `.github/workflows` for the repo."""
        url = (
            "https://api.github.com/repos/"
            f"{repo}/contents/.github/workflows?ref={branch}"
        )
        resp = self.session.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
        )
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

    # ------------------------ Coverage helpers ------------------------ #
    def _coverage_from_codecov(self, repo: str, branch: str) -> Optional[str]:
        """Retrieve coverage percentage from the shields.io Codecov proxy."""
        url = f"https://img.shields.io/codecov/c/github/{repo}/{branch}.svg"
        resp = self.session.get(url, timeout=10)
        if resp.status_code == 200:
            m = re.search(r">(\d{1,3})%<", resp.text)
            if m:
                return f"{m.group(1)}%"
        return None

    def _parse_coverage(
        self, readme: Optional[str], repo: str, branch: str
    ) -> Optional[str]:
        if not readme:
            return None

        # 1. Fast path – percentage already in the README (shields badge, etc.)
        m = re.search(r"(\d{1,3})%", readme)
        if m:
            return f"{m.group(1)}%"

        # 2. README mentions Codecov → query shields proxy.
        if "codecov.io" in readme:
            pct = self._coverage_from_codecov(repo, branch)
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
        workflow_files = self._list_workflows(repo, branch)
        wf1 = (
            self._fetch_file(
                repo,
                ".github/workflows/01-lint-format.yml",
                branch,
            )
            or ""
        )
        wf2 = (
            self._fetch_file(
                repo,
                ".github/workflows/02-tests.yml",
                branch,
            )
            or ""
        )
        installer = (
            "uv"
            if (
                "uv pip" in wf1
                or "uv pip" in wf2
                or "setup-uv" in wf1
                or "setup-uv" in wf2
            )
            else "pip"
        )
        latest_commit = self._latest_commit(repo, branch)
        return RepoInfo(
            name=repo,
            branch=branch,
            coverage=coverage,
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
        )

    def crawl(self) -> List[RepoInfo]:
        return [self._check_repo(r) for r in self.repos]

    def generate_summary(self) -> str:
        repos = self.crawl()
        header = (
            "| Repo | Branch | Coverage | Installer | License | CI | "
            "AGENTS.md | Code of Conduct | Contributing | Pre-commit | "
            "Commit |"
        )
        sep = (
            "| ---- | ------ | -------- | --------- | ------- | -- | "
            "--------- | --------------- | ------------ | ---------- | "
            "------ |"
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
            header,
            sep,
        ]
        for idx, info in enumerate(repos):
            coverage = "❌"
            if info.coverage:
                coverage = f"✅ ({info.coverage})"
            repo_link = f"[{info.name}](https://github.com/{info.name})"
            if idx == 0:
                repo_link = f"**{repo_link}**"
            commit = f"`{info.latest_commit}`" if info.latest_commit else "n/a"
            row = "| {} | {} | {} | {} | {} | {} | {} | {} | ".format(
                repo_link,
                info.branch,
                coverage,
                "🚀 uv" if info.installer == "uv" else "pip",
                "✅" if info.has_license else "❌",
                "✅" if info.has_ci else "❌",
                "✅" if info.has_agents else "❌",
                "✅" if info.has_coc else "❌",
            ) + "{} | {} | {} |".format(
                "✅" if info.has_contributing else "❌",
                "✅" if info.has_precommit else "❌",
                commit,
            )
            lines.append(row)
        lines.append("")
        lines.append(
            "Legend: ✅ indicates the repo has adopted that feature from "
            "flywheel. 🚀 uv highlights repos using uv for faster installs. "
            "Coverage percentages are parsed from their badges where "
            "available. The commit column shows the short SHA of the latest "
            "default branch commit at crawl time."
        )
        return "\n".join(lines)
