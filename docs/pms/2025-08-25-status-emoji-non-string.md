# Non-string conclusion crashes status_to_emoji

## Summary
`status_to_emoji` crashed with `AttributeError` when GitHub's API returned a non-string `conclusion` value.

## Root Cause
The function unconditionally called `.lower()` on the `conclusion` parameter, assuming it was a string.

## Resolution
Cast the value to `str` before lowercasing so unexpected types fall back to the failure emoji.

## Impact
Any tooling using `status_to_emoji` could crash if the API returned numeric or boolean conclusions.

## Mitigation
Add type coercion and a regression test to ensure robust handling of malformed API responses.
