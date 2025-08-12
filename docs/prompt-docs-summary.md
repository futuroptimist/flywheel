# Prompt Docs Summary

This index is auto-generated with [scripts/update_prompt_docs_summary.py](../scripts/update_prompt_docs_summary.py) using RepoCrawler to discover prompt documents across repositories.

## Template Prompts (futuroptimist/flywheel)

### [Codex CAD Prompt](https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-codex-cad.md)

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

### [Codex CI-Failure Fix Prompt](https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-codex-ci-fix.md)

```
SYSTEM:
You are an automated contributor for the target repository.

PURPOSE:
Diagnose a failed GitHub Actions run and produce a fix.

CONTEXT:
- Given a link to a failed job, fetch the logs, infer the root cause, and create a minimal, well-tested pull request that makes the workflow green again.
- Constraints:
  * Do **not** break existing functionality.
  * Follow the repository’s style guidelines and commit-lint rules.
  * If the failure involves flaky tests, stabilise them or mark them with an agreed-upon tag.
  * Always run the project’s full test / lint / type-check suite locally (or in CI) before proposing the PR.
  * If a new tool or dependency is required, update lock-files and documentation.
  * Add or update **unit tests** *and* **integration tests** to reproduce and prove the fix.
  * Provide a concise changelog entry.

REQUEST:
1. Read the failure logs and locate the first real error.
2. Explain (in the pull-request body) *why* the failure occurred.
3. Commit the necessary code, configuration, or documentation changes.
4. Push to a branch named `codex/ci-fix/<short-description>`.
5. Open a pull request that – once merged – makes the default branch CI-green.
6. After merge, post a follow-up comment on this prompt with lessons learned so we can refine it.

OUTPUT:
A GitHub pull request URL. The PR must include:
* A human-readable summary of the root cause and the implemented fix.
* Evidence that **all** checks are now passing (`✔️`).
* Links to any new or updated tests.
Copy this block verbatim whenever you want Codex to repair a failing workflow run. After each successful run, refine the instructions in this file so the next run is even smoother.
After opening the pull request, create a new postmortem file under `docs/pms/` named `YYYY-MM-DD-short-title.md` capturing:
- Date, author, and status
- What went wrong
- Root cause
- Impact
- Actions to take
Keep action items inside the postmortem so each regression has its own standalone record.
```

### [Codex Prompt Cleanup](https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-codex-cleanup.md)

```
SYSTEM: You are an automated contributor for the Flywheel repository.

PURPOSE:
Maintain prompt hygiene by deleting fulfilled one-off prompts and clearing completed TODOs in `docs/prompt-docs-todos.md`.

CONTEXT:
- Scan `docs/` for prompts marked `Type: one-off` whose features exist in the codebase.
- Delete those prompt sections or files.
- Remove matching rows from `docs/prompt-docs-todos.md`.
- Regenerate `docs/prompt-docs-summary.md` using `python scripts/update_prompt_docs_summary.py`.
- Follow `AGENTS.md` for testing requirements.

REQUEST:
1. Identify an obsolete prompt or external TODO entry.
2. Remove it and update references.
3. Run all required checks before committing.

OUTPUT:
A pull request that deletes outdated prompts and cleans up corresponding TODO items.
```

### [Codex Physics Explainer Prompt](https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-codex-physics.md)

