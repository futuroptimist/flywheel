---
title: 'Repo Glean Prompt'
slug: 'prompt-glean-repos'
---

# Repo Glean Prompt
Type: evergreen

Use this prompt to scan downstream projects listed under “Related Projects” in the README and bubble
useful patterns back into Flywheel.

```text
SYSTEM:
You are an automated researcher for the Flywheel repository. Follow AGENTS.md and README.md.

USER:
1. For each repo in README's Related Projects, gather unique prompting, CI, or CAD patterns.
2. Summarize actionable ideas Flywheel can adopt.
3. Append findings under the "Findings" section of docs/prompt-glean-repos.md.
4. Regenerate docs/prompt-docs-summary.md with:
   python scripts/update_prompt_docs_summary.py --repos-from docs/repo_list.txt --out docs/prompt-docs-summary.md
5. Run pre-commit run --all-files, pytest -q, npm run test:ci, python -m flywheel.fit, and bash scripts/checks.sh.

OUTPUT:
A commit updating the findings and passing all checks.
```

## Findings

### Futuroptimist
- Orientation docs (`llms.txt`, `AGENTS.md`) improve agent alignment.
- Structured metadata files validated by JSON Schema.
- Cross-platform Make targets and high test coverage encourage portable automation.
- Separate runbook and setup instructions keep the README lean.

### token.place
- Hybrid RSA/AES encryption and relay architecture strengthen privacy.
- Docker-based cross-platform scripts streamline local or remote inference.
- Environment-aware logging patterns minimize noise in production.

### DSPACE
- Offline-first quest data patterns show how to maintain structured outages.
- Quest generator integration demonstrates cross-repo automation loops.

### Gabriel
- Risk model outlines security considerations for rapid automation.
- Shared tooling can provide dependency audits and threat modeling.

### f2clipboard
- Macro-style CLI shows how small utilities evolve using Flywheel's patterns.

### Axel
- Repo manager suggests quests across projects, keeping multiple repos in sync.

### Sigma
- Voice-driven ESP32 interface suggests hardware hooks for Flywheel prompts.

### gitshelves
- 3D commit visualizations offer new ways to represent repository history.

### wove
- Textile-focused prompts highlight domain-specific documentation patterns.

### sugarkube
- k3s cluster tooling enables off-grid CI experimentation.
