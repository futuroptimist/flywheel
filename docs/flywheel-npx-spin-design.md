## Implementation Progress
- **2025-10-26:** Added an `--llm-provider` flag to the Python `flywheel spin`
  CLI so dry-run payloads record the selected backend for future apply flows.
- **2025-10-25:** Added a `--apply none` skip mode to the Python `flywheel spin`
  CLI so operators can record skipped scaffolding without generating files.
- **2025-10-24:** Added a `--apply-all` flag to the Python `flywheel spin`
  CLI so scaffolding can run without prompts, matching the apply-all mode in the
  CLI experience below.
- **2025-10-23:** Added a minimal `--apply` scaffolder to the Python
  `flywheel spin` CLI so heuristics can bootstrap README, docs, and test
  placeholders while the TypeScript apply engine is under active development.
- **2025-10-17:** Added a `--cache-dir` flag to the Python `flywheel spin --dry-run`
  CLI that writes the JSON payload to a hashed filename inside the selected
  directory so repeated runs can reuse cached analysis artifacts.
- **2025-10-16:** Added a `--telemetry on|off|full` override to the Python
  `flywheel spin --dry-run` CLI so automation scripts can persist telemetry
  preferences without hitting the interactive prompt, aligning the current
  implementation with the CLI experience described below.
- **2025-10-10:** Added a Python `flywheel spin --dry-run` subcommand that emits
  heuristic suggestions in JSON. This provides a lightweight preview while the
  npm packaging and LLM integration remain under development.
- **2025-10-11:** Tagged heuristic suggestions with `category` values so the
  dry-run output matches the prompt schema (`docs`, `fix`, `chore`).
- **2025-10-11:** Added `--format table` and `--format markdown` output modes to
  the Python dry-run CLI so it matches the format matrix described below,
  including a stats block and suggestion table for copy/paste workflows.
- **2025-10-12:** Matched the dry-run CI detection to RepoCrawler's keyword
  heuristic so deploy-only workflows no longer mask missing CI.
- **2025-10-13:** Added `flywheel config telemetry` to manage opt-in
  preferences stored under `~/.config/flywheel/config.json` with a
  `FLYWHEEL_CONFIG_DIR` override for sandboxed runs.
- **2025-10-14:** Added `--analyzers` toggles to the Python dry-run CLI so teams
  can focus on specific heuristics while the npm implementation matures. The
  lint analyzer now surfaces an `add-linting` suggestion when projects lack
  pre-commit, ESLint, Ruff, or similar tooling.
- **2025-10-15:** Attached validation commands to the dry-run suggestions so the
  CLI calls out shell checks or test suites operators can run after applying a
  change.
- **2025-10-16:** Added `dependencies` arrays to dry-run suggestions so the
  heuristics align with the prompt schema when future patches require ordering.

## Architecture Overview
```mermaid
graph TD
    A[User runs npx flywheel spin] --> B[CLI Bootstrap]
    B --> C[Project Scanner]
    C -->|Artifacts| D[Embedding Builder]
    D --> E[Vector Store]
    E --> F[Retrieval Engine]
    F --> G[Prompt Orchestrator]
    G --> H[LLM Gateway]
    H --> I[Suggestion Synthesizer]
    I --> J[Suggestion Catalog]
    J --> K{User Selection}
    K -->|Apply| L[Patch Engine]
    K -->|Skip| M[Report Generator]
    L --> N[Git Integration]
    M --> O[Summary Output]
    N --> P[Post-Apply Validation]
    P --> Q[Telemetry Collector]
    O --> Q
```

### Components
- **CLI Bootstrap:** Node entrypoint that resolves the package, ensures dependencies (Python
  bridge, embeddings cache), and dispatches commands.
- **Project Scanner:** Reusable module that enumerates files, extracts metadata, and builds rich
  documents for retrieval. Borrow heuristics from RepoCrawler while abstracting analyzers (AST,
  dependency graphs, metadata) as pluggable providers.
- **Embedding Builder:** Uses selected LLM embedding endpoint (token.place embeddings when GA) with
  local cache and rate limiting.
- **Vector Store:** Local disk-backed store (SQLite + pgvector-like extension via `vectordb`, or
  `chromadb` wrapper) enabling reuse across runs. Provide fallback to in-memory store for ephemeral
  runs.
