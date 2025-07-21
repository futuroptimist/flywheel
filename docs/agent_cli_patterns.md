# Agent CLI Patterns

This project supports structured command output via a `--mode` flag shared by all
`flywheel` sub-commands. Use `--mode human` (default) for plain text or
`--mode jsonl` for newline-delimited JSON. The first line of JSON output includes
`{"total_lines": N}` so tools can anticipate the stream length.

Output from each invocation is cached under `$TMP/flw-cache/<sha256>.log` and
replayed when the same command runs again. This speeds up repeated queries and
guarantees deterministic results for LLM agents.
