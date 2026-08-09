# Coding Pattern Rule: Preserve Exact Request Semantics

## Context

When a caller requests a specific resource, endpoint, identifier, query, or operation, the implementation must perform that exact request unless the caller explicitly selects a different operation.

Infrastructure helpers such as request coalescers, caches, retry utilities, transport adapters, and persistence helpers must not silently change the meaning of the caller's request.

Retry behavior must also preserve the contract owned by the caller. A retry should repeat the request the caller intends to retry, not infer a different prior request from hidden state.

## Pattern to Use

Keep transport and infrastructure helpers narrowly scoped to their declared responsibility.

For example, a request-coalescing helper may share an identical in-flight request:

```ts
export async function coalescedGet<T>(url: string): Promise<T> {
  const existing = inFlight.get(url);

  if (existing !== undefined) {
    return existing;
  }

  const request = fetch(url).then(readResult);
  inFlight.set(url, request);

  try {
    return await request;
  } finally {
    if (inFlight.get(url) === request) {
      inFlight.delete(url);
    }
  }
}
```

The request key and the actual request remain the same.

If the application needs to retry a request with a specific identifier, the owning feature must retain that identifier explicitly and make the intended request:

```ts
await loadQuestion(questionId);
```

If the intended retry is the current-resource request, perform that exact request:

```ts
await loadCurrentQuestion();
```

The caller remains the source of truth for what operation is being performed.

## Pattern Not to Use

Do not keep hidden state in a generic transport helper and use that state to substitute one request for another.

Do not use patterns such as:

```ts
const failedRequests = new Map<string, string>();

function resolveRequest(url: string): string {
  return failedRequests.get(genericKey(url)) ?? url;
}

export async function get(url: string) {
  return fetch(resolveRequest(url));
}
```

In this pattern, code requesting:

```text
/api/items?category=current
```

may unknowingly receive the result of:

```text
/api/items?category=current&item_id=123
```

That changes the request contract without the caller's knowledge.

Also do not:

- retain failed identifiers inside generic networking utilities for later implicit reuse;
- rewrite query parameters based on previous failures;
- silently redirect a retry to a previous request;
- infer caller intent from transport-layer history;
- add hidden fallback requests when the explicit request fails;
- return successful data from a different request than the one the caller issued;
- maintain multiple competing sources of truth for which resource should be loaded.

## Rule

A function must execute the operation represented by its explicit inputs.

Infrastructure code may optimize how an operation is executed, but it must not change what operation is executed.

If a different request is required after failure, that decision must be explicit in the owning feature or action layer and the required identifier or state must be passed directly.

Never substitute a previous, inferred, or fallback request for the caller's current request without an explicit contract requiring that behavior.
