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

This review concerns only `<PR-URL>`. Every agent remediation must remain on that PR's existing head branch and in its head repository, including when the head repository is a fork. Never ask an agent to create, open, publish, use, or switch to a separate branch or pull request, or to move required work into a replacement, stacked, docs-only, or follow-up pull request. This invariant applies throughout the response, including the Scope Lock, tally entries, implementation instructions, verification, and recommendations. Use the verified head-branch name when available; otherwise say “the referenced PR's existing head branch.” Never invent a branch name or require a particular local checkout alias.

Review the PR using the available GitHub context:
- PR title, description, linked issues, branch/base status, mergeability, and latest commit.
- The diff and any files likely affected by the change.
- Required checks, check runs, and commit statuses for the latest head, following pagination where supported. Reconcile duplicate contexts by their current result: a failure superseded by a successful latest-head rerun is history, not an active failure. Inspect pending, failed, skipped, neutral, and stale results, including every Codecov context that the available GitHub context exposes.
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
Respond with exactly one of these four mutually exclusive categories, evaluated in this order:
- Highest priority: if code, tests, configuration, generated artifacts, documentation in the repository, or any other repository changes are still needed for merge readiness and at least one unresolved repository-work item is Codex-performable, return category 2. If a material PR-description correction is also already known, track it in the category 2 tally as described below, but do not ask Codex to perform PR metadata work.
- Next: otherwise, if the PR is technically merge-ready but its description is materially inaccurate, incomplete, stale, misleading, or missing information necessary for a responsible merge record, return category 3.
- Next: otherwise, if an external/manual blocker or material evidence limitation remains and no concrete repository change is established, return category 4. Also return category 4 when concrete repository work is known but an explicit hard user constraint or access limitation makes every remaining repository-work item unperformable by Codex; this narrow exception avoids emitting an impossible `@codex` task and does not make the underlying work optional.
- Otherwise: return category 1.

Category 1: exact conditional-success response
- If the PR is ready to merge and the PR description is merge-ready, select exactly one of these two responses.
- Respond with exactly:
  yes, it can be merged
  only when every relevant required check on the latest head is complete and each such check completed successfully, was verified intentionally non-applicable under the skipped/neutral rule and permitted by required-check policy, or, if adverse, was independently verified as unrelated under the exception below; all exposed Codecov evidence satisfies the Codecov rules; mergeability is acceptable; required approvals are satisfied or no longer needed; every substantive reviewer comment is addressed or safely non-blocking; and the PR description does not require a material correction.
- Respond with exactly:
  yes, it can be merged assuming the pending CI checks succeed
  only when every non-CI readiness condition is satisfied and the only remaining uncertainty is one or more expected, relevant checks on the latest head that are legitimately queued or in progress.
- Do not use the conditional response when any relevant check failed, was cancelled, timed out, requires action, or otherwise produced an adverse conclusion; when checks are stale, missing, attached only to an older commit, incomplete outside the narrow pending-CI case, or ambiguous in a way that matters; when the branch is unmergeable or materially out of date; when approvals, substantive reviewer concerns, repository changes, or a material PR-description correction remain; when there is evidence that pending CI requires repository work rather than merely time to complete; or when a completed adverse check is verified as unrelated under the exception below and no relevant latest-head checks are pending.
- Emit only the selected category 1 sentence, with no tally, caveats, summaries, bullets, or extra commentary.
- Do not include a merge-readiness tally in category 1.

