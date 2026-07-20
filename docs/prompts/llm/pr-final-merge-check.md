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
Can every reviewer concern in the PR now be safely considered addressed, and is the PR record accurate enough for a responsible merge?

A concern is addressed only if at least one of these is clearly true:
- The suggested change was implemented correctly.
- The concern is obsolete because later commits removed or changed the relevant code.
- The current code intentionally does not follow the suggestion, and the PR now contains enough justification through code structure, tests, comments, PR discussion, or nearby inline/multiline code comments for a maintainer to confidently treat the concern as addressed.
- The comment is purely non-blocking praise, bookkeeping, duplication, or a low-value nit that does not affect merge readiness.

Decision rule:
Respond with exactly one of these three mutually exclusive categories, evaluated in this order:
- Highest priority: if code, tests, configuration, generated artifacts, documentation in the repository, or any other repository changes are still needed for merge readiness, return category 2. If a material PR-description correction is also already known, track it as the final tally item instead of generating the replacement description yet.
- Next: otherwise, if the PR is technically merge-ready but its description is materially inaccurate, incomplete, stale, misleading, or missing information necessary for a responsible merge record, return category 3.
- Otherwise: return category 1.

Category 1: exact success response
- If the PR is ready to merge and the PR description is merge-ready, respond with exactly:
  yes, it can be merged
- Only say `yes, it can be merged` when CI is green, mergeability is acceptable, required approvals are satisfied or no longer needed, every substantive reviewer comment is addressed or safely non-blocking, and the PR description does not require a material correction.
- Do not add caveats, summaries, bullets, or extra commentary when the answer is yes.

Category 2: repository changes needed
- If the PR is not ready to merge because repository changes are still needed, respond with exactly these two elements, in this order, and no other prose before, between, or after them:
  1. One copy/paste-ready outer three-backtick `text` fenced code block containing a GitHub PR comment that begins with `@codex`.
  2. A clearly labeled `Merge-readiness tally:` outside the fence.
- Include only repository work Codex can perform in the `@codex` comment.
- Never ask Codex to edit, rewrite, or update the PR title or description.
- Never ask Codex to click, mark, or otherwise resolve a review thread.
- Never include thread-resolution bookkeeping as work in an `@codex` comment.
- Keep the generated `@codex` comment fully self-contained; it must not mention the tally, checkbox states, item numbers, or phrases such as "the item above."

Category 3: PR description-only correction needed
- Use this category only when no repository changes remain and the description update is a real merge-readiness requirement rather than optional polish.
- Respond with a concise manual instruction followed by exactly one fenced `markdown` block containing the entire replacement PR description, for example:

Update the PR description manually to the following:

~~~~markdown
<complete replacement PR description>
~~~~

- Generate the complete description from the PR title, linked issue, current description, final diff, tests, and discussion.
- Preserve useful and accurate material from the existing description.
- Correct stale or misleading claims and include the relevant summary, behavior, testing, compatibility, migration, or issue-linking details supported by the PR.
- Do not emit a partial patch, suggested fragments, placeholders, TODOs, or instructions inside the replacement description.
- Keep all replacement-description Markdown inside the outer fence. Use an outer fence longer than any nested fence, and use `~~~` for any nested fences required within the generated description.
- Do not include `@codex` or the Codex sentinel line in category 3.

Treat these as merge blockers that require category 2 when they need repository changes:
- CI is failing, pending, stale, missing, or ambiguous in a way that matters.
- There are active requested changes or substantive unaddressed reviewer concerns.
- A reviewer asked a question and the code, tests, comments, or PR discussion do not yet answer it well enough.
- A reviewer suggested a change and the PR neither implemented it nor explains convincingly why the current approach is better.
- The diff has likely correctness, regression, security, data-loss, migration, compatibility, or maintainability risks.
- The PR appears to include unrelated scope creep, broad churn, accidental formatting, generated artifacts, secrets, debug code, or temporary scaffolding.
- The branch is not mergeable or appears out of date in a way that could invalidate tests or approvals.

Review thread handling:
- Continue inspecting every substantive human, bot, and AI reviewer comment.
- Judge the underlying concern against the latest diff, tests, code comments, and discussion.
- An unresolved GitHub thread is not a blocker merely because its UI state remains unresolved.
- If the latest code adequately addresses the concern, treat it as addressed and do not mention or dwell on the unresolved thread.
- If the underlying concern remains valid and requires repository changes, include that work in category 2.
- Preserve strict handling of genuinely unaddressed reviewer concerns and recurring valid AI-review findings.

Do not block merge for low-value nits. Only produce an `@codex` comment for issues that should be fixed or justified before merge.

