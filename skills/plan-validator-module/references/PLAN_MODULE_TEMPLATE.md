## Goal

* One sentence restating the user's requested module outcome.

## Module summary

* **Module name:** [Human-readable module name]
* **Module short code:** [module-purpose, such as `user-profile-update`]
* **Module directory:** [Exact directory that owns all implementation files]
* **Language/runtime:** [Python version, Node version, TypeScript target, or other runtime]
* **Package metadata:** [Exact path to `pyproject.toml`, `package.json`, or equivalent]
* **Public package/import name:** [Import name parent projects will use]
* **Primary public API:** [Class, function, or functions parent projects will call]
* **Priority:** [High | Medium | Low]
* **Depends on:** [Plan files that must be completed first, or `None`]

## Success definition

* What must happen for the module request to be considered successful.

## Use cases

* [Specific use case where a caller invokes the module and receives the expected result.]
* [Another specific use case, or `None`]

## Scope

* In scope:
* Out of scope:

## Module boundary

* **Implementation directory:** [Exact module directory]
* **Files inside module directory:** [List the allowed implementation, test, resource, and package metadata paths]
* **Files outside module directory:** [Must be `None` unless the user explicitly requested combined work]
* **Parent project work:** [Import/use instructions only, or separate plan required]

## Parent integration contract

* **Import statement:** [Exact import parent projects will use]
* **Call pattern:** [Exact class construction or function call shape]
* **Inputs parent must provide:** [Data, services, callbacks, configuration, or `None`]
* **Outputs parent receives:** [Return type, data structure, side effects, or `None`]
* **Runtime assumptions:** [Environment variables, file paths, network access, clock behavior, or `None`]

## Public contract

* **Exports:** [Exact exported classes, functions, types, constants, or `None`]
* **Primary input type:** [Type name or inline structure]
* **Input fields:**
  * `[field_name]`: [type] - [purpose]
  * `[field_name]`: [type] - [purpose]
* **Primary output type:** [Type name or inline structure]
* **Output fields:**
  * `[field_name]`: [type] - [purpose]
  * `[field_name]`: [type] - [purpose]
* **Side effects:** [State changes, file writes, emitted events, API calls, or `None`]
* **Examples:** [Short code example or `None`]

## Error contract

| Error or exception | When raised or returned | Caller-visible result | Notes |
| ------------------ | ----------------------- | --------------------- | ----- |
| `[ERROR_NAME]`     | [Condition]             | [Result]              | [Notes] |
| `[ERROR_NAME]`     | [Condition]             | [Result]              | [Notes] |

## Package and test commands

* **Install command:** [Command run from the module directory]
* **Unit test command:** [Command run from the module directory]
* **Lint/type command:** [Command run from the module directory, or `N/A`]
* **Build command:** [Command run from the module directory, or `N/A`]

## Technical references

* **Related modules:** [Related modules or `None`]
* **Related parent plans:** [Parent project plans or `None`]
* **Dependencies:** [Libraries, local modules, services, or `None`]

## Test coverage

* `path/to/module/tests/test_file.py` `test_name` Description - Happy path
* `path/to/module/tests/test_file.py` `test_name` Description - Validation / error path
* `path/to/module/tests/test_file.py` `test_name` Description - Edge case
* `path/to/module/tests/test_file.py` `test_name` Description - Regression case

## Verification

* Commands or manual checks to run from the module directory.

## Implementation plan

* `{module_dir}/pyproject.toml` or `{module_dir}/package.json`
  * Python: package name, version, runtime, dependencies, and test configuration.
  * Node/TypeScript: package name, version, `exports`, `main`, `types`, dependencies, and `scripts.test`.
  * Reason: defines the module package and its module-owned test workflow.
* `{module_dir}/src/{package_name}/__init__.py` or `{module_dir}/src/index.ts`
  * Public exports imported by parent projects.
  * Reason: exposes the module's supported public API.
* `{module_dir}/src/{package_name}/service.py`
  * `PrimaryClassOrFunction`
  * Supporting validation or transformation functions.
  * Reason: implements the reusable module behavior.
* `{module_dir}/tests/test_{module_name}.py`
  * Unit tests named in `Test coverage`.
  * Reason: verifies the module independently from parent projects.

## Assumptions

* Assumptions made about design choices or requirements not explicitly stated in the plan.

## External interactions

* **External services:** [Services this module calls, or `None`]
* **APIs:** [External APIs this module calls, or `None`]
* **Events:** [Events emitted or consumed by this module, or `None`]
* **File or database operations:** [Reads/writes performed by this module, or `None`]
* **Other interactions:** [Other interactions, or `None`]

## Documentation Sources

* [Documentation name]: [Description of the documentation, location, and purpose]

## Questions

* Clarifications needed before implementation, if any.

## Answered questions

* [Question]
  [Answer]
* [Question]
  [Answer]

## Future features

* [Possible future extension that will not be implemented in the current plan]
* [Possible future extension]

## Suggested Improvements

* Useful but unrequested follow-up ideas, if any.
