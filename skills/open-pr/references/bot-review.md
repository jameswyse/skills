# Bot review

Which bots review a pull request, and whether they review again after a push, depends on the
repository's settings. Wait only for reviews a bot has started, and request one only where its
section below allows. For a stack, work from the bottom layer up, and restart the loop for higher
layers whenever a fix to a lower layer changes their head commits.

Read the signs on the head commit with:

```bash
gh api --paginate repos/{owner}/{repo}/commits/<head-sha>/check-runs --jq '.check_runs[] | [.name, .status, .conclusion, .started_at, .output.title] | @tsv'
gh api repos/{owner}/{repo}/commits/<head-sha>/status --jq '.statuses[] | [.context, .state, .created_at] | @tsv'
gh api --paginate repos/{owner}/{repo}/issues/<number>/comments --jq '.[] | select(.user.login | endswith("[bot]")) | [.id, .user.login, .updated_at, .body[0:600]] | @tsv'
```

Post every review request as a pull request comment, following the global rule for posting on the
user's behalf. Every push starts the reviews a repository runs on push, some of them billed, so push
each round's fixes together.

## Review bots

### Copilot

Never request a Copilot review. Repository rules decide when it reviews, to control its cost. A
`copilot_code_review` rule in `gh api repos/{owner}/{repo}/rules/branches/<base>` reviews later
pushes only with `review_on_push`, and drafts only with `review_draft_pull_requests`.

Copilot has started when a `copilot-pull-request-reviewer` check run appears on the commit, and has
finished when that run completes. Then read its newest review of the commit with
`gh api --paginate repos/{owner}/{repo}/pulls/<number>/reviews --jq '.[] | select(.user.login == "copilot-pull-request-reviewer[bot]" and .commit_id == "<head-sha>") | [.id, .submitted_at] | @tsv'`
and `gh api repos/{owner}/{repo}/pulls/<number>/reviews/<review-id> --jq .body`. A body saying
Copilot was unable to review, such as for a quota limit, means the review failed.

### Codex

Codex reviews automatically only in some organisations. Comment `@codex review` when Codex shows no
sign 5 minutes after a ready pull request opens or a draft is marked ready. After a fix push, request
it the same way only when the fixes change risky or sensitive code, such as authentication,
permissions, payments, stored data, or concurrency, or code in an area that has broken before. When
a request brings no sign within 5 minutes, report that Codex didn't respond and continue without
it.

Codex has started when its summary comment's `codex-review-state` shows `code_review` with the
commit as `commit_sha`. The state can list other reviews of the commit, such as `security_review`.
Codex has finished when every review listed for the commit has `status` `completed`, with findings
as review comments and a `+1` reaction on the pull request when it has none. A `failed` status, such
as for a usage limit, means that review failed. The listing command above truncates comment bodies,
so read the whole summary comment by its ID with
`gh api repos/{owner}/{repo}/issues/comments/<comment-id> --jq .body`. The security review can post
findings there under "Security findings" instead of inline. When the summary's `security_review`
names the head commit as `commit_sha`, treat each one as a comment in the loop's step 3, and reply
to it in one pull request comment that lists each finding with its fixing commit or the reason it
was rejected or accepted as a risk.

### Macroscope

Comment `@macroscope-app review` only for the first review, when Macroscope is active and its check
hasn't appeared 5 minutes after a ready pull request opens or a draft is marked ready, or the check
was `skipped` with a title other than "No code objects were reviewed." or "Diff unchanged".
Macroscope is active when its check appears in recent pull requests:

```bash
gh pr list --state all --limit 10 --json statusCheckRollup --jq '.[].statusCheckRollup[] | .name // .context' | grep -cx 'Macroscope - Correctness Check'
```

Macroscope has started when a `Macroscope - Correctness Check` run appears on the commit, and has
finished when it completes. Don't use the Macroscope CLI, which bills separately. Report
Macroscope's Approvability verdict, the title of its `Macroscope - Approvability Check` run on the
final head commit, when it ran. The verdict can depend on the change's scope rather than defects, so
report it without treating it as a finding.

### Other bots

Never request a review from another bot, such as Pullfrog, CodeRabbit, PR-Agent, or Claude. One has
started when its check run or commit status appears on the commit, or it comments that it's
reviewing the commit. It has finished when that check or status completes, or it posts its review
or findings.

## Loop

1. **Start the reviews.** After a ready pull request opens, a draft is marked ready, or a fix push,
   check the signs every 30 seconds for 5 minutes. Then make the requests each bot's section allows,
   and check for 5 more minutes when you made one. On a draft, request nothing.
2. **Wait for each started review.** Check every 30 seconds for up to 15 minutes after it started,
   taken from its check run's `started_at` or when its sign first appeared. Leave out bots that
   showed no sign, because they won't review this commit.
3. **Handle the comments.** Read every bot's inline comments on the head commit with
   `gh api --paginate repos/{owner}/{repo}/pulls/<number>/comments --jq '.[] | select(.user.type == "Bot" and .in_reply_to_id == null and .original_commit_id == "<head-sha>")'`.
   Treat a concern raised only in a review body, such as Copilot's "Needs a closer look", as a
   comment too.

   Verify and weigh each comment as a lead under the code-review skill's verification step, and
   record each bot's counts in the code-review run report. Update the description's run report to
   match. Fix the actionable ones, rerun the checks the fixes affect, then commit and push once.

   Reply to each thread with the fixing commit, or why it was rejected or accepted as a risk,
   following the global rule for posting on the user's behalf. Resolve it when the "babysit-pr"
   thread rules allow. Update the description when a fix changes what it says, and add review
   labels as [Airteam review labels](airteam-review-labels.md) describes when a fix adds a risk.

4. **Repeat after fixes.** When step 3 pushed a commit, return to step 1, for at most three rounds.
   The loop ends after a round in which no comment needed a fix, or no bot started on the new head
   commit.
5. **Finish.** Confirm the head commit is still the one the loop last checked, and return to step 1
   if it changed. Add each reviewing bot to the description's models note as a reviewer. When a
   review request fails, a started review fails or times out, or the third round still needed
   fixes, report why. When a pushed fix changed behaviour and no bot started on the new head
   commit, report that the fix had no independent review.