Codecov requirements:
- Patch coverage measures changed coverable code; project coverage measures the repository's whole configured coverage scope. Inspect both when the available GitHub context exposes them, but do not require a project result merely because a patch result exists.
- Treat every Codecov check or status on the latest head that the available GitHub context exposes as relevant evidence, including `codecov/patch`, `codecov/project`, and flag or component checks. A passing patch result must not conceal a visible adverse project, flag, or component result, even when GitHub does not label it required or the overall summary appears green.
- Classify results consistently. `success` is a successful measurement. `queued` or `in_progress` is legitimately pending only when it is a current, applicable latest-head run. Failed, errored, cancelled, timed-out, stale, or action-required results are adverse and block approval; exposed adverse Codecov results cannot use the demonstrably unrelated CI exception. A skipped or neutral result is not a successful coverage measurement: treat it as non-blocking only when available evidence establishes intentional non-applicability and required-check policy permits it; otherwise it is unresolved evidence for category 4 unless concrete repository work establishes category 2.
- Do not infer a Codecov failure, pending result, or publication defect from an absent `codecov/project`, `codecov/patch`, flag, or component context. A successful, complete read of both check runs and commit statuses showing no optional project context is absence, not incomplete inspection. API errors, permission failures, truncated responses, and partial screenshots are evidence limitations and must not be certified as passing.
- Repository workflow or Codecov configuration may explain intended targets, scope, and publication, but does not prove that an unexposed result failed, should have been published, or requires repository changes. Preserve actual required-check and explicit maintainer requirements, but never invent targets, require 100% coverage, or ask Codex to add or strengthen a coverage gate during readiness review. Configuration alone must not trigger repeated publication-setting tasks.
- An absent optional context alone must not block category 1, create a category 2 item, trigger a configuration task, or delay category 3. If a prior tally treated absence alone as a blocker, retain it but mark it `✅` as “non-blocking under the revised policy,” never as passed. Do not close a previously observed failure merely because it can no longer be retrieved; verify a current successful superseding result or use category 4 for the evidence limitation.
- Do not require inaccessible external Codecov diagnostics, account settings, API results, or dashboard state. If branch protection exposes an expected required check as pending or missing, approval remains blocked; diagnose the exact visible condition without assuming a repository defect, using category 2 only for established repository work and otherwise category 4.
- For an exposed queued or in-progress Codecov check, use the conditional category 1 response only when it satisfies the same narrow pending-CI rule as every other check.
- Read the applicable coverage target from the Codecov result, comment, or repository configuration. Never assume a universal percentage, and never substitute a remembered target from another repository. A passing project or overall coverage result does not override a failing patch, flag, or component result.

Category 2: repository changes needed
- If the PR is not ready to merge because repository changes are still needed, respond with exactly one element and no other prose before or after it:
  - One copy/paste-ready outer three-backtick `text` fenced code block containing the complete generated GitHub PR comment that begins with `@codex`.
- Put the complete `Merge-readiness tally:` inside the generated `@codex` comment. Do not emit any tally, caveat, summary, or explanation outside the fence.
- Include only work Codex can perform in the repository as targeted implementation instructions. Never ask Codex to edit, rewrite, or update the PR title or description, or to click, mark, or otherwise resolve a review thread.
- The `@codex` comment should target one small, coherent, reliably executable group of currently unchecked repository-work items. Group multiple tightly related items when safe to reduce unnecessary commits, but do not overload one Codex task with unrelated work.
- Every generated Scope Lock must explicitly require work on the same referenced PR and its existing head branch. Multiple bounded remediation batches are successive tasks or commits on that same branch and PR; blockers outside the current batch remain context-only until selected for a later batch.
- Minimal-diff guidance and default or LLM-invented file-count limits must not omit or relocate required implementation, tests, or documentation. Address unrelated churn by removing the unnecessary changes from the referenced PR, without asking an agent to preserve them elsewhere. If the necessary work is too broad for one task, reduce unrelated changes or divide the necessary work into bounded batches on the same branch and PR; do not “stop and split” it into another branch or PR.
- Use category 2 only when at least one unresolved repository-work item can be selected as a reliably executable, Codex-performable batch. If an explicit hard user constraint or access limitation makes every remaining repository-work item unperformable by Codex, use the narrow category 4 exception instead. Do not silently override the constraint, claim readiness, or propose another branch or PR.
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
- If a prior tally prescribed another branch or pull request, correct that invalid routing to the referenced PR's existing head branch while retaining the unmet repository requirement as `⬜️`. Superseding an invalid workflow does not prove the underlying defect is fixed.
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

