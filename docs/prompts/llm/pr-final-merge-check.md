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
Can the PR be responsibly merged now, considering repository state, tests, reviewer concerns, and the PR description?

A reviewer concern is addressed only if at least one of these is clearly true:
- The suggested change was implemented correctly.
- The concern is obsolete because later commits removed or changed the relevant code.
- The current code intentionally does not follow the suggestion, and the PR now contains enough justification through code structure, tests, comments, PR discussion, or nearby inline/multiline code comments for a maintainer to confidently consider the concern addressed.
- The comment is purely non-blocking praise, bookkeeping, duplication, or a low-value nit that does not affect merge readiness.

Reviewer-thread handling:
- Inspect every substantive human, bot, and AI reviewer comment.
- Judge the underlying concern against the latest diff, tests, code comments, and discussion.
- An unresolved GitHub thread is not a blocker merely because its UI state remains unresolved.
- If the latest code adequately addresses the concern, treat it as addressed and do not mention or dwell on the unresolved thread.
- If the underlying concern remains valid and requires repository changes, include that work in the `@codex` comment.
- Never instruct Codex to click, mark, or otherwise resolve a review thread.
- Never include thread-resolution bookkeeping as work in an `@codex` comment.

Output categories:
1. Exact success response: `yes, it can be merged`
2. One fenced code block containing an actionable `@codex` comment for repository changes needed to make the PR merge-ready.
3. A concise instruction for the user to update the PR description manually, followed by the complete replacement PR description inside one fenced `markdown` code block.

Decision rule: use the three output categories with this deterministic precedence:
1. If code, tests, configuration, or other repository changes are still needed, return category 2. If the PR description also needs work, defer that assessment until the repository changes are complete and this merge check is rerun; do not create a hybrid response.
2. Otherwise, if the PR is technically merge-ready but its description is materially inaccurate, incomplete, stale, misleading, or missing information necessary for a responsible merge record, return category 3.
3. Otherwise, return category 1 exactly and completely:
   yes, it can be merged

Only say `yes, it can be merged` when CI is green, mergeability is acceptable, required approvals are satisfied or no longer needed, every substantive reviewer concern is resolved, justified, or safely non-blocking, and the PR description is adequate for the merge record.
Do not add caveats, summaries, bullets, or extra commentary when the answer is yes.

Treat these as merge blockers requiring category 2 repository-change followup:
- CI is failing, pending, stale, missing, or ambiguous in a way that matters.
- Active requested changes or substantive unaddressed reviewer concerns remain valid against the latest code.
- A reviewer asked a question and the code, tests, comments, or PR discussion do not yet answer it well enough.
- A reviewer suggested a change and the PR neither implemented it nor explains convincingly why the current approach is better.
- The diff has likely correctness, regression, security, data-loss, migration, compatibility, or maintainability risks.
- The PR appears to include unrelated scope creep, broad churn, accidental formatting, generated artifacts, secrets, debug code, or temporary scaffolding.
- The branch is not mergeable or appears out of date in a way that could invalidate tests or approvals.

Do not block merge for low-value nits. Only produce an `@codex` comment for issues that should be fixed or justified in the repository before merge.

When recurring AI review comments are present:
- Determine whether the repeated comment is still valid.
- If it is valid, ask Codex to fix the underlying issue directly.
- If the current code is intentional and the AI reviewer is repeatedly asking to revert or change it, ask Codex to add a minimal inline or multiline code comment near the relevant logic explaining the invariant, tradeoff, or rationale, so future reviewers understand why the change should remain.
- Prefer durable explanations in code only when the rationale is not already obvious from names, tests, or surrounding context.
- Do not ask Codex to blindly placate a bot by weakening correct code.

