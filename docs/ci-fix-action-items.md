# CI Fix Action Items

## Prevent
- [x] Ensure every CI failure fix includes a dated mini postmortem document.
- [ ] Regenerate `docs/prompt-docs-summary.md` with a valid Markdown table so spellcheck can cover it.
- [x] Whitelist common physics notation like `precess` and `circ` in the spellcheck dictionary.
- [x] Pin docs link check workflow to Python 3.12 until `linkchecker` supports newer versions.

## Detect
- [ ] Monitor Playwright installation to keep CI downloads lightweight.
- [ ] Track `linkchecker` releases for Python 3.13 compatibility.

## Mitigate
- [x] Whitelist "Untriaged" in the spellcheck dictionary.
- [x] Skip auto-generated docs in spellcheck to prevent false positives.
