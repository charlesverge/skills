# Node Database Example

This example compares a per-user query loop against a single batched read using an instrumented database boundary.

## Code Review

- Check whether the code issues one query per item instead of one batched query.
- Check whether the same totals are produced before comparing database costs.
- Review whether the query boundary records count, rows, bytes, and time.

## Execution Test

1. Seed a fixed number of users and orders.
1. Run the baseline and candidate paths against the same data.
1. Capture query statistics for each run.
1. Compare the total database cost by query count first, then elapsed time.

## What Is Measured

- query count
- rows returned
- bytes returned
- elapsed milliseconds spent in the query boundary

## Manual Run

From the repository root, run:

```bash
cd skills/code-optimizer/resources/database/node && node --experimental-strip-types test_code.ts
```

## Files

- `code.ts`
- `test_code.ts`
