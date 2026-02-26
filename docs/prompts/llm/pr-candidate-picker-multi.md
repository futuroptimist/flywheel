---
title: "PR candidate picker (4-way, multi-merge) + per-PR finishing @codex comments"
slug: "pr-candidate-picker-multi"
conversational: true
---

# PR candidate picker (4-way, multi-merge) + per-PR finishing `@codex` comments

Use this when you have **exactly four** competing PR candidates that all claim to implement the same original prompt, but **more than one PR might be safe to merge together**.

This template helps you:

- pick **one or more** mergeable candidates,
- enforce **safe co-merge compatibility** (no merge conflicts, no contradictory behavior), and
- produce **copy/paste-ready `@codex` follow-up comments** for each selected PR.

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
1) Select a safe merge set of candidates (size 1 to 4), where all selected PRs are pairwise compatible and can be merged together without conflicts or contradictions.
   - Prefer the LARGEST safe merge set after prompt correctness: maximize safe co-merge size unless doing so increases conflict/contradiction risk.
   - A PR may be selected as a winner even if it is not yet “100%”, as long as it is merge-safe and prompt-aligned; use its `@codex` comment to enumerate the missing work.
   - Do not penalize a PR for missing bookkeeping/docs/PR-summary formatting/validation-command reporting if those can be added via focused follow-up without broad refactors.
2) Briefly justify why each selected PR belongs in the set (tight bullets; evidence-based).
3) For each selected PR, output one distinct PR comment that begins with `@codex` and contains the concrete remaining work needed to get that PR to "100%" in the context of the selected merge set.
4) For each non-selected PR, explicitly state why it is NOT a merge candidate, using exactly one of these labels plus one concise evidence-based reason (not vibes):
   - `Duplicate of winner`: substantially same solution/value as a selected PR.
   - `Conflict risk`: overlaps files/hunks or behavior in ways likely to cause bad merges.

Hard requirements:
- Select ONE OR MORE winners, but only if they are pairwise compatible as a merge set.
- “Compatible” means:
  - no file-level merge conflicts likely from overlapping edits, AND
  - no behavioral contradictions with each other or with the original prompt.
- Treat compatibility as pairwise across the full selected set (every selected PR must be compatible with every other selected PR).
- If multiple valid sets exist, choose the best set by this priority:
  1) prompt correctness,
  2) compatibility safety,
  3) largest safe merge set,
  4) minimal risk / minimal unrelated churn,
  5) maintainability.
- If no multi-PR set is safe, select exactly ONE best candidate.
- Assume all non-selected candidates will be closed.
- Do not include any candidate with suspicious unrelated churn unless explicitly required by the original prompt.
- Only exclude a PR when the risk is structural (merge conflicts or behavioral contradictions), not because it is missing finishable checklist/bookkeeping work.
- Every selected PR must include its own `@codex` comment (distinct and scoped to that PR).
- Append the following string verbatim as the last line of EACH `@codex` comment (after any other text):
  `new codex task, not a r/e/v/i/e/w task`
- Start EACH `@codex` comment with a Scope Lock recap (use provided Scope Lock if filled; otherwise state “No scope lock provided” and proceed):
  - “Only touch X/Y/Z; do not touch A/B/C; keep diff small; run these commands.”
- Include a diff sanity check in EACH `@codex` comment:
  - “If `git diff --stat` shows > <max files> or touches do-not-touch areas, stop and split.”

Optimization order:
correctness > prompt-alignment > minimal-risk changes > maintainability > style

How to evaluate candidates:
Pass A — merge-blocker scan (pairwise across all candidates):
- Identify likely merge conflicts from overlapping files/hunks.
- Identify behavioral contradictions with the original prompt or between PRs.
- Identify suspicious unrelated churn that would make co-merge risky.

Pass B — finishable-gap scan (for candidates that passed Pass A):
- Capture missing but fixable work in per-PR `@codex` comments instead of excluding the PR.
- Typical fixable gaps: missing bookkeeping updates, missing PR summary formatting, missing doc sync with limited churn, missing validation-command reporting.
- If a required bookkeeping/doc file would collide across winners, assign that shared file to exactly one PR and instruct other PRs: “do not touch shared file; handled by PR X”.

- Read PR description: does it match the original prompt or does it drift?
- Scan the diff: does it touch the right files and update references comprehensively?
- Watch for suspicious churn: broad refactors, mass formatting, unrelated renames, new features.
- Evaluate pairwise compatibility among selected candidates:
  - overlapping hunks in same files,
  - divergent APIs/contracts,
  - contradictory tests/fixtures/docs,
  - duplicate implementation of the same surface in incompatible ways.
