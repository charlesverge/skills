## Goal

- One sentence restating the user's requested outcome.

## Frontend summary

- **Feature name:** \[Feature name]
- **Feature short code:** \[Feature category or section-Sub category or sub section-action or feature name. For example, "auth-signin-email" or "favorites-company-add"]
- **Screen location:** \[Exact screen name from the nearest `plans/*/01_SCREENS.md` entry. If the plan only covers part of that screen, append the specific modal, section, tab, or component.]
- **Route:** \[route to the screen location]
- **Priority:** \[High | Medium | Low]
- **Caller or trigger:** \[Screen or location the user navigates from or preforms to reach this feature or screen]
- **Depends on API plan**: list of API plan files that this depends on that must be completed first. If there are truly  no dependencies then explain why here.
- **Depends on feature plans**: list of feature plan files that this depends on that must be completed first. For example, if the screen is a report screen that is accessed from a dashboard page, then the home page must be completed first. ie plans/feature/dashboard-page.md. If the screen is directly navigated to then None can be used. If there are truly  no dependencies then explain why here.
- **Depends on actions**: List of plans which are triggered by this screen or component. For if this was the dashboard plan, then it would link to the report screen plan. If there are truly  no dependencies then explain why here.

## Success definition

- What must be seen and happen on the screen for this feature to function successfully.
  - Condition 1
  - Condition 2
  - ...
- What must be seen and happen on the screen for this feature to function successfully.
  - Condition 1
  - Condition 2
  - ...

## Use cases

- \[Specific use case where it describes what a user does to trigger the feature or screen and what the expected outcome is. For example, "A user with an expired session tries to access a protected resource, the user is redirected to the login screen."]
- \[Another specific use case]

## Scope

### In scope:

- \[Specific items that are in scope for this feature or screen. For example, "The login screen will have a username and password field, a submit button, and a link to reset the password."]
- \[Specific items that are in scope for this feature or screen. For example, "The login screen will have a username and password field, a submit button, and a link to reset the password."]
- \[Specific items that are in scope for this feature or screen. For example, "The login screen will have a username and password field, a submit button, and a link to reset the password."]

### Out of scope:

- \[Specific items that are out of scope for this feature or screen. For example, "The login screen will not handle password recovery."]
- \[Specific items that are out of scope for this feature or screen. For example, "The login screen will not handle password recovery."]
- \[Specific items that are out of scope for this feature or screen. For example, "The login screen will not handle password recovery."]

## User goal

- **Primary user goal:** \[What the user is trying to accomplish]
- **User trigger:** \[Button, link, menu item, form submit, tab click, toggle, etc.]
- **Success definition:** \[What must happen for this feature to be considered successful]

## Input state before action

- **Authentication:** \[Required | Optional | None]
- **State required:** \[require state of the user before the action can be preformed or the state needed to see the screen when the user has already taken an action. This should be specific and not just "logged in" or "has access to feature". For example, "User must have at least one company added to see the favorites tab" or "User must have an active session to see the dashboard page"]
- **Failure inputs:** \[Invalid states which would cause the action to not work or not be visible to the user. This should be specific, user is logged in and has no companies created]

## Output state after action

- **Authentication:** \[Required | Optional | None]
- **State expected:** \[require state of the user before the action can be preformed or the state needed to see the screen when the user has already taken an action. This should be specific and not just "logged in" or "has access to feature". For example, "User must have at least one company added to see the favorites tab" or "User must have an active session to see the dashboard page"]
- **Failure states:** \[Invalid states which would cause the action to not work or not be visible to the user. This should be specific, user is logged in and has no companies created]

### Output data structures

- **Primary output type:** \[Structure name or inline description]
- **Fields:**
  - `[field_name]`: \[type] — \[purpose]
  - `[field_name]`: \[type] — \[purpose]
- **Nested objects / arrays:** \[Structure details or N/A]
- **Examples:** \[Short example response or N/A]

