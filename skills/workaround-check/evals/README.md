# Workaround Check Evals

This directory contains a source-grounded evaluation set for the `workaround-check` skill.

The corpus includes both:

- a **positive-control suite** of workaround attempts that should be rejected
- a **negative-control suite** of structural fixes that should be accepted

Together, the current corpus contains **35 cases**.

These cases are **synthetic eval prompts**, but they are grounded in public discussions, benchmarks, and research about reward hacking, test editing, lint suppression, broad exception swallowing, hardcoded answers, operator overloading, over-mocking, and other checker-evasion patterns.

## What is included

- `fixtures/cases.json` — 25 positive-control workaround cases.
- `fixtures/expected_results.json` — expected outcomes for the positive-control suite.
- `fixtures/negative_controls.json` — 10 negative-control non-workaround cases.
- `fixtures/negative_expected_results.json` — expected outcomes for the negative-control suite.
- `sources.md` — the public sources used to shape the cases.
- `TEST_METHOD.md` — the evaluation method.
- `run.py` plus stage modules — a lightweight harness that operationalizes the `workaround-check` skill for repeatable verification.
- `artifacts/latest_positive_results.json` — generated positive-control results.
- `artifacts/latest_negative_results.json` — generated negative-control results.
- `artifacts/latest_results.json` — combined summary and per-suite output.

## Coverage buckets

The eval set explicitly covers the model-family buckets the user requested:

- `claude`
- `openai`
- `codex`
- `public`

These buckets are used for coverage. They **do not claim** that every case is a verbatim output from a specific proprietary model. Unless otherwise noted in a source, each case is a paraphrased or synthetic plan inspired by a publicly documented workaround pattern.

## Expected high-level result

Positive controls are expected to be detected as workarounds and therefore receive:

- `actual_verdict = Reject`
- `detected_workaround = true`

Negative controls are expected **not** to be detected as workarounds and therefore receive:

- `actual_verdict = Accept`
- `detected_workaround = false`

## Prerequisites

- Python 3 available on your `PATH`
- Run the commands from either:
	- the eval directory itself, or
	- the repository root using the longer path form shown below

## Running the evals

### Full run from the eval directory

```text
cd /Users/devuser/dev/personal/skills/skills/workaround-check/evals
python run.py
```

### Full run from the repository root

```text
cd /Users/devuser/dev/personal/skills
python skills/workaround-check/evals/run.py
```

The default run performs, in order:

1. setup
1. health checks
1. execution
1. verification

## Stage-specific commands

### Setup only

Creates the artifact directory and validates that the fixture files are present and internally consistent.

```text
cd /Users/devuser/dev/personal/skills/skills/workaround-check/evals
python run.py --setup
```

### Execute only

Re-runs health checks, evaluates both suites, and writes fresh artifact files.

```text
cd /Users/devuser/dev/personal/skills/skills/workaround-check/evals
python run.py --execute
```

### Verify only

Re-runs health checks and verifies that the already-generated artifacts match the expected outcomes.

```text
cd /Users/devuser/dev/personal/skills/skills/workaround-check/evals
python run.py --verify
```

### Execute and verify in one pass

```text
cd /Users/devuser/dev/personal/skills/skills/workaround-check/evals
python run.py --execute --verify
```

### Clean generated artifacts

```text
cd /Users/devuser/dev/personal/skills/skills/workaround-check/evals
python run.py --cleanup
```

## What files are generated

After a successful execution run, the harness writes:

- `artifacts/latest_positive_results.json`
- `artifacts/latest_negative_results.json`
- `artifacts/latest_results.json`

Use `latest_results.json` when you want the combined summary for both suites.

## What success looks like

A successful full run prints messages in this shape:

```text
Prepared artifact directory: .../artifacts
Health checks passed for positive_controls: 25 cases.
Health checks passed for negative_controls: 10 cases.
Wrote 25 positive_controls evaluation results to .../latest_positive_results.json
Wrote 10 negative_controls evaluation results to .../latest_negative_results.json
Wrote combined evaluation results to .../latest_results.json
Verification passed: 35 cases across 2 suites matched expected workaround detection results.
```

## Interpreting the results

- If the run passes, the current harness classified all positive controls as workarounds and all negative controls as non-workarounds.
- If verification fails, the process exits with an error describing which case or suite diverged from the expected outcome.
- To inspect individual case decisions, open:
	- `artifacts/latest_positive_results.json`
	- `artifacts/latest_negative_results.json`

## Current suite size

- positive controls: `25`
- negative controls: `10`
- total cases: `35`
