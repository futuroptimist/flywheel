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
1) Select the largest safe merge set of candidates (size 1 to 4, but prefer 1 to 2 unless 3+ is clearly safe), where all selected PRs are pairwise compatible and can be merged together without conflicts or contradictions.
2) Briefly justify why each selected PR belongs in the set (tight bullets; evidence-based).
3) Explicitly state why each non-selected PR is not a candidate to move forward with, and classify each reason as either:
   - duplicate of a selected winner, or
   - overlapping/conflicting file edits likely to cause bad merge conflicts.
4) For each selected PR, output one distinct PR comment that begins with `@codex` and contains the concrete remaining work needed to get that PR to "100%" in the context of the selected merge set.

Hard requirements:
- Select ONE OR MORE winners, but only if they are pairwise compatible as a merge set.
- “Compatible” means:
  - no file-level merge conflicts likely from overlapping edits, AND
  - no behavioral contradictions with each other or with the original prompt.
- Treat compatibility as pairwise across the full selected set (every selected PR must be compatible with every other selected PR).
- For every non-selected PR, include a rejection reason tied to either (a) duplicate coverage of winner(s) or (b) overlap/conflict risk with winner file edits.
- If multiple valid sets exist, choose the best set by this priority:
  1) prompt correctness,
  2) compatibility safety,
  3) minimal risk / minimal unrelated churn,
  4) maintainability.
- If no multi-PR set is safe, select exactly ONE best candidate.
- Assume all non-selected candidates will be closed.
- Do not include any candidate with suspicious unrelated churn unless explicitly required by the original prompt.
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
- Read PR description: does it match the original prompt or does it drift?
- Scan the diff: does it touch the right files and update references comprehensively?
- Watch for suspicious churn: broad refactors, mass formatting, unrelated renames, new features.
- Evaluate pairwise compatibility among selected candidates:
  - overlapping hunks in same files,
  - divergent APIs/contracts,
  - contradictory tests/fixtures/docs,
  - duplicate implementation of the same surface in incompatible ways.
- If two candidates solve the same requirement in conflicting ways, keep only the stronger one.
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
  - Per-PR follow-up comments:
    - For <URL_1> (include its own fenced ```text block that starts with `@codex`; if already 100%, output `No follow-up needed.` instead):
      ```text
      @codex
      ...
      ```
    - For <URL_2> (include its own fenced ```text block that starts with `@codex`; if already 100%, output `No follow-up needed.` instead):
      ```text
      @codex
      ...
      ```
    - ...

- In ALL cases (single or multi winner), append:
  - Why each non-selected PR is not a candidate:
    - <URL>: <duplicate of winner(s) OR conflicting/overlapping file edits>; <brief evidence>
    - <URL>: <duplicate of winner(s) OR conflicting/overlapping file edits>; <brief evidence>
    - ...

What “100%” means (prompt-scoped):
- The original prompt’s requirements are satisfied (no more, no less).
- No unrelated behavior changes outside the prompt’s surface area.
- Diffs are intentionally small and localized; broad refactors are split.
- Tests added are minimal + deterministic and directly assert intended behavior.
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
