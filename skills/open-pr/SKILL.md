---
name: open-pr
description: Use when creating or opening a pull request, drafting, writing, or updating a pull request's title, description, or Airteam review labels, or adding screenshots or recordings to one.
---

# Pull requests

Write a pull request that lets the project's other contributors understand why the change exists and the shape of the implementation before they open the diff. Use "writing" for the prose and "explain-code" for the change outline.

Those contributors did not see the conversation that produced the change. Use the terms the codebase, tickets, and team already use. Leave out anything that only makes sense with that conversation, such as labels or shorthand coined during the work, options or attempts that were discussed, and the user's instructions.

## Authority

Committing, pushing, creating a pull request, and editing one change shared systems. Perform each only when the user authorised it for the current task.

- A request to create or open a pull request authorises committing the task's changes, pushing the branch with an upstream, and creating the pull request with its review labels. It also authorises fixing actionable "code-review" findings in step 7, and the bot review in step 8, including starting bot reviews, fixing the code they flag, and replying to and resolving bot threads on that pull request.
- A request to create or open a pull request for work tied to a Jira issue also authorises moving that issue to review in step 8.
- A request to update or rewrite a description authorises editing that pull request's title, body, and review labels. A request to label a pull request authorises editing its review labels, but not its title or body.
- Applying review labels also authorises creating a baseline label the repository lacks, exactly as [Airteam review labels](references/airteam-review-labels.md) defines it.
- A request to draft or review a description authorises only the draft. Return it in the reply without publishing.

Commit only the task's changes. When the current branch is the default branch, create a branch first. Follow the repository's Git safety rules. Never add AI attribution to commit messages or pull requests, such as a `Co-Authored-By` trailer or a "Generated with" line. The Models note and the review report are the only places a description names models.

## Workflow

For a request only to label a pull request, run steps 1, 2, and 5, then apply the labels as step 5's reference describes and report them. For a request only to add screenshots or recordings, run steps 1 and 6, publishing as [Visual evidence](references/visual-evidence.md) describes, and report the result.

1. **Find the pull request.** Run `gh pr view --json url,number,title,body,state,baseRefName,headRefName` on the current branch. When none exists, inspect `git status --short --branch` and the branch's commits against its base. Ask the user to choose only when the current branch has no relevant work and the target is unclear. For a stack of dependent branches, use "gh-stack".
2. **Gather only the context the description needs.**
   - The complete diff against the base branch, and enough surrounding code to understand behaviour and ownership.
   - The linked ticket, issue, or plan when one exists.
   - The repository's pull-request template, such as `.github/pull_request_template.md`, and the style of recent pull-request titles and commit messages.
   - The verification actually run for this change.
3. **Write the title.** Follow the repository's convention, such as Conventional Commits. Name the change in the common terms a contributor scanning the pull request list would recognise, not the activity or a label from the conversation: "Lock prices before saving orders", not "Order fixes" or "Apply option B to the checkout flow". Keep it clear, concise, and under 72 characters. For work tied to a Jira issue, prefix it with the key as "jira" describes.
4. **Write the body** with [the description template](references/description-template.md). When the repository has its own template, keep its headings, checklists, and required fields, and fill them with this skill's content where each fits.
5. **Choose review labels.** When the base repository's owner is `airteamaus`, follow [Airteam review labels](references/airteam-review-labels.md).
6. **Add visual evidence for interface changes.** Follow [Visual evidence](references/visual-evidence.md) to capture and place screenshots or recordings, or state in the description that no visual evidence is attached.
7. **Review before creating.** Before creating a pull request, when the global instructions' rule requires "code-review", review the diff, then check the draft against it once.
   - If no review has covered the final diff, run "code-review" against the base branch through its repeat rounds. Keep the draft out of its spec, because a draft in the spec goes stale after every fix round.
   - Then, in every case, run only its Spec axis once, with the drafted title, body, and review labels with their reasons as the spec and the final diff as the scope. Update the draft to match the diff wherever they disagree, and send nothing back for another round.
   - Add the run report to the draft, with the Spec-only run as its own round.
