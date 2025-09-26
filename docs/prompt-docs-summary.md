<!-- spellchecker: disable -->
# Prompt Docs Summary

This index is auto-generated with
[scripts/update_prompt_docs_summary.py]
(../../scripts/update_prompt_docs_summary.py)
using RepoCrawler to discover prompt documents across repositories.

RepoCrawler powers other reports like repo-feature summaries;
use it as a model for deep dives.

Think of each listed repository as a small flywheel belted to this codebase. The list in
dict/prompt-doc-repos.txt mirrors docs/repo_list.txt; if a repo drops from the output,
fix that integration rather than deleting it.

All prompts are verified with OpenAI Codex. Other coding agents like Claude Code, Gemini
CLI, and Cursor should work too.

**244 one-click prompts verified across 14 repos (95 evergreen, 5 one-off, 7 unknown).**

One-off prompts are temporary—copy them into issues or PRs, implement, and then remove
them from source docs.

All listed prompts are mechanically verified as 1-click ready: copy & paste without
editing.

Run this script to regenerate the table:

```bash
python scripts/update_prompt_docs_summary.py --repos-from docs/repo_list.txt --out docs/prompt-docs-summary.md
```

## Legend

| Type      | Description                                                                |
| --------- | -------------------------------------------------------------------------- |
| evergreen | prompts that can be reused to hillclimb toward goals like feature          |
|           | completeness or test coverage                                              |
| one-off   | prompts to implement features or make recommended changes (glorified TODO; |
|           | remove after cleanup)                                                      |
| unknown   | catch-all; refine into another category or create a new one                |

