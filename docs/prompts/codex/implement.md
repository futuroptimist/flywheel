---
title: "Codex Implement Prompt"
slug: "codex-implement"
---

# Codex Implement Prompt

Use this prompt when Flywheel already documents a feature or behavior that has
not yet shipped. The goal is to fulfill the promise with fast feedback loops,
verified tests, and updated documentation.

## When to use it

- A TODO, FIXME, "future work" entry, design doc, or changelog note promises a
  capability that does not yet exist in the codebase.
- Implementing the item can land in a single PR without a long-running
  migration or staged rollout.
- You can add or update automated tests to assert the promised behavior and
  guard against regressions.

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
- Primary source lives in `flywheel/` (Python agents and tooling), `webapp/`
  (Next.js/TypeScript UI), `viewer/` (three.js), and `docs/` (guides and
  prompts). Tests live in `tests/`, `webapp/`, and co-located modules.
- Install dependencies with `pip install -r requirements.txt` and `npm ci`
  before running checks.
- Run the full suite before committing: `pre-commit run --all-files`,
  `pytest -q`, `npm run test:ci`, `python -m flywheel.fit`, and
  `bash scripts/checks.sh`. Match any extra checks mandated by the workflows.
- Use `rg` (ripgrep) to enumerate TODO, FIXME, and design promises across code
  and docs. Prioritize work items that ship immediate value.
- Add targeted tests first, then make them pass. Keep patch coverage high and
  avoid regressions.
- Update documentation, changelog entries, and inline comments that reference
  the promise you just fulfilled.
- Scan staged changes with `git diff --cached | ./scripts/scan-secrets.py`.
- Refresh `docs/prompt-docs-summary.md` via
  `python scripts/update_prompt_docs_summary.py --repos-from \
  dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md` if you add or
  relocate prompt docs.

REQUEST:
1. Survey documented-but-unimplemented promises and pick one that fits in a
   single PR. Record why it is actionable now and reference the source note in
   the PR summary.
2. Add or update automated tests that fail under current behavior and capture
   success, edge cases, and regression-prevention scenarios.
3. Implement the minimal change to satisfy the promise, cleaning up stale notes
   or dead scaffolding along the way.
4. Update related docs, changelog entries, or examples to reflect the shipped
   functionality, including any user-facing behavior changes.
5. Run the commands listed above, address failures, and summarize outcomes in
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
