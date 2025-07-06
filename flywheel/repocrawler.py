"""Utilities to crawl GitHub repositories for flywheel features."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests


@dataclass
class RepoInfo:
    name: str
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

    def __init__(
        self, repos: Iterable[str], session: Optional[requests.Session] = None
    ) -> None:
        self.repos = list(repos)
        self.session = session or requests.Session()

    def _fetch_file(self, repo: str, path: str) -> Optional[str]:
        for branch in ("main", "master"):
            base = "https://raw.githubusercontent.com/"
            url = f"{base}{repo}/{branch}/{path}"
            resp = self.session.get(url)
            if resp.status_code == 200:
                return resp.text
        return None

    def _latest_commit(self, repo: str) -> Optional[str]:
        url = f"https://api.github.com/repos/{repo}/commits?per_page=1"
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

    def _has_file(self, repo: str, path: str) -> bool:
        return self._fetch_file(repo, path) is not None

    def _parse_coverage(self, readme: Optional[str]) -> Optional[str]:
        if not readme:
            return None
        match = re.search(r"(\d{1,3})%", readme)
        if match:
            return f"{match.group(1)}%"
        if "coverage" in readme.lower():
            return "unknown"
        return None

    def _check_repo(self, repo: str) -> RepoInfo:
        readme = self._fetch_file(repo, "README.md")
        coverage = self._parse_coverage(readme)
        wf1 = (
            self._fetch_file(
                repo,
                ".github/workflows/01-lint-format.yml",
            )
            or ""
        )
        wf2 = self._fetch_file(repo, ".github/workflows/02-tests.yml") or ""
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
        latest_commit = self._latest_commit(repo)
        return RepoInfo(
            name=repo,
            coverage=coverage,
            has_license=self._has_file(repo, "LICENSE"),
            has_ci=self._has_file(
                repo,
                ".github/workflows/01-lint-format.yml",
            ),
            has_agents=self._has_file(repo, "AGENTS.md"),
            has_coc=self._has_file(repo, "CODE_OF_CONDUCT.md"),
            has_contributing=self._has_file(repo, "CONTRIBUTING.md"),
            has_precommit=self._has_file(repo, ".pre-commit-config.yaml"),
            installer=installer,
            latest_commit=latest_commit,
        )

    def crawl(self) -> List[RepoInfo]:
        return [self._check_repo(r) for r in self.repos]

    def generate_summary(self) -> str:
        repos = self.crawl()
        header = (
            "| Repo | Coverage | Installer | License | CI | AGENTS.md | "
            "Code of Conduct | Contributing | Pre-commit | Commit |"
        )
        sep = (
            "| ---- | -------- | --------- | ------- | -- | --------- | "
            "--------------- | ------------ | ---------- | ------ |"
        )
        lines = [
            "# Repo Feature Summary",
            "",
            (
                "This table tracks which flywheel features each related "
                "repository has adopted."
            ),
            "",
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
            row = "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                repo_link,
                coverage,
                "🚀 uv" if info.installer == "uv" else "pip",
                "✅" if info.has_license else "❌",
                "✅" if info.has_ci else "❌",
                "✅" if info.has_agents else "❌",
                "✅" if info.has_coc else "❌",
                "✅" if info.has_contributing else "❌",
                "✅" if info.has_precommit else "❌",
                info.latest_commit or "n/a",
            )
            lines.append(row)
        lines.append("")
        lines.append(
            "Legend: ✅ indicates the repo has adopted that feature from "
            "flywheel. 🚀 uv highlights repos using uv for faster installs. "
            "Coverage percentages are parsed from their badges where "
            "available. The commit column shows the short SHA of the latest "
            "main branch commit at crawl time."
        )
        return "\n".join(lines)
