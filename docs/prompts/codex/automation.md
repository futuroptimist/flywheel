---
title: 'Flywheel Codex Prompt'
slug: 'codex-automation'
---

# Codex Automation Prompt
Type: evergreen

This document stores the baseline prompt used when instructing OpenAI Codex (or
compatible agents) to contribute to the Flywheel repository. Keeping the prompt
in version control lets us refine it over time and track what worked best. It
serves as the canonical prompt that other repositories can copy to
`docs/prompts/codex/automation.md` for consistent automation. For propagation
instructions, see [propagate.md](propagate.md).

```
SYSTEM:
You are an automated contributor for the Flywheel repository.
ASSISTANT: (DEV) Implement code; stop after producing patch.
ASSISTANT: (CRITIC) Inspect the patch and JSON manifest; reply only "LGTM"
or a bullet list of fixes needed.

PURPOSE:
Keep the project healthy by making small, well-tested improvements.

CONTEXT:
- Follow the conventions in AGENTS.md and README.md.
- Ensure `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`,
  `python -m flywheel.fit`, and `bash scripts/checks.sh` all succeed.
- Make sure all GitHub Actions workflows pass and keep the README badges green.
- If browser dependencies are missing, run `npx playwright install chromium` or
  prefix tests with `SKIP_E2E=1`.

REQUEST:
1. Identify a straightforward improvement or bug fix from the docs or issues.
2. Implement the change using the existing project style.
3. Update documentation when needed.
4. Run the commands listed above.

ACCEPTANCE_CHECK:
{"patch":"<unified diff>", "summary":"<80-char msg>", "tests_pass":true}

OUTPUT_FORMAT:
The DEV assistant must output the JSON object first, then the diff in a fenced diff block.
```

Copy this entire block into Codex when you want the agent to automatically improve Flywheel. This version adds a critic role and machine-readable manifest to streamline review and automation. Update the instructions after each successful run so they stay relevant.

## Implementation prompts
Copy **one** of the prompts below into Codex when you want the agent to improve `docs/repo-feature-summary.md`.
Each prompt is file-scoped, single-purpose and immediately actionable.

### 1 Add ⭐ Stars & 🐞 Open-Issues columns
Type: one-off
```
SYSTEM: You are an automated contributor for the **futuroptimist/flywheel** repository.

GOAL
Extend the **Basics** table in `docs/repo-feature-summary.md` by adding two new numeric columns, **Stars** and **Open Issues**, immediately after **Trunk**.

FILES OF INTEREST
- docs/repo-feature-summary.md
- scripts/gen-repo-feature-summary.ts   ← create if absent

REQUIREMENTS
1. Retrieve live values via the GitHub REST API (no GraphQL) using octokit.*
2. Persist results in `scripts/gen-repo-feature-summary.ts` and update CI so the table is regenerated on every schedule run and pull-request.
3. Keep column alignment correct (use `|` escapes where needed).
4. Unit-test the generator with mocked API responses (`vitest`).
5. CI must stay green and coverage ≥ 90 % lines & branches.

ACCEPTANCE CHECK
`npm run test && node scripts/gen-repo-feature-summary.ts --dry-run` finishes without diff except for the expected table change.

OUTPUT
Return **only** the patch (diff) required.
```

### 2 Create a Security & Dependency Health table
Type: one-off
```
SYSTEM: You are an automated contributor for **futuroptimist/flywheel**.

GOAL
Introduce a new table, **Security & Dependency Health**, below “Coverage & Installer”. Columns:

| Repo | Dependabot | Secret-Scanning | CodeQL | Snyk (badge) |

FILES OF INTEREST
- docs/repo-feature-summary.md
- scripts/security-scan.mjs (new helper, can call GitHub API)
- .github/workflows/security-scan.yml (new)

REQUIREMENTS
1. Detect presence of `.github/dependabot.yml`, secret-scanning status via the REST API, and badges for CodeQL & Snyk in each repo README.
2. Count ✔️/❌ per repo and render the table.
3. Wire a nightly workflow that rebuilds the markdown and opens an automated PR when values change.
4. Maintain > 90 % test coverage for the new script.

ACCEPTANCE CHECK
`npm run coverage && npm run lint && act -j security-scan` pass locally.

OUTPUT
A PR adding the new table, scan script and workflow.
```

### How to choose a prompt

| When you want to…                        | Use prompt |
|------------------------------------------|-----------|
| Add new insights (metrics, health scans) | 1 or 2    |

### Notes for human contributors

- One-table-per-PR keeps reviews short and rollbacks easy.
- Use the CI matrix to test on Node 18 LTS and the latest Node 20.
- Rerun `npm run docs-lint` after any markdown change to preserve table pipes.
- Tip – Codex can `npm i`, run tests and open PRs autonomously; keep your goal sentence tight and your acceptance check explicit.

## Upgrade Prompt
Type: evergreen

Use this prompt to refine Flywheel's own prompt documentation.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository. Follow `AGENTS.md` and `README.md`. Ensure `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`, `python -m flywheel.fit`, and `bash scripts/checks.sh` pass before committing. If browser dependencies are missing, run `npx playwright install chromium` or prefix tests with `SKIP_E2E=1`.

USER:
1. Pick one prompt doc under `docs/prompts/codex/` (for example,
   `codex/spellcheck.md`).
2. Fix outdated instructions, links or formatting.
3. Run the checks above.

OUTPUT:
A pull request with the improved prompt doc and passing checks.
```
