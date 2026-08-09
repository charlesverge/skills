# Coding Pattern Rule: State Owners Must Emit Their Own Resulting Behavior

## Context

When a component, service, action, or domain object owns a state transition, behavior that directly results from that transition should be triggered by the same owner.

Examples include:

- announcing successful actions;
- showing success or error feedback;
- recording analytics;
- enabling follow-up controls;
- updating related local state;
- invoking completion callbacks;
- triggering accessibility status messages.

Other parts of the application should not inspect rendered output, CSS classes, DOM attributes, or other implementation details to infer that the state transition occurred.

## Pattern to Use

Trigger dependent behavior directly from the successful operation that owns the state transition.

```ts
async function performAction() {
  const result = await saveAction();

  setCommitted(true);
  setAnnouncement(`Action completed for ${result.name}`);
  onComplete?.();
}
```

The operation establishes success, updates its state, and emits the behavior associated with that success.

For UI accessibility feedback, render the live region from state owned by the same component:

```tsx
const [announcement, setAnnouncement] = useState('');

async function performAction() {
  await submitAction();
  setCommitted(true);
  setAnnouncement('Action completed');
}

return (
  <>
    {announcement ? (
      <p role="status" aria-live="polite" className="sr-only">
        {announcement}
      </p>
    ) : null}

    <ActionControls />
  </>
);
```

The application therefore has one authoritative success path.

## Pattern Not to Use

Do not infer application state by observing its rendered representation.

For example, do not watch the document for a CSS class that happens to represent successful state:

```ts
const observer = new MutationObserver(() => {
  const committed = document.querySelector('.action.committed');

  if (committed) {
    announceSuccess();
  }
});

observer.observe(document.body, {
  subtree: true,
  childList: true,
  attributes: true,
  attributeFilter: ['class'],
});
```

Do not use:

- `MutationObserver` to discover domain or application state;
- CSS class changes as an event system;
- DOM attributes as a state synchronization mechanism;
- document-wide scanning to detect successful operations;
- polling rendered elements to determine whether an action completed;
- a global component that reconstructs state already known by the component performing the operation.

Rendered DOM is an output of application state, not an authoritative source from which application state should normally be reconstructed.

## Rule

Behavior caused by a state transition must be emitted by the code that owns and confirms that transition whenever that ownership path is available.

Pass the resulting state or event explicitly through React state, props, callbacks, context, returned values, or the appropriate domain interface.

Do not observe the DOM to infer an application event that the application already knows occurred.
