# Node CPU Example

This example compares a CPU-heavy baseline against a version that moves invariant work out of the per-record loop.

## Code Review

- Check whether the same sort and regex construction happen for every record.
- Confirm the optimized path computes the same result before comparing performance.
- Compare per-record work, not only total wall-clock time.

## Execution Test

1. Build a fixed representative input.
1. Warm the runtime before collecting timings.
1. Run both implementations multiple times.
1. Compare the median elapsed and CPU time.

## What Is Measured

- elapsed milliseconds with `performance.now()`
- user CPU milliseconds with `process.cpuUsage()`
- system CPU milliseconds with `process.cpuUsage()`

## Manual Run

From the repository root, run:

```bash
cd skills/code-optimizer/resources/cpu/node && node --experimental-strip-types test_code.ts
```

## Files

- `code.ts`
- `test_code.ts`
