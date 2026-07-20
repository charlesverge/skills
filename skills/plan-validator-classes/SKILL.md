---
name: plan-validator-classes
description: Validate draft plans for class-based work before they are saved, finalized, or handed to implementation. Use when checking a plan for one primary class or class-family object model inside an owning module, including original-intent alignment, unasked features, scope creep, module directory boundaries, class hierarchy and inheritance, generic base-class use, subclass/adaptor overrides, class properties, class functions, linked function-plan markdown files generated with plan-validator-functions, package metadata, implementation-plan details, rule compliance, test-convention compliance, and required unit-test details. A class plan follows the hierarchy that modules contain functions or classes, and classes contain properties and functions.
---

# Classes Plan Validator

Use this skill before saving or finalizing a plan for class-based work. A class plan covers one primary class or one class-family object model inside an owning module directory. Treat validation as a gate: if the plan fails a hard-stop check, revise the plan before proceeding.

## Core Rules

1. This skill is the authoritative validator for class plans.
1. The template in `references/PLAN_CLASSES_TEMPLATE.md` is the required plan format. Use it to check that the plan includes all required sections in order, with concrete details rather than placeholders.
1. Validate the plan from the user's original request and the plan content. Do not infer missing plan details from surrounding code.
1. The plan must name exactly one primary class or root/base class for a class-family object model.
1. Application code for the class must stay inside the owning module directory. Test and test-support files must follow `test-conventions` under the top-level `tests/` directory.
1. A module may contain standalone functions, classes, or both. A class contains properties and functions.
1. The plan must include a `Class hierarchy and object model` section that explains inheritance, base classes, subclasses, generic use, and override responsibilities.
1. Class properties must list `name`, `type`, and `description of use`.
1. Class functions must list `name`, `type`, `description of use`, and a linked function-plan markdown file.
1. Each linked function-plan markdown file must be generated and validated using `plan-validator-functions`.
1. Python class plans must name the owning module's `pyproject.toml` and a unit-test command runnable from that module directory.
1. Node or TypeScript class plans must name the owning module's `package.json` and a unit-test command runnable from that module directory.
1. Apply the `test-conventions` skill to every test plan or rule group, test helper file, and test file split described by the plan. Treat `test-conventions` as authoritative for test organization.

## Validation Workflow

1. Restate the user's original intent in one sentence.
1. Compare every planned task to that intent.
1. Move unrequested features, speculative improvements, broad refactors, parent-project edits, route wiring, UI wiring, and unrelated package work out of `Implementation plan` into `Suggested Improvements` or `Questions`.
1. Run the hard-stop rule checklist.
1. Check the plan format and required sections in `references/PLAN_CLASSES_TEMPLATE.md`.
1. Verify the `Class hierarchy and object model` section names the root/base class or interface, generic use pattern, hierarchy, shared behavior, required overrides, and concrete subclasses/adaptors in scope.
1. Verify the `Implementation plan` names exact application files inside the owning module directory and exact test files under the top-level `tests/` directory, and covers the primary class or root/base class, hierarchy classes, class properties, class functions, override functions, variables, imports, types, resources, construction contract, input contract, output contract, errors, side effects, package metadata reference, tests, and reasons each file must contain.
1. Verify every `Class functions` row links to an exact `.md` function-plan file.
1. Open each linked function-plan markdown file and validate it with `plan-validator-functions`; do not treat a link alone as sufficient.
1. Ensure there are no extra sections or fields that are not in the template.
1. Check rule compliance against active repo, user, developer, and skill instructions.
1. Apply `test-conventions` and verify the `Test coverage` section is specific enough to execute from the owning module directory.
1. Finalize only after all required confirmations are true.

## Class Boundary Rules

