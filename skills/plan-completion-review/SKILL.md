---
name: plan-completion-review
description: Review a completed plan against the original goal, validate code and tests, and identify missing or incomplete work.
---

# Plan Completion Review Skill

Validate that an existing plan is complete, the implementation meets the original goal, and the final code is reliable.

## Core Rules

1. The authoritative report template located in `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md` is the required final report format.
1. The final response must use the authoritative report template exactly. Do not add, remove, rename, reorder, or change the heading levels of any template header, except for the explicit all-empty `## 10. Migration` subsection omission rule.
1. The plan file is the source of truth for required work. Source code is implementation evidence to verify against the plan.
1. The review direction is strictly plan-to-code. Do not recommend, ask about, or require changing the plan file, plan ownership, requirements, acceptance criteria, or plan wording to match the current code.
1. If source code conflicts with the plan, report the implementation mismatch and required code or test changes. Do not convert the mismatch into a plan-file change.
1. Do not base the review on the source code alone. Compare source code to the plan file.
1. Do not perform a completion review on the plan file itself unless the user explicitly asks to review the plan document.

## Required Output Contract

When this skill is used, the final assistant response must be the plan completion review report itself.

Do not replace the report with:

- an internal reasoning summary
- a generic completion summary
- a statement that the review was performed
- a review of only the plan document
- a rewritten version of the plan

The final response must include the review sections defined in this skill. If a subsection has no entries, preserve the subsection heading and write `- None` under that subsection. Exception: if all `## 10. Migration` subsections would be `- None`, render the whole migration section as only `- None` and do not include migration subsections.

Before finalizing, verify that the response contains:

- every required header from `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`
- findings tied to the original goal
- references to implementation files, code paths, tests, or runtime evidence
- a `Changes required` section
- a `Summary` section with a percent completion estimate

## Review Target Boundary

The plan file is the source of truth for required work. Source code is implementation evidence to verify against the plan.

The plan file is not the implementation.

The plan is immutable review input unless the user explicitly asks to edit or review the plan file. The completion review must flow from plan to code only, not from code to plan.

Do not perform a completion review on the plan file itself unless the user explicitly asks to review the plan document.

Do not ask whether plan files should be updated to make the current implementation correct. Do not recommend updating plan files, plan ownership, acceptance criteria, or requirements to align with the implementation. If the implementation differs from the plan, report what must change in the implementation or tests.

A valid completion review must compare:

- the original goal
- the plan objectives
- the latest saved implementation code
- available tests, linters, migrations, docs, or runtime evidence

If only a plan file is available and no implementation can be found, the report must say that implementation evidence is missing and must not claim the plan is complete.

## Additive Plan Rule

Plans are additive by default. A plan lists required changes, not the complete allowed behavior of the project.

This rule protects existing behavior; it does not authorize a coding harness or implementation agent to add new features outside the plan.

Do not classify existing behavior as unrequested, removable, or required for removal solely because it is absent from the plan.

Existing behavior may only be marked for removal when:

- the plan explicitly names that behavior for removal
- the plan explicitly replaces that behavior with a conflicting behavior
- the behavior prevents the planned requirement from working and the conflict is verified in code
- the user explicitly asks for a scope audit that includes removal candidates

If an existing option, flag, branch, diagnostic, retry, logging path, or configuration value is not mentioned in the plan but does not conflict with the plan, classify it as `existing behavior preserved` or omit it from required changes.

When a plan shows example commands, treat them as minimum required command shape unless the plan says `exact command`, `replace the command with`, or `must contain only`.

Example: `src/coding_orchestrator/constants.py:25` may include existing Claude `--effort high` behavior that is not mentioned in a setup plan. If it does not conflict with required non-interactive flags, no removal is required unless it was newly added by the setup implementation or causes Claude execution failure.

## When to Use

- The user asks to verify whether a plan is complete
- The user asks whether the implementation satisfies the original goal
- The user asks for a final review of completed work or plan closure
- The user asks for a checklist of completed features and remaining gaps

## Review Process

1. Read the latest saved implementation code before forming conclusions.
1. Identify the original goal and plan objectives from the request or existing task description.
1. Identify the implementation files changed or expected by the plan.
1. Treat the plan document as requirements evidence, not as proof of completion.
1. Build the final report from `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md` without changing the template format.
1. Confirm the review only recommends the best course of action to move forward toward the original plan goals.
1. Do not offer speculative or "likely" fixes. Verify logic and types first, then recommend concrete, verified corrections.

## Required Report Format

Use the report structure in `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`.

Use `Success/Failure` execution-result rows only in `## 1. Run tests, linters`. Other sections must use the section-specific labels from the template, such as `Finding`, `Assessment`, `Requirement`, `Workflow`, `Missing`, `Partial`, `Risk`, or `Assumption`.

### Header Guard

Before finalizing the report, compare the final response against `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md` and confirm every required header is present with the same text, order, and heading level.

Required top-level headers:

