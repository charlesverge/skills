## Goal

- One sentence restating the user's requested outcome.

## API summary

- **API name:** \[API name]
- **API short code:** \[API area-action or route-purpose]
- **Route:** \[HTTP method and route]
- **Priority:** \[High | Medium | Low]
- **Caller or trigger:** \[Screen, component, background task, chat step, or other caller that will invoke this API, class, function, job etc]
- **Depends on**: list of plan files that this depends on that must be completed first. ie plans/api/job-create.md

## Success definition

- What must happen for the request to be considered successful.
  - Condition 1
  - Condition 2
  - ...
- What must happen for the request to be considered successful.
  - Condition 1
  - Condition 2
  - ...

## Use cases

- \[Specific use case where it describes what a user does to trigger the API and what the expected outcome is. For example, "A user with an expired session tries to access a protected resource, triggering the API to refresh their session and allow access without forcing them to log in again."]
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

## Request contract

- **Authentication:** \[Required | Optional | None]
- **Headers:** \[Required headers, content type, idempotency rules, or N/A]
- **Path params:** \[Param name, type, meaning, or N/A]
- **Query params:** \[Param name, type, meaning, defaults, or N/A]
- **Request body contract:** \[Describe the request body structure]
- **Validation rules:** \[Required fields, allowed values, size limits, format constraints]
- **Failure inputs:** \[Invalid input cases and what causes rejection]
- **Method**: \[POST, GET, PUT, PATCH, DELETE]

### Input contract structures

- **Primary input type:** \[Structure name or inline description]
- **Fields:**
  - `[field_name]`: \[type] — \[purpose]
  - `[field_name]`: \[type] — \[purpose]
- **Nested objects / arrays:** \[Structure details or N/A]
- **Examples:** \[Short example payload or N/A]

## Output contract

- **Success envelope:**
  - \[Describe the success response]
    - ```json
      {
        "data": { ... },
        "status": "success",
        "message": "..."
      }
      ```
    - \[Additional conditions]
- **Output data contract:**
  - \[Describe the `data` structure]
  - ```json
    {
      "field1": "...",
      "field2": "...",
      ...
    }
    ```
  - \[Additional conditions]
- **State changes:**
  - \[Persistence, events, cache updates, or N/A]
  - \[Persistence, events, cache updates, or N/A]
- **Failure behavior:**
  - \[What the caller receives on failure]
  - ```json
    {
      "error": { ... },
      "status": "error",
      "message": "..."
    }
    ```
  - \[Additional conditions]

### Output data structures

- **Primary output type:** \[Structure name or inline description]
- **Fields:**
  - `[field_name]`: \[type] — \[purpose]
  - `[field_name]`: \[type] — \[purpose]
- **Nested objects / arrays:** \[Structure details or N/A]
- **Examples:** \[Short example response or N/A]

## Error codes

| Code           | HTTP status | When returned | Notes    |
| -------------- | ----------- | ------------- | -------- |
| `[ERROR_CODE]` | `[status]`  | \[Condition]  | \[Notes] |
| `[ERROR_CODE]` | `[status]`  | \[Condition]  | \[Notes] |

## Generic endpoint usage

- **Is this a generic endpoint?:** \[Yes | No]
- **Selector field or route segment:** \[Field, route param, or N/A]
- **Supported behaviors:** \[List each supported internal behavior]
- **Internal dispatch rules:** \[How the request is routed internally]
- **Caller expectations:** \[What different callers must send and what they can expect back]
- **Consistency rules:** \[What must remain shared across all uses of the endpoint]

## Technical references

- **Related APIs:** \[Related routes or N/A]
- **Related features:** \[Feature plan links or N/A]
- **Dependencies:** \[External services, libraries, queues, or N/A]

## Test coverage

- `tests/{plan_dir}/test_{plan_file}.py` `test_feature_uses_enabled_path_when_flag_enabled` Ensures the feature uses the enabled path when the feature flag is enabled - Happy path
- `tests/{plan_dir}/test_{plan_file}.py` `test_feature_rejects_invalid_input` Ensures the feature returns the documented validation error code for invalid input - Validation / error path
- `tests/{plan_dir}/test_{plan_file}.py` `test_feature_handles_empty_input` Ensures the feature returns the documented empty result for empty input - Edge case
- `tests/{plan_dir}/test_{plan_file}.py` `test_feature_preserves_existing_contract` Ensures the existing response contract remains unchanged - Regression case

## Verification

- Commands or manual checks to run.

## Implementation plan

- `{project_dir}/src/{api}/{endpoint}.py`
  - `EndpointHandler`
  - `handle_request`
  - Reason: main entry point for the API endpoint that accepts the request, validates it, performs the required action, and returns the response.
- `{project_dir}/src/{api}/contracts.py`
  - `FeatureRequest`
  - `FeatureResponse`
  - Reason: defines the request and response contracts callers depend on.
- `{project_dir}/settings.py`
  - `PLAN_VALIDATION_ENABLED = True`
  - Reason: configures the enabled path for this API behavior.

## Assumptions

- Assumptions made about design choices, or other items that are not explicitly stated in the plan

## Data storage and operations

- **Data models:** \[List of data models used this API, ie models/model.md]
- **Persistence operations:** \[Create, read, update, delete operations performed on the data models]

### Queries

- Create session: insert a new document with `session_id`, `user_id`, `created_at`, `expires_at`, `last_seen_at`, `revoked_at: null`, `ip`, and `user_agent`.
- Validate session: find document by `session_id`, check `revoked_at` is `null` and `expires_at` is in the future, update `last_seen_at` to now

## External interactions

- **External services:** \[List of external services this API interacts with]
- **APIs:** \[List of external APIs this API calls, with brief descriptions]
- **Events:** \[List of events emitted or consumed by this API, with brief descriptions]
- **Other interactions:** \[Any other external interactions, such as message queues, caches, etc.]

### Documentation Sources

- \[Documentation name]: \[Description of the documentation, its location, and what it's used for, this could be a url or an internal doc like api/opencode.md]

## Questions

- Clarifications needed before implementation, if any.

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
