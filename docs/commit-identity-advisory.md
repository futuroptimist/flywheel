# Commit identity advisory

Flywheel provides a dependency-free, warning-only committer metadata checker,
reused from DSPACE. It does not authenticate people, block merges, rewrite history,
or alter repository permissions. Authors are never compared or changed.

## Reuse and trust

The reusable workflow is `.github/workflows/commit-identity-reusable.yml`.
A caller pins both the reusable workflow reference and its `checker_sha` input to
one reviewed, full Flywheel commit SHA. The thin caller in
`.github/workflows/commit-identity.yml` demonstrates this contract. Upgrade both
pins together after reviewing changes; never replace them with a mutable branch.

The bootstrap runs no checkout, PR code, dependency installation, or PR policy.
It fetches the checker from the fixed Flywheel repository at `checker_sha`, and
fetches caller policy from the caller's server-resolved default branch at a full
SHA. Code and policy load into memory. Policy is not fetched for synthetic tests.
The bootstrap uses bounded responses, timeouts, fatal UTF-8 decoding, and rejects
redirects. Supplied pagination URLs are never followed.

A writer can change a push workflow or its pins. This is an advisory, not a
tamper-resistant security boundary. Review workflow and policy changes carefully.
The initial PR cannot load new caller policy from main until it is merged.
A bootstrap coverage warning during rollout does not mean the checker ran.

## Reviewed policy and attribution

`.github/commit-identity-policy.json` uses version 1 and repository-keyed
`committers` entries containing a stable `accountId`, `login`, `nameSha256`, and
`emailSha256`. The Flywheel entry carries forward Daniel's reviewed DSPACE policy.
Digests compare exact UTF-8 strings; hashing minimizes output, not disclosure or
identity authentication. Do not infer an email from a login or membership list.
No relationship between `danielsmith4483` and any email is asserted or configured.

A committer is in scope if its GitHub account ID, raw name digest, or raw email
digest matches a reviewed entry. A conflicting pair or API account ID produces
`COMMITTER_IDENTITY_MISMATCH`. Outside contributors receive neutral
`ATTRIBUTED_COMMITTER_UNREVIEWED`; GitHub-attributed bots receive neutral
`BOT_ATTRIBUTION_UNREVIEWED`. A self-declared bot name grants no exemption, and
bot attribution cannot override a reviewed identity match. Imported authors and
GitHub web-flow attribution remain intact. Null or malformed attribution warns
about coverage. Unrelated incorrect identities cannot be detected by this narrow
comparison; neutral status is not proof of provenance.

## Optional Slack delivery

Delivery defaults to off. Only mismatch categories produce a Slack message,
including `TEST_COMMITTER_IDENTITY_MISMATCH`. Benign controls and coverage warnings
never send Slack messages. At most 20 mismatches are included per run, in one
message; all inspected commits still receive local advisory output. Repeated
push/PR events may notify twice; no durable deduplication or retries are claimed.

An operator may opt in with repository variable `COMMIT_IDENTITY_SLACK_ENABLED`
set to `true`, verified `COMMIT_IDENTITY_SLACK_CHANNEL`, and an existing
`COMMIT_IDENTITY_SLACK_TOKEN` secret able to post to that channel. The reusable
workflow receives only this named optional secret, never `secrets: inherit`.
Do not create or transmit credentials through chat or commit them. This change
creates no secrets and changes no permissions or channel membership.

Slack channel `#github` was resolved and its history read on 2026-10-10:
[C0C81UWJE5B](https://kepler-dqx2375.slack.com/archives/C0C81UWJE5B), created by
Daniel. This verifies the destination, not workflow credential availability or
successful delivery. Repository configuration remains opt-in. Slack requests go
only to `https://slack.com/api/chat.postMessage`, reject redirects, disable markup
and unfurling, and never print response bodies. Delivery requires HTTP success,
`ok: true`, and the matching channel. Failures emit `COVERAGE_SLACK_UNAVAILABLE`;
there is no retry that could duplicate a message after an uncertain outcome.

## Manual test dispatch

The caller exposes `test_case` choices `mismatch` and `benign`, plus `notify`
(default false). Every manual dispatch uses an in-memory mock committer and a
fixed synthetic SHA. No deliberately misattributed Git commit is ever created.
Every synthetic result has a fixed `TEST_` category, including Slack payloads.
A dispatch can send only when both repository opt-in and `notify: true` are set.
The benign case never sends. Other input values produce a fixed coverage warning.
GitHub requires a dispatchable workflow to be present on the default branch;
unmerged code can still be verified with the exact bootstrap mock tests.

## Output and coverage

Output and message text contain only a validated owner/repository, optional full
hexadecimal SHA, and a fixed category. No emails, names, refs, messages, raw API
bodies, or exception text appear in checker output, summaries, or artifacts.
Warning annotations carry the same payload. Keep HTTP/body debugging disabled.
GitHub's platform event storage and unrelated workflows are outside this contract.

PR enumeration checks count, head, and base snapshots before and after pagination;
GitHub's 250-commit PR cap, races, duplicates, and missing heads warn. Ordinary
push comparisons cap at 30 pages/3,000 commits. Force pushes warn about removed
history. New branches inspect only the head; deletions warn without claiming
inspection. Tags are excluded. API errors, malformed data, missing trusted files,
and interrupted steps produce fixed warnings. `COVERAGE_COMMIT_LIST_COMPLETE`
means enumeration completed, not identity verification or absence of mismatches.
GitHub event suppression (including GITHUB_TOKEN pushes), cancellation, disabled
Actions, or runner outages may prevent a run entirely.

Inspect a warned commit privately before correcting future local identity.
Never rewrite history or change permissions based solely on this advisory.

## Verification and rollout gates

Run `node --test tests/commitIdentity*.node.mjs`. Tests use built-in Node modules,
in-memory fixtures, mocked APIs, and captured stdout/stderr. They cover benign
controls, mismatch boundaries, pagination, exact bootstrap execution, malformed
metadata, response and exception sanitization, Slack payloads, and delivery errors.
The separate regression workflow runs these tests against the PR's exact head
without credentials. Passing mocks do not prove live Slack delivery.

Keep the Flywheel PR draft until tests, configured AI feedback, and exact-head CI
are green. No merge or deployment is part of this task. DSPACE keeps its existing
advisory. A separate cleanup PR requires owner merge of the reviewed Flywheel
implementation, a usable immutable pin, green exact-head CI, an observed synthetic
TEST alert in the verified channel, a benign control, and strict privacy schema
verification. Keep DSPACE policy and a thin pinned caller; remove only superseded
duplication. Credential or scope setup remains an owner action.