## **[futuroptimist/flywheel](https://github.com/futuroptimist/flywheel)**

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| [docs/pms/                             | [Spellcheck Prompt Summary Malformed]  | evergreen    | yes        |
| 2025-08-09-spellcheck-prompt-summary.md] | [prompt-2]                             |              |            |
| [path-1]                               |                                        |              |            |
| [docs/pms/                             | [Prompt summary spellcheck failure]    | evergreen    | yes        |
| 2025-08-15-prompt-summary-spellcheck.md] | [prompt-6]                             |              |            |
| [path-5]                               |                                        |              |            |
| [docs/pms/                             | [Prompt docs workflow run-checks       | evergreen    | yes        |
| 2025-08-16-prompt-docs-run-checks.md]  | failure] [prompt-8]                    |              |            |
| [path-7]                               |                                        |              |            |
| [docs/prompts/codex/automation.md]     | [Codex Automation Prompt] [prompt-12]  | evergreen    | yes        |
| [path-11]                              |                                        |              |            |
| [docs/prompts/codex/automation.md]     | [Implementation prompts] [prompt-13]   | evergreen    | yes        |
| [path-11]                              |                                        |              |            |
| [docs/prompts/codex/automation.md]     | [How to choose a prompt] [prompt-14]   | evergreen    | yes        |
| [path-11]                              |                                        |              |            |
| [docs/prompts/codex/automation.md]     | [Upgrade Prompt] [prompt-15]           | evergreen    | yes        |
| [path-11]                              |                                        |              |            |
| [docs/prompts/codex/cad.md]            | [Upgrade Prompt] [prompt-17]           | evergreen    | yes        |
| [path-16]                              |                                        |              |            |
| [docs/prompts/codex/ci-fix.md]         | [OpenAI Codex CI-Failure Fix Prompt]   | evergreen    | yes        |
| [path-18]                              | [prompt-19]                            |              |            |
| [docs/prompts/codex/ci-fix.md]         | [Upgrade Prompt] [prompt-22]           | evergreen    | yes        |
| [path-18]                              |                                        |              |            |
| [docs/prompts/codex/cleanup.md]        | [Upgrade Prompt] [prompt-24]           | evergreen    | yes        |
| [path-23]                              |                                        |              |            |
| [docs/prompts/codex/fuzzing.md]        | [OpenAI Codex Fuzzing Prompt]          | evergreen    | yes        |
| [path-25]                              | [prompt-26]                            |              |            |
| [docs/prompts/codex/fuzzing.md]        | [Upgrade Prompt] [prompt-27]           | evergreen    | yes        |
| [path-25]                              |                                        |              |            |
| [docs/prompts/codex/                   | [Codex Merge Conflicts Prompt]         | evergreen    | yes        |
| merge-conflicts.md] [path-28]          | [prompt-29]                            |              |            |
| [docs/prompts/codex/                   | [Upgrade Prompt] [prompt-30]           | evergreen    | yes        |
| merge-conflicts.md] [path-28]          |                                        |              |            |
| [docs/prompts/codex/physics.md]        | [Upgrade Prompt] [prompt-32]           | evergreen    | yes        |
| [path-31]                              |                                        |              |            |
| [docs/prompts/codex/                   | [OpenAI Codex Repo Glean Prompt]       | evergreen    | yes        |
| prompt-glean-repos.md] [path-34]       | [prompt-35]                            |              |            |
| [docs/prompts/codex/propagate.md]      | [Codex Prompt Propagation Prompt]      | evergreen    | yes        |
| [path-36]                              | [prompt-37]                            |              |            |
| [docs/prompts/codex/propagate.md]      | [Upgrade Prompt] [prompt-38]           | evergreen    | yes        |
| [path-36]                              |                                        |              |            |
| [docs/prompts/codex/spellcheck.md]     | [Codex Spellcheck Prompt] [prompt-40]  | evergreen    | yes        |
| [path-39]                              |                                        |              |            |
| [docs/prompts/codex/spellcheck.md]     | [Upgrade Prompt] [prompt-41]           | evergreen    | yes        |
| [path-39]                              |                                        |              |            |
| [docs/prompts/summary.md] [path-42]    | [TODO Prompts for Other Repos]         | evergreen    | yes        |
|                                        | [prompt-43]                            |              |            |
| [docs/prompts/summary.md] [path-42]    | [Prompt Docs TODOs] [prompt-44]        | evergreen    | yes        |
| [docs/pms/                             | [Spellcheck Untriaged Header]          | unknown      | yes        |
| 2025-08-10-untriaged-in-prompt-summary.md] | [prompt-4]                             |              |            |
| [path-3]                               |                                        |              |            |
| **[docs/prompts-major-filter.md]       | **[Prompt Docs Major Filter] [prompt-46]** | **one-off**  | **yes**    |
| [path-45]**                            |                                        |              |            |
| **[docs/prompts-major-filter.md]       | **[`scripts/                           | **evergreen** | **yes**    |
| [path-45]**                            | update_prompt_docs_summary.py`]        |              |            |
|                                        | [prompt-47]**                          |              |            |
| **[docs/prompts-salient.md] [path-48]** | **[Salient Prompt Launcher] [prompt-49]** | **evergreen** | **yes**    |
| [docs/pms/                             | [2025-08-23: Prompt docs newline]      | one-off      | yes        |
| 2025-08-23-prompt-docs-newline.md]     | [prompt-10]                            |              |            |
| [path-9]                               |                                        |              |            |
| [docs/prompts/codex/ci-fix.md]         | [2 – Commit and propagate] [prompt-20] | one-off      | yes        |
| [path-18]                              |                                        |              |            |
| [docs/prompts/codex/ci-fix.md]         | [4 – Further reading & references]     | one-off      | yes        |
| [path-18]                              | [prompt-21]                            |              |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`: `docs/pms`,
`docs/prompts-major-filter.md`, `docs/prompts-salient.md`, `docs/prompts`._

## [futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist)

| Path                               | Prompt                                | Type      | One-click? |
| ---------------------------------- | ------------------------------------- | --------- | ---------- |
| [docs/prompts/codex/automation.md] | [Codex Automation Prompt] [prompt-51] | evergreen | yes        |
| [path-50]                          |                                       |           |            |
| [docs/prompts/codex/automation.md] | [Implementation prompts] [prompt-52]  | evergreen | yes        |
| [path-50]                          |                                       |           |            |
| [docs/prompts/codex/automation.md] | [How to choose a prompt] [prompt-53]  | evergreen | yes        |
| [path-50]                          |                                       |           |            |
| [docs/prompts/codex/automation.md] | [Upgrade Prompt] [prompt-54]          | evergreen | yes        |
| [path-50]                          |                                       |           |            |
| [docs/prompts/codex/cad.md]        | [Upgrade Prompt] [prompt-56]          | evergreen | yes        |
| [path-55]                          |                                       |           |            |
| [docs/prompts/codex/ci-fix.md]     | [OpenAI Codex CI-Failure Fix Prompt]  | evergreen | yes        |
| [path-57]                          | [prompt-58]                           |           |            |
| [docs/prompts/codex/ci-fix.md]     | [Upgrade Prompt] [prompt-61]          | evergreen | yes        |
| [path-57]                          |                                       |           |            |
| [docs/prompts/codex/cleanup.md]    | [Obsolete Prompt Cleanup] [prompt-63] | evergreen | yes        |
| [path-62]                          |                                       |           |            |
| [docs/prompts/codex/cleanup.md]    | [Upgrade Prompt] [prompt-64]          | evergreen | yes        |
| [path-62]                          |                                       |           |            |
| [docs/prompts/codex/fuzzing.md]    | [OpenAI Codex Fuzzing Prompt]         | evergreen | yes        |
| [path-65]                          | [prompt-66]                           |           |            |
| [docs/prompts/codex/fuzzing.md]    | [Upgrade Prompt] [prompt-67]          | evergreen | yes        |
| [path-65]                          |                                       |           |            |
| [docs/prompts/codex/physics.md]    | [OpenAI Codex Physics Explainer       | evergreen | yes        |
| [path-68]                          | Prompt] [prompt-69]                   |           |            |
| [docs/prompts/codex/physics.md]    | [Upgrade Prompt] [prompt-70]          | evergreen | yes        |
| [path-68]                          |                                       |           |            |
| [docs/prompts/codex/propagate.md]  | [Codex Prompt Propagation Prompt]     | evergreen | yes        |
| [path-71]                          | [prompt-72]                           |           |            |
| [docs/prompts/codex/propagate.md]  | [Upgrade Prompt] [prompt-73]          | evergreen | yes        |
| [path-71]                          |                                       |           |            |
| [docs/prompts/codex/spellcheck.md] | [Codex Spellcheck Prompt] [prompt-75] | evergreen | yes        |
| [path-74]                          |                                       |           |            |
| [docs/prompts/codex/spellcheck.md] | [Upgrade Prompt] [prompt-76]          | evergreen | yes        |
| [path-74]                          |                                       |           |            |
| [docs/prompts/codex/               | [Video Script Ideas Prompt]           | evergreen | yes        |
| video-script-ideas.md] [path-77]   | [prompt-78]                           |           |            |
| [docs/prompts/codex/ci-fix.md]     | [2 – Committing & propagating]        | one-off   | yes        |
| [path-57]                          | [prompt-59]                           |           |            |
| [docs/prompts/codex/ci-fix.md]     | [3 – Further reading & references]    | one-off   | yes        |
| [path-57]                          | [prompt-60]                           |           |            |

## [democratizedspace/dspace](https://github.com/democratizedspace/dspace)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| **[docs/prompts-outages.md] [path-79]** | **[Outage prompts for the DSPACE repo] | **evergreen** | **yes**    |
|                                        | [prompt-80]**                          |              |            |
| **[docs/prompts-outages.md] [path-79]** | **[Upgrader Prompt] [prompt-81]**      | **evergreen** | **yes**    |
| **[frontend/src/pages/docs/md/         | **[Accessibility prompts for the       | **evergreen** | **yes**    |
| prompts-accessibility.md] [path-82]**  | _dspace_ repo] [prompt-83]**           |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-84]**      | **evergreen** | **yes**    |
| prompts-accessibility.md] [path-82]**  |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Dependency audit prompts for the    | **evergreen** | **yes**    |
| prompts-audit.md] [path-85]**          | _dspace_ repo] [prompt-86]**           |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-87]**      | **evergreen** | **yes**    |
| prompts-audit.md] [path-85]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Backend prompts for the _dspace_    | **evergreen** | **yes**    |
| prompts-backend.md] [path-88]**        | repo] [prompt-89]**                    |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-90]**      | **evergreen** | **yes**    |
| prompts-backend.md] [path-88]**        |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Backup prompts for the _dspace_ repo] | **evergreen** | **yes**    |
| prompts-backups.md] [path-91]**        | [prompt-92]**                          |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-93]**      | **evergreen** | **yes**    |
| prompts-backups.md] [path-91]**        |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Chat UI prompts for the _dspace_    | **evergreen** | **yes**    |
| prompts-chat-ui.md] [path-94]**        | repo] [prompt-95]**                    |              |            |
| **[frontend/src/pages/docs/md/         | **[OpenAI Codex CI-Failure Fix Prompt] | **evergreen** | **yes**    |
| prompts-codex-ci-fix.md] [path-96]**   | [prompt-97]**                          |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-98]**      | **evergreen** | **yes**    |
| prompts-codex-ci-fix.md] [path-96]**   |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Codex merge conflict prompt]        | **evergreen** | **yes**    |
| prompts-codex-merge-conflicts.md]      | [prompt-100]**                         |              |            |
| [path-99]**                            |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrade Prompt] [prompt-101]**      | **evergreen** | **yes**    |
| prompts-codex-merge-conflicts.md]      |                                        |              |            |
| [path-99]**                            |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-102]**     | **evergreen** | **yes**    |
| prompts-codex-merge-conflicts.md]      |                                        |              |            |
| [path-99]**                            |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Codex Meta Prompt] [prompt-104]**   | **evergreen** | **yes**    |
| prompts-codex-meta.md] [path-103]**    |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-105]**     | **evergreen** | **yes**    |
| prompts-codex-meta.md] [path-103]**    |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Codex Prompt Upgrader] [prompt-107]** | **evergreen** | **yes**    |
| prompts-codex-upgrader.md] [path-106]** |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-108]**     | **evergreen** | **yes**    |
| prompts-codex-upgrader.md] [path-106]** |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Writing great Codex prompts for the | **evergreen** | **yes**    |
| prompts-codex.md] [path-109]**         | _dspace_ repo] [prompt-110]**          |              |            |
| **[frontend/src/pages/docs/md/         | **[Related prompt guides] [prompt-111]** | **evergreen** | **yes**    |
| prompts-codex.md] [path-109]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[1. Quick start (Web vs CLI)]        | **one-off**  | **yes**    |
| prompts-codex.md] [path-109]**         | [prompt-112]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[2. Prompt ingredients] [prompt-113]** | **one-off**  | **yes**    |
| prompts-codex.md] [path-109]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[3. Reusable template] [prompt-114]** | **one-off**  | **yes**    |
| prompts-codex.md] [path-109]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrade Prompt] [prompt-115]**      | **evergreen** | **yes**    |
| prompts-codex.md] [path-109]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Prompt Upgrader] [prompt-116]**     | **evergreen** | **yes**    |
| prompts-codex.md] [path-109]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-117]**     | **evergreen** | **yes**    |
| prompts-codex.md] [path-109]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Documentation prompts for the       | **evergreen** | **yes**    |
| prompts-docs.md] [path-118]**          | _dspace_ repo] [prompt-119]**          |              |            |
| **[frontend/src/pages/docs/md/         | **[Proofreading prompt] [prompt-120]** | **evergreen** | **yes**    |
| prompts-docs.md] [path-118]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Cross-link check prompt] [prompt-121]** | **evergreen** | **yes**    |
| prompts-docs.md] [path-118]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-122]**     | **evergreen** | **yes**    |
| prompts-docs.md] [path-118]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Frontend prompts for the _dspace_   | **evergreen** | **yes**    |
| prompts-frontend.md] [path-123]**      | repo] [prompt-124]**                   |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-125]**     | **evergreen** | **yes**    |
| prompts-frontend.md] [path-123]**      |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Writing great item prompts for the  | **evergreen** | **yes**    |
| prompts-items.md] [path-126]**         | DSPACE repository] [prompt-127]**      |              |            |
| **[frontend/src/pages/docs/md/         | **[1. Quick start (Web vs CLI)]        | **one-off**  | **yes**    |
| prompts-items.md] [path-126]**         | [prompt-128]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[2. Prompt ingredients] [prompt-129]** | **one-off**  | **yes**    |
| prompts-items.md] [path-126]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[3. Reusable template] [prompt-130]** | **one-off**  | **yes**    |
| prompts-items.md] [path-126]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Implementation Prompt] [prompt-131]** | **evergreen** | **yes**    |
| prompts-items.md] [path-126]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrade prompt for existing items]  | **evergreen** | **yes**    |
| prompts-items.md] [path-126]**         | [prompt-132]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-133]**     | **evergreen** | **yes**    |
| prompts-items.md] [path-126]**         |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Monitoring prompts for the DSPACE   | **evergreen** | **yes**    |
| prompts-monitoring.md] [path-134]**    | repository] [prompt-135]**             |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-136]**     | **evergreen** | **yes**    |
| prompts-monitoring.md] [path-134]**    |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Writing great NPC prompts for the   | **evergreen** | **yes**    |
| prompts-npcs.md] [path-137]**          | _dspace_ repo] [prompt-138]**          |              |            |
| **[frontend/src/pages/docs/md/         | **[1. Quick start (Web vs CLI)]        | **one-off**  | **yes**    |
| prompts-npcs.md] [path-137]**          | [prompt-139]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[2. Prompt ingredients] [prompt-140]** | **one-off**  | **yes**    |
| prompts-npcs.md] [path-137]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[3. Reusable template] [prompt-141]** | **one-off**  | **yes**    |
| prompts-npcs.md] [path-137]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Implementation Prompt] [prompt-142]** | **evergreen** | **yes**    |
| prompts-npcs.md] [path-137]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrade prompt for existing NPCs]   | **evergreen** | **yes**    |
| prompts-npcs.md] [path-137]**          | [prompt-143]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-144]**     | **evergreen** | **yes**    |
| prompts-npcs.md] [path-137]**          |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Outage Prompts] [prompt-146]**      | **evergreen** | **yes**    |
| prompts-outages.md] [path-145]**       |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Playwright test prompts for the     | **evergreen** | **yes**    |
| prompts-playwright-tests.md]           | _dspace_ repo] [prompt-148]**          |              |            |
| [path-147]**                           |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-149]**     | **evergreen** | **yes**    |
| prompts-playwright-tests.md]           |                                        |              |            |
| [path-147]**                           |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Writing great process prompts for the | **evergreen** | **yes**    |
| prompts-processes.md] [path-150]**     | _dspace_ repo] [prompt-151]**          |              |            |
| **[frontend/src/pages/docs/md/         | **[1. Quick start (Web vs CLI)]        | **one-off**  | **yes**    |
| prompts-processes.md] [path-150]**     | [prompt-152]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[2. Prompt ingredients] [prompt-153]** | **one-off**  | **yes**    |
| prompts-processes.md] [path-150]**     |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[3. Reusable template] [prompt-154]** | **one-off**  | **yes**    |
| prompts-processes.md] [path-150]**     |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Implementation Prompt] [prompt-155]** | **evergreen** | **yes**    |
| prompts-processes.md] [path-150]**     |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrade prompt for existing         | **evergreen** | **yes**    |
| prompts-processes.md] [path-150]**     | processes] [prompt-156]**              |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-157]**     | **evergreen** | **yes**    |
| prompts-processes.md] [path-150]**     |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Writing great quest prompts for the | **evergreen** | **yes**    |
| prompts-quests.md] [path-158]**        | _dspace_ repo] [prompt-159]**          |              |            |
| **[frontend/src/pages/docs/md/         | **[1. Quick start (Web vs CLI)]        | **one-off**  | **yes**    |
| prompts-quests.md] [path-158]**        | [prompt-160]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[2. Prompt ingredients] [prompt-161]** | **one-off**  | **yes**    |
| prompts-quests.md] [path-158]**        |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[3. Reusable template] [prompt-162]** | **one-off**  | **yes**    |
| prompts-quests.md] [path-158]**        |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Implementation Prompt] [prompt-163]** | **evergreen** | **yes**    |
| prompts-quests.md] [path-158]**        |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrade prompt for new quests]      | **evergreen** | **yes**    |
| prompts-quests.md] [path-158]**        | [prompt-164]**                         |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-165]**     | **evergreen** | **yes**    |
| prompts-quests.md] [path-158]**        |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Refactor prompts for the _dspace_   | **evergreen** | **yes**    |
| prompts-refactors.md] [path-166]**     | repo] [prompt-167]**                   |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-168]**     | **evergreen** | **yes**    |
| prompts-refactors.md] [path-166]**     |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Secret scanning prompts for the     | **evergreen** | **yes**    |
| prompts-secrets.md] [path-169]**       | _dspace_ repo] [prompt-170]**          |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-171]**     | **evergreen** | **yes**    |
| prompts-secrets.md] [path-169]**       |                                        |              |            |
| **[frontend/src/pages/docs/md/         | **[Vitest test prompts for the _dspace_ | **evergreen** | **yes**    |
| prompts-vitest.md] [path-172]**        | repo] [prompt-173]**                   |              |            |
| **[frontend/src/pages/docs/md/         | **[Upgrader Prompt] [prompt-174]**     | **evergreen** | **yes**    |
| prompts-vitest.md] [path-172]**        |                                        |              |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`: `docs/prompts-outages.md`,
`frontend/src/pages/docs/md`._

