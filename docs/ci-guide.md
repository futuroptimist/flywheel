# CI Guide – Why some PRs fail in the `crawl` job

The `crawl` workflow generates a Markdown summary of features across related repositories. Earlier versions attempted to commit that file back to the branch that triggered the run. Pull requests opened by bots like Dependabot use a read‑only `GITHUB_TOKEN`, so the push failed and the job ended with exit code 128.

The workflow now commits `docs/repo-feature-summary.md` only when it runs on the `main` branch. Pull requests opened by bots like Dependabot simply skip that step so the job succeeds. After the PR is merged and a push hits `main`, the workflow updates and commits the summary automatically. You can still generate it locally if you need the file before merging.

## How to update the summary locally
1. Check out the branch you want to update.
2. Run `flywheel crawl --repos-file docs/repo_list.txt --output docs/repo-feature-summary.md`.
3. Commit the updated `docs/repo-feature-summary.md` yourself.

## Workflow naming for CI detection
`flywheel crawl` marks a repository as having CI only when a workflow file
name contains common keywords like `ci`, `test`, `lint`, `build`, `docs`, or
`qa`. A lone `deploy.yml` will be treated as missing CI. Include one of these
keywords in at least one workflow filename so the feature summary reflects your
setup accurately.

## CI best practices
| Scenario | Recommended approach |
|----------|---------------------|
| Internal commits | The workflow will commit the summary when `main` is updated. |
| Dependabot / external PRs | The push step is skipped; merge the PR and let `main` update the summary. |
