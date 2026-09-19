---
name: triage-sentry
description: Triage a supplied Sentry issue or a project, then carry out only authorised actions.
---

# Triage Sentry issues

Assess the requested issues from events and relevant source, then present one reviewable action plan. Use "engineering" and its [execution guidance](../engineering/references/execution.md) for pending work, corrections, or delegated investigation.

## Tools and authority

Use "sentry-cli" when available. Prefer dedicated commands and compact structured output. Inspect `sentry schema` and use `sentry api` only for operations dedicated commands cannot perform.

When the CLI is unavailable or cannot perform the operation, use an available browser capability within the same authorised account, target, and action. Follow its instructions and verify the signed-in identity. A tool change alone does not require renewed permission. Preserve explicit CLI-only or other tool restrictions. Ask when the account, target, effects, or tool restriction is unresolved, while continuing independent authorised work.

Triage alone authorises read-only investigation and reporting. Comments, status changes, merges, filters, settings, source edits, deployments, and releases need authority covering those actions. Approval for Sentry changes does not imply approval for settings, code, or deployment. Carry forward existing approval; do not ask for it again.

Keep tokens, cookies, request bodies, complete headers, and raw personal data out of commands, outputs, reports, and saved files. Use selected issue and event fields. If authentication is missing, direct the user to the tool's login flow, never ask for a token.

## Resolve only the requested target

A supplied short key, numeric issue ID, or issue URL selects single-issue mode and overrides project-wide triage. Do not inventory or recommend actions for other issues. Related events, traces, logs, releases, replays, and source may be inspected when they explain the selected issue.

For a short key, use `sentry issue view <key>`. For a numeric ID or URL, use a supported read-only lookup found through the installed tool's help or API schema. Verify that the returned identifier matches the supplied target and record its numeric ID, short key, organisation, and project. Continue when the exact target resolves unambiguously. If lookup is unsupported, ambiguous, mismatched, or unavailable, ask for the short key or missing organisation/project. Never substitute a project-wide listing for failed single-issue resolution.

When no issue identifier is supplied, read [Project triage](references/project-triage.md) before resolving the project or collecting its issues. That branch owns complete inventory, historical statuses, pagination, and project reporting.

Saving a resolved target in repository instructions is optional and requires authority for that edit. It must not block investigation.

## Collect evidence

For every selected issue, start with compact fields such as:

- Numeric ID and short ID.
- Title, culprit, status, substatus, priority, and level.
- Event count, affected-user count, first seen, and last seen.
- Whether the error is unhandled, platform, assignee, fixability score, and permalink.

Then inspect each selected issue deeply enough to support its classification. Sample representative recent events rather than relying on the title or latest event alone. Compare releases, environments, transactions, safe tags, exception type and message, stack frames, breadcrumbs, recurrence, and affected cohorts when they distinguish the cause. Check related source and Sentry SDK configuration in the current repository when available. Use Seer explanations or plans selectively as supporting evidence, never as proof.

Keep collection bounded per issue. Expand the sample for high-impact, heterogeneous, or uncertain groups. Record an evidence gap instead of inventing a cause when retention, sampling, grouping, permissions, or missing source prevents a sound conclusion.

## Classify and recommend

Assign every selected issue to one primary category:

- `urgent real error`: active user harm, security or privacy risk, data loss, or a rapidly worsening failure.
- `actionable defect`: a real product, service, dependency, or integration error with a plausible repair.
- `observability defect`: broken instrumentation, source maps, release tagging, grouping, sampling, or tracking that obscures the real behaviour.
- `expected noise`: understood and non-actionable behaviour whose telemetry cost exceeds its diagnostic value.
- `duplicate`: the same underlying failure as another issue, supported by matching mechanism and evidence rather than similar titles.
- `already handled`: a resolved, archived, or ignored historical issue whose current state remains justified by the evidence.
- `needs evidence`: the available data cannot yet distinguish a real defect from noise.

Recommend the smallest action justified by the evidence. Typical actions are:

- Leave open and add a triage comment with the likely cause and repair recommendation.
- Add a comment, then resolve after a verified fix or when the issue is demonstrably no longer active.
- Add a comment, then archive with a stated unarchive condition. Prefer `auto`, a bounded period, event threshold, or user threshold over `forever` unless permanent suppression is clearly justified.
- Comment on each affected issue, then merge confirmed duplicates into a named canonical issue.
- Suppress future noise with a narrowly scoped Sentry inbound filter, SDK hook, or ignore rule. Treat this as a separate settings or repository change from archiving the current issue. Explain what matching condition will be dropped and what useful failures could be hidden.
- Gather named missing evidence and leave the issue open.

Do not recommend suppression merely because an issue is low frequency, old, hard to reproduce, or emitted by a third party. Do not archive an urgent real error, privacy concern, or data-loss risk as noise.

For every active issue classified as `urgent real error`, `actionable defect`, or `observability defect`, the proposed Sentry action must include a comment with the likely cause, confidence, and repair recommendation. Keep the issue open unless the approved plan includes a justified terminal action. Do not add retroactive comments to an already handled historical issue merely to satisfy this workflow.

For every active `expected noise` issue, propose a comment followed by archive. When future events match a stable, narrow condition and have no diagnostic value, propose a separate Sentry setting or SDK suppression action as well. Do not make permanent suppression part of the archive action by implication.

## Report and finish

Return a Markdown report with the exact target, a stable report ID, collection time, scope, retention or access gaps, and number of issues reviewed. Put the highest-impact findings first.

For one issue, include the supplied identifier and verified numeric ID/short key, status, impact signals, evidence, likely cause with confidence, and recommended action. Do not create project category sections or an inventory table for this mode. Project-wide reports follow their reference.

Provide a numbered plan separating Sentry changes, settings or SDK changes, and code fixes. Name exact targets and transitions, including `no action` when appropriate. Ask for approval of concrete action numbers or a named batch only when those actions are not already authorised.

A read-only request ends with the evidence and plan. When actions are authorised, read [Approved actions](references/approved-actions.md) before the first mutation and continue within that authority. That reference owns comment-before-transition ordering, retry markers, stale-state checks, and outcome verification.