## [futuroptimist/token.place](https://github.com/futuroptimist/token.place)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| **[docs/prompts-codex-chore.md]        | **[Codex Chore Prompt] [prompt-176]**  | **evergreen** | **yes**    |
| [path-175]**                           |                                        |              |            |
| **[docs/prompts-codex-ci-fix.md]       | **[Codex CI-Failure Fix Prompt]        | **evergreen** | **yes**    |
| [path-177]**                           | [prompt-178]**                         |              |            |
| **[docs/prompts-codex-docs.md]         | **[Codex Docs Update Prompt]           | **evergreen** | **yes**    |
| [path-179]**                           | [prompt-180]**                         |              |            |
| **[docs/prompts-codex-feature.md]      | **[Codex Feature Prompt] [prompt-182]** | **evergreen** | **yes**    |
| [path-181]**                           |                                        |              |            |
| **[docs/prompts-codex-refactor.md]     | **[Codex Refactor Prompt] [prompt-184]** | **evergreen** | **yes**    |
| [path-183]**                           |                                        |              |            |
| **[docs/prompts-codex-security.md]     | **[Codex Security Review Prompt]       | **evergreen** | **yes**    |
| [path-185]**                           | [prompt-186]**                         |              |            |
| **[docs/prompts-codex.md] [path-187]** | **[token.place Codex Prompt]           | **evergreen** | **yes**    |
|                                        | [prompt-188]**                         |              |            |
| **[docs/prompts-codex.md] [path-187]** | **[Specialized prompts] [prompt-189]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-187]** | **[Implementation prompts] [prompt-190]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-187]** | **[1 Document environment variables in | **one-off**  | **yes**    |
|                                        | README] [prompt-191]**                 |              |            |
| **[docs/prompts-codex.md] [path-187]** | **[2 Add API rate limit test]          | **one-off**  | **yes**    |
|                                        | [prompt-192]**                         |              |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`:
`docs/prompts-codex-chore.md`, `docs/prompts-codex-ci-fix.md`,
`docs/prompts-codex-docs.md`, `docs/prompts-codex-feature.md`,
`docs/prompts-codex-refactor.md`, `docs/prompts-codex-security.md`,
`docs/prompts-codex.md`._

## [futuroptimist/gabriel](https://github.com/futuroptimist/gabriel)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| [prompts/README.md] [path-201]         | [Prompt Templates] [prompt-202]        | evergreen    | yes        |
| [prompts/README.md] [path-201]         | [Prompt Catalog] [prompt-203]          | evergreen    | yes        |
| [prompts/refresh-related-projects.md]  | [Codex Related Projects Refresh        | evergreen    | yes        |
| [path-206]                             | Prompt] [prompt-207]                   |              |            |
| **[docs/prompts-codex.md] [path-193]** | **[Codex Automation Prompt] [prompt-194]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-193]** | **[Implementation prompts] [prompt-195]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-193]** | **[1 Track a new related repository]   | **one-off**  | **yes**    |
|                                        | [prompt-196]**                         |              |            |
| **[docs/prompts-codex.md] [path-193]** | **[2 Expand service improvement        | **one-off**  | **yes**    |
|                                        | checklists] [prompt-197]**             |              |            |
| **[docs/prompts-codex.md] [path-193]** | **[How to choose a prompt] [prompt-198]** | **evergreen** | **yes**    |
| **[prompts-repos.md] [path-199]**      | **[Related Repository Scan Prompts]    | **evergreen** | **yes**    |
|                                        | [prompt-200]**                         |              |            |
| [prompts/generate-improvements.md]     | [Generate Improvement Checklist Items] | unknown      | yes        |
| [path-204]                             | [prompt-205]                           |              |            |
| [prompts/                              | [Scan for Bright and Dark Patterns]    | unknown      | yes        |
| scan-bright-dark-patterns.md]          | [prompt-209]                           |              |            |
| [path-208]                             |                                        |              |            |
| [prompts/update-risk-model.md]         | [Update Flywheel Risk Model]           | unknown      | yes        |
| [path-210]                             | [prompt-211]                           |              |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`: `docs/prompts-codex.md`,
`prompts-repos.md`, `prompts`._

## [futuroptimist/f2clipboard](https://github.com/futuroptimist/f2clipboard)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| **[docs/prompts-codex-ci-fix.md]       | **[Codex CI-Failure Fix Prompt]        | **evergreen** | **yes**    |
| [path-212]**                           | [prompt-213]**                         |              |            |
| **[docs/prompts-codex-docs.md]         | **[Codex Docs Update Prompt]           | **evergreen** | **yes**    |
| [path-214]**                           | [prompt-215]**                         |              |            |
| **[docs/prompts-codex.md] [path-216]** | **[Codex prompts for the *f2clipboard* | **evergreen** | **yes**    |
|                                        | repo] [prompt-217]**                   |              |            |
| **[docs/prompts-codex.md] [path-216]** | **[Baseline automation prompt]         | **evergreen** | **yes**    |
|                                        | [prompt-218]**                         |              |            |
| **[docs/prompts-codex.md] [path-216]** | **[Roadmap implementation prompt]      | **evergreen** | **yes**    |
|                                        | [prompt-219]**                         |              |            |
| **[docs/prompts-codex.md] [path-216]** | **[Task-specific prompts] [prompt-220]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-216]** | **[2 Emit Markdown to stdout and       | **one-off**  | **yes**    |
|                                        | clipboard] [prompt-221]**              |              |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`:
`docs/prompts-codex-ci-fix.md`, `docs/prompts-codex-docs.md`, `docs/prompts-codex.md`._

## [futuroptimist/axel](https://github.com/futuroptimist/axel)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| [.axel/hillclimb/prompts/code.md]      | [code.md] [path-222]                   | unknown      | yes        |
| [path-222]                             |                                        |              |            |
| [.axel/hillclimb/prompts/              | [critique.md] [path-223]               | unknown      | yes        |
| critique.md] [path-223]                |                                        |              |            |
| [.axel/hillclimb/prompts/plan.md]      | [plan.md] [path-224]                   | unknown      | yes        |
| [path-224]                             |                                        |              |            |
| **[docs/prompts-codex-ci-fix.md]       | **[OpenAI Codex CI-Failure Fix Prompt] | **evergreen** | **yes**    |
| [path-225]**                           | [prompt-226]**                         |              |            |
| **[docs/prompts-codex-spellcheck.md]   | **[Codex Spellcheck Prompt] [prompt-228]** | **evergreen** | **yes**    |
| [path-227]**                           |                                        |              |            |
| **[docs/prompts-codex.md] [path-229]** | **[Automation Prompt] [prompt-230]**   | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-229]** | **[Implementation Prompts] [prompt-231]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-229]** | **[1. Fetch repositories from the GitHub | **one-off**  | **yes**    |
|                                        | API] [prompt-232]**                    |              |            |
| **[docs/prompts-codex.md] [path-229]** | **[2. Update roadmap status]           | **one-off**  | **yes**    |
|                                        | [prompt-233]**                         |              |            |
| **[docs/prompts-codex.md] [path-229]** | **[How to Choose a Prompt] [prompt-234]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-229]** | **[Upgrade Prompt] [prompt-235]**      | **evergreen** | **yes**    |
| **[docs/prompts/prompts-hillclimb.md]  | **[Hillclimb Prompts] [prompt-237]**   | **evergreen** | **yes**    |
| [path-236]**                           |                                        |              |            |
| **[docs/prompts/prompts-hillclimb.md]  | **[Plan Prompt] [prompt-238]**         | **evergreen** | **yes**    |
| [path-236]**                           |                                        |              |            |
| **[docs/prompts/prompts-hillclimb.md]  | **[Code Prompt] [prompt-239]**         | **evergreen** | **yes**    |
| [path-236]**                           |                                        |              |            |
| **[docs/prompts/prompts-hillclimb.md]  | **[Critique Prompt] [prompt-240]**     | **evergreen** | **yes**    |
| [path-236]**                           |                                        |              |            |
| **[docs/prompts/prompts-hillclimb.md]  | **[add-pipx-install.yml] [prompt-241]** | **unknown**  | **yes**    |
| [path-236]**                           |                                        |              |            |
| **[docs/prompts/prompts-hillclimb.md]  | **[docker-compose-mock.yml] [prompt-242]** | **unknown**  | **yes**    |
| [path-236]**                           |                                        |              |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`: `.axel/hillclimb/prompts`,
`docs/prompts-codex-ci-fix.md`, `docs/prompts-codex-spellcheck.md`,
`docs/prompts-codex.md`, `docs/prompts`._

