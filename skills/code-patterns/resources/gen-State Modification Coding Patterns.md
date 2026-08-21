# Global State Modification Coding Patterns

## Purpose

Code must not mutate process-, runtime-, browser-, or module-lifetime state when the same behavior can be owned by the current request, component, service instance, test, or fixture.

The important distinction is **ownership and lifetime**, not whether a binding uses `const`, nor whether the mutation is hidden behind a helper such as `Object.defineProperty`.

The repository's module-state guidance already defines mutable values attached to `globalThis`, imported modules, React contexts, and other process-lifetime singletons as mutable module state. It also states that moving mutation into a closure, singleton, or reset helper does not correct ownership.

## General rule

Avoid:

```ts
globalValue.property = value;
```

and equivalent indirect forms when `globalValue` is not owned by the current execution scope.

Prefer:

```ts
const dependency = createDependency();

run(dependency);
```

or use the framework's existing request-, component-, fixture-, worker-, or service-owned dependency boundary.

The goal is:

```text
global/process lifetime
        ↓
avoid mutable ownership here

request / component / fixture / test / service instance
        ↓
own mutable state here
```

## Direct property assignment

### Avoid

```ts
window.ResizeObserver = MockResizeObserver;

global.fetch = mockFetch;

globalThis.cache = cache;

process.someState = value;

navigator.customValue = value;

document.customState = state;
```

Nested assignment is the same problem:

```ts
process.env.NODE_ENV = 'test';

window.config.current = value;

globalThis.runtime.state.ready = true;
```

The property depth does not change ownership. The root object is still global.

### Production alternative

Pass dependencies explicitly:

```ts
class Runtime {
  constructor(private readonly fetcher: Fetcher) {}

  async run(): Promise<Result> {
    return this.fetcher.fetch();
  }
}
```

For browser behavior, use an existing abstraction or component-owned dependency:

```ts
function createObserver(
  Observer: typeof ResizeObserver,
): ResizeObserver {
  return new Observer(() => {});
}
```

For request-specific state, keep it on the request/service instance:

```ts
class RequestContext {
  cache = new Map<string, Result>();
}
```

Do not attach request-specific state to `globalThis`.

### Test alternative

Create the replacement inside the test and pass it through the real dependency boundary:

```ts
test('uses observer', () => {
  const observer = new MockResizeObserver();

  renderSubject(observer);
});
```

For browser integration behavior, use Playwright's browser-owned environment rather than replacing JSDOM globals:

```ts
test('renders in the browser', async ({ page }) => {
  await page.goto('/agents/chat');
});
```

For HTTP interception, use a test-scoped Playwright route rather than replacing `global.fetch`:

```ts
test('handles response', async ({ page }) => {
  await page.route('**/api/v1/example', async (route) => {
    await route.fulfill({
      status: 200,
      json: { status: 'success' },
    });
  });

  await page.goto('/example');
});
```

The repository already uses Playwright fixtures such as `request`, `runtime`, and `testInfo.parallelIndex` to give tests isolated runtime resources rather than process-global ownership.

***

## `Object.defineProperty`

### Avoid

```ts
Object.defineProperty(window, 'ResizeObserver', {
  configurable: true,
  value: MockResizeObserver,
});
```

Also avoid equivalent mutations:

```ts
Object.defineProperty(globalThis, 'fetch', {
  value: mockFetch,
});

Object.defineProperties(window, {
  EventSource: {
    value: MockEventSource,
  },
});
```

`Object.defineProperty` is still a mutation. It differs mechanically from assignment, but not in state ownership.

The lint rule explicitly treats `Object.defineProperty`, `Object.defineProperties`, `Object.assign`, and `Object.setPrototypeOf` as mutation APIs whose first argument is the mutation target.

### Alternative

Inject or instantiate the dependency at the owning scope.

Bad:

```ts
Object.defineProperty(window, 'ResizeObserver', {
  value: MockResizeObserver,
});
```

