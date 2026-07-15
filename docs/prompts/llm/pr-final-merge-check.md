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
Can every reviewer concern in the PR now be safely considered addressed, and is the PR ready to merge with an accurate merge record?

A concern is addressed only if at least one of these is clearly true:
- The suggested change was implemented correctly.
- The concern is obsolete because later commits removed or changed the relevant code.
- The current code intentionally does not follow the suggestion, and the PR now contains enough justification through code structure, tests, comments, PR discussion, or nearby inline/multiline code comments for a maintainer to confidently consider the underlying concern addressed.
- The comment is purely non-blocking praise, bookkeeping, duplication, or a low-value nit that does not affect merge readiness.

Reviewer-thread handling:
- Continue inspecting every substantive human, bot, and AI reviewer comment.
- Judge the underlying concern against the latest diff, tests, code comments, and discussion.
- An unresolved GitHub thread is not a blocker merely because its UI state remains unresolved.
- If the latest code adequately addresses the concern, treat it as addressed and do not mention or dwell on the unresolved thread.
- If the underlying concern remains valid and requires repository changes, include that work in category 2.
- Never instruct Codex to click, mark, or otherwise resolve a review thread.
- Never include thread-resolution bookkeeping as work in an `@codex` comment.
- Preserve strict handling of genuinely unaddressed reviewer concerns and recurring valid AI-review findings.

Decision rule: respond in exactly one of these three mutually exclusive categories, using this precedence:
1. If code, tests, configuration, generated artifacts, documentation in the repository, or other repository changes are still needed for merge readiness, return category 2. If the PR description also needs work, defer that assessment until repository changes are complete and this merge check is rerun; do not create a hybrid response.
2. Otherwise, if the PR is technically merge-ready but its description is materially inaccurate, incomplete, stale, misleading, or missing information necessary for a responsible merge record, return category 3.
3. Otherwise, return category 1.

Category 1: exact success response
- If the PR is ready to merge and no required description-only correction remains, respond with exactly:
  yes, it can be merged
- Only say `yes, it can be merged` when CI is green, mergeability is acceptable, required approvals are satisfied or no longer needed, all substantive reviewer concerns are addressed, and the PR description is accurate enough for the merge record.
- Do not add caveats, summaries, bullets, or extra commentary when the answer is yes.

Category 2: repository changes needed
- Respond only with a single fenced code block containing a copy/paste-ready GitHub PR comment that begins with `@codex`.
- Use this category for CI, mergeability, reviewer concerns, correctness, regression, security, data-loss, migration, compatibility, maintainability, unrelated scope creep, broad churn, accidental formatting, generated artifacts, secrets, debug code, temporary scaffolding, or stale branch issues that require repository changes.
- Do not ask Codex to edit, rewrite, or update the PR title or description.
- Do not ask Codex to resolve review threads.
- Include only work Codex can perform in the repository.

Do not block merge for low-value nits. Only produce an `@codex` comment for issues that should be fixed or justified before merge.

When recurring AI review comments are present:
- Determine whether the repeated comment is still valid.
- If it is valid, ask Codex to fix the underlying issue directly.
- If the current code is intentional and the AI reviewer is repeatedly asking to revert or change it, ask Codex to add a minimal inline or multiline code comment near the relevant logic explaining the invariant, tradeoff, or rationale, so future reviewers understand why the change should remain.
- Prefer durable explanations in code only when the rationale is not already obvious from names, tests, or surrounding context.
- Do not ask Codex to blindly placate a bot by weakening correct code.

The category 2 `@codex` comment must:
- Be concise but complete enough for a fresh Codex task.
- Start with a brief Scope Lock stating allowed files/areas, do-not-touch areas if known, and that the diff should stay minimal.
- Include a "Reviewer comment resolution" section that maps each remaining substantive reviewer concern to the concrete repository change or durable in-code justification needed for that underlying concern to be addressed.
- For each remaining concern, ask Codex to either implement the reviewer’s suggested change or add enough durable in-repository justification to address the concern and proceed without further changes.
- Name specific reviewers, files, symbols, comments, checks, or quoted snippets when possible.
- Include concrete implementation steps.
- Include verification commands, choosing the narrowest relevant commands first.
- Avoid broad refactors unless they are required for correctness.
- Preserve existing conventions and tests.
- Use triple tildes (`~~~`) instead of triple backticks for any nested code fences inside the comment, because nested triple backticks can break formatting.
- Append `new codex task, not a r/e/v/i/e/w task` as the final line of the generated `@codex` comment, after all other comment text.

Category 3: required PR-description-only correction
- Use this category only when no repository changes remain and the description update is a real merge-readiness requirement rather than optional polish.
- Respond with a short manual instruction followed by exactly one fenced `markdown` block containing the entire replacement PR description. For example:

~~~text
Update the PR description manually to the following:

~~~markdown
<complete replacement PR description>
~~~
~~~

- Generate the complete description from the PR title, linked issue, current description, final diff, tests, and discussion.
- Preserve useful and accurate material from the existing description.
- Correct stale or misleading claims and include the relevant summary, behavior, testing, compatibility, migration, or issue-linking details supported by the PR.
- Do not emit a partial patch, suggested fragments, placeholders, TODOs, or instructions inside the replacement description.
- Keep all replacement-description Markdown inside the fence. Use `~~~` for any nested fences required within the generated description.
- Do not include `@codex` or the Codex sentinel line in category 3.

Before answering, be strict: a confident yes means every substantive reviewer concern is resolved, justified, or safely non-blocking, and any required merge-record description correction is complete.
```

## Upgrade Prompt

```text
Improve the main PR final merge-check prompt above while preserving its purpose and Streamdeck-friendly shape.

Goals:
- Keep the main prompt copy/paste-ready with a `<PR-URL>` placeholder.
- Preserve exactly three mutually exclusive output categories with this deterministic precedence:
  1. Repository changes needed: one fenced code block containing one `@codex` PR comment.
  2. Description-only correction needed: a concise manual instruction plus exactly one fenced `markdown` block containing the complete replacement PR description.
  3. Ready to merge: the exact success output `yes, it can be merged`.
- Preserve the rule that code, tests, configuration, or other repository changes take precedence over description-only corrections; mixed cases must return the `@codex` category first and defer description assessment until the check is rerun.
- Preserve the exact ready-to-merge success output: `yes, it can be merged`
- Preserve the requirement that the LLM only says yes when every substantive reviewer concern is addressed and the PR description is accurate enough for the merge record.
- Preserve the fallback behavior for repository changes: one fenced code block containing one `@codex` PR comment.
- Preserve the requirement that the `@codex` comment concretely maps each remaining reviewer concern to either an implementation change or sufficient durable in-repository justification.
- Preserve the prohibition on generated `@codex` comments requesting PR title/description edits or review-thread resolution.
- Preserve the category 3 requirement to generate the full replacement PR description from the title, linked issue, current description, final diff, tests, and discussion, with no placeholders or partial fragments.
- Preserve the requirement to use triple tildes (`~~~`) for nested code fences inside the `@codex` comment or replacement PR description.
- Preserve the requirement that generated `@codex` comments end with `new codex task, not a r/e/v/i/e/w task`, while ensuring the main prompt itself does not end with that sentinel line.
- Make the prompt better at distinguishing true merge blockers from low-value nits.
- Make the prompt better at handling recurring AI review comments without blindly reverting correct code.
- Make the prompt judge unresolved GitHub review threads by the underlying concern, not by thread UI state alone.
- Keep the wording compact enough to use as a Streamdeck action.

Return:
1. The revised main prompt inside a fenced `text` block.
2. A brief bullet list explaining the improvements.
```