## [futuroptimist/sigma](https://github.com/futuroptimist/sigma)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| **[docs/prompts-codex-cad.md]          | **[Codex CAD Prompt] [prompt-244]**    | **evergreen** | **yes**    |
| [path-243]**                           |                                        |              |            |
| **[docs/prompts-codex-ci-fix.md]       | **[Codex CI-Failure Fix Prompt]        | **evergreen** | **yes**    |
| [path-245]**                           | [prompt-246]**                         |              |            |
| **[docs/prompts-codex-docs.md]         | **[Codex Docs Update Prompt]           | **evergreen** | **yes**    |
| [path-247]**                           | [prompt-248]**                         |              |            |
| **[docs/prompts-codex-spellcheck.md]   | **[Codex Spellcheck Prompt] [prompt-250]** | **evergreen** | **yes**    |
| [path-249]**                           |                                        |              |            |
| **[docs/prompts-codex-tests.md]        | **[Codex Test Addition Prompt]         | **evergreen** | **yes**    |
| [path-251]**                           | [prompt-252]**                         |              |            |
| **[docs/prompts-codex.md] [path-253]** | **[Codex Automation Prompt] [prompt-254]** | **evergreen** | **yes**    |

_Note: Prompt docs also found outside `docs/prompts/codex/`:
`docs/prompts-codex-cad.md`, `docs/prompts-codex-ci-fix.md`,
`docs/prompts-codex-docs.md`, `docs/prompts-codex-spellcheck.md`,
`docs/prompts-codex-tests.md`, `docs/prompts-codex.md`._

