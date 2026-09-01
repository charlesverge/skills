---
name: code-optimizer
description: Review plans and code modifications for CPU, database, and memory cost regressions when one or more of those resources are a priority to optimize.
---

# Code Optimizer

## Use This Skill When

Use this skill when CPU, database, memory, latency under load, throughput, or infrastructure cost are explicit priorities for a plan or code change.

Use it when a plan is created, and again when the code is implemented.

## Purpose

This skill checks whether a modification increases resource requirements compared with the previous behavior or the intended budget.

It focuses on three resource classes:

- **CPU:** more computation, worse algorithmic complexity, repeated parsing or serialization, repeated scans, extra sorting, or repeated helper calls
- **Database:** more queries, larger result sets, less selective filters, more round trips, or N+1 reads and writes
- **Memory:** larger retained objects, duplicate copies of data, unbounded accumulation, or longer-lived buffers and caches

The goal is to catch regressions early and recommend structural improvements that reduce or hold steady the targeted resource usage.

## Review Model

Compare the proposed or modified code path against the earlier path using the same workload shape.

Check:

1. what work happens per request, per item, and per batch
1. whether the time complexity increases
1. whether query count or transferred data increases
1. whether more data is retained in memory or copied unnecessarily
1. whether a resource increase is bounded and explicitly justified by the stated priority

A change is a regression when it increases one of the target resources without an explicit, bounded reason.

## CPU Testing

### Code Review

Review whether the plan or implementation adds more work per request, per item, or per batch. Check for higher algorithmic complexity, repeated parsing or serialization, repeated regex or sorting, extra collection scans, or expensive work moved inside a loop.

Questions to answer:

- Did the change increase algorithmic complexity, such as $O(n)$ to $O(n^2)$?
- Was heavy work moved inside a loop?
- Are parse, serialize, regex, sort, or hash operations repeated for the same input?
- Is the same computation performed multiple times instead of being reused?
- Does the code scan the same collection multiple times when one pass would preserve behavior?
- Does the change introduce busy waiting, repeated polling, or unnecessary retries inside hot paths?

### Execution Test

Run the baseline and candidate paths with the same representative inputs. Use at least a small, expected, and high-volume workload so the growth pattern is visible, warm the runtime before timed runs, and repeat each run enough times to compare medians instead of single samples.

### What Is Measured

- elapsed time per operation, request, or batch
- process CPU time or equivalent runtime CPU counters
- throughput such as items per second
- how runtime grows as input size increases

## Database Testing

### Code Review

Review the data-access path for added round trips, larger result sets, and work that should stay in the database. Focus on query count, query shape, batching, projection, filtering, aggregation, and whether the selection logic still allows efficient index use.

Questions to answer:

- Did the number of queries increase per request, job, or item?
- Was a set-based query replaced by per-row lookups?
- Are filtering, aggregation, projection, and limits still pushed down to the database?
- Does the code fetch rows or fields that it never uses?
- Did the write path gain extra reads or round trips?
- Does the modification make index usage less likely by moving selection logic into application code?

### Execution Test

Run the baseline and candidate paths against the same seeded data volume and record every query boundary. Compare query counts, total database time, transferred rows, and bytes returned for one request, one batch, or one full job run.

### What Is Measured

- query count per request, item, or batch
- total query time and slowest-query time
- rows returned or written
- bytes transferred when available
- repeated round trips caused by N+1 or read-after-write patterns

## Memory Testing

### Code Review

Review whether the plan or implementation materializes more data, duplicates large objects, extends object lifetimes, or adds unbounded accumulation. Look for full dataset loads, chained collection transforms, duplicated payloads, and caches without a hard size limit.

Questions to answer:

- Does the change load complete datasets or files where streaming, pagination, or chunking existed before?
- Does it build duplicate lists, dicts, payloads, or strings?
- Does it materialize intermediate data structures that are consumed once?
- Does it keep references alive longer than needed?
- Does it accumulate results without a hard bound?
- Does it introduce a cache or preloaded structure without a clear size limit and ownership model?

### Execution Test

Run the baseline and candidate paths with representative and high-volume inputs while recording memory before, during, and after execution when the runtime supports it. Compare peak memory during the operation and retained memory after the operation completes.

### What Is Measured

- peak memory used during execution
- retained memory after the operation completes
- allocation growth as input size increases
- object or buffer duplication introduced by the new path

## Trade-Off Rule

Sometimes one resource increases to reduce another. That can be acceptable only when the chosen priority is explicit and the increase is clearly bounded.

Examples:

- a small request-scoped lookup map may be acceptable if it removes repeated database reads for the same bounded batch
- a single aggregate query may be acceptable even if it increases temporary database work because it removes many application round trips

If the priority is not explicit, flag the trade-off instead of assuming it is acceptable.

## Node and TypeScript Methods

Use built-in Node runtime measurement tools first so the same harness can be used during plan review and after implementation.

### CPU

