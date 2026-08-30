---
title: 'Multi-Step Progress Ledger Prompt'
slug: 'multi-step-progress-ledger'
conversational: true
---

# Multi-Step Progress Ledger Prompt
Type: evergreen

Paste the copy-ready block directly after any feature request, bug report,
investigation, migration, or deployment request. It uses that preceding request
and the visible conversation as its task, so no editing or duplicated request
text is needed.

## Copy-ready workflow

````text
Manage the request immediately preceding this message, together with all visible
conversation context, as a durable multi-step workflow. Treat that material as
the primary task. Do not ask me to paste or restate it.

Before constructing the workflow, inspect all applicable context available to
you. Decompose the task into the smallest useful dependency-aware sequence.
Include investigation, repository implementation, review/merge, deployment, and
live verification only when applicable; never invent operational stages for a
documentation-only or code-only task. Separate repository work from operational
work and make release and deployment dependencies explicit.

Ledger rules:
- Give every step a stable number and concise stable title. Regenerate the
  complete ledger on every response, including completed, active, blocked,
  superseded, and not-yet-started work, so compaction cannot erase workflow
  state. Use exactly this row format:
  `Step 03 | attempts=2 | estimated_complete=65% | status=in_progress | Qualify the release candidate`
- Use only `not_started`, `in_progress`, `blocked`, `completed`, and
  `superseded`. Normally keep exactly one step `in_progress`. Parallelize only
  independent work when safe and materially useful, and make each separate
  active attempt explicit.
- Start untouched work at `attempts=0` and `estimated_complete=0%`. Increment a
  step to attempt 1 when you first emit a concrete actionable prompt, command
  sequence, or authorized action whose primary target is that step. Increment
  it once for each later concrete diagnostic, implementation, verification, or
  remediation attempt targeting that step. Do not increment for discussion,
  passive waiting, status reporting, or merely receiving results.
- If one action explicitly targets multiple steps, increment every targeted
  step once. Evidence discovered incidentally may change another step's
  percentage without incrementing its attempts; annotate the source
  relationship in the ledger or evidence notes.
- Estimate completion only from verified evidence, not elapsed time,
  confidence, or optimism. Reserve 100% for independently verified acceptance
  criteria. A prompt or PR does not complete repository work. An artifact or a
  successful deployment command does not complete deployment: require the
  applicable readiness, identity, functional, observability, soak, and rollback
  evidence. Never treat skipped, stale, or historical evidence as current
  success.
- A percentage may decrease when evidence proves a regression, invalid
  assumption, or newly required scope; state the evidence-backed reason.
- Preserve IDs and history. Never silently delete a step. Mark obsolete work
  `superseded` and name its replacement. If splitting a step, retain it and use
  stable children such as `Step 04a` and `Step 04b`.
- Identify dependencies and never advance past an unmet gate. Do not repeat a
  successful action merely to gather more evidence unless a named verification
  gap remains.

After I return output from the prior action: (1) validate and classify the
evidence; (2) update attempts, statuses, and percentages; (3) decide whether to
retry or advance; (4) regenerate the entire ledger; and (5) emit exactly one
next action.

Choose that one action from context:
- For new repository work, emit a fresh, self-contained Codex prompt containing
  the repository and base branch when known, objective, scope constraints,
  acceptance criteria, applicable `AGENTS.md` instructions, verification
  commands, and expected final reporting.
- For work on an existing PR, emit one copy-ready comment beginning with
  `@codex` and ending exactly with
  `new codex task, not a r/e/v/i/e/w task`.
- For operator or live-environment work, emit guarded shell commands. Use
  explicit host, context, environment, and target checks; classify read-only
  before mutation; avoid printing secrets; fail closed; report whether cluster,
  repository, or external state changed; capture durable evidence when
  appropriate; and include exact rollback coordinates before any production
  mutation.
- Ask one concise blocking question with clearly distinct options only when a
  missing user decision materially changes the safe next action.

Never fabricate tags, digests, versions, dates, check results, or live state.
Never perform or instruct an unauthorized destructive operation. Choose one
concrete next action, not alternatives.

Response contract:
- During active work, output exactly one fenced code block and no surrounding
  prose. Except for an existing-PR comment, begin the block with the regenerated
  full ledger, then put the single next action immediately after it.
- Use a `bash` fence for shell work and render every ledger and evidence-note
  line as a shell comment before the commands. Use a `text` fence for a fresh
  Codex prompt, with the ledger before the action. For an existing-PR comment,
  use a `text` fence that begins with `@codex`, places the ledger and action
  instructions after that mention, and ends with the required task phrase.
- If blocked on a required decision, use one `text` fence containing the ledger
  followed by the one concise question and its distinct options.
- Continue until every applicable step is `completed` or explicitly
  `superseded`. At final completion, use one `text` fence containing the full
  ledger with every completed step at 100%. Superseded entries must retain
  their status, replacement note, and last evidence-backed percentage. Include
  a compact evidence summary and `WORKFLOW_COMPLETE=true`. Emit no additional
  task prompt.

Generic active-work example (illustrative only):
```text
Step 01 | attempts=2 | estimated_complete=100% | status=completed | Establish acceptance criteria
Step 02 | attempts=1 | estimated_complete=60% | status=in_progress | Implement the change
Step 03 | attempts=0 | estimated_complete=25% | status=blocked | Obtain required authorization
Step 04 | attempts=0 | estimated_complete=0% | status=not_started | Prepare the release
Step 05 | attempts=0 | estimated_complete=100% | status=completed | Verify compatibility
Evidence note: Step 05 completed incidentally from Step 02's multi-step verification; its attempt count remains 0. Step 03 is blocked but is not the current dependency gate.

Repository: example/project
Base branch: main
Objective: Complete Step 02 and verify its acceptance criteria.
Scope: Change only the files required by the preceding request; preserve unrelated behavior.
Acceptance criteria: The requested behavior is implemented and focused checks pass.
Instructions: Read and follow every applicable AGENTS.md before editing. Keep the diff minimal.
Verification: Run the repository's focused tests and required validation commands, then inspect git diff --check and git diff --stat.
Final report: Summarize changed files, evidence, command results, and any exact blockers.
```
The example's Step 02 row already records attempt 1 because the self-contained
Codex prompt immediately following the ledger is the concrete next action that
primarily targets Step 02. Do not copy example repository details into the real
workflow.
````
