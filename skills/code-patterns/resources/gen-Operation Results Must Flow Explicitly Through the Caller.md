# Coding Pattern Rule: Operation Results Must Flow Explicitly Through the Caller

## Context

When a function performs a focused operation such as parsing, fetching, validating, transforming, or decoding data, callers should receive that result directly and decide what happens next.

Application state transitions, navigation, follow-up actions, notifications, and other side effects should be owned by the layer that initiated the operation or explicitly owns the resulting behavior.

A utility must not depend on mutable module-global callbacks or registries to trigger unrelated application behavior after it completes.

## Pattern to Use

Keep focused utilities focused on their declared responsibility:

```ts
async function readResult(response: Response): Promise<Result | null> {
  if (!response.ok) {
    return null;
  }

  return parseResult(await response.json());
}
```

The owning caller then handles the result explicitly:

```ts
const result = await readResult(response);

if (result === null) {
  handleFailure();
  return;
}

setResult(result);

const decision = await route({
  intent: 'next-state',
  currentPathname,
});

await executeRouteDecision(decision, {
  navigate,
  applyState,
});
```

The control flow should be visible from the call site:

```text
caller
  → operation
  → returned result
  → caller-owned state transition
```

If multiple callers need different follow-up behavior, each caller should handle the same returned result according to its own contract.

## Pattern Not to Use

Do not store a callback in mutable module-global state and invoke it implicitly from an otherwise unrelated utility:

```ts
let activeHandoff: (() => Promise<void>) | null = null;

export function registerHandoff(callback: () => Promise<void>) {
  activeHandoff = callback;
}

export async function readResult(response: Response) {
  const result = parseResult(await response.json());

  await activeHandoff?.();

  return result;
}
```

Do not create control flow where the apparent caller is not the actual owner of the resulting behavior:

```text
caller
  → parser
      → hidden global callback
          → unrelated provider
              → state transition
```

Also avoid:

- mutable module-global callback slots;
- singleton callback registries for request completion;
- parser or transport helpers that trigger unrelated UI state changes;
- registration/unregistration lifecycles solely to transfer operation results;
- hidden navigation or routing side effects inside data-processing helpers;
- behavior that changes depending on whether some unrelated component previously registered a callback.

## Rule

Return operation results directly to the caller.

The layer that owns the action must explicitly perform the state transition or follow-up behavior caused by that result.

Do not use mutable module-global callbacks, registries, or hidden handoffs to transfer control between unrelated parts of the application when normal return values, callbacks passed as explicit arguments, props, or owned state can express the flow directly.
