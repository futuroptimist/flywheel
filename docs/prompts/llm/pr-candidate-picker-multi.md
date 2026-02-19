---
title: "PR candidate picker (4-way, multi-merge) + finishing @codex comments"
slug: "pr-candidate-picker-multi"
conversational: true
---

# PR candidate picker (4-way, multi-merge) + finishing `@codex` comments

Use this when you have **exactly four** competing PR candidates that all claim to
implement the same original prompt, and you need to:

- pick **one or more** mergeable winners, and
- produce **copy/paste-ready `@codex` PR comments** that get each selected PR to
  “100%”.

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
1) Determine the largest safe subset of PRs that can be merged together with no
   merge conflicts and no behavioral contradictions.
2) If only one PR is safely mergeable, pick the single best PR.
3) Briefly justify your selection decisions (tight bullets; evidence-based).
4) For each selected PR that is not already “100%”, output one PR comment that
   begins with `@codex` and contains the concrete remaining work needed.

Hard requirements:
- You may pick 1, 2, 3, or 4 winners, but ONLY if all selected winners are pairwise
  merge-compatible:
  - no overlapping/conflicting edits that would cause merge conflicts,
  - no contradictory behavior, API, schema, or test expectations.
- If safe multi-merge is not possible, choose exactly ONE winner.
- Prefer the maximal safe set; if multiple sets are equally safe, choose the set with
  the best prompt alignment and lowest risk.
- If none are perfect, still choose the least-bad safe option(s) and use `@codex`
  comment(s) to close gaps.
- Each `@codex` comment must be actionable:
  - name specific files/paths when possible,
  - include specific search commands when you’re not sure where the last stragglers are,
  - include verification commands (tests, lint, a specific CLI invocation, etc.).
- Append the following string verbatim as the last line of EVERY `@codex` comment
  (after any other text):
  `new codex task, not a r/e/v/i/e/w task`
- Start every `@codex` comment with a Scope Lock recap (use provided Scope Lock if
  filled; otherwise state “No scope lock provided” and proceed):
  - “Only touch X/Y/Z; do not touch A/B/C; keep diff small; run these commands.”
- Include a diff sanity check in every `@codex` comment:
  - “If `git diff --stat` shows > <max files> or touches do-not-touch areas, stop and split.”

Optimization order:
correctness > prompt-alignment > merge-compatibility > minimal-risk changes > maintainability > style

How to evaluate candidates:
- Read PR description: does it match the original prompt or does it drift?
- Scan each diff: does it touch the right files and update references comprehensively?
- Build a compatibility matrix across candidates:
  - file overlap and likely textual merge conflicts,
  - semantic contradictions (different behavior for same surface area),
  - test incompatibilities (one PR invalidates another PR’s expected outputs).
- Watch for suspicious churn: big refactors, mass formatting, unrelated renames, new features.
- If a candidate touches unrelated areas (new features, unrelated tests, refactors),
  treat that as suspicious churn and downgrade it unless the original prompt explicitly requires it.
- Prefer PRs that touch fewer files and are localized to the bug surface; penalize
  new features, unrelated refactors, or non-required tests.
- Prefer regression tests that assert the user-visible contract directly; avoid
  brittle heuristics (e.g., scanning DOM for “widest element”, visualViewport math
  hacks) unless explicitly requested.
- If tests are flaky, fix the layout/cause rather than loosening tests.
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
- If selected candidates exceed scope, @codex comment(s) MUST:
  (a) shrink scope back to the prompt, and
  (b) explicitly defer unrelated changes to follow-up PR(s).

Output format (must be exactly this structure):
- Merge decision: <"single" or "multi">
- Selected PR(s):
  - <URL>
  - <URL>  (include one or more)
- Why these:
  - <bullet>
  - <bullet>
- Compatibility check:
  - <bullet about conflict safety>
  - <bullet about non-contradiction>
- Follow-up `@codex` comment(s):
  - <URL_1>
    ```text
    @codex
    ...
    ```
  - <URL_2>
    ```text
    @codex
    ...
    ```
  - <repeat for each selected PR that needs follow-up>

Formatting notes:
- If exactly one PR is selected, still use the same structure with one URL.
- If a selected PR is already 100%, write: `No follow-up needed.` instead of a code block.
- If multiple PRs are selected, each selected PR must have its own distinct
  follow-up block (or explicit “No follow-up needed.” line).

What “100%” means (prompt-scoped):
- The original prompt’s requirements are satisfied (no more, no less).
- No unrelated behavior changes outside the prompt’s surface area.
- Diffs are intentionally small and localized; broad refactors must be split into a follow-up PR.
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

Use this if you already selected one or more winners, but you want Codex to
sharpen your follow-up comments into something maximally actionable.

```text
Rewrite the follow-up content below to be maximally actionable and likely to succeed.

Rules:
- Keep one distinct `@codex` comment per selected PR.
- Output each comment in its own fenced block.
- Do NOT broaden scope beyond the original prompt.
- Convert vague asks into concrete steps.
- Prefer file paths, exact strings to search for, and exact commands to run.
- Keep each comment short, but not underspecified.
- If a comment lacks scope constraints, add a “Scope Lock” line:
  - “Only touch: … / Do not touch: … / Keep changes localized.”
- Append the following string verbatim as the last line of EACH `@codex` comment
  (after any other text):
  `new codex task, not a r/e/v/i/e/w task`

Input follow-up comments:
<PASTE_DRAFT_MULTI_COMMENT_SET_HERE>
```
