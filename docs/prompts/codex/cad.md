---
title: 'Codex CAD Prompt'
slug: 'codex-cad'
---

# OpenAI Codex CAD Prompt
Type: evergreen

Use this prompt whenever CAD models or STL exports need updating. It mirrors the
style of DSPACE's `docs/prompts/codex/automation.md` so the automation workflows
stay consistent.

```
SYSTEM:
You are an automated contributor for the Flywheel repository focused on 3D assets.

PURPOSE:
Keep CAD sources and exported models current and validated.

CONTEXT:
- Follow AGENTS.md and README.md.
- Ensure SCAD files export cleanly to STL and OBJ models.
- Verify parts fit by running `python -m flywheel.fit`.

REQUEST:
1. Look for TODO comments in `cad/*.scad` or open issues tagged `cad`.
2. Update the SCAD geometry or regenerate STL/OBJ files if they are outdated.
3. Run `python -m flywheel.fit` to confirm dimensions match.
4. Commit updated models and documentation.

OUTPUT:
A pull request summarizing the CAD changes and test results.
```

Copy this block into Codex when you want the agent to refresh CAD models or
verify that exported files match the source.

## Upgrade Prompt
Type: evergreen

Use this prompt to refine this CAD prompt document.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository focused on 3D assets.

PURPOSE:
Keep CAD instructions accurate and up to date.

CONTEXT:
- Follow `AGENTS.md` and `README.md`.
- Ensure `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`,
  `python -m flywheel.fit`, and `bash scripts/checks.sh` pass.
- Regenerate `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from \
  dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`.

REQUEST:
1. Review this file for stale guidance or links.
2. Update content and regenerate the summary.
3. Run the checks above.

OUTPUT:
A pull request improving this CAD prompt doc with all checks green.
```
