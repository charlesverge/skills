---
name: plan-validator-frontend
description: Validate draft plans for frontend user-facing features (UI components, pages, screens, interactions) before they are saved, finalized, or handed to implementation. Use when checking a plan for original-intent alignment, unasked features, scope creep, fallback-rule violations, banned recovery language, feature-flag wording, plan structure, concrete feature build details, defined UI states (loading, success, error, empty, disabled), accessibility coverage, mockup reconciliation, API-consumption details, rule compliance, test-convention compliance, and required interaction/component test details.
---

## Core rules

1. This skill is the authoritative validator for frontend user-facing feature plans. Use it to validate that a plan meets the user's original request, follows all rules, and is ready for implementation.
1. The authoritative template located in `.agents/skills/plan-validator-frontend/references/PLAN_FRONTEND_TEMPLATE.md` is the authoritative required plan format. Use it to check that the plan includes all required sections, and that each section is filled with concrete details rather than placeholders.
1. Do not base the validation of the format on the existing plan content or surrounding plans or code. Do not add, remove, or rewrite a section, heading, or title to match other plans or code. Format conformance is judged
   only against the authoritative template, never against sibling files.
1. Plan generation is based on the plan content, not the code content. Code is generated from the plan not the other way around, so the plan must be complete and specific on its own.
1. Apply the `test-conventions` skill to every test plan or rule group, test helper file, and test file split described by the plan. Treat `test-conventions` as authoritative for test organization.

## Validation Workflow

1. Restate the user's original intent in one sentence.
1. Compare every planned task to that intent.
1. Move unrequested features, speculative improvements, broad refactors, and extra compatibility work out of implementation steps unless the user explicitly asked for them into the Suggested Improvements section or Questions.
1. Run the hard-stop fallback checklist.
1. Check the plan format and required sections out lined in the template `.agents/skills/plan-validator-frontend/references/PLAN_FRONTEND_TEMPLATE.md`.
1. Verify the `Implementation plan` section names exact files and covers the components, hooks, stores, styles, types, and resources each file must contain for this feature.
1. Verify the plan covers exactly one action or rendered state, and that the other related states (loading, error, empty, etc.) are referenced as sibling plans rather than inlined.
1. Verify the single state this plan implements is fully specified and its accessibility is addressed.
1. Verify each consumed API is named and linked to its `plans/api/{endpoint}.md` plan.
1. Ensure there is no extra sections or fields in the plan that are not in the template.
1. Verify the plan is reconciled against the referenced mockup.
1. Check rule compliance against any active repo, user, developer, or skill instructions.
1. Apply `test-conventions` and verify the `Test coverage` section is specific enough to execute.
1. Finalize only after all required confirmations are true.

# Frontend plan Validator for features that are user facing

1. Use this skill before saving or finalizing a plan for a frontend user facing feature like a UI component, page, or interaction. Treat validation as a gate: if the plan fails any hard-stop check, revise the plan before proceeding.
1. Feature plans must follow the structure in `.agents/skills/plan-validator-frontend/references/PLAN_FRONTEND_TEMPLATE.md` and cover exactly one user-facing action or rendered state (loading, success, error, empty, disabled). Related states must be implemented in sibling plans and referenced, not inlined.
1. Only the sections outlined in `.agents/skills/plan-validator-frontend/references/PLAN_FRONTEND_TEMPLATE.md` are allowed.
1. If there is an extra section merge it into the closest relevant section or move it to `Suggested Improvements` if it is a useful but unrequested addition. Do not leave extra sections in the plan.
1. Generate any missing required section content or details before finalizing. Do not leave template placeholders or vague language in the plan.

## Single-Action Scope

A plan addresses a single action or a single rendered screen state, not a whole feature with all of its states.

Each distinct rendered state the user sees is its own plan. For example, a plan to load and render a previously saved favorites list (the user clicks a company in the favorites list and the loaded list view renders) is one plan. The loading screen, the load-error screen, and the empty/no-results screen are each separate plans:

- `plans/features/favorites-load.md` — the happy-path loaded view and the API call that populates it
- `plans/features/favorites-loading.md` — the loading screen
- `plans/features/favorites-load-error.md` — the error screen
- `plans/features/favorites-no-results.md` — the empty screen

The plan under review defines only the one state or action it is responsible for. It must reference the sibling plans where the other states are implemented (in `Depends on` when there is an ordering dependency, otherwise under `Technical references` → `Related features`). If a related state plan does not exist yet, list it in `Questions`. Do not inline multiple states or actions into one plan, and do not claim every state is defined inside a single plan.

### Example: splitting one request into sibling plans

A request like "show the user's saved favorite companies when they open the favorites tab" is not one plan. Split it by rendered state, one plan per rendering, and let each plan own only its files and tests:

- `plans/features/favorites-loading.md`
  - Owns: the loading/skeleton screen shown while the list request is in flight.
  - Key files: `FavoritesList.tsx` loading branch, `FavoritesSkeleton.tsx`.
- `plans/features/favorites-load.md`
  - Owns: the loaded list view rendered from a successful response.
  - Key files: `FavoritesList.tsx` loaded branch, `FavoriteCard.tsx`.
- `plans/features/favorites-load-error.md`
  - Owns: the error screen shown when the request fails.
  - Key files: `FavoritesList.tsx` error branch, `FavoritesError.tsx`.
- `plans/features/favorites-no-results.md`
  - Owns: the empty screen shown when the user has no favorites.
  - Key files: `FavoritesList.tsx` empty branch, `FavoritesEmpty.tsx`.

Each plan references the others under `Related features`. The `favorites-load.md` plan owns the GET call and the loaded view; it links the loading, error, and empty siblings rather than defining their screens.

## Future additions vs Suggested Improvements vs Questions

- Future additions are additions that the user has decided to be located in that section, they are not to be moved to suggested improvements or questions.
- Suggested improvements are useful but unrequested ideas that may still be worth doing, but are not required to satisfy the user's original request. They should be moved to the `Suggested Improvements` section.
- Questions are uncertain scope or requirement decisions that need to be clarified with the user before implementation.

## Hard-Stop Fallback Checklist

Fallback behavior is banned unless the user explicitly requests it using the word `fallback` or clearly describes automatic recovery to an alternate path.

Before writing, saving, or finalizing a plan, scan the proposed plan for:

- `fallback`
- `fall back`
- `fallback path`
- `backup path`
- `alternate path on failure`
- `retry with old behavior`
- `recovery path`
- `compatibility path`
- `graceful degradation`
- `if new path fails, use old path`

If any of these appear and the user did not explicitly request fallback behavior, stop and remove the fallback behavior or wording before continuing.

Feature flags are not fallbacks. A feature flag may define:

- enabled path
- disabled path

A feature flag must not define:

- automatic fallback from enabled path to disabled path
- fallback on error
- recovery to old behavior

When a user says `feature flag`, use only `enabled path` and `disabled path`. Never use `fallback` to describe either path.

Hard stop if the plan does not follow the required template format `.agents/skills/plan-validator-frontend/references/PLAN_FRONTEND_TEMPLATE.md`.

## Required Plan Format

Use the plan structure in `.agents/skills/plan-validator-frontend/references/PLAN_FRONTEND_TEMPLATE.md`.

### How to use the template

1. Create a feature short code.
   - **Feature short code:** \[Feature category-subcategory-action or feature name. For example, `auth-signin-email` or `favorites-company-add`]
