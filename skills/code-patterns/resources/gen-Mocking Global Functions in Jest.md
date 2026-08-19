# Coding Pattern: Mocking Global Functions in Jest

## Purpose

Use this pattern when a Jest test needs to replace or intercept an existing global function such as `fetch`.

The test must not directly mutate `global`, `globalThis`, or another process-lifetime singleton.

## Do Not Use

Do not assign directly to properties of `global` or `globalThis`.

```typescript
global.fetch = jest.fn(async () => {
  return response;
});
```

```typescript
globalThis.fetch = jest.fn();
```

Do not work around the rule using another mutation mechanism.

```typescript
Object.assign(global, {
  fetch: jest.fn(),
});
```

```typescript
Reflect.set(global, 'fetch', jest.fn());
```

```typescript
Object.defineProperty(global, 'fetch', {
  value: jest.fn(),
});
```

Do not alias the global object and mutate through the alias.

```typescript
const root = global;
root.fetch = jest.fn();
```

These patterns still mutate process-lifetime global state directly.

## Use

Use Jest's spy mechanism to intercept an existing global function.

```typescript
jest.spyOn(global, 'fetch').mockImplementation(
  async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    // Test-specific response handling.
    return response;
  },
);
```

For a simple response:

```typescript
jest.spyOn(global, 'fetch').mockResolvedValue({
  ok: true,
  status: 200,
  json: async () => ({ data: {} }),
} as Response);
```

## Existing Harness Pattern

When a test harness already owns request routing, keep that routing unchanged and replace only the mutation boundary.

Do not change:

```typescript
global.fetch = jest.fn(
  async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    // Existing request routing.
  },
);
```

by restructuring the harness.

Instead make the surgical replacement:

```typescript
jest.spyOn(global, 'fetch').mockImplementation(
  async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    // Existing request routing remains unchanged.
  },
);
```

## Why

`global` and `globalThis` are process-lifetime objects. Assigning properties directly creates mutable shared state visible through the module/test worker lifecycle.

Using `jest.spyOn` keeps the interception under Jest's mock lifecycle instead of expressing the replacement as direct mutation of the module/global object.

The change should modify only the interception mechanism. It must not alter:

- request matching;
- response payloads;
- counters;
- callback invocation;
- retry behavior;
- application behavior;
- the purpose of the tests.

## Test-State Ownership

This pattern does not justify storing additional mutable state at module scope.

Do not introduce module-level mutable mocks such as:

```typescript
const fetchResult = jest.fn();
```

when their implementation or return value is changed between tests.

Mutable scenario state should remain owned by the individual test, fixture invocation, or render lifecycle.

## Validation

Run the module-state rule against the changed test or helper:

```bash
npx eslint \
  --config scripts/eslint/module-state.config.mjs \
  --max-warnings=0 \
  tests/ui-actions/helpers/onboarding-chat-shell-harness.tsx
```

For branch validation:

```bash
npm run lint:module-state -- --changedSince=<base-branch>
```

Also run the directly affected Jest tests.

## Review Checklist

- [ ] No direct assignment to `global.*` or `globalThis.*`.
- [ ] No `Object.assign`, `Reflect.set`, or equivalent global mutation workaround.
- [ ] Existing request-routing behavior is unchanged.
- [ ] Existing response fixtures are unchanged.
- [ ] No unrelated refactor was introduced.
- [ ] Mutable scenario state remains test-owned.
- [ ] `jest.spyOn(...).mockImplementation(...)` is used for the global function interception.
- [ ] Targeted module-state lint passes.
- [ ] Directly affected Jest tests pass.
