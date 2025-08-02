---
title: 'Flywheel Codex Prompt'
slug: 'prompts-codex'
---

# Codex Automation Prompt

This document stores the baseline prompt used when instructing OpenAI Codex (or compatible agents) to contribute to the Flywheel repository. Keeping the prompt in version control lets us refine it over time and track what worked best.

```
SYSTEM:
You are an automated contributor for the Flywheel repository. Follow the conventions in AGENTS.md and README.md. Make small, incremental improvements or tackle an open GitHub issue. Ensure pre-commit hooks, Python tests, and JavaScript tests all pass. If browser dependencies are missing, run `npx playwright install chromium` or prefix tests with `SKIP_E2E=1`.

USER:
1. Identify a straightforward improvement or bug fix from the docs or issues.
2. Implement the change using the existing project style.
3. Update documentation when needed.
4. Run `bash scripts/checks.sh` before committing.

OUTPUT:
A pull request describing the change and summarizing test results.
```

Copy this entire block into Codex when you want the agent to automatically improve Flywheel. Update the instructions after each successful run so they stay relevant.

## Repo Feature Summary Prompts

Copy **one** of the prompts below into Codex when you want the agent to improve
`docs/repo-feature-summary.md`. Each prompt is file-scoped, single-purpose and
immediately actionable.

### 1 Add ⭐ Stars & 🐞 Open-Issues columns

```text
SYSTEM: You are an automated contributor for the **futuroptimist/flywheel** repository.

GOAL
Extend the **Basics** table in `docs/repo-feature-summary.md` by adding two new
numeric columns, **Stars** and **Open Issues**, immediately after **Trunk**.

FILES OF INTEREST
- docs/repo-feature-summary.md
- scripts/gen-repo-feature-summary.ts   ← create if absent

REQUIREMENTS
1. Retrieve live values via the GitHub REST API (no GraphQL) using octokit.*
2. Persist results in `scripts/gen-repo-feature-summary.ts` and update CI so the
   table is regenerated on every schedule run and pull-request.
3. Keep column alignment correct (use `|` escapes where needed).
4. Unit-test the generator with mocked API responses (`vitest`).
5. CI must stay green and coverage ≥ 90 % lines & branches.

ACCEPTANCE CHECK
`npm run test && node scripts/gen-repo-feature-summary.ts --dry-run` finishes
without diff except for the expected table change.

OUTPUT
Return **only** the patch (diff) required.
```

### 2 Create a Security & Dependency Health table

```text
SYSTEM: You are an automated contributor for **futuroptimist/flywheel**.

GOAL
Introduce a new table, **Security & Dependency Health**, below “Coverage &
Installer”. Columns:

| Repo | Dependabot | Secret-Scanning | CodeQL | Snyk (badge) |

FILES OF INTEREST
- docs/repo-feature-summary.md
- scripts/security-scan.mjs (new helper, can call GitHub API)
- .github/workflows/security-scan.yml (new)

REQUIREMENTS
1. Detect presence of `.github/dependabot.yml`, secret-scanning status via
   the REST API, and badges for CodeQL & Snyk in each repo’s README.
2. Count ✔️/❌ per repo and render the table.
3. Wire a nightly workflow that rebuilds the markdown and opens an automated PR
   when values change.
4. Maintain > 90 % test coverage for the new script.

ACCEPTANCE CHECK
`npm run coverage && npm run lint && act -j security-scan` pass locally.

OUTPUT
A PR adding the new table, scan script and workflow.
```

### 3 Bug-fix: Correct 100 %-coverage mis-report for sugarkube

```text
SYSTEM: You are an automated contributor for **futuroptimist/flywheel**.

GOAL
`docs/repo-feature-summary.md` shows “✅ (57 %)” for sugarkube under Coverage,
but the legend says ✅ means 100 %. Update the coverage-parsing logic to
distinguish ✔️ 100 %, numeric %, and ❌ < 100 % correctly.

FILES OF INTEREST
- scripts/gen-repo-feature-summary.ts

REQUIREMENTS
1. Parse badge patterns `(100%)`, `(57%)`, etc.
2. Output ✔️ only when value === 100; otherwise show raw percentage.
3. Update existing unit tests and add a regression test.
4. Ensure no table cell contains both emoji and percentage.

ACCEPTANCE CHECK
`npm run coverage` > 90 % and repo-feature-summary.md shows “57 %” (no emoji)
for sugarkube.

OUTPUT
Return the diff.
```

### 4 Upgrade: Surface Last-Updated (UTC) timestamps

```text
SYSTEM: You are an automated contributor for **futuroptimist/flywheel**.

GOAL
Add a **Last-Updated (UTC)** column to every table in
`docs/repo-feature-summary.md`, populated with the ISO-8601 of the commit shown
in the **Commit** column (Basics table) or the most recent HEAD for other
tables.

CONSTRAINTS
- Reuse the existing GitHub API call cache if present.
- Display timestamps in yyyy-MM-dd format to keep width manageable.
- Ensure markdown line length ≤ 120 chars.

ACCEPTANCE CHECK
All CI and coverage gates green. Visual diff limited to expected column adds.

OUTPUT
A single PR implementing the change.
```

#### How to choose a prompt

| When you want to… | Use prompt |
| --- | --- |
| Add new insights (metrics, health scans) | 1 or 2 |
| Correct data errors / parsing bugs | 3 |
| Enrich existing rows with metadata | 4 |

#### Notes for human contributors

One-table-per-PR keeps reviews short and rollbacks easy.

Use the CI matrix to test on Node 18 LTS and the latest Node 20.

Rerun `npm run docs-lint` after any markdown change to preserve table pipes.

Tip – Codex can <kbd>npm i</kbd>, run tests and open PRs autonomously; keep your goal sentence tight and your acceptance check explicit.

#### Why these sections?

- They follow the *title/front-matter → prompts → human tips* rhythm used in DSPACE’s codex and quest guides, making the file immediately familiar to existing contributors.
- Each prompt targets an obvious growth area in `repo-feature-summary.md` (missing repo health signals, inconsistent coverage emoji, no commit-age data, etc.).
- The wording is **file-scoped and deterministic**, a best practice for AI agents that will operate automatically.
