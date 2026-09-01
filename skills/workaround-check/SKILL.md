---
name: workaround-check
description: Review generated modification plans and reject workaround-style solutions that evade constraints instead of fixing the root cause.
---

# Workaround Check

## Use This Skill When

Use this skill whenever a modification is made from instructions and a plan has been generated. Run it after the initial plan is written and before implementation begins.

Apply it to plans for:

- lint or static-analysis fixes
- bug fixes
- type-checking fixes
- refactors
- architecture or layering changes
- validation or policy-compliance work
- test-related changes that respond to constraints or failures

## Purpose

This skill ensures the plan satisfies both:

- the literal rule or instruction
- the intent behind that rule or instruction

A plan fails this check if it preserves the prohibited behavior through indirection, renaming, wrapping, relocation, delay, suppression, or other forms of tool-only compliance.

## Definition of a Workaround

In a generic sense, a workaround is any approach that circumvents a rule, error, or constraint by manipulating the syntax or execution to silence a check, without addressing the structural or logical root cause. It is an evasion or "band-aid" rather than a true fix. A workaround superficially satisfies constraints but explicitly violates their spirit or intent.

### Characteristics of a Workaround

- **Symptom over root cause:** It patches the immediate error rather than fixing the underlying design flaw.
- **Evasion:** It relies on suppression, arbitrary casting, or wrapping to hide the violation from tools.
- **Mechanical compliance:** It changes the code just enough to satisfy a linter or test without correcting the underlying unsafe or incorrect behavior.
- **Tool-only compliance:** It passes linting, tests, or validation while leaving the real forbidden behavior intact.
- **Semantic equivalence through indirection:** It keeps the same prohibited outcome but routes it through a different alias, helper, layer, or wrapper.

## Difference Between a Workaround and a Staged Fix

A staged fix is acceptable when each stage moves toward the real solution and does not preserve the prohibited behavior.

A workaround is unacceptable when it preserves the bad behavior while hiding, repackaging, renaming, or relocating it.

## Required Review Procedure

When applying this skill, perform the following review in order:

1. Extract the original instruction, rule, or constraint.
1. State the real behavior the instruction is trying to prevent.
1. Review each plan step against both the literal wording and the intent.
1. Ask whether the step changes the structure or logic, or merely hides the violation.
1. Check whether the same prohibited effect still happens through indirection.
1. Identify any plan step that treats the symptom instead of the root cause.
1. Reject the plan if any step preserves the forbidden behavior.

## Intent-Matching Rule

Do not approve a plan simply because it satisfies the text of a rule. Approve it only when it also satisfies the reason the rule exists.

If removing indirection would reveal that the exact same forbidden behavior remains, the plan is a workaround and must be rejected.

## Red Flags

Treat the following as warning signs that require explicit scrutiny:

- suppression comments such as lint disables or rule ignores
- aliasing mutable state to avoid a direct mutation check
- moving unsafe behavior into a thin helper without changing semantics
- broad exception swallowing used to silence failures
- arbitrary casts or loosened typing used only to satisfy a checker
- wrapping forbidden behavior in a differently named function
- shifting the same side effect to another layer without redesigning ownership
- adding indirection that changes appearance but not outcome

### Concrete Example

For example, if a linter requests no mutation of global variables, and the plan proposes to copy the global variable to a local reference and mutate its contents in a way that *still* causes the global variable to mutate, but it passes the linter checks mechanically, it is considered a workaround.

## Rejected and Accepted Examples

### Mutable State

- **Reject:** Alias shared or module-level mutable state and mutate it through the alias.
- **Accept:** Move state ownership into an instance, parameter, return value, or dedicated state owner so the prohibited mutation model no longer exists.

### Type Safety

- **Reject:** Add a cast, loosen a type, or suppress a type error without correcting the data contract.
- **Accept:** Fix the type boundary, input shape, parser, or caller so the data actually matches the required type.

### Error Handling

- **Reject:** Wrap code in a broad catch or except block that only silences the failure.
- **Accept:** Handle the specific failure mode correctly, or change the control flow so the failure is prevented or surfaced intentionally.

### Architecture Boundaries

- **Reject:** Move prohibited logic into another helper, service, singleton, or layer while keeping the same behavior.
- **Accept:** Redesign responsibilities so the logic lives in the correct boundary and the original violation no longer occurs.

### Validation and Security

- **Reject:** Bypass validation or authorization checks indirectly while keeping the same unsafe path.
- **Accept:** Change the data flow or permissions model so valid inputs and authorized access are enforced structurally.

## Scope-Boundary Shell Games

Be especially careful when a plan appears to fix a violation by moving it across boundaries rather than resolving it.

Common examples:

- moving mutable module logic into a singleton without changing semantics
- shifting prohibited business logic from one layer to another only to satisfy an architectural rule
- wrapping blocking or unsafe operations in a thin helper while still invoking them from the same forbidden context

## Root-Cause Requirement

Every approved plan must explicitly identify the root cause.

At minimum, the plan should make clear:

- what is structurally wrong
- why the rule or failure occurred
- what design or logic change removes the need for the violating behavior

If the plan cannot name the root cause, treat that as evidence that it may be a workaround.

## Questions to Ask Before Approval

Before approving a plan, answer these questions:

- Does this plan remove the prohibited behavior or merely rename or repackage it?
- Is the constraint satisfied semantically, or only syntactically?
- Would the same violation still exist if the indirection were removed?
- Does the plan reduce technical debt, or only hide it?
- Would a human reviewer say the intent of the instruction was respected?

If the answers point to concealment rather than correction, reject the plan.

## Partial-Plan Handling

If only one step in a plan is workaround-like, reject the plan as written.

When rejecting it:

- identify the offending step clearly
- preserve the acceptable steps only if they still make sense after revision
- require the invalid step to be replaced with a structural fix

Do not silently approve the rest of the plan while leaving the workaround step ambiguous.

## Required Verdict Format

Return the review result in this structure:

- **Verdict:** `Accept` or `Reject`
- **Protected Constraint:** the instruction, rule, or behavior being protected
- **Problematic Step(s):** the specific plan step or steps at issue
- **Reasoning:** why the plan is or is not a workaround
- **Required Structural Fix:** what kind of real fix is needed instead, if rejected

## Approval Standard

Approve only if the plan removes or redesigns the underlying prohibited behavior rather than hiding, relocating, delaying, or renaming it.

## Rule

1. First, generate the modification plan.
1. Then, apply this skill to review the plan against the original constraints and their intent.
1. If any step in the plan proposes a workaround, **the plan must be rejected** and revised to provide a proper structural fix.
