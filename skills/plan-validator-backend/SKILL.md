---
name: plan-validator-backend
description: Validate draft plans for api, backend, job, non user facing plans before they are saved, finalized, or handed to implementation. Use when checking a plan for original-intent alignment, unasked features, scope creep, fallback-rule violations, banned recovery language, feature-flag wording, plan structure, concrete implementation-plan details, rule compliance, and required unit-test details.
---

# API / backend plan Validator for features that are non user facing

Use this skill before saving or finalizing a plan for a backend non user facing feature like an api, backend task or job. Treat validation as a gate: if the plan fails any hard-stop check, revise the plan before proceeding.

## Validation Workflow

1. Restate the user's original intent in one sentence.
1. Compare every planned task to that intent.
1. Move unrequested features, speculative improvements, broad refactors, and extra compatibility work out of the `Implementation plan` unless the user explicitly asked for them into the Suggested Improvements section or Questions.
1. Run the hard-stop fallback checklist.
1. Check the plan format and required sections.
1. Verify the `Implementation plan` section names exact files and covers the classes, functions, methods, variables, settings, resources, request and response contracts, persistence operations, and reasons each file must contain for this backend/API feature.
1. Check rule compliance against any active repo, user, developer, or skill instructions.
1. Verify the unit-test section is specific enough to execute.
1. Finalize only after all required confirmations are true.

## Hard-Stop Fallback Checklist

Fallback behavior is banned unless the user explicitly requests it using the word `fallback` or clearly describes automatic recovery to an alternate path.

Before writing, saving, or finalizing a plan, scan the proposed plan for:

- `fallback`
- `fall back`
- `fallback path`
- `backup path`
- `alternate path on failure`
- `retry with old behavior`
- `recovery path`
- `compatibility path`
- `graceful degradation`
- `if new path fails, use old path`

If any of these appear and the user did not explicitly request fallback behavior, stop and remove the fallback behavior or wording before continuing.

Feature flags are not fallbacks. A feature flag may define:

- enabled path
- disabled path

A feature flag must not define:

- automatic fallback from enabled path to disabled path
- fallback on error
- recovery to old behavior

When a user says `feature flag`, use only `enabled path` and `disabled path`. Never use `fallback` to describe either path.

## Required Plan Format

Use the plan structure in references/PLAN_API_TEMPLATE.md

### How to use the template

1. Create an API short code.
   - **API short code:** [API area-action or route-purpose. For example, `auth-session`, `questions-area-suggestions`, or `coaching-resume-review-session`]
1. Fill out every section. If a section does not apply, write `N/A` or `None`.
1. Save the API plan as `plans/api/{api-short-code}.md`.
1. Keep the plan backend, api and contract-first. Document the request and response structures the client depends on before internal implementation notes.
1. If the endpoint is generic and serves multiple internal purposes, document:
   - how callers select the internal behavior
   - which request field or route segment controls the behavior
   - which internal handler, class, or function is responsible for each behavior
   - any constraints that keep the endpoint consistent across those behaviors

## Plan Review Gate

- No fallback behavior was added.
- No fallback language remains.
- Feature flags are described only as enabled and disabled paths.
- The plan follows the original intent.
- Unasked features are placed in `Suggested Improvements` or `Questions`.
- Implementation plan lists exact files, classes, functions, methods, variables, settings, resources, request and response contracts, persistence operations, and reasons.

## Plan Checks

### Intent Alignment

- Confirm the plan solves the user's stated request, not a broader inferred project goal.
- Mark each `Implementation plan` item as `requested`, `required to satisfy request`, `suggested improvement`, `question`, or `remove`.
- Keep only `requested` and `required to satisfy request` items in `Implementation plan`.
- Move useful but unrequested ideas to `Suggested Improvements`.
- Move uncertain scope or requirement decisions to `Questions`.
- Remove items that are neither useful follow-ups nor valid questions.
- If a step depends on an assumption, state the assumption and keep only the best direct path.

### Scope Creep

Reject plan items that introduce:

- new user-facing features the user did not ask for
- generalized frameworks for a narrow change
- unrelated cleanup or refactors
- compatibility layers not required by the request
- migrations, feature flags, background jobs, telemetry, retries, or operational flows not requested or required

When a rejected item may still be useful later, relocate it to `Suggested Improvements`. When an item depends on missing user intent or unclear requirements, relocate it to `Questions`. Do not leave rejected or out-of-scope items in `Implementation plan`.

### Rule Compliance

Check the plan against all active instructions and project rules. Call out violations explicitly and revise the plan. Common failures include:

- banned fallback behavior or language
- tests described vaguely instead of by file and test name
- implementation-plan entries without target files or backend contract details
- implementation-plan entries without exact files, covered classes, functions, variables, settings, resources, persistence operations, or reasons
- optional alternatives where the user asked for a concrete path
- changes that contradict existing codebase patterns
- skipped validation without stating why it cannot run

## Implementation plan Section Requirements

The plan must include one `Implementation plan` section. Use this section as the canonical place for concrete file-level implementation details.

