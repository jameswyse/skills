---
name: full-send
description: Take a task through to a ready pull request with passing checks and resolved bot comments when the user asks to full-send it, says "full send", or ends the prompt with the word "FS".
---

# Full send

Take the request through implementation and review to a pull request that is ready for review, with passing checks and every review-bot comment handled. A trailing "FS" invokes this skill and isn't part of the request. A request to discuss or edit this skill doesn't invoke it, and neither does a delegated task's prompt.

## Authority

Invoking this skill authorises, for the current task:

- implementing the request and fixing actionable "code-review" findings within it;
- everything a request to create a pull request authorises under "pull-requests", including its bot draft review and marking the pull request ready;
- under "babysit-pr", fixing valid review feedback within the request and CI failures the branch caused, pushing those fixes, rerunning failed checks within its retry budget, requesting bot reviews, updating the description to match, and replying to and resolving review-bot threads.

It doesn't authorise merging, force-pushing, production changes, or replying to a human reviewer.

## Decide or stop

These conditions replace the engineering skill's pause rule for this task. Decide everything else yourself. Stop and ask only when:

- the request can't be delivered as written, such as conflicting requirements, evidence that the requested approach fails, or a Spec finding that "code-review" leaves to the user;
- neither the request nor the codebase settles a choice about product behaviour, a public interface, stored data, dependencies, or infrastructure, and a wrong guess would mean rework after review;
- the work needs a one-way door the authority above doesn't cover;
- missing access, or a check failure the branch didn't cause, still blocks progress after the retries "babysit-pr" allows.

## Other issues

Keep the branch to the request. When you find an issue outside it, such as a pre-existing bug, a "code-review" finding beyond the request, review feedback asking for more scope, or a bot finding left after the round limit, note it with its evidence and continue. Fix it on the branch only when the request needs the fix. This replaces the engineering skill's rule to fix minor instances of the same pattern.

In the final account, list these under "Other issues" with the fix you recommend. Then offer to fix them on this branch or in a separate T3 thread launched with `t3_thread_launch` in a new worktree from the default branch. Without T3, offer a separate branch instead. Skip the list and the offer when there are none.

## Workflow

1. **Implement** with "engineering" and the skills it routes to, and verify the change as it requires.
2. **Review** with "code-review" through its repeat rounds.
3. **Open the pull request** with "pull-requests", which commits, pushes, and runs its bot draft review. Just before the pull request is marked ready, note the IDs of the active bots' check runs and reviews on the head commit. When that review leaves the pull request as a draft, mark it ready anyway and report why.
4. **Watch** with "babysit-pr". After each push, or when resuming a pull request whose head commit an active bot hasn't reviewed, request and wait for the active bots' reviews with steps 1 and 2 of the bot draft review. After marking the pull request ready, use step 2 to wait for bot runs and reviews missing from the IDs noted in step 3. Handle their comments as the bot draft review's step 3 describes. A round is one push of fixes for bot findings. After three rounds since marking the pull request ready, stop fixing bot findings and list the rest as other issues.
5. **Finish** when all of these hold, even on the first snapshot:
   - the pull request is open and ready for review;
   - every required check on the final head commit has passed, and no check has failed;
   - every active review bot has reviewed the final head commit, including any review that marking the pull request ready started, unless its review request or review failed or timed out;
   - every review-bot thread has a reply and is resolved where the "babysit-pr" thread rules allow.

   These conditions replace the stopping conditions in "babysit-pr". Human approval isn't one of them. Once they hold, stop the watcher or T3 watch as "babysit-pr" describes. Include the pull request link, final head commit, check results, any checks still pending, and any drafted human replies in the final account.