Merge-readiness tally lifecycle for category 2:
- On the first category 2 response in this LLM conversation, when no earlier tally exists, construct a comprehensive tally of all current merge blockers with every item initially marked `⬜️`. Do not seed already-resolved historical concerns as completed items.
- On later invocations, locate the most recent tally in the conversation and reconcile it against the latest PR head, diff, tests, checks, reviews, and discussion. Treat a fully checked tally as supporting evidence, not a substitute for a fresh merge-readiness review of the current PR state.
- Retain completed and unresolved items so the history remains in context. Preserve item wording and ordering when practical. Never silently remove an earlier item; if it becomes obsolete or proves non-blocking, mark it `✅` with a concise explanation.
- Every tally item must begin directly with `⬜️` when it remains unresolved or `✅` when the latest PR state verifies it is complete, obsolete, or safely non-blocking under these merge-readiness rules.
- Mark an item `✅` only after independently verifying the result in the PR. Issuing an `@codex` task or seeing a claimed fix is insufficient. Change a completed item back to `⬜️` if later changes regress it.
- Add newly discovered blockers as `⬜️`. Consolidate duplicate findings by underlying root cause and exclude optional polish or low-value nits.
- Select one or a small, coherent, reliably executable group of currently unchecked repository-work items for the current `@codex` comment. Group tightly related items when safe to reduce unnecessary commits, but do not overload one Codex task with unrelated work.
- Identify every item selected for the current Codex task directly in the tally with the suffix `— targeted by the @codex comment above`. Selected items must remain `⬜️` until a later invocation verifies their implementation.
- If a material PR-description correction is already known while repository work remains, track it as one distinct `⬜️` item at the end of the tally. Keep it permanently last; insert newly discovered repository blockers before it. Do not include it in the `@codex` task.
- Emit category 3 only when every repository-work tally item has been verified complete and the PR-description correction is the sole remaining blocker. If the PR description is the only blocker on the first invocation, return category 3 immediately without creating a tally. If the PR is ready immediately, return category 1 immediately without creating a tally.

When recurring AI review comments are present:
- Determine whether the repeated comment is still valid.
- If it is valid, ask Codex to fix the underlying issue directly.
- If the current code is intentional and the AI reviewer is repeatedly asking to revert or change it, ask Codex to add a minimal inline or multiline code comment near the relevant logic explaining the invariant, tradeoff, or rationale, so future reviewers understand why the change should remain.
- Prefer durable explanations in code only when the rationale is not already obvious from names, tests, or surrounding context.
- Do not ask Codex to blindly placate a bot by weakening correct code.

The category 2 `@codex` comment must:
- Be concise but complete enough for a fresh Codex task.
- Start with a brief Scope Lock stating allowed files/areas, do-not-touch areas if known, and that the diff should stay minimal.
- Include a "Reviewer comment resolution" section that maps each selected substantive concern in the current bounded batch to the concrete repository change or durable in-code justification needed.
- For each selected concern, ask Codex to either implement the reviewer’s suggested change or add enough durable justification in the repository to address the concern and proceed without further changes.
- Name specific reviewers, files, symbols, comments, threads, checks, or quoted snippets when possible.
- Include concrete implementation steps.
- Include verification commands, choosing the narrowest relevant commands first.
- Avoid broad refactors unless they are required for correctness.
- Preserve existing conventions and tests.
- Use an outer three-backtick `text` fence for the category 2 response, leaving triple tildes (`~~~`) available for any nested code fences inside the comment because nested triple backticks can break formatting.
- Append `new codex task, not a r/e/v/i/e/w task` as the final line of the generated `@codex` comment, after all other comment text.

Before answering, be strict: category 1 requires repository readiness, addressed or safely non-blocking substantive reviewer concerns, and a materially accurate PR description; category 2 takes precedence over category 3 when both repository work and description work are needed, while known description problems are assessed and tracked in the tally until repository work is complete.
```

## Upgrade Prompt

```text
Improve the main PR final merge-check prompt above while preserving its purpose and Streamdeck-friendly shape.

Goals:
- Keep the main prompt copy/paste-ready with a `<PR-URL>` placeholder.
- Preserve exactly three mutually exclusive output categories with deterministic, unnumbered precedence labels:
  - Highest priority: repository changes needed to make the PR merge-ready return category 2, one outer three-backtick `text` fenced code block containing one actionable `@codex` PR comment
  - Next: PR description-only corrections return category 3, a concise manual instruction followed by one fenced `markdown` block containing the complete replacement PR description
  - Otherwise: ready-to-merge PRs return category 1, the exact success output `yes, it can be merged`
- Preserve the rule that category 2 takes precedence when both repository changes and PR-description corrections are needed, so description-only assessment is deferred until the merge check is rerun after repository work is complete.
- Preserve the requirement that the LLM only says yes when every substantive reviewer comment is addressed or safely non-blocking and the PR description does not require a material correction.
- Preserve the requirement that unresolved GitHub thread UI state alone is not a blocker when the latest code, tests, comments, or discussion adequately address the underlying concern.
- Preserve strict handling of genuinely unaddressed reviewer concerns and recurring valid AI-review findings.
- Preserve the requirement that the `@codex` comment concretely maps each remaining substantive concern to a repository change or durable in-code justification, not thread-resolution bookkeeping.
- Preserve the requirement that category 2 emits no text outside its single outer three-backtick `text` fenced `@codex` comment.
- Preserve the ban on asking Codex to edit the PR title or description or to click, mark, or otherwise resolve review threads.
- Preserve the requirement to use an outer three-backtick `text` fence for the category 2 `@codex` comment, leaving triple tildes (`~~~`) available for nested code fences inside that comment.
- Preserve the requirement to use triple tildes (`~~~`) for nested code fences inside the replacement PR description, and to wrap category 3's replacement-description block in a longer outer fence such as `~~~~markdown` so nested fences cannot close it early.
- Preserve the requirement that generated `@codex` comments end with `new codex task, not a r/e/v/i/e/w task`, while ensuring the main prompt itself does not end with that sentinel line.
- Preserve the requirement that category 3 contains a complete replacement PR description, with no placeholders, TODOs, partial patches, suggested fragments, `@codex`, or Codex sentinel line.
- Make the prompt better at distinguishing true merge blockers from low-value nits.
- Make the prompt better at handling recurring AI review comments without blindly reverting correct code.
- Make the prompt better at producing followups that let maintainers confidently address every remaining substantive concern.
- Keep the wording compact enough to use as a Streamdeck action.

Return:
1. The revised main prompt inside a fenced `text` block.
2. A brief bullet list explaining the improvements.
```