## Error codes

### `[ERROR_CODE]`

- **Status**: \[status]
- **When returned**: \[Condition]
- **Notes**: \[Notes]

### `[ERROR_CODE]`

- **Status**: \[status]
- **When returned**: \[Condition]
- **Notes**: \[Notes]

...repeat for each error code. None allowed when there are no error cases.

## Generic user interface usage

- **Is this a generic user interface?:** \[Yes | No]
- **Selector field or route segment:** \[Field, route param, or N/A]
- **Supported behaviors:** \[List each supported internal behavior]
- **Internal dispatch rules:** \[How the request is routed internally]
- **Caller expectations:** \[What different callers must send and what they can expect back]
- **Consistency rules:** \[What must remain shared across all uses of the user interface]

## Technical references

- **Related APIs:**
  - \[Related route or None]
  - \[Related route]
  - ...
- **Related plans:**
  - \[plan or None]
  - \[plan]
  - ...
- **Dependencies:**
  - \[Other plan, External service, library, queue, or None]
  - \[Other plan, External service, library, queue]
  - ...

## UI details

- **Visible elements:** \[Buttons, links, text fields, cards, menus, labels]
- **States:** \[Default, loading, success, error, empty, disabled]
- **Accessibility notes:** \[Keyboard behavior, labels, focus, screen reader notes]

## Mockups

- **Mockup file name:** [mockups/file-name.html\[#section-id\]](mockups/file-name.html#data-section)
- **Mockup section:** \[Mockup files often have more then one screen, each feature plan is intended to only have one screen. If a mockup has multiple screens in a single html files then each screen will have a <section> tag. For example <section class="screen active" data-screen="favorites" data-screen-label="Favorites"> in this case mockups/Tools.html has a section with data-screen set to favorites which would produce the Mockup file mockups/Tools.html#favorites with a section of favorites]
- **Mockup notes:** \[Any specific notes about the mockup and how it functions, for example animations, if it is full screen, specific customizations that don't follow existing patterns, etc.]

## Api routes

- List of api routes needed with the definition of the data sent and received if it is not implemented. if it is implemented, provide the endpoint and method and link to the documentation in plans/api/{endpoint}.md

## Test coverage

- Description - Shared fixture
  - `tests/global/fixtures/{fixture file}`
- Description - Shared fixture
  - `tests/{plan_dir}/fixtures/{fixture file}`
- Description - Happy path
  - `tests/{plan_dir}/{plan_file}.test.tsx`
  - `renders the completed feature state`
- Description - Validation / error path
  - `tests/{plan_dir}/{plan_file}.test.tsx`
  - `shows the documented validation message`
- Description - Edge case
  - `tests/{plan_dir}/{plan_file}.test.tsx`
  - `handles an empty response without layout breakage`
- Description - Regression case
  - `tests/{plan_dir}/{plan_file}.test.tsx`
  - `preserves the existing keyboard interaction`
- Description - Happy path
  - `tests/{plan_dir}/{plan_file}.spec.ts`
  - `completes the documented user flow`

## Verification

- Commands or manual checks to run.

## Files

### `{file location}`

**Short description**: \[Short description of the file's purpose]

- \[function name, class name, variable, etc]
- \[function name, class name, variable, etc]

...This section can repeat for each file required for the functionally of this plan. The files section does not repeat the test files.

## Assumptions

- Assumptions made about design choices, or other items that are not explicitly stated in the plan

## Questions

- Clarifications needed before implementation, if any.
- If the plan is covering more then one features then outline how the plan should be split into multiple plan files, include recommended file names and short descriptions of the feature, mockup file and section. One line per feature.

## Answered questions

- \[Question]
  \[Answer]
- \[Question]
  \[Answer]

## Future features

- \[Possible future extension that won't be implemented in the current plan but is worth noting for future work]
- \[Possible future extension]

## Suggested Improvements

- Useful but unrequested follow-up ideas, if any.
