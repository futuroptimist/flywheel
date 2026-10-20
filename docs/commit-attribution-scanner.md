# Central commit attribution scanner (K332)

This warning-only library prospectively inspects GitHub commit metadata for
accessible repositories owned by the stable owner ID in
`.github/commit-attribution-scan.json`, plus its explicit additional repository.
It is inactive: no workflow, schedule, Slack delivery, enforcement, repair,
credential changes, historical audit, or history rewriting is introduced.
Existing advisory workflows, pins and DSPACE duplication are preserved.

## Identity policy

The scanner calls the existing `commit-identity.mjs` classifier independently for
the author and committer. It reuses only the reviewed digests and stable account
ID from the configured repository in `.github/commit-identity-policy.json`.
These are identity anchors across the selected inventory, not a requirement that
all contributors use that identity. No new name, email or login mapping is inferred.
The configured obsolete account ID produces a separate role-specific warning,
including when the raw identity is unrelated to the reviewed mapping.

Coherent reviewed identities remain neutral; conflicting reviewed anchors warn.
External authors and committers, API-attributed bots and web-flow identities remain
neutral unless they conflict with a reviewed anchor or obsolete ID. Shared names
and emails prefer a coherent reviewed identity, independent of entry ordering.
Null attribution and malformed metadata report coverage limitations. Attribution
is neither authentication nor proof of intent. Authors are never changed.

## Prospective coverage

Inventory uses paginated authenticated repository metadata and selects by stable
owner ID, not login spelling. Repository IDs key checkpoints; repository ID plus
SHA deduplicates observations across branches and open PRs. Renames retain state.
Explicit additional repositories resolve through their canonical API metadata.
Their mutable lookup names are excluded from the identity-policy fingerprint:
updating a configured name after a rename retains that repository ID's checkpoint.
If the name instead resolves to a different ID, that ID receives its own unscanned
baseline; the old ID's state is retained with an access-gap warning.
The token's visibility is always reported as limited: invisible private
repositories cannot be discovered or counted by this scanner. Previously visible
repositories that disappear retain their state and report an access gap.

On first observation of a repository, current branch and open-PR heads become an
explicitly **unscanned** baseline. No historical commit walk occurs. Subsequent
stable, fast-forward head changes compare immutable old and new SHAs with paginated
metadata. Newly observed refs in an already baselined repository inspect only their
head and report `COVERAGE_NEW_REF`; their earlier history remains unscanned.
Closed PRs and deleted branches report `COVERAGE_DELETED_REF`. Refs created and
deleted entirely between observations cannot be detected.

Branch and PR snapshots are checked before and after inspection, including PR
base SHAs. A changed base, changed snapshot, incomplete comparison, malformed
commit, force push or per-repository API failure retains that repository's prior
checkpoint. Independent repositories can still progress. Force pushes and
changed bases require private investigation; this implementation does not silently
rebaseline them or claim to inspect removed commits. Repeated warnings are expected
until the cause is resolved or an operator explicitly accepts a new unscanned baseline.

Pagination uses locally generated page numbers, never API-supplied URLs. Duplicate
keys, inconsistent counts, missing comparison heads, empty nonterminal pages and
page caps report gaps. A full terminal page requires an additional sentinel read.
Inventory is repeated before saving; changes discard the proposed update. GitHub
does not provide an atomic snapshot: stable snapshots cannot rule out an ABA race,
an unseen pagination omission, or changes immediately after the final read.
`COVERAGE_OBSERVED_RANGE_COMPLETE` only describes a repository's observed ranges;
it does not claim historical, inventory-wide, or durable checkpoint completeness.
Checkpoint saving can still fail after this category. Any warnings remain material.

## Private checkpoints and public output

Public output is a fixed category per line, optionally prefixed `::warning::`.
It contains no names, emails, logins, repository identifiers, refs, SHAs, API
bodies, exception messages or stacks. Never enable HTTP debug logging or publish
checkpoints, raw API responses, or private investigation notes as artifacts.
There is no notification or delivery adapter in this scanner.

