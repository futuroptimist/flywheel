# Flask reloader leaves zombie server

- Date: 2025-08-22
- Author: OpenAI Codex
- Status: fixed

## What went wrong
Playwright launched the Flask app with debug mode enabled, which spawned a reloader process. The reloader persisted after tests, leaving the CI job hanging.

## Root cause
`webapp/app.py` ran `app.run(debug=True)` which enabled the auto-reloader. Playwright only terminated the parent process, so the child process continued to serve requests.

## Impact
CI runs for branches touching the webapp never completed, blocking merges.

## Actions to take
- Keep Flask in production mode during tests.
- Monitor future CI runs for lingering processes.