## [futuroptimist/gitshelves](https://github.com/futuroptimist/gitshelves)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| [docs/repo_feature_summary_prompt.md]  | [Repo Feature Summary Prompt]          | evergreen    | yes        |
| [path-270]                             | [prompt-271]                           |              |            |
| **[docs/prompts-codex-ci-fix.md]       | **[Codex CI-Failure Fix Prompt]        | **evergreen** | **yes**    |
| [path-255]**                           | [prompt-256]**                         |              |            |
| **[docs/prompts-codex-docs.md]         | **[Codex Docs Update Prompt]           | **evergreen** | **yes**    |
| [path-257]**                           | [prompt-258]**                         |              |            |
| **[docs/prompts-codex-refactor.md]     | **[Codex Refactor Prompt] [prompt-260]** | **evergreen** | **yes**    |
| [path-259]**                           |                                        |              |            |
| **[docs/prompts-codex-spellcheck.md]   | **[Codex Spellcheck Prompt] [prompt-262]** | **evergreen** | **yes**    |
| [path-261]**                           |                                        |              |            |
| **[docs/prompts-codex-tests.md]        | **[Codex Test Prompt] [prompt-264]**   | **evergreen** | **yes**    |
| [path-263]**                           |                                        |              |            |
| **[docs/prompts-codex.md] [path-265]** | **[Codex Automation Prompt] [prompt-266]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-265]** | **[Implementation prompts] [prompt-267]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-265]** | **[1 Document the `--months-per-row`   | **one-off**  | **yes**    |
|                                        | option] [prompt-268]**                 |              |            |
| **[docs/prompts-codex.md] [path-265]** | **[2 Add a spellcheck dictionary]      | **one-off**  | **yes**    |
|                                        | [prompt-269]**                         |              |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`:
`docs/prompts-codex-ci-fix.md`, `docs/prompts-codex-docs.md`,
`docs/prompts-codex-refactor.md`, `docs/prompts-codex-spellcheck.md`,
`docs/prompts-codex-tests.md`, `docs/prompts-codex.md`,
`docs/repo_feature_summary_prompt.md`._

## [futuroptimist/wove](https://github.com/futuroptimist/wove)

| Path                                   | Prompt                                 | Type         | One-click? |
| -------------------------------------- | -------------------------------------- | ------------ | ---------- |
| **[docs/prompts-codex-cad.md]          | **[Codex CAD Prompt] [prompt-273]**    | **evergreen** | **yes**    |
| [path-272]**                           |                                        |              |            |
| **[docs/prompts-codex.md] [path-274]** | **[Codex Automation Prompt] [prompt-275]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-274]** | **[Implementation prompts] [prompt-276]** | **evergreen** | **yes**    |
| **[docs/prompts-codex.md] [path-274]** | **[1 Add a Gauge Swatch section]       | **one-off**  | **yes**    |
|                                        | [prompt-277]**                         |              |            |
| **[docs/prompts-codex.md] [path-274]** | **[2 Document `checks.sh` in the README] | **one-off**  | **yes**    |
|                                        | [prompt-278]**                         |              |            |
| **[docs/prompts-codex.md] [path-274]** | **[3 Add a Crochet Glossary]           | **one-off**  | **yes**    |
|                                        | [prompt-279]**                         |              |            |
| **[docs/prompts-docs.md] [path-280]**  | **[Codex Docs Prompt] [prompt-281]**   | **evergreen** | **yes**    |
| **[docs/prompts-tests.md] [path-282]** | **[Codex Test Prompt] [prompt-283]**   | **evergreen** | **yes**    |

_Note: Prompt docs also found outside `docs/prompts/codex/`:
`docs/prompts-codex-cad.md`, `docs/prompts-codex.md`, `docs/prompts-docs.md`,
`docs/prompts-tests.md`._

## [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube)

| Path                                   | Prompt                                 | Type      | One-click? |
| -------------------------------------- | -------------------------------------- | --------- | ---------- |
| [docs/archived/                        | [Codex Tutorials Implementation        | evergreen | yes        |
| prompt-codex-tutorials.md] [path-284]  | Prompt] [prompt-285]                   |           |            |
| [docs/archived/                        | [Upgrade Prompt] [prompt-286]          | evergreen | yes        |
| prompt-codex-tutorials.md] [path-284]  |                                        |           |            |
| [docs/archived/                        | [Pi Image Improvement Checklist        | evergreen | yes        |
| prompt-pi-image-improvement-checklist.md] | Implementation Prompt] [prompt-288]    |           |            |
| [path-287]                             |                                        |           |            |
| [docs/archived/                        | [Upgrade Prompt] [prompt-289]          | evergreen | yes        |
| prompt-pi-image-improvement-checklist.md] |                                        |           |            |
| [path-287]                             |                                        |           |            |
| [docs/prompts/codex/automation.md]     | [Codex Automation Prompt] [prompt-291] | evergreen | yes        |
| [path-290]                             |                                        |           |            |
| [docs/prompts/codex/automation.md]     | [Upgrade Prompt] [prompt-292]          | evergreen | yes        |
| [path-290]                             |                                        |           |            |
| [docs/prompts/codex/cad.md]            | [Upgrade Prompt] [prompt-294]          | evergreen | yes        |
| [path-293]                             |                                        |           |            |
| [docs/prompts/codex/ci-fix.md]         | [Codex CI-Failure Fix Prompt]          | evergreen | yes        |
| [path-295]                             | [prompt-296]                           |           |            |
| [docs/prompts/codex/ci-fix.md]         | [Upgrade Prompt] [prompt-297]          | evergreen | yes        |
| [path-295]                             |                                        |           |            |
| [docs/prompts/codex/docker-repo.md]    | [Codex Docker Repo Prompt]             | evergreen | yes        |
| [path-298]                             | [prompt-299]                           |           |            |
| [docs/prompts/codex/docker-repo.md]    | [Upgrade Prompt] [prompt-300]          | evergreen | yes        |
| [path-298]                             |                                        |           |            |
| [docs/prompts/codex/docs.md]           | [Codex Documentation Prompt]           | evergreen | yes        |
| [path-301]                             | [prompt-302]                           |           |            |
| [docs/prompts/codex/docs.md]           | [Upgrade Prompt] [prompt-303]          | evergreen | yes        |
| [path-301]                             |                                        |           |            |
| [docs/prompts/codex/elex.md]           | [Codex Electronics Prompt]             | evergreen | yes        |
| [path-304]                             | [prompt-305]                           |           |            |
| [docs/prompts/codex/elex.md]           | [Upgrade Prompt] [prompt-306]          | evergreen | yes        |
| [path-304]                             |                                        |           |            |
| [docs/prompts/codex/pi-image.md]       | [Codex Pi Image Prompt] [prompt-310]   | evergreen | yes        |
| [path-309]                             |                                        |           |            |
| [docs/prompts/codex/pi-image.md]       | [Upgrade Prompt] [prompt-311]          | evergreen | yes        |
| [path-309]                             |                                        |           |            |
| [docs/prompts/codex/                   | [Codex Pi token.place & dspace Prompt] | evergreen | yes        |
| pi-token-dspace.md] [path-312]         | [prompt-313]                           |           |            |
| [docs/prompts/codex/                   | [Upgrade Prompt] [prompt-314]          | evergreen | yes        |
| pi-token-dspace.md] [path-312]         |                                        |           |            |
| [docs/prompts/codex/spellcheck.md]     | [Sugarkube Codex Spellcheck Prompt]    | evergreen | yes        |
| [path-315]                             | [prompt-316]                           |           |            |
| [docs/prompts/codex/spellcheck.md]     | [Upgrade Prompt] [prompt-317]          | evergreen | yes        |
| [path-315]                             |                                        |           |            |
| [docs/prompts/codex/tests.md]          | [Codex Tests Prompt] [prompt-319]      | evergreen | yes        |
| [path-318]                             |                                        |           |            |
| [docs/prompts/codex/tests.md]          | [Upgrade Prompt] [prompt-320]          | evergreen | yes        |
| [path-318]                             |                                        |           |            |
| [docs/prompts/simplification.md]       | [Codebase Simplification Prompt]       | evergreen | yes        |
| [path-321]                             | [prompt-322]                           |           |            |
| [docs/prompts/simplification.md]       | [Before you run the prompt]            | evergreen | yes        |
| [path-321]                             | [prompt-323]                           |           |            |
| [docs/prompts/simplification.md]       | [Upgrade Prompt] [prompt-324]          | evergreen | yes        |
| [path-321]                             |                                        |           |            |

_Note: Prompt docs also found outside `docs/prompts/codex/`: `docs/archived`,
`docs/prompts`._

## [futuroptimist/pr-reaper](https://github.com/futuroptimist/pr-reaper)

| Path                               | Prompt                                 | Type      | One-click? |
| ---------------------------------- | -------------------------------------- | --------- | ---------- |
| [docs/prompts/codex/automation.md] | [Codex Automation Prompt] [prompt-326] | evergreen | yes        |
| [path-325]                         |                                        |           |            |

## [futuroptimist/jobbot3000](https://github.com/futuroptimist/jobbot3000)

| Path                                | Prompt                                 | Type      | One-click? |
| ----------------------------------- | -------------------------------------- | --------- | ---------- |
| [docs/prompts/codex/                | [Codex Accessibility Prompt]           | evergreen | yes        |
| accessibility.md] [path-327]        | [prompt-328]                           |           |            |
| [docs/prompts/codex/automation.md]  | [Codex Automation Prompt] [prompt-330] | evergreen | yes        |
| [path-329]                          |                                        |           |            |
| [docs/prompts/codex/chore.md]       | [Codex Chore Prompt] [prompt-332]      | evergreen | yes        |
| [path-331]                          |                                        |           |            |
| [docs/prompts/codex/chore.md]       | [Upgrade Prompt] [prompt-333]          | evergreen | yes        |
| [path-331]                          |                                        |           |            |
| [docs/prompts/codex/ci.md]          | [Codex CI Prompt] [prompt-335]         | evergreen | yes        |
| [path-334]                          |                                        |           |            |
| [docs/prompts/codex/docs.md]        | [Codex Docs Prompt] [prompt-337]       | evergreen | yes        |
| [path-336]                          |                                        |           |            |
| [docs/prompts/codex/feature.md]     | [Codex Feature Prompt] [prompt-339]    | evergreen | yes        |
| [path-338]                          |                                        |           |            |
| [docs/prompts/codex/fix.md]         | [Codex Fix Prompt] [prompt-341]        | evergreen | yes        |
| [path-340]                          |                                        |           |            |
| [docs/prompts/codex/                | [Codex Localization Prompt]            | evergreen | yes        |
| localization.md] [path-343]         | [prompt-344]                           |           |            |
| [docs/prompts/codex/                | [Upgrade Prompt] [prompt-345]          | evergreen | yes        |
| localization.md] [path-343]         |                                        |           |            |
| [docs/prompts/codex/performance.md] | [Codex Performance Prompt]             | evergreen | yes        |
| [path-346]                          | [prompt-347]                           |           |            |
| [docs/prompts/codex/refactor.md]    | [Codex Refactor Prompt] [prompt-349]   | evergreen | yes        |
| [path-348]                          |                                        |           |            |
| [docs/prompts/codex/security.md]    | [Codex Security Prompt] [prompt-351]   | evergreen | yes        |
| [path-350]                          |                                        |           |            |
| [docs/prompts/codex/security.md]    | [Upgrade Prompt] [prompt-352]          | evergreen | yes        |
| [path-350]                          |                                        |           |            |
| [docs/prompts/codex/                | [Codex Simplification Prompt]          | evergreen | yes        |
| simplification.md] [path-353]       | [prompt-354]                           |           |            |
| [docs/prompts/codex/                | [Upgrade Prompt] [prompt-355]          | evergreen | yes        |
| simplification.md] [path-353]       |                                        |           |            |
| [docs/prompts/codex/spellcheck.md]  | [Codex Spellcheck Prompt] [prompt-357] | evergreen | yes        |
| [path-356]                          |                                        |           |            |
| [docs/prompts/codex/style.md]       | [Codex Style Prompt] [prompt-359]      | evergreen | yes        |
| [path-358]                          |                                        |           |            |
| [docs/prompts/codex/test.md]        | [Codex Test Prompt] [prompt-361]       | evergreen | yes        |
| [path-360]                          |                                        |           |            |

## [futuroptimist/danielsmith.io](https://github.com/futuroptimist/danielsmith.io)

| Path                               | Prompt                                 | Type      | One-click? |
| ---------------------------------- | -------------------------------------- | --------- | ---------- |
| [docs/prompts/codex/automation.md] | [Codex Automation Prompt] [prompt-364] | evergreen | yes        |
| [path-363]                         |                                        |           |            |
| [docs/prompts/codex/automation.md] | [Implementation prompts] [prompt-365]  | evergreen | yes        |
| [path-363]                         |                                        |           |            |
| [docs/prompts/codex/automation.md] | [How to choose a prompt] [prompt-366]  | evergreen | yes        |
| [path-363]                         |                                        |           |            |
| [docs/prompts/codex/automation.md] | [Upgrade Prompt] [prompt-367]          | evergreen | yes        |
| [path-363]                         |                                        |           |            |

## TODO Prompts for Other Repos

# Prompt Docs TODOs

Track outstanding prompt documentation work across repositories. Add rows below as TODOs
emerge.

| Repo                    | Suggested Prompt                                    | Type      | Notes |
| ----------------------- | --------------------------------------------------- | --------- | ----- |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | evergreen |       |
| dspace                  | prompts-codex-ci-fix.md] [path-96]                  |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | evergreen |       |
| dspace                  | prompts-codex-meta.md] [path-103]                   |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | evergreen |       |
| dspace                  | prompts-codex-upgrader.md] [path-106]               |           |       |
| futuroptimist/axel      | [docs/prompts-codex-ci-fix.md] [path-225]           | evergreen |       |
| futuroptimist/axel      | [docs/prompts-codex-spellcheck.md] [path-227]       | evergreen |       |
| futuroptimist/          | [docs/prompts-codex-ci-fix.md] [path-212]           | evergreen |       |
| f2clipboard             |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-docs.md] [path-214]             | evergreen |       |
| f2clipboard             |                                                     |           |       |
| futuroptimist/flywheel  | [docs/prompts/codex/automation.md] [path-11]        | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/cad.md] [path-16]               | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/ci-fix.md] [path-18]            | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/cleanup.md] [path-23]           | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/fuzzing.md] [path-25]           | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/merge-conflicts.md] [path-28]   | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/physics.md] [path-31]           | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/prompt-glean-repos.md]          | evergreen |       |
|                         | [path-34]                                           |           |       |
| futuroptimist/flywheel  | [docs/prompts/codex/propagate.md] [path-36]         | evergreen |       |
| futuroptimist/flywheel  | [docs/prompts/codex/spellcheck.md] [path-39]        | evergreen |       |
| futuroptimist/          | [docs/prompts-codex-spellcheck.md] [todo-368]       | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-video-script-ideas.md]          | evergreen |       |
| futuroptimist           | [todo-369]                                          |           |       |
| futuroptimist/          | [docs/prompts-codex-video-script.md] [todo-370]     | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex.md] [todo-371]                  | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts/codex/automation.md] [path-50]        | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts/codex/cad.md] [path-55]               | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts/codex/cleanup.md] [path-62]           | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts/codex/fuzzing.md] [path-65]           | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts/codex/physics.md] [path-68]           | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts/codex/propagate.md] [path-71]         | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts/codex/spellcheck.md] [path-74]        | evergreen |       |
| futuroptimist           |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-ci-fix.md] [path-255]           | evergreen |       |
| gitshelves              |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-docs.md] [path-257]             | evergreen |       |
| gitshelves              |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-refactor.md] [path-259]         | evergreen |       |
| gitshelves              |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-spellcheck.md] [path-261]       | evergreen |       |
| gitshelves              |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-tests.md] [path-263]            | evergreen |       |
| gitshelves              |                                                     |           |       |
| futuroptimist/sigma     | [docs/prompts-codex-cad.md] [path-243]              | evergreen |       |
| futuroptimist/sigma     | [docs/prompts-codex-ci-fix.md] [path-245]           | evergreen |       |
| futuroptimist/sigma     | [docs/prompts-codex-docs.md] [path-247]             | evergreen |       |
| futuroptimist/sigma     | [docs/prompts-codex-spellcheck.md] [path-249]       | evergreen |       |
| futuroptimist/sigma     | [docs/prompts-codex-tests.md] [path-251]            | evergreen |       |
| futuroptimist/sigma     | [docs/prompts-codex.md] [path-253]                  | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-cad.md] [todo-372]              | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-ci-fix.md] [todo-373]           | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-docker-repo.md] [todo-374]      | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-docs.md] [todo-375]             | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-elex.md] [todo-376]             | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-pi-image.md] [todo-377]         | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-spellcheck.md] [todo-378]       | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex-tests.md] [todo-379]            | evergreen |       |
| futuroptimist/sugarkube | [docs/prompts-codex.md] [todo-380]                  | evergreen |       |
| futuroptimist/          | [docs/prompts-codex-chore.md] [path-175]            | evergreen |       |
| token.place             |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-ci-fix.md] [path-177]           | evergreen |       |
| token.place             |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-docs.md] [path-179]             | evergreen |       |
| token.place             |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-feature.md] [path-181]          | evergreen |       |
| token.place             |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-refactor.md] [path-183]         | evergreen |       |
| token.place             |                                                     |           |       |
| futuroptimist/          | [docs/prompts-codex-security.md] [path-185]         | evergreen |       |
| token.place             |                                                     |           |       |
| futuroptimist/wove      | [docs/prompts-codex-cad.md] [path-272]              | evergreen |       |
| futuroptimist/flywheel  | [docs/pms/2025-08-09-spellcheck-prompt-summary.md]  | one-off   |       |
|                         | [path-1]                                            |           |       |
| futuroptimist/flywheel  | [docs/pms/                                          | one-off   |       |
|                         | 2025-08-10-untriaged-in-prompt-summary.md] [path-3] |           |       |
| futuroptimist/flywheel  | [docs/pms/2025-08-15-prompt-summary-spellcheck.md]  | one-off   |       |
|                         | [path-5]                                            |           |       |
| futuroptimist/flywheel  | [docs/pms/2025-08-16-prompt-docs-run-checks.md]     | one-off   |       |
|                         | [path-7]                                            |           |       |
| futuroptimist/flywheel  | [docs/pms/2025-08-23-prompt-docs-newline.md]        | one-off   |       |
|                         | [path-9]                                            |           |       |
| democratizedspace/      | [docs/prompts-outages.md] [path-79]                 | unknown   |       |
| dspace                  |                                                     |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | unknown   |       |
| dspace                  | prompts-accessibility.md] [path-82]                 |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/prompts-audit.md]       | unknown   |       |
| dspace                  | [path-85]                                           |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/prompts-backend.md]     | unknown   |       |
| dspace                  | [path-88]                                           |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/prompts-backups.md]     | unknown   |       |
| dspace                  | [path-91]                                           |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/prompts-docs.md]        | unknown   |       |
| dspace                  | [path-118]                                          |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | unknown   |       |
| dspace                  | prompts-frontend.md] [path-123]                     |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | unknown   |       |
| dspace                  | prompts-monitoring.md] [path-134]                   |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/prompts-outages.md]     | unknown   |       |
| dspace                  | [path-145]                                          |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | unknown   |       |
| dspace                  | prompts-playwright-tests.md] [path-147]             |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/                        | unknown   |       |
| dspace                  | prompts-refactors.md] [path-166]                    |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/prompts-secrets.md]     | unknown   |       |
| dspace                  | [path-169]                                          |           |       |
| democratizedspace/      | [frontend/src/pages/docs/md/prompts-vitest.md]      | unknown   |       |
| dspace                  | [path-172]                                          |           |       |
| futuroptimist/flywheel  | [docs/prompts/summary.md] [path-42]                 | unknown   |       |
| futuroptimist/gabriel   | [prompts-repos.md] [path-199]                       | unknown   |       |
| futuroptimist/gabriel   | [prompts/README.md] [path-201]                      | unknown   |       |
| futuroptimist/          | [docs/repo_feature_summary_prompt.md] [path-270]    | unknown   |       |
| gitshelves              |                                                     |           |       |
| futuroptimist/wove      | [docs/prompts-docs.md] [path-280]                   | unknown   |       |
| futuroptimist/wove      | [docs/prompts-tests.md] [path-282]                  | unknown   |       |


[path-1]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-09-spellcheck-prompt-summary.md
[prompt-2]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-09-spellcheck-prompt-summary.md#spellcheck-prompt-summary-malformed
[path-3]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-10-untriaged-in-prompt-summary.md
[prompt-4]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-10-untriaged-in-prompt-summary.md#spellcheck-untriaged-header
[path-5]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-15-prompt-summary-spellcheck.md
[prompt-6]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-15-prompt-summary-spellcheck.md#prompt-summary-spellcheck-failure
[path-7]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-16-prompt-docs-run-checks.md
[prompt-8]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-16-prompt-docs-run-checks.md#prompt-docs-workflow-run-checks-failure
[path-9]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-23-prompt-docs-newline.md
[prompt-10]: https://github.com/futuroptimist/flywheel/blob/main/docs/pms/
    2025-08-23-prompt-docs-newline.md#2025-08-23-prompt-docs-newline
[path-11]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    automation.md
[prompt-12]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    automation.md#codex-automation-prompt
[prompt-13]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    automation.md#implementation-prompts
[prompt-14]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    automation.md#how-to-choose-a-prompt
[prompt-15]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    automation.md#upgrade-prompt
[path-16]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/cad.md
[prompt-17]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    cad.md#upgrade-prompt
[path-18]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    ci-fix.md
[prompt-19]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    ci-fix.md#openai-codex-ci-failure-fix-prompt
[prompt-20]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    ci-fix.md#2-commit-and-propagate
[prompt-21]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    ci-fix.md#4-further-reading-references
[prompt-22]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    ci-fix.md#upgrade-prompt
[path-23]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    cleanup.md
[prompt-24]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    cleanup.md#upgrade-prompt
[path-25]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    fuzzing.md
[prompt-26]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    fuzzing.md#openai-codex-fuzzing-prompt
[prompt-27]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    fuzzing.md#upgrade-prompt
[path-28]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    merge-conflicts.md
[prompt-29]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    merge-conflicts.md#codex-merge-conflicts-prompt
[prompt-30]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    merge-conflicts.md#upgrade-prompt
[path-31]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    physics.md
[prompt-32]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    physics.md#upgrade-prompt
[path-33]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    prompt-docs-triage.md
[path-34]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    prompt-glean-repos.md
[prompt-35]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    prompt-glean-repos.md#openai-codex-repo-glean-prompt
[path-36]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    propagate.md
[prompt-37]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    propagate.md#codex-prompt-propagation-prompt
[prompt-38]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    propagate.md#upgrade-prompt
[path-39]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    spellcheck.md
[prompt-40]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    spellcheck.md#codex-spellcheck-prompt
[prompt-41]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/codex/
    spellcheck.md#upgrade-prompt
[path-42]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/summary.md
[prompt-43]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/
    summary.md#todo-prompts-for-other-repos
[prompt-44]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts/
    summary.md#prompt-docs-todos
[path-45]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-major-filter.md
[prompt-46]: https://github.com/futuroptimist/flywheel/blob/main/docs/
    prompts-major-filter.md#prompt-docs-major-filter
[prompt-47]: https://github.com/futuroptimist/flywheel/blob/main/docs/
    prompts-major-filter.md#scriptsupdatepromptdocssummarypy
[path-48]: https://github.com/futuroptimist/flywheel/blob/main/docs/prompts-salient.md
[prompt-49]: https://github.com/futuroptimist/flywheel/blob/main/docs/
    prompts-salient.md#salient-prompt-launcher
[path-50]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    automation.md
[prompt-51]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    automation.md#codex-automation-prompt
[prompt-52]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    automation.md#implementation-prompts
[prompt-53]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    automation.md#how-to-choose-a-prompt
[prompt-54]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    automation.md#upgrade-prompt
[path-55]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    cad.md
[prompt-56]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    cad.md#upgrade-prompt
[path-57]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    ci-fix.md
[prompt-58]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    ci-fix.md#openai-codex-ci-failure-fix-prompt
[prompt-59]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    ci-fix.md#2-committing-propagating
[prompt-60]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    ci-fix.md#3-further-reading-references
[prompt-61]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    ci-fix.md#upgrade-prompt
[path-62]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    cleanup.md
[prompt-63]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    cleanup.md#obsolete-prompt-cleanup
[prompt-64]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    cleanup.md#upgrade-prompt
[path-65]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    fuzzing.md
[prompt-66]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    fuzzing.md#openai-codex-fuzzing-prompt
[prompt-67]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    fuzzing.md#upgrade-prompt
[path-68]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    physics.md
[prompt-69]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    physics.md#openai-codex-physics-explainer-prompt
[prompt-70]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    physics.md#upgrade-prompt
[path-71]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    propagate.md
[prompt-72]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    propagate.md#codex-prompt-propagation-prompt
[prompt-73]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    propagate.md#upgrade-prompt
[path-74]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    spellcheck.md
[prompt-75]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    spellcheck.md#codex-spellcheck-prompt
[prompt-76]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    spellcheck.md#upgrade-prompt
[path-77]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    video-script-ideas.md
[prompt-78]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts/codex/
    video-script-ideas.md#video-script-ideas-prompt
[path-79]: https://github.com/democratizedspace/dspace/blob/v3/docs/prompts-outages.md
[prompt-80]: https://github.com/democratizedspace/dspace/blob/v3/docs/
    prompts-outages.md#outage-prompts-for-the-dspace-repo
[prompt-81]: https://github.com/democratizedspace/dspace/blob/v3/docs/
    prompts-outages.md#upgrader-prompt
[path-82]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-accessibility.md
[prompt-83]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-accessibility.md#accessibility-prompts-for-the-dspace-repo
[prompt-84]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-accessibility.md#upgrader-prompt
[path-85]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-audit.md
[prompt-86]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-audit.md#dependency-audit-prompts-for-the-dspace-repo
[prompt-87]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-audit.md#upgrader-prompt
[path-88]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-backend.md
[prompt-89]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-backend.md#backend-prompts-for-the-dspace-repo
[prompt-90]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-backend.md#upgrader-prompt
[path-91]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-backups.md
[prompt-92]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-backups.md#backup-prompts-for-the-dspace-repo
[prompt-93]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-backups.md#upgrader-prompt
[path-94]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-chat-ui.md
[prompt-95]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-chat-ui.md#chat-ui-prompts-for-the-dspace-repo
[path-96]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-ci-fix.md
[prompt-97]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-ci-fix.md#openai-codex-ci-failure-fix-prompt
[prompt-98]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-ci-fix.md#upgrader-prompt
[path-99]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-merge-conflicts.md
[prompt-100]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-merge-conflicts.md#codex-merge-conflict-prompt
[prompt-101]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-merge-conflicts.md#upgrade-prompt
[prompt-102]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-merge-conflicts.md#upgrader-prompt
[path-103]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-meta.md
[prompt-104]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-meta.md#codex-meta-prompt
[prompt-105]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-meta.md#upgrader-prompt
[path-106]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-upgrader.md
[prompt-107]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-upgrader.md#codex-prompt-upgrader
[prompt-108]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex-upgrader.md#upgrader-prompt
[path-109]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md
[prompt-110]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#writing-great-codex-prompts-for-the-dspace-repo
[prompt-111]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#related-prompt-guides
[prompt-112]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#1-quick-start-web-vs-cli
[prompt-113]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#2-prompt-ingredients
[prompt-114]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#3-reusable-template
[prompt-115]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#upgrade-prompt
[prompt-116]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#prompt-upgrader
[prompt-117]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-codex.md#upgrader-prompt
[path-118]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-docs.md
[prompt-119]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-docs.md#documentation-prompts-for-the-dspace-repo
[prompt-120]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-docs.md#proofreading-prompt
[prompt-121]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-docs.md#cross-link-check-prompt
[prompt-122]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-docs.md#upgrader-prompt
[path-123]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-frontend.md
[prompt-124]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-frontend.md#frontend-prompts-for-the-dspace-repo
[prompt-125]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-frontend.md#upgrader-prompt
[path-126]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md
[prompt-127]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md#writing-great-item-prompts-for-the-dspace-repository
[prompt-128]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md#1-quick-start-web-vs-cli
[prompt-129]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md#2-prompt-ingredients
[prompt-130]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md#3-reusable-template
[prompt-131]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md#implementation-prompt
[prompt-132]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md#upgrade-prompt-for-existing-items
[prompt-133]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-items.md#upgrader-prompt
[path-134]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-monitoring.md
[prompt-135]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-monitoring.md#monitoring-prompts-for-the-dspace-repository
[prompt-136]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-monitoring.md#upgrader-prompt
[path-137]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md
[prompt-138]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md#writing-great-npc-prompts-for-the-dspace-repo
[prompt-139]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md#1-quick-start-web-vs-cli
[prompt-140]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md#2-prompt-ingredients
[prompt-141]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md#3-reusable-template
[prompt-142]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md#implementation-prompt
[prompt-143]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md#upgrade-prompt-for-existing-npcs
[prompt-144]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-npcs.md#upgrader-prompt
[path-145]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-outages.md
[prompt-146]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-outages.md#outage-prompts
[path-147]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-playwright-tests.md
[prompt-148]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-playwright-tests.md#playwright-test-prompts-for-the-dspace-repo
[prompt-149]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-playwright-tests.md#upgrader-prompt
[path-150]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md
[prompt-151]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md#writing-great-process-prompts-for-the-dspace-repo
[prompt-152]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md#1-quick-start-web-vs-cli
[prompt-153]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md#2-prompt-ingredients
[prompt-154]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md#3-reusable-template
[prompt-155]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md#implementation-prompt
[prompt-156]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md#upgrade-prompt-for-existing-processes
[prompt-157]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-processes.md#upgrader-prompt
[path-158]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md
[prompt-159]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md#writing-great-quest-prompts-for-the-dspace-repo
[prompt-160]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md#1-quick-start-web-vs-cli
[prompt-161]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md#2-prompt-ingredients
[prompt-162]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md#3-reusable-template
[prompt-163]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md#implementation-prompt
[prompt-164]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md#upgrade-prompt-for-new-quests
[prompt-165]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-quests.md#upgrader-prompt
[path-166]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-refactors.md
[prompt-167]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-refactors.md#refactor-prompts-for-the-dspace-repo
[prompt-168]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-refactors.md#upgrader-prompt
[path-169]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-secrets.md
[prompt-170]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-secrets.md#secret-scanning-prompts-for-the-dspace-repo
[prompt-171]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-secrets.md#upgrader-prompt
[path-172]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-vitest.md
[prompt-173]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-vitest.md#vitest-test-prompts-for-the-dspace-repo
[prompt-174]: https://github.com/democratizedspace/dspace/blob/v3/frontend/src/pages/docs/
    md/prompts-vitest.md#upgrader-prompt
[path-175]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-chore.md
[prompt-176]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-chore.md#codex-chore-prompt
[path-177]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-ci-fix.md
[prompt-178]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt
[path-179]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-docs.md
[prompt-180]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-docs.md#codex-docs-update-prompt
[path-181]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-feature.md
[prompt-182]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-feature.md#codex-feature-prompt
[path-183]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-refactor.md
[prompt-184]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-refactor.md#codex-refactor-prompt
[path-185]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-security.md
[prompt-186]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex-security.md#codex-security-review-prompt
[path-187]: https://github.com/futuroptimist/token.place/blob/main/docs/prompts-codex.md
[prompt-188]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex.md#tokenplace-codex-prompt
[prompt-189]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex.md#specialized-prompts
[prompt-190]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex.md#implementation-prompts
[prompt-191]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex.md#1-document-environment-variables-in-readme
[prompt-192]: https://github.com/futuroptimist/token.place/blob/main/docs/
    prompts-codex.md#2-add-api-rate-limit-test
[path-193]: https://github.com/futuroptimist/gabriel/blob/main/docs/prompts-codex.md
[prompt-194]: https://github.com/futuroptimist/gabriel/blob/main/docs/
    prompts-codex.md#codex-automation-prompt
[prompt-195]: https://github.com/futuroptimist/gabriel/blob/main/docs/
    prompts-codex.md#implementation-prompts
[prompt-196]: https://github.com/futuroptimist/gabriel/blob/main/docs/
    prompts-codex.md#1-track-a-new-related-repository
[prompt-197]: https://github.com/futuroptimist/gabriel/blob/main/docs/
    prompts-codex.md#2-expand-service-improvement-checklists
[prompt-198]: https://github.com/futuroptimist/gabriel/blob/main/docs/
    prompts-codex.md#how-to-choose-a-prompt
[path-199]: https://github.com/futuroptimist/gabriel/blob/main/prompts-repos.md
[prompt-200]: https://github.com/futuroptimist/gabriel/blob/main/
    prompts-repos.md#related-repository-scan-prompts
[path-201]: https://github.com/futuroptimist/gabriel/blob/main/prompts/README.md
[prompt-202]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    README.md#prompt-templates
[prompt-203]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    README.md#prompt-catalog
[path-204]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    generate-improvements.md
[prompt-205]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    generate-improvements.md#generate-improvement-checklist-items
[path-206]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    refresh-related-projects.md
[prompt-207]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    refresh-related-projects.md#codex-related-projects-refresh-prompt
[path-208]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    scan-bright-dark-patterns.md
[prompt-209]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    scan-bright-dark-patterns.md#scan-for-bright-and-dark-patterns
[path-210]: https://github.com/futuroptimist/gabriel/blob/main/prompts/update-risk-model.md
[prompt-211]: https://github.com/futuroptimist/gabriel/blob/main/prompts/
    update-risk-model.md#update-flywheel-risk-model
[path-212]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex-ci-fix.md
[prompt-213]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt
[path-214]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex-docs.md
[prompt-215]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex-docs.md#codex-docs-update-prompt
[path-216]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/prompts-codex.md
[prompt-217]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex.md#codex-prompts-for-the-f2clipboard-repo
[prompt-218]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex.md#baseline-automation-prompt
[prompt-219]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex.md#roadmap-implementation-prompt
[prompt-220]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex.md#task-specific-prompts
[prompt-221]: https://github.com/futuroptimist/f2clipboard/blob/main/docs/
    prompts-codex.md#2-emit-markdown-to-stdout-and-clipboard
[path-222]: https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/
    code.md
[path-223]: https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/
    critique.md
[path-224]: https://github.com/futuroptimist/axel/blob/main/.axel/hillclimb/prompts/
    plan.md
[path-225]: https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex-ci-fix.md
[prompt-226]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex-ci-fix.md#openai-codex-ci-failure-fix-prompt
[path-227]: https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex-spellcheck.md
[prompt-228]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex-spellcheck.md#codex-spellcheck-prompt
[path-229]: https://github.com/futuroptimist/axel/blob/main/docs/prompts-codex.md
[prompt-230]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex.md#automation-prompt
[prompt-231]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex.md#implementation-prompts
[prompt-232]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex.md#1-fetch-repositories-from-the-github-api
[prompt-233]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex.md#2-update-roadmap-status
[prompt-234]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex.md#how-to-choose-a-prompt
[prompt-235]: https://github.com/futuroptimist/axel/blob/main/docs/
    prompts-codex.md#upgrade-prompt
[path-236]: https://github.com/futuroptimist/axel/blob/main/docs/prompts/
    prompts-hillclimb.md
[prompt-237]: https://github.com/futuroptimist/axel/blob/main/docs/prompts/
    prompts-hillclimb.md#hillclimb-prompts
[prompt-238]: https://github.com/futuroptimist/axel/blob/main/docs/prompts/
    prompts-hillclimb.md#plan-prompt
[prompt-239]: https://github.com/futuroptimist/axel/blob/main/docs/prompts/
    prompts-hillclimb.md#code-prompt
[prompt-240]: https://github.com/futuroptimist/axel/blob/main/docs/prompts/
    prompts-hillclimb.md#critique-prompt
[prompt-241]: https://github.com/futuroptimist/axel/blob/main/docs/prompts/
    prompts-hillclimb.md#add-pipx-installyml
[prompt-242]: https://github.com/futuroptimist/axel/blob/main/docs/prompts/
    prompts-hillclimb.md#docker-compose-mockyml
[path-243]: https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-cad.md
[prompt-244]: https://github.com/futuroptimist/sigma/blob/main/docs/
    prompts-codex-cad.md#codex-cad-prompt
[path-245]: https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-ci-fix.md
[prompt-246]: https://github.com/futuroptimist/sigma/blob/main/docs/
    prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt
[path-247]: https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-docs.md
[prompt-248]: https://github.com/futuroptimist/sigma/blob/main/docs/
    prompts-codex-docs.md#codex-docs-update-prompt
[path-249]: https://github.com/futuroptimist/sigma/blob/main/docs/
    prompts-codex-spellcheck.md
[prompt-250]: https://github.com/futuroptimist/sigma/blob/main/docs/
    prompts-codex-spellcheck.md#codex-spellcheck-prompt
[path-251]: https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex-tests.md
[prompt-252]: https://github.com/futuroptimist/sigma/blob/main/docs/
    prompts-codex-tests.md#codex-test-addition-prompt
[path-253]: https://github.com/futuroptimist/sigma/blob/main/docs/prompts-codex.md
[prompt-254]: https://github.com/futuroptimist/sigma/blob/main/docs/
    prompts-codex.md#codex-automation-prompt
[path-255]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-ci-fix.md
[prompt-256]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-ci-fix.md#codex-ci-failure-fix-prompt
[path-257]: https://github.com/futuroptimist/gitshelves/blob/main/docs/prompts-codex-docs.md
[prompt-258]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-docs.md#codex-docs-update-prompt
[path-259]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-refactor.md
[prompt-260]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-refactor.md#codex-refactor-prompt
[path-261]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-spellcheck.md
[prompt-262]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-spellcheck.md#codex-spellcheck-prompt
[path-263]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-tests.md
[prompt-264]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex-tests.md#codex-test-prompt
[path-265]: https://github.com/futuroptimist/gitshelves/blob/main/docs/prompts-codex.md
[prompt-266]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex.md#codex-automation-prompt
[prompt-267]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex.md#implementation-prompts
[prompt-268]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex.md#1-document-the---months-per-row-option
[prompt-269]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    prompts-codex.md#2-add-a-spellcheck-dictionary
[path-270]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    repo_feature_summary_prompt.md
[prompt-271]: https://github.com/futuroptimist/gitshelves/blob/main/docs/
    repo_feature_summary_prompt.md#repo-feature-summary-prompt
[path-272]: https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex-cad.md
[prompt-273]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-codex-cad.md#codex-cad-prompt
[path-274]: https://github.com/futuroptimist/wove/blob/main/docs/prompts-codex.md
[prompt-275]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-codex.md#codex-automation-prompt
[prompt-276]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-codex.md#implementation-prompts
[prompt-277]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-codex.md#1-add-a-gauge-swatch-section
[prompt-278]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-codex.md#2-document-checkssh-in-the-readme
[prompt-279]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-codex.md#3-add-a-crochet-glossary
[path-280]: https://github.com/futuroptimist/wove/blob/main/docs/prompts-docs.md
[prompt-281]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-docs.md#codex-docs-prompt
[path-282]: https://github.com/futuroptimist/wove/blob/main/docs/prompts-tests.md
[prompt-283]: https://github.com/futuroptimist/wove/blob/main/docs/
    prompts-tests.md#codex-test-prompt
[path-284]: https://github.com/futuroptimist/sugarkube/blob/main/docs/archived/
    prompt-codex-tutorials.md
[prompt-285]: https://github.com/futuroptimist/sugarkube/blob/main/docs/archived/
    prompt-codex-tutorials.md#codex-tutorials-implementation-prompt
[prompt-286]: https://github.com/futuroptimist/sugarkube/blob/main/docs/archived/
    prompt-codex-tutorials.md#upgrade-prompt
[path-287]: https://github.com/futuroptimist/sugarkube/blob/main/docs/archived/
    prompt-pi-image-improvement-checklist.md
[prompt-288]: https://github.com/futuroptimist/sugarkube/blob/main/docs/archived/
    prompt-pi-image-improvement-checklist.md#pi-image-improvement-checklist-implementation-prompt
[prompt-289]: https://github.com/futuroptimist/sugarkube/blob/main/docs/archived/
    prompt-pi-image-improvement-checklist.md#upgrade-prompt
[path-290]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    automation.md
[prompt-291]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    automation.md#codex-automation-prompt
[prompt-292]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    automation.md#upgrade-prompt
[path-293]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/cad.md
[prompt-294]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    cad.md#upgrade-prompt
[path-295]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    ci-fix.md
[prompt-296]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    ci-fix.md#codex-ci-failure-fix-prompt
[prompt-297]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    ci-fix.md#upgrade-prompt
[path-298]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    docker-repo.md
[prompt-299]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    docker-repo.md#codex-docker-repo-prompt
[prompt-300]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    docker-repo.md#upgrade-prompt
[path-301]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    docs.md
[prompt-302]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    docs.md#codex-documentation-prompt
[prompt-303]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    docs.md#upgrade-prompt
[path-304]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    elex.md
[prompt-305]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    elex.md#codex-electronics-prompt
[prompt-306]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    elex.md#upgrade-prompt
[path-307]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    implement.md
[path-308]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    observability.md
[path-309]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    pi-image.md
[prompt-310]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    pi-image.md#codex-pi-image-prompt
[prompt-311]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    pi-image.md#upgrade-prompt
[path-312]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    pi-token-dspace.md
[prompt-313]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    pi-token-dspace.md#codex-pi-tokenplace-dspace-prompt
[prompt-314]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    pi-token-dspace.md#upgrade-prompt
[path-315]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    spellcheck.md
[prompt-316]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    spellcheck.md#sugarkube-codex-spellcheck-prompt
[prompt-317]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    spellcheck.md#upgrade-prompt
[path-318]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    tests.md
[prompt-319]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    tests.md#codex-tests-prompt
[prompt-320]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/
    tests.md#upgrade-prompt
[path-321]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/
    simplification.md
[prompt-322]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/
    simplification.md#codebase-simplification-prompt
[prompt-323]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/
    simplification.md#before-you-run-the-prompt
[prompt-324]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/
    simplification.md#upgrade-prompt
[path-325]: https://github.com/futuroptimist/pr-reaper/blob/main/docs/prompts/codex/
    automation.md
[prompt-326]: https://github.com/futuroptimist/pr-reaper/blob/main/docs/prompts/codex/
    automation.md#codex-automation-prompt
[path-327]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    accessibility.md
[prompt-328]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    accessibility.md#codex-accessibility-prompt
[path-329]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    automation.md
[prompt-330]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    automation.md#codex-automation-prompt
[path-331]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    chore.md
[prompt-332]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    chore.md#codex-chore-prompt
[prompt-333]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    chore.md#upgrade-prompt
[path-334]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/ci.md
[prompt-335]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    ci.md#codex-ci-prompt
[path-336]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    docs.md
[prompt-337]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    docs.md#codex-docs-prompt
[path-338]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    feature.md
[prompt-339]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    feature.md#codex-feature-prompt
[path-340]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    fix.md
[prompt-341]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    fix.md#codex-fix-prompt
[path-342]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    implement.md
[path-343]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    localization.md
[prompt-344]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    localization.md#codex-localization-prompt
[prompt-345]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    localization.md#upgrade-prompt
[path-346]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    performance.md
[prompt-347]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    performance.md#codex-performance-prompt
[path-348]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    refactor.md
[prompt-349]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    refactor.md#codex-refactor-prompt
[path-350]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    security.md
[prompt-351]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    security.md#codex-security-prompt
[prompt-352]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    security.md#upgrade-prompt
[path-353]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    simplification.md
[prompt-354]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    simplification.md#codex-simplification-prompt
[prompt-355]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    simplification.md#upgrade-prompt
[path-356]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    spellcheck.md
[prompt-357]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    spellcheck.md#codex-spellcheck-prompt
[path-358]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    style.md
[prompt-359]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    style.md#codex-style-prompt
[path-360]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    test.md
[prompt-361]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    test.md#codex-test-prompt
[path-362]: https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/
    upgrade.md
[path-363]: https://github.com/futuroptimist/danielsmith.io/blob/main/docs/prompts/codex/
    automation.md
[prompt-364]: https://github.com/futuroptimist/danielsmith.io/blob/main/docs/prompts/codex/
    automation.md#codex-automation-prompt
[prompt-365]: https://github.com/futuroptimist/danielsmith.io/blob/main/docs/prompts/codex/
    automation.md#implementation-prompts
[prompt-366]: https://github.com/futuroptimist/danielsmith.io/blob/main/docs/prompts/codex/
    automation.md#how-to-choose-a-prompt
[prompt-367]: https://github.com/futuroptimist/danielsmith.io/blob/main/docs/prompts/codex/
    automation.md#upgrade-prompt
[todo-368]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/
    prompts-codex-spellcheck.md
[todo-369]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/
    prompts-codex-video-script-ideas.md
[todo-370]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/
    prompts-codex-video-script.md
[todo-371]: https://github.com/futuroptimist/futuroptimist/blob/main/docs/prompts-codex.md
[todo-372]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-cad.md
[todo-373]: https://github.com/futuroptimist/sugarkube/blob/main/docs/
    prompts-codex-ci-fix.md
[todo-374]: https://github.com/futuroptimist/sugarkube/blob/main/docs/
    prompts-codex-docker-repo.md
[todo-375]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-docs.md
[todo-376]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-elex.md
[todo-377]: https://github.com/futuroptimist/sugarkube/blob/main/docs/
    prompts-codex-pi-image.md
[todo-378]: https://github.com/futuroptimist/sugarkube/blob/main/docs/
    prompts-codex-spellcheck.md
[todo-379]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex-tests.md
[todo-380]: https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts-codex.md

_Updated automatically: 2025-09-26_
