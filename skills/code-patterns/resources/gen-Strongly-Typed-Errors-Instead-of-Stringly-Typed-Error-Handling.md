# Coding Pattern Rule: Strongly Typed Errors Instead of Stringly Typed Error Handling

## Context

When program flow depends on an error condition, the error must be represented by a strongly typed structure with a stable machine-readable code and a separate human-readable message.

Human-readable messages are for logs, debugging, and users. They are not a safe control-flow contract. If behavior depends on matching message text exactly, or on finding a substring inside the message, a wording change can silently break the logic.

This applies to exceptions, validation failures, retry classification, API errors, worker outcomes, and any other path where code branches based on why an operation failed.

## Pattern to Use

Represent each error with:

- a stable snake_case error code;
- a human-readable message string;
- a strongly typed error shape or exception type that carries both values.

Branch on the typed code or the specific error type, not on the message text.

Prefer:

```python
from enum import StrEnum


class ErrorCode(StrEnum):
    RATE_LIMITED = "rate_limited"
    RECORD_NOT_FOUND = "record_not_found"


class AppError(Exception):
    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def classify_error(error: AppError) -> str:
    if error.code == ErrorCode.RATE_LIMITED:
        return "retry"
    if error.code == ErrorCode.RECORD_NOT_FOUND:
        return "stop"
    raise error
```

The message may change from:

```text
"Rate limit exceeded"
```

to:

```text
"Too many requests from upstream service"
```

without changing the control flow, because the code remains `rate_limited`.

If the error crosses a boundary, preserve the same structure:

```ts
type AppErrorCode = 'rate_limited' | 'record_not_found';

type AppError = {
  code: AppErrorCode;
  message: string;
};

if (result.error?.code === 'rate_limited') {
  scheduleRetry();
}
```

## Pattern Not to Use

Do not make control flow depend on the exact text of an exception or error message.

Rejected pattern: exact string equality

```python
try:
    await client.send_request()
except Exception as exc:
    if str(exc) == "Rate limit exceeded":
        return "retry"
    raise
```

Rejected pattern: substring search

```python
try:
    await client.send_request()
except Exception as exc:
    if "rate limit" in str(exc).lower():
        return "retry"
    raise
```

Rejected TypeScript examples:

```ts
if (error.message === 'Record not found') {
  return;
}

if (error.message.includes('timeout')) {
  retryRequest();
}
```

These patterns are brittle because:

- message wording changes break behavior;
- punctuation, casing, and localization can change matches;
- unrelated errors can accidentally match the same substring;
- reviewers cannot tell whether the message text is a stable contract or incidental copy.

## Review and testing guidance

When reviewing or testing error handling:

1. Verify that each controlled error path has a stable snake_case code.
1. Verify that program flow branches on `error.code` or a specific error type.
1. Reject logic that uses `str(error)`, `error.message`, equality against message text, or substring checks to decide behavior.
1. Prefer tests that assert the error code.

It is acceptable to test message text separately when validating user-facing copy, logs, or API response text, but those tests must not define program control flow.

## Rule

Errors used for application behavior must be strongly typed.

Each error must have a stable snake_case code and a human-readable message.

Control flow must depend on the code or error type, never on exact message equality or substring matching against the message text.