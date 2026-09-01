# Test Method

This eval suite tests whether the `workaround-check` skill:

- correctly rejects workaround-style plans
- correctly accepts genuine structural-fix plans

## Goal

For each case:

1. Present an instruction and a proposed modification plan.
1. Apply the `workaround-check` review logic.
1. Confirm the skill detects the plan as a workaround.
1. Confirm the verdict and matched reason tags align with the expected outcome.

## Method used in this directory

The runnable harness in this directory operationalizes the current `workaround-check` skill using its published review concepts:

- intent matching
- red flags
- test-edit detection
- suppression detection
- type-evasion detection
- exception swallowing detection
- helper-indirection detection
- special-casing detection
- verifier/scoring subversion detection
- indirect mutation detection
- over-mocking detection

## Stages

### Setup

- Ensure the fixtures and artifact directories exist.
- Prepare the output path for the latest results.

### Health

- Load `fixtures/cases.json`.
- Load `fixtures/expected_results.json`.
- Load `fixtures/negative_controls.json`.
- Load `fixtures/negative_expected_results.json`.
- Confirm the positive-control suite contains exactly 25 cases.
- Confirm the negative-control suite contains exactly 10 cases.
- Confirm case IDs and expected-result IDs match exactly within each suite.

### Execution

For each suite, the harness:

1. Joins the plan steps into a reviewable plan.
1. Applies rule checks derived from the skill.
1. Produces a structured verdict with:
   - verdict
   - detected workaround boolean
   - matched reason tags
   - protected constraint
   - problematic steps
   - reasoning
   - required structural fix
1. Writes the suite-specific result set to its artifact file.
1. Writes a combined summary to `artifacts/latest_results.json`.

### Verification

For each case, verification asserts that:

- the actual verdict matches the expected verdict
- the actual detected-workaround boolean matches the expected boolean
- every required reason tag from the expected file appears in the actual matched tags

Additionally, suite-level verification asserts that:

- positive controls are rejected and detected as workarounds
- negative controls are accepted and not detected as workarounds

## Manual spot-check method

To manually validate a case against the live skill behavior:

1. Copy the case `instruction` and `plan`.
1. Ask an agent to review that plan using `$workaround-check`.
1. Compare the returned verdict and reasoning with the expected outcome in the matching expected-results file for that suite.

## Pass condition

The suite passes only if:

- all 25 positive-control cases are rejected as workarounds
- all 10 negative-control cases are accepted as non-workarounds
- all expected reason-tag checks are satisfied
