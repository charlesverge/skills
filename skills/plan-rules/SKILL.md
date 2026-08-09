---
name: plan-rules
description: Apply plan rules whenever creating any type of plan, including a change request or a plan for a function, class, module, or other work. Use to prevent cross-pollination of functionality and keep unrequested scope expansions in Suggested Improvements.
---

# Plan Rules

Apply these rules whenever creating a plan:

1. Plans are requirement statements and should be written with this in mind. For example, When a feature is removed from an application the feature should removed from the plan and have no reference to it.
1. If a change request is needed use the change-request skill.
1. Do not cross-pollinate functionality. Keep separate responsibilities and their data separate. For example, do not use an authentication system to store user preferences; authentication data and user-preference data are separate.
1. Do not expand scope unless the user explicitly requests the expansion. Put proposed scope expansions under `Suggested Improvements` instead of including them in the planned work.
1. Look for solutions that minimize the changes required, keeping changes to a central location or with in a sub set rather then multiple touch points. There is exceptions, for example type changes which often change multiple files.
1. The fixture should not be autouse across unrelated tests. Narrow it to explicit opt-in where a fixture is required.
1. If a test assert is to be changed require a specific reason, suspect changes are changing of values, success to failure asserts and other unsupported reasons. This change would be required to be associated with a plan or a change request to justify. If it is not present then use ask-a-question skill to request a decision.

## Goals

1. Goals for plans should cover the overall goal of the plan.
1. Goals which cover a group or the entire application should have their own plan. Plans which depend on those plans can reference the plans which cover the group or entire application rather then restating the overarching goals for the group in the plan for a specific module, function, class, action, feature.

## Finishing checks

1. Before finishing check for unneeded changes, ie comment rewording that adds no value. Changing intentionally generic statements into specific statements when specific statements exist else where in the plans.
