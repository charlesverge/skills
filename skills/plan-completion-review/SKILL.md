---
name: plan-completion-review
description: Review a completed plan against the original goal, validate code and tests, and identify missing or incomplete work.
---

# Plan Completion Review Skill

Validate that an existing plan is complete, the implementation meets the original goal, and the final code is reliable.

## When to Use

- The user asks to verify whether a plan is complete
- The user asks whether the implementation satisfies the original goal
- The user asks for a final review of completed work or plan closure
- The user asks for a checklist of completed features and remaining gaps

## Review Process

1. Read the most recently saved code before forming conclusions.
1. Identify the original goal and plan objectives from the request or existing task description.
1. Confirm the review only recommends the best course of action to move forward toward the original plan goals.
1. Do not offer speculative or "likely" fixes. Verify logic and types first, then recommend concrete, verified corrections.

## Review Sections

### 1. Run tests, linters

- Confirm whether the existing code has test coverage for the completed plan.
- Recommend running the appropriate test suite and static analysis tools.
- Note any failures or missing checks that prevent a reliable conclusion.
- Ensure that all tests pass and linters are clean before proceeding with the review.

### 2. Review code for unexpected side effects

- Look for changes that may affect unrelated behavior.
- Verify that side effects are intentional, documented, and isolated.
- Confirm no silent global state mutations, hidden I/O, or unsafe retries were introduced.

### 3. Create a list of features and ensure they are all completed

- Extract the feature list from the original plan or request.
- Check each feature against the code and mark it as completed, missing, or partial.

### 4. Verify the plan is valid. Ensure the original goal has been met with the plan

- Confirm the plan structure itself is coherent and directly aligned with the original goal.
- Verify the plan covers all required steps and does not contain unsupported assumptions.

### 5. Verify the code completes the original goal

- Confirm that the implementation satisfies the requested outcome.
- Validate the expected behavior with the code paths and any available examples.

### 6. What is missing from code, what was requested but not added or modified

- Identify requested items that are absent from the final code.
- Distinguish between omitted work and work that may be present but incomplete.

### 7. What is incomplete, what was partially completed

- Identify partial implementations, placeholders, or half-finished sections.
- Call out any work that requires further completion before the plan can be deemed done.

### 8. Is there anything that will fail to execute, or produce the expected outcome

- Detect code paths that will raise exceptions, fail runtime checks, or return incorrect data.
- Confirm whether the implementation can execute end-to-end and produce the desired outcome.

### 9. Questions: Is there any thing you are unsure about
- Ask any questions you have in this section

### 10. Suggested improvements

- Recommend specific improvements to address any identified gaps, failures, or incomplete work.
- Recommend improvements that directly serve the original plan goal and do not introduce unnecessary complexity or scope creep.
- Recommend improvements that are precise, actionable, and grounded in the current implementation. Avoid speculative suggestions that are not directly supported by the existing code or plan.

### 11. Migration

- Include any necessary migration steps if the plan involves changes that require data transformation, schema updates, or other non-backwards-compatible modifications.

### 12. Assumptions

- List any assumptions that were made during the review process, such as inferred requirements, expected behavior, or interpretations of the original goal.

### 13. Verification

- List steps to verify the changes where successful

### 14. Changes required

- Create a list of files which need changes and describe what needs to change
- Create a list of classes and describe what changes need to be made to those classes to ensure the plan is complete
- Create a list of types and describe specifically what needs to change, is it a field rename? New type? Remove property? Be specific about the change needed.
- Create a list of functions that require changes along with description of what change needs to be made to ensure the plan is complete.
- Be specific, assume the developer is a junior developer and provide specific references and line numbers.
- If it is not in the plan, favor asking for it to be removed.
- Do not get optional fixes, do this or that. Only give one option and the option that is the most likely to be the best. The secondary option should be recorded in the Assumptions or Suggested Improvements section, not here in the required changes.
- Outline specific changes, don't report something like  add the five tests listed in the plan, list each test individually with the specific location and description of the test to be added.
- Do not give vague change requirements, be specific. For example, if a new function is needed, give the exact function signature and a brief description of the logic that should be implemented in the function. If a new class is needed, give the exact class name, its properties with types, and a brief description of its methods and their logic.
- Do not require the coder to make a choice between options, select the best option.

### 15. Summary

- Provide a percent estimation of plan completion based on the original goal and the current state of the code.

## Rules

- Use the latest saved code snapshot for the review.
- Only recommend the best path forward that directly serves the original plan goal.
- Verify logic and type correctness before suggesting fixes.
- Keep recommendations precise and grounded in the current implementation.
- If there is a missing package, then recommend adding it to the project dependencies and include the necessary import statement in the code.
- Put extra effort on creating the Changes required section