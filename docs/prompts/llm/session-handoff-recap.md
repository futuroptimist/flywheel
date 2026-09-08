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
Create a self-contained session-handoff recap from the full visible conversation,
accessible attachments, available memory or context, and any relevant read-only
tool results. Do not ask me to restate or summarize the conversation. Produce the
recap directly in your response; do not create a downloadable file or attachment.

Output exactly one outer fenced code block with the `markdown` info string and no
surrounding prose. Use four backticks for that outer fence. Within the recap, use
triple tildes for every nested command, code, log, or prompt block so no nested
content can close the outer fence.

Produce only the recap. Do not continue the underlying task, change files, execute
mutations, spend authorizations, or trigger stateful actions. You may perform
narrowly relevant read-only inspection when tools are available. If current
external state materially affects safe continuation, verify it read-only when
possible. Otherwise preserve the last known state with an explicit as-of marker
and state that fresh verification is required.

Make the recap understandable to an LLM that has no access to this conversation,
prior model memory, hidden state, or tool history. Never rely on phrases such as
“as discussed above,” “the previous output,” or “same as before” without restating
the referenced fact. Summarize redundant chatter and repeated raw logs, but retain
decisions, evidence, failed approaches, corrections, and operationally significant
details. Keep the result thorough enough for lossless continuation without
narrative repetition.

Evidence and state rules:
- Prefer the latest independently verified evidence when messages conflict.
  Record material contradictions and unresolved ambiguity rather than silently
  choosing an unsupported version.
- Clearly distinguish current verified state, historical state, inference,
  provisional work, and facts requiring fresh verification.
- Never fabricate repository state, issue status, commits, branches, paths,
  hashes, commands, authorizations, test results, dates, deployment state, or
  external facts.
- Preserve exact strings when continuation depends on them, including repository
  names and URLs; branches, commits, tags, pull requests, and issues; file and
  evidence paths; artifact identities, hashes, versions, and sizes; environment,
  host, service, timer, deployment, and runtime identities; authorization tokens
  and their exact scope; validated commands and required sentinels; error
  classifications; and acceptance criteria.
- Do not reproduce secrets, credentials, private tokens, or unnecessary raw
  sensitive output. Record only safe identifiers, hashes, sanitized
  classifications, and locations needed for continuation.

Continuation rules:
- Begin the recap with one immediate next task, concrete enough for a fresh model
  to act on without rediscovery. If the next artifact or command is provisional,
  say prominently that it must not be executed and identify the qualification
  still required.
- Include success and failure branches when the next action is one-shot,
  stateful, destructive, authorization-gated, or evidence-producing.
- Distinguish permissions already granted from permissions still required.
  Authorizations are narrow and non-transitive. Identify spent one-shot actions
  that must not be retried.
- Identify files or attachments the next session must receive. Include exact
  filenames and hashes when known. Tell the user to reattach, rather than
  reconstruct, any missing critical artifact.
- For repository work, include related open issues and pull requests that remain
  in scope. Separate genuine implementation work from duplicate, stale,
  superseded, closed, or cleanup-only items, and mark time-sensitive status for
  rechecking.

Ledger rules:
- If a progress ledger exists, reproduce the complete current ledger. Retain all
  stable step identifiers, attempt counts, percentages, statuses, and titles,
  including completed, active, blocked, superseded, and not-started rows. Apply
  only evidence-backed updates, never silently omit older rows, and explicitly
  instruct the next session to propagate the full ledger in every future attempt.
- If no ledger exists, do not invent a large historical ledger. Provide a
  dependency-ordered remaining-work list and only the minimal continuation
  structure needed.

Use the following section order when applicable, omitting only sections that are
genuinely irrelevant while preserving the order of those retained:
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
single immediate task to perform; what must not be rerun or mutated; which ledger
or state record must continue to be propagated; which facts require fresh
read-only verification; and when new explicit authorization is required.
```

## Upgrade Prompt

```text
Improve the Main Prompt above rather than executing it. Preserve its purpose and
zero-edit behavior: it must use the visible conversation and available context
without placeholders, configuration, user substitutions, or a request to restate
the task.

Preserve the response contract requiring one directly copyable inline recap in a
single outer Markdown code block, with no surrounding prose or file attachment.
Also preserve cross-LLM portability, evidence precedence, complete ledger
retention, exact-identity preservation, authorization boundaries, sensitivity
protections, and the requirement to identify one immediate task. Do not overfit
the prompt to any incident, repository, platform, or deployment environment.

Improve clarity, completeness, compaction resistance, and concision without
weakening any safety or evidence requirement.

Return:
1. The complete revised Main Prompt in one fenced `text` block.
2. A brief bullet list of material improvements.

Do not revise the Upgrade Prompt itself unless explicitly asked.
```
