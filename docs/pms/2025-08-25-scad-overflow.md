# SCAD variable overflow

## Summary
`parse_scad_vars` accepted numbers exceeding float range and produced infinite values.

## Impact
Unbounded CAD parameters could propagate into fit checks or geometry calculations.

## Root Cause
The parser converted numeric strings without verifying finiteness, so `1e309` became `inf`.

## Resolution
Reject non-finite numbers during parsing and raise `ValueError`.

## Prevention
Add fuzz tests for extreme numeric values.
