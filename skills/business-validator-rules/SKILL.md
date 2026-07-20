---
name: business-validator-rules
description: Create and validate project business-rule documentation before implementation plans are saved or finalized. Use when defining or reviewing plans/rules/TERMS.md, plans/rules/AREAS.md, area-specific or general business rules, rule labels, rule relationships, rule dependencies, and implementation-plan references to business rules.
---

# Business Rules Validator

Use this skill to create or validate the project's business-rule catalog. Treat validation as a gate: revise invalid rule documentation before using it in implementation plans.

## Core rules

1. Use [BUSINESS_RULE_TEMPLATE.md](references/BUSINESS_RULE_TEMPLATE.md) as the authoritative format for every individual rule file.
1. Use [TERMS_TEMPLATE.md](references/TERMS_TEMPLATE.md) to create or validate `plans/rules/TERMS.md`.
1. Use [AREAS_TEMPLATE.md](references/AREAS_TEMPLATE.md) to create or validate `plans/rules/AREAS.md`.
1. Base business rules on the user's requirements and authoritative documentation, not on incidental current-code behavior.
1. Write declarative target-state rules. Do not write implementation instructions as business rules.
1. Fill every required template field. Use `None` only where the template permits it.

## Required directory structure

```text
plans/
└── rules/
    ├── TERMS.md
    ├── AREAS.md
    ├── general/
    │   └── {rule-name}.md
    └── {rule-area}/
        └── {rule-name}.md
```

- Store canonical domain vocabulary in `TERMS.md`.
- Store the complete flat taxonomy of rule areas in `AREAS.md`.
- Store globally applicable rules in `general/`.
- Store every other rule in the one area directory registered for it in `AREAS.md`.
- Use one human-readable, kebab-case directory segment for each area.
- Reject nested area directories. If the domain needs multiple taxonomy levels, record a question or recommend splitting it into separate projects and documenting the cross-project hierarchy outside `plans/rules/`.

## Rule identity

Label every rule `{rule-area}-{rule-subsection}-{rule-label}`.

- Build the label from three nonempty kebab-case components. A component may contain multiple words, so validate the components against the `Rule summary` fields instead of counting hyphens.
- Use `general` as the area segment for rules in `plans/rules/general/`.
- Choose a meaningful subsection even when the area has no directory-level subdivisions.
- Make the full label unique across the entire project.
- Keep the label stable after implementation plans reference it. If the rule's meaning changes substantially, create a new rule and update affected references explicitly.
- Use the exact rule label in the rule file and beside every entry in its `Implementation plans` list.

Example: `onboarding-location-supported-city` in `plans/rules/onboarding/supported-city.md`.

## Rule relationships

- `Related to` identifies rules that concern adjacent behavior but are not prerequisites.
- `Depends on` identifies rules whose definitions or constraints must be established first.
- Reference related and prerequisite rules by their unique labels and exact file paths.
- Use `None` when no relationship exists.
- Reject self-references, unknown labels, duplicate references, and circular dependency chains.
- Do not treat a related rule as a prerequisite unless its outcome must exist first.

## Validation workflow

1. Restate the requested business outcome in one sentence.
1. Read `plans/rules/TERMS.md`, `plans/rules/AREAS.md`, all rule files referenced by the draft, and all implementation plans listed by the draft.
1. Confirm every important domain word, actor, role, object, and lifecycle term uses the canonical vocabulary in `TERMS.md`.
1. Confirm the rule area exists in `AREAS.md`, matches the rule label, and matches the rule file's directory.
1. Confirm `AREAS.md` is flat, exhaustive for the current rule catalog, human-focused, and free of overlapping area names.
1. Confirm the rule label is the ordered concatenation of its three meaningful kebab-case components and is unique project-wide.
1. Validate every `Related to` and `Depends on` reference, including dependency ordering and cycle checks.
1. Compare the rule's goal, use cases, scope, assumptions, and normative statement for contradictions or missing cases.
1. Confirm each implementation-plan entry uses an exact plan file path and the exact rule label.
1. Confirm every listed implementation plan exists and references the rule label; report missing reciprocal references.
1. Move useful but unrequested ideas to `Suggested Improvements`, unresolved requirements to `Questions`, and explicitly deferred work to `Future features`.
1. Run the internal review gate and finalize only when every check passes.

## Terms checks

- Define one canonical term for each distinct concept.
- Distinguish often-confused concepts such as account versus profile and user versus administrator.
- Define stakeholder roles by permissions or responsibilities, not by vague audience labels.
- List discouraged synonyms so rule authors do not introduce parallel vocabulary.
- Detect two terms with materially identical meanings and require one canonical term.
- Detect one term used for materially different meanings and require distinct canonical terms.

## Area checks

- Model areas around concepts people recognize in the product or business flow, such as `auth`, `onboarding`, `account`, `permissions`, or `admin-portal`.
- Keep areas at one consistent level of abstraction.
- Reject area names that merely repeat a technical layer, code package, class, database collection, or endpoint unless that is also the human-recognized domain area.
- Reject parent-child entries in the same taxonomy, such as both `settings` and `settings-notifications`.
- Require every non-general rule directory to have exactly one matching `AREAS.md` entry.

## Rule quality checks

- State the business constraint with `must`, `must not`, `only`, or another testable normative phrase.
- Identify the actor, trigger or condition, allowed or required outcome, and important boundary cases.
- Reject vague qualifiers such as `usually`, `where appropriate`, `might`, `possibly`, or `etc.` when they affect enforceability.
- Keep technology choices out of the normative rule unless the technology itself is a business requirement.
- Ensure assumptions do not silently weaken or contradict the rule.
- Ensure out-of-scope statements do not exclude behavior required to satisfy the goal.

## Implementation-plan references

Use this exact form in each rule file:

```markdown
## Implementation plans

- `plans/api/onboarding-location.md` - `onboarding-location-supported-city`
- `plans/frontend/onboarding-location.md` - `onboarding-location-supported-city`
```

- List only plan files that implement or enforce the rule.
- Use `None` when the rule has no implementation plan yet.
- Do not put source-code paths in this section.

## Internal review gate

Do not add this gate as a section in rule documents.

- The directory structure matches the required structure.
- `TERMS.md` contains unambiguous canonical vocabulary.
- `AREAS.md` contains one flat, human-focused taxonomy.
- Every rule uses the required template and a unique label built from the three required components.
- Every relationship resolves to a known rule and dependency links are acyclic.
- Every implementation-plan reference is reciprocal and uses the exact rule label.
- The rule is declarative, testable, internally consistent, and aligned with the user's request.
- Unrequested work appears only in `Suggested Improvements`, `Questions`, or `Future features`, as appropriate.

## Final confirmation

Before saving or finalizing, confirm internally that the review gate passes. Report exact file paths and rule labels for every failure so the author can correct them directly.