- **Retrieval Engine:** Hybrid search (semantic + keyword) to gather context for prompt generation.
- **Prompt Orchestrator:** Template-driven prompts referencing prompt doc; includes conversation
  state and tool usage instructions.
- **LLM Gateway:** Adapter pattern to support token.place v1 API, OpenAI, Anthropic. Handles retries,
  exponential backoff, and token accounting.
- **Suggestion Synthesizer:** Normalizes LLM outputs into structured `Suggestion` objects with
  metadata (summary, rationale, diff snippets, confidence, dependencies).
- **Suggestion Catalog:** Ranking + deduping; surfaces grouping (refactor, docs, chore) and tracks
  prerequisites.
- **Patch Engine:** Applies selected suggestions using patch hunks, AST transforms, or invoking
  external scripts. Supports `--dry-run` to emit patches without applying.
- **Telemetry Collector:** Opt-in analytics: command duration, LLM cost, applied suggestions (hash).

## Detailed Design
### Package Structure
```
flywheel/
├── package.json (npm entrypoints)
├── src/
│   ├── cli/
│   │   ├── index.ts (command router)
│   │   ├── spin.ts (main command)
│   │   └── prompts/
│   ├── core/
│   │   ├── scanner/
│   │   ├── embeddings/
│   │   ├── retrieval/
│   │   ├── suggestions/
│   │   ├── apply/
│   │   └── telemetry/
│   ├── adapters/
│   │   ├── llm/
│   │   │   ├── tokenplace.ts
│   │   │   ├── openai.ts
│   │   │   └── anthropic.ts
│   │   └── repo/
│   └── utils/
├── docs/
│   └── prompts/
└── tests/
```
- Reuse existing Python components via Node bindings only if necessary. Primary implementation stays
  in TypeScript to simplify npm distribution.
- Provide optional bridge to Python scanner for advanced heuristics; expose through feature flag.

### CLI Experience
- `npx flywheel spin [path] [options]`
  - `--analyzers` list to enable/disable modules (lint, dependency, test coverage).
  - `--llm-provider tokenplace|openai|anthropic`
  - `--tokenplace-api-key $TOKENPLACE_API_KEY` (environment variable fallback).
  - `--format table|json|markdown`
  - `--apply` (interactive prompt), `--apply-all` (apply without prompts),
    `--apply none` (skip scaffolding while recording the decision)
  - `--dry-run` to output patches without applying.
  - `--cache-dir` for embeddings/vector store.
  - `--telemetry on|off|full`

### Prompting Strategy
- Maintain dedicated prompt docs under `docs/prompts/codex/flywheel-spin.md` referencing context windows,
  instructions, and fallback modes.
- Structure conversation:
  1. System prompt: repo context, style guides, request for suggestions.
  2. Tool message: retrieved chunks (code, docs, tests).
  3. User prompt: ask for top N suggestions with rationale, diff preview, impact level, dependency
     chain.
  4. Assistant response: JSON schema for `Suggestion` objects.

### Suggestion Schema
```ts
interface Suggestion {
  id: string; // deterministic hash of title + primary file
  title: string;
  category: "feature" | "fix" | "refactor" | "docs" | "chore";
  summary: string;
  rationale: string;
  files: string[];
  diffPreview: string; // optional unified diff snippet
  impact: "low" | "medium" | "high";
  confidence: number; // 0-1
  prerequisites: string[]; // other suggestion ids
  applyCommand?: string; // optional command to run
}
```
- CLI renders suggestions in a table with selection indices. Applying suggestions uses diff or
  `applyCommand` if provided (e.g., `npm run lint -- --fix`).

### Integration with Git
- Use `simple-git` or native `child_process` to inspect repo state, create WIP branches, and apply
  patch hunks.
- Validate clean working tree before applying; offer `--allow-dirty` override.
- After applying suggestions, run `npm run lint` and/or `npm run test:ci` when project scripts exist.

### Telemetry and Privacy
- Default telemetry is opt-in via interactive prompt on first run (shipped in the Python CLI).
  Store preference in
  `~/.config/flywheel/config.json`, configurable via `flywheel config telemetry`
  or the `FLYWHEEL_CONFIG_DIR` environment variable.
