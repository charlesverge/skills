# Skills Catalog

## function-creation-rules

- `id`: `function-creation-rules`
- `path`: `skills/function-creation-rules`
- `category`: `engineering`
- `name`: `function-creation-rules`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-24`

### Description

Enforce function creation and reuse rules extracted from agents.md without line modifications.

### Skill File

- [skills/function-creation-rules/SKILL.md](skills/function-creation-rules/SKILL.md)

## qdrant-database-operations

- `id`: `qdrant-database-operations`
- `path`: `skills/qdrant-database-operations`
- `category`: `engineering`
- `name`: `qdrant-database-operations`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-24`

### Description

Use Qdrant Python client patterns for common collection operations including insert, upsert, delete, and retrieval with clear payload type expectations.

### Skill File

- [skills/qdrant-database-operations/SKILL.md](skills/qdrant-database-operations/SKILL.md)

## code-cleanup-rules

- `id`: `code-cleanup-rules`
- `path`: `skills/code-cleanup-rules`
- `category`: `engineering`
- `name`: `code-cleanup-rules`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-20`

### Description

Apply cleanup-focused refactor rules for phased invalid/orphan deletion logic, strict typing at API boundaries, linear validation flow, and minimal operational wrappers. Use when implementing or reviewing cleanup-style functions.

### Skill File

- [skills/code-cleanup-rules/SKILL.md](skills/code-cleanup-rules/SKILL.md)

## needless-helper-decisions

- `id`: `needless-helper-decisions`
- `path`: `skills/needless-helper-decisions`
- `category`: `engineering`
- `name`: `needless-helper-decisions`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-19`

### Description

Use this rubric and example set for future needless helper decisions. Use when reviewing or refactoring helper methods to decide whether to keep phase-boundary logic helpers or inline thin pass-through wrappers while preserving behavior, side effects, exception semantics, and logging.

### Skill File

- [skills/needless-helper-decisions/SKILL.md](skills/needless-helper-decisions/SKILL.md)

## single-read-decision-update

- `id`: `single-read-decision-update`
- `path`: `skills/single-read-decision-update`
- `category`: `engineering`
- `name`: `single-read-decision-update`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-19`

### Description

Enforce a single-read decision update pattern for repository/service methods that read current entity state, compute outcomes from current state plus new input, persist one mutation, and return a `DecisionResult` used by callers without same-entity re-reads.

### Skill File

- [skills/single-read-decision-update/SKILL.md](skills/single-read-decision-update/SKILL.md)

## naming-rules

- `id`: `naming-rules`
- `path`: `skills/naming-rules`
- `category`: `engineering`
- `name`: `naming-rules`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-19`

### Description

Apply concise naming rules for variables, properties, fields, and functions while preserving existing names unless explicitly requested.

### Skill File

- [skills/naming-rules/SKILL.md](skills/naming-rules/SKILL.md)

## code-patterns

- `id`: `code-patterns`
- `path`: `skills/code-patterns`
- `category`: `engineering`
- `name`: `code-patterns`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-19`

### Description

Enforce Python and Beanie code patterns that avoid unsafe defaults, inline imports, unnecessary comments/checks, manual model wiring, and non-streaming cursor usage. Use when writing or reviewing repository/service code for consistency and performance.

### Skill File

- [skills/code-patterns/SKILL.md](skills/code-patterns/SKILL.md)

## record-state-handling

- `id`: `record-state-handling`
- `path`: `skills/record-state-handling`
- `category`: `engineering`
- `name`: `record-state-handling`
- `risk`: `safe`
- `source`: `personal`
- `date_added`: `2026-03-24`

### Description

Enforce record-state handling patterns that separate non-blocking invalid state from blocking invalid state, prohibit implicit repair unless explicitly authorized, and require functions to avoid local skip behavior that preserves stale retry-selection state. Use when writing or reviewing record-processing code that validates state, updates records, raises structured state exceptions, and leaves retry or terminal disposition to the caller.

### Skill File

* [skills/record-state-handling/SKILL.md](skills/record-state-handling/SKILL.md)
