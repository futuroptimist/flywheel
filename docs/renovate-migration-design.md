# Design: dependency updates with Renovate, Dependabot, or both

Status: proposal, not rollout approval. Evidence checked November 13, 2026 UTC.
This PR changes documentation only. It does not install an app, change bot configuration,
permissions, security settings, schedules, automerge, dependencies, or deployments.

## Recommendation and decision

Pilot the free hosted Renovate app for **runner labels only**, alongside existing Dependabot.
If a later parity pilot demonstrates adequate coverage and manageable workload at no subscription
cost, prefer one Renovate version-update writer per repository over permanent dual-bot complexity.
Do not declare full parity from a supported-manager list alone. Keep GitHub's dependency graph and
Dependabot alerts enabled even if Renovate eventually replaces dependency-update PR creation.

The owner decides between:

1. Keep Dependabot and manually review runner upgrades: least new access, persistent manual gap.
2. Use Dependabot plus runner-only Renovate: recommended initial, bounded experiment.
3. Migrate version-update PRs fully to Renovate: conditional target after the gates below.

No option authorizes automatic merges. A bot proposing an upgrade is not proof of compatibility.

## Current evidence and why this matters

At Flywheel main `7cd3c46d9338b723768c6cd35cd290a487b4821e`, the
[Dependabot configuration][flywheel-config] enables weekly GitHub Actions, root npm and root pip
updates. This is not a complete cross-repository inventory. Audit the repositories in
[repo-feature-summary.md](repo-feature-summary.md), actual manifests, workflows, lockfiles and
release branches before deciding coverage.