Each entry must start with the exact file path and then list the concrete backend updates inside that file. Cover every relevant class, function, method, variable, setting, resource, request and response contract, persistence operation, and error mapping in the file entry instead of using those as separate top-level subsections.

For each file entry, include:

- The exact file path
- Exact class, function, method, variable, setting, resource, request and response contract, persistence operation, or error mapping being added or modified
- Short description of the class, function, method, variable, setting, resource, request and response contract, persistence operation, or error mapping
- Reason for the file modification

When adding configuration or feature flags, name the exact variable or setting. For example, do not write "add a config flag to settings". Write the concrete target, such as `src/module_name/settings.py::FEATURE_NAME_ENABLED`, and explain why it is needed.

Use this format:

```markdown
## Implementation plan

- `src/module_name/feature_name/state.py`
  - `FeatureState.feature_name_enabled: bool = True`.
  - Reason: stores the requested default-enabled feature flag in feature state.
- `src/module_name/feature_name/settings.py`
  - `FeatureSettings.feature_name_enabled: bool = True`.
  - `load_feature_settings` sets `FeatureSettings.feature_name_enabled` from `feature_state.feature_name_enabled`.
  - Reason: passes the feature flag to the feature implementation without reading state from lower-level helper code.
```

If any target file is already above 500 lines, or the plan would push it above 500 lines, treat that as a design warning. Prefer splitting work into subfeatures or helpers using `src/{module name}/{feature name}/{sub feature}` organization, with separate files for types, helpers, models, and a supporting resources directory for static data files. If the plan still modifies the large file directly, it must explain why that is the best direct path.

## Test coverage Section Requirements

The plan must include a Test coverage section even when no tests are added.

- Tests must cover the happy path, validation and error paths, edge cases, and regression cases.
- Tests must include both unit tests and integrations using a real database or API when persistence is involved. For real apis specifically ones that have a cost or side effects, use a sandbox or staging environment.
- If not sandbox is possible, then they must be only triggered with a manual flag. see "Manual unit tests" in skill pytest-unit-test-generation for details on how to implement this.
- Every row in the plan's `Error codes` table must have a corresponding `Test coverage` entry (added or existing) that asserts that status/code, or an explicit concrete reason it cannot be tested. Error-path tests must not be relocated to `Suggested Improvements`.

For each test added or modified, list:

- exact file path
- test name
- added or modified
- short description of what it ensures

Do not accept wildcard, glob, placeholder, or guessed paths. A unit-test entry is invalid if the path contains `*`, `**`, `<...>`, `[...]`, `tests/path/`, `some/path/`, or any placeholder instead of the concrete file where the test will be placed.

Invalid format:

```markdown
## Test coverage

- Added:
  - `src/**/tests/**::test_feature_uses_enabled_path_when_flag_enabled`
    Ensures the feature uses the enabled path when the feature flag is enabled.
```

Valid format:

```markdown
## Test coverage
- Added:
  - `src/module_name/feature_name/tests/test_feature_name_optional_subfeature.py::test_feature_uses_enabled_path_when_flag_enabled`
    Ensures the feature uses the enabled path when the feature flag is enabled.
- Modified:
  - `src/module_name/feature_name/tests/test_existing_feature_behavior.py::test_existing_behavior`
    Updates the assertion for the changed contract.
- Not added:
  No unit tests added because this is a documentation-only plan.
```

If the exact test file is not known, inspect the repository before finalizing the plan. If the repository cannot be inspected, put the test-location uncertainty in `Questions` and do not claim that unit tests are planned with exact locations. If tests are not added, explain the concrete reason. Do not leave the section empty.

## Data base and api persistence operations

When a plan involves database or API persistence, check for the following:

1. Plans must name every DB field written (state changes/output contract), and document where cross-route data (like a job snapshot) originates and how it flows to the persisting route.
1. Every write route needs a real-DB integration test that re-reads the record to confirm the write; read-only routes need an integration test against seeded known records.
1. Every write route needs a real-DB integration test that re-reads the record to confirm the write, plus a test for each documented 4xx failure path (auth, validation, missing-resource); read-only routes need an integration test against seeded known records.

## Final Confirmation

Before saving or finalizing, include these confirmations in the plan review gate:

- no fallback behavior was added
- no fallback language remains
- feature flags are described only as enabled and disabled paths
- the original user intent is followed
- unasked features are placed in `Suggested Improvements` or `Questions`
- implementation plan lists exact files, classes, functions, methods, variables, settings, resources, request and response contracts, persistence operations, and reasons
- unit tests are listed with exact file paths, test names, and descriptions, or a concrete reason is given for no tests
- Database operations have complete contracts, integrations which ensure persistence of data
- every error code in the `Error codes` table has a corresponding test entry or a concrete documented reason
- Verify the plan does not use vague language, it should not have language like "it could be implemented like this", "possibly is", "might", "maybe", etc other vague descriptions. Concrete details are needed. if something is vague locate supporting details to make it certain or add a question clarify.
