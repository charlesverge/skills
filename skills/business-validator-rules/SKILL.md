---
name: business-validator-rules
description: Create and validate project business-rule documentation before implementation plans are saved or finalized. Use when defining or reviewing plans/rules/TERMS.md, plans/rules/AREAS.md, files containing related groups of business rules, individual rule labels and descriptions, rule relationships, rule dependencies, rule-group size limits, and implementation-plan references to business rules.
---

# Business Rules Validator

Use this skill to create or validate the project's business-rule catalog. Treat validation as a gate: revise invalid rule documentation before using it in implementation plans.

## Core rules

1. Use [BUSINESS_RULE_TEMPLATE.md](references/BUSINESS_RULE_TEMPLATE.md) as the authoritative format for every business-rule group file.
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
    │   └── {rule-group}.md
    └── {rule-area}/
        └── {rule-group}.md
```

- Store canonical domain vocabulary in `TERMS.md`.
- Store the complete flat taxonomy of rule areas in `AREAS.md`.
- Store globally applicable rules in `general/`.
- Store each group of related rules in the one area directory registered for it in `AREAS.md`.
- Use one human-readable, kebab-case directory segment for each area.
- Reject nested area directories. If the domain needs multiple taxonomy levels, record a question or recommend splitting it into separate projects and documenting the cross-project hierarchy outside `plans/rules/`.

## Rule groups

- Treat each business-rule file as a group of closely related individual rules, not as one rule.
- Give the file a human-readable, kebab-case name that describes the group.
- Include between 1 and 15 individual rules in one rule-group file.
- Write each individual rule as a one-to-five-sentence description of one testable business constraint.
- Give every individual rule its own unique label, `Related to` field, and `Depends on` field.
- If a group would exceed 15 individual rules, divide it into coherent rule groups and create a separate business-rule file from the same template for each group.
- Keep split rule-group files in the same flat rule-area directory unless they belong to different registered areas. Do not create nested directories for the split.
- Preserve cross-file relationships by referencing exact rule labels and file paths after a rule group is split.

## Rule identity

Label every rule `{rule-area}-{rule-group}-{rule-label}`.

- Build the label from three nonempty kebab-case components. A component may contain multiple words, so validate the components against the rule area, rule group, and individual rule entry instead of counting hyphens.
- Use `general` as the area segment for rules in `plans/rules/general/`.
- Make the rule-group component match the rule group's kebab-case file name without the `.md` extension.
- Make the full label unique across the entire project.
- Keep the label stable after implementation plans reference it. If the rule's meaning changes substantially, create a new rule and update affected references explicitly.
- Use the exact rule label in its individual rule entry and beside every corresponding entry in the rule-group file's `Implementation plans` list.

Example: `onboarding-locations-supported-city` in the `locations` rule group at `plans/rules/onboarding/locations.md`.

## Rule relationships

- `Related to` identifies rules that concern adjacent behavior but are not prerequisites.
- `Depends on` identifies rules whose definitions or constraints must be established first.
- Reference related and prerequisite rules by their unique labels and exact file paths.
- Use `None` when no relationship exists.
- Reject self-references, unknown labels, duplicate references, and circular dependency chains.
- Do not treat a related rule as a prerequisite unless its outcome must exist first.

## Validation workflow

1. Restate the requested business outcome in one sentence.
1. Read `plans/rules/TERMS.md`, `plans/rules/AREAS.md`, all rule-group files referenced by the draft, and all implementation plans listed by the draft.
1. Confirm every important domain word, actor, role, object, and lifecycle term uses the canonical vocabulary in `TERMS.md`.
1. Confirm the group's rule area exists in `AREAS.md`, matches every rule label in the group, and matches the rule-group file's directory.
1. Confirm `AREAS.md` is flat, exhaustive for the current rule catalog, human-focused, and free of overlapping area names.
1. Count the individual rules. Require 1 to 15 rules; split a group with more than 15 rules into separate rule-group files before finalizing.
1. Confirm each rule description contains one to five sentences and expresses one business constraint.
1. Confirm every rule label is the ordered concatenation of its rule area, rule group, and individual rule label components and is unique project-wide.
1. Validate every individual rule's `Related to` and `Depends on` references, including dependency ordering and cycle checks.
1. Compare the group's goal, use cases, scope, assumptions, and individual rules for contradictions or missing cases.
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

- Keep each individual rule to one to five sentences.
- Cover one business constraint per individual rule. Split compound constraints into separately labeled rules.
- State each business constraint with `must`, `must not`, `only`, or another testable normative phrase.
- Identify the actor, trigger or condition, allowed or required outcome, and important boundary cases in the individual rule description.
- Reject vague qualifiers such as `usually`, `where appropriate`, `might`, `possibly`, or `etc.` when they affect enforceability.
- Keep technology choices out of the normative rule unless the technology itself is a business requirement.
- Ensure assumptions do not silently weaken or contradict the rule.
- Ensure out-of-scope statements do not exclude behavior required to satisfy the goal.

## Implementation-plan references

Use this exact form in each rule-group file:

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
- Every rule-group file uses the required template and contains 1 to 15 closely related individual rules.
- Every individual rule is one to five sentences and has a unique label built from the three required components.
- Every relationship resolves to a known rule and dependency links are acyclic.
- Every implementation-plan reference is reciprocal and uses the exact rule label.
- Every individual rule is declarative and testable, and the group is internally consistent and aligned with the user's request.
- Unrequested work appears only in `Suggested Improvements`, `Questions`, or `Future features`, as appropriate.

## Final confirmation

Before saving or finalizing, confirm internally that the review gate passes. Report exact file paths and rule labels for every failure so the author can correct them directly.
