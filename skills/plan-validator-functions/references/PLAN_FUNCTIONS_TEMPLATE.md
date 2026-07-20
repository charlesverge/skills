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

## Use cases

- \[Specific use case where a caller invokes the entry point and receives the expected result.]
- \[Another specific use case, or `None`]

## Scope

- In scope:
- Out of scope:

## Function boundary

- **Owning module directory:** \[Exact module directory]
- **Files inside module directory:** \[List the allowed implementation, test, resource, and package metadata paths]
- **Files outside module directory:** \[Must be `None` unless the user explicitly requested combined work]
- **Primary entry point:** \[Function name and signature]
- **Helper scope:** \[Helpers in entry point file, existing reused helpers, modified shared helpers, or `None`]
- **Caller wiring:** \[Import/use instructions only, or separate plan required]

## Entry point contract

- **Import statement:** \[Exact import callers will use]
- **Call pattern:** \[Exact function call shape]
- **Inputs caller must provide:** \[Arguments, injected services, callbacks, configuration, or `None`]
- **Primary input type:** \[Type name or inline structure]
- **Input fields:**
  - `[field_name]`: \[type] - \[purpose]
  - `[field_name]`: \[type] - \[purpose]
- **Primary output type:** \[Type name or inline structure]
- **Output fields:**
  - `[field_name]`: \[type] - \[purpose]
  - `[field_name]`: \[type] - \[purpose]
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

| Helper function | Location           | Classification                                                                           | Inputs    | Output    | Purpose    |
| --------------- | ------------------ | ---------------------------------------------------------------------------------------- | --------- | --------- | ---------- |
| `[helper_name]` | \[Exact file path] | \[New private helper, Existing reused helper, Modified shared helper, or Removed helper] | \[Inputs] | \[Output] | \[Purpose] |
| `[helper_name]` | \[Exact file path] | \[New private helper, Existing reused helper, Modified shared helper, or Removed helper] | \[Inputs] | \[Output] | \[Purpose] |

## Error contract

| Error or result | When raised or returned | Caller-visible result | Notes    |
| --------------- | ----------------------- | --------------------- | -------- |
| `[ERROR_NAME]`  | \[Condition]            | \[Result]             | \[Notes] |
| `[ERROR_NAME]`  | \[Condition]            | \[Result]             | \[Notes] |

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

- **Related modules:** \[Related modules or `None`]
- **Related APIs or components:** \[Related routes, jobs, components, or `None`]
- **Dependencies:** \[Libraries, local helpers, services, or `None`]

## Test coverage

- `path/to/module/tests/test_file.py` `test_name` Description - Happy path
- `path/to/module/tests/test_file.py` `test_name` Description - Validation / error path
- `path/to/module/tests/test_file.py` `test_name` Description - Edge case
- `path/to/module/tests/test_file.py` `test_name` Description - Regression case

## Verification

- Commands or manual checks to run from the owning module directory.

## Implementation plan

- `{module_dir}/pyproject.toml` or `{module_dir}/package.json`
  - Existing package metadata used by the owning module.
  - Python: package name, runtime, dependencies, and test configuration.
  - Node/TypeScript: package name, `exports`, `main`, `types`, dependencies, and `scripts.test`.
  - Reason: provides the owning module package and test workflow used by this function group.
- `{module_dir}/src/{package_name}/status.py` or `{module_dir}/src/status.ts`
  - `primary_entry_point`
  - New private helper functions.
  - Existing reused helper imports.
  - Reason: contains the single entry point and helper orchestration for the function group.
- `{module_dir}/tests/test_{function_group}.py` or `{module_dir}/src/{function_group}.test.ts`
  - Unit tests named in `Test coverage`.
  - Reason: verifies the function group through the primary entry point.

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
