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
Create a self-contained session-handoff recap from the full conversation visible
to you, accessible attachments, available memory or context, and relevant
read-only tool results. Do not ask me to restate or summarize the conversation.

Return the recap directly in your response, not as a file or attachment. Emit
exactly one outer fenced code block with the `markdown` info string and no prose
before or after it. Delimit that outer block with exactly four consecutive
backtick characters. Use triple tildes for every nested command, code, log, or
prompt block so none can terminate the outer block.

Produce only the recap. Do not continue the underlying task, change files,
update remote state, execute stateful actions, or perform any other mutation.
When tools are available, narrowly relevant read-only inspection is permitted.
If current external state materially affects safe continuation, verify it with
read-only tools. Otherwise preserve the last known state, label it with an
explicit as-of date or time when known, and require fresh verification.

Write for a new LLM that has no access to the original conversation, prior model
memory, hidden state, or tool history. Restate every fact needed to continue;
never depend on phrases such as “as discussed above,” “the previous output,” or
“same as before.” Prefer the latest independently verified evidence when
messages conflict. Record material contradictions and unresolved ambiguity
instead of silently selecting an unsupported account. Clearly distinguish:
- current verified state;
- historical state;
- inference;
- provisional work; and
- facts that require fresh verification.

Never fabricate repository state, issue or pull-request status, commits,
branches, paths, hashes, commands, authorizations, test results, dates,
deployment state, or external facts. Preserve exact strings whenever
continuation depends on them, including:
- repository names and URLs;
- branches, commits, tags, pull requests, and issues;
- file and evidence paths;
- artifact identities, hashes, versions, and sizes;
- environment, host, service, timer, deployment, and runtime identities;
- authorization tokens and their exact scope;
- validated commands and required sentinels; and
- error classifications and acceptance criteria.

Do not reproduce secrets, credentials, private tokens, or unnecessary raw
sensitive output. Record only safe identifiers, hashes, sanitized
classifications, and locations required for continuation. Summarize redundant
chatter and repeated raw logs while retaining decisions, evidence, failed
approaches, corrections, and operationally significant details.

Begin the recap with one immediate next task. Make it concrete enough that the
new model can act without rediscovery. If its next artifact or command is
provisional, state prominently that it MUST NOT be executed and name the
qualification still required. For any one-shot, stateful, destructive,
authorization-gated, or evidence-producing next action, include both success
and failure continuation branches.

Distinguish permissions already granted from those still required.
Authorizations are narrow and non-transitive. Identify spent one-shot actions
that must not be retried, and require new explicit authorization whenever the
next mutation falls outside an existing grant.

Identify every file or attachment the next session must receive. Include exact
filenames and hashes when known. If a critical artifact is unavailable, tell
the user to reattach it rather than reconstructing it.

When the conversation covers repository work, include related open issues and
pull requests that remain in scope. Separate genuine implementation work from
duplicate, stale, superseded, closed, or cleanup-only items. Mark time-sensitive
status for read-only rechecking.

If a progress ledger exists, reproduce its complete current form. Retain all
stable step identifiers, attempt counts, percentages, statuses, and titles,
including completed, active, blocked, superseded, and not-started rows. Apply
only evidence-backed updates, never silently omit older rows, and explicitly
instruct the next session to propagate the full ledger on every future attempt.
If no ledger exists, do not invent a large historical ledger. Instead provide a
dependency-ordered remaining-work list and only the minimal continuation
structure needed.

Keep the recap thorough enough for lossless continuation without narrative
repetition. Use the following section order, omitting a section only when it is
truly inapplicable:
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

In “New-session operating instructions,” explicitly state what to inspect first,
the single immediate task to perform, what must not be rerun or mutated, which
ledger or state record must continue to be propagated, which facts require
fresh read-only verification, and when new explicit authorization is required.
```

## Upgrade Prompt

```text
Improve the Main Prompt above; do not execute it.

Preserve its purpose as a reusable, zero-edit session-handoff prompt and its
cross-LLM portability. Preserve the contract that executing the Main Prompt
returns the recap inline as exactly one outer Markdown code block with no
surrounding prose. Also preserve evidence precedence, complete ledger retention,
exact-identity preservation, authorization boundaries, sensitivity protections,
and the requirement to identify one immediate next task.

Do not overfit the revision to any particular incident, repository, platform,
or deployment environment. Improve clarity, completeness, resistance to context
compaction, and concision without weakening any safety or evidence requirement.

Respond with:
1. the complete revised Main Prompt in exactly one fenced `text` block; and
2. a brief bullet list of material improvements.

Do not revise the Upgrade Prompt itself unless explicitly asked.
```