1. Fill out every section. If a section does not apply, write `N/A` or `None`.
1. Save the feature plan as `plans/features/{feature-short-code}.md`.
1. Keep the plan screen and interaction-first, and scoped to a single action or rendered state. Document the visible elements, user triggers, and the one state this plan owns before internal implementation notes; reference the sibling plans that own the other states (loading, error, empty). Consume APIs by linking to `plans/api/{endpoint}.md`; do not define database writes here.
1. If the component or screen is generic and reused across multiple screens or purposes, document:
   - how callers select the rendered behavior or variant
   - which prop, route segment, or selector controls the behavior
   - which component, hook, or function is responsible for each behavior
   - any constraints that keep the component consistent across those uses (shared state, styling, accessibility)

## Internal Plan Review Gate

Use this gate to validate the plan internally. Do not add a `Plan review gate` section to the plan unless the template includes one.

- No fallback behavior is present.
- No fallback language remains.
- Feature flags are described only as enabled and disabled paths.
- The plan follows the original intent.
- Unasked features are placed in `Suggested Improvements` or `Questions`.
- Implementation plan lists exact files, components, hooks, stores, variables, styles, and reasons.
- Every test path, filename, plan or rule comment, helper, and file split follows `test-conventions`.
- The plan covers a single action or rendered state; related states are referenced as sibling plans, not inlined.
- The one state this plan implements is fully specified, accessibility is addressed, and the plan is reconciled against the referenced mockup.
- The template is a hard requirement (exhaustive section list, mandatory, fields/order)
- Plans are declarative target-state descriptions (no change-request verbs).

## Plan Checks

### Intent Alignment

- Confirm the plan solves the user's stated request, not a broader inferred project goal.
- Mark each implementation step as `requested`, `required to satisfy request`, `suggested improvement`, `question`, or `remove`.
- Keep only `requested` and `required to satisfy request` items in implementation steps.
- Move useful but unrequested ideas to `Suggested Improvements`.
- Move uncertain scope or requirement decisions to `Questions`.
- Remove items that are neither useful follow-ups nor valid questions.
- If a step depends on an assumption, state the assumption and keep only the best direct path.

### Scope Creep

Reject plan items that introduce:

- more than one action or rendered state in a single plan (each state belongs in its own plan; reference siblings instead)
- extra screens, components, or views the user did not ask for
- unrequested UI states, animations, transitions, theming, or responsive breakpoints
- accessibility work beyond the baseline the request implies (where it expands scope rather than meeting it)
- generalized component frameworks or design-system abstractions for a narrow feature
- unrelated cleanup or refactors
- compatibility layers not required by the request
- feature flags, client-side telemetry, analytics events, retries, or operational flows not requested or required

When a rejected item may still be useful later, relocate it to `Suggested Improvements`. When an item depends on missing user intent or unclear requirements, relocate it to `Questions`. Do not leave rejected or out-of-scope items in `Implementation plan`.

### Rule Compliance

Check the plan against all active instructions and project rules. Call out violations explicitly and revise the plan. Common failures include:

- banned fallback behavior or language
- tests described vaguely instead of by file and test name
- implementation steps without target files or components
- implementation-plan entries without exact files, covered components, hooks, stores, variables, styles, or reasons
- multiple actions or rendered states bundled into one plan instead of split into single-action plans
- related states (loading, error, empty) neither referenced as sibling plans nor raised in `Questions`
- missing accessibility coverage (keyboard, focus, labels, screen reader) for the state this plan implements
- consumed APIs that are not linked to a `plans/api/{endpoint}.md` plan
- optional alternatives where the user asked for a concrete path
- planned work that contradicts existing codebase patterns
- skipped validation without stating why it cannot run

## Implementation plan Section Requirements

The plan must include one `Implementation plan` section. Use this section as the canonical place for concrete file-level implementation details.

Each entry must start with the exact file path and then list the concrete feature work inside that file. Cover every relevant component, hook, store, function, variable, style, and resource in the file entry instead of using those as separate top-level subsections.

For each file entry, include:

- The exact file path
- exact component, hook, store, function, prop, variable, style, or resource name
- Short description of the component, hook, store, function, prop, variable, style, or resource

