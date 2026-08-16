---
name: gh-fix-ci
description: Command reference for using the GitHub CLI to inspect pull-request checks and retrieve GitHub Actions run and job logs. Use when investigating failing GitHub Actions checks on a pull request with `gh`.
---

# GitHub Actions CI Commands

## Set repository and pull request values

```bash
repo="OWNER/REPO"
pr="123"
```

Use a pull request URL instead of a number when needed:

```bash
pr="https://github.com/OWNER/REPO/pull/123"
```

## Check authentication

```bash
gh auth status
```

## Resolve the current branch pull request

```bash
gh pr view --repo "$repo" --json number,url,headRefName,headRefOid
```

## List pull request checks

```bash
gh pr checks "$pr" --repo "$repo"
```

```bash
gh pr checks "$pr" --repo "$repo" \
  --json name,state,bucket,link,startedAt,completedAt,workflow
```

List failed checks only:

```bash
gh pr checks "$pr" --repo "$repo" \
  --json name,state,bucket,link,startedAt,completedAt,workflow \
  --jq '.[] | select(.bucket == "fail")'
```

## List Actions runs for the pull request commit

```bash
head_sha="$(gh pr view "$pr" --repo "$repo" --json headRefOid --jq '.headRefOid')"
gh run list --repo "$repo" --commit "$head_sha" \
  --json databaseId,name,workflowName,status,conclusion,url,event,headBranch,headSha,createdAt
```

List failed runs only:

```bash
gh run list --repo "$repo" --commit "$head_sha" --status failure \
  --json databaseId,name,workflowName,status,conclusion,url,event,headBranch,headSha,createdAt
```

## Inspect a run

```bash
run_id="123456789"
gh run view "$run_id" --repo "$repo"
```

```bash
gh run view "$run_id" --repo "$repo" \
  --json databaseId,name,workflowName,status,conclusion,url,event,headBranch,headSha,jobs
```

## Retrieve run logs

Retrieve all logs:

```bash
gh run view "$run_id" --repo "$repo" --log
```

Retrieve logs for failed steps only:

```bash
gh run view "$run_id" --repo "$repo" --log-failed
```

Save all logs as text:

```bash
gh run view "$run_id" --repo "$repo" --log > "run-$run_id.log"
```

Save failed-step logs as text:

```bash
gh run view "$run_id" --repo "$repo" --log-failed > "run-$run_id-failed.log"
```

## List jobs in a run

```bash
gh run view "$run_id" --repo "$repo" --json jobs \
  --jq '.jobs[] | {databaseId, name, status, conclusion, url}'
```

List failed jobs only:

```bash
gh run view "$run_id" --repo "$repo" --json jobs \
  --jq '.jobs[] | select(.conclusion == "failure") | {databaseId, name, status, conclusion, url}'
```

## Retrieve a job log

```bash
job_id="987654321"
gh run view "$run_id" --repo "$repo" --job "$job_id" --log
```

Retrieve failed steps for one job:

```bash
gh run view "$run_id" --repo "$repo" --job "$job_id" --log-failed
```

Save one job log through the Actions API:

```bash
gh api "/repos/$repo/actions/jobs/$job_id/logs" > "job-$job_id.log"
```

## Download a run log archive

```bash
gh api "/repos/$repo/actions/runs/$run_id/logs" > "run-$run_id-logs.zip"
unzip -l "run-$run_id-logs.zip"
unzip "run-$run_id-logs.zip" -d "run-$run_id-logs"
```

## Watch a run

```bash
gh run watch "$run_id" --repo "$repo" --exit-status
```
