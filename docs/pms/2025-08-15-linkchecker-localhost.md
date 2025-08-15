# Docs linkchecker localhost failure

- **Date**: 2025-08-15
- **Author**: Codex
- **Status**: resolved

## What went wrong
The Docs workflow's link checker attempted to validate links pointing to `localhost` and `127.0.0.1`. These addresses are unreachable in CI and caused connection errors, failing the job.

## Root cause
The linkchecker command did not ignore local development URLs, so it tried to crawl them and exited non-zero when the connections were refused.

## Impact
Documentation changes could not merge while the link check job failed, blocking contributors.

## Actions to take
- Ignore localhost links in linkchecker invocations for workflows and local scripts.
- Add tests ensuring the configuration stays in place.
