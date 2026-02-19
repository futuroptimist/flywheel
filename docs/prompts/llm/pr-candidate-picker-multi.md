---
title: "PR candidate picker (4-way, multi-merge) + finishing @codex comments"
slug: "pr-candidate-picker-multi"
conversational: true
---

# PR candidate picker (4-way, multi-merge) + finishing `@codex` comments

Use this when you have **exactly four** competing PR candidates that all claim
to implement the same original prompt, and you need to:

- pick the **largest safe mergeable subset** (size 1-4), and
- produce **copy/paste-ready `@codex` PR comments** to get each selected PR to
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
1) Determine which PRs can be merged together safely:
   - no merge conflicts,
   - no contradictory behavior/spec changes,
   - no duplicate/cherry-pick overlap that would break clean merge sequencing.
2) Pick the LARGEST safe mergeable set (size 1-4).
3) If size is 1, pick the single best PR as usual.
4) For each selected PR that is not already “100%”, output a distinct follow-up
   PR comment beginning with `@codex` with concrete remaining work.

Hard requirements:
- The selected set must be pairwise and jointly compatible (conflict-safe and
  behavior-consistent).
- Maximize cardinality first (prefer 2 compatible PRs over 1, 3 over 2, etc.).
- If multiple sets have same size, choose the one with best prompt alignment and
  lowest risk/scope creep.
- If only one PR is safely mergeable, output exactly one winner URL and one
  follow-up `@codex` comment (usual flow).
- If more than one PR is safely mergeable, output each selected PR URL and its
  own distinct follow-up `@codex` comment, each wrapped in a fenced code block.
- For any unselected PRs, briefly state why they were excluded (conflict,
  contradiction, drift, risky churn, etc.).
- Each `@codex` comment must be actionable:
  - name specific files/paths when possible,
  - include specific search commands when you’re not sure where the last
    stragglers are,
  - include verification commands (tests, lint, specific CLI invocation, etc.).
- Append the following string verbatim as the last line of EACH `@codex`
  comment (after any other text):
  `new codex task, not a r/e/v/i/e/w task`
- Start EACH `@codex` comment with a Scope Lock recap (use provided Scope Lock
  if filled; otherwise state “No scope lock provided” and proceed):
  - “Only touch X/Y/Z; do not touch A/B/C; keep diff small; run these commands.”
- Include a diff sanity check in EACH `@codex` comment:
  - “If `git diff --stat` shows > <max files> or touches do-not-touch areas,
    stop and split.”

Optimization order:
compatibility/safety > correctness > prompt-alignment > minimal-risk changes >
maintainability > style

How to evaluate candidates:
- Read PR description: does it match the original prompt or drift?
- Scan diff overlap across candidates: files, hunks, and semantic intent.
- Detect conflict risk:
  - same lines/functions edited differently,
  - incompatible migrations/config changes,
  - mutually exclusive API/interface assumptions.
- Detect contradiction risk:
  - opposing product behavior,
  - incompatible tests asserting different contracts,
  - one PR undoing assumptions introduced by another.
- Watch for suspicious churn: big refactors, mass formatting, unrelated renames,
  new features.
- Prefer PRs touching fewer files and localized bug surfaces.
- Prefer regression tests that directly assert user-visible contract.
- Check durability: tests/fixtures/docs updated to prevent regressions.
- Prefer “complete + boring” over “clever + risky”.

Scope Lock (fill in if you care; otherwise leave blank)
- Allowed files/paths:
  - <optional list>
- Do NOT touch:
  - <optional list>
- Max files changed (default 8): <optional number>

Enforcement rules:
- Strongly prefer candidates that stay within scope.
- If a selected candidate exceeds scope, still include it only if needed for the
  largest safe set, and in that PR’s `@codex` comment MUST:
  (a) shrink scope back to the prompt, and
  (b) explicitly defer unrelated changes to a follow-up PR.

Output format (must be exactly this structure):
- Selected PRs (merge order):
  1. <URL>
  2. <URL> (optional)
  3. <URL> (optional)
  4. <URL> (optional)
- Why this set:
  - <bullet>
  - <bullet>
- Excluded PRs:
  - <URL>: <short reason>
  - <URL>: <short reason>
- Follow-up comments:
  - <URL_1>:
    ```text
    @codex
    ...
    ```
  - <URL_2> (if selected):
    ```text
    @codex
    ...
    ```

Additional formatting rule:
- If exactly one PR is selected, you may label it as:
  - Winner: <URL>
  instead of listing multiple selected PRs.

What “100%” means (prompt-scoped):
- The original prompt’s requirements are satisfied (no more, no less).
- No unrelated behavior changes outside the prompt’s surface area.
- Diffs are intentionally small and localized; broad refactors must be split
  into follow-up PRs.
- Tests added are minimal + deterministic and directly assert intended contract.
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

## Optional: compatibility matrix helper mini-prompt

Use this if you want the model to explicitly reason about pairwise compatibility
before deciding the final merge set.

```text
Given 4 candidate PRs for the same prompt, build a 4x4 compatibility matrix.

For each pair (A, B), classify as:
- Compatible
- Merge-conflict risk
- Behavioral contradiction
- Redundant overlap

Then propose the largest compatible merge set (size 1-4), with a merge order,
and explain why alternatives were rejected.

Keep reasoning concise and evidence-based (file overlap, behavior, tests, scope).
```