- Data collected: anonymized command metadata, error codes, LLM cost. No code content unless user
  opts-in (`--telemetry=full`).
- Use `posthog-node` (self-hosted endpoint) or local logging integration.

## Roadmap & Milestones
```mermaid
gantt
    dateFormat  YYYY-MM
    title Flywheel npx Spin Roadmap
    section Foundation
    Repo Audit & Gap Analysis        :done,    a1, 2024-02, 2024-02
    Package Scaffolding              :active,  a2, 2024-03, 2024-04
    TypeScript Core Modules          :         a3, 2024-04, 2024-05
    section Retrieval Pipeline
    Embedding Service Selection      :         b1, 2024-05, 2024-05
    Vector Store Implementation      :         b2, 2024-05, 2024-06
    Prompt Doc Draft                 :         b3, 2024-05, 2024-05
    section Suggestion Engine
    LLM Schema Prototyping           :         c1, 2024-06, 2024-06
    Patch Engine MVP                 :         c2, 2024-06, 2024-07
    User Selection UX                :         c3, 2024-07, 2024-07
    section Release Prep
    Telemetry + Opt-In Flow          :         d1, 2024-07, 2024-07
    Docs & Tutorials                 :         d2, 2024-07, 2024-08
    Beta Program & Feedback          :         d3, 2024-08, 2024-08
    section GA Launch
    npm Publish Automation           :         e1, 2024-08, 2024-08
    GA Release & Announcement        :         e2, 2024-08, 2024-08
    Post-GA Iteration                :         e3, 2024-09, 2024-10
```

### Phase Breakdown
1. **Foundation (Mar–Apr 2024)**
   - Audit existing Python CLI to identify reusable modules.
   - Scaffold TypeScript project structure with ESLint, Prettier, `tsup` bundling.
   - Establish integration tests using `npm run test:ci` with mock repos.

2. **Retrieval Pipeline (May 2024)**
   - Evaluate embedding providers (token.place, OpenAI, local models) for latency and cost.
   - Implement abstraction layer for embeddings with caching to disk.
   - Draft prompt templates and store in version-controlled docs.

3. **Suggestion Engine (Jun–Jul 2024)**
   - Build LLM request/response adapters with strict JSON schema validation.
   - Implement patch generation using diff apply + AST transformations for supported languages.
   - Design interactive selection UI (Inquirer.js or `@clack/prompts`).

4. **Release Preparation (Jul–Aug 2024)**
   - Add telemetry, error handling, and auto-update checks.
   - Create docs: quickstart, configuration, troubleshooting.
   - Launch private beta with seed users, gather feedback, iterate.

5. **GA Launch (Aug 2024 onward)**
   - Automate `npm publish` via GitHub Actions on tagged releases.
   - Coordinate marketing, blog post, and community announcement.
   - Plan post-GA sprints for plugin ecosystem, enterprise auth, and integrations.

## Workstreams & Ownership
| Workstream | Owner | Dependencies | Notes |
|------------|-------|--------------|-------|
| TypeScript CLI Scaffold | Tooling Platform | None | Setup build, lint, test pipelines. |
| Scanner Abstractions | Repo Intelligence Team | CLI scaffold | Share heuristics with RepoCrawler. |
| Embeddings & Vector Store | ML Infra | Scanner | Evaluate token.place vs fallback providers. |
| Prompt Orchestration | Prompt Agent | Embeddings | Maintain prompt docs & testing harness. |
| Suggestion Engine | Core Automation | Prompt Orchestration | JSON schema, ranking, dedupe. |
| Patch Application | Core Automation | Suggestion Engine | Git operations, conflict handling. |
| Telemetry & Analytics | Observability | CLI scaffold | Ensure privacy compliance. |
| Documentation | Docs Agent | All | Quickstart, troubleshooting, API reference. |
| Release Automation | DevOps | All | GitHub Actions, npm access tokens, security scans. |