The JSON checkpoint contains repository IDs, refs, head/base SHAs, inspected SHAs,
an identity-policy fingerprint and an explicit `historical: "unscanned"` marker.
The fingerprint canonicalizes the effective account-ID/name-digest/email-digest
triples and obsolete-account set. Entry ordering and mutable login labels do not
invalidate state; an effective identity-policy change still fails closed.
Treat the entire file as private. `privateCheckpoint(path)` requires a dedicated,
existing, owner-only POSIX directory (0700), outside Git checkouts, with no symlink
ancestors. It rejects nonprivate files, symlinks, hard links and oversized state.
Every ancestor must be owned by the current user or root; group/world-writable
ancestors also require the sticky bit, preventing another user from replacing a
checked private directory through an unsafe shared parent. These checks run before
creating a lock or reading state. Trusted owners (including root) remain outside
this protection boundary.
Windows is deliberately unsupported for persistence because POSIX mode bits do
not establish Windows ACL privacy; it fails closed without modifying permissions.

The adapter holds an exclusive lock for the caller's whole operation. Always call
`close()` in a `finally` block. Writes use an exclusive 0600 temporary file, file
sync, atomic rename and directory sync. Failures report a fixed checkpoint warning;
after an interrupted rename the durable outcome can be uncertain. Keep the old
checkpoint until it has been inspected privately. Stale locks require checking
that no process is still using the directory before manual removal. Concurrent
or crashed runs never automatically steal locks. Filesystem permissions cannot
protect against another process running as the same OS user.

Missing state explicitly reports lost/absent coverage and establishes a fresh
unscanned baseline. Corrupt state, policy fingerprint changes, size/dedup limits,
and load errors fail closed without accepting the previous state or silently
discarding deduplication. Restoring a known checkpoint may repeat observations;
there is no exactly-once delivery claim. Raising limits or resetting a baseline
requires explicit review. Interrupted runs may repeat warnings on the next run.

## Validation and operation

Run synthetic regression tests first, with no credentials or network:

```sh
node --test tests/commitIdentityScanner.node.mjs tests/commitIdentityAdvisory.node.mjs tests/commitIdentityCaller.node.mjs
```

The existing regression workflow discovers the new test file without modification.
POSIX file privacy tests run on Linux CI; Windows tests verify safe rejection.
Mocks cover role combinations, collisions, null/malformed identities, inventory
and comparison pagination, renames, overlaps, access gaps, state failures/loss,
races, force pushes, timeouts, fixed-output privacy and GET-only transport.

The sole CLI mode is an explicit bounded read-only baseline dry run:

```sh
node .github/scripts/commit-attribution-cli.mjs --dry-run
```

Use only an already authorized `GITHUB_TOKEN` supplied through the process
environment. Do not put credentials on the command line or in files. The dry run
keeps its baseline in memory, emits only fixed categories, writes no checkpoint,
and does not inspect historical commits. It is not proof of prospective coverage.
The defaults cap each list at 30 pages, the whole run at 500 requests and two
minutes, each HTTP request at 20 seconds, and each response at 8 MiB. Larger
inventories can legitimately hit these bounds and must report the gap.
Library transport callers must supply positive safe-integer request/time limits;
time limits must fit Node's timer range. Missing or invalid limits emit a fixed
policy warning without a request. Each client snapshots its limits at construction.
Errors and findings remain warning-only; the CLI never converts them into a
failing exit status or invokes an enforcement API.

Persistent use requires a separately reviewed integration that supplies `get`,
validated reviewed `entries`, `config`, the private checkpoint adapter, and the
fixed `publicReporter()` to `scan()`. That integration must acquire the adapter
before scanning and close it afterward, reporting lock/open/close failures using
`COVERAGE_CHECKPOINT_FAILURE`. No such integration is activated by this change.
Keep the PR draft until final-head CI and reviews are handled. Merge, deployment,
activation and DSPACE cleanup remain separate decisions.
