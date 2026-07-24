---
name: github-operations
description: Use GitHub safely for repository inspection, branch management, commits, pushes, and ready-for-review pull requests without using GitHub Actions to modify repository files.
---

# GitHub Operations

Use this skill whenever work requires GitHub repository inspection, branch management, commits, pushes, or pull-request creation.

## Non-negotiable rules

1. Never create a draft pull request.
1. Never convert a pull request to draft.
1. Never use GitHub Actions, workflow dispatches, workflow scripts, workflow artifacts, or bot-triggered workflows to create, update, delete, move, or generate repository files.
1. Repository file changes must be made through the active workspace, normal Git commands, or direct GitHub repository file APIs exposed by the GitHub plugin.
1. Pull requests must be opened as ready for review.

## Fast availability checks

### GitHub plugin

The quickest check is to inspect the currently exposed tools:

- If a callable tool such as `GitHub.create_pull_request`, `GitHub.get_repo`, or `GitHub.get_profile` is present, the GitHub plugin is available.
- Do not perform an extra network probe when the callable GitHub namespace is already visible.
- When tool exposure is unclear, call `GitHub.get_profile`. A successful authenticated profile response confirms that the plugin is connected and usable.

### GitHub CLI

Check the executable and authentication together:

```bash
command -v gh >/dev/null 2>&1 && gh auth status
```

Treat `gh` as available for PR creation only when both checks succeed.

## Pull-request tool selection

Use the first matching path:

1. If `gh` is installed and authenticated, open the pull request with `gh pr create`.
1. Otherwise, if the GitHub plugin is available, open the pull request with `GitHub.create_pull_request`.
1. If neither path is available, stop and report that the pull request could not be opened. Do not substitute GitHub Actions or browser automation.

## Required PR settings

### With `gh`

Use a command equivalent to:

```bash
gh pr create --base "<base-branch>" --head "<head-branch>" --title "<title>" --body-file "<body-file>"
```

Requirements:

- Do not pass `--draft`.
- Confirm the head branch is pushed before opening the PR.
- Use a body file rather than a large inline shell string.
- After creation, verify the PR is open and not a draft with `gh pr view`.

### With the GitHub plugin

Call `GitHub.create_pull_request` with:

- the exact repository name,
- the intended head and base branches,
- the final title and body,
- `draft: false`.

After creation, inspect the returned PR state or call `GitHub.get_pr_info` and confirm the pull request is open and ready for review.

## Repository-change workflow

1. Resolve the repository, default branch, and current branch.
1. Inspect repository-specific instructions before editing.
1. Make the requested file changes directly in the workspace or through explicit GitHub plugin file operations.
1. Validate the changed files using repository-provided tooling.
1. Review the diff and confirm that no workflow was used to modify files.
1. Commit the intended changes.
1. Push the branch using normal Git transport when working locally.
1. Open a non-draft pull request using the tool-selection rules above.
1. Verify the PR is ready for review and report its URL.

## Prohibited patterns

Do not:

- create draft PRs,
- pass `--draft` to `gh pr create`,
- set `draft: true` through the plugin,
- call `GitHub.convert_pull_request_to_draft`,
- add or modify a workflow whose purpose is to edit repository contents,
- dispatch an Action to apply patches, generate files, commit changes, or push a branch,
- use workflow artifacts as an indirect file-modification channel,
- claim the plugin or CLI is available without checking tool exposure or authentication.

## Completion report

Report:

- the pull-request URL.
