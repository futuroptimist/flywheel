---
title: 'Codex Physics Explainer Prompt'
slug: 'codex-physics'
---

# OpenAI Codex Physics Explainer Prompt
Type: evergreen

Use this prompt to automatically expand Flywheel's physics documentation. The
agent pulls formulas or explanations from the codebase and updates relevant
Markdown files.

```
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Enrich and clarify the physics documentation.

CONTEXT:
- Focus on improving the explainers in `docs/*`.
- Follow [AGENTS.md](../../../AGENTS.md) and [README.md](../../../README.md)
  for style and testing requirements.
- Cross-reference CAD dimensions where helpful.
- If browser dependencies are missing, run `npx playwright install chromium` or
  set `SKIP_E2E=1`.

REQUEST:
1. Inspect [docs/flywheel-physics.md](../../flywheel-physics.md) for gaps or TODO notes.
2. Add clear explanations or equations where needed.
3. Run these commands before committing:
   - `pre-commit run --all-files`
   - `pytest -q`
   - `npm run test:ci`
   - `python -m flywheel.fit`
   - `bash scripts/checks.sh`

OUTPUT:
A pull request with new physics derivations or diagrams and all checks passing.
```

This keeps the physics guides fresh and consistent across updates.