- The class plan must have one primary class or one root/base class for a class family, such as `HealthCheckRunner` or `HarnessBase`.
- The owning module directory is the application-code boundary for the plan. Test files are the required exception and must live under the top-level `tests/` directory derived from the plan path.
- Use `Allowed plan files` to list the exact module-owned files and exact convention-derived test files the plan may modify or reference.
- Use `External files explicitly in scope` only to record other outside-module files the user explicitly requested as combined work; convention-derived test files do not belong in this field.
- Parent project imports belong in `Parent or caller integration contract`, not as parent project file edits.
- API routes, job handlers, UI components, and parent projects may construct or call the class, but their wiring belongs in another plan unless the user explicitly requested combined work.
- Related subclasses, concrete adaptors, abstract classes, protocols, or interfaces may be in the same class plan only when they are part of the requested object model and are listed in `Class hierarchy and object model`.
- Class properties are state, dependencies, constants, computed values, or exposed attributes owned by the class.
- Class functions are constructors, public methods, private methods, class methods, static methods, property accessors with logic, abstract methods, template methods, override methods, or removed methods.
- Pure data properties belong in `Class properties`. Property accessors with branching logic, side effects, validation, or caller-visible errors belong in `Class functions` and require linked function plans.
- The plan must make the class construction contract, property contract, function contract, error contract, and side effects concrete enough for callers to use the class without reading implementation code.

## Class Hierarchy and Object Model Rules

- Always include the `Class hierarchy and object model` section.
- Use the section to explain the class relationship model, not implementation steps.
- For a simple single-class plan, state `Single class` as the object model type and use `None` for base class, subclasses, required overrides, and subclass/adaptor rows.
- For a base-class harness model, name the root/base harness class, the generic use pattern, the shared workflow functions, and every function concrete harnesses must override.
- For interface, protocol, or abstract-base-class designs, name the contract type and the concrete implementations/adaptors that satisfy it.
- Each required override must appear in `Class functions` with type `abstract method`, `template method`, or `override method`, and must link to a function-plan markdown file.
- Each concrete subclass or adaptor in scope must name its exact class, exact file path, parent class or contract, override functions, and purpose.
- Do not use the hierarchy section to introduce unrequested subclasses or broad extension frameworks.

## Function Plan Link Rules

- Each class function must have exactly one linked function-plan markdown file.
- The link must be a Markdown link in the `Function plan markdown file` column and must target a concrete `.md` path, such as `[run check](plans/health-check-runner/run-check.md)`.
- The linked function plan must name the same owning module directory, entry point file, and caller context as the class plan.
- The linked function plan's primary entry point must use the class function name or a language-appropriate method signature, such as `HealthCheckRunner.run_check(target: HealthCheckTarget) -> HealthStatus`.
- The linked function plan must cover the function's helper functions, variables, imports, types, resources, input contract, output contract, errors, side effects, dependency boundaries, package metadata, and tests.
- If the class has no class functions, the `Class functions` section must contain `None` and explain why the class still needs a class plan.
- Do not accept wildcard, glob, placeholder, or guessed function-plan paths.

## Hard-Stop Rule Checklist

Before writing, saving, or finalizing a class plan:

- Reject any automatic alternate execution behavior that violates active no-alternate-behavior instructions.
- Reject banned alternate-execution wording defined by active user or repo instructions.
- Feature flags may describe only the enabled path and disabled path.
- Feature flags must not define automatic switching after an error.
- Hard stop if the plan does not follow `references/PLAN_CLASSES_TEMPLATE.md`.
- Hard stop if the plan has zero or multiple primary/root object models.
- Hard stop if any application `Implementation plan` file is outside the owning module directory or any test file violates `test-conventions`.
- Hard stop if the owning package metadata file is missing from the plan.
- Hard stop if tests cannot run from the owning module directory.
- Hard stop if `Class hierarchy and object model` does not explain object model type, generic use pattern, root/base class or interface, hierarchy, shared behavior, required overrides, and concrete subclasses/adaptors in scope.
- Hard stop if any class property omits name, type, or description of use.
- Hard stop if any class function omits name, type, description of use, or function-plan markdown file.
- Hard stop if any required override is missing from `Class functions` or lacks a linked function-plan markdown file.
- Hard stop if any linked function-plan markdown file is missing or does not validate with `plan-validator-functions`.

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
- generalized frameworks for a narrow class
- unrelated cleanup or refactors
- package setup changes not required by the class request
- migrations, feature flags, background jobs, telemetry, retries, or operational flows not requested or required

