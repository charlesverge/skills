---
name: single-read-decision-update
description: Enforce a single-read decision update pattern for repository/service methods that read current entity state, compute outcomes from current state plus new input, persist one mutation, and return a DecisionResult used by callers without same-entity re-reads. Use when refactoring or reviewing update flows that currently do write-then-reload, multiple reads for one decision path, or caller-side follow-up fetches for outcomes that should come from apply_event-style methods.
---

# Single-Read Decision Update

## Objective

Implement state transition flows as one calculation transaction:

1. Read target entity once per execution path.
1. Compute decisions once from existing state and new input.
1. Write one mutation once per execution path.
1. Return decisions once in a `DecisionResult` object.

## Required Method Shape

Use an `apply_event(...) -> DecisionResult` style method name when possible.

Ensure `DecisionResult` includes every downstream outcome needed by callers, such as:

* Updated status/flags.
* Threshold crossing results.
* Retry/defer/block timestamps.
* Side-effect booleans (`should_block`, `should_defer`, `should_notify`).

## Stage Separation (Required)

Keep the flow in clearly separated stages with explicit handoff data:

1. `Fetch`: Load the current entity state once.
1. `Decide`: Compute outcomes from fetched state and event input.
1. `Record modification`: Build the exact mutation payload.
1. `Update (DB record/api)`: Persist one write and return `DecisionResult`.

Each stage must be implemented as its own method. Do not combine stage logic into one method.

Use an explicit method chain with handoff data between methods:

1. `fetch_*` method for `Fetch`
1. `decide_*` method for `Decide`
1. `record_modification_*` method for `Record modification`
1. `update_*` method for `Update (DB record/api)`

Do not blend these stages into one mixed loop or interleave extra reads between stages.

## Conditional Use Case: No-Read Simple Operations

When an operation does not require reading current state, the four-stage method split is not required.

Allowed case:

* A direct counter update using PyMongo with `$inc`.
* No decisioning from existing record fields.
* No follow-up read needed for outcomes in the same flow.

In this case, execute the operation inline in the event handler.

Example:

* Event: `agent_success_ping(agent_id)`
* Inline operation: `collection.update_one({"agent_id": agent_id}, {"$inc": {"success_counter": 1}})`
* No separate `fetch_*`, `decide_*`, `record_modification_*`, `update_*` methods required.

If later behavior needs record-derived decisions (for example reading `pending_tasks` to choose a message), move back to the full staged method pattern.

## Generic Failure Handling (Required)

Wrap the entire operation flow in a `try/except` and route exceptions to a transaction-failed handler.

Required behavior:

* Catch exceptions at the operation boundary.
* Invoke a transaction-failed handler with relevant context.
* Re-raise the exception or return a typed failure result according to the service contract.

Application-specific decisions:

* Whether to roll back the entire transaction.
* Duplicate-event strategy.
* Retry policy and side-effect guarantees.

## Questions for User (Before Modifications)

Ask for clarification before making modifications when required behavior is not explicit.

1. If error-handling behavior is unclear, stop execution and request clarification from the user before changing code.
1. Ask whether failures should retry the entire operation or fail fast without retry.
1. Ask which log level should be used for failure cases (`error`, `warning`, or `info`) and whether different exception types need different levels.
1. Ask whether failed operations should be queued for delayed retry, including the trigger conditions for queueing.
1. Ask whether delayed retry should have limits (max attempts, backoff strategy, or cutoff time) or use existing application defaults.

## Caller Contract

After `apply_event(...)` returns:

* Execute downstream actions only from `DecisionResult`.
* Do not perform `get_*`, `find_*`, or `fetch_*` for the same entity in the same flow.
* Allow a follow-up read only when a separate, explicit consistency boundary requires it.

## Prohibited Pattern

Do not implement:

1. read/update call,
1. then a second read of the same entity,
1. only to recover outcomes that the update method should have returned.

## Refactor Checklist

When converting an existing flow:

1. Locate all same-entity reads in the execution path.
1. Keep only the first read used for decisioning.
1. Move decision calculations into the update method.
1. Return a complete `DecisionResult` from that method.
1. Replace caller follow-up reads with `DecisionResult` fields.
1. Verify one read + one write per execution path in tests and code review.

## Generic Example: Blinker Success Event

Event: `agent_task_completed` with `agent_id`.

1. `Fetch` (`fetch_agent_progress(agent_id)`)

* Read agent progress record once by `agent_id`.
* Capture current `success_counter` and `pending_tasks`.

2. `Decide` (`decide_agent_completion(progress_record)`)

* Compute `new_success_counter = success_counter + 1`.
* If `pending_tasks > 0`, set notification message to `Working`.
* If `pending_tasks == 0`, set notification message to `Finished`.

3. `Record modification` (`record_modification_agent_completion(decision)`)

* Build one update payload with `success_counter = new_success_counter`.
* Build `DecisionResult` with:
  * `success_counter`
  * `pending_tasks`
  * `should_send_user_notification = True`
  * `notification_message` (`Working` or `Finished`)

4. `Update (DB record/api)` (`update_agent_progress(agent_id, mutation, decision_result)`)

* Execute one write for the prepared update payload.
* Return `DecisionResult` from this write path.

Caller behavior:

* Emit `send_user_notification` from `DecisionResult.notification_message`.
* Do not re-fetch the same agent record in this flow.

### One Computation per Outcome

In a single execution path, any business outcome must be computed exactly once and reused everywhere else.

Definition of outcome:

* Any derived decision or value (state transition, flag, counter, ratio, timestamp, status, message, side-effect trigger).

Required:

1. Choose one authority point where each outcome is computed.
1. Return/pass that computed outcome forward as data.
1. Downstream code may map, persist, or emit only; it must not recompute the same outcome.
1. Callers/handlers must consume returned outcomes; no recovery reads or parallel re-derivation.

Prohibited:

* Recomputing the same business outcome in multiple methods, layers, or branches of the same path.
* Re-reading state only to derive outcomes that should already be returned.

Review gate:

* If identical/equivalent decision logic appears in more than one location for the same path, the change is non-compliant.
