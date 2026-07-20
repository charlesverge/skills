---
name: test-conventions
description: Govern naming, file placement, directory structure, plan or rule traceability, and file-size limits for automated tests. Use when creating, moving, splitting, organizing, or reviewing any automated test suite, including unit, integration, component, contract, end-to-end, smoke, and regression tests in pytest, Jest, Playwright, or other test frameworks.
---

# Test Conventions

Apply these conventions to every automated test type and framework.

## Use consistent path terms

- `{plan_dir}`: the directory directly beneath `plans/`, such as `api` or `e2e`.
- `{plan_file}`: the plan filename without its `.md` extension.
- `{rule_area}`: the directory beneath `plans/rules/` that owns a set of rules.
- `{rule_group}`: the rule filename without its `.md` extension.

Treat these as descriptive placeholders. Replace them with the exact values from the plan or rule; never use the placeholder text in a completed test path.

## Establish the plan or rule file

1. Identify the plan or rule file that requires or defines the tests.
1. Use its repository-relative path as the test organizing path.
1. Require a canonical plan or rule file before adding tests. If none is identifiable, ask which file governs the tests.
1. Record the exact repository-relative path in every test file.

## Transform plan paths into test paths

Put every automated test beneath the top-level `tests/` directory. Never place tests inside `src/`, `app/`, `lib/`, or another application source tree.

For a plan at:

```text
plans/{plan_dir}/{plan_file}.md
```

discard the `.md` extension and transform it as follows:

- pytest: `tests/{plan_dir}/test_{plan_file}.py`
- Jest: `tests/{plan_dir}/{plan_file}.test.ts`, `{plan_file}.test.tsx`, or the project's matching JavaScript extension
- Playwright: `tests/{plan_dir}/{plan_file}.spec.ts` or the project's matching JavaScript extension

For a rule at:

```text
plans/rules/{rule_area}/{rule_group}.md
```

discard the `.md` extension and transform it as follows:

- pytest: `tests/rules/{rule_area}/test_{rule_group}.py`
- Jest: `tests/rules/{rule_area}/{rule_group}.test.ts`, `{rule_group}.test.tsx`, or the project's matching JavaScript extension
- Playwright: `tests/rules/{rule_area}/{rule_group}.spec.ts` or the project's matching JavaScript extension

Preserve `{plan_dir}` and `{rule_area}` exactly. Preserve the JavaScript or TypeScript stem style. Normalize hyphens in `{plan_file}` or `{rule_group}` to underscores for Python filenames.

Do not introduce a directory into the test path that is absent from the plan or rule path. The `rules/` directory appears under `tests/` only when the rule file is under `plans/rules/`.

## Keep tests separate from source code

Use this separation:

```text
src/{source_dir}/{source_file}.py
tests/{plan_dir}/test_{plan_file}.py
```

Do not use this intermixing:

```text
src/{source_dir}/{source_file}.py
src/{source_dir}/tests/test_{plan_file}.py
```

Configure the framework's discovery path so the dedicated `tests/` tree is authoritative.

## Reference the plan or rule file at the head

Place a comment before imports at the head of every test file. Use the exact repository-relative path.

Python plan test:

```python
# Plan: plans/{plan_dir}/{plan_file}.md

import pytest
```

TypeScript or JavaScript rule test:

```typescript
// Rule: plans/rules/{rule_area}/{rule_group}.md

import { test, expect } from "@playwright/test";
```

Keep a required shebang, encoding declaration, copyright notice, or license header first; place the plan or rule comment immediately after it.

When a test file covers a specific section, append its stable section identifier:

```python
# Plan: plans/{plan_dir}/{plan_file}.md#section-identifier
```

## Name tests by observable behavior

- Name each test after the condition or action and its expected observable result.
- Keep names specific enough that a failure identifies the broken contract without reading the test body.
- Avoid names based only on issue numbers, plan step numbers, `works`, `success`, or `test1`.
- Use the terminology from the plan or rule.

pytest:

```python
def test_condition_returns_expected_result() -> None:
    ...


def test_invalid_input_returns_validation_error() -> None:
    ...
```

