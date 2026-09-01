# Node Memory Example

This example compares a path that materializes multiple intermediate arrays against a single-pass path.

## Code Review

- Check whether large intermediate arrays or object copies are created.
- Check whether the same result is produced before comparing memory cost.
- Review whether the optimized path keeps only the data needed for the next step.

## Execution Test

1. Build a representative high-volume input.
1. Measure both implementations on the same data.
1. Compare retained heap delta and RSS after each run.
1. Pair this harness with a heap profiler when peak memory detail is required.

## What Is Measured

- elapsed milliseconds
- heap delta bytes from `process.memoryUsage()`
- resident set size bytes from `process.memoryUsage()`

## Manual Run

From the repository root, run:

```bash
cd skills/code-optimizer/resources/memory/node && node --experimental-strip-types --expose-gc test_code.ts
```

## Files

- `code.ts`
- `test_code.ts`
