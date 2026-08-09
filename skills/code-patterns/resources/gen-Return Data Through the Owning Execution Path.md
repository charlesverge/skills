# Coding Pattern Rule: Return Data Through the Owning Execution Path

## Context

When an operation retrieves, computes, retries, or recovers data for a caller, the caller that initiated the operation should receive the result directly and update the state it owns.

Do not create a secondary communication mechanism to propagate the same result to another part of the application when the normal call/return path can carry that data.

This applies to UI state, API results, retries, recovered requests, background operations, and other application flows where a clear caller already exists.

## Pattern to Use

Use the existing execution path as the single source of truth:

1. The caller initiates the operation.
1. The operation returns a typed success or failure result.
1. The caller consumes that result.
1. The caller updates the state or invokes the next operation it owns.
1. Rendering or downstream behavior derives from that state.

When retrying an operation, return the recovered result to the retry owner and let that owner apply the result through the same state-management path used by a normal successful request.

Example:

```ts
const result = await loadItem();

if (!result.ok) {
  setLoadError(true);
  return;
}

setLoadError(false);
setItem(result.data);
```

The returned value is the authoritative result. State changes remain explicit and traceable to the caller.

## Pattern Not to Use

Do not add side-channel communication to duplicate or bypass the normal execution path.

Examples of prohibited patterns include:

- dispatching a browser `CustomEvent` with data already returned by a function;
- adding a global event listener solely to transfer operation results into application state;
- storing a callback in module-global mutable state so unrelated code can invoke it when an operation completes;
- writing transient operation results to browser storage so another component can discover them;
- mutating the DOM to communicate state between React components;
- intercepting or replacing global functions such as `fetch` to observe completion that the caller can already await;
- updating two independent state paths from the same successful operation.

Do not use this pattern:

```ts
async function loadItem() {
  const result = await fetchItem();

  window.dispatchEvent(
    new CustomEvent('item-loaded', {
      detail: result,
    }),
  );

  return result;
}
```

with another component doing:

```ts
useEffect(() => {
  const handler = (event: Event) => {
    setItem((event as CustomEvent).detail);
  };

  window.addEventListener('item-loaded', handler);
  return () => window.removeEventListener('item-loaded', handler);
}, []);
```

Instead, the caller of `loadItem()` must consume the returned result and update the appropriate state directly.

## Rule

If the required data is already available through the function's return value, callback contract, component props, or established state owner, use that path.

A secondary event, storage, DOM, global callback, interception, or synchronization mechanism must not be introduced for the same result.
