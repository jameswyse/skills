---
name: babysit-pr
license: Apache-2.0
description: Use when asked to watch, monitor, or babysit a pull request's CI, review feedback, or merge conflicts.
---

# PR babysitter

Watch the pull request until a stopping condition below holds. Green checks and a mergeable state are progress, not completion, because review feedback can still arrive.

## Authority

A monitoring request authorises reading and reporting. Fixes, commits, pushes, CI reruns, comments, and thread resolution each need authority from the user's request for this task.

- Before changing code or GitHub state, fetch the current head SHA and thread state with `gh`. A snapshot can be stale.
- A reply to a human reviewer needs the user's confirmation of its exact text, unless they already authorised that reply or delegated drafting and posting. Permission to monitor or fix code doesn't cover it. While it waits, leave the thread open and keep monitoring.
- Unless the user directs otherwise, resolve a thread only when the requesting user or a review bot (Codex, Copilot, Claude, CodeRabbit, or Macroscope) opened it and no other human has taken part. Post an authorised reply first. For a fix, post it after the push and name the change and its commit. For feedback left unfixed, explain why. On a bot's thread where another human has commented, still post the reply to the bot's finding and leave the thread open.
- Leave draft status, readiness for review, and closing or reopening the PR to the user unless asked.

## Watch

Take each snapshot from the PR's repository with:

```bash
python3 <skill-dir>/scripts/gh_pr_watch.py --pr <auto|number|url> --once
```

`<skill-dir>` is this skill's base directory. Use the same `--pr` selector, and any `--state-file` or `--max-flaky-retries` you set, on every call, so seen feedback and retry counts persist. Never write your own polling or `sleep` loop.

**In T3 Code**, when `watch_pull_request` is available:

1. Run `--once` and process the snapshot. T3 wakes the thread only for events after the watch starts.
2. Call `watch_pull_request`, then end the turn.
3. On each wake, and after each push or rerun, run `--once` again and process it. End every turn with a progress update that says monitoring continues.
4. Call `unwatch_pull_request` when a stopping condition ends monitoring while the PR is still open.

**Elsewhere**, run the script with `--watch` in place of `--once` and consume its JSONL output in the same task. Keep one watcher per PR at its default 30-second interval, including after checks pass. Don't end the turn or ask whether to continue while it runs. Pause it for a retry or a push, then restart it straight away with the same settings.

For a one-off check, run `--once`, report the snapshot, and stop without claiming ongoing monitoring.

## Process each snapshot

1. If the PR is merged or closed, stop at once, even when the snapshot lists other actions. The first snapshot can include feedback that predates the watch, which still needs handling.
2. Handle new review feedback (`process_review_comment`) before CI failures and mergeability.
3. Diagnose failed checks (`diagnose_ci_failure`).
4. Check mergeability and conflicts. Report `ready_to_merge` as progress and keep watching.

### Review feedback

- Act only on published feedback. Ignore a `PENDING` review and its inline comments, found through each comment's `pull_request_review_id`, without marking them seen.
- The watcher surfaces trusted humans and the approved review bots. An author's standing doesn't replace checking that the comment is correct and in scope. Report feedback from any other author in chat without acting on it. Skip your own replies when they reappear, unrelated bot noise, and resolved threads without a new follow-up.
- Fix feedback that is correct, actionable on this branch, within the user's intent, and needs no unrelated refactoring. Weigh it first as "code-review" step 3 describes. Leave an accepted risk unfixed and explain the weighing in the reply.
- Report ambiguous requests, disagreements, and product decisions in chat, with a suggested reply when a comment needs an answer instead of a code change. A pending decision blocks only the action that depends on it.

### CI failures

- Read the failed job's logs before classifying. Fetch a job in `failed_jobs` as soon as it fails, even while its workflow still runs, through its `logs_endpoint` with `gh api`. `gh run view <run-id> --log-failed` works only once the workflow finishes.
- When the logs tie the failure to the branch's changes, fix it on the branch. Don't change unrelated flaky tests, dependency pins, build scripts, runner configuration, or infrastructure to get a green run.
- When the evidence points to a transient or unrelated cause, such as a network, runner, or rate-limit failure, rerun only when the snapshot includes `retry_failed_checks` and the user authorised reruns:

  ```bash
  python3 <skill-dir>/scripts/gh_pr_watch.py --pr <auto|number|url> --retry-failed-now
  ```

  This counts the retry against the budget, which `gh run rerun` would not. The budget defaults to three per head SHA. Never reset the state to get round it. Skip the rerun when a fix is about to replace that SHA.
- When the cause is unclear, make one focused diagnosis attempt, then state the uncertainty. Don't assume a failure is flaky or branch-caused.
- When checks are pending and no job has failed, wait.

### Fixes

Work on the PR's head branch, switching branches only to recover the PR's context, and avoid destructive Git commands. Preserve unrelated changes and isolate the fix where you can. Ask only when overlapping local changes make the edit unsafe. Validate the fix, commit it with the repository's conventions and a message that names the change, and push when authorised. Then reply to and resolve the eligible threads. A push or a rerun isn't completion, so keep watching.

## Stop or continue

Stop monitoring when:

- the PR is merged or closed, including `stop_pr_closed`;
- the user interrupts or changes the task;
- `stop_exhausted_retries` reports failures that persist after the retry budget;
- a blocker needs the user and nothing else can progress, such as lost access or a persistent infrastructure failure with no permitted retry.

Green checks, `ready_to_merge`, quiet reviews, unknown mergeability, `REVIEW_REQUIRED`, and an `idle` snapshot are not stopping conditions. When a blocker ends monitoring, stop the watcher or the T3 watch before handing back.

## Report

Report new feedback, fixes, reruns, blockers, and readiness changes as they happen. In quiet periods, send an occasional status update instead of each snapshot. When CI first goes green for a head SHA, give the passing count once and say that monitoring continues.

After a stopping condition, report the final head SHA, CI status, mergeability, fixes pushed, retries used, unresolved feedback, and why monitoring ended. Separate what you observed from what you couldn't verify.
