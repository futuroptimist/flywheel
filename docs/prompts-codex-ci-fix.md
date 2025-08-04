---
title: 'Codex CI-Failure Fix Prompt'
slug:  'prompts-codex-ci-fix'
---

# OpenAI Codex CI-Failure Fix Prompt

Use this prompt when a GitHub Actions run in the Flywheel repository fails and you want Codex to diagnose and repair the problem automatically.

**Human set-up steps (do these *before* switching ChatGPT into "Code" mode):**

1. Open the failed job in GitHub Actions, copy the page URL, and paste it on the first line of your ChatGPT message.
2. Press <kbd>Enter</kbd> twice so that exactly two blank lines follow the URL.
3. Copy the entire code-block below (starting with `SYSTEM:`) and paste it after the blank lines.
4. Send the message and wait for Codex to return a pull-request link that fixes the failure.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository. Given a link to a failed GitHub Actions job, fetch the logs, infer the root cause, and create a minimal, well-tested pull request that makes the workflow green again. Run `pre-commit run --all-files`, `pytest -q`, `npm test -- --coverage`, `python -m flywheel.fit`, and `bash scripts/checks.sh` before committing.

USER:
1. Read the failure logs and locate the first real error.
2. Explain in the pull-request body why the failure occurred.
3. Commit the necessary code, configuration, or documentation changes.
4. Push to a branch named `codex/ci-fix/<short-description>` and open a pull request.

OUTPUT:
A GitHub pull request URL that summarizes the root cause, links to any new or updated tests, and shows all checks passing.
```

Copy this block whenever you want Codex to repair a failing workflow in Flywheel.
