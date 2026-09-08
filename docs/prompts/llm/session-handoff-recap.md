---
title: 'Session Handoff Recap Prompt'
slug: 'session-handoff-recap'
conversational: true
---

# Session Handoff Recap Prompt
Type: evergreen

This prompt creates a portable continuation handoff from the visible conversation.

## Main Prompt

```text
Create a lossless session-handoff recap from the full visible conversation,
accessible attachments, available context, and relevant read-only tool results.
Do not ask me to restate the conversation.

Return the recap directly in your response, not as a downloadable file or
attachment. Emit exactly one outer fenced code block with the `markdown` info
string and no surrounding prose. Delimit that outer block with exactly four
backticks. Use triple tildes for every nested command, code, log, or prompt
block so no nested content can close the outer block.

Produce only the recap; do not continue the task or mutate any state. Narrowly
relevant read-only inspection is allowed. Make the recap understandable without
the original conversation, hidden state, or tool history, and restate rather
than indirectly reference prior facts.

Prefer the latest independently verified evidence. Distinguish verified,
historical, inferred, provisional, conflicting, and stale information. Never
invent state, identities, commands, permissions, results, dates, or external
facts. Verify material current state read-only when possible; otherwise record
the last known state, its as-of date, and the need to reverify it.

Preserve exact continuation-critical repository and artifact names, URLs,
branches, commits, tags, issue/PR identifiers, paths, hashes, versions, sizes,
environment, host, service, timer, deployment, and runtime identities,
validated commands, sentinels, error classifications, and acceptance criteria.
Preserve verbatim non-secret user approval markers, authorization grants, their
exact scope and limits, and consumed or remaining one-shot status. These are
authorization evidence, not bearer, API, OAuth, session, or other credential
values, which must never be reproduced. Sensitivity protections override
exact-string, command, and ledger preservation: exclude embedded secrets while
preserving safe surrounding evidence. Exclude unnecessary sensitive output;
retain only safe identifiers, hashes, sanitized classifications, and locations.
Condense repeated chatter and logs without losing decisions, evidence,
failures, corrections, or operational details.

If a progress ledger exists, reproduce every row and its stable ID, attempt
count, percentage, status, and title, including completed, active, blocked,
superseded, and not-started work. Make only evidence-backed updates and require
future sessions to propagate the full ledger. Otherwise, create only a
dependency-ordered remaining-work list.

Immediately after the title and handoff/as-of date, identify exactly one
concrete next task. Mark any provisional action as not executable and state its
missing qualification. For one-shot, stateful, destructive,
authorization-gated, or evidence-producing actions, include success and failure
branches. Separate granted from required permissions; authorizations are narrow
and non-transitive, and spent one-shot actions must not be retried.

List required files or attachments with exact names and hashes when known; ask
the user to reattach, not reconstruct, missing critical artifacts. For
repository work, include in-scope issues and PRs, distinguishing active work
from duplicate, stale, superseded, closed, or cleanup-only items and marking
time-sensitive state for rechecking.

Keep the recap thorough enough for lossless continuation without narrative
repetition. Use the following section order when applicable, omitting only
sections that genuinely have no relevant content:
1. Title and handoff/as-of date
2. Immediate next task
3. Objective and scope
4. Current verified state
5. Completed work and chronology
6. Decisions, contracts, and invariants
7. Attempts, failures, classifications, and lessons
8. Exact identities and evidence anchors
9. Canonical progress ledger, if one exists
10. Remaining work in dependency order
11. Authorization and safety boundaries
12. Success and failure continuation branches
13. Relevant repository issue and PR backlog
14. Risks, unknowns, stale facts, and required reverification
15. Files or attachments required by the next session
16. New-session operating instructions

In the final section, state what to inspect first, the one immediate task, what
must not be rerun or mutated, which ledger or state must be propagated, what
needs fresh read-only verification, and when new authorization is required.
```

## Upgrade Prompt

```text
Improve the Main Prompt above rather than executing it.

Preserve its reusable, zero-edit, self-contained handoff purpose; single inline
recap block; cross-LLM portability; evidence precedence; full-ledger retention;
safe exact identities; verbatim non-secret approval markers, authorization
grants, their exact scope and limits, and consumed or remaining one-shot status;
the distinction between that evidence and prohibited credential values; the
precedence of sensitivity protections over exact-string, command, and ledger
preservation; and one immediate next task. Do not overfit it to an incident or
environment.

Improve clarity, completeness, compaction resistance, and concision without
weakening safety or evidence rules. Keep it copy/paste-ready without
placeholders, configuration, or user edits.

Return:
1. The complete revised Main Prompt in one fenced `text` block.
2. A brief bullet list of the material improvements.

Do not revise the Upgrade Prompt itself unless explicitly asked.
```
