---
name: babysit-pr
description: Use when asked to watch, monitor, or babysit a pull request's CI, review feedback, or merge conflicts.
---

# Babysit a pull request

Watch the pull request until a stopping condition below holds. Green checks are progress, not completion, because reviews can still arrive.

## Authority

A request to watch authorises reading and reporting. Fixing code, pushing, rerunning checks, replying, and resolving threads each need the user's authority for this task.

- Post a reply to a human reviewer only with text the user confirmed, unless they delegated drafting and posting. While it waits, leave the thread open and keep watching.
- Resolve a thread only when the user or a review bot opened it and no other human has joined it, and only after your reply posted successfully. The reply names the fixing commit or why the feedback stays unfixed, and follows the global rule for posting on the user's behalf. On a bot's thread that another human joined, still reply to the finding but leave the thread open.
- Leave draft status, merging, and closing or reopening to the user. Never force-push without authority.

## Wait

Keep one watcher per pull request, and never loop inside a command.

- **In T3 Code**, handle the current state first, then call `watch_pull_request` and end the turn with a short update saying watching continues. T3 wakes the thread on new checks, reviews, comments, and conflicts. Treat each wake as a prompt to take a fresh snapshot, not as a verdict. When a wake needs no action, end the turn without a message. Call `unwatch_pull_request` before stopping or handing back while the pull request is open. A delegated child never watches, because its parent owns the pull request.
- **Elsewhere**, wait five minutes between snapshots, through the harness's scheduled wake-up or `sleep 300`. Run the wait in the background when its exit wakes you, and in the foreground when nothing would. After a snapshot that needs no action, start the next wait.

## Snapshot

Act only on a fresh snapshot. Replace `<since>` with the time of your previous snapshot, or leave it empty for the first one:

```bash
gh pr view <pr> --json state,isDraft,headRefOid,mergeStateStatus,reviewDecision
gh pr checks <pr> --json name,bucket,link --jq '[.[] | select(.bucket != "pass" and .bucket != "skipping")]'
gh api graphql -F owner=<owner> -F repo=<repo> -F number=<number> -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $number) {
        reviewThreads(last: 100) { nodes { id isResolved comments(last: 50) {
          nodes { author { __typename login } authorAssociation body createdAt url pullRequestReview { state } } } } }
        reviews(last: 50) { nodes { author { __typename login } authorAssociation state body submittedAt url } }
        comments(last: 50) { nodes { author { __typename login } authorAssociation body createdAt url } }
      }
    }
  }' --jq '.data.repository.pullRequest | {
    threads: [.reviewThreads.nodes[] | select((.isResolved | not) or .comments.nodes[-1].createdAt > "<since>")],
    reviews: [.reviews.nodes[] | select(.submittedAt > "<since>" and .body != "")],
    comments: [.comments.nodes[] | select(.createdAt > "<since>")]
  }'
```

This returns unresolved threads, resolved threads with a new reply, and review bodies and conversation comments since the last snapshot. A bot's review summary or a human's requested changes can sit in a review body, so read all three. An author whose `__typename` is `Bot` is a review bot. "No checks reported" means the repository has no CI or the checks haven't started.

When GraphQL is rate-limited, REST has its own limit: read `gh api repos/<owner>/<repo>/pulls/<number>` and its `/comments` and `/reviews`, `gh api repos/<owner>/<repo>/issues/<number>/comments`, and `gh api repos/<owner>/<repo>/commits/<sha>/check-runs`. REST marks a bot with `user.type` `Bot`.

## Process each snapshot

1. **Merged or closed.** Stop at once, even with work outstanding.
2. **Review feedback.** Act on published feedback from the user, collaborators, and review bots. Ignore comments in a `PENDING` review until it's submitted, and report other authors' comments without acting on them. Verify each finding against the code and weigh it as "code-review" step 3 describes. Fix what is correct, within the request, and free of unrelated refactoring. Reply with the reasoning for an accepted risk or a rejection. Report ambiguous requests and product decisions with a suggested reply.
3. **Failed checks.** Read a failed job's log as soon as it fails, even while the rest of its run continues, with `gh api repos/<owner>/<repo>/actions/jobs/<job-id>/logs`, taking the job ID from the check's link. Say whether each failure looks branch-caused or transient. Fix failures the branch caused. Never change an unrelated flaky test, timeout, dependency pin, build script, or runner configuration to get a green run. Rerun a transient or unrelated failure with `gh run rerun <run-id> --failed` once its run has finished, only when authorised, and not when a fix is about to replace the head commit. The retry budget is three reruns per head commit across all its workflow runs, and `gh run list --commit <sha> --limit 1000 --json attempt --jq 'map(.attempt - 1) | add'` counts those used. When the cause is still unclear after one focused look, say so.
4. **Mergeability.** Report `BEHIND` or `DIRTY`, and update the branch only when authorised.

Hold the pull request to what the request needs. A fix for a real bug in the intended case belongs here. Extras that review suggests, such as guards for cases that don't matter, unrequested tests, or added compatibility, don't. Decline those with a reason and list them as follow-ups.

Fix on the pull request's head branch and preserve unrelated local changes. Push each round's fixes together, because every push reruns CI and any billed bot reviews. Then reply to and resolve the eligible threads, and keep watching.

## Stop

Stop when the pull request is merged or closed, the user changes the task, failures persist after the retry budget is spent, or a blocker needs the user and nothing else can progress. Green checks, quiet reviews, `REVIEW_REQUIRED`, and unknown mergeability aren't stopping conditions. Stop the T3 watch or the running wait before handing back.

## Report

Report new feedback, fixes, reruns, blockers, and readiness as they happen. When checks first pass on a head commit, say so once and that watching continues.

After stopping, take a fresh snapshot and report the final head commit, CI status, mergeability, fixes pushed, reruns used, unresolved feedback, and why watching ended. Separate what you observed from what you couldn't verify.