```
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Enrich and clarify the physics documentation.

CONTEXT:
- Focus on improving the explainers in `docs/*`.
- Follow AGENTS.md for style and testing requirements.
- Cross-reference CAD dimensions where helpful.

REQUEST:
1. Inspect `docs/flywheel-physics.md` for gaps or TODO notes.
2. Add clear explanations or equations where needed.
3. Run `bash scripts/checks.sh` before committing.

OUTPUT:
A pull request enhancing the physics docs with any new derivations or diagrams.
```

### [Codex Prompt Propagation Prompt](https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-codex-propagate.md)

```
SYSTEM:
You are an automated contributor for the provided repositories.

PURPOSE:
Ensure each repository has a canonical `docs/prompts-codex.md` file so future agents have guidance.

CONTEXT:
- For each repo in the list, check for existing `docs/prompts-*.md` files.
- If none exist, create `docs/prompts-codex.md` based on the version in `futuroptimist/flywheel`.
- Follow the repository's `AGENTS.md`, style guides, and commit conventions.
- Run `npm run lint` (or equivalent) and the primary test suite before committing.

REQUEST:
1. Clone the repository and add the prompt doc.
2. Include a short README update linking to the new doc.
3. Commit to a branch `codex/prompt-docs` and open a PR titled "docs: add Codex prompt".
4. Return the pull request URL.

OUTPUT:
A list of pull request links, one per repository.
```

### [Codex Spellcheck Prompt](https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-codex-spellcheck.md)

```
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Keep Markdown documentation free of spelling errors.

CONTEXT:
- Run `pre-commit run codespell --files $(git ls-files '*.md')` to spell-check Markdown.
- Add unknown but legitimate words to [dict/allow.txt](../dict/allow.txt).
- Follow [AGENTS.md](../AGENTS.md) and [README.md](../README.md); ensure these commands succeed:
  - `pre-commit run --all-files`
  - `pytest -q`
  - `npm run test:ci`
  - `python -m flywheel.fit`
  - `bash scripts/checks.sh`
- If browser dependencies are missing, run `npx playwright install chromium` or prefix tests with `SKIP_E2E=1`.

REQUEST:
1. Run the spellcheck command and inspect the results.
2. Correct misspellings or update `dict/allow.txt` as needed.
3. Re-run the spellcheck until it reports no errors.
4. Run all checks listed above.
5. Commit the changes with a concise message and open a pull request.

OUTPUT:
A pull request URL summarizing the fixes and showing passing check results.
```

### [Flywheel Codex Prompt](https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-codex.md)

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

## [futuroptimist/axel](https://github.com/futuroptimist/axel)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/axel's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [code.md](https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/code.md) | unknown |
| [critique.md](https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/critique.md) | unknown |
| [plan.md](https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/plan.md) | unknown |
| [OpenAI Codex CI-Failure Fix Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex-ci-fix.md#openai-codex-ci-failure-fix-prompt) | unknown |
| [Codex Spellcheck Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex-spellcheck.md#codex-spellcheck-prompt) | unknown |
| [Automation Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#automation-prompt) | unknown |
| [Implementation Prompts](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [1. Fetch repositories from the GitHub API](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#1-fetch-repositories-from-the-github-api) | unknown |
| [2. Update roadmap status](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#2-update-roadmap-status) | unknown |
| [How to Choose a Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#how-to-choose-a-prompt) | unknown |
| [Upgrade Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#upgrade-prompt) | unknown |

## [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/gabriel's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [Codex Automation Prompt](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |
| [Implementation prompts](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [1 Track a new related repository](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#1-track-a-new-related-repository) | unknown |
| [2 Expand service improvement checklists](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#2-expand-service-improvement-checklists) | unknown |
| [How to choose a prompt](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#how-to-choose-a-prompt) | unknown |
| [Prompt Templates](https://github.com/futuroptimist/gabriel/blob/main/prompts/README.md#prompt-templates) | unknown |
| [Prompt Catalog](https://github.com/futuroptimist/gabriel/blob/main/prompts/README.md#prompt-catalog) | unknown |
| [Generate Improvement Checklist Items](https://github.com/futuroptimist/gabriel/blob/main/prompts/generate-improvements.md#generate-improvement-checklist-items) | unknown |
| [Scan for Bright and Dark Patterns](https://github.com/futuroptimist/gabriel/blob/main/prompts/scan-bright-dark-patterns.md#scan-for-bright-and-dark-patterns) | unknown |
| [Update Flywheel Risk Model](https://github.com/futuroptimist/gabriel/blob/main/prompts/update-risk-model.md#update-flywheel-risk-model) | unknown |

## [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/futuroptimist's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [Codex Spellcheck Prompt](https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts-codex-spellcheck.md#codex-spellcheck-prompt) | unknown |
| [Codex Video Script Prompt](https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts-codex-video-script.md#codex-video-script-prompt) | unknown |
| [Codex Automation Prompt](https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |

## [futuroptimist/token.place](https://github.com/futuroptimist/token.place)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/token.place's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [Codex CI-Failure Fix Prompt](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt) | unknown |
| [Codex Security Review Prompt](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex-security.md#codex-security-review-prompt) | unknown |
| [token.place Codex Prompt](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#tokenplace-codex-prompt) | unknown |
| [Implementation prompts](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [1 Document environment variables in README](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#1-document-environment-variables-in-readme) | unknown |
| [2 Add API rate limit test](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#2-add-api-rate-limit-test) | unknown |

## [democratizedspace/dspace](https://github.com/democratizedspace/dspace)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align democratizedspace/dspace's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [OpenAI Codex CI-Failure Fix Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex-ci-fix.md#openai-codex-ci-failure-fix-prompt) | unknown |
| [Writing great Codex prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#writing-great-codex-prompts-for-the-dspace-repo) | unknown |
| [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#1-quick-start-web-vs-cli) | unknown |
| [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#2-prompt-ingredients) | unknown |
| [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#3-reusable-template) | unknown |
| [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#implementation-prompt) | unknown |
| [Upgrade Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#upgrade-prompt) | unknown |
| [Writing great item prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#writing-great-item-prompts-for-the-dspace-repo) | unknown |
| [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#1-quick-start-web-vs-cli) | unknown |
| [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#2-prompt-ingredients) | unknown |
| [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#3-reusable-template) | unknown |
| [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#implementation-prompt) | unknown |
| [Upgrade prompt for existing items](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#upgrade-prompt-for-existing-items) | unknown |
| [Writing great process prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#writing-great-process-prompts-for-the-dspace-repo) | unknown |
| [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#1-quick-start-web-vs-cli) | unknown |
| [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#2-prompt-ingredients) | unknown |
| [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#3-reusable-template) | unknown |
| [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#implementation-prompt) | unknown |
| [Upgrade prompt for existing processes](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#upgrade-prompt-for-existing-processes) | unknown |
| [Writing great quest prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#writing-great-quest-prompts-for-the-dspace-repo) | unknown |
| [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#1-quick-start-web-vs-cli) | unknown |
| [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#2-prompt-ingredients) | unknown |
| [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#3-reusable-template) | unknown |
| [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#implementation-prompt) | unknown |
| [Upgrade prompt for new quests](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#upgrade-prompt-for-new-quests) | unknown |

## [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/f2clipboard's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [Codex prompts for the *f2clipboard* repo](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#codex-prompts-for-the-f2clipboard-repo) | unknown |
| [Baseline automation prompt](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#baseline-automation-prompt) | unknown |
| [Roadmap implementation prompt](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#roadmap-implementation-prompt) | unknown |
| [Task-specific prompts](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#task-specific-prompts) | unknown |
| [1 Size-gate logs and summarise via LLM](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#1-size-gate-logs-and-summarise-via-llm) | unknown |
| [2 Emit Markdown to stdout and clipboard](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#2-emit-markdown-to-stdout-and-clipboard) | unknown |

## [futuroptimist/sigma](https://github.com/futuroptimist/sigma)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/sigma's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [Codex CAD Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-cad.md#codex-cad-prompt) | unknown |
| [Codex CI-Failure Fix Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt) | unknown |
| [Codex Spellcheck Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-spellcheck.md#codex-spellcheck-prompt) | unknown |
| [Codex Automation Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |

## [futuroptimist/wove](https://github.com/futuroptimist/wove)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/wove's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [Codex CAD Prompt](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex-cad.md#codex-cad-prompt) | unknown |
| [Codex Automation Prompt](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |
| [Implementation prompts](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [1 Add a Gauge Swatch section](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#1-add-a-gauge-swatch-section) | unknown |
| [2 Document `checks.sh` in the README](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#2-document-checkssh-in-the-readme) | unknown |
| [3 Add a Crochet Glossary](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#3-add-a-crochet-glossary) | unknown |

## [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube)

```
Use https://github.com/futuroptimist/flywheel prompt docs as templates. Align futuroptimist/sugarkube's prompts in docs/prompts-*.md.
```

| Prompt | Type |
| --- | --- |
| [OpenAI Codex CAD Prompt](https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-cad.md#openai-codex-cad-prompt) | unknown |
| [Codex Documentation Prompt](https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-docs.md#codex-documentation-prompt) | unknown |
| [Codex Automation Prompt](https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |

## Untriaged Prompt Docs

| Repo | Prompt | Type |
| --- | --- | --- |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [code.md](https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/code.md) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [critique.md](https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/critique.md) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [plan.md](https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/plan.md) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [OpenAI Codex CI-Failure Fix Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex-ci-fix.md#openai-codex-ci-failure-fix-prompt) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [Codex Spellcheck Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex-spellcheck.md#codex-spellcheck-prompt) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [Automation Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#automation-prompt) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [Implementation Prompts](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [1. Fetch repositories from the GitHub API](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#1-fetch-repositories-from-the-github-api) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [2. Update roadmap status](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#2-update-roadmap-status) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [How to Choose a Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#how-to-choose-a-prompt) | unknown |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | [Upgrade Prompt](https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md#upgrade-prompt) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [Codex Automation Prompt](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [Implementation prompts](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [1 Track a new related repository](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#1-track-a-new-related-repository) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [2 Expand service improvement checklists](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#2-expand-service-improvement-checklists) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [How to choose a prompt](https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md#how-to-choose-a-prompt) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [Prompt Templates](https://github.com/futuroptimist/gabriel/blob/main/prompts/README.md#prompt-templates) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [Prompt Catalog](https://github.com/futuroptimist/gabriel/blob/main/prompts/README.md#prompt-catalog) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [Generate Improvement Checklist Items](https://github.com/futuroptimist/gabriel/blob/main/prompts/generate-improvements.md#generate-improvement-checklist-items) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [Scan for Bright and Dark Patterns](https://github.com/futuroptimist/gabriel/blob/main/prompts/scan-bright-dark-patterns.md#scan-for-bright-and-dark-patterns) | unknown |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | [Update Flywheel Risk Model](https://github.com/futuroptimist/gabriel/blob/main/prompts/update-risk-model.md#update-flywheel-risk-model) | unknown |
| [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) | [Codex Spellcheck Prompt](https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts-codex-spellcheck.md#codex-spellcheck-prompt) | unknown |
| [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) | [Codex Video Script Prompt](https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts-codex-video-script.md#codex-video-script-prompt) | unknown |
| [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) | [Codex Automation Prompt](https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | [Codex CI-Failure Fix Prompt](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt) | unknown |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | [Codex Security Review Prompt](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex-security.md#codex-security-review-prompt) | unknown |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | [token.place Codex Prompt](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#tokenplace-codex-prompt) | unknown |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | [Implementation prompts](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | [1 Document environment variables in README](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#1-document-environment-variables-in-readme) | unknown |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | [2 Add API rate limit test](https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md#2-add-api-rate-limit-test) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [OpenAI Codex CI-Failure Fix Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex-ci-fix.md#openai-codex-ci-failure-fix-prompt) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Writing great Codex prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#writing-great-codex-prompts-for-the-dspace-repo) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#1-quick-start-web-vs-cli) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#2-prompt-ingredients) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#3-reusable-template) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#implementation-prompt) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Upgrade Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-codex.md#upgrade-prompt) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Writing great item prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#writing-great-item-prompts-for-the-dspace-repo) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#1-quick-start-web-vs-cli) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#2-prompt-ingredients) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#3-reusable-template) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#implementation-prompt) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Upgrade prompt for existing items](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-items.md#upgrade-prompt-for-existing-items) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Writing great process prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#writing-great-process-prompts-for-the-dspace-repo) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#1-quick-start-web-vs-cli) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#2-prompt-ingredients) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#3-reusable-template) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#implementation-prompt) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Upgrade prompt for existing processes](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-processes.md#upgrade-prompt-for-existing-processes) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Writing great quest prompts for the _dspace_ repo](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#writing-great-quest-prompts-for-the-dspace-repo) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [1 Quick start (Web vs CLI)](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#1-quick-start-web-vs-cli) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [2 Prompt ingredients](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#2-prompt-ingredients) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [3 Reusable template](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#3-reusable-template) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Implementation Prompt](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#implementation-prompt) | unknown |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | [Upgrade prompt for new quests](https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/md/prompts-quests.md#upgrade-prompt-for-new-quests) | unknown |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | [Codex prompts for the *f2clipboard* repo](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#codex-prompts-for-the-f2clipboard-repo) | unknown |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | [Baseline automation prompt](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#baseline-automation-prompt) | unknown |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | [Roadmap implementation prompt](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#roadmap-implementation-prompt) | unknown |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | [Task-specific prompts](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#task-specific-prompts) | unknown |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | [1 Size-gate logs and summarise via LLM](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#1-size-gate-logs-and-summarise-via-llm) | unknown |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | [2 Emit Markdown to stdout and clipboard](https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md#2-emit-markdown-to-stdout-and-clipboard) | unknown |
| [futuroptimist/sigma](https://github.com/futuroptimist/sigma) | [Codex CAD Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-cad.md#codex-cad-prompt) | unknown |
| [futuroptimist/sigma](https://github.com/futuroptimist/sigma) | [Codex CI-Failure Fix Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt) | unknown |
| [futuroptimist/sigma](https://github.com/futuroptimist/sigma) | [Codex Spellcheck Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-spellcheck.md#codex-spellcheck-prompt) | unknown |
| [futuroptimist/sigma](https://github.com/futuroptimist/sigma) | [Codex Automation Prompt](https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | [Codex CAD Prompt](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex-cad.md#codex-cad-prompt) | unknown |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | [Codex Automation Prompt](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | [Implementation prompts](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#implementation-prompts) | unknown |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | [1 Add a Gauge Swatch section](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#1-add-a-gauge-swatch-section) | unknown |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | [2 Document `checks.sh` in the README](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#2-document-checkssh-in-the-readme) | unknown |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | [3 Add a Crochet Glossary](https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md#3-add-a-crochet-glossary) | unknown |
| [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube) | [OpenAI Codex CAD Prompt](https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-cad.md#openai-codex-cad-prompt) | unknown |
| [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube) | [Codex Documentation Prompt](https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-docs.md#codex-documentation-prompt) | unknown |
| [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube) | [Codex Automation Prompt](https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex.md#codex-automation-prompt) | unknown |

## TODO Prompts for Other Repos

| Repo | Suggested Prompt | Type | Notes |
|------|-----------------|------|-------|
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | Add Codex security review prompt | evergreen | TODO: provide security checklist similar to Flywheel's |

_Updated automatically: 2025-08-12_