8. **Publish when authorised.** Every new pull request opens ready for review unless the user asked for a draft. First check the title, body, and attachments for secrets, tokens, and private details. Write the body to a file in the temporary directory, then publish it:
   - For a new pull request, run `gh pr create --base <base> --title <title> --body-file <file>`. Add `--draft` only when the user asked for a draft, and an `--attach` flag for each capture from step 6. If GraphQL is rate-limited and `gh pr create` fails, REST still works: `gh api repos/<owner>/<repo>/pulls -f title=<title> -f head=<branch> -f base=<base> -F body=@<file>`, with `head` as `<fork-owner>:<branch>` from a fork, `-f head_repo=<fork-owner>/<fork-repo>` too when the fork belongs to the base repository's organisation, and `-F draft=true` for a draft. The labels, attachments, and confirmation below use GraphQL, so finish them once the limit resets, publishing the captures with the existing pull request's `gh pr edit` command.
   - For a stack, open its pull requests with `gh stack submit --auto --open` from "gh-stack" instead of `gh pr create`. `--open` marks every pull request in the stack ready for review, including existing drafts. When the user asked for a draft of any pull request in the stack, in this task or an earlier one, omit `--open`, which creates the new pull requests as drafts. Set each title and body with `gh pr edit <url>`. After a submit without `--open`, run `gh pr ready <url>` on each new pull request the user did not ask to keep as a draft.
   - For an existing pull request, run `gh pr edit <url> --title <title> --body-file <file>`, with an `--attach` flag for each new capture. Keep content the description does not own, such as author notes, media, checklists, linked issues, and bot sections.

   Apply the review labels from step 5 as its reference describes. For a new pull request that is ready for review and tied to a Jira issue, move the issue to review as "jira" describes. Confirm each pull request with `gh pr view <url> --json url,title,body,labels`. Bot review applies to a new pull request on github.com that needed "code-review". Follow [Bot review](references/bot-review.md) once it is open.
9. **Report.** Give the pull request link, title, and review labels, two or three sentences on the change and its notes, and any authorised step that did not happen, such as an unpushed branch. Paste the full body only when the request was to draft a description without publishing it.

## Write the description

Write as one person explaining the change to another. Use plain, specific language without jargon or slang.

- **Why the change.** One or two concise sentences: the problem this solves and what becomes possible after it ships. Prefer one.
- **Change outline.** A compact view of the implementation, not narrative paragraphs and not a file-by-file changelog. Build it from the "explain-code" views as GitHub Markdown, which are fenced code blocks, `diff` blocks, and `mermaid` diagrams, and use short bullets for behaviour those views can't show. A pull request body cannot hold an HTML file, so skip explain-code's HTML option.
- **Notes.** One to three bullets for reviewer warnings, migrations, compatibility constraints, deliberate omissions, or surprising decisions. Each bullet must make sense to a contributor reading only the pull request. Write `- None.` when there are none.
- **Verification.** The checks that confirmed the change, with their results. Leave out checks that did not run. Leave out external or private references, such as links only the author can open, local paths, and the names of models or agents that helped.
- **Review report.** When "code-review" ran on the change, put its run report, covering every round, in a collapsed block after the verification. For a stack, put it on each layer that review covered. When updating a description, keep its run report, and add the rounds of any review this task ran with an updated outcome line.
- **Models.** End the body with a GitHub note listing every model that worked on the change and its role, including reviewers. When updating a description, keep the models already listed.

Include only the outline views that explain this change, ordered so the story is easiest to follow:

- SQL table and endpoint request and response changes, with pseudocode for the business logic.
- Key data structure and type changes.
- A shallow file tree showing changed responsibilities.
- React component tree changes, including important hooks, state, and package boundaries.
- Call-tree, call-stack, control-flow, or data-flow changes.

Put something in a block only when a reader could find its shape in the code, such as a schema, type, query, file tree, component tree, call tree, or pseudocode with branches. Use a `diff` block for a change to an existing shape, where unmarked lines are its unchanged parts. Show the complete target shape when most of it is new or diff notation would obscure ownership or order. When a line would be a sentence, or would need wrapping, an arrow, or brackets to make sense, write bullets instead: one per behaviour, with the area it affects as the sentence's subject, not a bold label, and identifiers in backticks. Show each fact once. A bullet shouldn't repeat what a block above it already shows, and a block earns its place only when a reviewer needs to see that shape to understand the change. Omit categories that did not change. A small change can skip the outline and explain itself in a sentence.

When the pull request makes more than one distinct change, give each change a `###` subheading under the change outline, named in the codebase's terms, and keep its explanation and views beneath it. Use a subheading instead of an inline label such as "Checkout:". Test changes that span several changes can take their own subheading. Skip subheadings when the parts are steps of one change that reads better as a single story.

When a ticket, issue, plan, or related document is known, link it in a header line. Otherwise omit the header.

Do not expand the body beyond the template.
