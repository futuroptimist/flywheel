# CI Guide – Why some PRs fail in the `crawl` job

The `crawl` workflow generates a Markdown summary of features across related repositories. Earlier versions attempted to commit that file back to the branch that triggered the run. Pull requests opened by bots like Dependabot use a read‑only `GITHUB_TOKEN`, so the push failed and the job ended with exit code 128.

The workflow now commits `docs/repo-feature-summary.md` only when it runs on the `main` branch. Pull requests opened by bots like Dependabot simply skip that step so the job succeeds. After the PR is merged and a push hits `main`, the workflow updates and commits the summary automatically. You can still generate it locally if you need the file before merging.

## How to update the summary locally
1. Check out the branch you want to update.
2. Run `flywheel crawl futuroptimist/flywheel futuroptimist/axel --output docs/repo-feature-summary.md`.
3. Commit the updated `docs/repo-feature-summary.md` yourself.

## CI best practices
| Scenario | Recommended approach |
|----------|---------------------|
| Internal commits | The workflow will commit the summary when `main` is updated. |
| Dependabot / external PRs | The push step is skipped; merge the PR and let `main` update the summary. |
