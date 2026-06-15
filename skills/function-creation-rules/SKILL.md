---
name: function-creation-rules
description: Rules for creating functions, modifying existing ones, including when to create new functions, how to structure them, and how to handle parameters and backward compatibility.
---

# Function Creation Rules

## Extracted function-related rules

* Do not define nested functions inside other functions or methods unless explicitly asked for.
* Before creating custom code, check whether a module already provides the requested functionality. If a module is close but not exact, outline the differences and ask whether the user wants to adjust the specifications.
* nonlocal is not allowed. Use a class.

## Function creation

* If a function is in another module do not copy it, import and use it. If you need the function to modified, request modification approval.
* Do not create a duplicate function, reuse existing functions and utilities. If there is not an exact function that can be reused, check if there is a function that can be modified to satisfy the requirements without breaking existing functionality. If there is a function that can be modified, ask the user if they want to modify the existing function or create a new one.
* When a shared utility is the declared source of truth (for example `recruiter_common.urls.url_candidates`), do not implement endpoint-local fallback/canonicalization logic for the same concern.
* If required behavior is missing from the shared utility, report it explicitly as a shared-utility defect with concrete input/output examples and stop local workaround changes unless explicitly approved.
* Don't create a fall back unless explicitly asked for
* Avoid the use of built in functions like attrib, hasattr for classes which can accessed like ClassName.property\_name
* If a reference is already a str don't add str() to it.
* Avoid unnecessary copying of input data structures (lists, dicts, sets, tuples, dataclasses, models, arrays, payload objects, and nested structures). Reuse existing references and process data in place or as a stream unless duplication is required for correctness (immutability boundaries, mutation safety, ordering guarantees, concurrency isolation, or explicit API contract).
* Keep multi-step processes in distinct phases with explicit boundaries and handoff data (for example: collect/validate, transform/enrich, persist/output). Do not blend unrelated phases in one loop or helper unless explicitly required.
* Do not introduce phase-boundary carrier types (for example dedicated dataclasses, models, or wrappers created only to move data between internal phases) unless explicitly asked by the user.
* Prefer passing existing domain models or standard built-in containers across phase boundaries. If stricter typing is needed, update function signatures/call sites directly instead of creating a carrier type.
* Prefer streaming data from databases/cursors and process records incrementally; avoid materializing full result sets in memory unless required by correctness or an explicit API contract.
* Do not repeat validation/error checks for invariants already guaranteed by an earlier phase in the same execution flow. Downstream phases should rely on established contracts and only validate new assumptions introduced at that phase.
* Avoid the use of built in functions like attrib, hasattr for classes which can accessed like ClassName.property_name
* Functions in classes that don't use self should be staticmethod or moved to a helpers module. If the function is only used in one class, staticmethod is preferred. If the function is used in multiple classes, move it to a helpers module.


## Function parameters

* Prefer creating functions that accept a single type and avoid multiple types or a None parameter.
* If the function requires the parameter, then it cannot accept a type of None
* Any caller of a function must pass a valid value for all parameters that are required.
* Avoid adding parameters with a default value or a type or None. This causes bugs to occur as it hides type check errors. Is a very strong case to use parameter_name: type | None = None then stop and request permission.
* Use the skill python-type-rules to ensure that parameters have strict types and avoid the use of Any, object, or other escape hatches that allow any type.
* Use of type | None, ie int | None = None requires approval

## No Pass-Through Helpers

* Do not create one-line wrapper/helper functions that only forward arguments and return another function call.
* If a signature changes, update all call sites and tests directly instead of adding compatibility wrappers.
* Allowed exception: explicit user request for backward compatibility (must be documented in the change note with the dependent caller).

## No Read-Time Repairs

* Do not mutate persisted records, payloads, config, files, or schema fields during read/fetch paths to repair missing or legacy data.
* Read paths may interpret documented defaults for returned objects, but they must not save those defaults back to storage.

## No Pass-Through Helpers

* Do not create one-line wrapper/helper functions that only forward arguments and return another function call.
* If a signature changes, update all call sites and tests directly instead of adding compatibility wrappers.
* Allowed exception: explicit user request for backward compatibility (must be documented in the change note with the dependent caller).

## Function name

* Keep existing function names unless asked to change them explicitly.
* For new function names use the naming-rules skill for naming rules.

## Backward compatibility

* Do not maintain backward compatibility unless asked for.

## Function parameter rules

* Don't use compatibility signature tricks, stop and ask for guidance if an obvious solution is available. For example, if an function call adds a new parameter and you have it available then simply add the parameter to the function call and update all call sites instead of adding a compatibility shim that checks for the presence of the parameter and provides a fallback value. Update the unit tests to reflect the new parameter and its expected value instead of adding a guard for the new parameter in the code to satisfy existing unit tests.

## Handling failures and errors

### Exceptions

- Exceptions should be properly handled and logged. If an exception is not expected then it should be logged and raised to lead to the end of execution or handled by the parent caller
- Add specific exception handling for expected error cases (e.g., validation errors, known failure modes) with clear logging and recovery steps if applicable.
- There should be no silent failures. If an error occurs, it should be logged with sufficient context and either handled or raised to prevent unnoticed issues.
- Do not use # noqa: BLE001 to ignore exception handling issues. Address them directly by adding appropriate try/except blocks or ensuring exceptions are properly propagated.
- If a critical error occurs, throw an exception. If it is specific to the application create a custom exception to allow identification to allow it to be handled by the proper caller in the tree. For example, if a dependency requires reading a file. But that is read several calls deep into the exception, rather then passing a True / False value or another value up the call stack. raise an error.

### Fail backs