Category 4: external/manual blocker or insufficient evidence
- Use this category when merge approval cannot be justified because an external/manual condition or material evidence limitation remains and no concrete repository change is established. Also use it when concrete repository work is known but an explicit hard user constraint or access limitation makes every remaining repository-work item unperformable by Codex. Examples include missing permissions, an external service publication problem, an outstanding approval, unexplained skipped/neutral evidence, a required-but-missing context, or incomplete check/status retrieval.
- Respond concisely with the exact check or context and latest-head SHA, or the exact unavailable evidence; what was successfully verified; and the smallest maintainer action or read-only verification needed next.
- Do not claim merge readiness, emit a tally, or include a speculative `@codex` task. Do not prescribe repository or publication-setting edits without evidence that they are needed.
- Category 2 takes precedence whenever concrete repository work remains and at least one unresolved item is Codex-performable; record external blockers there as context only, not as targeted work. The all-work-unperformable exception above is category 4: identify each known repository blocker, the exact constraint or missing access that prevents Codex from acting, and the smallest maintainer action needed to unblock it, without an `@codex` task or tally. Category 3 applies only when description correction is the sole blocker. Ordinary legitimately pending CI still uses the conditional category 1 sentence when every other condition is satisfied.
- Repeating the same unresolved external diagnosis without new evidence must not generate a new configuration-change task.

Treat these as merge blockers that require category 2 when they need repository changes:
- CI is failing, cancelled, timed out, requires action, stale, missing, attached only to an older commit, ambiguous in a way that matters, or otherwise reveals or requires repository changes, except for completed adverse checks that qualify for the demonstrably unrelated CI exception below and unexposed Codecov contexts covered by the Codecov requirements above; ordinary expected latest-head checks that are merely queued or in progress do not create or continue category 2 by themselves when no repository work is needed.
- There are active requested changes or substantive unaddressed reviewer concerns.
- A reviewer asked a question and the code, tests, comments, or PR discussion do not yet answer it well enough.
- A reviewer suggested a change and the PR neither implemented it nor explains convincingly why the current approach is better.
- The diff has likely correctness, regression, security, data-loss, migration, compatibility, or maintainability risks.
- The PR appears to include unrelated scope creep, broad churn, accidental formatting, generated artifacts, secrets, debug code, or temporary scaffolding.
- The branch is not mergeable or appears out of date in a way that could invalidate tests or approvals.

Demonstrably unrelated CI exception:
- A completed adverse check may be treated as non-blocking only after independently comparing its failure output, affected files, affected code paths, and timing with the PR title, description, final diff, and current base branch, and verifying that the current PR could not reasonably have caused the failure and no change in this PR is needed to correct it.
- Require a specific relevant GitHub issue or separate pull request that documents or addresses the same underlying root cause. An author assertion, unsupported flakiness claim, different filenames alone, or the mere existence of an unrelated issue or pull request is not sufficient.
- Treat an already-existing external issue or pull request only as read-only evidence for this exception; never instruct the agent to create a tracking pull request or implement a separate fix there.
- Keep the check blocking when attribution is ambiguous, the changed code could affect the failure, the tracking issue or pull request does not cover the same root cause, the failure invalidates testing relevant to this PR, mergeability or branch protection still mechanically prevents merging, or the branch is materially out of date in a way that could invalidate checks.
- When all other readiness conditions are satisfied, every relevant required latest-head check is complete, and each check succeeded, was verified intentionally non-applicable under the skipped/neutral rule and permitted by required-check policy, or had an adverse result verified under this exception, category 1 may use the unconditional `yes, it can be merged` response. An unrelated completed adverse check must not mask another relevant check that is pending, missing, stale, attached only to an older commit, or otherwise unresolved. Do not use the pending-CI response for an already-completed unrelated failure.

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
- Be a concise, self-contained agent task in the existing PR context.
- Start with a brief Scope Lock stating the referenced PR and its existing head branch, allowed files/areas, do-not-touch areas if known, and that the diff should stay minimal without excluding required implementation, tests, or documentation.
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
- Treat that required closing sentinel only as a task-mode marker; it never authorizes a new branch or pull request.

