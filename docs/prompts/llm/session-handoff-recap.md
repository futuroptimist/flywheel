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
accessible attachments, available memory or context, and any relevant read-only
tool results. Do not ask me to restate or summarize the conversation.

Return the recap directly in your response, not as a downloadable file or
attachment. Emit exactly one outer fenced code block with the `markdown` info
string and no surrounding prose. Delimit that outer block with exactly four
backticks. Use triple tildes for every nested command, code, log, or prompt
block so no nested content can close the outer block.

Produce only the recap. Do not continue the underlying task or mutate any
repository, service, issue, pull request, environment, or other state. You may
perform narrowly relevant read-only inspection when tools are available.

Make the recap understandable without the original conversation, prior model
memory, hidden state, or tool history. Never rely on phrases such as “as
discussed above,” “the previous output,” or “same as before” without restating
the referenced fact. Prefer the latest independently verified evidence when
messages conflict. Record material contradictions or unresolved ambiguity
instead of silently choosing an unsupported version. Clearly distinguish
current verified state, historical state, inference, provisional work, and
facts requiring fresh verification.

Never fabricate repository state, issue status, commits, branches, paths,
hashes, commands, authorizations, test results, dates, deployment state, or
external facts. If current external state can be checked read-only with
available tools and materially affects continuation, verify it. Otherwise,
preserve the last known state with an explicit as-of marker and a requirement
to reverify it.

Preserve exact strings whenever continuation depends on them, including:
- repository names and URLs;
- branches, commits, tags, pull requests, and issues;
- file and evidence paths;
- artifact identities, hashes, versions, and sizes;
- environment, host, service, timer, deployment, and runtime identities;
- authorization tokens and their exact scope;
- validated commands and required sentinels;
- error classifications and acceptance criteria.

Do not reproduce secrets, credentials, private tokens, or unnecessary raw
sensitive output. Record only safe identifiers, hashes, sanitized
classifications, and locations needed for continuation. Summarize redundant
chatter and repeated raw logs while retaining decisions, evidence, failed
approaches, corrections, and operationally significant details.

If a progress ledger exists, reproduce the complete current ledger. Retain all
stable step identifiers, attempt counts, percentages, statuses, and titles,
including completed, active, blocked, superseded, and not-started rows. Apply
only evidence-backed updates, never silently omit older rows, and explicitly
instruct the next session to propagate the full ledger in every future attempt.
If no ledger exists, do not invent a large historical ledger; provide a
dependency-ordered remaining-work list and only the minimal continuation
structure needed.

At the beginning of the recap, identify exactly one immediate next task. Make
it concrete enough for a fresh model to act without rediscovery. If the next
artifact or command is provisional, prominently state that it must not be
executed and identify the qualification that remains. Include success and
failure branches when the next action is one-shot, stateful, destructive,
authorization-gated, or evidence-producing.

Distinguish permissions already granted from permissions still required.
Treat authorizations as narrow and non-transitive, and identify spent one-shot
actions that must not be retried. Identify files or attachments the next
session must receive, including exact filenames and hashes when known. Tell the
user to reattach, rather than reconstruct, any missing critical artifact.

When the thread covers repository work, include related open issues or pull
requests that remain in scope. Separate genuine implementation work from
duplicate, stale, superseded, closed, or cleanup-only items, and mark
time-sensitive status for rechecking.

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

In the final section, explicitly tell the next model what to inspect first; the
single immediate task to perform; what must not be rerun or mutated; which
ledger or state record must continue to be propagated; which facts require
fresh read-only verification; and when new explicit authorization is required.
```

## Upgrade Prompt

```text
Improve the Main Prompt above rather than executing it.

Preserve its purpose as a reusable, zero-edit prompt that derives a portable,
self-contained continuation handoff from the visible conversation and
available context. Preserve its single inline recap code-block response
contract, cross-LLM portability, evidence precedence, full-ledger retention,
exact-identity preservation, authorization boundaries, sensitivity
protections, and requirement for one immediate next task. Do not overfit the
prompt to any particular incident, repository, platform, or deployment
environment.

Improve clarity, completeness, resistance to context compaction, and concision
without weakening any safety or evidence requirement. The upgraded prompt
must remain directly copy/paste-ready without placeholders, configuration,
fill-in fields, or required user edits.

Return:
1. The complete revised Main Prompt in one fenced `text` block.
2. A brief bullet list of the material improvements.

Do not revise the Upgrade Prompt itself unless explicitly asked.
```
