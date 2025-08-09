# CI Fix Action Items

## Prevent
- [ ] Ensure every CI failure fix includes a dated mini postmortem document.
- [ ] Regenerate `docs/prompt-docs-summary.md` with a valid Markdown table so spellcheck can cover it.
- [ ] Whitelist common physics notation like `precess` and `circ` in the spellcheck dictionary.

## Detect
- [ ] Monitor Playwright installation to keep CI downloads lightweight.

## Mitigate
- [ ] Skip auto-generated docs in spellcheck to prevent false positives.