Before answering, be strict: unconditional category 1 requires every relevant required latest-head check to be complete and individually successful, intentionally non-applicable under the skipped/neutral rule, or verified unrelated under the demonstrably unrelated CI exception; all exposed coverage evidence must satisfy the Codecov rules above. Conditional category 1 is available only under the narrow pending-CI rule. Both category 1 responses also require acceptable mergeability and branch protection, repository readiness, addressed or safely non-blocking substantive reviewer concerns, and a materially accurate PR description. Apply the four-category precedence exactly; never convert absent optional evidence or an external limitation into invented repository work.
```

## Upgrade Prompt

```text
Improve the main PR final merge-check prompt above while preserving its purpose and Streamdeck-friendly shape.

Goals:
- Keep the main prompt copy/paste-ready with a `<PR-URL>` placeholder.
- Preserve the invariant that the review and all remediation concern only `<PR-URL>` and its existing head branch and head repository, including forks. Require every Scope Lock, tally target, implementation step, verification command, and recommendation to stay there; use the verified branch name or “the referenced PR's existing head branch,” never an invented name or required checkout alias; and never request a separate, replacement, stacked, docs-only, tracking, or follow-up branch or pull request. The closing sentinel does not relax this rule.
- Preserve exactly four mutually exclusive output categories with deterministic, unnumbered precedence labels:
  - Highest priority: repository changes needed to make the PR merge-ready return category 2 when at least one unresolved repository-work item is Codex-performable, with one outer three-backtick `text` fenced code block containing the complete generated `@codex` PR comment, including the self-contained merge-readiness tally
  - Next: PR description-only corrections return category 3, a concise manual instruction followed by one fenced `markdown` block containing the complete replacement PR description
  - Next: external/manual blockers or insufficient evidence with no established repository fix return category 4. Category 4 also covers the narrow case where concrete repository work is known but an explicit hard user constraint or access limitation makes every remaining item unperformable by Codex. Return a concise diagnosis naming the exact latest-head context or unavailable evidence, completed verification, known repository blockers when applicable, and smallest maintainer action or read-only verification; it must not claim readiness or emit a speculative `@codex` task
  - Otherwise: ready-to-merge PRs return category 1, the exact success output `yes, it can be merged`, including when all other readiness conditions are satisfied, every relevant required latest-head check is complete, and each check succeeded, was verified intentionally non-applicable under the skipped/neutral rule, or was verified under the demonstrably unrelated CI exception rather than still pending
- Preserve the rule that category 2 takes precedence when both repository changes and PR-description corrections are needed, so description-only assessment is tracked as non-targeted maintainer context in the category 2 tally and replacement-description generation is deferred until repository work is complete.
- Preserve the requirement that the LLM only says yes when every substantive reviewer comment is addressed or safely non-blocking and the PR description does not require a material correction.
- Preserve the demonstrably unrelated CI exception: adverse completed checks are non-blocking only when every relevant required latest-head check is complete, the LLM independently compares the failure with the PR description, final diff, and base branch; verifies the PR could not reasonably have caused it and needs no corrective change; identifies a specific relevant GitHub issue or separate pull request owning the same root cause; and confirms mergeability or branch protection does not still prevent merging.
- Preserve strict CI evidence requirements: do not waive failures based only on author assertions, generic flakiness claims, different filenames, or unrelated tracking records; keep failures blocking when attribution is ambiguous, changed code could affect them, the tracker does not cover the same root cause, or relevant testing is invalidated.
- Preserve evidence-based Codecov handling: explain patch versus project scope; inspect both check runs and commit statuses with pagination and reconcile current results per context; inspect every exposed patch, project, flag, and component result without requiring an optional project context merely because patch exists. Define success, legitimate queued/in-progress, adverse, and skipped/neutral separately. Skipped/neutral is non-blocking only when verified intentionally non-applicable and policy permits it; otherwise use category 4 unless repository work is established. Never waive an exposed adverse Codecov result, hide it behind a passing result, invent a target or 100% requirement, or add/strengthen a gate. Distinguish complete absence from failed/incomplete retrieval; configuration may explain intent but cannot prove failure or required remediation. Preserve actual required checks, and use category 4 for external or evidence blockers without an established repository fix.
- Preserve tally history accurately: retain absence-only entries as completed and “non-blocking under the revised policy,” never as passed; do not close a previously visible failure solely because it is no longer retrievable.
- Preserve unmet requirements when correcting a prior tally's invalid branch/PR routing; workflow correction alone does not prove the defect fixed.
- Preserve the requirement that unresolved GitHub thread UI state alone is not a blocker when the latest code, tests, comments, or discussion adequately address the underlying concern.
- Preserve strict handling of genuinely unaddressed reviewer concerns and recurring valid AI-review findings.
- Preserve the requirement that the category 2 comment includes a self-contained `Merge-readiness tally:` with current-target versus context-only labeling, full tally lifecycle/history retention, completed entries for prior CI blockers later verified under the unrelated-failure exception with the owning issue or pull request named, and no tally text outside the fence.
- Preserve the requirement that the `@codex` comment concretely maps only currently targeted substantive concerns to repository changes or durable in-code justification, not thread-resolution bookkeeping.
- Preserve root-cause-oriented reviewer-resolution instructions: inspect current code, identify evidence and the underlying contract/risk/user-visible failure, require the outcome, suggest implementations only when evidence supports them, and verify the outcome directly.
- Preserve bounded task scope: only one small coherent batch is targeted, context-only and completed tally entries are not work requests, and PR-description corrections are manual maintainer actions.
- Preserve bounded work on the same branch and PR: multiple batches are successive tasks or commits there, while untargeted blockers remain context-only. Minimal-diff guidance or invented file-count limits must not omit or relocate required implementation, tests, or documentation; remove unrelated churn from this PR rather than preserving it elsewhere; and replace “stop and split” advice with removing unrelated changes or batching necessary work on the same branch and PR.
- Preserve explicit hard user constraints and access limitations: use category 2 when at least one unresolved repository-work item remains Codex-performable, but use category 4 without an `@codex` task or tally when every remaining repository-work item is unperformable by Codex. Report the exact conflict and known blockers, and never silently override it, claim readiness, or route work to another branch or PR.
- Preserve existing external issues or pull requests as permissible read-only evidence for the demonstrably unrelated CI exception, never as instructions to create a tracker or perform a separate fix.
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

