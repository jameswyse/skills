# Copilot draft review

Use after creating a draft pull request whose change needed "code-review". Copilot reviews the draft,
so its comments are handled before the pull request is marked ready for review. For a stack, work
from the bottom layer up, and restart the loop for higher layers whenever a fix to a lower layer
changes their head commits.

1. **Request the review.** Note the IDs of Copilot's existing reviews, then run
   `gh pr edit <number> --add-reviewer @copilot`.
2. **Wait for the review of the head commit.** Every 30 seconds for up to 15 minutes, run
   `gh api --paginate repos/{owner}/{repo}/pulls/<number>/reviews --jq '.[] | select(.user.login == "copilot-pull-request-reviewer[bot]" and .commit_id == "<head-sha>") | .id'`
   until it prints a review ID that wasn't there before the request, and use the newest one. Read
   that review's body with
   `gh api repos/{owner}/{repo}/pulls/<number>/reviews/<review-id> --jq .body`. A body saying
   Copilot was unable to review, such as for a quota limit, means the review failed.
3. **Handle the comments.** Read the review's inline comments with
   `gh api --paginate repos/{owner}/{repo}/pulls/<number>/reviews/<review-id>/comments`, along with
   any other review bot's inline comments on the head commit. Treat a concern raised only in the
   review body, such as "Needs a closer look", as a comment too. Verify and weigh each one as a lead
   under the code-review skill's verification step. Fix the actionable ones, rerun the checks the fixes affect, then commit and push. Reply to each thread with the
   fixing commit, or why it was rejected or accepted as a risk, following the global rule for
   posting on the user's behalf, then resolve it when the "babysit-pr" thread rules allow. Update
   the description when a fix changes what it says.
4. **Repeat after fixes.** When step 3 pushed a commit, request the review again and return to step
   2, for at most three Copilot reviews. A review whose comments needed no fix is clean and ends the
   loop.
5. **Mark ready when clean.** After a clean review, confirm the head commit is still the one Copilot
   reviewed, and return to step 1 if it changed. Then add Copilot to the description's models note
   as a reviewer, and run `gh pr ready <number>` unless the user asked for a draft. When the review
   request in step 1 fails, the review fails or times out, or the third review still needed fixes,
   leave the pull request as a draft and report why.
