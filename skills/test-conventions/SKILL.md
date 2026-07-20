---
name: test-conventions
description: Govern naming, file placement, directory structure, plan or rule traceability, and file-size limits for automated tests. Use when creating, moving, splitting, organizing, or reviewing any automated test suite, including unit, integration, component, contract, end-to-end, smoke, and regression tests in pytest, Jest, Playwright, or other test frameworks.
---

# Test Conventions

Apply these conventions to every automated test type and framework.

## Establish the governing file

1. Identify the plan or rule file that requires or defines the tests.
1. Use its repository-relative path as the canonical organizing path.
1. Require a canonical plan or rule file before adding tests. If none is identifiable, ask which file governs the tests.
1. Record the exact repository-relative path in every test file.

## Derive the test location and filename

1. Put all automated tests beneath a dedicated top-level `tests/` directory. Never place tests inside `src/`, `app/`, `lib/`, or another application source tree.
1. Transform `plans/<directories>/<governing-file>` into `tests/<directories>/<test-file>`.
1. Replace the leading `plans/` directory with `tests/` and preserve every directory component that follows it. Treat `rules/`, `api/`, `unit/`, `integration/`, and similar directories as meaningful parts of the mirrored path.
1. Convert the governing filename to the framework's test filename pattern:
   - pytest: `test_<governing-stem>.py`
   - Jest: `<governing-stem>.test.ts`, `<governing-stem>.test.tsx`, or the project's matching JavaScript extension
   - Playwright: `<governing-stem>.spec.ts` or the project's matching JavaScript extension
1. Normalize the filename stem for the target language: use snake case for Python and the repository's established JavaScript or TypeScript filename style for Jest and Playwright.

Apply the transformation as follows:

- `plans/rules/onboarding/question-filter.md` becomes `tests/rules/onboarding/test_question_filter.py` for pytest.
- `plans/api/onboarding/question-filter.md` becomes `tests/api/onboarding/test_question_filter.py` for pytest.
- `plans/rules/onboarding/question-filter.md` becomes `tests/rules/onboarding/question-filter.test.ts` for Jest.
- `plans/e2e/onboarding/question-filter.md` becomes `tests/e2e/onboarding/question-filter.spec.ts` for Playwright.

Do not introduce a directory into the test path unless it exists after `plans/` in the governing path. For example, `tests/rules/` comes from `plans/rules/`, while `tests/api/` comes from `plans/api/`.

## Keep tests separate from source code

Use this separation:

```text
src/app/app_class.py
tests/app/test_app_class.py
```

Do not use this intermixing:

```text
src/app/app_class.py
src/app/tests/test_app_class.py
```

Configure the framework's discovery paths when necessary so the dedicated `tests/` tree is authoritative.

## Reference the governing file at the head

Place a comment before imports at the head of every test file. Use the exact repository-relative path and a stable label.

Python:

```python
# Governing plan: plans/app/app_class.md

import pytest
```

TypeScript or JavaScript:

```typescript
// Governing rule: plans/rules/app/app-class.md

import { test, expect } from "@playwright/test";
```

Keep a required shebang, encoding declaration, copyright notice, or license header first; place the governing-file comment immediately after it.

When a test file covers a specific section, append a stable section identifier:

```python
# Governing plan: plans/billing/invoice.md#overdue-invoices
```

## Name tests by observable behavior

- Name each test after the condition or action and its expected observable result.
- Keep names specific enough that a failure identifies the broken contract without reading the test body.
- Avoid names based only on issue numbers, plan step numbers, `works`, `success`, or `test1`.
- Use the terminology from the governing plan or rule.

pytest examples:

```python
def test_expired_token_rejects_login() -> None:
    ...


def test_valid_token_returns_authenticated_user() -> None:
    ...
```

Jest examples:

```typescript
describe("authenticateUser", () => {
  test("rejects login when the token is expired", () => {
    // ...
  });

  test("returns the authenticated user when the token is valid", () => {
    // ...
  });
});
```

Playwright examples:

```typescript
test("shows an expiration message when the session has expired", async ({ page }) => {
  // ...
});
```

## Enforce the 600-line limit

1. Estimate the completed test file size before adding a large set of tests.
1. Keep every test file at or below 600 lines.
1. Split the tests before implementation when the planned cases would make a file exceed 600 lines.
1. Split by coherent behavior, feature area, scenario, or plan section. Give each split file a descriptive suffix and retain the governing filename stem.
1. Extract repeated setup, builders, fixtures, and assertions into helper or fixture files when this makes each test file easier to navigate.
1. Keep assertions that define a scenario's intent in the test file. Do not hide the behavior being verified behind a generic helper.
1. Keep helper files alongside the related tests in the mirrored directory. Prefix Python support modules with `helpers_` and keep every support filename outside the framework's test discovery patterns.
1. Apply the same governing-file comment to every split test file. Add a section anchor when it clarifies the split.

Example split for `plans/api/onboarding/question-filter.md`:

```text
tests/api/onboarding/helpers_question_filter.py
tests/api/onboarding/test_helpers_question_filter.py
tests/api/onboarding/test_question_filter.py
tests/api/onboarding/test_question_filter_location.py
tests/api/onboarding/test_question_filter_selector.py
```

Keep the primary cases in `test_question_filter.py`. Move cohesive location and selector cases into files that retain the `question_filter` governing stem. Put shared test support in `helpers_question_filter.py`, outside pytest's test discovery pattern, and test that support explicitly in `test_helpers_question_filter.py`. Begin every test file in the group with a reference to `plans/api/onboarding/question-filter.md`.

## Framework directory examples

### Python with pytest

```text
plans/
└── api/
    └── app/
        ├── app_class.md
        └── authentication.md
src/
└── app/
    ├── app_class.py
    └── authentication.py
tests/
└── api/
    └── app/
        ├── test_app_class.py
        ├── test_authentication_login.py
        ├── test_authentication_tokens.py
        ├── conftest.py
        └── helpers_authentication.py
```

The two authentication files are a behavior-based split of `plans/api/app/authentication.md`; both begin with a reference to that plan.

### Node or TypeScript with Jest

```text
plans/
└── rules/
    └── app/
        ├── app-class.md
        └── authentication.md
src/
└── app/
    ├── app-class.ts
    └── authentication.ts
tests/
└── rules/
    └── app/
        ├── app-class.test.ts
        ├── authentication-login.test.ts
        ├── authentication-tokens.test.ts
        └── helpers-authentication.ts
```

### Node or TypeScript with Playwright

```text
plans/
└── e2e/
    └── checkout/
        ├── payment.md
        └── receipt.md
src/
└── checkout/
    ├── payment.ts
    └── receipt.ts
tests/
└── e2e/
    └── checkout/
        ├── payment-card.spec.ts
        ├── payment-declined.spec.ts
        ├── receipt.spec.ts
        ├── fixtures-checkout.ts
        └── helpers-checkout-page.ts
```

The Playwright configuration must point test discovery at `tests/e2e`.

## Review checklist

- Confirm every test has a governing plan or rule file.
- Confirm every test file begins with the governing-file comment.
- Confirm the test path replaces leading `plans/` with `tests/` and preserves every following directory.
- Confirm all tests live under the dedicated top-level `tests/` tree.
- Confirm filenames match the framework's discovery pattern.
- Confirm test names state observable behavior and outcome.
- Confirm no test file exceeds 600 lines.
- Confirm planned oversized files are split by behavior or reduced with focused helpers.
- Confirm helpers cannot be collected as tests.
