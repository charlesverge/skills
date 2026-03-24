---
name: naming-rules
description: Apply concise naming rules for variables, properties, fields, and functions while preserving existing names unless explicitly requested. Use when adding new identifiers during code changes or reviews and when enforcing boolean/action function naming patterns.
---

# Naming Rules

## Variable, property, field naming

- Keep existing variables
- New variables should be concise, ideally limited to one or two words.
- For local scope inside a function use generic names if possible. ie result, result_counter, total, item, record, entry.

## Function naming

- Keep existing function names unless explicitly asked to rename.
- New function names must prioritize clarity and explicit meaning.
- Prefer clear patterns:
  - Boolean functions: is_*, has_*, can_*, should_*
  - Action functions: create_*, update_*, delete_*, defer_*, block_*, enqueue_*
- Target length is 1-3 words.
- If a new function name needs more than 3 words:
  - Stop implementation for that naming decision.
  - Perform a design check:
    1. Should the function be split into smaller functions?
    2. Should the operation move to another class/module?
  - Ask the user for clarification before proceeding.
- Do not over-shorten names when meaning is lost (for example, prefer is_blocked over blocked).