- Only create fail backs if explicitly asked for. For example if a module is missing and the user asks to create a fallback implementation or type for it, then create it. Otherwise report the missing module and let the user decide how to proceed.
- Only create fail backs if explicitly asked for is any case.

## Examples

### Good function examples

```python
def update_task(job_id: str, status: str) -> None:
  if not status:
    raise ValueError("status is required")
  task = task_repo.get(job_id)
  task.status = status
  task_repo.save(task)
```

Why this is good:

* Parameters are all used.
* Function name is concise and action-oriented.
* Logic is direct with no compatibility shim.

```python
def batch(records: list[Record]) -> int:
  total = 0
  for record in records:
    if not record.is_valid:
      continue
    total += 1
  return total
```

Why this is good:

* No unnecessary wrappers.
* No unnecessary copying of `records`.
* Clear and minimal flow.

### Bad function examples and what to do instead

```python
def update_task(job_id: str, status: str, legacy_mode: bool) -> None:
  del legacy_mode
  task = task_repo.get(job_id)
  task.status = status
  task_repo.save(task)
```

What is wrong:

* Has a parameter and deletes it immediately.
* The parameter is unneeded.

What to do:

* Remove the unneeded parameter from the function signature.
* Remove the same parameter from all calling sites and tests.

```python
def run(records: list[Record], trace_id: str) -> int:
  total = 0
  for record in records:
    if record.is_valid:
      total += 1
  return total
```

What is wrong:

* `trace_id` is never used.

What to do:

* Remove `trace_id` from the function signature.
* Remove `trace_id` from all call sites instead of keeping a compatibility parameter.

```python
def process(records: list[Record]) -> int:
  return process_records(records)
```

What is wrong:

* One-line pass-through helper.

What to do:

* Remove the helper.
* Call `process_records` directly from existing callers.

## Breaking large function bodies into pieces

When a function body is large, break it into smaller pieces with clear responsibilities.

Signals that a function should be split:

1. An individual chunk is 5 to 30 lines and can be unit tested separately.
1. Large bodies exist inside `if`, `while`, `for`, or other flow control blocks. Keep flow control in one place and move actions into focused functions.

### Bad example

```python
def run(records: list[Record]) -> dict[str, int]:
  total = 0
  failed = 0
  for record in records:
    if not record.id:
      failed += 1
      continue
    if record.status not in {"new", "retry"}:
      failed += 1
      continue
    payload = {
      "id": record.id,
      "name": record.name.strip().lower(),
      "score": normalize_score(record.score),
      "tags": [tag.strip().lower() for tag in record.tags if tag.strip()],
    }
    result = api_client.submit(payload)
    if result.ok:
      total += 1
    else:
      failed += 1
  return {"total": total, "failed": failed}
```

What is wrong:

* Validation, payload building, submission, and counting are blended in one loop.
* The loop body has testable chunks that should be split into separate functions.

### Better example

```python
def run(records: list[Record]) -> dict[str, int]:
  total = 0
  failed = 0
  for record in records:
    if not is_valid_record(record):
      failed += 1
      continue
    payload = build_payload(record)
    if submit_payload(payload):
      total += 1
      continue
    failed += 1
  return {"total": total, "failed": failed}


def is_valid_record(record: Record) -> bool:
  if not record.id:
    return False
  if record.status not in {"new", "retry"}:
    return False
  return True


def build_payload(record: Record) -> dict[str, object]:
  return {
    "id": record.id,
    "name": record.name.strip().lower(),
    "score": normalize_score(record.score),
    "tags": [tag.strip().lower() for tag in record.tags if tag.strip()],
  }


def submit_payload(payload: dict[str, object]) -> bool:
  result = api_client.submit(payload)
  return result.ok
```

Why this is better:

* Flow control remains in `run`.
* Action chunks are separated and unit-testable.
* Each function has a single responsibility.

## When to create a new file for a function

Inline small utilities; only create a new file when more than one module needs it. Never name a file after a single micro-feature — name modules by category, and let the second real consumer trigger extraction.

## Rule: No External State Mirroring or Logic Duplication

Do not recreate, mirror, or duplicate a class's internal state, data structures, or formatting logic outside of the class itself. If global or cross-instance aggregation is needed, use one of these approved patterns:

1. **Class-level state**: Add the shared state as a class attribute with its own methods.
2. **Composition**: Create a wrapper or aggregator class that holds instances of the target class and delegates to their public API.
3. **Shared instance**: Use a single shared instance that all callers reference.

### Forbidden

- Module-level dicts or variables that replicate a class's internal structure.
- Functions that reach into another class's returned data and manually reimplement its behavior.
- Parallel implementations of formatting, reporting, or serialization that duplicate a class's existing methods.
- Any code that would silently break if the target class renamed a key, changed a value type, or altered its internal structure.

### What to Consider as Alternatives

When cross-instance or global aggregation is needed, evaluate these patterns before writing code:

- **Does the class already provide a public API for aggregation?** If so, use it. Pass results from `get_stats()` or similar methods back into the class's own `report()` method. Do not reimplement formatting or structure traversal.
- **Can a factory function return a shared instance?** A single function that returns a cached or module-scoped instance ensures all callers use the same object without exposing internals.
- **Is the aggregation concern better owned by the class itself?** If every caller needs the same aggregated view, the class should expose it as a class method or property.
- **Would composition be cleaner than patching?** An aggregator class that holds references to target instances and delegates to their public methods keeps coordination logic separate from internal structure.

### Rationale

External mirroring creates tight coupling to internal implementation details. Changes to the source class will silently corrupt or break the mirrored code, producing bugs that are difficult to trace and test.
