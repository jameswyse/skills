# GitHub CLI and API notes

## Primary commands used

### PR metadata

- `gh pr view --json number,url,state,mergedAt,closedAt,headRefName,headRefOid,headRepository,headRepositoryOwner`

Resolves the PR number, URL, branch, head SHA, and whether the PR is closed or merged.

### PR checks summary

- `gh pr checks --json name,state,bucket,link,workflow,event,startedAt,completedAt`

Reports pending, failed, and passed checks, including whether the current CI round has finished.

### Workflow runs for head SHA

- `gh api repos/{owner}/{repo}/actions/runs -X GET -f head_sha=<sha> -f per_page=100`

Finds failed workflow runs and run IDs eligible for retry.

### Failed log inspection

- `gh run view <run-id> --json jobs,name,workflowName,conclusion,status,url,headSha`
- `gh api repos/{owner}/{repo}/actions/runs/{run_id}/jobs -X GET -f per_page=100`
- `gh api repos/{owner}/{repo}/actions/jobs/{job_id}/logs > /tmp/codex-gh-job-{job_id}-logs.zip`
- `gh run view <run-id> --log-failed`

Use job logs to classify failures under [the CI criteria](heuristics.md#ci-failures).
The watcher's `failed_jobs` entries provide each failed job's `job_id` and `logs_endpoint`.
Fetch those logs as soon as the job fails. Use `gh run view --log-failed` as a fallback after
the workflow finishes; it may not return failed-job logs while other jobs are still running.

### Retry failed jobs only

- `gh run rerun <run-id> --failed`

Reruns failed jobs and their dependencies for a workflow run. Use the skill's `--retry-failed-now`
command for babysitting so the watcher records retry usage against the head SHA.

## Review-related endpoints

- Issue comments on PR:
  - `gh api repos/{owner}/{repo}/issues/<pr_number>/comments?per_page=100`
- Inline PR review comments:
  - `gh api repos/{owner}/{repo}/pulls/<pr_number>/comments?per_page=100`
- Review submissions:
  - `gh api repos/{owner}/{repo}/pulls/<pr_number>/reviews?per_page=100`

Use each inline comment's `pull_request_review_id` to find its parent review. Ignore parent reviews
whose `state` is `PENDING`, along with their inline comments, until the review is submitted.

## JSON fields consumed by the watcher

### `gh pr view`

- `number`
- `url`
- `state`
- `mergedAt`
- `closedAt`
- `headRefName`
- `headRefOid`

### `gh pr checks`

- `bucket` (`pass`, `fail`, `pending`, `skipping`)
- `state`
- `name`
- `workflow`
- `link`

### Actions runs API (`workflow_runs[]`)

- `id`
- `name`
- `status`
- `conclusion`
- `html_url`
- `head_sha`

### Actions run jobs API (`jobs[]`)

- `id`
- `name`
- `status`
- `conclusion`
- `html_url`