Preferred:

```ts
const observerFactory = (): ResizeObserver =>
  new MockResizeObserver();

renderSubject({ observerFactory });
```

For tests that actually require browser semantics, prefer Playwright rather than reconstructing browser globals in Jest.

***

## `Object.assign`

### Avoid

```ts
Object.assign(globalThis, {
  fetch: mockFetch,
});
```

Also avoid using an alias:

```ts
const root = globalThis;

Object.assign(root, {
  fetch: mockFetch,
});
```

Aliasing does not establish new ownership.

### Alternative

Construct a local value:

```ts
const runtime = {
  fetch: mockFetch,
};
```

and pass it:

```ts
await run(runtime);
```

***

## `Reflect` mutation APIs

These should be treated like assignment.

### Avoid

```ts
Reflect.set(window, 'ResizeObserver', MockResizeObserver);

Reflect.defineProperty(globalThis, 'cache', {
  value: cache,
});

Reflect.deleteProperty(globalThis, 'cache');

Reflect.setPrototypeOf(window, prototype);

Reflect.preventExtensions(globalThis);
```

The current rule explicitly recognizes `Reflect.defineProperty`, `Reflect.deleteProperty`, `Reflect.preventExtensions`, `Reflect.set`, and `Reflect.setPrototypeOf` as mutating operations.

### Alternative

Operate on an object created and owned by the current scope:

```ts
const runtime = {};

Reflect.set(runtime, 'observer', MockResizeObserver);
```

Better still, when the shape is known:

```ts
const runtime = {
  observer: MockResizeObserver,
};
```

***

## Collection mutation

Global state does not need to look like a browser global.

### Avoid

```ts
const cache = new Map<string, Result>();

export function save(key: string, value: Result): void {
  cache.set(key, value);
}
```

Also:

```ts
const listeners = new Set<Listener>();

listeners.add(listener);
listeners.delete(listener);
listeners.clear();
```

and arrays:

```ts
const messages: Message[] = [];

messages.push(message);
messages.splice(0, 1);
messages.sort(compare);
```

A module-level `const` only prevents rebinding. It does not make the referenced value immutable.

The repository guideline explicitly identifies module-level objects, arrays, `Map`, `Set`, and Jest mocks whose internal state changes as mutable module state.

### Production alternative

Put mutable collections on an instance whose lifecycle matches their intended ownership:

```ts
class SessionState {
  messages: Message[] = [];
  listeners = new Set<Listener>();
}
```

Create the instance at the appropriate boundary:

```ts
const state = new SessionState();
```

Do not create one module-level shared instance unless shared process-lifetime state is explicitly part of the required architecture.

### Test alternative

Create one state container per test:

```ts
test('adds a listener', () => {
  const listeners = new Set<Listener>();

  runSubject(listeners);

  expect(listeners.size).toBe(1);
});
```

***

## Mutating instance methods

The lint rule recognizes common mutation methods including:

```text
add
append
clear
copyWithin
delete
fill
pop
prepend
push
reverse
set
shift
sort
splice
unshift
```

It also treats methods matching `setX...` as potentially mutating.

### Avoid

```ts
globalCache.set(key, value);

window.someList.push(item);

document.body.append(node);

globalRegistry.clear();
```

### Alternative

Mutate a locally owned instance:

```ts
const cache = new Map<string, Result>();

cache.set(key, value);
```

Local mutation is not inherently wrong. The problem is mutation of an object whose lifetime exceeds the owning operation.

***

## Borrowed mutation methods

Moving the method does not change the target.

### Avoid

```ts
Array.prototype.push.call(globalMessages, message);

Set.prototype.add.call(globalListeners, listener);
```

Likewise:

```ts
Array.prototype.push.apply(globalMessages, messages);
```

The mutation target remains the global object.

The rule specifically follows borrowed mutating methods through `.call()` and `.apply()`.

