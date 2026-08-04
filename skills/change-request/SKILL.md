---
name: change-request
description: Define a large or cross-cutting software change as a precise, implementation-ready change request grounded in the current codebase. Use when a user wants to scope a substantial feature, refactor, migration, behavior change, or multi-file modification before implementation.
---

# Change Request

Turn a broad requested outcome into one concrete set of code, test, configuration, migration, and resource changes. Define the work; do not implement it unless the user separately asks for implementation.

## Output Contract

Read `references/CHANGE_REQUEST_TEMPLATE.md` before drafting the response. Use that template as the final response and preserve its headings, category labels, field labels, order, and heading levels.

If the request requires no changes, write only `- None` under `## Changes required` and omit all categories. If a category has no entries, write `- None` directly under that category and omit its `Add`, `Modify`, and `Remove` groups. If a category has entries, include only the non-empty groups.

Write `- None` in an empty `Out of scope` or `Assumptions` section. Every other section must contain at least one concrete entry.

## Workflow

1. Identify the requested outcome, constraints, acceptance conditions, and explicitly excluded scope.
1. Read the latest saved code, tests, configuration, migrations, and resource files relevant to the request.
1. Trace the affected behavior through its callers, state changes, data boundaries, and tests.
1. Select the single best implementation path that fits the current architecture and project conventions.
1. Identify every required addition, modification, and removal.
1. Assign each change to its single most-specific template category.
1. Write exact paths, symbols, signatures, control flow, conditions, types, assertions, commands, and file content where they are known.
1. Define the exact tests, checks, builds, and observable behaviors that verify the completed change.
1. Record assumptions that materially affect the request definition.
1. Verify that the combined entries completely define the requested outcome without adding unrelated work.
1. Render the final response from `references/CHANGE_REQUEST_TEMPLATE.md`.

If a material product or architecture choice cannot be resolved from the request and repository evidence, ask one concise blocking question before producing the change request. Do not make the implementer choose between alternatives inside a required change.

## Required-Change Rules

- Make each `Required change` one concrete request.
- Change requests cannot be vague, they must be specific and actionable.
- Using multiple select is can be considered vague, so avoid it. "For example rename `code_*` variables to `other_*` variable names". In this case this requires extra effort on the coders part which is already known on the plan writers part in a specific details.
- Select one implementation. Do not use `either`, `one of`, `could`, `maybe`, `option`, `choose`, or `do X or Y` to present alternatives.
- Split independently required changes into separate entries. Keep mandatory ordered steps together only when they form one indivisible change.
- Name the exact behavior, call, field, assertion, command, file content, or removal.
- Include exact file paths and line numbers when known.
- Write for a junior developer: make control flow, calls, conditions, data shapes, and expected outcomes explicit.
- Verify logic and type correctness before specifying a change.
- Ground every entry in the requested outcome and current implementation. Do not include speculative work or unrelated cleanup.
- Do not duplicate a change across categories. Use the most-specific category.
- Distinguish file-level outcomes from symbol-level logic. When both are necessary, make their scopes non-overlapping.
- Put classes, properties, and types only under `Classes, properties, and types needing changes`.
- Put functions only under `Functions needing changes`.
- Put constants only under `Constants needing changes`.
- Put tests only under `Tests needing changes`.
- Put Markdown, text, JSON, XML, data, and other non-code files only under `Resource files needing changes`.
- Use `Notes of major removals` only for removal impact that is not already captured by a `Remove` entry.
- For a new function, provide its exact signature and the logic it must implement.
- For a new class, provide its exact name, typed properties, methods, and method behavior.
- For a function modification, include the concrete control flow, calls, and conditions in `Required change`.
- For a test change, name each test separately and make `Verification` state the exact assertion or behavior it must prove.
- When a required package is missing, add separate entries for the dependency declaration and the necessary code import or usage.
- Require removal only when the user requests it, current behavior conflicts with the requested outcome, or the proposed work would otherwise introduce an unnecessary addition.
- Do not require changes to request wording, ownership, requirements, or acceptance criteria. Target implementation, tests, dependencies, configuration, migrations, or resources.
- The use of or, maybe is not allowed, research specific and provide a single answer. If there are multiple options and a single option is not clear, ask a question in the questions section.

## Context and Verification Rules

- State `Goal` as the single specific outcome the completed work must achieve.
- Put included behavior and deliverables under `In scope`; put explicit exclusions under `Out of scope`.
- Ground `Current state` in the latest saved code. Include exact paths and symbols with concise behavioral evidence.
- Do not describe the requested future behavior as current state.
- List every test, type check, linter, build, migration check, or manual behavior check required to validate the change under `Verification Required`.
- Make each verification entry name its expected result and the requirement it covers.
- Keep verification requirements consistent with the individual entries under `Tests needing changes` without duplicating implementation instructions.
- State only assumptions that influence scope or implementation. Do not use assumptions to hide unresolved product or architecture decisions.

## Scope Rules

- Treat existing behavior as preserved unless the request explicitly removes it or it conflicts with the requested outcome.
- Treat example commands as minimum required command shapes unless the user says they are exact or exclusive.
- Include migrations when data, schema, files, or configuration must change for the requested behavior to work.
- Describe feature flags only as enabled and disabled paths. Do not specify automatic switching between those paths after an error.
- Include all directly required files even when the result spans many files; do not replace detailed entries with a summary such as `update related tests`.

## Final Audit

Before finalizing:

1. Confirm every entry is necessary for the requested outcome.
1. Confirm every entry has all supporting fields required by its category.
1. Scan every `Required change` for alternatives and replace them with one selected action.
1. Confirm no item is duplicated across categories.
1. Confirm every affected test is listed individually with an exact verification target.
1. Confirm all feature flags use only enabled-path and disabled-path language.
1. Confirm the goal, scope, current state, verification requirements, and assumptions agree with the required changes.
1. Confirm the response exactly follows `references/CHANGE_REQUEST_TEMPLATE.md`.
1. Confirm that specific files, functions, classes and types are named in every entry, and that no entry is vague or speculative or requires a decision from the implementer.
1. If a decision is required, complete additional research to identify the solution.
1. If a decision is required use the ask-a-question skill to resolve it.
1. Execute `plan_validator` validate the plan meets the `references/CHANGE_REQUEST_TEMPLATE.md` format requirements.