Jest:

```typescript
describe("featureFunction", () => {
  test("returns the expected result when the condition is met", () => {
    // ...
  });

  test("returns a validation error when the input is invalid", () => {
    // ...
  });
});
```

Playwright:

```typescript
test("shows the expected result when the condition is met", async ({ page }) => {
  // ...
});
```

## Enforce the 600-line limit

1. Estimate the completed test file size before adding a large set of tests.
1. Keep every test file at or below 600 lines.
1. Split the tests before implementation when the planned cases would make a file exceed 600 lines.
1. Split by coherent behavior, feature area, scenario, or plan section. Retain `{plan_file}` or `{rule_group}` in every split filename.
1. Extract repeated setup, builders, fixtures, and assertions into helper or fixture files when this makes each test file easier to navigate.
1. Keep assertions that define a scenario's intent in the test file. Do not hide the behavior being verified behind a generic helper.
1. Keep helper files alongside the related tests. Prefix Python support modules with `helpers_` and keep support filenames outside the framework's test discovery patterns.
1. Apply the same plan or rule comment to every split test file. Add a section anchor when it clarifies the split.

Generic pytest split for `plans/{plan_dir}/{plan_file}.md`:

```text
tests/{plan_dir}/helpers_{plan_file}.py
tests/{plan_dir}/test_helpers_{plan_file}.py
tests/{plan_dir}/test_{plan_file}.py
tests/{plan_dir}/test_{plan_file}_condition.py
tests/{plan_dir}/test_{plan_file}_result.py
```

Keep primary cases in `test_{plan_file}.py`. Put shared support in `helpers_{plan_file}.py`, and test that support in `test_helpers_{plan_file}.py`. Use behavior suffixes such as `_condition` and `_result` for coherent splits. Normalize `{plan_file}` to snake case in every Python filename.

## Framework structure examples

### Python with pytest

```text
plans/{plan_dir}/{plan_file}.md
src/{source_dir}/{source_file}.py
tests/{plan_dir}/helpers_{plan_file}.py
tests/{plan_dir}/test_helpers_{plan_file}.py
tests/{plan_dir}/test_{plan_file}.py
tests/{plan_dir}/test_{plan_file}_condition.py
tests/{plan_dir}/test_{plan_file}_result.py
```

### Node or TypeScript with Jest

```text
plans/rules/{rule_area}/{rule_group}.md
src/{source_dir}/{source_file}.ts
tests/rules/{rule_area}/helpers-{rule_group}.ts
tests/rules/{rule_area}/{rule_group}.test.ts
tests/rules/{rule_area}/{rule_group}-condition.test.ts
tests/rules/{rule_area}/{rule_group}-result.test.ts
```

### Node or TypeScript with Playwright

```text
plans/{plan_dir}/{plan_file}.md
src/{source_dir}/{source_file}.ts
tests/{plan_dir}/fixtures-{plan_file}.ts
tests/{plan_dir}/helpers-{plan_file}-page.ts
tests/{plan_dir}/{plan_file}.spec.ts
tests/{plan_dir}/{plan_file}-condition.spec.ts
tests/{plan_dir}/{plan_file}-result.spec.ts
```

Configure Playwright test discovery to use the applicable `tests/{plan_dir}` directory.

## Review checklist

- Confirm every test has a plan or rule file.
- Confirm every test file begins with the exact plan or rule comment.
- Confirm plan tests map `plans/{plan_dir}/{plan_file}.md` to the framework pattern beneath `tests/{plan_dir}/`.
- Confirm rule tests map `plans/rules/{rule_area}/{rule_group}.md` to the framework pattern beneath `tests/rules/{rule_area}/`.
- Confirm `.md` is discarded before the framework filename pattern is applied.
- Confirm all tests live under the dedicated top-level `tests/` tree.
- Confirm test names state observable behavior and outcome.
- Confirm no test file exceeds 600 lines.
- Confirm planned oversized files are split by behavior or reduced with focused helpers.
- Confirm helpers cannot be collected as tests.
