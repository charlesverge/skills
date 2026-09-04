---
name: plan-validator-module
description: Validate draft plans for reusable module work before they are saved, finalized, or handed to implementation. Use when checking a module plan for original-intent alignment, unasked features, scope creep, module directory boundaries, package metadata, public exports and import contracts, implementation-plan details, rule compliance, test-convention compliance, and required unit-test details. A module plan covers code based on a class, function, or functions that can be unit tested as its own unit and imported by parent projects.
---

# Module Plan Validator

Use this skill before saving or finalizing a plan for a reusable module. A module is independently packaged code centered on a class, function, or set of functions, with its own tests and package metadata. Treat validation as a gate: if the plan fails a hard-stop check, revise the plan before proceeding.

## Core Rules

1. This skill is the authoritative validator for reusable module plans.
1. The template in `references/PLAN_MODULE_TEMPLATE.md` is the required plan format. Use it to check that the plan includes all required sections in order, with concrete details rather than placeholders.
1. Validate the plan from the user's original request and the plan content. Do not infer missing plan details from surrounding code.
1. Application code for a module plan must stay inside the module directory. Test and test-support files must follow `test-conventions` under the top-level `tests/` directory. Parent projects may import the module, but parent project code changes require a separate plan unless the user explicitly requested combined work.
1. Python modules must have a module-owned `pyproject.toml` and unit tests runnable from the module directory.
1. Node or TypeScript modules must have a module-owned `package.json` and unit tests runnable from the module directory.
1. Apply the `test-conventions` skill to every test plan or rule group, test helper file, and test file split described by the plan. Treat `test-conventions` as authoritative for test organization.

## Validation Workflow

1. Restate the user's original intent in one sentence.
1. Compare every planned task to that intent.
1. Move unrequested features, speculative improvements, broad refactors, parent-project edits, and unrelated packaging work out of `Implementation plan` into `Suggested Improvements` or `Questions`.
1. Run the hard-stop rule checklist.
1. Check the plan format and required sections in `references/PLAN_MODULE_TEMPLATE.md`.
1. Verify the `Implementation plan` names exact application files inside the module directory and exact test files under the top-level `tests/` directory, and covers the classes, functions, methods, variables, exported symbols, package metadata, resources, input contracts, output contracts, errors, side effects, and reasons each file must contain.
1. Ensure there are no extra sections or fields that are not in the template.
1. Check rule compliance against active repo, user, developer, and skill instructions.
1. Apply `test-conventions` and verify the `Test coverage` section is specific enough to execute from the module directory.
1. Finalize only after all required confirmations are true.

## Module Boundary Rules

- The module directory is the application-code boundary for the plan. Test files are the required exception and must live under the top-level `tests/` directory derived from the plan path.
- Application `Implementation plan` entries must be under the module directory. Test entries must use exact `test-conventions` paths.
- Parent project imports belong in `Parent integration contract`, not as parent project file edits.
- If the module needs parent project registration, workspace configuration, route wiring, UI wiring, deployment setup, or job scheduling, put that work in `Questions` or a separate plan unless the user explicitly requested it in this module plan.
- Shared interfaces must be expressed as public exports, input contracts, output contracts, exceptions, and documented side effects.

## Hard-Stop Rule Checklist

Before writing, saving, or finalizing a module plan:

- Reject any automatic alternate execution behavior that violates the active no-alternate-behavior instructions.
- Reject banned alternate-execution wording defined by active user or repo instructions.
- Feature flags may describe only the enabled path and disabled path.
- Feature flags must not define automatic switching after an error.
- Hard stop if the plan does not follow `references/PLAN_MODULE_TEMPLATE.md`.
- Hard stop if any application `Implementation plan` file is outside the module directory or any test file violates `test-conventions`.
- Hard stop if the package metadata file is missing for the module language.
- Hard stop if tests cannot run from the module directory.

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
- new user-facing features the user did not ask for
- generalized frameworks for a narrow module
- unrelated cleanup or refactors
- workspace-level package changes not required by the module request
- migrations, feature flags, background jobs, telemetry, retries, or operational flows not requested or required

When a rejected item may still be useful later, relocate it to `Suggested Improvements`. When an item depends on missing user intent or unclear requirements, relocate it to `Questions`. Do not leave rejected or out-of-scope items in `Implementation plan`.

### Package and Import Contract

