## Goal

- One sentence restating the user's requested function-group outcome.

## Function summary

- **Function group name:** \[Human-readable function group name]
- **Function short code:** \[function-purpose, such as `health-status-check`]
- **Owning module directory:** \[Exact directory that owns all implementation files]
- **Language/runtime:** \[Python version, Node version, TypeScript target, or other runtime]
- **Package metadata:** \[Exact path to owning module `pyproject.toml`, `package.json`, or equivalent]
- **Primary entry point:** \[Exact function name or Class and function name with signature]
- **Entry point file:** \[Exact file path that contains the entry point]
- **Caller context:** \[Module, Class, backend API, job, frontend component, or other caller that invokes the entry point]
- **Priority:** \[High | Medium | Low]
- **Depends on:** \[Plan files that must be completed first, or `None`]

## Success definition

- What must happen for the function-group request to be considered successful.
  - Condition 1
  - Condition 2
  - ...
- What must happen for the function-group request to be considered successful.
  - Condition 1
  - Condition 2
  - ...

## Use cases

- \[Specific use case where a caller invokes the entry point and receives the expected result.]
- \[Another specific use case, or `None`]

## Scope

### In scope:

- \[Specific items that are in scope for this feature or screen. For example, "The login screen will have a username and password field, a submit button, and a link to reset the password."]
- \[Specific items that are in scope for this feature or screen. For example, "The login screen will have a username and password field, a submit button, and a link to reset the password."]
- \[Specific items that are in scope for this feature or screen. For example, "The login screen will have a username and password field, a submit button, and a link to reset the password."]

### Out of scope:

- \[Specific items that are out of scope for this feature or screen. For example, "The login screen will not handle password recovery."]
- \[Specific items that are out of scope for this feature or screen. For example, "The login screen will not handle password recovery."]
- \[Specific items that are out of scope for this feature or screen. For example, "The login screen will not handle password recovery."]

## Function boundary

- **Owning module directory:** \[Exact module directory]
- **Files inside module directory:** \[List the allowed application implementation, resource, and package metadata paths]
- **Files outside module directory:** \[List exact `test-conventions` paths, plus other exact files only when the user explicitly requested combined work; otherwise only the test paths]
- **Primary entry point:** \[Function name and signature]
- **Helper scope:** \[Helpers in entry point file, existing reused helpers, modified shared helpers, or `None`]
- **Caller wiring:** \[Import/use instructions only, or separate plan required]

## Entry point contract

- **Import statement:** \[Exact import callers will use]
- **Call pattern:** \[Exact function call shape]
- **Inputs caller must provide:** \[Arguments, injected services, callbacks, configuration, or `None`]
- **Primary input type:** \[Type name or inline structure]
- **Input fields:**
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]
- **Primary output type:** \[Type name or inline structure]
- **Output fields:**
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]
- **Side effects:** \[State changes, file writes, emitted events, API calls, or `None`]
- **Runtime assumptions:** \[Environment variables, file paths, network access, clock behavior, or `None`]
- **Examples:** \[Short code example or `None`]

## Core functionality and logic

### Functionality short name 1

- Description of the Functionality and exact details on how it works
- Description of the functionality and specific case specific details

### Functionality short name 2..n

- Description of the Functionality and exact details on how it works
- Description of the functionality and specific case specific details

### Functionality logic name 1

- Description of the logic and exact details on how it works
- Description of the logic and specific case specific details

### Functionality logic name 2..n

- Description of the logic and exact details on how it works
- Description of the logic and specific case specific details

## Helper functions

### `[helper_name]`

- **Purpose**: \[Short description of the helper function's purpose]
- **Location**: \[Exact file path]
- **Classification**: \[Private, Shared]
- **Input fields:**
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]
- **Primary output type:** \[Type name or inline structure]
- **Output fields:**
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]
  - `[field_name]`: \[type | int | str | bool | list | dict | None | ClassName | InlineStructure | ...] - \[purpose]

...repeat for each helper function in the entry point file, and any shared helpers that are modified or newly created for this function group. - None allowed when there is no helper functions. Helper functions are used to break a larger function into smaller unit testable pieces. Private helper is only used by this plan, shared helper is used by multiple plans and should be in a shared location.

## Error contract

### `[ERROR_NAME]`

- **When raised or returned**: \[Condition]
- **Caller-visible result**: \[Result]
- **Notes**: \[Notes]

### `[ERROR_NAME]`

- **When raised or returned**: \[Condition]
- **Caller-visible result**: \[Result]
- **Notes**: \[Notes]

...repeat for each error. None allowed when there are no error cases.

## Dependency boundaries

- **Network:** \[DNS, port, HTTP, websocket, or `None`]
- **Filesystem:** \[Reads/writes, or `None`]
- **Database:** \[Reads/writes, or `None`]
- **Browser or DOM:** \[Interactions, or `None`]
- **Clock/time:** \[Time reads, timers, timeouts, or `None`]
- **Environment/configuration:** \[Environment variables, settings, or `None`]
- **Injected dependencies:** \[Clients, functions, adapters, callbacks, or `None`]

## Package and test commands

- **Install command:** \[Command run from the owning module directory]
- **Unit test command:** \[Command run from the owning module directory]
- **Lint/type command:** \[Command run from the owning module directory, or `N/A`]
- **Build command:** \[Command run from the owning module directory, or `N/A`]

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

## Test coverage

- Description - Shared fixture
  - `tests/global/fixtures/{fixture file}`
- Description - Shared fixture
  - `tests/{plan_dir}/fixtures/{fixture file}`
- Description - Happy path
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_primary_entry_point_returns_expected_result`
- Description - Validation / error path
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_primary_entry_point_returns_documented_error`
- Description - Edge case
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_primary_entry_point_handles_boundary_input`
- Description - Regression case
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_primary_entry_point_preserves_result_contract`

## Verification

- Commands or manual checks to run from the owning module directory.

## Files

### `{file location}`

**Short description**: \[Short description of the file's purpose]

- \[function name, class name, variable, etc]
- \[function name, class name, variable, etc]

...This section can repeat for each file required for the functionally of this plan. The files section does not repeat the test files.

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
