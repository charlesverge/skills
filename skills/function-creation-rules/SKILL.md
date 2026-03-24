---
name: function-creation-rules
description: Enforce function creation and reuse rules extracted from agents.md without line modifications.
---

# Function Creation Rules

## Extracted function-related rules

- Do not define nested functions inside other functions or methods unless explicitly asked for.
- Before creating custom code, check whether a module already provides the requested functionality. If a module is close but not exact, outline the differences and ask whether the user wants to adjust the specifications.
- nonlocal is not allowed. Use a class.

## Function creation

- If a function is in another module do not copy it, import and use it. If you need the function to modified, request modification approval.
- Do not create a duplicate function, reuse existing functions and utilities. If there is not an exact function that can be reused, check if there is a function that can be modified to satisfy the requirements without breaking existing functionality. If there is a function that can be modified, ask the user if they want to modify the existing function or create a new one.
- When a shared utility is the declared source of truth (for example `recruiter_common.urls.url_candidates`), do not implement endpoint-local fallback/canonicalization logic for the same concern.
- If required behavior is missing from the shared utility, report it explicitly as a shared-utility defect with concrete input/output examples and stop local workaround changes unless explicitly approved.
- Don't create a fall back unless explicitly asked for
- Avoid the use of built in functions like attrib, hasattr for classes which can accessed like ClassName.property_name
- If a reference is already a str don't add str() to it.
- Avoid unnecessary copying of input data structures (lists, dicts, sets, tuples, dataclasses, models, arrays, payload objects, and nested structures). Reuse existing references and process data in place or as a stream unless duplication is required for correctness (immutability boundaries, mutation safety, ordering guarantees, concurrency isolation, or explicit API contract).
- Keep multi-step processes in distinct phases with explicit boundaries and handoff data (for example: collect/validate, transform/enrich, persist/output). Do not blend unrelated phases in one loop or helper unless explicitly required.
- Do not introduce phase-boundary carrier types (for example dedicated dataclasses, models, or wrappers created only to move data between internal phases) unless explicitly asked by the user.
- Prefer passing existing domain models or standard built-in containers across phase boundaries. If stricter typing is needed, update function signatures/call sites directly instead of creating a carrier type.
- Prefer streaming data from databases/cursors and process records incrementally; avoid materializing full result sets in memory unless required by correctness or an explicit API contract.
- Do not repeat validation/error checks for invariants already guaranteed by an earlier phase in the same execution flow. Downstream phases should rely on established contracts and only validate new assumptions introduced at that phase.

## No Pass-Through Helpers

- Do not create one-line wrapper/helper functions that only forward arguments and return another function call.
- If a signature changes, update all call sites and tests directly instead of adding compatibility wrappers.
- Allowed exception: explicit user request for backward compatibility (must be documented in the change note with the dependent caller).

## Function name

- Keep existing function names unless asked to change them explicitly.
- For new function names use the naming-rules skill for naming rules.

## Backward compatibility

- Do not maintain backward compatibility unless asked for.

## Function parameter rules

- Don't use compatibility signature tricks, stop and ask for guidance if an obvious solution is available. For example, if an function call adds a new parameter and you have it available then simply add the parameter to the function call and update all call sites instead of adding a compatibility shim that checks for the presence of the parameter and provides a fallback value. Update the unit tests to reflect the new parameter and its expected value instead of adding a guard for the new parameter in the code to satisfy existing unit tests.
