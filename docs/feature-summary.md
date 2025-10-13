# Feature Summary

<!-- BEGIN: RELEASE-READINESS DASHBOARD -->
# Release‑Readiness Dashboard (Aug–Sep 2025)

**How to use:** Check items as they are completed. `[ ]` open, `[x]` done.
See [repo-feature-summary.md](repo-feature-summary.md) for auto-generated
feature adoption across repositories.

**Definition of Done for v0.1**

- [ ] Tag `v0.1` and publish release notes
- [ ] 1‑click install path available
- [ ] 90‑second demo video or GIF
- [ ] Quickstart and mini-architecture diagram
- [ ] CI + coverage badges in README
- [ ] CodeQL, Dependabot, and secret scanning enabled
- [ ] Docs include FAQ and Known issues
- [ ] “Alpha” status badge
- [ ] ≥3 good‑first‑issues labeled

| Repo | v0.1 tag | Release notes | 1‑click install | Demo | Landing page | CI green | Coverage badge | Security scans | Arch doc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [token.place](https://github.com/futuroptimist/token.place) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [f2clipboard](https://github.com/futuroptimist/f2clipboard) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [flywheel](https://github.com/futuroptimist/flywheel) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [gitshelves](https://github.com/futuroptimist/gitshelves) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [sugarkube](https://github.com/futuroptimist/sugarkube) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [sigma](https://github.com/futuroptimist/sigma) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [DSPACE](https://github.com/democratizedspace/dspace) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Other | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

<details>
<summary><a href="https://github.com/futuroptimist/token.place">token.place</a></summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] `docker compose` for relay+server+mock LLM (single command)
- [ ] Basic threat model & privacy notes
- [ ] Sample benchmarks (latency/throughput on a canned workload)

</details>

<details>
<summary><a href="https://github.com/futuroptimist/f2clipboard">f2clipboard</a></summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] Publish to **PyPI**; recommend `pipx install f2clipboard`
- [x] CLI `--help` includes 2 concrete examples _(flywheel)_
- [ ] Shell completions (bash/zsh/fish)

</details>

<details>
<summary><a href="https://github.com/futuroptimist/flywheel">flywheel</a></summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] Mark as **Template** repo
- [ ] “Use this template” one‑page walkthrough + screenshot/GIF
- [x] Option to inject best‑practice scaffolding via `--save-dev`

</details>

<details>
<summary><a href="https://github.com/futuroptimist/gitshelves">gitshelves</a></summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] Usage examples for common “archive/shelf” flows
- [ ] Large file story (Git LFS?) if relevant

</details>

<details>
<summary><a href="https://github.com/futuroptimist/sugarkube">sugarkube</a></summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] KiCad/BOM artifacts attached to releases
- [ ] Assembly instructions w/ photos; cut list

</details>

<details>
<summary><a href="https://github.com/futuroptimist/sigma">sigma (ESP32 “AI pin”)</a></summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] Firmware: build steps + prebuilt artifact
- [ ] Test jig notes; bring‑up checklist
- [ ] Enclosure STLs + simple print settings

</details>

<details>
<summary><a href="https://github.com/democratizedspace/dspace">DSPACE</a></summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] MVP sim core + one “quest” example
- [ ] Data model & plugin architecture sketch
- [ ] “A/B test gardening params” example scenario

</details>

<details>
<summary>Other/placeholder</summary>

1) **Releases & Packaging**
- [ ] Tag **v0.1.0** and push tag
- [ ] Write release notes with **What’s new**, **Try it in 60s**, **Roadmap next**
- [ ] Adopt SemVer; add CHANGELOG (or Release Drafter)
- [ ] 1-click install path(s):
  - [ ] `pipx install <pkg>` (if Python CLI)
  - [ ] `docker run ghcr.io/<owner>/<image>:<tag>` or `docker compose up`
  - [ ] Homebrew formula or Scoop/winget (optional; if widely useful)

2) **On‑Ramp & Dev Experience**
- [ ] `make dev` (or `uv`/`just`) to spin up everything locally (no config)
- [ ] `make test`, `make lint`, `make fmt`, `make docs`
- [ ] Devcontainer (`.devcontainer/`) for Codespaces
- [ ] Pre‑commit with ruff/black/isort/mypy (or equivalents)

3) **CI & Quality**
- [ ] GitHub Actions: lint+test+coverage on PRs / default branch
- [ ] Coverage report + **Codecov badge** in README
- [ ] OS/Python matrix (if applicable)
- [ ] Smoke test workflow; gate release on passing status
- [ ] Automated publish on tag (PyPI / GHCR / Homebrew tap as relevant)

4) **Security & Supply Chain**
- [ ] CodeQL enabled
- [ ] Secret scanning + push protection
- [ ] Dependabot (or Renovate) for deps + GH Actions
- [ ] (Optional) SBOM (syft) + provenance (SLSA) for releases

5) **Docs & Comms**
- [ ] README “above the fold” pitch + **Quickstart (≤60s)**
- [ ] **90‑second demo GIF/video** linked at top
- [ ] **Architecture** (3 bullets + one diagram image)
- [ ] Status badge (“Alpha”) + Support matrix (if applicable)
- [ ] FAQ / Known issues / Footguns
- [ ] Website or GitHub Pages landing page (when appropriate)

6) **Community & Operations**
- [ ] CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Issue/PR templates
- [ ] ≥3 “good first issue” tickets
- [ ] Project board or milestones

**Repo-specific extras**
- [ ] (placeholder)

</details>

### Global tasks (non‑repo‑specific)

- [ ] Update GitHub profile with “Hiring managers start here” + links to top **two** releases/demos
- [ ] Land **2–3 upstream PRs** in dependencies you already use
- [ ] Ensure LICENSE and SECURITY.md present across repos

For longer-term cross-repo planning, see [REPOS_ROADMAP.md](REPOS_ROADMAP.md).

<!-- END: RELEASE-READINESS DASHBOARD -->
