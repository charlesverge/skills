---
name: plan-rules
description: Apply plan rules whenever creating any type of plan, including a change request or a plan for a function, class, module, or other work. Use to prevent cross-pollination of functionality and keep unrequested scope expansions in Suggested Improvements.
---

# Plan Rules

Apply these rules whenever creating a plan:

1. Read the TERMS.md file and use the terms defined in that file.
1. Plans are requirement statements and should be written with this in mind. For example, When a feature is removed from an application the feature should removed from the plan and have no reference to it.
1. If a change request is needed use the change-request skill.
1. Do not cross-pollinate functionality. Keep separate responsibilities and their data separate. For example, do not use an authentication system to store user preferences; authentication data and user-preference data are separate.
1. Do not expand scope unless the user explicitly requests the expansion. Put proposed scope expansions under `Suggested Improvements` instead of including them in the planned work.
1. Look for solutions that minimize the changes required, keeping changes to a central location or with in a sub set rather then multiple touch points. There is exceptions, for example type changes which often change multiple files.
1. The fixture should not be autouse across unrelated tests. Narrow it to explicit opt-in where a fixture is required.
1. If a test assert is to be changed require a specific reason, suspect changes are changing of values, success to failure asserts and other unsupported reasons. This change would be required to be associated with a plan or a change request to justify. If it is not present then use ask-a-question skill to request a decision.
1. Check plan changes to ensure that no statement is duplicated, if needed reference another plan rather then duplicating what is in an existing plan.
1. Use terms defined in the TERMS.md files, do not use variations of those terms when one exists. Goal is to use the same wording when referring to the same thing, concept or action.
1. No wording churn is allowed unless it is needed to bring plans in line with TERMS.md definitions. Do not make changes which are simply rewording of a statement which does not change the meaning.
1. Plans should focus on what should things should be and avoid dictating what it should not be. Plans should be affirmative.
1. Apply description edits at the claim level. When approved functionality changes a stated subject, action, or object, update that exact phrase and retain the remaining wording verbatim.

## Goals

1. Goals for plans should cover the overall goal of the plan.
1. Goals which cover a group or the entire application should have their own plan. Plans which depend on those plans can reference the plans which cover the group or entire application rather then restating the overarching goals for the group in the plan for a specific module, function, class, action, feature.
1. Goal rarely need to be updated once created. Most updates to the are to the plan details rather then the goal. If the goal is truly different then consider a new plan and if the current plan should be removed.

## Examples of needless edits

Changing a statement to another statement that is the same meaning. In the bellow example adding "Adding on " in every environment" is redundant as the original already expresses that. In this case the edit should of never happened.

Original:

```markdown
- `checkStartup()` calls the existing `connectMongo()` once, then checks question readiness and city readiness independently.
```

Changed to:

```markdown
- `checkStartup()` calls the existing `connectMongo()` once, then checks question readiness and city readiness independently in every environment.
```

Restructuring of a statement is considered a needless edit and should not be done

Original:

```markdown
- Production application code reads and writes records in its configured application database.
```

Changed to:

```markdown
- When production application code reads or writes records, it uses its configured application database.
```

## Plan duplicates

1. Review edits and ensure they are not duplicates and they are required. Required classified as related directly to that plan or controlled by that plan.
1. Plans should not explain features that are part of another plan which would qualify as a duplicate.

## Finishing checks

1. Before finishing check for unneeded changes, ie comment rewording that adds no value. Changing intentionally generic statements into specific statements when specific statements exist else where in the plans.
1. Before finishing check for unasked for scope expansions
1. Before finishing check for needless changes to plans that do not add value or duplicated the information or updated a plan that has no feature changes.
1. Before finishing check for needless duplication of information in the plan that is already covered in the plan or a referenced plan.
1. Before finishing check for any wording churn that does not change functionality or meaning of the plan. Wording changes to align with TERMS.md is allowed.
