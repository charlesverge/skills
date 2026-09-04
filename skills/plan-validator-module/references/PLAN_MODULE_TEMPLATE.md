## Goal

- One sentence restating the user's requested module outcome.

## Module summary

- **Module name:** \[Human-readable module name]
- **Module short code:** \[module-purpose, such as `user-profile-update`]
- **Module directory:** \[Exact directory that owns all implementation files]
- **Language/runtime:** \[Python version, Node version, TypeScript target, or other runtime]
- **Package metadata:** \[Exact path to `pyproject.toml`, `package.json`, or equivalent]
- **Public package/import name:** \[Import name parent projects will use]
- **Primary public API:** \[Class, function, or functions parent projects will call]
- **Priority:** \[High | Medium | Low]
- **Depends on:** \[Plan files that must be completed first, or `None`]

## Success definition

- What must happen for the module request to be considered successful.
  - Condition 1
  - Condition 2
  - ...
- What must happen for the module request to be considered successful.
  - Condition 1
  - Condition 2
  - ...

## Use cases

- \[Specific use case where a caller invokes the module and receives the expected result.]
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

## Module boundary

- **Implementation directory:** \[Exact module directory]
- **Files inside module directory:** \[List the allowed application implementation, resource, and package metadata paths]
- **Files outside module directory:** \[List exact `test-conventions` paths, plus other exact files only when the user explicitly requested combined work; otherwise only the test paths]
- **Parent project work:** \[Import/use instructions only, or separate plan required]

## Parent integration contract

- **Import statement:** \[Exact import parent projects will use]
- **Call pattern:** \[Exact class construction or function call shape]
- **Inputs parent must provide:** \[Data, services, callbacks, configuration, or `None`]
- **Outputs parent receives:** \[Return type, data structure, side effects, or `None`]
- **Runtime assumptions:** \[Environment variables, file paths, network access, clock behavior, or `None`]

## Public contract

- **Exports:** \[Exact exported classes, functions, types, constants, or `None`]
- **Primary input type:** \[Type name or inline structure]
- **Input fields:**
  - `[field_name]`: \[type] - \[purpose]
  - `[field_name]`: \[type] - \[purpose]
- **Primary output type:** \[Type name or inline structure]
- **Output fields:**
  - `[field_name]`: \[type] - \[purpose]
  - `[field_name]`: \[type] - \[purpose]
- **Side effects:** \[State changes, file writes, emitted events, API calls, or `None`]
- **Examples:** \[Short code example or `None`]

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

## Package and test commands

- **Install command:** \[Command run from the module directory]
- **Unit test command:** \[Command run from the module directory]
- **Lint/type command:** \[Command run from the module directory, or `N/A`]
- **Build command:** \[Command run from the module directory, or `N/A`]

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
  - `test_module_returns_expected_result`
- Description - Validation / error path
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_module_rejects_invalid_input`
- Description - Edge case
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_module_handles_boundary_input`
- Description - Regression case
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_module_preserves_public_contract`

## Verification

- Commands or manual checks to run from the module directory.

## Files

### `{file location}`

**Short description**: \[Short description of the file's purpose]

- \[function name, class name, variable, etc]
- \[function name, class name, variable, etc]

...This section can repeat for each file required for the functionally of this plan. The files section does not repeat the test files.

## Assumptions

- Assumptions made about design choices or requirements not explicitly stated in the plan.

## External interactions

- **External services:** \[Services this module calls, or `None`]
- **APIs:** \[External APIs this module calls, or `None`]
- **Events:** \[Events emitted or consumed by this module, or `None`]
- **File or database operations:** \[Reads/writes performed by this module, or `None`]
- **Other interactions:** \[Other interactions, or `None`]

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
