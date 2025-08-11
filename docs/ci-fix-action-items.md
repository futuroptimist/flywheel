# CI Fix Action Items

## Prevent
- [x] Ensure every CI failure fix includes a dated mini postmortem document.
- [ ] Regenerate `docs/prompt-docs-summary.md` with a valid Markdown table so spellcheck can cover it.
- [x] Whitelist common physics notation like `precess` and `circ` in the spellcheck dictionary.
- [x] Test templates for required `package-lock.json` files.

## Detect
- [ ] Monitor Playwright installation to keep CI downloads lightweight.
- [ ] Alert on missing lock files in template directories.

## Mitigate
- [x] Whitelist "Untriaged" in the spellcheck dictionary.
- [x] Skip auto-generated docs in spellcheck to prevent false positives.
- [x] Commit missing `package-lock.json` for the JavaScript template.
