## Loaded Data Stability Rule

Components that have successfully rendered data must distinguish **initial loading** from **subsequent refetching**.

- A full loading skeleton, empty placeholder, or replacement loading view may render only when the component has no successful data for the active dataset.
- After successful data has rendered, a filter, sort, refresh, pagination, retry, or other user-triggered refetch must not unmount or replace the existing content solely because the request is pending.
- During a refetch, the existing content must remain mounted until the replacement response is ready. The component may set `aria-busy="true"` and show a non-disruptive progress indicator.
- Mutation controls associated with potentially stale data must be disabled or otherwise made non-interactive while the refetch is pending. Removing the entire content subtree to hide those controls is prohibited.
- Successful refetch results must replace the previous data in one render transition. A failed refetch must retain the previous successful data and show the error separately.
- The content region must preserve its layout dimensions during the request and response transition. Loading behavior must not cause the surrounding page to collapse, expand abruptly, or visibly flash.
- Changing to a dataset that has never loaded may use the initial loading state. Previously loaded datasets should retain their last successful state while being refreshed.

Required regression tests must verify that:

1. Initial loading can render a skeleton.
1. A refetch keeps previously rendered records mounted.
1. Existing mutation controls are unavailable during the refetch.
1. The loading skeleton does not replace previously rendered records.
1. The new response replaces the old records only after it resolves.
1. A failed refetch leaves the previous successful records visible.
