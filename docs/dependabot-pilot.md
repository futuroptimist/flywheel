# Dependabot pilot and staged adoption

Status: active pilot; findings incomplete. Keep this document's pull request in draft throughout
the pilot. At its conclusion, record the outcome, finish review and checks, then ask the repository
owner to merge the document. Neither this document nor a green check authorizes a dependency merge,
broader rollout, repository setting change, deployment or automatic merging.

Last evidence refresh: November 11, 2026 at 07:22 UTC (November 10 at 23:22 PST).

## Purpose

Use a small, manually reviewed pilot to establish whether Dependabot finds the intended dependencies,
runs reliably, produces a manageable queue, and supports informed compatibility review. Record the
evidence here before choosing the next repository or ecosystem. Configuration presence, successful
updater jobs and accepted dependency changes are three different kinds of evidence.

Flywheel hosts the cross-repository procedure. The active pilot runs in **f2clipboard**, not Flywheel.
Flywheel's [existing configuration](../.github/dependabot.yml) is separate and is unchanged by this
documentation PR. The [repository inventory](repo-feature-summary.md) is a starting point for later
coverage audits, not proof that every dependency or security setting is covered.

## Active scope

The owner merged [f2clipboard PR #168][pilot-pr] on November 10, 2026 at 22:54:50 PST
(November 11 at 06:54:50 UTC), creating [commit fb5e068][pilot-commit]. The
[configuration at that commit][pilot-config] enables:

| Ecosystem | Directory | Update interval | Open version-update PR limit |
| --- | --- | --- | --- |
| Python (`pip`) | `/` | Weekly | 2 |
| GitHub Actions (`github-actions`) | `/` | Weekly | 2 |

- Manually inspect each update's diff, dependency source, release notes, runtime compatibility,
  checks and review findings. The owner decides whether to merge, defer or close it.
- Security-update PRs have a separate GitHub limit. This pilot did not change security-update
  settings. Do not count them as ordinary version updates or assume they explain excess PRs.
- No grouping, explicit day/time/timezone, package allowlist or major-version exclusion was added.
  Weekly creation does not mean every update is low risk. Majors and toolchain changes still need
  individual review.
- Repository auto-merge was disabled at the evidence refresh. The implementation did not change
  branch protection, credentials, repository permissions or deployment settings.
- The configuration, regression test and contributor guidance merged in #168 establish the
  approved scope. No other repository or ecosystem is approved for expansion by this document.

## Initial findings

### Startup succeeded; scheduled cycles remain unobserved

Two overlapping updater runs per ecosystem completed successfully against `fb5e068` immediately
after the configuration merged. These are startup observations, not two weekly cycles.

| Ecosystem | Run | Started, November 11 UTC | Conclusion | Weekly credit |
| --- | --- | --- | --- | --- |
| GitHub Actions | [42975743807][actions-start-1] | 06:54:58 | Success | None: startup |
| GitHub Actions | [42975750581][actions-start-2] | 06:55:02 | Success | None: startup |
| Python | [42975743675][pip-start-1] | 06:54:58 | Success | None: startup |
| Python | [42975748769][pip-start-2] | 06:55:01 | Success | None: startup |

Verified successful scheduled weekly cycles: **Python 0/2; GitHub Actions 0/2**.
GitHub reports these updater runs as dynamic events. A run's success or event name alone does not
prove that it represents a new scheduled weekly cycle. Record the schedule/cycle evidence as well.

### Open finding: startup Actions PR volume exceeded the configured limit

The initial complete open-PR enumeration, before the owner merges below, returned six Dependabot
PRs. The last column records the later disposition at the current evidence refresh:

| Ecosystem | PR | Update | Review disposition in this record |
| --- | --- | --- | --- |
| GitHub Actions | [#169][pr169] | `actions/checkout` 3 to 7 | Owner merged; see log below |
| GitHub Actions | [#170][pr170] | `actions/setup-python` 4 to 7 | Repair and final checks in progress |
| GitHub Actions | [#171][pr171] | `anthropics/claude-code-action` 1.0.180 to 1.0.269 | Owner merged; see log below |
| GitHub Actions | [#172][pr172] | `codecov/codecov-action` 5 to 7 | Owner merged; see log below |
| Python | [#173][pr173] | `flake8` 7.3.0 to 7.4.1 | Repair and final checks in progress |
| Python | [#174][pr174] | `isort` 8.0.1 to 9.0.2 | Repair and final checks in progress |

Four Actions version-update PRs initially exceeded the intended limit of two. All four startup
job definitions report `command: version`, `security-updates-only: false` and
`existing-pull-requests: []`.
The observed jobs do not support a security-update explanation for the excess.

Concurrent initialization is a plausible contributor, **not an established root cause**. The updater
logs' "created" summaries also list more dependencies than the actual open PR enumeration. Use
verified PR records for queue counts; a log summary is not proof of distinct PR creation. Reconcile
job timing, request results and subsequent scheduled behavior before declaring the cap effective.
No speculative configuration fix, PR closure or rerun is part of documenting this finding.

The initial queue is a dated snapshot. Owner merges reduced the outstanding queue, but do not
explain the startup excess or demonstrate normal scheduled cap behavior. The unmerged updates
are not ready-to-merge claims; their final heads, checks and review threads still need verification.

### Owner merge and review log: November 11 UTC

GitHub records `futuroptimist` as the merging owner for these three Actions updates:

| PR | Merged, November 11 UTC | Merge commit | PR head at merge |
| --- | --- | --- | --- |
| [#169 checkout][pr169] | 07:14:21 | [56c9184][merge169] | `4aca211e067c4be2cecc27d84866daf2eeb3d0bd` |
| [#172 Codecov][pr172] | 07:14:34 | [06b8354][merge172] | `d8ac82c4a41a64aa2189059f9a1a8992d63e4ba5` |
| [#171 Claude action][pr171] | 07:20:31 | [60d29b9][merge171] | `5e0cf79b342d34bbae5424b2c99bfb30172a8659` |

The #171 assessment included assistant-performed local validation of the exact
[upstream candidate 61a9c27][claude-candidate]: **302 focused offline tests passed**, using
Bun 1.4.4 and its frozen lockfile, and TypeScript checking passed. Separately, the candidate's
[upstream CI run][claude-ci] completed successfully. The 302-test count comes from the local
assessment, not that upstream CI run. A [Codex review summary][claude-review] reported no issues.

The exact f2clipboard live Claude sandbox/signed-write smoke test was **not run**. Offline tests
and upstream CI do not establish that repository-specific live behavior. No blocker was found in
the completed assessment, but retain this coverage limit rather than treating the merge as proof
of every behavior or of the pilot's success.

At 07:22 UTC, the complete open-PR listing contained #170, #173 and #174: one Actions update and
two Python updates. Repairs and final-head checks/review follow-up were in progress. The #170
repair preserves the public `action.yml` setup-python v4 reference while upgrading hosted workflows;
the #173/#174 repairs align duplicate hard pins. Final repair evidence and owner dispositions are
pending. The smaller queue resulted from owner merges and does not resolve the startup cap finding.

These merges add no scheduled weekly cycles. Counters remain **Python 0/2; GitHub Actions 0/2**,
and the full representative-review checklist and proposed conclusion gate remain open.

## Observation and review procedure

1. Read the current default-branch configuration and record its commit. Enumerate all open PR pages
   and verify the Dependabot author identity. Track version updates and security updates separately.
2. For each updater run, record ecosystem, distinct weekly cycle/date, run link and ID, source
   commit, attempt, outcome and observation time. Separate startup/manual runs and retries from
   scheduled cycles. Do not count two attempts or simultaneous jobs as two weeks.
3. Count actual open PRs by ecosystem. Compare new PRs, closures, superseded updates and outstanding
   backlog with the configured limit. Preserve anomalies and unknowns rather than smoothing them out.
4. Review representative updates from both ecosystems using the checklist below. Record review time,
   failures, rework and the owner's disposition so the final recommendation reflects real workload.
5. Append material findings to this draft and update the pending items. Reuse evidence only while the
   exact head and relevant base remain unchanged. Report significant failures promptly.
6. Once **both ecosystems have two successful distinct scheduled weekly cycles**, provide the owner
   a concise findings update even if other exit criteria remain unmet. A requested progress report
   must not wait for every rollout blocker to disappear.

### Per-update review checklist

- Record PR URL, verified author, immutable head SHA, current base SHA, old/new versions and time.
- Inspect the complete manifest/lock/workflow diff and actual upstream source and release notes.
  Check supported runtimes, peer dependencies, APIs, transitive additions, integrity/source changes,
  install hooks and native binaries. For Actions, check runner/runtime requirements and permissions.
- Inspect every applicable check/status and review-thread page on the final head, or a verified
  integration commit of that head plus the current base. Explain skipped jobs. Handle review findings
  within approved scope; a review-service check is not owner approval.
- Record the owner's merge, defer, repair or close decision. Do not infer safety from semver labels,
  compatibility scores or green CI alone. Do not weaken checks or expand credentials to unblock it.
- Recheck head, base, checks and reviews immediately before the owner acts. A new head, material base
  change or new review finding invalidates the prior readiness assessment.

### Weekly evidence log

Append one entry per ecosystem and distinct scheduled cycle. Keep failed and missing cycles visible.
Use this structure for each entry; do not replace unknown values with assumed success:

- Ecosystem and cycle/date:
- Run URL/ID, attempt and evidence that it was the scheduled weekly cycle:
- Source commit and observation time:
- Outcome, error details and whether it counts toward the two-cycle checkpoint:
- Actual open version/security PR counts, additions/closures and cap finding:
- Representative PR review links, exact heads and owner dispositions:
- Review effort, regression/rework and next action/owner:

No scheduled-cycle entries have been verified yet. Writing this procedure does not install a
monitoring schedule; any scheduled observation must be set up and verified separately.

## Proposed conclusion criteria

November 24, 2026 PST is a planning checkpoint derived from the November 10 launch, not an agreed
deadline or an automatic success date. The proposed assessment window is **at least two weeks**.
Missing or failed evidence extends observation. Recommend successful completion only when:

- [ ] Each ecosystem has two successful **distinct scheduled weekly cycles** after launch, with
      links and cycle evidence. Startup jobs, manual runs and retries do not add cycles.
- [ ] At least one real update per ecosystem has received the full manual review above, with
      applicable final-head checks passing, review findings handled and owner disposition recorded.
- [ ] The four-versus-two Actions discrepancy is reconciled and subsequent behavior demonstrates
      the intended version-update cap. Security-update counts remain separate.
- [ ] Accepted updates have no unresolved regression or unsupported runtime/toolchain migration.
- [ ] Observed queue size, review effort and rework are manageable, with the evidence summarized.
- [ ] The owner has an evidence-backed recommendation to continue, extend, stop or expand narrowly.

The two-cycle notification checkpoint and the broader success criteria are separate. Report the
checkpoint when reached even if the recommendation is to extend observation or hold expansion.

## Steps after the pilot

1. **Conclude the experiment explicitly.** Fill in the conclusion record below. Summarize updater
   reliability, PR volume, reviewed outcomes, workload, remaining unknowns and the cap investigation.
   Choose a recommendation: extend, stop, retain the current scope, or propose a small expansion.
   The owner makes the decision; elapsed time does not approve it.
2. **Finish this documentation PR.** Keep it draft until the pilot concludes, including if the
   conclusion is unsuccessful. Replace provisional findings with the final evidence and decision,
   address review feedback, and verify checks on the final commit. Then present it for owner review
   and owner-performed merge. Do not enable auto-merge or merge it during observation.
3. **Refresh coverage before selecting a next batch.** Reconcile the current repository inventory,
   config files, dependency-bearing manifests, includes/workspaces and lock ownership. Distinguish
   configuration, observed updates, security settings and unknowns. Do not schedule every nested
   template, fixture, Helm chart, firmware or downloaded binary as though Dependabot covers it.
4. **Propose a bounded manual-review expansion.** Name the exact repository, ecosystem, directory,
   dependency/runtime scope, schedule and PR cap. Prefer one independently reviewable scope at a
   time, with a new observation gate and recovery plan. Refresh existing queues and effective
   check/review requirements first. Obtain owner approval before implementing that batch.
5. **Evaluate the next batch before widening again.** Apply the same evidence discipline and stop
   promotion on errors, unsupported migrations, unexpected volume or regressions. Preserve evidence
   and give the owner concrete remediation/revert options. Settings changes, reverts and deployments
   are separate actions, not automatic recovery steps.
6. **Consider automation only as a separate proposal.** The automatic-merge allowlist remains empty.
   Any future shadow evaluation must name exact repository/package/source/bot/update scopes and
   measure reviewed samples without merging. A later automation proposal would need enforced checks,
   review gates, protection against changed heads/base races, least privilege and a recovery plan.
   A separate shadow proposal's duration or sample count does not set this pilot's exit criteria.

### Ongoing maintenance proposal

After a separately approved expansion, use a short read-only review pass to discover the complete
open queue, prioritize verified security issues and breaking/runtime changes, inspect changed heads
and failing checks, and record the next owner/action. Bound deep reviews to available capacity.
Send useful changes with direct PR links, without repeating unchanged alerts. Periodically reconcile
coverage and settings again. This is a proposed workflow, not authorization for recurring actions,
dependency edits, messages to other reviewers or automatic merges.

## Pending items and conclusion record

- [ ] Record Python weekly cycle 1 and cycle 2.
- [ ] Record Actions weekly cycle 1 and cycle 2.
- [ ] Reconcile the Actions PR-limit discrepancy and verify subsequent cap behavior.
- [ ] Complete and record a representative Python update review and owner disposition.
- [ ] Complete and record a representative Actions update review and owner disposition.
- [ ] Deliver the two-cycle findings update, with remaining blockers if any.
- [ ] Summarize review effort, updater reliability and regression/recovery experience.
- [ ] Record the owner's conclusion and any separately approved next batch.
- [ ] Finish review/checks for this document and hand its final merge to the owner.

Conclusion date: pending.

Evidence window and successful scheduled cycles: pending.

Reviewed updates and dispositions: three owner-performed Actions merges recorded above; Python
updates and the complete representative-review evidence remain pending.

Cap finding and unresolved risks: open, as described above.

Recommendation and rationale: pending.

Owner decision, exact next scope and approval reference: pending.

[pilot-pr]: https://github.com/futuroptimist/f2clipboard/pull/168
[pilot-commit]: https://github.com/futuroptimist/f2clipboard/commit/fb5e068f666434aa31dd1525efdcfef7fa02fec3
[pilot-config]: https://github.com/futuroptimist/f2clipboard/blob/fb5e068f666434aa31dd1525efdcfef7fa02fec3/.github/dependabot.yml
[actions-start-1]: https://github.com/futuroptimist/f2clipboard/actions/runs/42975743807
[actions-start-2]: https://github.com/futuroptimist/f2clipboard/actions/runs/42975750581
[pip-start-1]: https://github.com/futuroptimist/f2clipboard/actions/runs/42975743675
[pip-start-2]: https://github.com/futuroptimist/f2clipboard/actions/runs/42975748769
[pr169]: https://github.com/futuroptimist/f2clipboard/pull/169
[pr170]: https://github.com/futuroptimist/f2clipboard/pull/170
[pr171]: https://github.com/futuroptimist/f2clipboard/pull/171
[pr172]: https://github.com/futuroptimist/f2clipboard/pull/172
[pr173]: https://github.com/futuroptimist/f2clipboard/pull/173
[pr174]: https://github.com/futuroptimist/f2clipboard/pull/174
[merge169]: https://github.com/futuroptimist/f2clipboard/commit/56c91841442bc744ec6beabad48cc03c6fa1bdeb
[merge172]: https://github.com/futuroptimist/f2clipboard/commit/06b8354ac1f50241a7bd36c0991d9c979f1a7577
[merge171]: https://github.com/futuroptimist/f2clipboard/commit/60d29b911e5764d19e1144617fdc9c3f3d838c32
[claude-candidate]: https://github.com/anthropics/claude-code-action/commit/61a9c274fa7110a66dfafc1bbbced03833eb25fe
[claude-ci]: https://github.com/anthropics/claude-code-action/actions/runs/42258364367
[claude-review]: https://github.com/futuroptimist/f2clipboard/pull/171#issuecomment-6789245411
