---
name: review-pr
description: Use when asked to review someone else's pull request, or to draft or post a review comment on one. For the user's own change, use code-review.
---

# Pull request reviews

Review someone else's pull request with "code-review", then give the author one review comment they can act on without seeing the review run. Use "writing" for the prose.

## Authority

Posting a review contacts the author. A request to leave, post, or submit the review authorises posting one review comment on that pull request. Otherwise return the draft. Always submit with the comment event, never approve or request changes. Follow the global rule for posting on the user's behalf.

## Workflow

1. **Find the pull request.** Run `gh pr view <ref> --json url,number,title,body,author,headRefName,baseRefName,baseRefOid,headRefOid,closingIssuesReferences`, then `gh api user --hostname <pull request host> --jq .login`.
2. **Check it out in a worktree.** Use a full clone whose remote URL matches the base repository, or make a full clone in the temporary directory. Run `git fetch <remote> <baseRefName> pull/<number>/head`, confirm `baseRefOid` and `headRefOid` exist with `git cat-file -e`, and repeat step 1 when either is missing. Then run `git worktree add --detach <new mktemp -d directory>/pr-<number> <headRefOid>`. Leave the current checkout alone.
3. **Gather the spec and earlier reviews.** Read the linked ticket or issue from the closing references, or a ticket key in the title, body, or branch name, through its tracker. Read every review and review thread on the pull request, including bot comments. The user's earlier reviews from this skill contain the "How this review was run" footer. Note the commit each one covered.
4. **Review.** Run "code-review" from the worktree with `baseRefOid` as the fixed point, the ticket, title, and body as its spec, and skip its step 4. When the author isn't the user, use its another-author mode. Give reviewers the worktree as their checkout, and add the existing threads and earlier findings to every manifest as already-raised items, to report again only with new evidence. On a re-review, still review the whole pull request as a first round, and note which earlier findings the new commits resolve.

   Review Spec and Correctness on both Opus and Fable. Once code-review's first-round reviewers and any replacements are settled, run each of those axes on the newest listed Opus or Fable that hasn't reviewed it yet, on `claudeAgent` at High effort, with Delegated review's call rules, or on a native subagent that can select that model when Delegated review's replacement rule applies. Each model sometimes catches what the other misses. When that model can't run, record that in the run report and don't substitute another model.
5. **Choose what to post.** Post every actionable finding, Spec findings left for a decision as questions to the author, and accepted risks. Drop findings that rest only on a personal preference and points an existing thread already makes. Dropped findings appear only as counts in the footer.
6. **Write the comment** with [the comment template](references/comment-template.md). Use the priorities and ID prefixes from "code-review" step 3, numbering only the posted items. On a re-review, an item that still stands keeps its ID from the earlier comment, and new items continue after the highest earlier number.
7. **Post when authorised.** When one of the user's earlier reviews from this skill already covers `headRefOid`, don't post again. Otherwise write the comment to a file in the temporary directory and pin it to the reviewed commit:

   ```bash
   gh api --hostname <host> repos/<owner>/<repo>/pulls/<number>/reviews \
     -f commit_id=<headRefOid> -f event=COMMENT -F body=@<file>
   ```

   Confirm it with `gh pr view <url> --json reviews,headRefOid`. When the returned head differs from the reviewed `headRefOid`, say in the report that the newer commits weren't reviewed.
8. **Clean up and report.** Remove the worktree with `git worktree remove --force <absolute path>`, then its temporary directory and any clone you made. Report the review link, or the draft when nothing was posted, the posted counts, and the run report.
