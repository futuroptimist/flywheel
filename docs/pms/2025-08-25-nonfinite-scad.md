# Non-finite SCAD value handling

## Summary
`parse_scad_vars` previously accepted extremely large numeric assignments like `1e5000`,
returning `inf` and risking downstream geometry calculations.

## Impact
Malformed SCAD files could bypass size checks and produce invalid meshes.

## Root Cause
The parser converted numeric literals to floats without validating finiteness.

## Resolution
Added `math.isfinite` checks to raise `ValueError` on non-finite numbers and
added regression tests.

## Mitigation
Rejecting `inf` and `NaN` protects dimension logic and prevents resource
consumption from unbounded values.

## Action Items
- [x] Add non-finite number regression test
- [x] Guard `parse_scad_vars` against `inf`/`NaN`