When a rejected item may still be useful later, relocate it to `Suggested Improvements`. When an item depends on missing user intent or unclear requirements, relocate it to `Questions`. Do not leave rejected or out-of-scope items in `Implementation plan`.

### Class Contract

- Validate the class name, constructor signature, import path, property contract, callable functions, caller-visible errors, and side effects are explicit.
- Validate the hierarchy has one primary/root object model and all related classes belong to that object model.
- Validate the generic use pattern explains how callers use the base class, interface, protocol, or primary class without depending on subclass internals.
- Validate abstract methods, template methods, and override methods state which subclasses or adaptors implement them.
- Validate each property is named and has an exact type and description of use.
- Validate each class function is named and classified by type, such as `constructor`, `public method`, `private method`, `class method`, `static method`, `computed property accessor`, `abstract method`, `template method`, `override method`, or `removed method`.
- Validate each class function links to a generated function-plan markdown file that passes `plan-validator-functions`.
- Validate dependency order is clear when the class coordinates several functions.
- Validate side effects, timeouts, external interactions, and deterministic test controls are named when the class touches network, file, database, browser, clock, or environment boundaries.
- Validate the plan names the owning package metadata file and the command that runs tests from the owning module directory.

### Rule Compliance

Check the plan against all active instructions and project rules. Call out violations explicitly and revise the plan. Common failures include:

- banned alternate-execution behavior or wording
- tests described vaguely instead of by file and test name
- application implementation-plan entries outside the owning module directory or test entries outside the convention-derived top-level test path
- implementation-plan entries without exact files, class hierarchy, classes, properties, functions, override methods, variables, imports, types, resources, contracts, side effects, function-plan links, package metadata, tests, or reasons
- optional alternatives where the user asked for a concrete path
- changes that contradict existing codebase patterns
- skipped validation without stating why it cannot run

## Test Coverage Section Requirements

The plan must include a `Test coverage` section even when no tests are required.

Load and apply the `test-conventions` skill before accepting this section.

- Tests must cover the happy path, validation and error paths, edge cases, and regression cases.
- Unit tests are required for class plans unless the plan is only documentation.
- Tests must run from the owning module directory using that module's test command.
- Class-level tests should verify construction, property contracts, class coordination, and cross-function behavior.
- Hierarchy tests should verify base-class generic behavior, required override enforcement, and concrete adaptor behavior when the object model includes inheritance or interfaces.
- Function-level behavior must be covered in the linked function plans.
- If the class performs file, network, database, browser, clock, environment, or API operations, include tests for the dependency boundary using fixtures, fakes, sandbox resources, or explicit manual checks when automated checks are not possible.
- Every row in the plan's `Error contract` table must have a corresponding `Test coverage` entry that asserts the exception, error result, validation result, or a concrete reason it cannot be tested.
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

Valid format:

```markdown
## Test coverage

- `tests/{plan_dir}/test_{plan_file}.py` `test_class_constructs_with_required_dependencies` Ensures construction stores the documented dependencies - Happy path
- `tests/{plan_dir}/test_{plan_file}.py` `test_class_rejects_missing_required_dependency` Ensures missing required dependencies produce the documented validation error - Validation / error path
- `tests/{plan_dir}/test_{plan_file}.py` `test_class_preserves_optional_default` Ensures omitted optional configuration produces the documented default state - Edge case
- `tests/{plan_dir}/test_{plan_file}.py` `test_class_keeps_public_properties` Ensures callers continue receiving the documented public property names and types - Regression case
```

