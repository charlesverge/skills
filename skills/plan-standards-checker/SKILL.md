---
name: plan-standards-checker
description: Checks whether a modification plan or change request follows project standards and, when project standards are absent for the topic, applicable industry standards. Rejects non-compliant plans, cites the violated standard, and records reusable industry-standard research in the repository root `docs/research/`.
---

# Plan Standards Checker

Use this skill when reviewing, validating, or finalizing a modification plan or change request. This skill validates plan text and change requests, not implementation code or completed code changes.

## When to use this skill

- Use this skill after scope validation from `plan-rules` or a relevant `plan-validator-*` skill.
- Use this skill before finalizing a plan or change request.
- Use `change-request` when the user needs a formal change request rather than direct plan edits.
- Use `ask-a-question` when standards conflict, required intent is missing, or no authoritative standard resolves the issue.

## Standards precedence order

When standards differ, apply them in this order. Higher items win over lower items:

1. explicit user request
1. repository root `AGENTS.md`
1. relevant local `SKILL.md` rules
1. plan-specific templates or rules
1. established codebase conventions
1. industry standards

Industry standards apply only when the higher-precedence project sources do not define the topic.

## Validation Process

1. **Confirm scope**: Validate the proposed plan or change request text. Do not drift into code review or implementation review.
1. **Identify project standards**: Look for applicable requirements using precedence items 1-5.
1. **Use industry standards when project standards are absent**:
   - Check the repository root `docs/research/index.md` for previously documented research.
   - If the topic is not already documented, search the web for authoritative sources.
   - Prefer official specs, language or framework documentation, security standards bodies, vendor documentation, and recognized references such as RFCs, OWASP, WCAG, and PEPs.
   - Do not treat blogs, forum posts, or AI-generated summaries as authoritative unless they directly cite and help interpret a primary source.
   - Save new research in the repository root `docs/research/` using the format from `skills/plan-standards-checker/resources/research-template.md`.
   - Update the repository root `docs/research/index.md` after creating or revising research.
1. **Compare plan vs standards**: Evaluate the plan against the highest-precedence applicable standard.
1. **Approve or reject**: Reject plans that violate the applicable standard and require a compliant plan change.

## Research file naming

- Save reusable research in the repository root `docs/research/`.
- Use stable kebab-case filenames that describe the standard topic, for example:
  - `rest-api-error-handling.md`
  - `python-typing-expectations.md`
  - `frontend-accessibility-wcag.md`
- If a version is essential, append it to the filename, for example `wcag-2-2-accessibility.md`.
- Reuse and update the existing topic file instead of creating near-duplicate files for the same standard.

## Ambiguity handling

If project standards are unclear and industry sources conflict:

1. record the conflicting standards in the research note
1. identify the stronger source using the precedence order and authority of the source
1. use `ask-a-question` when the conflict cannot be resolved confidently
1. do not guess, average, or silently choose a weaker source

## Required rejection output

When the plan is rejected, respond using this structure:

- `Decision`: `Rejected`
- `Violated standard`: name of the standard or rule
- `Standard source`: project or industry source, with the file path or URL/reference name
- `Why it conflicts`: specific conflict between the plan and the standard
- `Required plan change`: the single change needed for compliance
- `Research reused/new`: whether existing repo-root research was reused or new research was added

## Rules

- **Validate plans, not implementations**: This skill evaluates plan text and change requests only.
- **Do Not Compromise on Standards**: A plan must not proceed if it fundamentally violates the applicable standard unless a higher-precedence project instruction explicitly allows an exception.
- **Cite the Standard**: When rejecting, clearly state the governing standard and whether it is project-specific or industry-wide.
- **Use the strongest applicable source**: Lower-precedence or less-authoritative sources must not override higher-precedence requirements.
