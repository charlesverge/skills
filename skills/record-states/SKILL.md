# Record State Handling Skill

## Purpose

Provide a consistent way to handle invalid or incomplete record state during processing while preserving workflow convergence and keeping responsibility boundaries clear between the processing function and its caller.

This skill applies regardless of where records are stored:

* in memory
* database
* cache
* queue payloads
* serialized files

## Core Rule

**Favor convergent state transitions over local purity. Never skip processing in a way that preserves stale retry-selection state.**

## Responsibility Boundary

This skill separates responsibilities between two layers.

### Callee responsibility

The function operating on the record must decide:

* whether the current record state is valid for the operation
* whether the operation can continue safely
* whether the state issue is blocking or non-blocking
* whether any repair is allowed by explicit contract

### Caller responsibility

The caller of the function must decide what to do after a blocking failure, such as:

* retry later
* mark terminal failure
* quarantine
* escalate
* trigger repair flow

The callee must not silently decide workflow disposition unless that responsibility is explicitly part of its contract.

## Operating Principles

### 1. No automatic repair by default

Do not repair, synthesize, backfill, normalize, or infer missing or invalid record state unless explicitly allowed.

### 2. Non-blocking invalid state may continue

If a state issue does not affect the correctness of the current operation, the operation may continue.

### 3. Blocking invalid state must fail fast

If a required field, value, or invariant is needed for the current operation and is missing or invalid, raise an exception immediately.

### 4. Local safety is not enough

A locally safe action such as `continue`, `return`, or `skip` is not acceptable if it leaves the record in a stale state that causes repeated future selection without convergence.

### 5. Exceptions should be structured

A blocking failure should raise a structured exception type that describes the state problem clearly enough for the caller to decide workflow disposition.

## Decision Model

When a function encounters a record state issue, evaluate the following in order:

1. Is the field or invariant required for the current operation?
2. If missing or invalid, would continuing produce an incorrect result?
3. If the operation is skipped, would the record remain eligible for repeated future processing?
4. Is repair explicitly allowed for this field or issue type?
5. Is the issue non-blocking, or must execution stop now?

From that evaluation, the function must choose one of the following outcomes.

## Allowed Outcomes

### Outcome A: Continue unchanged

Use when the record state is valid enough for the operation and no state issue needs to be surfaced.

### Outcome B: Log and continue

Use when the record has an invalid or incomplete state, but that issue does not affect the correctness of the current operation.

Requirements:

* log the issue clearly
* continue the operation
* do not auto-repair unless explicitly allowed
* do not hide the state issue

Example:

* `created_on` is missing
* current operation only updates payload data and writes `updated_on`
* `created_on` is not required for this decision

### Outcome C: Raise blocking state exception

Use when the record is in an invalid state that prevents the function from making a correct decision or performing the operation safely.

Requirements:

* raise immediately
* do not continue partially
* do not guess or infer missing required values
* leave retry or terminal handling to the caller

Example:

* `record_type` is required for branching
* `record_type` is missing or not in the allowed enum

### Outcome D: Repair and continue

Use only when explicit policy, configuration, or caller contract allows deterministic repair.

Requirements:

* repair must be explicit, not assumed
* repair must be deterministic
* repair must be logged
* operation may continue only after repair makes the state valid enough

Example:

* caller explicitly allows backfilling a lifecycle field using a known deterministic rule

## Non-Blocking vs Blocking Guidance

### Non-blocking state issue

A state issue is non-blocking when all of the following are true:

* the current operation does not require the missing or invalid field
* continuing does not change branching or correctness
* continuing does not hide a workflow-level convergence problem
* the issue can be surfaced through logging

### Blocking state issue

A state issue is blocking when any of the following are true:

* the field is required to make a decision
* the field is required to preserve correctness
* the value is invalid and affects branching or output
* continuing would produce undefined or misleading behavior
* skipping would preserve stale retry-selection state and prevent convergence

## Convergence Rule

The function must not silently skip work in a way that leaves the record eligible for repeated future processing without state advancement.

This means:

* do not use `continue` as a local escape hatch without checking workflow impact
* do not preserve stale selection markers when the operation is being abandoned
* do not encode a consistency-over-liveness tradeoff silently

If the function cannot both preserve correctness and advance the record safely, it must raise an exception and let the caller decide workflow disposition.

## Exception Contract

Blocking invalid state exceptions should be structured and machine-readable where possible.

Recommended minimum fields:

* exception type
* record identifier if available
* operation name
* field name or invariant name
* failure reason
* observed value if safe to include
* expected requirement

Example categories:

* missing required field
* invalid enum value
* invariant violation
* malformed record state

The goal is that the caller can make a workflow decision without reinterpreting vague error text.

## What This Skill Does Not Decide

This skill does not define caller-side workflow disposition.

After a blocking exception is raised, the caller may choose actions such as:

* retry
* fail permanently
* quarantine
* alert
* repair through a separate path

Those decisions belong to orchestration logic, not to the callee, unless explicitly delegated.

## Examples

### Example 1: Missing optional lifecycle field

Record state:

* `created_on` missing

Operation:

* update record payload
* write `updated_on`

Decision:

* `created_on` is not required for this operation
* operation correctness is preserved without it

Result:

* log invalid state
* continue
* do not auto-repair

### Example 2: Missing required type field

Record state:

* `record_type` missing

Operation:

* branch behavior depends on `record_type`

Decision:

* function cannot choose a correct path

Result:

* raise blocking state exception
* caller decides retry, terminal failure, or other disposition

### Example 3: Deterministic repair explicitly allowed

Record state:

* lifecycle field missing

Operation:

* caller contract explicitly allows deterministic backfill

Decision:

* repair is allowed
* repair rule is known and stable

Result:

* repair field
* log repair
* continue

### Example 4: Local skip would break convergence

Record state:

* required metadata missing during update path
* skipping would leave retry-selection state unchanged

Decision:

* local skip is not acceptable because the record would remain eligible for repeated reprocessing

Result:

* do not silently skip
* either repair if explicitly allowed or raise blocking exception

## Review Checklist

Before choosing to continue, skip, or fail, ask:

1. Is this field required for the current operation?
2. Can the operation still produce a correct result?
3. Would skipping preserve stale retry-selection state?
4. Am I about to hide a workflow-level liveness problem behind a local guard?
5. Am I repairing something that has not been explicitly authorized?
6. If I raise, will the caller receive a clear enough reason to decide what happens next?

## Minimal Rule Set

Use this shorter form when embedding the skill into another specification.

* Do not auto-repair record state unless explicitly allowed.
* If a state issue is non-blocking, log it and continue.
* If a state issue is blocking, raise an exception immediately.
* Do not skip processing in a way that preserves stale retry-selection state.
* The callee decides whether execution can continue; the caller decides workflow disposition after blocking failure.
* Blocking state exceptions should classify the failure clearly enough for the caller to act.

## Summary

This skill exists to prevent a common failure mode: choosing a locally safe action that preserves global non-convergence.

The main rule is not simply to protect field integrity. The main rule is to protect correctness while ensuring that invalid-state handling does not silently create endless retry loops or hide workflow-level failure behind local control flow.
