## Goal

- One sentence restating the user's requested outcome.

## API summary

- **API name:** [API name]
- **API short code:** [API area-action or route-purpose]
- **Route:** [HTTP method and route]
- **Priority:** [High | Medium | Low]
- **Caller or trigger:** [Screen, component, background task, chat step, or other caller that will invoke this API, class, function, job etc]
- **Depends on**: list of plan files that this depends on that must be completed first. ie plans/api/job-create.md

## Success definition

- What must happen for the request to be considered successful

## Use cases

- [Specific use case where it describes what a user does to trigger the API and what the expected outcome is. For example, "A user with an expired session tries to access a protected resource, triggering the API to refresh their session and allow access without forcing them to log in again."]
- [Another specific use case]

## Scope

- In scope:
- Out of scope:

## Request contract

- **Authentication:** [Required | Optional | None]
- **Headers:** [Required headers, content type, idempotency rules, or N/A]
- **Path params:** [Param name, type, meaning, or N/A]
- **Query params:** [Param name, type, meaning, defaults, or N/A]
- **Request body contract:** [Describe the request body structure]
- **Validation rules:** [Required fields, allowed values, size limits, format constraints]
- **Failure inputs:** [Invalid input cases and what causes rejection]
- **Method**: [POST, GET, PUT, PATCH, DELETE]

### Input contract structures

- **Primary input type:** [Structure name or inline description]
- **Fields:**
  - `[field_name]`: [type] — [purpose]
  - `[field_name]`: [type] — [purpose]
- **Nested objects / arrays:** [Structure details or N/A]
- **Examples:** [Short example payload or N/A]

## Output contract

- **Success envelope:** [Describe the success response]
- **Output data contract:** [Describe the `data` structure]
- **State changes:** [Persistence, events, cache updates, or N/A]
- **Failure behavior:** [What the caller receives on failure]

### Output data structures

- **Primary output type:** [Structure name or inline description]
- **Fields:**
  - `[field_name]`: [type] — [purpose]
  - `[field_name]`: [type] — [purpose]
- **Nested objects / arrays:** [Structure details or N/A]
- **Examples:** [Short example response or N/A]

## Error codes

| Code | HTTP status | When returned | Notes |
| --- | --- | --- | --- |
| `[ERROR_CODE]` | `[status]` | [Condition] | [Notes] |
| `[ERROR_CODE]` | `[status]` | [Condition] | [Notes] |

## Generic endpoint usage

- **Is this a generic endpoint?:** [Yes | No]
- **Selector field or route segment:** [Field, route param, or N/A]
- **Supported behaviors:** [List each supported internal behavior]
- **Internal dispatch rules:** [How the request is routed internally]
- **Caller expectations:** [What different callers must send and what they can expect back]
- **Consistency rules:** [What must remain shared across all uses of the endpoint]

## Technical references

- **Related APIs:** [Related routes or N/A]
- **Related features:** [Feature plan links or N/A]
- **Dependencies:** [External services, libraries, queues, or N/A]

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
