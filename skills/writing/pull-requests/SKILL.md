---
name: pull-requests
description: Create a pull request, or write or update a pull request's title and description.
---

# Pull requests

Write a pull request that lets the project's other contributors understand why the change exists and the shape of the implementation before they open the diff. Use "writing" for the prose and "show-me" for the change outline.

Those contributors did not see the conversation that produced the change. Use the terms the codebase, tickets, and team already use. Leave out anything that only makes sense with that conversation, such as labels or shorthand coined during the work, options or attempts that were discussed, and the user's instructions.

## Authority

Committing, pushing, creating a pull request, and editing one change shared systems. Perform each only when the user authorised it for the current task.

- A request to create or open a pull request authorises committing the task's changes, pushing the branch with an upstream, and creating the pull request. It also authorises fixing actionable "code-review" findings in step 6, and the bot draft review in step 7, including starting bot reviews, fixing the code they flag, replying to and resolving bot threads on that pull request, and marking it ready.
- A request to update or rewrite a description authorises editing that pull request's title and body.
- A request to draft or review a description authorises only the draft. Return it in the reply without publishing.

Commit only the task's changes. When the current branch is the default branch, create a branch first. Follow the repository's Git safety rules and any commit or pull-request attribution lines the harness requires.

## Workflow

1. **Find the pull request.** Run `gh pr view --json url,number,title,body,state,baseRefName,headRefName` on the current branch. When none exists, inspect `git status --short --branch` and the branch's commits against its base. Ask the user to choose only when the current branch has no relevant work and the target is unclear. For a stack of dependent branches, use "gh-stack".
2. **Gather only the context the description needs.**
   - The complete diff against the base branch, and enough surrounding code to understand behaviour and ownership.
   - The linked ticket, issue, or plan when one exists.
   - The repository's pull-request template, such as `.github/pull_request_template.md`, and the style of recent pull-request titles and commit messages.
   - The verification actually run for this change.
3. **Write the title.** Follow the repository's convention, such as Conventional Commits. Name the change in the common terms a contributor scanning the pull request list would recognise, not the activity or a label from the conversation: "Lock prices before saving orders", not "Order fixes" or "Apply option B to the checkout flow". Keep it clear, concise, and under 72 characters.
4. **Write the body** with [the description template](references/description-template.md). When the repository has its own template, keep its headings, checklists, and required fields, and fill them with this skill's content where each fits.
5. **Add visual evidence for interface changes.** Use "before-and-after" when it is available and screenshots or recordings exist. Otherwise state in the description that no visual evidence is attached.
6. **Review before creating.** Before creating a pull request, when the global instructions' rule requires "code-review", review the draft and the diff together. If no review has covered the final diff, run "code-review" against the base branch with the drafted title and body in its spec, through its repeat rounds. If one has, run only its Spec axis on the drafted title and body against the diff, and update the draft to match its findings.
7. **Publish when authorised.** Write the body to a file in the temporary directory, then publish it:
   - For a new pull request, run `gh pr create --base <base> --title <title> --body-file <file>`. Add `--draft` when bot draft review applies or the user asked for a draft.
   - For a stack, open its pull requests with `gh stack submit --auto` from "gh-stack" instead of `gh pr create`. It creates new pull requests as drafts. Set each title and body with `gh pr edit`, then mark each new pull request ready with `gh pr ready <number>` unless bot draft review applies or the user asked for drafts.
   - For an existing pull request, run `gh pr edit <number> --title <title> --body-file <file>`. Keep content the description does not own, such as author notes, media, checklists, linked issues, and bot sections.

   Confirm the result with `gh pr view --json url,title,body`. Bot draft review applies to a new pull request on github.com that needed "code-review". Follow [Bot draft review](references/bot-draft-review.md) before it's marked ready.
8. **Report.** Give the pull request link and title, two or three sentences on the change and its notes, and any authorised step that did not happen, such as an unpushed branch. Paste the full body only when the request was to draft a description without publishing it.

## Write the description

Write as one person explaining the change to another. Use plain, specific language without jargon or slang.

- **Why the change.** One or two concise sentences: the problem this solves and what becomes possible after it ships. Prefer one.
- **Change outline.** A compact structural view of the implementation, not prose and not a file-by-file changelog. Build it from the "show-me" views as GitHub Markdown: fenced code blocks, `diff` blocks, and `mermaid` diagrams. A pull request body cannot hold an HTML file, so skip show-me's HTML option.
- **Notes.** One to three bullets for reviewer warnings, migrations, compatibility constraints, deliberate omissions, or surprising decisions. Each bullet must make sense to a contributor reading only the pull request. Write `- None.` when there are none.
- **Verification.** The checks that confirmed the change, with their results. Leave out checks that did not run. Leave out external or private references, such as links only the author can open, local paths, and the names of models or agents that helped.
- **Models.** End the body with a GitHub note listing every model that worked on the change and its role, including reviewers. When updating a description, keep the models already listed.

Include only the outline views that explain this change, ordered so the story is easiest to follow:

- SQL table and endpoint contract changes, with pseudocode for the business logic.
- Key data structure and type changes.
- A shallow file tree showing changed responsibilities.
- React component tree changes, including important hooks, state, and package boundaries.
- Call-tree, call-stack, control-flow, or data-flow changes.

Prefer `diff` blocks for changes to an existing shape. Show the complete target shape when most of it is new or diff notation would obscure ownership or order. Keep each view to what a reviewer needs and omit categories that did not change. A small change can skip the outline and explain itself in a sentence.

When the pull request makes more than one distinct change, give each change a `###` subheading under the change outline, named in the codebase's terms, and keep its explanation and views beneath it. Use a subheading instead of an inline label such as "Checkout:". Test changes that span several changes can take their own subheading. Skip subheadings when the parts are steps of one change that reads better as a single story.

When a ticket, issue, plan, or related document is known, link it in a header line. Otherwise omit the header.

Do not expand the body beyond the template.
