---
name: full-send
description: Use when the user says "full send" or ends a prompt with the word "FS".
---

# Full send

Take the request through implementation and review to a pull request that is ready for review, with passing checks and every review-bot comment handled. A trailing "FS" invokes this skill and isn't part of the request. A request to discuss or edit this skill doesn't invoke it, and neither does a delegated task's prompt.

## Authority

Invoking this skill authorises, for the current task:

- implementing the request and fixing actionable "code-review" findings within it;
- everything a request to create a pull request authorises under "open-pr", including its bot review, and marking a draft pull request ready;
- under "babysit-pr", fixing valid review feedback within the request and CI failures the branch caused, pushing those fixes, rerunning failed checks within its retry budget, requesting bot reviews, updating the description to match, and replying to and resolving review-bot threads.

It doesn't authorise merging, force-pushing, production changes, or replying to a human reviewer. Because it never merges, it authorises turning off auto-merge.

## Decide or ask

Decide everything yourself except the cases below, which replace the engineering skill's pause rule for this task. Ask only in these cases, after finishing whatever doesn't depend on the answer:

- the request can't be delivered as written, such as conflicting requirements, evidence that the requested approach fails, or a Spec finding that "code-review" leaves to the user;
- neither the request nor the codebase settles a choice about product behaviour, a public interface, stored data, dependencies, or infrastructure, and a wrong guess would mean rework after review;
- the work needs a one-way door the authority above doesn't cover;
- missing access, or a check failure the branch didn't cause, still blocks progress after the retries "babysit-pr" allows;
- the pull request is in a merge queue.

Ask with the session's question tool, such as `AskUserQuestion` in Claude Code or `request_user_input` in Codex, because a question in an ordinary message leaves the thread looking finished. The tool holds the turn until the user answers, which is why the independent work comes first. Put the blocker, the pull request link when there is one, and the options in the question, with your recommended option first. Without a question tool, or when it returns no answer, leave any pull request open and lead the final account with the question.

## Other issues

Keep the branch to the request. When you find an issue outside it, such as a pre-existing bug, a "code-review" finding beyond the request, review feedback asking for more scope, or a bot finding left after the round limit, note it with its evidence and continue. Fix it on the branch only when the request needs the fix. This replaces the engineering skill's rule to fix minor instances of the same pattern.

List these under "Other issues" in the final account with the fix you recommend, and offer to fix them on this branch or in a separate T3 thread launched with `t3_thread_launch` in a new worktree from the default branch. Without T3, offer a separate branch.

## Workflow

When a pull request already exists at the start, once you open one, and before each push, check its auto-merge and merge queue state with `gh api graphql -F owner=<owner> -F repo=<repo> -F number=<number> -f query='query($owner: String!, $repo: String!, $number: Int!) { repository(owner: $owner, name: $repo) { pullRequest(number: $number) { isInMergeQueue autoMergeRequest { enabledAt } } } }'`. Turn auto-merge off with `gh pr merge --disable-auto <url>` and report it. A pull request in a merge queue is a case to ask about.

1. **Implement** with "engineering" and the skills it routes to, and verify the change as it requires.
2. **Review** with "code-review" through its repeat rounds.
3. **Open the pull request** with "open-pr", which commits, pushes, and runs its bot review. When a pull request was a draft before publishing and still is, mark it ready with `gh pr ready <url>`.
4. **Watch** with "babysit-pr". After each push, run the bot review loop from its step 1 for that push. When step 3 above made a draft ready, or when resuming a pull request whose bot review step 1 didn't finish after it became ready, run its step 1 as for a newly ready pull request. A round is one push of fixes for bot findings. After three rounds in this step, stop fixing bot findings, reply to each remaining thread that it is listed as an other issue, and list them there.
5. **Finish** when all of these hold, even on the first snapshot:
   - the pull request is open and ready for review;
   - every required check on the final head commit has passed, and no check has failed;
   - every bot review that started on the final head commit has finished, failed, or timed out;
   - every review-bot thread has a reply and is resolved where the "babysit-pr" thread rules allow.

   These conditions replace the stopping conditions in "babysit-pr", and human approval isn't one of them. Once they hold, stop the watcher or T3 watch as "babysit-pr" describes. Include the pull request link, final head commit, check results, any checks still pending, and any drafted human replies in the final account.
