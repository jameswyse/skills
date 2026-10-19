# Bot draft review

Use after creating a draft pull request whose change needed "code-review". The repository's review
bots review the draft, so their comments are handled before the pull request is marked ready for
review. For a stack, work from the bottom layer up, and restart the loop for higher layers whenever a
fix to a lower layer changes their head commits.

## Review bots

| Bot        | Detection name                   | How a review starts                                                  |
| ---------- | -------------------------------- | -------------------------------------------------------------------- |
| Copilot    | `copilot-pull-request-reviewer`  | `gh pr edit <number> --add-reviewer @copilot`                        |
| Macroscope | `Macroscope - Correctness Check` | Automatically after each push, or a comment `@macroscope-app review` |

A bot is active when its detection name appears in the output below, or when it reviews the new
draft by itself:

```bash
gh pr list --state all --limit 10 --json reviews,statusCheckRollup \
  --jq '.[] | (.reviews[].author.login), (.statusCheckRollup[] | .name // .context)' | sort -u
```

Wait only for active bots in the table. When there are none, run `gh pr ready <number>` unless the
user asked for a draft, and stop.

Every push starts a billed Macroscope review, so push each round's fixes together. Don't use the
Macroscope CLI, which bills separately.

## Loop

1. **Start the reviews.** When Copilot is active, note the IDs of its existing reviews, then request
   its review.
2. **Wait for each active bot to review the head commit.** Check every 30 seconds for up to 15
   minutes.
   - Copilot has finished when
     `gh api --paginate repos/{owner}/{repo}/pulls/<number>/reviews --jq '.[] | select(.user.login == "copilot-pull-request-reviewer[bot]" and .commit_id == "<head-sha>") | .id'`
     prints an ID missing from step 1's list. Read the newest such review's body with
     `gh api repos/{owner}/{repo}/pulls/<number>/reviews/<review-id> --jq .body`. A body saying
     Copilot was unable to review, such as for a quota limit, means the review failed.
   - Macroscope has finished when
     `gh api -X GET repos/{owner}/{repo}/commits/<head-sha>/check-runs -f check_name="Macroscope - Correctness Check" --jq '.check_runs[] | [.status, .conclusion, .output.title] | @tsv'`
     prints `completed`. Comment `@macroscope-app review` on the pull request, following the global
     rule for posting on the user's behalf, when that check hasn't appeared after 5 minutes, or when
     it was `skipped` with a title other than "No code objects were reviewed." or "Diff unchanged".
     The repository may not review drafts automatically, or may have reached its automatic review
     limit.
3. **Handle the comments.** Read every bot's inline comments on the head commit with
   `gh api --paginate repos/{owner}/{repo}/pulls/<number>/comments --jq '.[] | select(.user.type == "Bot" and .in_reply_to_id == null and .original_commit_id == "<head-sha>")'`.
   This includes other bots, such as the Codex connector. Treat a concern raised only in Copilot's
   review body, such as "Needs a closer look", as a comment too.

   Verify and weigh each comment as a lead under the code-review skill's verification step. Fix the
   actionable ones, rerun the checks the fixes affect, then commit and push once.

   Reply to each thread with the fixing commit, or why it was rejected or accepted as a risk,
   following the global rule for posting on the user's behalf. Resolve it when the "babysit-pr"
   thread rules allow. Update the description when a fix changes what it says, and add review
   labels as [Airteam review labels](airteam-review-labels.md) describes when a fix adds a risk.
4. **Repeat after fixes.** When step 3 pushed a commit, return to step 1, for at most three rounds. A
   round in which no comment needed a fix is clean and ends the loop.
5. **Mark ready when clean.** After a clean round, confirm the head commit is still the one the bots
   reviewed, and return to step 1 if it changed. Add each reviewing bot to the description's models
   note as a reviewer, then run `gh pr ready <number>` unless the user asked for a draft. Macroscope
   checks again when the pull request is marked ready, and "babysit-pr" handles comments from that
   check. When a review request fails, a review fails or times out, or the third round still needed
   fixes, leave the pull request as a draft and report why.

Report Macroscope's Approvability verdict, the title of its `Macroscope - Approvability Check` run on
the final head commit. The verdict can depend on the change's scope rather than defects, so it never
blocks marking the pull request ready.
