---
title: 'PR Final Merge-Readiness Check Prompt'
slug: 'pr-final-merge-check'
conversational: true
---

# PR Final Merge-Readiness Check Prompt
Type: evergreen

## Main Prompt

```text
Is <PR-URL> ready to merge?

Assume I am asking for a final merge-readiness check after reviewer comments appear resolved and CI appears green, but verify that assumption from the PR itself before answering.

Review the PR using the available GitHub context:
- PR title, description, linked issues, branch/base status, mergeability, and latest commit.
- The diff and any files likely affected by the change.
- Required checks, CI status, pending checks, failed checks, skipped checks that look relevant, and stale results.
- Review state, unresolved review threads, requested changes, bot comments, and recent human comments.
- Every reviewer comment that appears substantive, whether from a human reviewer, Copilot, Greptile, Codex, another AI reviewer, or a CI/review bot.
- Any recurring AI review comments, especially from tools such as Greptile, that appear to repeat after prior fixes or after Codex changes.

Core question:
Can every reviewer concern in the PR now be safely considered addressed?

A concern is addressed only if at least one of these is clearly true:
- The suggested change was implemented correctly.
- The concern is obsolete because later commits removed or changed the relevant code.
- The current code intentionally does not follow the suggestion, and the PR now contains enough justification through code structure, tests, comments, PR discussion, or nearby inline/multiline code comments for a maintainer to confidently mark the thread resolved.
- The comment is purely non-blocking praise, bookkeeping, duplication, or a low-value nit that does not affect merge readiness.

Decision rule:
- If the PR is ready to merge, respond with exactly:
  yes, it can be merged
- Only say `yes, it can be merged` when CI is green, mergeability is acceptable, required approvals are satisfied or no longer needed, and every unresolved or substantive reviewer comment can safely be marked Resolved without further code changes, discussion, or justification.
- Do not add caveats, summaries, bullets, or extra commentary when the answer is yes.
- If the PR is not ready to merge, respond only with a single fenced code block containing a copy/paste-ready GitHub PR comment that begins with `@codex`.

Treat these as merge blockers:
- CI is failing, pending, stale, missing, or ambiguous in a way that matters.
- There are unresolved review threads, active requested changes, or substantive unaddressed reviewer concerns.
- Any unresolved thread cannot yet be safely marked Resolved.
- A reviewer asked a question and the code, tests, comments, or PR discussion do not yet answer it well enough.
- A reviewer suggested a change and the PR neither implemented it nor explains convincingly why the current approach is better.
- The diff has likely correctness, regression, security, data-loss, migration, compatibility, or maintainability risks.
- The PR appears to include unrelated scope creep, broad churn, accidental formatting, generated artifacts, secrets, debug code, or temporary scaffolding.
- The branch is not mergeable or appears out of date in a way that could invalidate tests or approvals.

Do not block merge for low-value nits. Only produce an `@codex` comment for issues that should be fixed or justified before merge.

When recurring AI review comments are present:
- Determine whether the repeated comment is still valid.
- If it is valid, ask Codex to fix the underlying issue directly.
- If the current code is intentional and the AI reviewer is repeatedly asking to revert or change it, ask Codex to add a minimal inline or multiline code comment near the relevant logic explaining the invariant, tradeoff, or rationale, so future reviewers understand why the change should remain.
- Prefer durable explanations in code only when the rationale is not already obvious from names, tests, or surrounding context.
- Do not ask Codex to blindly placate a bot by weakening correct code.

The `@codex` comment must:
- Be concise but complete enough for a fresh Codex task.
- Start with a brief Scope Lock stating allowed files/areas, do-not-touch areas if known, and that the diff should stay minimal.
- Include a "Reviewer comment resolution" section that lists each remaining unresolved or substantive reviewer concern and says exactly what must happen for that concern to be safely marked Resolved.
- For each remaining concern, ask Codex to either implement the reviewer’s suggested change or add enough justification to address the concern and proceed without further changes.
- Name specific reviewers, files, symbols, comments, threads, checks, or quoted snippets when possible.
- Include concrete implementation steps.
- Include verification commands, choosing the narrowest relevant commands first.
- Avoid broad refactors unless they are required for correctness.
- Preserve existing conventions and tests.
- Use triple tildes (`~~~`) instead of triple backticks for any nested code fences inside the comment, because nested triple backticks can break formatting.
- Append `new codex task, not a r/e/v/i/e/w task` as the final line of the generated `@codex` comment, after all other comment text.

Before answering, be strict: a confident yes means every substantive reviewer concern is resolved, justified, or safely non-blocking.
```

## Upgrade Prompt

```text
Improve the main PR final merge-check prompt above while preserving its purpose and Streamdeck-friendly shape.

Goals:
- Keep the main prompt copy/paste-ready with a `<PR-URL>` placeholder.
- Preserve the exact ready-to-merge success output: `yes, it can be merged`
- Preserve the requirement that the LLM only says yes when every unresolved or substantive reviewer comment can safely be marked Resolved.
- Preserve the fallback behavior: one fenced code block containing one `@codex` PR comment.
- Preserve the requirement that the `@codex` comment concretely maps each remaining reviewer concern to either an implementation change or sufficient justification.
- Preserve the requirement to use triple tildes (`~~~`) for nested code fences inside the `@codex` comment.
- Preserve the requirement that generated `@codex` comments end with `new codex task, not a r/e/v/i/e/w task`, while ensuring the main prompt itself does not end with that sentinel line.
- Make the prompt better at distinguishing true merge blockers from low-value nits.
- Make the prompt better at handling recurring AI review comments without blindly reverting correct code.
- Make the prompt better at producing followups that let maintainers confidently resolve every remaining review thread.
- Keep the wording compact enough to use as a Streamdeck action.

Return:
1. The revised main prompt inside a fenced `text` block.
2. A brief bullet list explaining the improvements.
```