The separate f2clipboard pilot remains active and unchanged. Its evolving record is
[Flywheel draft PR #790][pilot]. It covers Python and Actions, excludes startup/retry runs from
weekly-cycle credit, and retains the unresolved observation of four initial Actions version-update
PRs despite a limit of two. Do not reset its counters, claim its conclusion, or change f2clipboard's
configuration as a side effect of this design. Capture fresh pilot evidence at any future decision.

[DSPACE #4874][dspace-pr] exposed a concrete gap: a floating `ubuntu-latest` runner moved to an OS
unsupported by the locked Playwright installer, failing before test assertions. Explicit runner
labels make OS-generation changes reviewable. They do not freeze GitHub's whole VM image: installed
software still changes under the [runner-image maintenance policy][runner-images]. Pin critical
language/tool versions and container digests independently where reproducibility requires it.

## Cost and deployment options

| Option | Subscription expectation | Other costs and constraints | Decision |
| --- | --- | --- | --- |
| Mend Renovate Community Cloud | Currently free for unlimited public/private repositories | Shared resources and queue latency; app access approval; repository CI still costs resources | Preferred pilot |
| Community OSS enhanced hosting | Free offering with increased resources | Request and eligibility review; acceptance is discretionary | Optional, not assumed |
| Renovate open-source CLI, self-hosted | No CLI subscription requirement | Compute, storage, maintenance, credentials, monitoring and updater upgrades | Fallback, not automatically zero cost |
| Enterprise hosting | Paid | Higher resources/support/features | Not required by this proposal |

These are current vendor statements, not a permanent price guarantee or a measured capacity result.
Recheck [hosting plans][hosting] and [resource tiers][tiers] before installation. Record the selected
plan, queue times, job duration, failures and any usage charge during the pilot. Stop expansion if
free-tier capacity is inadequate; bring a free self-hosted plan or paid tradeoff to the owner.
Do not enroll in a subscription, assume OSS enhanced eligibility, or claim zero operational cost.
[Self-hosting responsibilities][running] include infrastructure and keeping Renovate itself current.

## Coverage and remaining proof

| Need | Dependabot today / Renovate candidate | Required evidence before migration |
| --- | --- | --- |
| Action and reusable-workflow refs | Both; Renovate can also maintain SHA pins | Representative action and reusable-workflow PRs; preserve intended downstream compatibility |
| Literal hosted runner labels | Renovate `github-runner` type; Dependabot lacks this feature | Extract intended labels and propose supported OS generation without hidden variable misses |
| npm manifests and lockfiles | Both have managers | Every root/workspace lockfile regenerated with project tool versions and tested |
| Python requirements and pyproject | Renovate has multiple Python managers | Inventory actual formats, including duplicate CI/pre-commit pins; prove coordinated updates |
| Docker, Helm and runtime versions | Renovate offers relevant managers | Per-format extraction report; digest handling, chart/image separation and architecture tests |
| Arbitrary shell-installed versions | Not universally discovered by either bot | Inventory misses; documented manual ownership or tested custom manager, never blanket parity claim |
| Vulnerability detection and fixes | GitHub alerts are separate from version-update bots | Preserve alert ingestion and prove fix routing; define exactly one fix-PR owner per scope |
| Scheduling, grouping and queue limits | Both configurable with different semantics | Observe regular and security queues separately; measure volume, review time and blocked PR age |

Primary capability references: [Actions manager][actions], [manager catalog][managers],
[PEP 621 manager][pep621], [npm manager][npm], and [Dependabot Actions scope][dependabot-actions].
Renovate's built-in manager ignores variable-based runner labels; its
[runner datasource][runner-data] may lag newly announced images. Explicit `ubuntu-24.04` therefore
means a reviewable OS generation, not guaranteed immediate notification or an immutable image.

Security parity is a separate gate. Renovate's [vulnerability-alert integration][vulnerabilities]
uses GitHub's dependency graph and Dependabot alerts with appropriate read permission. It does not
replace GitHub's vulnerability database/alerting. Security fixes can bypass normal schedules and
limits by default: do not infer security-queue behavior from ordinary update caps. Leave security
settings unchanged during the runner-only pilot. A full switch must separately assign security PR
ownership and verify alert/fix behavior before disabling overlapping security-update writers.

## Proposed runner-only configuration boundary

The implementation PR must use the current Renovate schema and validate the resolved configuration.
This document intentionally installs no executable configuration. The desired policy is:

- Enable only the `github-actions` manager.
- Disable every dependency extracted by that manager, then enable only `github-runner` dependencies.
  Merely selecting the manager would also update Actions and overlap Dependabot.
- Disable Renovate vulnerability-fix PR creation during the runner-only experiment; retain existing
  GitHub alert/security-update settings and owners.
- Explicitly disable automerge. Use a low ordinary PR limit, manual review and required CI.
- Schedule ordinary update creation outside weekday work hours in `America/Los_Angeles`; verify
  hosted scheduling semantics. A schedule is not a precise wall-clock guarantee or a merge approval.
- Prove extraction and candidate diffs in a no-write dry run on an isolated fixture. Include literal
  runner labels, action refs, reusable workflows, container refs and an intentionally hidden variable.
  Assert that only runner labels are eligible, no action/container update is proposed, and the hidden
  variable is recorded as a coverage gap. Validate custom rules against the pinned CLI version.

Do not bypass a failed test to accept an OS upgrade. Pair runner and Playwright/tool compatibility
review; preserve architecture-specific runner choices. Record intentional pin exceptions and owners.

## Phased procedure and deliverables

| Phase | Deliverable | Gate / owner action |
| --- | --- | --- |
| 0. Inventory | Repo/path/branch inventory with current bot, versions, lockfiles, exclusions and alert owner | Review coverage gaps, compare with current pilot; no settings changes |
| 1. Design review | This design PR and chosen free hosting mode | Owner approves a named pilot repo, app access and scope separately |
| 2. Prepare | Small pilot config PR, pinned validator/dry-run evidence and rollback snapshot | Demonstrate runner-only extraction; review requested app permissions |
| 3. Install and observe | Owner-authorized app installation limited to pilot repo; run/PR log | No production deployment or dependency automerge; full CI and human merges |
| 4. Evaluate | At least two distinct successful scheduled cycles over at least two weeks, plus reviewed real runner-update evidence or explicitly recorded absence | If no actual candidate occurs, extend or use an isolated fixture; do not manufacture production churn |
| 5. Parity pilot | Separately approved repo/ecosystem config PR and coverage/security checklist | Do not switch f2clipboard mid-observation without explicit owner decision |
| 6. Migrate in batches | One reviewed migration PR per repo or small coherent group, plus versioned evidence | Owner approves expansion; one writer per dependency scope; monitor before next batch |
| 7. Close | Inventory updated with bot ownership, gaps, rollback links and measured outcome | No unresolved coverage/security/volume issue; owner accepts full or mixed model |

Choose a small non-production pilot with literal runner labels after inventory; do not silently use
DSPACE's active hotfix or disturb f2clipboard's existing experiment. Run the new pilot's clocks and
metrics separately from the Dependabot pilot. Deliver a short comparison: detection latency, real
updates reviewed/merged, failures, duplicate PRs, review effort, CI resource use and hosting queues.

## Full migration and duplicate prevention

1. Snapshot the last known-good bot configurations, open PRs and relevant settings. Assign each
   dependency path/ecosystem and security-fix lane exactly one writer. Keep an explicit exception map.
2. Validate Renovate extraction and artifacts for every in-scope manifest and release branch before
   enabling writes. Record unsupported formats with named manual ownership; do not label them covered.
3. In a reviewed handoff window, stop Dependabot version-update creation only for the scope moving.
   Reconcile in-flight PRs first; do not close a security fix or useful review blindly. Settings changes
   need the owner's approval. Keep dependency graph and alerts enabled.
4. Enable only the equivalent Renovate scope, retaining manual merges and required CI. Review the
   first generated diffs for duplicate-pin and downstream compatibility issues found in the old pilot.
5. Prove normal and security update routes independently. If security PR ownership changes, test the
   authorized configuration with a controlled fixture; never deliberately introduce a vulnerable
   dependency into a production repository to trigger an alert.
6. Expand only after measured results meet the gates. Record adopted/partial/not-applicable states
   in the repo feature summary, with evidence links and next action, not a single misleading checkbox.

A complete replacement means replacing update-PR writers where proven, not deleting every GitHub
feature with the Dependabot name. A mixed model is acceptable when it preserves a necessary
capability at lower maintenance cost; overlapping write scopes are not.

## Rollback and operational ownership

Triggers: missed dependencies/security fixes, duplicate or excessive PRs, unauthorized scope,
incompatible generated changes, persistent queue delays, or unacceptable cost/review load.

Pause the new writer for the affected scope using the approved operational path; retain logs and
open-PR state. Restore the snapshot of the prior version-update configuration, verify a successful
scheduled run and expected coverage, and reconcile each pending PR. Confirm alerts remained active.
Revoke app access only with explicit approval, not as an automatic destructive cleanup step. If the
scope cannot be proven safe, stop expansion and report the exact gap. Closing this design PR or
merging its documentation does not itself approve installation, migration or rollback operations.

The owner approves installations, new access, migrations and merges. Kepler prepares evidence,
reviewable PRs and operational handoffs within the granted scope and work-hours constraints. Keep
credentials out of configuration examples and reports. Use selected-repository access, not account-
wide access merely for convenience; review the app's current requested permissions before approval.

## Decision record to complete after pilot

- Chosen mode and repository scopes:
- Cost/resource evidence and checked plan date:
- Inventory coverage and unresolved exceptions:
- Two-cycle and real-update evidence:
- Security detection/fix ownership and proof:
- Duplicate/volume/compatibility findings:
- Owner decision, implementation PRs and rollback snapshot:

[flywheel-config]: https://github.com/futuroptimist/flywheel/blob/7cd3c46d9338b723768c6cd35cd290a487b4821e/.github/dependabot.yml
[pilot]: https://github.com/futuroptimist/flywheel/pull/790
[dspace-pr]: https://github.com/democratizedspace/dspace/pull/4874
[hosting]: https://docs.renovatebot.com/mend-hosted/overview/
[tiers]: https://docs.mend.io/renovate/latest/mend-renovate-cloud-resource-tiers
[running]: https://docs.renovatebot.com/getting-started/running/
[actions]: https://docs.renovatebot.com/modules/manager/github-actions/
[runner-data]: https://docs.renovatebot.com/modules/datasource/github-runners/
[runner-images]: https://github.com/actions/runner-images
[managers]: https://docs.renovatebot.com/modules/manager/
[pep621]: https://docs.renovatebot.com/modules/manager/pep621/
[npm]: https://docs.renovatebot.com/modules/manager/npm/
[dependabot-actions]: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions
[vulnerabilities]: https://docs.renovatebot.com/configuration-options/#vulnerabilityalerts