- Use `node:perf_hooks` with `performance.now()` for elapsed time.
- Use `process.cpuUsage()` to compare user and system CPU time between the baseline and candidate paths.
- Warm the code before timed runs so JIT compilation cost does not distort the comparison.
- Use the same generated dataset for both versions and compare medians across repeated runs.
- Example resources: [Node CPU example](resources/cpu/node/README.md)

### Database

- Wrap the query boundary so each call records query count, elapsed time, rows returned, and bytes returned.
- Compare one batched path against per-item query loops with the same seeded data.
- When a real SQL query exists, inspect the real query plan after measuring round trips so query count and query shape agree.
- Example resources: [Node database example](resources/database/node/README.md)

### Memory

- Use `process.memoryUsage()` before and after the measured operation to compare heap and resident memory.
- If the runtime exposes `global.gc()`, call it between trials to reduce retained-noise between measurements.
- Compare materialized arrays and copies against single-pass or chunked processing on the same input sizes.
- Example resources: [Node memory example](resources/memory/node/README.md)

## Python Methods

Use Python standard-library instrumentation first so the test remains easy to repeat in a minimal environment.

### CPU

- Use `time.perf_counter()` for elapsed time and `time.process_time()` for process CPU time.
- Repeat the same run enough times to compare medians, not just a single timing sample.
- Use `cProfile` when the total time changed but the expensive function or call tree is not yet obvious.
- Example resources: [Python CPU example](resources/cpu/python/README.md)

### Database

- Wrap the repository, cursor, or client boundary so every query records count, elapsed time, rows returned, and bytes returned when available.
- Run the same seeded workload through the baseline and candidate paths and compare round trips before comparing wall-clock time.
- Keep the seed data size stable so changes in query count are attributable to the implementation, not the test data.
- Example resources: [Python database example](resources/database/python/README.md)

### Memory

- Use `tracemalloc` to capture current and peak allocated memory for the measured operation.
- Call `gc.collect()` between runs when retained objects from earlier trials would otherwise hide the comparison.
- Compare full materialization against iterators, chunked processing, or bounded accumulation using the same input sizes.
- Example resources: [Python memory example](resources/memory/python/README.md)

## Good and Bad Patterns

### CPU Patterns

- **Good:** Hoist invariant work out of a loop.
- **Good:** Precompile a regex once instead of recompiling it for every record.
- **Good:** Merge multiple passes over the same collection when behavior stays the same.
- **Bad:** Re-parse the same JSON payload for each branch or iteration.
- **Bad:** Sort inside a loop when one outer sort would do.
- **Bad:** Recompute an expensive helper result for identical inputs.

### Database Patterns

- **Good:** Fetch related rows with one set-based query.
- **Good:** Select only the fields the caller needs.
- **Good:** Batch writes when the contract allows it.
- **Bad:** Perform an N+1 query sequence from inside a loop.
- **Bad:** Run an existence check and then a second fetch when one query can answer both.
- **Bad:** Pull a large table into memory and then filter it in application code.

### Memory Patterns

- **Good:** Stream data or process it in chunks.
- **Good:** Keep only the fields needed for the next step.
- **Good:** Reuse bounded request-scoped data structures when ownership is clear.
- **Bad:** Build a giant list only to iterate over it once.
- **Bad:** Duplicate a large payload just to change a small part of it.
- **Bad:** Keep request-scoped data in a long-lived process-wide cache without a hard bound.

### Mixed Resource Patterns

- **Good:** Replace per-item database reads with one indexed query and a small bounded lookup map.
- **Good:** Push filtering and aggregation to the database so the application transfers and stores less data.
- **Bad:** Move filtering from SQL to Python, increasing transferred rows, CPU work, and memory retention at the same time.
- **Bad:** Add an unbounded cache to hide repeated work instead of fixing the repeated access pattern.

## Required Output Format

When using this skill, return the review in this structure:

- **Optimization Priority:** CPU, database, memory, or a combination
- **Hot Path:** where the affected work runs
- **CPU Impact:** lower, neutral, or higher with a short reason
- **Database Impact:** lower, neutral, or higher with a short reason
- **Memory Impact:** lower, neutral, or higher with a short reason
- **Trade-Offs:** explicit bounded exchange, if any
- **Verdict:** accept or revise
- **Smallest Fix:** the smallest structural change that removes the regression

## Review Heuristics

- Prefer one-pass, set-based, bounded-memory designs.
- Prefer measured or estimated work counts over vague performance claims.
- Prefer fixing the true source of repeated work instead of hiding it behind extra state.
- Reject arguments based only on “the dataset is probably small” unless the size bound is part of the contract.

## Rule

1. Identify whether CPU, database, memory, or a combination is the optimization priority.
1. Compare the proposed or modified path to the earlier path for work count, query count, and retained data.
1. When reviewing a plan, estimate the likely resource impact from the proposed design before implementation begins.
1. When reviewing implemented code, run the matching execution tests and compare measured results to the earlier path.
1. Flag any increase in the prioritized resources, even when behavior remains correct.
1. Approve only when increases are explicit, bounded, and aligned with the stated priority.
1. Recommend concrete alternatives using the good patterns above.
