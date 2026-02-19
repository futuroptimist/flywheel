---
title: "PR candidate picker (4-way, multi-merge-safe) + finishing @codex comments"
slug: "pr-candidate-picker-multi"
conversational: true
---

# PR candidate picker (4-way, multi-merge-safe) + finishing `@codex` comments

Use this when you have **exactly four** competing PR candidates that all claim to implement the
same original prompt, and you need to:

- pick **one or more** winners, **only if** they can be merged together safely,
- avoid merge conflicts and contradictory behavior, and
- produce **copy/paste-ready `@codex` PR comments** that get each chosen PR to “100%”.

This template has two fill-in sections:
1) an unordered list of **4 PR URLs**
2) the **original prompt** (verbatim) in a code block

---

## Copy-ready prompt

````text
You are an advanced LLM with reasoning reviewing pull requests.

You will be given:
- Exactly 4 candidate PR URLs (same repo, same goal).
- The original prompt that the PRs were supposed to implement.

Your tasks:
1) Select the merge-safe set of winners: either exactly ONE PR, or MULTIPLE PRs.
2) Briefly justify why each selected PR belongs in the winning set.
3) If any selected PR is not already “100%”, output a distinct PR comment for each selected PR
   that begins with `@codex` and contains the concrete remaining work needed to get it to “100%”.

Hard requirements:
- You may pick 1 or more winners.
- Pick multiple winners IF AND ONLY IF all selected PRs can be merged safely together:
  - no textual merge conflicts on the same hunks/files, and
  - no behavioral contradictions (one PR negates or conflicts with another).
- If only one PR can be merged safely, pick exactly one best winner.
- Assume all non-selected PRs will be closed.
- Prefer the smallest merge-safe set that fully satisfies the original prompt.
- If none are perfect, still pick the best merge-safe option and use `@codex` comment(s) to close
  the remaining gap.
- Every `@codex` comment must be actionable:
  - name specific files/paths when possible,
  - include specific search commands when you’re not sure where the last stragglers are,
  - include verification commands (tests, lint, a specific CLI invocation, etc.).
- Append the following string verbatim as the last line of every `@codex` comment (after any
  other text):
  `new codex task, not a r/e/v/i/e/w task`
- Start each `@codex` comment with a Scope Lock recap (use provided Scope Lock if filled;
  otherwise state “No scope lock provided” and proceed):
  - “Only touch X/Y/Z; do not touch A/B/C; keep diff small; run these commands.”
- Include a diff sanity check in each `@codex` comment:
  - “If `git diff --stat` shows > <max files> or touches do-not-touch areas, stop and split.”

Optimization order:
correctness > prompt-alignment > merge-safety > minimal-risk changes > maintainability > style

How to evaluate candidates:
- Read PR description: does it match the original prompt or drift?
- Scan each diff: does it touch the right files and update references comprehensively?
- Watch for suspicious churn: big refactors, mass formatting, unrelated renames, new features.
- If a candidate touches unrelated areas (new features, unrelated tests, refactors), treat that as
  suspicious churn and downgrade it unless the original prompt explicitly requires it.
- Prefer PRs that touch fewer files and are localized to the bug surface; penalize new features,
  unrelated refactors, or non-required tests.
- Prefer regression tests that assert the user-visible contract directly; avoid brittle heuristics
  unless explicitly requested.
- If tests are flaky, fix the cause rather than loosening tests.
- Check durability: tests/fixtures/docs updated so the change won’t regress.
- Prefer “complete + boring” over “clever + risky”.

How to evaluate merge-safety across multiple winners:
- Compare touched paths and likely overlapping hunks.
- Detect direct conflicts (same lines changed differently).
- Detect semantic conflicts (different APIs/contracts, opposite behavior, duplicate incompatible
  migrations, contradictory docs).
- If conflicts are uncertain, default to the safer smaller winning set.
- Do NOT choose multiple winners that require manual conflict resolution.

Scope Lock (fill in if you care; otherwise leave blank)
- Allowed files/paths:
  - <optional list>
- Do NOT touch:
  - <optional list>
- Max files changed (default 8): <optional number>

Enforcement rules:
- Strongly prefer candidates that stay within scope.
- If the best merge-safe set exceeds scope, still pick the least-bad set but each `@codex`
  comment MUST:
  (a) shrink scope back to the prompt, and
  (b) explicitly defer unrelated changes to a follow-up PR.

Output format (must be exactly this structure):
- Winners:
  - <URL>
  - <URL> (optional additional winners)
- Why these:
  - <bullet>
  - <bullet>
- Follow-up `@codex` comments:
  - For <URL_1>:
    ```text
    @codex
    ...
    ```
  - For <URL_2> (include only when multiple winners selected):
    ```text
    @codex
    ...
    ```

Linking rule:
- If exactly one winner is selected, output one winner link and one `@codex` comment.
- If multiple winners are selected, output each winner link and provide a separate fenced
  `@codex` comment for each winner.

What “100%” means (prompt-scoped):
- The original prompt’s requirements are satisfied (no more, no less).
- No unrelated behavior changes outside the prompt’s surface area.
- Diffs are intentionally small and localized; broad refactors must be split into follow-up PRs.
- Tests added are minimal + deterministic and directly assert the intended contract.
- Verification steps are included and plausibly pass.

Now process the inputs below.

### Candidate PRs (exactly 4)
- <PR_URL_1>
- <PR_URL_2>
- <PR_URL_3>
- <PR_URL_4>

### Original prompt (paste verbatim)
```text
<PASTE_ORIGINAL_PROMPT_HERE>
```
````

---

## Optional: “tighten my @codex comments” mini-prompt

Use this if you already picked winner(s), but you want Codex to sharpen your PR comments into
maximally actionable instructions.

```text
Rewrite the `@codex` comment set below to be maximally actionable and likely to succeed.

Rules:
- Keep each winner mapped to ONE `@codex` comment in ONE fenced block.
- Do NOT broaden scope beyond the original prompt.
- Convert vague asks into concrete steps.
- Prefer file paths, exact strings to search for, and exact commands to run.
- Keep each comment short, but not underspecified.
- If input comments lack scope constraints, add a “Scope Lock” line:
  - “Only touch: … / Do not touch: … / Keep changes localized.”
- Append the following string verbatim as the last line of EACH `@codex` comment (after any
  other text):
  `new codex task, not a r/e/v/i/e/w task`

Input comments:
- For <PR_URL_1>:
  @codex
  <PASTE_DRAFT_COMMENT_HERE>
- For <PR_URL_2> (optional):
  @codex
  <PASTE_DRAFT_COMMENT_HERE>
```
