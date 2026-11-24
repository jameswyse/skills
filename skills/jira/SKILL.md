---
name: jira
description: Use when a Jira issue key or link comes up, before branching or committing in a repository that records a Jira project, or when creating, updating, splitting, or transitioning Jira issues, including filing problems found during other work.
---

# Jira

Use the Atlassian connector, on the site the repository records or the only one the account can reach. A token shaped like an issue key whose prefix isn't a project on that site, such as `UTF-8`, is ordinary text.

## Authority

Reading needs no permission. Creating, editing, commenting on, linking, and transitioning issues change a shared system, so do each only when the user's request covers it. A request to file issues also covers choosing their parent, type, labels, links, and assignee as this skill describes. A request to do an issue's work across several pull requests covers creating its sub-tasks. Never delete an issue. Comments follow the global rule for posting on the user's behalf.

## Read an issue

Before acting on a named issue, read its description, status, parent epic, linked issues, comments, and the attachments the task depends on. Read the parent too when the issue alone doesn't explain the goal. Carry forward only what the task needs. When a named issue can't be read, say so and continue only with work that doesn't depend on its contents.

## Repository project

A repository's instructions can record its Jira site and project:

```markdown
## Jira

- Site: `example.atlassian.net`
- Project: `ABC`. Use $jira before branching or committing.
```

Use them to search and to file new issues. When the repository's instructions lack the entry and the task showed which project the repository belongs to, such as through the issue in the request, the branch name, or the commit history, suggest the entry in your final report, and add it once the user agrees. Save it in `AGENTS.md` when the repository root's `CLAUDE.md` imports it, otherwise in the repository-root instruction file the current agent loads, and never in a user-global file.

## File an issue

1. **Search first.** Look for an open or recently resolved issue that already covers the problem, including support or service-desk projects that report into this one. Use the existing issue when one fits, and ask when the match is partial.
2. **Choose the parent.** Prefer the epic that the current work's issue sits under, then the epic its closest siblings use. Ask when two epics fit equally well.
3. **Copy the project's conventions.** Read the parent's recent child issues and match their issue type, summary prefix style, labels, and link types. Projects rename issue types, so check the project's create metadata for valid types and required fields instead of assuming defaults such as `Bug`.
4. **Write for the person who will do the work,** who may be another agent: the background with its evidence, a suggested fix, acceptance criteria, and the relevant files and tests. Scale the detail to the problem.
5. **Link** the issue that reported the problem and any pull request that addresses it.
6. **Leave planning to the team.** Leave new issues unassigned and in the backlog unless the user asks otherwise. Assign sub-tasks of work the user is doing now to the user.

Report each issue's key as a link to it.

## Split large work

When an issue's work needs more than one pull request, give each pull request its own sub-task, named for its change, and use that sub-task's key for its branch, commits, and pull request. A stack gets one sub-task per layer. Read the existing sub-tasks first and reuse any that already match a pull request, so a resumed split doesn't duplicate them. When the issue is itself a sub-task, use it for one pull request and create siblings under its parent for the rest. Work that fits one pull request gets no sub-tasks. Don't comment on the parent or the sub-tasks unless the user asks.

## Branches, commits, and pull requests

For work tied to an issue, put its key in the branch name and in every commit message and pull request title. Place it the way the repository's recent commits do, and with no precedent, lead with it: `ABC-123: Lock prices before saving orders`. When the repository records a Jira project and no issue is known, ask for its key before the first commit, and offer to file one.

## Move to review

When a pull request opens ready for review, move the issue whose key it carries into its project's review status, such as Review & Test or Code Review. In a stack, that is each layer's sub-task, not the parent. Read the issue's available transitions, because workflows differ by project, and ask when none clearly fits. Don't comment on the issue.