- Validate the package metadata file exists in the module directory: `pyproject.toml` for Python, `package.json` for Node or TypeScript.
- Validate the module name, package name, public exports, and parent import path are explicit.
- Validate the plan names the concrete class, function, or functions that make up the module's public API.
- Validate the input contract, output contract, error contract, and side effects are concrete enough for a parent project to call the module without inspecting internal files.
- Validate the test command runs from the module directory and does not require unrelated parent project setup.

### Rule Compliance

Check the plan against all active instructions and project rules. Call out violations explicitly and revise the plan. Common failures include:

- banned alternate-execution behavior or wording
- tests described vaguely instead of by file and test name
- application implementation-plan entries outside the module directory or test entries outside the convention-derived top-level test path
- implementation-plan entries without exact files, covered classes, functions, variables, exported symbols, package metadata, resources, contracts, side effects, or reasons
- optional alternatives where the user asked for a concrete path
- changes that contradict existing codebase patterns
- skipped validation without stating why it cannot run

## Test Coverage Section Requirements

The plan must include a `Test coverage` section even when no tests are required.

Load and apply the `test-conventions` skill before accepting this section.

- Tests must cover the happy path, validation and error paths, edge cases, and regression cases.
- Unit tests are required for module plans unless the plan is only package metadata or documentation.
- Tests must run from the module directory using the module-owned test command.
- If the module performs file, network, database, or API operations, include tests for the dependency boundary using fixtures, fakes, sandbox resources, or explicit manual checks when automated checks are not possible.
- Every row in the plan's `Error contract` table must have a corresponding `Test coverage` entry that asserts the exception, error result, or validation outcome, or a concrete reason it cannot be tested.
- The `Test coverage` section must describe the tests that should exist for the completed plan. Do not use change-action buckets or change verbs.
- Hard stop if `## Test coverage` does not contain exact test cases or a concrete message explaining why no test cases are needed.
- Derive plan tests from `plans/{plan_dir}/{plan_file}.md`: discard `.md` and use the framework pattern under `tests/{plan_dir}/`.
- Derive rule tests from `plans/rules/{rule_area}/{rule_group}.md`: discard `.md` and use the framework pattern under `tests/rules/{rule_area}/`.
- Require every test file to begin with the exact `# Plan:` or `# Rule:` comment required by `test-conventions`.
- Keep every test file at or below 600 lines and require exact convention-compliant helper and split paths when planned coverage would exceed that limit.

For each test case, list in order:

- exact file path
- test name
- short description of what it ensures
- one required coverage category: `Happy path`, `Validation / error path`, `Edge case`, or `Regression case`

Do not accept wildcard, glob, placeholder, or guessed paths. A unit-test entry is invalid if the path contains `*`, `**`, `<...>`, `[...]`, `tests/path/`, `some/path/`, or any placeholder instead of the concrete file where the test will be placed.

## Files Section Requirements

The plan must include one `Files` section.
Each application entry must start with the exact file path inside the module directory.
Use this section as the place for which plans which outline the functionality for this module.

If any target file is already above 500 lines, or the plan would push it above 500 lines, treat that as a design warning. Prefer splitting work into focused plans for public types, public functions, helpers. If the plan requires the file to larger then 500 lines, it must explain why that is the best path.

## Plan Validator CLI Guard

After writing every plan file created by the task and every plan file changed by the task, run `plan_validator <plan-path>`.
Fix every reported issue. Repeat validation until exit status `0`. Finalize the plan and hand it off only after validation passes.
Installation note: `python3 -m pip install "git+https://github.com/charlesverge-dev-org/coding-tools.git"`.

## Final Confirmation

Before saving or finalizing, verify these confirmations internally. Do not add these confirmations to the plan unless the template includes a section for them:

- no banned alternate-execution behavior was added
- no banned alternate-execution wording remains
- feature flags are described only as enabled and disabled paths
- the original user intent is followed
- unasked features are placed in `Suggested Improvements` or `Questions`
- implementation plan lists exact module-directory files, classes, functions, methods, variables, exported symbols, package metadata, resources, contracts, side effects, and reasons
- unit tests are listed with exact file paths, test names, and descriptions, or a concrete reason is given for no tests
- every test path, filename, plan or rule comment, helper, and file split follows `test-conventions`
- package metadata and module-local verification commands are complete
- every error contract row has a corresponding test entry or a concrete documented reason
- vague language has been removed or converted into concrete target-state details
