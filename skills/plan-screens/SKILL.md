---
name: plan-screens
description: Create and maintain app screen registry files named `01_SCREENS.md` under `plans/*/`. Use when a frontend plan needs a documented screen reference, when adding a new screen, when updating screen names or mockup links, or when the `Screen location` field must match the nearest screen registry such as `plans/features/01_SCREENS.md` or `plans/features/ui-shared/01_SCREENS.md`.
---

# Plan Screens

Use this skill to manage `01_SCREENS.md` files that catalog the screens available in an app for a given plan area.

## File location

1. A screen registry file is always named `01_SCREENS.md`.
1. It may exist in any `plans/*/` directory.
1. Typical locations include:
   - `plans/features/01_SCREENS.md`
   - `plans/ui-shared/01_SCREENS.md`
1. Use the nearest applicable registry for the plan you are writing. Prefer the most specific shared location that matches the screen ownership.

## When to update

1. Create the file if the relevant `plans/*/01_SCREENS.md` does not exist and a frontend plan in that area needs a screen reference.
1. Add a new screen entry when a feature introduces a screen that is not already listed.
1. Update the existing screen entry when the screen name, description, or mockup sources change.
1. Reuse an existing entry when multiple feature plans target the same screen. Do not create duplicate sections for the same screen in one file.

## Relationship to frontend plans

1. The `Screen location` field in the frontend plan template `.agents/skills/plan-validator-frontend/references/PLAN_FRONTEND_TEMPLATE.md` must reference the exact screen name from the applicable `01_SCREENS.md` entry.
1. If the planned work targets a nested area inside that screen, the plan may append the specific modal, section, tab, or component within that screen.
1. If the screen registry and the frontend plan disagree, update the registry first, then align the plan.

## Entry requirements

1. Use the template in `resources/SCREENS_TEMPLATE.md`.
1. Each screen entry must have:
   - `## {Screen name}`
   - `**Description**`: one or two sentences
   - `**Screen short code**`: `snake_case` short code
   - `**Mockups**`: links to repo mockups, Figma, or another source
1. Screen names and short codes are unique.
1. Screen names and short codes should be {Category} {Subcategory} {Action} style, for example `Auth Signin Email` or `Favorites Company Add`.
1. Keep screen names stable and user-facing enough that other plans can reference them directly.
1. Keep mockup links specific enough that a reviewer can open the intended screen without guessing.

## Workflow

1. Determine the frontend plan's directory under `plans/`.
1. Locate the nearest applicable `01_SCREENS.md` file.
1. If it does not exist, create it from `resources/SCREENS_TEMPLATE.md`.
1. Check whether the screen already exists in that file.
1. Add or update the screen entry.
1. Set the frontend plan's `Screen location` field to the exact registered screen name, adding the more specific internal location only when needed.
1. After writing every file created by the task and every plan file changed by the task, run `plan_validator <plan-path>`.

## Example locations

- `plans/features/01_SCREENS.md` for product screens shared across feature plans.
- `plans/ui-shared/01_SCREENS.md` for reusable shared UI screens or shell areas.
