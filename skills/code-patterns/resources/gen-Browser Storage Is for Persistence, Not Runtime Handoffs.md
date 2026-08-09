# Coding Pattern Rule: Browser Storage Is for Persistence, Not Runtime Handoffs

## Context

Browser storage such as `sessionStorage` and `localStorage` may be used when state genuinely needs to survive beyond the current in-memory application lifecycle.

Valid persistence requirements can include:

- surviving a page reload;
- surviving a new browser navigation where application state is intentionally recreated;
- preserving an explicitly documented user preference;
- retaining data across browser sessions when that persistence is part of the product contract.

Browser storage should not be used merely to transfer transient state between components, route handlers, providers, or consecutive operations while the application is already running.

If React state, context, router state, function return values, explicit parameters, or another established state owner already represents the information, that existing path should remain authoritative.

## Pattern to Use

Keep transient state with the component or system that owns it:

```ts id="rgsrva"
const [retainSummary, setRetainSummary] = useState(false);

return (
  <Summary
    showAction={showAction || retainSummary}
  />
);
```

For routing or authentication transitions, invoke the owning routing mechanism directly:

```ts id="2iwph3"
const decision = await route({
  intent: 'error.unauthenticated',
  currentPathname,
});

await executeRouteDecision(decision, {
  navigate,
  applyState,
});
```

For state that must cross component boundaries during the same application lifecycle, use an explicit ownership mechanism:

```text id="tljnrk"
action
  → returned result
  → owning component/context/router
  → state update
  → render
```

Use browser storage only when persistence itself is a requirement:

```ts id="h8um62"
localStorage.setItem('theme', selectedTheme);
```

and consume that persisted value through a clearly defined persistence boundary.

## Pattern Not to Use

Do not use browser storage as a one-shot message queue between application layers:

```ts id="0h2bfk"
sessionStorage.setItem('next-chat-state', 'watch');
```

followed elsewhere by:

```ts id="q2o1w1"
const state = sessionStorage.getItem('next-chat-state');
sessionStorage.removeItem('next-chat-state');

if (state) {
  applyState(state);
}
```

Do not stage transient control-flow markers before invoking an operation that already owns the transition:

```ts id="0twpur"
sessionStorage.setItem('unauthenticated', 'true');

navigateToSignIn();
```

when the router or authentication flow can represent the unauthenticated transition directly.

Also avoid:

- storing temporary UI flags solely so another mounted component can recover them;
- writing route state to storage and reading it back after navigation when the router already carries that state;
- using `sessionStorage` as an event bus;
- using storage keys as hidden communication between unrelated modules;
- writing a value only to immediately consume and delete it elsewhere;
- maintaining both browser-storage state and live application state for the same transient condition.

## Rule

Use browser storage only when persistence across an application-lifecycle boundary is an explicit requirement.

For transient application state, keep one authoritative runtime owner and pass state through normal application mechanisms such as return values, React state, context, props, callbacks, or router state.

Do not introduce browser storage merely to hand state from one part of a running application to another.