## Risk Assessment
| Risk | Impact | Likelihood | Mitigations |
|------|--------|------------|-------------|
| token.place v1 API delayed | Medium | Medium | Provide adapters for OpenAI, Anthropic; design provider interface for easy swap. |
| LLM output invalid JSON | High | High | Use streaming parser with repair logic, schema validation, fallback prompts. |
| Large repos exceed token limits | High | Medium | Implement chunking, summarization, and priority-based retrieval. |
| Diff application conflicts | Medium | Medium | Offer manual review mode, git patch fallback, `--dry-run`. |
| npm supply chain security | High | Low | Enable `npm audit`, 2FA publishing, `sigstore` provenance. |
| Telemetry privacy concerns | Medium | Medium | Opt-in flow, anonymization, data retention policy. |

## Testing Strategy
- **Unit Tests:** Cover core modules (scanner, embeddings, retrieval, suggestion parsing, patch
  application). Use `vitest` for TypeScript tests.
- **Integration Tests:** Spin against fixture repos (JavaScript, Python, polyglot) with mocked LLM
  responses using `msw` or recorded transcripts.
- **End-to-End Tests:** GitHub Actions workflow runs `npx flywheel spin --dry-run` on a sample repo
  to validate CLI packaging.
- **Performance Benchmarks:** Measure scan and suggestion generation time on repos of varying sizes.
- **Security Checks:** `npm audit`, `npx license-checker`, secret scanning before release.

## Release Plan
1. **Pre-release (`0.1.0-beta`):** Private npm tag, manual install instructions, gather feedback.
2. **Release Candidate (`1.0.0-rc.1`):** Freeze features, document upgrade path, finalize telemetry.
3. **General Availability (`1.0.0`):** Publish stable tag, announce, update docs + changelog.
4. **Maintenance:** Semver compliance, monthly patch releases, security backports.

### npm Publish Automation
- Configure GitHub Actions workflow triggered on `release/*` tags.
- Steps:
  1. `npm ci`
  2. `npm run lint`
  3. `npm run test:ci`
  4. `npm run build`
  5. `npm publish --access public`
- Use `NPM_TOKEN` secret scoped to publish rights; enforce 2FA on maintainers.

## Operational Readiness Checklist
- [ ] Docs: Quickstart, configuration, troubleshooting, FAQ.
- [ ] Telemetry policy reviewed by legal/compliance.
- [ ] Incident response playbook updated for CLI issues.
- [ ] Support rotation on-call schedule defined.
- [ ] Changelog automation aligned with Release Drafter.
- [ ] `scripts/checks.sh` updated to include TypeScript CLI tests.

## Open Questions
1. Should we ship prebuilt binaries via `pkg` to reduce cold start time, or rely on ts-node/Node
   runtime?
2. What is the minimum Node.js version we must support (e.g., 18 LTS vs 20 LTS)?
3. Do we bundle a lightweight local vector store by default or require external services?
4. How will we handle large binary files or generated assets during scanning to avoid cost spikes?
5. Should suggestion application automatically create git branches or stay on current branch?

## Appendices
### Appendix A: CLI Command Reference (Draft)
| Command | Description | Status |
|---------|-------------|--------|
| `flywheel spin` | Scan repo, generate suggestions. | Draft |
| `flywheel spin --dry-run` | Output suggestions without LLM or patch application (mock data). | Draft |
| `flywheel spin --apply` | Interactive apply mode. | Prototype |
| `flywheel spin --apply-all` | Apply all suggestions with zero prompts (Python CLI scaffolding). | Prototype |
| `flywheel config telemetry` | Manage telemetry preferences. | Shipped |

### Appendix B: Sample Prompt Skeleton
```
<system>
You are Flywheel Automation AI. Analyze the provided repository context and produce high-quality
engineering improvement suggestions. Follow coding standards, maintain test coverage, and limit
responses to valid JSON following the provided schema.
</system>
<user>
Repository metadata: {{metadata}}
Coding conventions: {{styleguides}}
Provide the top {{n}} suggestions ranked by impact. Each suggestion must include summary, rationale,
impacted files, diff preview, dependencies, and confidence score between 0 and 1.
</user>
<assistant>
{"suggestions": [ ... ]}
</assistant>
```

### Appendix C: Beta Feedback Survey Outline
- How relevant were the suggestions? (1-5)
- Did patch application succeed without conflicts? (Yes/No; if no, describe)
- Time taken from command start to completion? (minutes)
- Preferred LLM provider? (token.place/OpenAI/Anthropic/Other)
- Feature requests or pain points?
