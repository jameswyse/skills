---
name: triage-sentry
description: Use when given a Sentry issue URL, ID, or short key to investigate, or asked to triage a Sentry project's issues.
---

# Triage Sentry issues

Assess the requested issues from their events and the relevant source, then present one reviewable action plan.

## Tools and authority

Use "sentry-cli" when available, with dedicated commands and compact structured output. Use `sentry api`, after inspecting `sentry schema`, only for what dedicated commands can't do. When the CLI can't perform an operation, use an available browser capability within the same authorised account, target, and action, and verify the signed-in identity. A change of tool needs no new permission, but keep any explicit CLI-only or other tool restriction. Ask when the account, target, effects, or a tool restriction is unresolved, and continue the independent authorised work.

Triage alone is read-only. Comments, status changes, merges, filters, settings, source edits, deployments, and releases each need authority that covers them, and approval for Sentry changes doesn't extend to settings, code, or deployment.

Keep tokens, cookies, request bodies, complete headers, and raw personal data out of commands, output, reports, and saved files, and work from selected issue and event fields. When authentication is missing, point the user to the tool's login flow and never ask for a token.

## Resolve only the requested target

A short key, numeric issue ID, or issue URL selects single-issue mode and overrides project-wide triage, even when a default project is recorded. Don't inventory or recommend actions for other issues. Related events, traces, logs, releases, replays, and source are in scope when they explain the selected issue.

Use `sentry issue view <key>` for a short key, or a read-only lookup from the tool's help or API schema for an ID or URL. Check that the returned identifier matches, and record its numeric ID, short key, organisation, and project. If the lookup is unsupported, ambiguous, mismatched, or unavailable, ask for the short key or the organisation and project. Never fall back to a project-wide listing.

With no issue identifier, read [Project triage](references/project-triage.md) before resolving the project or collecting its issues.

## Collect evidence

Start from each issue's compact fields: IDs, title, culprit, status, substatus, priority, level, event and affected-user counts, first and last seen, handled state, assignee, fixability score, and permalink. Then sample representative recent events instead of trusting the title or latest event, and compare whatever distinguishes the cause, such as releases, environments, transactions, safe tags, exception type and message, stack frames, breadcrumbs, recurrence, and affected cohorts. Check the related source and the repository's Sentry SDK configuration. Use Seer explanations or plans selectively, as supporting evidence and never proof. Keep collection bounded per issue, and expand the sample for high-impact, mixed, or uncertain groups, and record an evidence gap instead of inventing a cause when retention, sampling, grouping, permissions, or missing source prevents a sound conclusion.

## Classify and recommend

Give every selected issue one primary category:

- `urgent real error`: active user harm, security or privacy risk, data loss, or a rapidly worsening failure.
- `actionable defect`: a real product, service, dependency, or integration error with a plausible repair.
- `observability defect`: broken instrumentation, source maps, release tagging, grouping, sampling, or tracking that obscures the real behaviour.
- `expected noise`: understood, non-actionable behaviour whose telemetry cost exceeds its diagnostic value.
- `duplicate`: the same underlying failure as another issue, shown by matching mechanism and evidence, not similar titles.
- `already handled`: a resolved, archived, or ignored historical issue whose state the evidence still justifies.
- `needs evidence`: the data can't yet tell a real defect from noise.

Recommend the smallest action the evidence justifies:

- **Active real error or defect of any of the first three kinds.** A comment with the likely cause, confidence, and repair recommendation. Keep the issue open unless the approved plan includes a justified terminal action.
- **Active expected noise.** A comment, then archive with a stated unarchive condition. Prefer `auto`, a bounded period, or an event or user threshold over `forever` unless permanent suppression is clearly justified.
- **Suppressing future noise.** When future events match a stable, narrow condition with no diagnostic value, also propose a narrowly scoped inbound filter, SDK hook, or ignore rule, as a separate settings or repository action from archiving the issue. Say what will be dropped and which useful failures it could hide.
- **Duplicate.** A comment on each affected issue, then a merge into a named canonical issue.
- **Resolve.** A comment, then resolve, only after a verified fix or when the issue is demonstrably no longer active.
- **Needs evidence.** Gathering the named missing evidence, with the issue left open.
- **Already handled.** No retroactive comment merely to satisfy this workflow.

Don't recommend suppression because an issue is low frequency, old, hard to reproduce, or emitted by a third party. Never archive an urgent real error, privacy concern, or data-loss risk as noise.

## Report and finish

Return a Markdown report with the exact target, a stable report ID, the collection time, scope, retention or access gaps, and the number of issues reviewed, highest impact first. For one issue, give the supplied identifier and the verified numeric ID and short key, status, impact signals, evidence, likely cause with confidence, and recommended action, with no category sections or inventory table.

Add a numbered plan that separates Sentry changes, settings or SDK changes, and code fixes, with exact targets and transitions, including `no action`. Ask for approval of specific action numbers or a named batch only for actions that aren't already authorised.

A read-only request ends with the evidence and plan. When actions are authorised, read [Approved actions](references/approved-actions.md) before the first mutation.
