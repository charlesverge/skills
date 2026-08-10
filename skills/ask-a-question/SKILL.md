---
name: ask-a-question
description: Ask, structure, save, and resolve clarification questions tied to implementation plans and change specifications. Use when a plan or specification contains an ambiguity, conflict, missing behavior, or unresolved implementation policy that must be decided before or during code work, especially for frontend expectations, backend policy decisions, option comparison, recommendations, question-file naming, answer recording, and related-plan updates.
---

# Ask a Question

## Source of truth

1. Read the controlling implementation plan and change specification before examining implementation details.
1. Treat plans and change specifications as the source of truth for intended behavior.
1. Do not ask a question that the controlling plan or specification already answers.
1. When code differs from the plan or specification, frame the question around the intended documented behavior rather than treating current code as authoritative.
1. When plans or specifications conflict, cite the conflicting statements and ask for the decision needed to make them consistent.

## Question workflow

1. Identify the exact plan and specification statements that create the unresolved decision.
1. Confirm the question is about implementation behavior, scope, or policy, not authorization or approval.
1. Classify the affected system as user-facing or non-user-facing.
1. Ask one decision per question file.
1. Present 2-3 viable solutions that each resolve the issue.
1. State the tradeoff of each solution.
1. Recommend one solution and explain why it best matches the controlling plan or specification.
1. Create the question file using the required path and the template in resources/question-template.md.
1. After receiving an answer, record it in the question file and update every affected plan or specification so the documents agree.

## Frame the question

### User-facing systems

Start from the user's perspective when the application has a frontend component:

1. State what the user is doing.
1. State what the user currently sees or what the plan says they will see.
1. Ask what the user is expected to see or experience after the action.
1. Describe options in visible behavior, interaction, state, and accessibility terms before implementation details.

Example:

> When the user submits the form with an expired session, they currently remain on the form and see a generic error. What should the user see and be able to do next?

### Non-user-facing systems

Frame questions about a backend, API, module, function, job, or other internal system as policy decisions:

1. Name the invariant, requirement, or competing logic.
1. Ask whether the behavior is always required, conditionally required, or prohibited.
1. Ask which logic is correct when two implementations differ.
1. Describe options in contract, state-transition, persistence, and error-handling terms.

Examples:

> Is idempotency always required for this operation, or only when the caller supplies an idempotency key?

> Which policy is correct: reject an incomplete record before persistence, or persist it with an explicit incomplete state?

## Options and recommendation

Provide 2-3 options. Every option must fully answer the question and be implementable.

For each option:

- State the resulting behavior.
- State the main benefit.
- State the main cost or constraint.
- Identify any plan or specification text that the option requires changing.

Recommend exactly one option. Base the recommendation on the source-of-truth documents, user impact for frontend work, and contract consistency for non-user-facing work. Do not recommend a compromise that leaves the decision unresolved.

## Suggested features

When the question is related to adding a feature the topic short name start with suggestion. ie widget-3-suggestion-spinner.md

## File location and naming

Require a related plan before creating a question file.

Given a related plan: `plans/{plan-dir}/{plan-file}.md`

Save its question as: `questions/{plan-dir}/{plan-file}_{n}-{short-topic}.md`

Apply these rules:

1. Preserve the related plan's directory beneath plans/.
1. Use the related plan filename without .md.
1. Use a lowercase hyphenated short topic.
1. Start {n} at 1.
1. Determine {n} from existing question files for that same plan and use the next integer.
1. Keep numbering independent for each plan.

Example:

```markdown
    Related plan: plans/features/favorites-load.md
    First question: questions/features/favorites-load_1-empty-state.md
    Second question: questions/features/favorites-load_2-card-selection.md
```

## Authorization and approval

Do not create question files for authorization or approval requests. Request permission through the active interaction or tool mechanism without adding a file under questions/.

Examples include permission to run a command, access credentials, deploy, publish, spend money, or modify an external system.

## Record an answer

When the user answers:

1. Copy the decision into the question file's Answer section.
1. Change its status from Open to Answered.
1. Record which option was selected, or describe the answer precisely when it differs from the listed options.
1. Update the related plan and every affected change specification with the decided behavior.
1. Remove or revise contradictory plan language and unresolved alternatives.
1. Complete the question file's Plan and specification updates section with the exact files and decisions updated.
1. Keep the question file as the decision record; do not delete it after resolution.