Configuration or feature flags should have a exact variable or setting. For example, do not write "add a config flag to settings". Write the concrete target, such as `src/config/features.ts::FEATURE_NAME_ENABLED`, and explain why it is needed.

Use this format:

This example is the `Implementation plan` for the single sibling plan `plans/features/favorites-load.md` (the loaded list view only); the loading, error, and empty renderings are owned by their own sibling plans.

```markdown
## Implementation plan

- src/features/favorites/components/FavoritesList.tsx`
  - `FavoriteCard` items from a successful `useFavorites` response.
  - Reason: renders the happy-path loaded view this plan owns.
- src/config/config.yml 
  - `FEATURE_FAVORITES_ENABLED = true`
  - Reason: enables the favorites feature flag for this plan's loaded view.
- src/features/favorites/constants.ts
  - `FAVORITES_API_ENDPOINT = '/api/favorites'`
  - Reason: centralizes the API endpoint this plan's `useFavorites` hook consumes.

```

If any target file is already above 500 lines, or the plan would push it above 500 lines, treat that as a design warning. Prefer splitting work into subfeatures using `src/features/{feature name}/{sub feature}` organization, with separate files for components, hooks, stores, types, styles, and a supporting resources directory for static assets. If the plan still places the feature in the large file directly, it must explain why that is the best direct path.

## Test coverage Section Requirements

The plan must include a Test coverage section even when no tests are required.

Load and apply the `test-conventions` skill before accepting this section.

- Tests must cover the single state or action this plan implements: its render, the user interactions that belong to it, its edge cases, and regression cases.
- Tests must include component/render tests for the rendered state this plan owns and interaction tests for every user trigger it handles (click, submit, toggle, keyboard).
- Tests must include accessibility assertions (roles, labels, focus order, keyboard operability) for the interactive elements in this plan.
- When the plan consumes an API, the API must be mocked at the network boundary so the state this plan owns is exercised against the relevant response. End-to-end flows that hit a real backend must use a staging or sandbox environment.
- End-to-end tests must be included for the user-facing behavior this plan implements, even when component and interaction tests are present.
- Every row in the plan's `Error codes` table must have a corresponding `Test coverage` entry that asserts the user-facing error state for that code, or an explicit concrete reason it cannot be tested. Error-state tests must not be relocated to `Suggested Improvements`.
- The `Test coverage` section must describe the tests that should exist for the completed plan. Do not use change-action buckets or change verbs.
- Include test coverage for happy paths, error states, edge cases, and regression cases.
- Derive plan tests from `plans/{plan_dir}/{plan_file}.md`: discard `.md` and use `tests/{plan_dir}/{plan_file}.test.tsx` for component or interaction tests and `tests/{plan_dir}/{plan_file}.spec.ts` for Playwright tests.
- Derive rule tests from `plans/rules/{rule_area}/{rule_group}.md`: discard `.md` and apply the same framework suffix beneath `tests/rules/{rule_area}/`.
- Require every test file to begin with the exact `// Plan:` or `// Rule:` comment required by `test-conventions`.
- Keep every test file at or below 600 lines. Require exact convention-compliant helper and split paths when planned coverage would exceed that limit.
- Keep all automated tests under the top-level `tests/` directory and never intermix them with application source.

For each test case, list in order:

- exact file path
- test name
- short description of what it ensures
- one required coverage category: `Happy path`, `Validation / error path`, `Edge case`, or `Regression case`

Do not accept wildcard, glob, placeholder, or guessed paths. A test entry is invalid if the path contains `*`, `**`, `<...>`, `[...]`, `tests/path/`, `some/path/`, or any placeholder instead of the concrete file where the test will be placed.

Valid format:

