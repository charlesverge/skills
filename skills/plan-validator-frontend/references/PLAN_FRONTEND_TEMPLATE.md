## Goal

- One sentence restating the user's requested outcome.

## API summary

- **Feature name:** [Feature name]
- **Feature short code:** [Feature category or section-Sub category or sub section-action or feature name. For example, "auth-signin-email" or "favorites-company-add"]
- **Screen location:** [Page, route, modal, section, tab, or component]
- **Route:** [route to the screen location]
- **Priority:** [High | Medium | Low]
- **Caller or trigger:** [Screen or location the user navigates from or preforms to reach this feature or screen]
- **Depends on**: list of plan files that this depends on that must be completed first. ie plans/api/job-create.md plans/features/auth-login.md

## Success definition

- What must be seen and happen on the screen for this feature to function successfully.

## Use cases

- [Specific use case where it describes what a user does to trigger the feature or screen and what the expected outcome is. For example, "A user with an expired session tries to access a protected resource, the user is redirected to the login screen."]
- [Another specific use case]

## Scope

- In scope:
- Out of scope:

## User goal

- **Primary user goal:** [What the user is trying to accomplish]
- **User trigger:** [Button, link, menu item, form submit, tab click, toggle, etc.]
- **Success definition:** [What must happen for this feature to be considered successful]

## Input state before action

- **Authentication:** [Required | Optional | None]
- **State required:** [require state of the user before the action can be preformed or the state needed to see the screen when the user has already taken an action. This should be specific and not just "logged in" or "has access to feature". For example, "User must have at least one company added to see the favorites tab" or "User must have an active session to see the dashboard page"]
- **Failure inputs:** [Invalid states which would cause the action to not work or not be visible to the user. This should be specific, user is logged in and has no companies created]


## Output state after action

- **Authentication:** [Required | Optional | None]
- **State expected:** [require state of the user before the action can be preformed or the state needed to see the screen when the user has already taken an action. This should be specific and not just "logged in" or "has access to feature". For example, "User must have at least one company added to see the favorites tab" or "User must have an active session to see the dashboard page"]
- **Failure states:** [Invalid states which would cause the action to not work or not be visible to the user. This should be specific, user is logged in and has no companies created]

### Output data structures

- **Primary output type:** [Structure name or inline description]
- **Fields:**
  - `[field_name]`: [type] — [purpose]
  - `[field_name]`: [type] — [purpose]
- **Nested objects / arrays:** [Structure details or N/A]
- **Examples:** [Short example response or N/A]

## Error codes

| Code | status | When returned | Notes |
| --- | --- | --- | --- |
| `[ERROR_CODE]` | `[status]` | [Condition] | [Notes] |
| `[ERROR_CODE]` | `[status]` | [Condition] | [Notes] |

## Generic user interface usage

- **Is this a generic user interface?:** [Yes | No]
- **Selector field or route segment:** [Field, route param, or N/A]
- **Supported behaviors:** [List each supported internal behavior]
- **Internal dispatch rules:** [How the request is routed internally]
- **Caller expectations:** [What different callers must send and what they can expect back]
- **Consistency rules:** [What must remain shared across all uses of the user interface]

## Technical references

- **Related APIs:** [Related routes or N/A]
- **Related features:** [Feature plan links or N/A]
- **Dependencies:** [External services, libraries, queues, or N/A]

## UI details

- **Visible elements:** [Buttons, links, text fields, cards, menus, labels]
- **States:** [Default, loading, success, error, empty, disabled]
- **Accessibility notes:** [Keyboard behavior, labels, focus, screen reader notes]

## Mockups

- **Mockup file name:** [mockups/file-name.html]
- **Mockup section:** [Relevant screen, panel, modal, or component]
- **Mockup notes:** [Any mismatch, ambiguity, or confirmed behavior from the mockup]

## Api routes

 - List of api routes needed with the definition of the data sent and received if it is not implemented. if it is implemented, provide the endpoint and method and link to the documentation in plans/api/{endpoint}.md

## Test coverage

- **Test cases needed:**
  - [file name] [test name] [description of what test is ensuring - Happy path]
  - [file name] [test name] [description of what test is ensuring - Validation / error path]
  - [file name] [test name] [description of what test is ensuring - Edge case]
  - [file name] [test name] [description of what test is ensuring - Regression case]

## Verification

- Commands or manual checks to run.

## Current State

- Files, modules, or behavior inspected.
- Relevant constraints or existing patterns.

## Questions

- Clarifications needed before implementation, if any.

## Answered questions

- [Question]
  [Answer]
- [Question]
  [Answer]

## Future features

- [Possible future extension that won't be implemented in the current plan but is worth noting for future work]
- [Possible future extension]

## Suggested Improvements

- Useful but unrequested follow-up ideas, if any.

## Files and Updates

- Modify `path/to/file.py`
  - Add or modify the exact class, function, method, variable, setting, model, db, or resource.
  - Reason: explain why this file must change.
