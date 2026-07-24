---
name: code-cleanup-rules
description: Apply cleanup-focused refactor rules for phased invalid/orphan deletion logic, strict typing at API boundaries, linear validation flow, and minimal operational wrappers. Use when implementing or reviewing cleanup-style functions.
---

# Code Cleanup Rules

Apply the following rules exactly when implementing or reviewing cleanup-style functions.

## Change Pattern Summary

- Prefer index-first and target-first cleanup logic over broad source scans.
- Split cleanup into clear phases with explicit intent (collect invalids, validate references, delete).
- Centralize repeated thresholds/config in settings (`job_seen_since_threshold_days`) instead of hardcoded literals.
- Add trigger scripts for operational entry points, with env-file support and minimal orchestration.
- Enforce strict typing from library contracts (`PointId` vs hand-written unions), and align annotations with actual API signatures.
- Reduce branching and duplicate checks by consolidating validation flow into one linear path.
- Remove non-essential logging/noise in hot cleanup loops.
- Keep counting logic simple and consistent (compute totals in one place, avoid scattered increments).
- Remove redundant intermediate state (no duplicate collections unless required for correctness).
- Prefer direct deletion paths for clearly invalid records (missing payload, invalid IDs).

## Proposed Agent Rule Set (for cleanup-style functions)

- Use phased cleanup structure: discover invalids, verify valids, delete invalids/orphans.
- Start from the smallest authoritative set first (index/target collection), not the largest source collection.
- Keep condition flow linear: one validation gate per field, no repeated type checks.
- Treat malformed/contract-violating records as delete candidates, not “skip and ignore.”
- Keep deletion accounting in one place; avoid incrementing totals in multiple branches.
- Minimize state: keep only collections needed for deletion and final counts.
- Use typed aliases from upstream libraries for API boundaries (`PointId`, etc.).
- Prefer `is None` checks over truthiness when paginating offsets.
- Avoid per-record warning logs in expected-cleanup paths unless explicitly requested.
- Put repeated numeric thresholds in settings with clear names and env overrides.
- Trigger scripts should be thin wrappers: parse args, load env, run one action, report result.
- Preserve existing function names unless explicitly asked to rename; keep new names short and action-oriented.
