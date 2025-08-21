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
1. For each repo listed under Related Projects in the README,
   gather unique prompting, CI, or CAD patterns.
2. Summarize actionable ideas Flywheel can adopt.
3. Append findings under the "Findings" section of docs/prompt-glean-repos.md.
4. Regenerate docs/prompt-docs-summary.md with:
   python scripts/update_prompt_docs_summary.py --repos-from docs/repo_list.txt --out docs/prompt-docs-summary.md
5. Run pre-commit run --all-files, pytest -q, npm run test:ci, python -m flywheel.fit, and bash scripts/checks.sh.

OUTPUT:
A commit updating the findings and passing all checks.
```

## Action Items

- [ ] Futuroptimist
  - [ ] Incorporate orientation docs (`llms.txt`, `AGENTS.md`) to improve agent alignment.
  - [ ] Validate structured metadata files using JSON Schema.
  - [ ] Provide cross-platform Make targets and maintain high test coverage.
  - [ ] Move runbook and setup instructions out of the README to keep it lean.

- [ ] token.place
  - [ ] Explore hybrid RSA/AES encryption and relay architecture for stronger privacy.
  - [ ] Offer Docker-based cross-platform scripts for local or remote inference.
  - [x] Implement environment-aware logging helpers to minimize production noise. 💯

- [ ] DSPACE
  - [ ] Adopt offline-first quest data patterns to maintain structured outages.
  - [ ] Integrate quest generator loops for cross-repo automation.

- [ ] Gabriel
  - [ ] Incorporate a risk model outlining security considerations for rapid automation.
  - [ ] Share tooling for dependency audits and threat modeling.

- [ ] f2clipboard
  - [ ] Provide macro-style CLI examples showing how small utilities can grow using Flywheel patterns.

- [ ] Axel
  - [ ] Implement repo manager hooks to suggest quests across projects and keep repos in sync.

- [ ] Sigma
  - [ ] Add voice-driven ESP32 interfaces as hardware hooks for Flywheel prompts.

- [ ] gitshelves
  - [ ] Investigate 3D commit visualizations to represent repository history.

- [ ] wove
  - [ ] Incorporate textile-focused prompts to highlight domain-specific documentation patterns.

- [ ] sugarkube
  - [ ] Experiment with k3s cluster tooling for off-grid CI.

## Random Implementation Prompt

```text
SYSTEM:
You are a Flywheel contributor ensuring continuous improvement.

USER:
1. Randomly select an unchecked item from the Action Items list above.
2. Implement the change in the repository.
3. Mark its checkbox as completed with a "💯".
4. Regenerate docs/prompt-docs-summary.md with:
   python scripts/update_prompt_docs_summary.py --repos-from docs/repo_list.txt --out docs/prompt-docs-summary.md
5. Run pre-commit run --all-files, pytest -q, npm run test:ci, python -m flywheel.fit, and bash scripts/checks.sh.
6. Commit your work.

OUTPUT:
A commit implementing the chosen action item and marking it complete with a 💯.
```
