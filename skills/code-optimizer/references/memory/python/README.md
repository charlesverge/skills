# Python Memory Example

This example compares a path that materializes multiple intermediate collections against a single-pass path.

## Code Review

- Check whether large intermediate collections or payload copies are created.
- Check whether the same result is produced before comparing memory cost.
- Review whether the optimized path keeps only the data needed for the next step.

## Execution Test

1. Build a representative high-volume input.
1. Measure both implementations on the same data.
1. Compare current and peak allocated memory for each run.
1. Compare the retained shape after execution by reviewing current allocated memory.

## What Is Measured

- elapsed milliseconds
- current allocated bytes from `tracemalloc`
- peak allocated bytes from `tracemalloc`

## Manual Run

From the repository root, run:

```bash
cd skills/code-optimizer/resources/memory/python && python3 test_code.py
```

## Files

- `code.py`
- `test_code.py`