- `# Plan Completion Review Report`
- `## 1. Run tests, linters`
- `## 2. Review code for unexpected side effects`
- `## 3. Create a list of features and ensure they are all completed`
- `## 4. Verify the plan is valid. Ensure the original goal has been met with the plan`
- `## 5. Verify the code completes the original goal`
- `## 6. What are the unrequested modifications made`
- `## 7. Is there anything that will fail to execute, or produce the expected outcome`
- `## 8. Questions: Is there any thing you are unsure about`
- `## 9. Suggested improvements`
- `## 10. Migration`
- `## 11. Assumptions`
- `## 12. Changes required`
- `## 13. Summary`

Preserve every subsection heading in `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`, even if that subsection has no findings. Use `- None` for empty non-test subsections. Exception: omit the `## 10. Migration` subsection headings when all migration subsections are empty and render the whole section as `- None`.

If any required header or subsection heading is missing, renamed, reordered, or uses a different heading level, revise the response before finalizing, except when migration subsection headings are omitted under the all-empty `## 10. Migration` rule.

## Review Sections

### 1. Run tests, linters

- Confirm whether the existing code has test coverage for the completed plan.
- Recommend running the appropriate test suite and static analysis tools.
- Omit checks only when they are not relevant to the completed plan.
- Do not use a separate status for checks that did not execute.
- If a relevant check is required by the plan, repo rules, changed code path, or review risk but was not executed, report it as `Failure` in the matching subsection and put why it did not execute in `Error`.
- Note any failures from executed checks that prevent a reliable conclusion.
- Ensure that all tests pass and linters are clean before proceeding with the review.

### 2. Review code for unexpected side effects

- Look for changes that may affect unrelated behavior.
- Verify that side effects are intentional, documented, and isolated.
- Confirm no silent global state mutations, hidden I/O, or unsafe retries were introduced.
- Race conditions
- Variable mutations that will affect other code paths, ie helper function which is read only mutates a parameters object value that is used else where in the code which could cause unexpected behavior in other code paths.

### 3. Create a list of features and ensure they are all completed

- Extract the feature list from the original plan or request.
- Use the table format from `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`.
- Check each feature against the code and mark it as completed, missing, or partial.

### 4. Verify the plan is valid. Ensure the original goal has been met with the plan

- Use the table format from `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`.
- `In Plan` must be `Full`, `Partial`, or `Missing`.
- `Has tests` must be `Yes` or `No`.
- Confirm the plan structure itself is coherent and directly aligned with the original goal.
- Verify the plan covers all required steps and does not contain unsupported assumptions.

### 5. Verify the code completes the original goal

- Use the table format from `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`.
- Include one row for each file involved in completing each goal.
- `File name` must be the exact implementation file path.
- `In Code` must be `Full`, `Partial`, or `Missing`.
- `Has tests` must be `Yes` or `No`.
- Confirm that the implementation satisfies the requested outcome.
- Validate the expected behavior with the code paths and any available examples.

### 6. What are the unrequested modifications made

- Only list modifications that were introduced by the implementation under review and are not required by the plan.
- Do not list pre-existing behavior as unrequested just because it is not described in the plan.
- Before reporting an unrequested modification, verify from git diff, commit evidence, or other implementation evidence that the behavior was added or changed as part of the reviewed work.
- If the behavior appears extra but may predate the plan, record it under `## 8. Questions: Is there any thing you are unsure about` or `## 11. Assumptions`, not this section.
- Use the list format from `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`.
- Use `High` when the modification changes functionality counter to the original goal.
- Use `Medium` when the modification adds a feature.
- Use `Low` when the modification is limited to spelling or message verbiage.
- If there are no unrequested modifications, write `- None`.

### 7. Is there anything that will fail to execute, or produce the expected outcome

- Detect code paths that will raise exceptions, fail runtime checks, or return incorrect data.
- Confirm whether the implementation can execute end-to-end and produce the desired outcome.
- Do not include required-change details in this section. Any correction needed for a failure, incorrect output, or blocking risk must be listed in `## 12. Changes required`.

### 8. Questions: Is there any thing you are unsure about
- Use a flat list of questions.
- If there are no questions, write `- None`.
- Do not ask whether the plan file should be updated to match the implementation.
- Questions may ask only about ambiguity in applying the plan to the implementation, not whether to change the plan to fit the code.

### 9. Suggested improvements

- Use a flat list of suggested improvements.
- If there are no suggested improvements, write `- None`.
- Recommend specific improvements to address any identified gaps, failures, or incomplete work.
- Recommend improvements that directly serve the original plan goal and do not introduce unnecessary complexity or scope creep.
- Recommend improvements that are precise, actionable, and grounded in the current implementation. Avoid speculative suggestions that are not directly supported by the existing code or plan.
- Do not suggest plan-file, plan-ownership, requirements, acceptance-criteria, or plan-wording changes that would make the plan match the current code.
- Suggested improvements must move implementation, tests, or configuration toward the plan requirements.

### 10. Migration

- Include any necessary migration steps if the plan involves changes that require data transformation, schema updates, or other non-backwards-compatible modifications.
- Use the migration subsections from `.agents/skills/plan-completion-review/references/PLAN_COMPLETION_REVIEW_TEMPLATE.md`: `Database`, `Files`, `Configuration`, and `Other`.
- Each migration subsection must be a simple list.
- If a migration subsection has no items, write `- None`.
- If all migration subsections have no items, write only `- None` directly under `## 10. Migration` and do not include the migration subsection headings.

