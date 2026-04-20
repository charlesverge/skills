---
name: error-classification-policy
description: Classify failures into temporary versus permanent using a contract-aware policy that treats transport failures as retryable by default and shape/invariant mismatches as usually non-retryable unless policy says otherwise.
---

# Error Classification Policy

## Use This Skill When

Use this skill when you need to classify failures as temporary or permanent in multi-stage processing flows, especially where an LLM produces payloads consumed by later stages.

## Core Definitions

### Contract errors

Contract errors are invariant or payload shape mismatches between producer and consumer. They are not transport conditions.

Common contract errors:

* missing required payload fields
* wrong payload type (expected dict/string shape but got another type)
* unsupported request type for a stage
* schema validation mismatch where input format is wrong for the called stage or model

### Connection errors

Connection errors are transport or environment failures such as timeout, DNS, connection reset, or `APIConnectionError`.

## Default Classification Policy

Apply the following defaults unless an explicit local policy overrides them:

1. Connection errors: classify as temporary.
2. Contract and schema errors: classify as permanent by default.
3. Validation errors: classify according to explicit team policy for that flow.

## LLM-Specific Rule In This Policy

For this flow, classify data-contract outcomes as:

1. Temporary: payload produced by an LLM that fails contract/shape requirements.
2. Permanent: LLM response is structurally proper, but business-result data indicates failure (for example, explicit fail outcome in valid output).

Use this rule consistently across stage paths and script paths so retries and terminal handling behave the same.

## Why Contract Errors Differ From Connection Failures

* connection failures often succeed on retry without input change
* contract errors usually repeat until code mapping, schema expectations, or data production is corrected

Do not treat these categories as interchangeable.

## Validation Errors Are Policy-Sensitive

Validation errors are not universally temporary or permanent.

* In eventually consistent systems, they can be temporary.
* In local deterministic payload/schema checks, they are often repeatable and therefore often non-temporary.

When implementing logic, avoid hard-coding universal assumptions like `validation == temporary`. Use explicit policy flags or clear per-flow rules.

## Decision Procedure

Classify in this order:

1. Determine error family: connection, contract/schema, validation, or business-result failure.
2. Check whether local policy overrides the default.
3. If no override exists, apply defaults in this skill.
4. Emit classification with machine-usable metadata (family, temporary/permanent, reason, stage).

## Output Contract Recommendation

When returning classification from code paths, include:

* `error_family`
* `classification` (`temporary` or `permanent`)
* `reason`
* `stage`
* `retry_recommended` (boolean)

Keep naming and values stable across services so orchestration logic stays deterministic.
