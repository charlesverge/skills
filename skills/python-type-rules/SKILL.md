---
name: python-type-rules
description: Enforce strict Python typing when creating or modifying types for variables, function parameters, function return values, classes, dataclasses, Pydantic models, TypedDicts, protocols, aliases, and structured objects. Use whenever creating, changing, fixing, reviewing, or type-checking Python annotations or object shapes, especially when resolving typing errors without suppressions, fallbacks, Any, object, loose unions, casts, or runtime attribute workarounds.
---


# When to use this skill

When modifying or creating a new type for a variable or a function.

## Core Rule

Use strict, explicit Python types. When a value has structure, define that structure with a real typed class, dataclass, Pydantic model, TypedDict, or existing domain type instead of using loose containers or escape hatches.

If a strict type cannot be written without weakening the code, stop and ask the user how to proceed.

Do not attempt to fix the type problems fast, focus on fixing them right. If the fix is not obvious, stop and ask for direction on how to proceed.

## Required Practices

- Define the structure of created objects.
- Prefer one precise parameter type over parameters that accept multiple unrelated types.
- For return values, avoid tuples when the values have meaning; define a named class with typed properties instead.
- Fix typing issues by correcting annotations, constructors, imports, stubs, or helper signatures.
- Keep behavior and control flow unchanged when the task is a typing fix.
- Verify the edited file locally with the available type checker or test command when practical.
- Keep changes minimal and targeted to the typing problem.

# Creating and modifying types

- Use strict typing, when creating an object it's structure should be defined. Do not use types like any, object to allow any structure.
- For return values avoid tuples and use a define a class with properties instead

## Stubs and type definitions

- Do not create .pyi stub files unless explicitly asked for.
- Do not create Protocols or type aliases to work around missing types in third-party libraries.
- For third party libraries if there stubs are not installed the locate them and install them. Search the web for existing stubs, stop and ask for approval to install them, if they do not exist report the missing types and ask for direction on how to proceed.

## Rules for type fixes and adjustments

- Do not use the type Any, object, if there is no other solution then stop and request user input on how to proceed.
- Prefer strict typing, avoid creating parameters that can take multiple types.
- Do not attempt to get around typing, ie for example if a value is required, don't use a fail back value which is also not allowed.
- Do not use TYPE_CHECKING imports
- Do not use fallback TypedDicts (no if TYPE_CHECKING: ... else: class X(TypedDict, ...) pattern).
- Do not use # type: ignore unless explicitly asked for.
- Do not use # noqa:
- Do not add or preserve # type: ignore lines when modifying code.
- If an existing pattern uses # type: ignore, refactor the code to satisfy typing instead of copying the pattern.
- When a type mismatch appears, prefer adjusting types, constructors, or helper utilities rather than suppressing the error.
- Denied getattr
- Denied setattr
- paper over missing attributes with a default/fallback. Ensure the attribute is correctly typed and validated via proper type annotations and imports.
- Do not use try/except AttributeError or other runtime workarounds to bypass typing issues. Fix the types directly (e.g., correct type annotations, constructors, or imports) so the attribute access is properly typed.
- When fixing typing issues, avoid introducing new typing errors or runtime side effects; verify types locally in the edited file and keep changes minimal and targeted.
- Do not add runtime guards or exception handling solely to satisfy typing. Fix types directly (or use narrow, accurate casts only when third-party stubs are incorrect).
- Do not use typing.cast to resolve typing issues unless explicitly asked for. Fix the types directly instead.
- Do not introduce local protocol/alias wrappers (e.g., COUNTRIES: CountriesLike) to mask third-party typing gaps. Fix types directly or update stubs when needed.
- Do not use Any (including typing.Any, dict[str, Any], or similar) to bypass typing. Define concrete types instead.
- Do not use assert isinstance(...) solely to satisfy typing outside of unit tests. In unit tests, assert isinstance(...) is allowed.
- Do not use NoReturn/Never to silence typing issues in reachable code.
- Do not use from typing import * or re-exports to hide typing gaps.
- Do not use type checker suppression comments (e.g., # pyright: ignore, # pyright: report...=none, # type: ignore[code]).
- Do not re-export symbols; import from the correct module instead.
- Never use the if TYPE_CHECKING: ... else: ... pattern for any module.
- Do not create pyi files unless asked for, report back the type errors and let the user decide if they can be resolved in the source module or a pyi file is needed.
- Don't down grade types for example changing a specific set of types to a general type, if you think this should be done. Stop and explain why it is required. For example, don't change Command[Literal["__end__"]] | Command[Literal["search"]] | Command[Literal["logout"]] to Command
- kwargs is denied and use of patterns like **fields: object,
you are not allowed to use this conditional logic. agent_id=agent_id.value if isinstance(agent_id, LlmBatchAgentId) else agent_id, you should now what type it is and what type is needed. This parameter is also denied for a function parameter which triggers these usless if else conditions agent_id: LlmBatchAgentId | str,
- don't make typing weaker
- when fixing typing issues, don't alter the existing logic or flow of the code, only make the necessary adjustments to satisfy the type checker without changing the behavior of the code.