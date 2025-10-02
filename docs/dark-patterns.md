# Dark Patterns and Bright Patterns

This guide catalogs user-hostile design tactics, explains why they are problematic, and offers "bright pattern" alternatives that respect the user's agency. See [bright-patterns.md](bright-patterns.md) for a dedicated catalog of pro-user practices. The repo crawler counts potential dark patterns across related projects and records the results in `docs/repo-feature-summary.md`.

Regenerate the summary with up-to-date dark and bright pattern counts by running:

```bash
python scripts/update_repo_feature_summary.py --repos-from docs/repo_list.txt --out docs/repo-feature-summary.md
```

## Why avoid dark patterns?

Manipulative interfaces erode trust and may even violate privacy or consumer protection laws. Sustainable communities grow when contributors feel respected and in control of their data.

## Catalog

| Dark pattern | Why it's harmful | Bright pattern |
| ------------ | ---------------- | -------------- |
| **Bait and switch** | Promising one thing but delivering another confuses users. | Be transparent about outcomes and label actions clearly. |
| **Forced continuity** | Making subscriptions hard to cancel traps users. | Provide an easy, single-step opt-out path. |
| **Hidden costs** | Surprises at checkout feel deceptive. | Display full pricing upfront, including fees. |
| **Privacy Zuckering** | Coercing users to share more data than necessary violates consent. | Offer clear privacy choices and respect opt-outs. |
| **Roach Motel** | Easy to sign up, hard to leave. | Allow account deletion without hoops. |
| **Confirmshaming** | Guilt-tripping language pressures users. | Use neutral copy for decline options. |
| **Disguised ads** | Ads that look like native content mislead readers. | Clearly label promotional material. |
| **Misdirection** | Visual tricks nudge clicks toward unintended actions. | Use straightforward navigation and button labels. |
| **Nagging** | Persistent pop-ups or notifications wear users down. | Provide respectful reminders that can be dismissed permanently. |
| **Trick questions** | Ambiguous wording leads to wrong choices. | Write plain-language questions with unambiguous answers. |
| **Sneak into basket** | Adding items to a cart without consent exploits inattentive users. | Require explicit confirmation before modifying orders. |
| **Scarcity cues** | Countdown timers or "only X left" messages create unnecessary urgency. | Provide honest stock levels and reasonable time to decide. |
| **Activity notifications** | Fake or repeated updates about other shoppers apply social pressure. | Show only genuine activity or none at all. |
| **Data grabs** | Requesting excess personal details risks privacy misuse. | Collect only what is needed for the task. |
| **False hierarchy** | Interface layout pushes the provider's preferred option. | Present choices evenly so the user can decide freely. |
| **Redirection or nagging** | Repeated pop-ups steer users away from their intended action. | Let people dismiss prompts and continue without detours. |

This list incorporates examples from [NSW Fair Trading's dark pattern guide](https://www.nsw.gov.au/departments-and-agencies/fair-trading/dark-patterns).

For additional guidance, see [best_practices_catalog.md](best_practices_catalog.md).
