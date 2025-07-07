# Codex Assistant Rules – v2 (2025-07-06)

This guide unifies **AGENTS.md**, **llms.txt**, and **CLAUDE.md** and is written *for autonomous or semi-autonomous LLM agents*.
Our philosophy is **"move fast, fix-forward, and keep trunk green."** If a change causes breakage, prefer an immediate patch PR over a rollback.

> **Scope:** flywheel itself plus any sibling repos listed in `docs/repo-feature-summary.md`.

---

## 0. Quick-Start Checklist (≤3 min)

1. **Bootstrap**
   - Parse `AGENTS.md`, `README.md`, repo root, and `docs/` folders; build an **index of prompts & workflows** in memory.
2. **Run Quality Gates**
   - `npm run lint && npm test` **or** `uv pip install . && pytest`. Failures? Open an issue titled “🚨 Gate fails on fresh clone”.
3. **Select a Micro-Win**
   - Pick *one* change ≤50 LoC or ≤100 words of docs. Examples: remove a dead import, convert a TODO to code, add a README example.

---

## 1. Commit & PR Etiquette

| Rule | Why |
|------|-----|
| **Atomic commits**: one intent per commit | Speeds up `git bisect` & review |
| **Conventional Commits** (`feat: …`, `fix: …`, `docs: …`) | Keeps changelogs & semver automatic |
| **Tiny PRs (≤400 LoC or  <5 files)** | Review stays <15 min |

A PR template lives at `.github/pull_request_template.md`; keep its check-list green and update it if new automated checks are added.

---

## 2. Fix-Forward Doctrine

*If trunk turns red, ship a patch instead of reverting*

1. Create `fix: hot-patch <summary>` branch off `main`.
2. Add a failing test first when possible.
3. Merge once CI passes; reference the SHA that introduced the break.

---

## 3. Quality Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Test coverage (repo-wide) | ≥80 % | Typical OSS baseline |
| Coverage per-commit | ≥95 % of *previous* commit’s figure | Prevents regressions |
| ESLint / Flake8 errors | 0 | Custom rules can be added under `tools/lint-rules/` |

When coverage is low, agents should auto-generate *minimal* tests that assert public contracts only—never snapshot private state.

---

## 4. Agent Playbooks

### 4.1 Codex / Cursor (code-first)

1. Search for `PROMPT = """` blocks; standardise to **purpose / context / request** format.
2. Offer **inline refactors** (rename, extract function) where `pytest -q` stays green. See MANTRA for agent-driven refactor patterns.

### 4.2 Windsurf (UI-centric)

1. Ensure Storybook stories compile.
2. Create a skeleton-loader placeholder if a component lacks loading state.

### 4.3 Cline (docs-first)

1. If a paragraph in `docs/` exceeds 120 chars line-length, wrap it.
2. Autolink any bare GitHub URLs with Markdown.

---

## 5. Cross-Repo Synergies

1. Duplicate helpers → propose `@futuroptimist/common`.
2. In each repo, sync `.editorconfig`, `.pre-commit-config.yaml`, PR templates and CI workflows.
3. Add a matrix job that runs *this very checklist* against the repo.

---

## 6. Continuous Feedback Loop

On every push, agents must:

- Re-run **Quick-Start Checklist**.
- Attach a comment summarising *why* the change helps the flywheel turn faster.
- Suggest the next micro-win (optional).

---

### Appendix A. Decision Matrix

| Situation | Action |
|-----------|--------|
| Linter fails only | Auto-fix → PR `style: lint --fix` |
| Tests fail but cause obvious typo | Patch + add regression test |
| Ambiguous spec | Open issue titled “❓ Spec Clarification: <area>” |

> **Tip:** Unsure? Leave the code untouched, open an issue, and move on—micro-wins beat mega-PRs every time.