### Alternative

Use an operation-owned collection:

```ts
const messages: Message[] = [];

messages.push(message);
```

***

## `delete`

### Avoid

```ts
delete globalThis.cache;

delete window.mockValue;

delete moduleState.current;
```

Removing a property is still mutation.

### Alternative

Do not install temporary process-global state that requires later deletion.

Bad lifecycle:

```ts
beforeEach(() => {
  globalThis.cache = cache;
});

afterEach(() => {
  delete globalThis.cache;
});
```

Preferred lifecycle:

```ts
test('uses cache', () => {
  const cache = new Map();

  runSubject(cache);
});
```

The repository guidance specifically rejects reset APIs and cleanup patterns as substitutes for correct ownership.

***

## Increment and update operators

### Avoid

```ts
globalThis.counter++;

window.runtime.retryCount--;

moduleState.count += 1;
```

These are equivalent to assignment for ownership purposes.

### Alternative

Keep the counter on the operation-owned object:

```ts
class RequestState {
  count = 0;

  increment(): void {
    this.count += 1;
  }
}
```

***

## Aliasing global state

### Avoid

```ts
const root = globalThis;

root.cache = cache;
```

or:

```ts
const runtime = window.runtime;

runtime.ready = true;
```

or destructuring:

```ts
const { runtime } = globalThis;

runtime.ready = true;
```

An alias does not create a new object or shorten its lifetime.

The existing lint implementation tracks aliases back to their protected origin specifically to prevent this kind of bypass.

### Alternative

Create a new instance owned by the current operation instead of aliasing an existing global.

***

## Imported module mutation

### Avoid

```ts
import { state } from './state';

state.ready = true;
```

Imports are process/module-owned references. Mutating an imported object changes shared module state.

### Alternative

Export constructors, factories, immutable values, or operations rather than mutable containers.

Preferred:

```ts
export function createState(): State {
  return {
    ready: false,
  };
}
```

Caller:

```ts
const state = createState();

state.ready = true;
```

The mutation is now owned by the caller's lifecycle.

***

## Environment variables

Runtime environment variables are configuration, not mutable application state.

### Avoid

```ts
process.env.NODE_ENV = 'test';

process.env.API_URL = testUrl;

delete process.env.FEATURE_FLAG;
```

Repository rules explicitly treat environment variables as read-only.

### Alternative

Read configuration at the boundary and pass the value into the code that needs it:

```ts
const config = {
  apiUrl: process.env.API_URL,
};

start(config);
```

Tests should provide configuration directly:

```ts
test('uses configured API', () => {
  const config = {
    apiUrl: 'http://example.test',
  };

  const result = run(config);
});
```

Do not modify the process environment to configure individual tests.

***

# Test-specific guidance

## Do not use `beforeEach` to repair global state ownership

### Avoid

```ts
beforeEach(() => {
  global.fetch = jest.fn();
  window.history.pushState(null, '', '/agents/chat');

  Object.defineProperty(window, 'ResizeObserver', {
    value: MockResizeObserver,
  });
});
```

Repeatedly resetting a global does not make it test-owned.

The repository's test-state guidance explicitly says mutable test values must be created inside the test, a test-scoped fixture, or a render-owned provider instance, and must not require reset functions to become safe for the next test.

## Prefer test-owned harnesses

```ts
class MockHarness {
  fetch = jest.fn();
  messages: Message[] = [];
  listeners = new Set<Listener>();
}

test('submits a message', () => {
  const harness = new MockHarness();

  renderSubject(harness);

  expect(harness.fetch).toHaveBeenCalled();
});
```

One test receives one harness.

Do not do:

```ts
const harness = new MockHarness();

beforeEach(() => {
  harness.reset();
});
```

That is still one module-owned mutable object.

## Prefer React provider ownership where mocks need render state

