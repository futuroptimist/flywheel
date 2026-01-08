---
title: "PR candidate picker (4-way) + finishing @codex comment"
slug: "pr-candidate-picker"
conversational: true
---

# PR candidate picker (4-way) + finishing `@codex` comment

Use this when you have **exactly four** competing PR candidates that all claim to implement the same original prompt, and you need to:

- pick **exactly one** winner (no ties), and
- produce a **copy/paste-ready `@codex` PR comment** that gets the winner to “100%”.

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
1) Pick exactly ONE winning PR (no ties).
2) Briefly justify why it’s the best match to the original prompt (tight bullets; evidence-based).
3) If the winner is not already “100%”, output a single PR comment that begins with `@codex` and contains the concrete remaining work needed to get it to “100%”.

Hard requirements:
- Choose exactly ONE winner. Do not suggest merging PRs together.
- Assume the other 3 PRs will be closed.
- Prefer the PR that best matches the original prompt with the least scope creep / least risky churn.
- If none are perfect, still pick the least-bad one and make the `@codex` comment close the gap.
- The `@codex` comment must be actionable:
  - name specific files/paths when possible,
  - include specific search commands when you’re not sure where the last stragglers are,
  - include verification commands (tests, lint, a specific CLI invocation, etc.).
- The `@codex` comment must begin with a Scope Lock recap if provided:
  - “Only touch X/Y/Z; do not touch A/B/C; keep diff small; run these commands.”

Optimization order:
correctness > prompt-alignment > minimal-risk changes > maintainability > style

How to evaluate candidates:
- Read PR description: does it match the original prompt or does it drift?
- Scan the diff: does it touch the right files and update references comprehensively?
- Prefer PRs that touch fewer files and stay localized to the bug surface.
- If a candidate touches unrelated areas (new features, unrelated tests, refactors), treat that as
  suspicious churn and downgrade it unless the original prompt explicitly requires it.
- Watch for suspicious churn: big refactors, mass formatting, unrelated renames, new features.
- Check durability: tests/fixtures/docs updated so the change won’t regress.
- Test quality guardrail: prefer regression tests that assert the user-visible contract directly.
  Avoid brittle heuristics unless the prompt explicitly asks for them. If tests are flaky, fix the
  layout cause rather than loosening tests.
- Prefer “complete + boring” over “clever + risky”.

What “100%” means (prompt-scoped):
- The original prompt’s requirements are satisfied (no more, no less).
- No unrelated behavior changes outside the prompt’s surface area.
- Diffs are intentionally small and localized; broad refactors must be split into a follow-up PR.
- Tests added are minimal + deterministic and directly assert the intended contract.
- Verification steps are included and plausibly pass.

Scope Lock (fill in if you care; otherwise leave blank)
- Allowed files/paths:
  - <optional list>
- Do NOT touch:
  - <optional list>
- Max files changed (default 8): <optional number>

Enforcement rules:
- Strongly prefer candidates that stay within scope.
- If the best candidate exceeds scope, still pick the least-bad one but the @codex comment MUST:
  (a) shrink scope back to the prompt, and
  (b) explicitly defer unrelated changes to a follow-up PR.

Output format (must be exactly this structure):
- Winner: <URL>
- Why this one:
  - <bullet>
  - <bullet>
- `@codex` comment:
  ```text
  @codex
  ...
  ```

Diff sanity check for the @codex comment:
- If `git diff --stat` shows > <max files> or touches do-not-touch areas, stop and split.

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

## Optional: “tighten my @codex comment” mini-prompt

Use this if you already picked a winner, but you want Codex to sharpen your PR comment into something maximally actionable.

```text
Rewrite the `@codex` comment below to be maximally actionable and likely to succeed.

Rules:
- Keep it as ONE `@codex` comment in ONE fenced block.
- Do NOT broaden scope beyond the original prompt.
- Convert vague asks into concrete steps.
- Prefer file paths, exact strings to search for, and exact commands to run.
- Keep it short, but not underspecified.
- If the input comment lacks scope constraints, add a “Scope Lock” line:
  - “Only touch: … / Do not touch: … / Keep changes localized.”

Input `@codex` comment:
@codex
<PASTE_DRAFT_COMMENT_HERE>
```