The category 2 `@codex` comment must:
- Be concise but complete enough for a fresh Codex task.
- Start with a brief Scope Lock stating allowed files/areas, do-not-touch areas if known, and that the diff should stay minimal.
- Include a "Reviewer comment resolution" section that maps each remaining substantive reviewer concern to the concrete repository change or durable in-code justification needed.
- For each remaining concern, ask Codex to either implement the reviewer’s suggested change or add enough durable repository justification to address the concern and proceed without further changes.
- Include only work Codex can perform in the repository.
- Never ask Codex to edit, rewrite, or update the PR title or description.
- Never ask Codex to resolve review threads.
- Name specific reviewers, files, symbols, comments, checks, or quoted snippets when possible.
- Include concrete implementation steps.
- Include verification commands, choosing the narrowest relevant commands first.
- Avoid broad refactors unless they are required for correctness.
- Preserve existing conventions and tests.
- Use triple tildes (`~~~`) instead of triple backticks for any nested code fences inside the comment, because nested triple backticks can break formatting.
- Append `new codex task, not a r/e/v/i/e/w task` as the final line of the generated `@codex` comment, after all other comment text.

The category 3 description-update response must:
- Be used only when no repository changes remain and the description update is a real merge-readiness requirement rather than optional polish.
- Contain a short manual instruction followed by exactly one fenced `markdown` block containing the complete replacement PR description, for example:
  Update the PR description manually to the following:

  ~~~markdown
  <complete replacement PR description>
  ~~~
- Generate the complete description from the PR title, linked issue, current description, final diff, tests, and discussion.
- Preserve useful and accurate material from the existing description.
- Correct stale or misleading claims and include the relevant summary, behavior, testing, compatibility, migration, or issue-linking details supported by the PR.
- Not emit a partial patch, suggested fragments, placeholders, TODOs, or instructions inside the replacement description.
- Keep all replacement-description Markdown inside the fence, using `~~~` for any nested fences required within the generated description.
- Not include `@codex` or the Codex sentinel line.

Before answering, be strict: a confident yes means repository state, reviewer concerns, and the PR description are all merge-ready.
```

## Upgrade Prompt

```text
Improve the main PR final merge-check prompt above while preserving its purpose and Streamdeck-friendly shape.

Goals:
- Keep the main prompt copy/paste-ready with a `<PR-URL>` placeholder.
- Preserve exactly three mutually exclusive output categories with deterministic precedence:
  1. Ready to merge: the exact complete response `yes, it can be merged`.
  2. Repository changes needed: one fenced code block containing one `@codex` PR comment.
  3. Description-only merge blocker: a concise manual instruction plus exactly one fenced `markdown` block containing the complete replacement PR description.
- Preserve the precedence that repository changes always produce the `@codex` category first, even when the PR description also needs work; category 3 description-only output is allowed only after no repository changes remain.
- Preserve the exact ready-to-merge success output: `yes, it can be merged`
- Preserve the requirement that the LLM only says yes when every substantive reviewer comment is resolved, justified, or safely non-blocking and the PR description is adequate.
- Preserve reviewer-thread handling: inspect every substantive comment, judge the underlying concern against the latest PR state, do not block solely on unresolved GitHub thread UI state, and never ask Codex to resolve threads.
- Preserve the requirement that the `@codex` comment concretely maps each remaining substantive concern to a repository change or durable in-code justification.
- Preserve the requirement that generated `@codex` comments include only repository work, never PR title/description edits or thread-resolution bookkeeping.
- Preserve the requirement to use triple tildes (`~~~`) for nested code fences inside the `@codex` comment and inside replacement PR descriptions.
- Preserve the requirement that generated `@codex` comments end with `new codex task, not a r/e/v/i/e/w task`, while ensuring the main prompt itself does not end with that sentinel line.
- Preserve the requirement that category 3 emits a complete replacement PR description inside one fenced `markdown` block, with no placeholders, TODOs, partial patches, or `@codex` sentinel.
- Make the prompt better at distinguishing true merge blockers from low-value nits.
- Make the prompt better at handling recurring AI review comments without blindly reverting correct code.
- Make the prompt better at producing followups that let maintainers confidently address every remaining substantive reviewer concern.
- Keep the wording compact enough to use as a Streamdeck action.

Return:
1. The revised main prompt inside a fenced `text` block.
2. A brief bullet list explaining the improvements.
```
