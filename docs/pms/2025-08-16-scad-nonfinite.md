# SCAD parser accepted non-finite numbers

- **Date**: 2025-08-16
- **Author**: Codex
- **Status**: resolved

## What went wrong
`parse_scad_vars` converted extremely large numeric literals to `inf` without error, allowing invalid geometry parameters.

## Root cause
Python's float conversion silently returns infinity for values beyond the double-precision range, and the parser lacked validation for finiteness.

## Impact
Non-finite parameters could propagate into fit checks, leading to misleading validations or resource exhaustion during model generation.

## Actions to take
- Validate parsed numbers with `math.isfinite` and raise `ValueError` on non-finite inputs.
- Consider additional range checks for other CAD parameters.
