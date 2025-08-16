# SCAD parse validation

## Summary
Malformed variable assignments in SCAD files were silently ignored.

## Impact
Invalid CAD parameters could propagate without notice.

## Root Cause
`parse_scad_vars` failed to validate assignments, skipping non-numeric values.

## Resolution
Raise `ValueError` when an assignment lacks a numeric value.

## Prevention
Add fuzz tests to ensure malformed content triggers errors.
