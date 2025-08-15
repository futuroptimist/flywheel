# Prompt Doc Filtering

Guidance for future LLMs to keep `prompt-docs-summary.md` focused and useful.

## Goals

- Only link to sections that contain a fenced code block with an LLM prompt.
- Surface major one-click prompts and outstanding feature requests.
- Remove entries once the referenced work is complete.

## Workflow

1. Crawl repositories for Markdown files mentioning prompts.
2. For each candidate section:
   - Confirm a code block exists and represents an LLM prompt.
   - Classify it as `evergreen` or `one-off`.
   - Skip sections lacking code blocks or unrelated content.
3. Update `prompt-docs-summary.md` with vetted entries only.
4. Run the full suite of checks:
   - `pre-commit run --all-files`
   - `pytest -q`
   - `npm run lint`
   - `npm run test:ci`
   - `python -m flywheel.fit`
   - `bash scripts/checks.sh`
5. Commit with a descriptive message and reference any relevant issues.
6. Repeat as new prompts are added across repositories.

