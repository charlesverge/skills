---
name: validate-user-change-request
description: Validate user change requests and provide guidance on whether they can be fulfilled without significant code changes.
---

# Validate User Change Request

The goal of this skill is a gate keeper for instructions to prevent requests that would require significant code changes to fulfill from being actioned without explicit approval. For each user change request, analyze the requested change and determine if it can be fulfilled with the current codebase or if it would require significant code changes. If it cannot be fulfilled, explain why and provide alternative solutions or workarounds that could achieve a similar outcome without requiring major modifications to the existing code.

Example scenarios include:
- A user requests a change that would require refactor of the architecture or data model.
- A user requests a change that would require changing more then three files in the codebase.
- A user requests a pattern to be applied that is not supported by the current codebase without changing more then three files or 100 lines or more of code.

In these cases, stop. Generate a summary of what the change would require to get confirmation that the user should proceed with the change.

An example of this is shown in `resources/example-unit-test.md` where the user requests a unit test pattern to be applied to an object that does not support that pattern without significant code changes. The assistant explains this and offers alternative solutions.
