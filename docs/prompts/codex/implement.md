---
title: "Codex Implement Prompt"
slug: "codex-implement"
---

# Codex Implement Prompt

Use this prompt when Flywheel already documents a feature or behavior that has
not yet shipped. The goal is to finish the promised functionality with tight
feedback loops, traceable documentation, and green checks.

## When to use it

- A TODO, FIXME, "future work" entry, design doc, or changelog note promises a
  capability that does not yet exist.
- The feature is still relevant, has a clear success condition, and fits in a
  single PR without a long-running migration.
- You can add or update automated tests to lock in the expected behavior and
  prevent regressions.

## Preparation checklist

Run through this list before launching the prompt so that work starts with the
latest context and tooling:

1. Confirm the referenced spec or TODO still matches product goals.
2. Skim `AGENTS.md`, `README.md`, and any module-level docs that apply to the
   target area.
3. Review `.github/workflows/` to mirror CI locally (linting, tests, security
   scans, docs builds).
4. Install dependencies with `uv pip install --system -r requirements.txt`
   (or `pip install -r requirements.txt`), `npm ci`, and any per-module setup
   scripts.
5. Make sure you can run `pre-commit run --all-files`, `pytest -q`,
   `npm run lint`, `npm run format:check`, `npm run test:ci`,
   `python -m flywheel.fit`, and `bash scripts/checks.sh` without unexpected
   failures.

## Prompt block

```prompt
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Ship a documented but unimplemented Flywheel feature with tests and docs.

USAGE NOTES:
- Prompt name: `prompt-implement`.
- Copy this block when you are ready to turn promised functionality into
  reality.
- Keep the change minimal, well-tested, and scoped to a single PR.

CONTEXT:
- Follow `AGENTS.md`, `README.md`, and neighboring module docs for local
  conventions.
- Inspect `.github/workflows/` so local runs mirror required CI checks.
- Source lives in `flywheel/` (Python), `webapp/` (Next.js/TypeScript), and
  `viewer/` (three.js). Tests live in `tests/`, `webapp/`, and co-located
  modules.
- Run the full suite before committing:
  - `pre-commit run --all-files`
  - `pytest -q`
  - `npm run lint`
  - `npm run format:check`
  - `npm run test:ci`
  - `python -m flywheel.fit`
  - `bash scripts/checks.sh`
- Install dependencies with `uv pip install --system -r requirements.txt`
  (or `pip install -r requirements.txt`) and `npm ci`. Use per-module scripts
  such as `scripts/setup.sh` when required.
- Use `rg` (ripgrep) or targeted search to locate TODO, FIXME, design promises,
  and changelog entries tied to the feature. Prioritize changes that ship
  immediate value.
- Add targeted tests first, then make them pass. Keep coverage high and avoid
  regressions.
- Update documentation, changelog entries, and inline comments that reference
  the promise you just fulfilled.
- Scan staged changes with `git diff --cached | ./scripts/scan-secrets.py`.
- Refresh `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from \
  dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md` if you add or
  relocate prompt docs.

REQUEST:
1. Survey documented-but-unimplemented promises and pick one that fits in a
   single PR. Explain why it is actionable now.
2. Add or update automated tests that fail under current behavior and capture
   success, edge cases, and regressions.
3. Implement the minimal change to satisfy the promise, cleaning up stale notes
   or dead scaffolding.
4. Update related docs, changelog entries, or examples to reflect the shipped
   functionality and new tests.
5. Run the commands listed above. Fix any failures and summarize the results in
   the PR description.

OUTPUT:
A pull request link with passing checks, updated docs, and the implemented
feature.
```

## Upgrade Instructions

```upgrade
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Improve or expand `docs/prompts/codex/implement.md` so it stays accurate and
useful.

USAGE NOTES:
- Use this prompt when refining the implement prompt itself.
- Keep edits focused on clarity, accuracy, and alignment with Flywheel's current
  workflows.

CONTEXT:
- Follow `AGENTS.md`, `README.md`, and `.github/workflows/` for guardrails.
- Run `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`,
  `python -m flywheel.fit`, and `bash scripts/checks.sh` before committing.
- Confirm referenced files exist; update `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from \
  dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md` if prompt docs
  move or change.
- Scan staged changes with `git diff --cached | ./scripts/scan-secrets.py`.

REQUEST:
1. Revise `docs/prompts/codex/implement.md` for clarity, fresh links, and
   alignment with current repo practices.
2. Ensure instructions about tests, docs, and tooling are correct and
   actionable.
3. Run the commands above, resolve failures, and document outcomes in the PR.

OUTPUT:
A pull request that updates `docs/prompts/codex/implement.md` with passing
checks.
```
