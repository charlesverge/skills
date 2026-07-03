---
name: plan-validator-functions
description: Validate draft plans for function-group work before they are saved, finalized, or handed to implementation. Use when checking a plan for a group of functions with one primary entry point, such as `check_health_status`, for original-intent alignment, unasked features, scope creep, owning module directory boundaries, helper-function scope, package metadata, implementation-plan details, rule compliance, and required unit-test details. A functions plan covers a callable entry point plus helpers that can be tested as part of the owning module, backend API, or frontend component.
---

# Functions Plan Validator

Use this skill before saving or finalizing a plan for a function group. A function group has exactly one primary entry point and any supporting helper functions needed to produce that entry point's result. Treat validation as a gate: if the plan fails a hard-stop check, revise the plan before proceeding.

## Core Rules

1. This skill is the authoritative validator for function-group plans.
1. The template in `references/PLAN_FUNCTIONS_TEMPLATE.md` is the required plan format. Use it to check that the plan includes all required sections in order, with concrete details rather than placeholders.
1. Validate the plan from the user's original request and the plan content. Do not infer missing plan details from surrounding code.
1. The plan must name exactly one primary entry point function.
1. Code work for the function group must stay inside the owning module directory.
1. Python function plans must name the owning module's `pyproject.toml` and a unit-test command runnable from that module directory.
1. Node or TypeScript function plans must name the owning module's `package.json` and a unit-test command runnable from that module directory.
1. New helper functions should live in the entry point file unless the plan names an existing module-local helper file or the user explicitly requested a shared helper.

## Validation Workflow

1. Restate the user's original intent in one sentence.
1. Compare every planned task to that intent.
1. Move unrequested features, speculative improvements, broad refactors, parent-project edits, route wiring, UI wiring, and unrelated package work out of `Implementation plan` into `Suggested Improvements` or `Questions`.
1. Run the hard-stop rule checklist.
1. Check the plan format and required sections in `references/PLAN_FUNCTIONS_TEMPLATE.md`.
1. Verify the `Implementation plan` names exact files inside the owning module directory and covers the entry point function, helper functions, variables, imports, types, resources, input contract, output contract, errors, side effects, and reasons each file must contain.
1. Ensure there are no extra sections or fields that are not in the template.
1. Check rule compliance against active repo, user, developer, and skill instructions.
1. Verify the unit-test section is specific enough to execute from the owning module directory.
1. Finalize only after all required confirmations are true.

## Function Boundary Rules

- The function group must have one primary entry point, such as `check_health_status`.
- Helper functions are supporting implementation details unless explicitly exported by the existing module.
- The entry point file should contain new private helpers for the function group when practical.
- Reused helpers must be named by exact import path and function name.
- Modified helper files must be inside the owning module directory and must explain why the helper belongs outside the entry point file.
- API routes, job handlers, UI components, and parent projects may call the entry point, but their wiring belongs in another plan unless the user explicitly requested combined work.
- The plan must make the entry point's input contract, output contract, error contract, and side effects concrete enough for callers to use it without reading helper code.

## Hard-Stop Rule Checklist

Before writing, saving, or finalizing a functions plan:

- Reject any automatic alternate execution behavior that violates active no-alternate-behavior instructions.
- Reject banned alternate-execution wording defined by active user or repo instructions.
- Feature flags may describe only the enabled path and disabled path.
- Feature flags must not define automatic switching after an error.
- Hard stop if the plan does not follow `references/PLAN_FUNCTIONS_TEMPLATE.md`.
- Hard stop if the plan has zero or multiple primary entry point functions.
- Hard stop if any `Implementation plan` file is outside the owning module directory.
- Hard stop if the owning package metadata file is missing from the plan.
- Hard stop if tests cannot run from the owning module directory.
- Hard stop if helper behavior is not covered through entry point tests or justified as directly tested shared helper behavior.

## Future Features vs Suggested Improvements vs Questions

- Future features are additions that the user has already decided belong in that section. Do not move them to `Suggested Improvements` or `Questions`.
- Suggested improvements are useful but unrequested ideas that may still be worth doing later. Move them out of `Implementation plan`.
- Questions are uncertain scope or requirement decisions that must be clarified before implementation.

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

- parent project edits not explicitly requested
- route, job, or UI wiring not explicitly requested
- new user-facing behavior the user did not ask for
- generalized frameworks for a narrow function group
- unrelated cleanup or refactors
- package setup changes not required by the function request
- migrations, feature flags, background jobs, telemetry, retries, or operational flows not requested or required

When a rejected item may still be useful later, relocate it to `Suggested Improvements`. When an item depends on missing user intent or unclear requirements, relocate it to `Questions`. Do not leave rejected or out-of-scope items in `Implementation plan`.

### Entry Point and Helper Contract

- Validate the entry point function name, signature, input type, return type, and caller-visible errors are explicit.
- Validate each helper function is named and classified as `new private helper`, `existing reused helper`, `modified shared helper`, or `removed helper`.
- Validate helper inputs and outputs are concrete when the helper has branching logic, side effects, or meaningful failure behavior.
- Validate the dependency order is clear when the entry point coordinates several checks, such as DNS lookup, TCP port check, and HTTP response validation.
- Validate side effects, timeouts, external interactions, and deterministic test controls are named when the function touches network, file, database, browser, clock, or environment boundaries.
- Validate the plan names the owning package metadata file and the command that runs tests from the owning module directory.

### Rule Compliance

