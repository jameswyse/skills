---
name: babysit-pr
license: Apache-2.0
description: Monitor a GitHub PR when asked to watch CI, review feedback, or merge conflicts; apply authorised fixes.
---

# PR babysitter

Monitor the PR persistently. A green, mergeable PR is a progress milestone, not completion:
new review feedback can arrive while it remains open.

## Authority and GitHub actions

A monitoring request authorises reading and reporting PR state. Fixes, commits, pushes, CI reruns,
comments, and thread resolution require authority from the user's request for the current task.
Carry existing authorisation forward without asking again. Apply these rules to every step below.

- Before changing code or GitHub state, fetch the current PR state directly with `gh`.
  Check the head SHA and relevant thread state rather than relying only on a watcher snapshot.
- For human-authored review replies, prepare the exact response for confirmation unless the user
  has already authorised that response or explicitly delegated drafting and posting replies.
  Permission to monitor or fix code does not itself authorise a reply.
- Unless the user explicitly directs otherwise, resolve only threads from the requesting user
  or the Codex, Copilot, Claude, Coderabbit, or Macroscope review bot, and only if no other human has participated.
  After the fix is pushed, post an authorised comment explaining the change and identifying its
  commit, then resolve. For feedback left unfixed after weighing, post the authorised reply
  explaining why, then resolve.
  If the comment still needs approval, leave the thread open and continue independent monitoring.
- Treat your own replies as handled if the watcher later reports them again.
- Leave draft status, readiness for review, and closing or reopening the PR to the user unless
  explicitly asked to change them. Report disagreements and requests for decisions in chat.

## Start the watcher

Use Python 3 and an authenticated `gh` installation with access to the target repository.
Run the watcher from that repository so `--pr auto` resolves its current branch.
Accept a PR number or URL in place of `auto` when supplied.

Set `BABYSIT_PR_SKILL_DIR` to the absolute directory containing this `SKILL.md`.
After this library's `scripts/sync-skills`, the default is:

```bash
BABYSIT_PR_SKILL_DIR="$HOME/.agents/skills/babysit-pr"
python3 "$BABYSIT_PR_SKILL_DIR/scripts/gh_pr_watch.py" --pr auto --watch
```

Use the actual skill directory if installed elsewhere. Prefer `--watch` for monitoring requests,
or T3 watching when it is available. Use `--once` for an explicitly requested snapshot, diagnosis,
local testing, or each T3 wake:

```bash
python3 "$BABYSIT_PR_SKILL_DIR/scripts/gh_pr_watch.py" --pr <number-or-url> --once
```

Keep exactly one watcher session for the PR and state file. Reuse that state file when restarting
so seen feedback and retry counts persist. Consume its JSONL output in the active task; do not
leave a detached watcher running and end the turn as though monitoring were complete.

The watcher defaults to a 30-second interval, configurable with `--poll-seconds`. Keep the base
interval while the PR is open, including after checks pass. Do not introduce a longer green-state
backoff that delays new review feedback.

### Watch through T3

When T3 Code's `watch_pull_request` tool is available, use it for wake-ups instead of `--watch`.
T3 checks the PR every minute and wakes this thread when a check fails, the required checks pass,
someone else comments or reviews, or the branch starts to conflict with its base.

1. Run `--once` and process the snapshot, because T3 wakes only for comments posted after the
   watch starts.
2. Call `watch_pull_request` for the PR, then end the turn. Ending the turn is correct here: T3
   owns the monitoring, and the `--watch` rules about consuming output in the same task do not apply.
3. On each wake, run `--once` with the same PR selector and state file, then process the snapshot.
   The snapshot and a direct `gh` check decide what to do.
4. After a push or rerun, run `--once` to confirm the new state, then end the turn while the watch
   continues.

T3 stops watching when the PR merges or closes, when it cannot read the PR for 15 minutes, or when
you call `unwatch_pull_request`. Call `unwatch_pull_request` when a stopping condition ends
monitoring while the PR is still open.

## Process each snapshot

1. Check for closure first. If the PR is merged or closed, stop immediately, even if the same
   snapshot includes review actions. Otherwise, read `actions` and surface new published review
   feedback before acting on CI failures or mergeability.
