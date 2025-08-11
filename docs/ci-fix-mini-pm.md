# CI Mini Postmortem

## 2025-08-10 – Docs link check failed on Python 3.13

### What went wrong
The link-check job in `.github/workflows/03-docs.yml` failed while installing `linkchecker`.

### Root cause
`actions/setup-python@v4` resolved to Python 3.13, which `linkchecker` does not yet support.

### Impact
Docs workflow runs on `main` were red, obscuring other CI signals.

### Actions to take
- [x] Pin Python to 3.12 in the docs workflow.
- [ ] Monitor `linkchecker` for Python 3.13 compatibility.

---

## 2025-?? – Spellcheck false positive on "Untriaged"

### What went wrong
Spellcheck failed on `docs/prompt-docs-summary.md` due to the word "Untriaged".

### Root cause
The term "Untriaged" was missing from the spellcheck allow list, causing a false positive.

### Impact
CI runs were blocked by the spellcheck job.

### Actions to take
- [x] Add "Untriaged" to the spellcheck dictionary.
- [ ] Regenerate `docs/prompt-docs-summary.md` with sanitized headings.
