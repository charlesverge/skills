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

- Provide a list of files, classes, functions that require changes along with description of what change needs to be made to ensure the plan is complete.
- Be specific, assume the developer is a junior developer.

### 15. Summary

- Provide a percent estimation of plan completion based on the original goal and the current state of the code.

## Rules

- Use the latest saved code snapshot for the review.
- Only recommend the best path forward that directly serves the original plan goal.
- Verify logic and type correctness before suggesting fixes.
- Keep recommendations precise and grounded in the current implementation.
- If there is a missing package, then recommend adding it to the project dependencies and include the necessary import statement in the code.