### 11. Assumptions

- List any assumptions that were made during the review process, such as inferred requirements, expected behavior, or interpretations of the original goal.
- Use a simple flat list.
- If there are no assumptions, write `- None`.

### 12. Changes required

- Use the exact category labels from the template's `## 12. Changes required` section.
- Use the `Add`, `Modify`, and `Remove` groups under each category.
- If there are no required changes at all, write only `- None` directly under `## 12. Changes required` and do not include any change categories.
- If a change category has no required changes, write `- None` directly under that category and do not include `Add`, `Modify`, or `Remove` groups for that category.
- If a change category has required changes, include only the `Add`, `Modify`, and `Remove` groups that contain entries. Do not include empty groups.
- Do not duplicate the same required change across categories. Choose one most-specific category for each required change.
- Do not replace required changes with vague summaries. Every non-`None` item must include the concrete `Required change` field and all supporting fields shown for that category in the template, such as `Reason`, `Verification`, or `Coverage category`.
- `Required change` must name the exact behavior, call, field, test assertion, command, file content, or removal that must be added, modified, or removed.
- **Single required change rule:** each `Required change` must be one concrete request. Do not write alternatives for the coder to choose between.
- Do not use alternative phrasing in `Required change`, such as `do X, or do Y`, `either`, `one of`, `could`, `maybe`, `option`, or `choose`.
- Before finalizing, scan every `Required change` for ` or ` used between possible implementations. Replace it with one selected action.
- If two changes are both required, split them into separate required-change entries or state them as mandatory steps in the same request. Do not phrase mandatory work as an alternative.
- If the reviewer cannot select the single best required change, move the uncertainty to `## 8. Questions: Is there any thing you are unsure about` and do not list the item as a required change.
- Use `Files needing changes` for file-level required changes. Include the exact file path and line when known, and describe the required file-level outcome with enough detail for implementation.
- Do not use generic file summaries such as `Update real-search start behavior`; write the specific required change, such as `Call POST /api/v1/jobs/search/start before routing to /searching`.
- Avoid copying the same wording into multiple categories. When a file also has a function-level entry, the file entry should describe the required file-level outcome and the function entry should describe the symbol-specific logic to implement.
- List class, property, and type changes only under `Classes, properties, and types needing changes`.
- List function changes only under `Functions needing changes`.
- List constant changes only under `Constants needing changes`.
- List test changes only under `Tests needing changes`.
- List markdown, text, JSON, XML, data, and other non-code resource-file changes only under `Resource files needing changes`.
- Use `Notes of major removals` only for removal impact notes that are not already captured by an individual `Remove` entry.
- Be specific, assume the developer is a junior developer and provide specific references and line numbers.
- For function changes, include concrete control flow, calls, and conditions inside `Required change` instead of using a separate implementation-detail field.
- For test changes, include `Verification` with the exact assertion or behavior the test must prove.
- Do not require removal of existing behavior unless the plan explicitly requests removal or the existing behavior directly conflicts with a planned requirement.
- If behavior appears extra but may predate the plan, record it under `## 8. Questions: Is there any thing you are unsure about` or `## 11. Assumptions`, not `## 12. Changes required`.
- If a coding harness or implementation agent added a feature, option, dependency, file, command, UI flow, or behavior that is not required by the plan and is not necessary to satisfy the plan, require that addition to be removed.
- Apply the removal rule only to additions or modifications introduced by the reviewed work. Do not apply it to behavior that existed before the reviewed work unless the plan explicitly requests removal or the preserved behavior conflicts with a planned requirement.
- Do not get optional fixes, do this or that. Only give one option and the option that is the most likely to be the best. The secondary option should be recorded in the Assumptions or Suggested Improvements section, not here in the required changes.
- Outline specific changes, don't report something like  add the five tests listed in the plan, list each test individually with the specific location and description of the test to be added.
- Do not give vague change requirements, be specific. For example, if a new function is needed, give the exact function signature and a brief description of the logic that should be implemented in the function. If a new class is needed, give the exact class name, its properties with types, and a brief description of its methods and their logic.
- Do not require the coder to make a choice between options, select the best option.
- Do not require changes to plan files, plan ownership, requirements, acceptance criteria, or plan wording. Required changes must target implementation, tests, dependencies, configuration, migrations, or code removal needed to satisfy the plan.

### 13. Summary

- Provide a percent estimation of plan completion based on the original goal and the current state of the code.
- Use only the two bullets from the template: `Percent complete` and `Rationale`.
- Write `Percent complete` as a whole-number percentage with a percent sign, for example `85%`.

## Rules

- Use the latest saved code snapshot for the review.
- Only recommend the best path forward that directly serves the original plan goal.
- Verify logic and type correctness before suggesting fixes.
- Keep recommendations precise and grounded in the current implementation.
- If there is a missing package, then recommend adding it to the project dependencies and include the necessary import statement in the code.
- Put extra effort on creating the Changes required section
