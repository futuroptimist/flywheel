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
- Highest priority: if code, tests, configuration, generated artifacts, documentation in the repository, or any other repository changes are still needed for merge readiness, return category 2. If a material PR-description correction is also already known, track it in the category 2 tally as described below, but do not ask Codex to perform PR metadata work.
- Next: otherwise, if the PR is technically merge-ready but its description is materially inaccurate, incomplete, stale, misleading, or missing information necessary for a responsible merge record, return category 3.
- Otherwise: return category 1.

Category 1: exact conditional-success response
- If the PR is ready to merge and the PR description is merge-ready, select exactly one of these two responses.
- Respond with exactly:
  yes, it can be merged
  only when all relevant required checks on the latest head have completed successfully or every completed adverse check is verified as unrelated under the exception below, mergeability is acceptable, required approvals are satisfied or no longer needed, every substantive reviewer comment is addressed or safely non-blocking, and the PR description does not require a material correction.
- Respond with exactly:
  yes, it can be merged assuming the pending CI checks succeed
  only when every non-CI readiness condition is satisfied and the only remaining uncertainty is one or more expected, relevant checks on the latest head that are legitimately queued or in progress.
- Do not use the conditional response when any relevant check failed, was cancelled, timed out, requires action, or otherwise produced an adverse conclusion; when checks are stale, missing, attached only to an older commit, or ambiguous in a way that matters; when the branch is unmergeable or materially out of date; when approvals, substantive reviewer concerns, repository changes, or a material PR-description correction remain; when there is evidence that pending CI requires repository work rather than merely time to complete; or when a completed adverse check is verified as unrelated under the exception below and no relevant latest-head checks are pending.
- Emit only the selected category 1 sentence, with no tally, caveats, summaries, bullets, or extra commentary.
- Do not include a merge-readiness tally in category 1.

Category 2: repository changes needed
- If the PR is not ready to merge because repository changes are still needed, respond with exactly one element and no other prose before or after it:
  - One copy/paste-ready outer three-backtick `text` fenced code block containing the complete generated GitHub PR comment that begins with `@codex`.
- Put the complete `Merge-readiness tally:` inside the generated `@codex` comment. Do not emit any tally, caveat, summary, or explanation outside the fence.
- Include only work Codex can perform in the repository as targeted implementation instructions. Never ask Codex to edit, rewrite, or update the PR title or description, or to click, mark, or otherwise resolve a review thread.
- The `@codex` comment should target one small, coherent, reliably executable group of currently unchecked repository-work items. Group multiple tightly related items when safe to reduce unnecessary commits, but do not overload one Codex task with unrelated work.
- The in-comment tally remains the authoritative record of all known blockers, including blockers not selected for the current task.
- The generated `@codex` comment must be fully self-contained and must not rely on phrases such as “the item above.”

Category 2 generated comment order:
- `@codex`
- Scope Lock
- Complete merge-readiness tally
- Task-selection warning
- Reviewer comment resolution
- Concrete implementation instructions
- Verification commands
- `new codex task, not a r/e/v/i/e/w task` as the final line

Category 2 task-selection warning:
- Include a warning section that says all of the following:
  - Implement only unresolved entries marked `— targeted by this Codex task`.
  - Unresolved entries marked `— context only; not targeted by this Codex task` are supplied solely for diagnosis and must not expand the Scope Lock.
  - Completed `✅` entries are history, not work requests.
  - PR-description corrections are manual maintainer actions and must never be implemented by Codex.

