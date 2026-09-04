## Goal

- One sentence restating the user's requested class outcome.

## Class summary

- **Class name:** \[Human-readable class name]
- **Class short code:** \[class-purpose, such as `health-check-runner`]
- **Owning module directory:** \[Exact directory that owns all implementation files]
- **Language/runtime:** \[Python version, Node version, TypeScript target, or other runtime]
- **Package metadata:** \[Exact path to owning module `pyproject.toml`, `package.json`, or equivalent]
- **Public package/import name:** \[Import name callers will use]
- **Primary class or root/base class:** \[Exact class name]
- **Class file:** \[Exact file path that contains the primary class or root/base class]
- **Caller context:** \[Module, backend API, job, frontend component, parent project, or other caller that constructs or calls the class]
- **Priority:** \[High | Medium | Low]
- **Depends on:** \[Plan files that must be completed first, or `None`]

## Success definition

- What must happen for the class request to be considered successful.
  - Condition 1
  - Condition 2
  - ...
- What must happen for the class request to be considered successful.
  - Condition 1
  - Condition 2
  - ...

## Use cases

- \[Specific use case where a caller constructs the class and receives the expected behavior.]
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

## Module and class boundary

- **Owning module directory:** \[Exact module directory that constrains application implementation, resources, package metadata, and function-plan files]
- **Primary class or root/base class:** \[Class name]
- **Class file:** \[Exact class file path under the owning module directory]
- **Allowed plan files:** \[Exact module-owned implementation, resource, package metadata, and function-plan paths plus exact `test-conventions` paths]
- **External files explicitly in scope:** \[Other exact files outside the owning module directory only when the user explicitly requested combined work; convention-derived test files are excluded; otherwise `None`]
- **Caller wiring:** \[Import/use instructions only, or separate plan required]

## Class hierarchy and object model

- **Object model type:** \[Single class, base class with subclasses, interface/protocol with implementations, abstract base class with concrete adaptors, or other exact model]
- **Generic use pattern:** \[How callers use the primary/root class or contract, such as a harness base class that runs a shared workflow while concrete harnesses override adaptor-specific functions]
- **Root/base class or contract:** \[Exact class, interface, protocol, or abstract base class name and file path, or `None`]
- **Primary class in this plan:** \[Exact primary class name]
- **Hierarchy:** \[Indented class chain such as `HarnessBase -> EmailHarness`, `HarnessBase -> ApiHarness`, or `None`]
- **Shared behavior:** \[Functions, properties, or workflow responsibilities implemented once by the root/base class, or `None`]
- **Required overrides:** \[Functions or properties subclasses/adaptors must implement or override, or `None`]
- **Concrete subclasses/adaptors in scope:** \[Exact classes in scope, or `None`]

| Class or adaptor  | Extends or implements     | File path          | Overrides                           | Purpose                      |
| ----------------- | ------------------------- | ------------------ | ----------------------------------- | ---------------------------- |
| `[ConcreteClass]` | `[BaseClass or Contract]` | \[Exact file path] | \[`function_name`, `function_name`] | \[Specific adaptor behavior] |
| `[ConcreteClass]` | `[BaseClass or Contract]` | \[Exact file path] | \[`function_name`, `function_name`] | \[Specific adaptor behavior] |

## Parent or caller integration contract

- **Import statement:** \[Exact import callers will use]
- **Construction pattern:** \[Exact class construction shape]
- **Call pattern:** \[Exact method/property access shape]
- **Inputs caller must provide:** \[Constructor arguments, method arguments, injected services, callbacks, configuration, or `None`]
- **Outputs caller receives:** \[Instance, return type, data structure, side effects, or `None`]
- **Runtime assumptions:** \[Environment variables, file paths, network access, clock behavior, or `None`]
- **Examples:** \[Short code example or `None`]

## Class public contract

- **Exports:** \[Exact exported classes, functions, types, constants, or `None`]
- **Constructor signature:** \[Exact constructor signature, or `None`]
- **Primary input type:** \[Type name or inline structure]
- **Input fields:**
  - `[field_name]`: \[type] - \[purpose]
  - `[field_name]`: \[type] - \[purpose]
- **Primary output type:** \[Type name or inline structure]
- **Output fields:**
  - `[field_name]`: \[type] - \[purpose]
  - `[field_name]`: \[type] - \[purpose]
- **Side effects:** \[State changes, file writes, emitted events, API calls, or `None`]

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

## Class properties

### `[property_name]`

- **Type**: \[Exact type]
- **Description of use**: \[How the class uses this property]

### `[property_name]`

- **Type**: \[Exact type]
- **Description of use**: \[How the class uses this property]

...repeat for each property. None allowed when there are no class properties.

## Class functions

### `[function_name]`

- **Type**: \[constructor, public method, private method, class method, static method, computed property accessor, abstract method, template method, override method, or removed method]
- **Description of use**: \[How the class uses this function]
- **Function plan markdown file**: [`function-plan-name`](path/to/function-plan.md)

### `[function_name]`

- **Type**: \[constructor, public method, private method, class method, static method, computed property accessor, abstract method, template method, override method, or removed method]
- **Description of use**: \[How the class uses this function]
- **Function plan markdown file**: [`function-plan-name`](path/to/function-plan.md)

...repeat for each function. None allowed when there are no class functions.

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
  - `test_class_constructs_with_required_dependencies`
- Description - Validation / error path
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_class_rejects_missing_required_dependency`
- Description - Edge case
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_class_preserves_optional_default`
- Description - Regression case
  - `tests/{plan_dir}/test_{plan_file}.py`
  - `test_class_keeps_public_properties`

## Verification

- Commands or manual checks to run from the owning module directory.
- Function-plan validation checks run with `plan-validator-functions` for each linked function-plan markdown file.

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