## Decision-table validation

Use these scenarios to validate revisions to both the Main Prompt and Upgrade
Prompt. “Complete inspection” means current-head check runs and commit statuses
were read through all available pages.

| Scenario | Required outcome |
| --- | --- |
| Patch passes; optional project context is absent after complete inspection; no other blocker | Category 1 |
| Same coverage evidence, but the PR description is materially stale | Category 3 |
| Patch passes; a project result visibly fails | No approval; category 2 only for established repository work, otherwise category 4 |
| GitHub explicitly requires a missing project check | No approval; diagnose without assuming a repository defect, using category 2 only for established repository work and otherwise category 4 |
| Applicable coverage is legitimately running; everything else is ready | Conditional category 1 |
| A skipped/neutral result is verified intentionally non-applicable and policy permits it | Non-blocking |
| A neutral result is unexplained, or evidence retrieval fails | Category 4; do not invent remediation |
| A prior failed result is superseded by a successful current-head rerun | No stale-failure blocker |
| An external publication problem persists without new repository evidence | Category 4; do not repeat a speculative Codex task |
| Required documentation exceeds a default file-count heuristic | Retain the documentation work in the same PR; the heuristic cannot narrow required scope |
| Several valid blockers require multiple bounded batches | Target successive tasks or commits on the same existing head branch and PR; keep untargeted blockers context-only |
| The diff contains unrelated churn | Remove the churn from this PR without requesting another branch or PR to preserve it |
| An earlier tally requested a docs-only PR, and the documentation is still missing | Correct routing to this PR's existing head branch and retain the documentation blocker until independently verified complete |
| An existing external PR documents the root cause of an unrelated adverse CI result | It may serve as read-only evidence for the exception; do not request a tracking PR or separate implementation |
| Branch identity is unavailable but work is otherwise Codex-performable | Use “the referenced PR's existing head branch”; do not invent another branch or PR |
| A hard constraint or access limitation prevents some repository work, but another coherent repository-work batch is Codex-performable | Category 2; target only the performable batch and retain the constrained blocker as context |
| A hard constraint or access limitation makes every remaining repository-work item unperformable by Codex | Category 4; identify the blockers, exact conflict, and smallest maintainer action without emitting an `@codex` task or tally |
