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
accessible attachments, available memory or context, and any relevant read-only tool
results. Do not ask me to restate or summarize anything. Produce the recap directly in
your response; do not create a file or attachment.

Output exactly one outer fenced code block with the `markdown` info string and no
surrounding prose. Use four backticks for that outer delimiter. Within the recap, use
triple tildes for every nested command, code, log, or prompt block so the outer block
remains intact and directly copyable.

Produce only the recap. Do not continue the underlying task or mutate repositories,
services, issues, pull requests, files, deployments, or other state. When tools are
available, narrowly relevant read-only inspection is permitted. The recap must be
understandable without the original conversation, prior model memory, hidden state, or
tool history. Never rely on phrases such as “as discussed above,” “the previous output,”
or “same as before” without restating the referenced fact.

Evidence and state rules:
- Prefer the latest independently verified evidence when messages conflict. Record any
  material contradiction or unresolved ambiguity instead of silently choosing an
  unsupported version.
- Clearly distinguish current verified state, historical state, inference, provisional
  work, and facts requiring fresh verification.
- Never fabricate repository state, issue status, commits, branches, paths, hashes,
  commands, authorizations, test results, dates, deployment state, or external facts.
- If current external state can be checked read-only with available tools and materially
  affects continuation, verify it. Otherwise preserve the last known state with an
  explicit as-of marker and a requirement to reverify it.
- Preserve exact strings when continuation depends on them: repository names and URLs;
  branches, commits, tags, PRs, and issues; file and evidence paths; artifact identities,
  hashes, versions, and sizes; environment, host, service, timer, deployment, and runtime
  identities; authorization tokens and their exact scope; validated commands and required
  sentinels; error classifications; and acceptance criteria.
- Do not reproduce secrets, credentials, private tokens, or unnecessary raw sensitive
  output. Retain only safe identifiers, hashes, sanitized classifications, and locations
  required for continuation.
- Compact redundant chatter and repeated raw logs while retaining decisions, evidence,
  failed approaches, corrections, and operationally significant details.

Continuation rules:
- Put one immediate next task at the beginning of the recap. Make it concrete enough for
  a fresh model to act without rediscovery. If its artifact or command is provisional,
  prominently say it must not be executed and identify the remaining qualification.
- For a one-shot, stateful, destructive, authorization-gated, or evidence-producing next
  action, include explicit success and failure continuation branches.
- Distinguish permissions already granted from permissions still required. Treat every
  authorization as narrow and non-transitive. Identify spent one-shot actions that must
  not be retried.
- Identify files or attachments the next session must receive, including exact filenames
  and hashes when known. Tell the user to reattach, rather than reconstruct, any missing
  critical artifact.
- For repository work, include related open issues and PRs still in scope. Separate
  genuine implementation work from duplicate, stale, superseded, closed, or cleanup-only
  items, and mark time-sensitive status for rechecking.

Ledger rules:
- If a progress ledger exists, reproduce its complete current form. Retain every stable
  step identifier, attempt count, percentage, status, and title, including completed,
  active, blocked, superseded, and not-started rows. Apply only evidence-backed updates,
  never silently omit older rows, and explicitly instruct the next session to propagate
  the full ledger in every future attempt.
- If no ledger exists, do not invent a large historical ledger. Give a dependency-ordered
  remaining-work list and create only the minimal continuation structure needed.

Use the following section order when applicable; omit only sections that genuinely do not
apply, while retaining enough explicit structure for lossless continuation:
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

In the final section, explicitly tell the next model what to inspect first; the single
immediate task to perform; what must not be rerun or mutated; which ledger or state record
must continue to be propagated; which facts require fresh read-only verification; and
when new explicit authorization is required. Keep the recap thorough enough for lossless
continuation without narrative repetition.
```

## Upgrade Prompt

```text
Improve the Main Prompt above; do not execute it. Return (1) the complete revised Main
Prompt in one fenced `text` block and (2) a brief bullet list of material improvements.
Do not revise the Upgrade Prompt itself unless explicitly asked.

Preserve the Main Prompt's purpose and zero-edit behavior, including its single inline
recap code-block response contract. Preserve cross-LLM portability, evidence precedence,
complete-ledger retention, exact-identity preservation, authorization boundaries,
sensitivity protections, and the requirement for one immediate next task. Do not overfit
the revision to any incident, repository, platform, or deployment environment. Improve
clarity, completeness, resistance to context compaction, and concision without weakening
any safety or evidence requirement.
```