Category 2 merge-readiness tally lifecycle:
- Every tally item must begin directly with `⬜️` when it remains unresolved or `✅` when the latest PR state verifies it is complete, obsolete, or safely non-blocking under these merge-readiness rules.
- On the first category 2 response when no earlier tally exists in the conversation, construct a comprehensive tally of all current merge blockers with every item initially marked `⬜️`. Do not seed already-resolved historical concerns as completed items.
- On later invocations, locate and reconcile the most recent tally from this conversation, including inside the single outer `text` fenced block of the most recent category 2 response, against the latest PR head, diff, tests, checks, reviews, and discussion.
- Retain every prior tally entry so the history remains in context. Never silently remove an earlier item. If it becomes obsolete or proves non-blocking, mark it `✅` with a concise explanation.
- Preserve item wording and ordering when practical.
- Mark an item `✅` only after independently verifying the result in the PR; issuing an `@codex` task or seeing a claimed fix is insufficient. If a prior category 2 tally recorded a CI failure that later qualifies for the demonstrably unrelated CI exception below, retain the item and mark it `✅` with a concise explanation identifying the specific owning GitHub issue or separate pull request.
- Change a completed item back to `⬜️` if later changes regress it.
- Add newly discovered blockers as `⬜️`. Consolidate duplicate findings by underlying root cause and exclude optional polish or low-value nits; when an earlier tally item is a duplicate of a retained consolidated item, keep the earlier item in place and mark it `✅` with a concise duplicate-of explanation rather than deleting it.
- Identify every item selected for the current Codex task directly in the tally with the suffix `— targeted by this Codex task`. Selected items must remain `⬜️` until a later invocation independently verifies their implementation.
- Identify unresolved items not selected for the current bounded batch with the suffix `— context only; not targeted by this Codex task`. These entries are diagnostic context only, not implementation instructions.
- On subsequent invocations, retain every prior tally entry, reconcile its status, and apply the targeted suffix only to the current bounded batch. Previously targeted but still unresolved entries become context-only unless selected again.
- Treat a fully checked tally as supporting evidence, not a substitute for a fresh merge-readiness review of the current PR state.
- If a material PR-description correction is already known while repository work remains, track it as one distinct `⬜️` item inside the complete merge-readiness tally with the suffix `— context only; not targeted by this Codex task`. Keep it permanently last; insert newly discovered repository blockers before it. Treat it solely as a manual maintainer action: defer generating the replacement PR description, keep assessing and tracking the known description problem, and never include it in Reviewer comment resolution or Concrete implementation instructions.
- Emit category 3 only when every repository-work tally item has been verified complete and the PR-description correction is the sole remaining blocker. This should be the final remediation response before category 1 when the user applies the replacement and no new blocker appears.
- If the PR description is the only blocker on the first invocation, return category 3 immediately without creating a tally.
- If the PR is ready immediately, return category 1 immediately without creating a tally.

Category 2 tally entry quality:
- Make each tally entry useful diagnostic context. When known, each entry should concisely identify the relevant reviewer, check, run, file, or symbol; the observed behavior or failed contract; why it blocks merging; and the condition that would prove it complete.
- Avoid vague entries that contain only a proposed solution.
- Do not imply that context-only or PR-description tally entries are implementation instructions.

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
- Do not include a merge-readiness tally in category 3.

Treat these as merge blockers that require category 2 when they need repository changes:
- CI is failing, cancelled, timed out, requires action, stale, missing, attached only to an older commit, ambiguous in a way that matters, or otherwise reveals or requires repository changes, except for completed adverse checks that qualify for the demonstrably unrelated CI exception below; ordinary expected latest-head checks that are merely queued or in progress do not create or continue category 2 by themselves when no repository work is needed.
- There are active requested changes or substantive unaddressed reviewer concerns.
- A reviewer asked a question and the code, tests, comments, or PR discussion do not yet answer it well enough.
- A reviewer suggested a change and the PR neither implemented it nor explains convincingly why the current approach is better.
- The diff has likely correctness, regression, security, data-loss, migration, compatibility, or maintainability risks.
- The PR appears to include unrelated scope creep, broad churn, accidental formatting, generated artifacts, secrets, debug code, or temporary scaffolding.
- The branch is not mergeable or appears out of date in a way that could invalidate tests or approvals.

Demonstrably unrelated CI exception:
- A completed adverse check may be treated as non-blocking only after independently comparing its failure output, affected files, affected code paths, and timing with the PR title, description, final diff, and current base branch, and verifying that the current PR could not reasonably have caused the failure and no change in this PR is needed to correct it.
- Require a specific relevant GitHub issue or separate pull request that documents or addresses the same underlying root cause. An author assertion, unsupported flakiness claim, different filenames alone, or the mere existence of an unrelated issue or pull request is not sufficient.
- Keep the check blocking when attribution is ambiguous, the changed code could affect the failure, the tracking issue or pull request does not cover the same root cause, the failure invalidates testing relevant to this PR, mergeability or branch protection still mechanically prevents merging, or the branch is materially out of date in a way that could invalidate checks.
- When all other readiness conditions are satisfied and every completed adverse check is verified under this exception, category 1 may use the unconditional `yes, it can be merged` response. Do not use the pending-CI response for an already-completed unrelated failure.

Review thread handling:
- Continue inspecting every substantive human, bot, and AI reviewer comment.
- Judge the underlying concern against the latest diff, tests, code comments, and discussion.
- An unresolved GitHub thread is not a blocker merely because its UI state remains unresolved.
- If the latest code adequately addresses the concern, treat it as addressed and do not mention or dwell on the unresolved thread.
- If the underlying concern remains valid and requires repository changes, include that work in the category 2 tally and select it for the `@codex` comment only if it belongs in the current bounded batch.
- Preserve strict handling of genuinely unaddressed reviewer concerns and recurring valid AI-review findings.

Do not block merge for low-value nits. Only produce an `@codex` comment for issues that should be fixed or justified before merge.

When recurring AI review comments are present:
- Determine whether the repeated comment is still valid.
- If it is valid, ask Codex to fix the underlying issue directly when selecting that concern for the current bounded batch.
- If the current code is intentional and the AI reviewer is repeatedly asking to revert or change it, ask Codex to add a minimal inline or multiline code comment near the relevant logic explaining the invariant, tradeoff, or rationale only when selecting that concern for the current bounded batch, so future reviewers understand why the change should remain.
- Prefer durable explanations in code only when the rationale is not already obvious from names, tests, or surrounding context.
- Do not ask Codex to blindly placate a bot by weakening correct code.