```markdown
## Test coverage

- `tests/{plan_dir}/{plan_file}.test.tsx` `renders the completed feature state` Ensures the expected state is visible - Happy path
- `tests/{plan_dir}/{plan_file}.test.tsx` `shows the documented validation message` Ensures invalid input renders the documented error - Validation / error path
- `tests/{plan_dir}/{plan_file}.test.tsx` `handles an empty response without layout breakage` Ensures empty data renders the documented state - Edge case
- `tests/{plan_dir}/{plan_file}.test.tsx` `preserves the existing keyboard interaction` Ensures keyboard behavior remains available - Regression case
- `tests/{plan_dir}/{plan_file}.spec.ts` `completes the documented user flow` Ensures the user-facing behavior works end to end - Happy path
```

## API consumption and client state

When a plan consumes an API or manages client state, check for the following:

1. Plans must name every API call this action makes and link each to its `plans/api/{endpoint}.md` plan (or flag it as not-yet-planned in `Questions`).
1. Plans must define the rendered state this plan owns and the API response that produces it, and reference the sibling plans that own the other response outcomes (loading, error, empty) rather than defining them inline.
1. Plans must specify how server data maps to displayed fields, and whether updates are optimistic or wait for the server response.
1. Client-side validation rules must match the consumed API's request contract so the UI rejects the same inputs the API would.
1. Each consumed API must have component/interaction tests that mock it at the network boundary and exercise the state this plan owns against its corresponding response.

## Frontend Section Requirements

The plan must fill these template sections with concrete, screen-level detail, not placeholders:

- **Success definition** — what must be seen and happen on the screen for this single action or state to be considered successful.
- **Use cases** — describes what the user does to reach this state and the expected on-screen outcome for it.
- **Input state before action** and **Output state after action** — concrete required states, not "logged in" or "has access". For example, "user must have at least one company added to see the favorites tab".
- **UI details** — visible elements (buttons, links, fields, cards, menus, labels) for this state, the state itself, and accessibility notes (keyboard behavior, labels, focus, screen reader). Reference the sibling plans that own the other states (loading, error, empty) instead of defining them here.
- **Mockups** — the mockup file is referenced and the plan is reconciled against it, with any mismatch or ambiguity called out.
- **Api routes** — every API this action calls is listed and linked to its `plans/api/{endpoint}.md` plan, or flagged in `Questions` if not yet planned.

If any of these sections is missing, vague, or left as a template placeholder, revise the plan before finalizing.

## Plan Validator CLI Guard

After writing every plan file created by the task and every plan file changed by the task, run `plan_validator <plan-path>`.
Fix every reported issue. Repeat validation until exit status `0`. Finalize the plan and hand it off only after validation passes.
Installation note: `python3 -m pip install "git+https://github.com/charlesverge-dev-org/coding-tools.git"`.

## Final Confirmation

Before saving or finalizing, verify these confirmations internally. Do not add these confirmations to the plan unless the template includes a section for them:

- no fallback behavior is present
- no fallback language remains
- feature flags are described only as enabled and disabled paths
- the original user intent is followed
- unasked features are placed in `Suggested Improvements` or `Questions`
- implementation plan lists exact files, components, hooks, stores, variables, styles, and reasons
- the plan covers a single action or rendered state, with the other related states referenced as sibling plans (or raised in `Questions`)
- the one state this plan implements is fully specified with the element that renders it
- accessibility is addressed (keyboard, focus, labels, screen reader) for the interactive elements in this plan
- the plan is reconciled against the referenced mockup
- every consumed API is named and linked to its `plans/api/{endpoint}.md` plan
- tests are listed with exact file paths, test names, and descriptions covering this plan's state, its interactions, and accessibility, or a concrete reason is given for no tests
- every test path, filename, plan or rule comment, helper, and file split follows `test-conventions`
- every test file remains at or below 600 lines or has exact convention-compliant split paths
- every error code in the `Error codes` table has a corresponding user-facing error-state test entry or a concrete documented reason
- Verify the plan does not use vague language, it should not have language like "it could be implemented like this", "possibly is", "might", "maybe", etc other vague descriptions. Concrete details are needed. if something is vague locate supporting details to make it certain or add a question clarify.
