---
title: 'Flywheel Codex Prompt'
slug: 'codex-automation'
---

# Codex Automation Prompt
Type: evergreen

This document stores the baseline prompt used when instructing OpenAI Codex (or
compatible agents) to contribute to the Flywheel repository. Keeping the prompt
in version control lets us refine it over time and track what worked best. It
serves as the canonical prompt that other repositories should copy to
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
- If browser dependencies are missing, run `npm run playwright:install` or
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

### How to choose a prompt

| When you want to…                        | Use prompt |
|------------------------------------------|-----------|
| Add new insights (metrics, health scans) | 1         |

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
You are an automated contributor for the Flywheel repository. Follow `AGENTS.md` and `README.md`. Ensure `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`, `python -m flywheel.fit`, and `bash scripts/checks.sh` pass before committing. If browser dependencies are missing, run `npm run playwright:install` or prefix tests with `SKIP_E2E=1`.

USER:
1. Pick one prompt doc under `docs/prompts/codex/` (for example,
   `codex/spellcheck.md`).
2. Fix outdated instructions, links or formatting.
3. Regenerate `docs/prompt-docs-summary.md` with
   `python scripts/update_prompt_docs_summary.py --repos-from \
   dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`.
4. Run the checks above.

OUTPUT:
A pull request with the improved prompt doc and passing checks.
```