- If two candidates solve the same requirement in conflicting ways, keep only the stronger one.
- When multiple PRs are merge-safe and collectively cover more of the prompt, select all of them, then distribute remaining work across their `@codex` comments to avoid overlapping edits.
- Prefer localized changes on the bug surface; penalize unrelated features/refactors/non-required tests.
- Prefer regression tests that directly assert user-visible behavior.
- If tests are flaky, fix the root cause rather than loosening assertions.
- Check durability: tests/fixtures/docs updated so the change won’t regress.
- Prefer “complete + boring” over “clever + risky”.

Scope Lock (fill in if you care; otherwise leave blank)
- Allowed files/paths:
  - <optional list>
- Do NOT touch:
  - <optional list>
- Max files changed (default 8): <optional number>

Enforcement rules:
- Strongly prefer candidates that stay within scope.
- If a selected PR exceeds scope, its `@codex` comment MUST:
  (a) shrink scope back to the prompt, and
  (b) explicitly defer unrelated changes to a follow-up PR.

Output format rules:
- If exactly ONE candidate is selected, output exactly:
  - Winner: <URL>
  - Why this one:
    - <bullet>
    - <bullet>
  - Why others were not selected:
    - <URL>: <<one allowed label>> — <one concise evidence-based reason>
    - <URL>: <<one allowed label>> — <one concise evidence-based reason>
    - <URL>: <<one allowed label>> — <one concise evidence-based reason>
  - `@codex` comment:
    ```text
    @codex
    ...
    ```

- If MORE THAN ONE candidate is selected, output exactly:
  - Winners:
    - <URL_1>
    - <URL_2>
    - ...
  - Why this merge set is safe:
    - <bullet about non-conflicting file/edit surfaces>
    - <bullet about non-contradictory behavior>
    - <bullet about prompt coverage>
  - Why others were not selected:
    - If all 4 candidates are selected, output `None`.
    - Otherwise, for each non-selected candidate:
      - <URL>: <<one allowed label>> — <one concise evidence-based reason>
  - Per-PR follow-up comments:
    - For <URL_1> (include its own fenced ```text block that starts with `@codex`; if already 100%, output `No follow-up needed.` instead):
      ```text
      @codex
      Merge blockers (must fix before merge):
      - ...
      Post-merge acceptable follow-ups (only truly optional):
      - ...
      ...
      ```
    - For <URL_2> (include its own fenced ```text block that starts with `@codex`; if already 100%, output `No follow-up needed.` instead):
      ```text
      @codex
      Merge blockers (must fix before merge):
      - ...
      Post-merge acceptable follow-ups (only truly optional):
      - ...
      ...
      ```
    - ...

What “100%” means (prompt-scoped):
- The original prompt’s requirements are satisfied (no more, no less).
- No unrelated behavior changes outside the prompt’s surface area.
- Diffs are intentionally small and localized; broad refactors are split.
- Tests added are minimal + deterministic and directly assert intended behavior.
- Verification steps are included and plausibly pass.
- If a PR is merge-safe but incomplete, keep it in winners and put required missing work in its `@codex` comment; default is to fix required items within the PR, not defer to post-merge.
- Explicitly separate each follow-up comment into:
  - `Merge blockers` (must be completed before merge), and
  - `Post-merge acceptable follow-ups` (only for truly optional items).

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

## Optional: “tighten my per-PR @codex comments” mini-prompt

Use this after selecting one or more winners if you want Codex to sharpen each follow-up comment.

```text
Rewrite each `@codex` comment below to be maximally actionable and likely to succeed.

Rules:
- Preserve one separate `@codex` comment per PR (do not merge them).
- Do NOT broaden scope beyond the original prompt.
- Convert vague asks into concrete steps.
- Prefer file paths, exact strings to search for, and exact commands to run.
- Keep each comment short, but not underspecified.
- If a comment lacks scope constraints, add a “Scope Lock” line:
  - “Only touch: … / Do not touch: … / Keep changes localized.”
- Append the following string verbatim as the last line of EACH `@codex` comment:
  `new codex task, not a r/e/v/i/e/w task`

Input comments:
- <PR_URL_1>
  @codex
  <PASTE_DRAFT_COMMENT_HERE>
- <PR_URL_2>
  @codex
  <PASTE_DRAFT_COMMENT_HERE>
```
