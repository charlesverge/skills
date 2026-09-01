# Plan Standards Checker Evals

This directory contains a baseline eval suite for `plan-standards-checker`.

## What is included

- `change-requests.json` with 25 common, realistic change-request fixtures.
- expected outcomes for each fixture, including whether it should be detected as standards compliant.
- a reusable manual test method for future regression checks.
- `assessment.md` with a human-readable summary matrix.

## Source basis

### Project standards

- repository root `AGENTS.md`
- `skills/plan-rules/SKILL.md`
- `skills/python-type-rules/SKILL.md`
- `skills/plan-standards-checker/SKILL.md`

### Repo-root research reused by the skill

- `docs/research/rest-api-error-handling.md`
- `docs/research/python-typing-expectations.md`
- `docs/research/authentication-and-error-messages.md`

### Web sources gathered for this suite

- [RFC 9110 – HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9457 – Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

### Source acquisition note

Official W3C/WAI WCAG pages returned HTTP 403 to the available fetch tool during this run, so accessibility-specific evals are intentionally omitted from this initial suite rather than being based on weaker unverifiable sources.

## Test method: `manual-skill-review-v1`

1. Open one case from `change-requests.json`.
1. Prompt the agent with the following structure:
   - `Use $plan-standards-checker to evaluate the following change request.`
   - include the full `change_request` text from the case.
   - require the skill's structured response fields:
     - `Decision`
     - `Violated standard`
     - `Standard source`
     - `Why it conflicts`
     - `Required plan change`
     - `Research reused/new`
1. Compare the actual `Decision` and `standards_compliant` judgment to the fixture's `expected_result`.
1. Mark the case as passing when:
   - the decision matches,
   - the compliance boolean matches, and
   - the cited standard source is the same as, or higher precedence than, the fixture's governing source.

## Expected distribution

- 25 total cases
- 9 expected standards-compliant cases
- 16 expected rejected cases

## Notes

- The `actual_skill_assessment` values in the fixtures are baseline assessments produced by applying the current `plan-standards-checker` rules to each case.
- This suite is ready for future automation, but the initial batch is manually curated and reviewed.
