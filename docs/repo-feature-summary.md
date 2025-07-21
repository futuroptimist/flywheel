# Repo Feature Summary

This table tracks which flywheel features each related repository has adopted.

<!-- spellchecker: disable -->
## Basics
| Repo | Branch | Commit | Trunk |
| ---- | ------ | ------ | ----- |
| **[futuroptimist/flywheel](https://github.com/futuroptimist/flywheel)** | main | `31bb4b0` | ❌ |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | main | `540fb42` | ❌ |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | main | `441852f` | ✅ |
| [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) | main | `bc9aa07` | ✅ |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | main | `1467519` | ✅ |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | v3 | `d6c8d6a` | ✅ |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | main | `37db08f` | ❌ |
| [futuroptimist/sigma](https://github.com/futuroptimist/sigma) | main | `6e349ed` | ❌ |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | main | `00d12c5` | ✅ |
| [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube) | main | `923728f` | ❌ |

## Coverage & Installer
| Repo | Coverage | Patch | Installer |
| ---- | -------- | ----- | --------- |
| **[futuroptimist/flywheel](https://github.com/futuroptimist/flywheel)** | ✅ (100%) | — | 🚀 uv |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | ✅ (100%) | — | 🚀 uv |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | ✅ (100%) | — | 🚀 uv |
| [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) | ✅ (100%) | — | 🚀 uv |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | ✅ (100%) | — | pip |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | ✅ (100%) | — | 🔶 partial |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | ✅ (100%) | — | 🚀 uv |
| [futuroptimist/sigma](https://github.com/futuroptimist/sigma) | ✅ (100%) | — | 🚀 uv |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | ✅ (100%) | — | pip |
| [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube) | ❌ | — | 🚀 uv |

## Policies & Automation
| Repo | License | CI | Workflows | AGENTS.md | Code of Conduct | Contributing | Pre-commit |
| ---- | ------- | -- | --------- | --------- | --------------- | ------------ | ---------- |
| **[futuroptimist/flywheel](https://github.com/futuroptimist/flywheel)** | ✅ | ✅ | 10 | ✅ | ✅ | ✅ | ✅ |
| [futuroptimist/axel](https://github.com/futuroptimist/axel) | ✅ | ✅ | 3 | ✅ | ✅ | ✅ | ✅ |
| [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel) | ✅ | ✅ | 3 | ✅ | ✅ | ✅ | ✅ |
| [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) | ✅ | ✅ | 4 | ✅ | ✅ | ✅ | ✅ |
| [futuroptimist/token.place](https://github.com/futuroptimist/token.place) | ✅ | ✅ | 2 | ✅ | ✅ | ✅ | ✅ |
| [democratizedspace/dspace](https://github.com/democratizedspace/dspace) | ✅ | ✅ | 3 | ✅ | ✅ | ✅ | ❌ |
| [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard) | ✅ | ✅ | 3 | ✅ | ✅ | ✅ | ✅ |
| [futuroptimist/sigma](https://github.com/futuroptimist/sigma) | ✅ | ✅ | 4 | ✅ | ✅ | ✅ | ✅ |
| [futuroptimist/wove](https://github.com/futuroptimist/wove) | ✅ | ✅ | 6 | ✅ | ✅ | ✅ | ✅ |
| [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube) | ✅ | ✅ | 4 | ✅ | ❌ | ❌ | ✅ |

Legend: ✅ indicates the repo has adopted that feature from flywheel. 🚀 uv means only uv was found. 🔶 partial signals a mix of uv and pip. Coverage percentages are parsed from their badges where available. Patch shows ✅ when diff coverage is at least 90% and ❌ otherwise, with the percentage in parentheses. The commit column shows the short SHA of the latest default branch commit at crawl time. The Trunk column indicates whether CI is green for that commit.