## Implementation Plan Section Requirements

The plan must include one `Implementation plan` section. Use this section as the canonical place for concrete file-level implementation details.

Each application entry must start with the exact file path inside the owning module directory. Each test entry must start with its exact convention-derived top-level test path. Cover every relevant object-model relationship, base class, subclass, adaptor, property, function, method, override method, variable, import, type, resource, construction contract, input contract, output contract, error contract, side effect, dependency boundary, function-plan link, package metadata reference, and test in the file entry instead of using those as separate top-level subsections.

For each file entry, include:

- The exact application file path inside the owning module directory or exact test path under the top-level `tests/` directory
- Exact object-model relationship, base class, subclass, adaptor, property, function, method, override method, variable, import, type, resource, construction contract, input contract, output contract, error contract, side effect, dependency boundary, function-plan link, package metadata reference, or test in the completed plan
- Short description of the item
- Reason for the file modification or reference

When adding configuration or feature flags, name the exact variable or setting. For example, do not write "add a config flag to settings". Write the concrete target, such as `modules/health-check/src/health_check/settings.py::HEALTH_CHECK_RUNNER_ENABLED`, and explain why it is needed.

Use this format:

```markdown
## Implementation plan

- `modules/health-check/pyproject.toml`
  - Existing package metadata used by the owning module.
  - Reason: provides the module-owned Python dependency and test configuration for this class.
- `modules/health-check/src/health_check/runner.py`
  - `HealthCheckRunner`.
  - `dns_client: DnsClient`.
  - `timeout_seconds: float`.
  - `__init__(dns_client: DnsClient, http_client: HttpClient, timeout_seconds: float) -> None`.
  - `run_check(target: HealthCheckTarget) -> HealthStatus`.
  - Function plan: `[run check](plans/health-check-runner/run-check.md)`.
  - Reason: contains the primary class, state, and class functions for the requested health check runner.
- `tests/{plan_dir}/test_{plan_file}.py`
  - `test_class_constructs_with_required_dependencies`.
  - `test_class_rejects_missing_required_dependency`.
  - Reason: verifies construction, property contract, and class-level behavior.
```

If any target file is already above 500 lines, or the plan would push it above 500 lines, treat that as a design warning. Prefer a dedicated class file. If the plan still modifies the large file directly, it must explain why that is the best direct path.

## Plan Validator CLI Guard

After writing every plan file created by the task and every plan file changed by the task, run `plan_validator --strict <plan-path>`.
Fix every reported issue. Repeat validation until exit status `0`. Finalize the plan and hand it off only after validation passes.
Installation note: `python3 -m pip install "git+https://github.com/charlesverge-dev-org/coding-tools.git"`.

## Final Confirmation

Before saving or finalizing, verify these confirmations internally. Do not add these confirmations to the plan unless the template includes a section for them:

- no banned automatic alternate behavior was added
- no banned automatic alternate wording remains
- feature flags are described only as enabled and disabled paths
- the original user intent is followed
- unasked features are placed in `Suggested Improvements` or `Questions`
- exactly one primary/root object model is named
- class hierarchy and object model details are explicit
- class properties list name, type, and description of use
- class functions list name, type, description of use, and linked function-plan markdown file
- required overrides are listed as class functions and have linked function-plan markdown files
- each linked function-plan markdown file exists and validates with `plan-validator-functions`
- implementation plan lists exact module-directory files, class hierarchy, classes, properties, functions, override methods, variables, imports, types, resources, contracts, side effects, package metadata reference, tests, function-plan links, and reasons
- unit tests are listed with exact file paths, test names, and descriptions, or a concrete reason is given for no tests
- every test path, filename, plan or rule comment, helper, and file split follows `test-conventions`
- package metadata and module-local verification commands are complete
- every error contract row has a corresponding test entry or a concrete documented reason
- vague language has been removed or converted into concrete target-state details