```ts
test('renders state', () => {
  const harness = new MockHarness();

  render(
    <HarnessProvider value={harness}>
      <Subject />
    </HarnessProvider>,
  );
});
```

The repository guideline specifically recommends a test-owned harness in a React provider when hoisted Jest mocks need render-scoped state.

## Prefer Playwright for real browser globals

When a test requires:

```text
window
document
navigator
history
ResizeObserver
EventSource
HTMLElement.prototype
real fetch/browser networking
```

consider whether the test is actually a browser integration test.

Instead of reconstructing the browser:

```ts
Object.defineProperty(window, 'ResizeObserver', ...);
Object.defineProperty(window, 'EventSource', ...);
global.fetch = jest.fn(...);
```

use the real Playwright page when the behavioral contract is browser-level:

```ts
test('completes the browser workflow', async ({ page }) => {
  await page.goto('/agents/chat');

  await page.getByLabel('Message input').fill(
    'Please review my resume.',
  );

  await page.getByRole('button', {
    name: 'Send',
  }).click();
});
```

Use Playwright fixtures to own mutable resources at the test/worker boundary. The existing isolated-database tests demonstrate this pattern with `request`, `runtime`, and `testInfo`.

***

# Production-specific guidance

## Prefer dependency injection

Bad:

```ts
globalThis.client = new ApiClient();
```

Preferred:

```ts
const client = new ApiClient();

const service = new Service(client);
```

## Prefer explicit parameters

Bad:

```ts
function search(): Promise<Result[]> {
  return globalThis.searchClient.search();
}
```

Preferred:

```ts
function search(
  client: SearchClient,
): Promise<Result[]> {
  return client.search();
}
```

## Prefer instance-owned state

Bad:

```ts
const cache = new Map<string, Result>();
```

Preferred:

```ts
class SearchSession {
  cache = new Map<string, Result>();
}
```

The instance should be created by the lifecycle that owns the state.

## Prefer immutable module definitions

Suitable module-level values include:

```ts
const RETRY_LIMIT = 3;

const EMPTY_RESULTS: readonly Result[] = [];

class SearchSession {}

function createSession(): SearchSession {
  return new SearchSession();
}
```

Avoid module-level values whose contents or behavior change during execution.

***

# Decision guide

Use this sequence when reviewing a mutation:

```text
1. What object is actually being mutated?
           ↓
2. Where was that object created?
           ↓
3. How long does that object live?
           ↓
4. Is that lifetime longer than the operation/test/request
   that owns the change?
           ↓
      yes → ownership defect
      no  → local mutation may be valid
```

Then choose the closest existing ownership boundary:

```text
Production
  request
  service instance
  component/provider
  explicit function parameter
  existing framework context

Tests
  local test variable
  test-owned harness
  render-owned provider
  Playwright page/context
  Playwright test or worker fixture
```

Do not create a parallel global registry or reset mechanism merely to make the mutation easier to access.

# Review checklist

- [ ] No direct assignment to externally owned globals.
- [ ] No nested assignment through `window`, `globalThis`, `global`, `process`, `document`, `navigator`, or another external root.
- [ ] No `Object.assign`, `Object.defineProperty`, `Reflect.*`, or equivalent helper mutates global/module state.
- [ ] No collection mutation operates on a process/module-owned object.
- [ ] No `.call()` or `.apply()` hides mutation of global state.
- [ ] No imported mutable object is modified.
- [ ] No alias is used to conceal a global origin.
- [ ] Tests do not depend on `beforeEach`/`afterEach` resetting global state.
- [ ] Jest mutable state belongs to one test or render lifecycle.
- [ ] Browser-level behavior uses Playwright when real browser APIs are part of the contract.
- [ ] Environment variables are treated as read-only.
- [ ] Mutable production state belongs to the narrowest appropriate service/request/component instance.
- [ ] No reset, cleanup, singleton, wrapper, or closure merely hides process-lifetime mutable state.