2. For `process_review_comment`, read the review criteria in
   [heuristics.md](references/heuristics.md#review-feedback). Fix valid, actionable feedback within
   the user's scope, except accepted risks. Report disagreements, unclear requests, and suggested
   replies in chat. If a decision or reply approval is pending, pause that action and continue
   independent work.
3. For `diagnose_ci_failure`, read the CI classification guidance in
   [heuristics.md](references/heuristics.md#ci-failures). Inspect logs before choosing a fix or rerun.
   If `failed_jobs` identifies a failed job while the workflow is still running, fetch that job's
   logs now. Use [the API notes](references/github-api-notes.md#failed-log-inspection) for commands.
   Patch only failures caused by the branch. Do not change unrelated flaky tests, dependency pins,
   build scripts, runner configuration, or infrastructure to make CI pass.
4. Before editing, verify that you are working on the PR head branch. Preserve unrelated changes;
   isolate the fix when possible. Ask only if overlapping changes make a safe edit uncertain.
   Avoid destructive Git commands and switch branches only when needed to recover the PR context.
   Validate the fix, commit and push when authorised, then handle eligible review threads under
   the authority rules above. If you paused `--watch`, restart it yourself immediately after the
   push, in the same turn, using the same PR and state file. A push is not completion.
5. For a likely flaky or unrelated failure, rerun only when `retry_failed_checks` is present and
   the user has authorised reruns. If a review or CI fix will replace the current SHA, prioritise
   that fix and skip the old SHA's rerun. The command below retries failed jobs. Honour the
   configured budget, which defaults to three cycles per head SHA; never reset state to evade it.
6. Check mergeability and conflicts alongside CI. Report `ready_to_merge` as progress and keep
   watching. After a rerun, consume fresh snapshots; do not end the task after reporting the action.
7. Apply the stopping conditions below. Otherwise keep consuming watcher output, or keep the T3
   watch active, including when `actions` contains only `idle`, CI is pending, or required review
   approval is outstanding.

Run an authorised retry when step 5 applies:

```bash
python3 "$BABYSIT_PR_SKILL_DIR/scripts/gh_pr_watch.py" --pr auto --retry-failed-now
```

Use the same PR selector and any custom `--state-file` or `--max-flaky-retries` values as the watcher.
Under `--watch`, avoid overlapping a retry with a watcher poll: pause the watcher, run the retry,
then restart `--watch` immediately with those same settings.

Use the repository's commit conventions. If none apply, the upstream defaults are:

- `fix: fix CI failure on PR #<n>`
- `fix: address PR review feedback (#<n>)`

## Published review feedback

Act only on published feedback. Ignore `PENDING` reviews and their inline comments without marking
them as seen; those comments must remain eligible when the reviewer submits the review.
The watcher can surface existing unaddressed feedback on its first run.

Review items include PR issue comments, inline comments, and submitted reviews. The watcher selects
trusted human authors, including repository owners, members, collaborators, and the authenticated
operator, plus approved review bots such as Codex, Copilot, Claude, Coderabbit, or Macroscope. Assess actionable
bot feedback as well as human feedback. Ignore unrelated bot noise and already-resolved threads
unless new unresolved feedback appears. The author's status does not replace checking the comment's
correctness or scope.

## Stop or continue

Stop monitoring when:

- The PR is merged or closed, including `stop_pr_closed`.
- The user interrupts or changes the monitoring task.
- `stop_exhausted_retries` reports persistent failures after the retry budget.
- A blocker requires user help and prevents further safe progress, such as lost access or a
  persistent infrastructure failure with no permitted retry.

An unresolved approval or product decision blocks the dependent action. Continue independent
monitoring while it remains useful and possible. Report the decision needed rather than guessing.
If a blocker ends monitoring, stop the owned watcher session or T3 watch before handing control
back.

Green checks, `ready_to_merge`, quiet reviews, unknown mergeability, and `REVIEW_REQUIRED` are not
stopping conditions for an open PR. Neither a successful push nor a rerun completes the task.
While the `--watch` watcher is running and no stopping condition applies, keep consuming output in
the same task instead of sending a final response or asking whether to continue. Under T3
watching, end each turn with a progress update that states monitoring continues.

## Report progress and completion

Report new review feedback, fixes, reruns, blockers, and readiness changes concisely. During quiet
periods, send occasional status updates rather than repeating the full snapshot each poll.
When CI first becomes green for a head SHA, report the actual passing count once and state that
monitoring continues. Keep push confirmations and merge-ready updates as progress messages.

After a stopping condition, report the final observed head SHA, CI status, mergeability, fixes
pushed, retries used, unresolved feedback, and the reason monitoring ended. Distinguish unverified
state from observed results. For a requested `--once` check, report the snapshot and exit without
claiming ongoing monitoring.
