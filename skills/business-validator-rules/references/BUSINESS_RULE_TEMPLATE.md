## Goal

- One sentence restating the user's requested outcome for this related group of business rules.

## Rule group summary

- **Rule area:** `[Exact area label from plans/rules/AREAS.md]`
- **Rule group:** `[Human-readable kebab-case group identifier shared by the individual rules and matching this file name]`

## Use cases

- \[Specific use case where a caller invokes the entry point and receives the expected result.]
- \[Another specific use case, or `None`]

## Scope

### In scope:

- \[Behavior, actors, states, or boundaries governed by this rule group.]

### Out of scope:

- \[Behavior explicitly excluded from this rule group, or `None`.]

## Rules

Repeat the following block for each of the 1 to 15 related individual rules in this file. Each rule description must contain one to five sentences and express one testable business constraint.

### `[rule-area]-[rule-group]-[rule-label]`

- **Related to:** `[rule-label]` (`plans/rules/{rule-area}/{rule-group}.md`), or `None`
- **Depends on:** `[rule-label]` (`plans/rules/{rule-area}/{rule-group}.md`), or `None`

\[One-to-five-sentence description of the individual business rule.]

### `[rule-area]-[rule-group]-[another-rule-label]`

- **Related to:** `[rule-label]` (`plans/rules/{rule-area}/{rule-group}.md`), or `None`
- **Depends on:** `[rule-label]` (`plans/rules/{rule-area}/{rule-group}.md`), or `None`

\[One-to-five-sentence description of another related individual business rule.]

If the group would contain more than 15 individual rules, divide it into coherent rule groups and create a separate business-rule file from this template for each group.

## Implementation plans

- `plans/{plan-area}/{plan-file}.md` - `[rule-area]-[rule-group]-[rule-label]`
- `plans/{another-plan-area}/{another-plan-file}.md` - `[rule-area]-[rule-group]-[another-rule-label]`, or `None`

## Assumptions

- Assumptions made about design choices or requirements not explicitly stated in the plan.

## Documentation Sources

- \[Documentation name]: \[Description of the documentation, location, and purpose]

## Questions

- Clarifications needed before implementation, if any.

## Answered questions

- \[Question]
  \[Answer]
- \[Question]
  \[Answer]

## Future features

- \[Possible future extension that will not be implemented in the current plan]
- \[Possible future extension]

## Suggested Improvements

- Useful but unrequested follow-up ideas, if any.
