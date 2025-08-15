---
title: 'Codex Physics Explainer Prompt'
slug: 'codex-physics'
---

# OpenAI Codex Physics Explainer Prompt
Type: evergreen

Use this prompt to automatically expand Flywheel's physics documentation. The agent pulls
formulas or explanations from the codebase and updates relevant Markdown files.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Enrich and clarify the physics documentation.

CONTEXT:
- Focus on improving the explainers in `docs/`.
- Follow [AGENTS.md](../../../AGENTS.md) and [README.md](../../../README.md).
- Ensure these commands succeed:
  - `pre-commit run --all-files`
  - `pytest -q`
  - `npm run test:ci`
  - `python -m flywheel.fit`
  - `bash scripts/checks.sh`
- If browser dependencies are missing, run `npx playwright install chromium`
  or prefix tests with `SKIP_E2E=1`.
- Cross-reference CAD dimensions where helpful.

REQUEST:
1. Inspect physics-related docs for gaps or TODO notes, such as
   [docs/flywheel-construction.md](../../flywheel-construction.md).
2. Add clear explanations or equations where needed.
3. Run the checks listed above.
4. Commit the changes with a concise message and open a pull request.

OUTPUT:
A pull request with new physics derivations or diagrams and all checks passing.
```

This keeps the physics guides fresh and consistent across updates.
