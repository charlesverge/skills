## Goal

- One sentence restating the user's requested outcome.

## Frontend summary

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

- **Mockup file name:** [mockups/file-name.html[#section-id]](mockups/file-name.html#data-section)
- **Mockup section:** [Mockup files often have more then one screen, each feature plan is intended to only have one screen. If a mockup has multiple screens in a single html files then each screen will have a <section> tag. For example <section class="screen active" data-screen="favorites" data-screen-label="Favorites"> in this case mockups/Tools.html has a section with data-screen set to favorites which would produce the Mockup file mockups/Tools.html#favorites with a section of favorites]
- **Mockup notes:** [Any specific notes about the mockup and how it functions, for example animations, if it is full screen, specific customizations that don't follow existing patterns, etc.]

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

## Implementation plan

- Each feature which has a visible ui component should have one or more files which render it. For example if a screen is a single button then a single file like {project_dir}/components/FeatureButton.tsx contains the ui component is needed
- If the screen is more complete then it should be broken into individual small components like {project_dir}/components/product/ProductView.tsx {project_dir}/components/product/ProductTitle.tsx {project_dir}/components/product/ProductDescription.tsx which would have rendering and styling for specific elements in the screen. 
- Where routes are defined if for a specific screen and what the route is visible for the user for example: {project_dir}/routes.tsx - /product/{product_id}
- tests {project_dir}/app/main-feature/feature-button.flow.test.tsx
- e2e tests {project_dir}/e2e/feature-button.spec.ts
- Files which link to the component for example: {project_dir}/components/product/ProductList.tsx 

## Questions

- Clarifications needed before implementation, if any.
- If the plan is covering more then one features then outline how the plan should be split into multiple plan files, include recommended file names and short descriptions of the feature, mockup file and section. One line per feature.

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