The category 2 `@codex` comment must:
- Be concise but complete enough for a fresh Codex task.
- Start with a brief Scope Lock stating allowed files/areas, do-not-touch areas if known, and that the diff should stay minimal.
- Include a "Reviewer comment resolution" section covering only entries marked `— targeted by this Codex task`.
- For each targeted concern, state the evidence from the current PR state; the underlying contract, risk, or user-visible failure; the required outcome; a suggested implementation only when the evidence supports it; and verification that directly proves the outcome.
- Require Codex to inspect the current code before applying a reviewer’s suggested patch. If a smaller or different change correctly satisfies the underlying contract, Codex should prefer that over blindly implementing a stale or speculative suggestion.
- Name specific reviewers, files, symbols, comments, threads, checks, or quoted snippets when possible.
- Include concrete implementation steps covering only currently targeted entries.
- Include verification commands, choosing the narrowest relevant commands first and tying them to the targeted outcomes.
- Avoid broad refactors unless they are required for correctness.
- Preserve existing conventions and tests.
- Use an outer three-backtick `text` fence for the category 2 response, leaving triple tildes (`~~~`) available for any nested code fences inside the comment because nested triple backticks can break formatting.
- Append `new codex task, not a r/e/v/i/e/w task` as the final line of the generated `@codex` comment, after all other comment text.

Before answering, be strict: category 1 requires fully green latest-head CI, completed adverse checks verified under the demonstrably unrelated CI exception, or conditional readiness under the narrow pending-CI rule above; acceptable mergeability and branch protection; repository readiness; addressed or safely non-blocking substantive reviewer concerns; and a materially accurate PR description. Category 2 takes precedence over category 3 when both repository work and description work are needed.
```

## Upgrade Prompt

```text
Improve the main PR final merge-check prompt above while preserving its purpose and Streamdeck-friendly shape.

Goals:
- Keep the main prompt copy/paste-ready with a `<PR-URL>` placeholder.
- Preserve exactly three mutually exclusive output categories with deterministic, unnumbered precedence labels:
  - Highest priority: repository changes needed to make the PR merge-ready return category 2, one outer three-backtick `text` fenced code block containing the complete generated `@codex` PR comment, including the self-contained merge-readiness tally
  - Next: PR description-only corrections return category 3, a concise manual instruction followed by one fenced `markdown` block containing the complete replacement PR description
  - Otherwise: ready-to-merge PRs return category 1, the exact success output `yes, it can be merged`, including when all other readiness conditions are satisfied and every completed adverse check is verified under the demonstrably unrelated CI exception rather than still pending
- Preserve the rule that category 2 takes precedence when both repository changes and PR-description corrections are needed, so description-only assessment is tracked as non-targeted maintainer context in the category 2 tally and replacement-description generation is deferred until repository work is complete.
- Preserve the requirement that the LLM only says yes when every substantive reviewer comment is addressed or safely non-blocking and the PR description does not require a material correction.
- Preserve the demonstrably unrelated CI exception: adverse completed checks are non-blocking only when the LLM independently compares the failure with the PR description, final diff, and base branch; verifies the PR could not reasonably have caused it and needs no corrective change; identifies a specific relevant GitHub issue or separate pull request owning the same root cause; and confirms mergeability or branch protection does not still prevent merging.
- Preserve strict CI evidence requirements: do not waive failures based only on author assertions, generic flakiness claims, different filenames, or unrelated tracking records; keep failures blocking when attribution is ambiguous, changed code could affect them, the tracker does not cover the same root cause, or relevant testing is invalidated.
- Preserve the requirement that unresolved GitHub thread UI state alone is not a blocker when the latest code, tests, comments, or discussion adequately address the underlying concern.
- Preserve strict handling of genuinely unaddressed reviewer concerns and recurring valid AI-review findings.
- Preserve the requirement that the category 2 comment includes a self-contained `Merge-readiness tally:` with current-target versus context-only labeling, full tally lifecycle/history retention, completed entries for prior CI blockers later verified under the unrelated-failure exception with the owning issue or pull request named, and no tally text outside the fence.
- Preserve the requirement that the `@codex` comment concretely maps only currently targeted substantive concerns to repository changes or durable in-code justification, not thread-resolution bookkeeping.
- Preserve root-cause-oriented reviewer-resolution instructions: inspect current code, identify evidence and the underlying contract/risk/user-visible failure, require the outcome, suggest implementations only when evidence supports them, and verify the outcome directly.
- Preserve bounded task scope: only one small coherent batch is targeted, context-only and completed tally entries are not work requests, and PR-description corrections are manual maintainer actions.
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
