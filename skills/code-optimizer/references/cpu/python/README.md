# Python CPU Example

This example compares a CPU-heavy baseline against a version that performs invariant work once.

## Code Review

- Check whether regex compilation and sorting happen for every record.
- Confirm the optimized path produces the same result before comparing timing.
- Compare work per record and how it grows with input size.

## Execution Test

1. Build a fixed representative input.
1. Warm the code before collecting timings.
1. Run both implementations multiple times.
1. Compare the median elapsed and CPU time.

## What Is Measured

- elapsed milliseconds with `time.perf_counter()`
- CPU milliseconds with `time.process_time()`

## Manual Run

From the repository root, run:

```bash
cd skills/code-optimizer/resources/cpu/python && python3 test_code.py
```

## Files

- `code.py`
- `test_code.py`