Check the plan against all active instructions and project rules. Call out violations explicitly and revise the plan. Common failures include:

- banned alternate-execution behavior or wording
- tests described vaguely instead of by file and test name
- implementation-plan entries outside the owning module directory
- implementation-plan entries without exact files, entry point, helpers, variables, imports, types, resources, contracts, side effects, or reasons
- optional alternatives where the user asked for a concrete path
- changes that contradict existing codebase patterns
- skipped validation without stating why it cannot run

## Test Coverage Section Requirements

The plan must include a `Test coverage` section even when no tests are required.

- Tests must cover the happy path, validation and error paths, edge cases, and regression cases.
- Unit tests are required for function-group plans unless the plan is only documentation.
- Tests must run from the owning module directory using that module's test command.
- Entry point behavior should be tested through the entry point function.
- Helper functions should be tested directly only when they are exported, reused shared helpers, or have enough branching complexity that direct tests are clearer.
- If the function performs file, network, database, browser, clock, environment, or API operations, include tests for the dependency boundary using fixtures, fakes, sandbox resources, or explicit manual checks when automated checks are not possible.
- Every row in the plan's `Error contract` table must have a corresponding `Test coverage` entry that asserts the exception, error result, validation result, or a concrete reason it cannot be tested.
- The `Test coverage` section must describe the tests that should exist for the completed plan. Do not use change-action buckets or change verbs.
- Hard stop if `## Test coverage` does not contain exact test cases or a concrete message explaining why no test cases are needed.

For each test case, list in order:

- exact file path
- test name
- short description of what it ensures
- one required coverage category: `Happy path`, `Validation / error path`, `Edge case`, or `Regression case`

Do not accept wildcard, glob, placeholder, or guessed paths. A unit-test entry is invalid if the path contains `*`, `**`, `<...>`, `[...]`, `tests/path/`, `some/path/`, or any placeholder instead of the concrete file where the test will be placed.

Valid format:

```markdown
## Test coverage

- `modules/health-check/tests/test_health_status.py` `test_check_health_status_returns_ok_when_all_checks_pass` Ensures DNS, port, and HTTP checks produce the documented healthy result - Happy path
- `modules/health-check/tests/test_health_status.py` `test_check_health_status_reports_dns_failure` Ensures DNS failure produces the documented unhealthy result - Validation / error path
- `modules/health-check/tests/test_health_status.py` `test_check_health_status_handles_empty_host` Ensures empty host input produces the documented validation error - Edge case
- `modules/health-check/tests/test_health_status.py` `test_check_health_status_preserves_result_contract` Ensures callers continue receiving the documented result fields - Regression case
```

## Implementation Plan Section Requirements

The plan must include one `Implementation plan` section. Use this section as the canonical place for concrete file-level implementation details.

Each entry must start with the exact file path inside the owning module directory and then list the concrete function updates inside that file. Cover every relevant entry point, helper function, variable, import, type, resource, input contract, output contract, error contract, side effect, dependency boundary, package metadata reference, and test in the file entry instead of using those as separate top-level subsections.

For each file entry, include:

- The exact file path inside the owning module directory
- Exact entry point, helper function, variable, import, type, resource, input contract, output contract, error contract, side effect, dependency boundary, package metadata reference, or test in the completed plan
- Short description of the item
- Reason for the file modification or reference

When adding configuration or feature flags, name the exact variable or setting. For example, do not write "add a config flag to settings". Write the concrete target, such as `modules/health-check/src/health_check/settings.py::HEALTH_CHECK_ENABLED`, and explain why it is needed.

Use this format:

```markdown
## Implementation plan

- `modules/health-check/pyproject.toml`
  - Existing package metadata used by the owning module.
  - Reason: provides the module-owned Python dependency and test configuration for this function group.
- `modules/health-check/src/health_check/status.py`
  - `check_health_status(target: HealthCheckTarget) -> HealthStatus`.
  - `_resolve_dns(host: str) -> DnsCheckResult`.
  - `_check_port(host: str, port: int, timeout_seconds: float) -> PortCheckResult`.
  - `_check_http_ok(url: str, timeout_seconds: float) -> HttpCheckResult`.
  - Reason: contains the single entry point and private helpers for the requested health status calculation.
- `modules/health-check/tests/test_health_status.py`
  - `test_check_health_status_returns_ok_when_all_checks_pass`.
  - `test_check_health_status_reports_dns_failure`.
  - Reason: verifies the function group through its entry point.
```

If any target file is already above 500 lines, or the plan would push it above 500 lines, treat that as a design warning. Prefer a dedicated entry point file for the function group. If the plan still modifies the large file directly, it must explain why that is the best direct path.

## Final Confirmation

Before saving or finalizing, verify these confirmations internally. Do not add these confirmations to the plan unless the template includes a section for them:

- no banned alternate-execution behavior was added
- no banned alternate-execution wording remains
- feature flags are described only as enabled and disabled paths
- the original user intent is followed
- unasked features are placed in `Suggested Improvements` or `Questions`
- exactly one primary entry point function is named
- helper functions are scoped to the entry point file or justified as existing module-local helpers
- implementation plan lists exact module-directory files, entry point, helpers, variables, imports, types, resources, contracts, side effects, package metadata reference, tests, and reasons
- unit tests are listed with exact file paths, test names, and descriptions, or a concrete reason is given for no tests
- package metadata and module-local verification commands are complete
- every error contract row has a corresponding test entry or a concrete documented reason
- vague language has been removed or converted into concrete target-state details
