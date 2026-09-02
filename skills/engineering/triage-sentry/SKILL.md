---
name: triage-sentry
description: Triage one supplied Sentry issue key or every issue in a project, report likely causes and recommended actions, then comment on and process only the actions the user approves. Use for focused issue review, project-wide noise reduction, and remediation planning.
---

# Triage Sentry issues

Assess the selected Sentry scope from its events and relevant source, then give the user one reviewable action plan before changing Sentry or the repository.

Call the Skill tool for "sentry-cli" when it is available. Follow its guidance, prefer dedicated `sentry issue` commands, use structured output with selected fields, and use `sentry schema` plus `sentry api` only for operations the dedicated commands do not support.

Chrome is a fallback, not a parallel source. Call the Skill tool for "chrome:control-chrome" only when the CLI is unavailable, fails after an appropriate retry, or cannot perform a required operation. Before controlling Chrome, ask the user to approve browser control and confirm that Sentry is already signed in in the Chrome profile to be used. Approval to use the CLI does not imply approval to control Chrome.

Do not expose authentication tokens, cookies, request bodies, complete headers, raw personal data, or other sensitive event data in commands, outputs, comments, reports, or saved files. Prefer named issue and event fields. Do not dump a complete event merely because it is available.

## Choose the scope

If the user supplies a Sentry short key such as `PROJECT-123`, use single-issue mode. The explicit key overrides project-wide triage. Do not list, inventory, classify, or recommend actions for other project issues. Events, traces, replays, logs, releases, and repository source connected to the selected issue remain within scope when they help explain it.

Numeric group IDs are not supported by this skill. If the user supplies one, ask for the issue's short key and do not fall back to project-wide triage. If a short key cannot be resolved, ask the user to check it or provide the organisation and project needed to disambiguate it. Do not fall back to project-wide triage.

Use project-wide mode only when the user does not supply an issue key or ID.

## Establish the target

In single-issue mode, treat the supplied short key as the exact read-only target. Use `sentry issue view <key>`, verify that the returned short key matches, and take the organisation and project from that issue. If the project was not already known, ask the user to confirm the resolved `org/project` and whether to save it in the project-level agent instructions. Do not ask them to restate a project the lookup already resolved.

In project-wide mode, treat the target as known only when the user supplied it or the project-level `AGENTS.md` or `CLAUDE.md` records it. Resolve the Sentry target in this order:

1. Use an explicit `org/project` from the user's request or the project-level agent instructions that govern the current directory.
2. Otherwise, let the CLI auto-detect a candidate and check it with a benign read. Ask the user to confirm the candidate before collecting issues.
3. If auto-detection is missing, ambiguous, or wrong, ask the user for the Sentry organisation and project. Do not guess from a DSN, repository name, or an unrelated project.

Whenever a project-wide target was not already known, ask whether to save the confirmed target in the project-level agent instructions. If they agree, add or update one concise entry under a `## Sentry` heading:

```markdown
## Sentry

- Default project: `org/project`
```

If the repository root's `CLAUDE.md` imports `AGENTS.md`, save the entry in `AGENTS.md`. Otherwise, use the repository-root instruction file loaded by the current agent. If both files exist without an import and neither owns the Sentry entry, ask the user which file should own it. Never use a user-global file. Preserve existing instructions and avoid duplicate headings or entries. Asking to save the target does not block read-only triage.

Before any mutation, verify that the authenticated Sentry identity can access the exact `org/project` and repeat that target in the proposed action plan. If CLI authentication is missing or expired, ask the user to complete the CLI's login flow. Never ask them to paste a token.

## Collect the selected issues

For every selected issue, start with compact fields such as:

- Numeric ID and short ID.
- Title, culprit, status, substatus, priority, and level.
- Event count, affected-user count, first seen, and last seen.
- Whether the error is unhandled, platform, assignee, fixability score, and permalink.

Then inspect each selected issue deeply enough to support its classification. Sample representative recent events rather than relying on the title or latest event alone. Compare releases, environments, transactions, safe tags, exception type and message, stack frames, breadcrumbs, recurrence, and affected cohorts when they distinguish the cause. Check related source and Sentry SDK configuration in the current repository when available. Use Seer explanations or plans selectively as supporting evidence, never as proof.

Keep collection bounded per issue. Expand the sample for high-impact, heterogeneous, or uncertain groups. Record an evidence gap instead of inventing a cause when retention, sampling, grouping, permissions, or missing source prevents a sound conclusion.

### Single-issue mode

Use the short-key lookup above without running `sentry issue list`. Confirm the final report names the exact supplied and resolved short key. If the lookup resolves a different issue, stop and ask the user to confirm the key.

### Project-wide mode

The default triage scope is every issue visible to the authenticated user across the project's retained history, including unresolved, resolved, and archived or ignored issues. State the visible statuses and any Sentry retention or permission limit in the report.

Fetch a fresh inventory with a time range broad enough to avoid the CLI's default 90-day window. Enumerate every issue status through explicit status queries or the API when the default list omits historical or archived issues. Follow pagination to exhaustion for each query, then deduplicate by numeric issue ID. Do not treat one page, one status, or the requested page limit as the complete project.

For a large project-wide inventory, triage in bounded batches while maintaining one compact, deduplicated ledger for the complete project. After each batch, retain only the report fields, classification, evidence summary, confidence, and proposed action. Discard raw event output. If a temporary ledger is needed, keep it outside the repository, exclude sensitive payloads, and remove that exact file after the final report. Batching must not omit issues or turn one project-wide approval plan into unrelated partial reports.

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

## Report before acting

Return a Markdown report that is easy to approve. It must contain:

1. The target, a stable report ID, collection time, scope, visible statuses, retention or access gaps, and number of issues reviewed.
2. A short priority summary with the highest-risk findings first.
3. Category sections that cover every inventoried issue. Give each issue its short ID and link, impact signals, evidence, likely cause with confidence, and recommended action.
4. An inventory table with one row per issue so the user can verify that none were omitted.
5. A numbered action plan split into `Sentry changes`, `settings or SDK changes`, and `code fixes`. Name every affected issue and the exact state change. Use `no action` when appropriate.

For a large project, keep routine issue notes to one table row and reserve longer analysis for high-impact or uncertain issues. The report must still account for every issue.

In single-issue mode, replace the category sections and project inventory table with one detailed issue section. Include the supplied and resolved short key, status, impact signals, evidence, likely cause with confidence, and recommended action. Keep the same numbered approval plan.

Ask the user to approve specific action numbers or a clearly identified batch. A general request to triage authorises the read-only inventory and report, not comments, status changes, merges, filters, settings changes, source edits, deployments, or releases. Approval of Sentry changes does not authorise settings changes, repository fixes, or deployment unless the approved plan names them.

## Process approved actions

Re-read the approved rows and verify the target before changing anything. Process only those rows. Identify each action with the report ID and numbered action, such as `2026-08-27T04:30Z/S-03`, and include that stable marker in its comment. If issue state or evidence has changed since the report, pause that action and show the difference instead of applying a stale decision.

Every terminal issue action requires a comment first. This includes resolve, archive, ignore, and merge. The comment should include:

- The classification and concise evidence.
- The likely cause and confidence, clearly marked as uncertain when appropriate.
- The approved next action and why.
- For noise or duplicates, the unarchive, re-open, or canonical-issue condition.

Use a dedicated CLI comment command if one becomes available. Otherwise inspect `sentry schema` for the supported issue-comment endpoint and use `sentry api`. If the CLI cannot create or verify the comment, request approval for the signed-in Chrome fallback. Do not perform the terminal action if the preceding comment cannot be created and verified.

Before posting, search the issue's comments for the exact action marker. Reuse and verify an existing matching comment instead of posting a duplicate. Before each status change or merge, read the current state. Treat the desired state as this batch's success only when the matching action marker is also present. If another actor reached the desired state without that marker, pause and report the external or stale change. Apply only a still-pending transition with its verified marker. For a merge, verify both the canonical issue and each source issue before deciding whether the approved merge is pending or already complete.

If a comment request has an uncertain result and the marker is not yet observable, stop rather than post it again. Before an approved Sentry setting mutation, read the current setting and compare the relevant match rule, action, and scope with the approved desired state. Write only when that exact transition is pending. Before an SDK or source mutation, inspect the current source and working-tree diff for an equivalent rule. Treat an equivalent existing change as complete, and pause on a different overlapping rule or edit.

Apply actions in small, recoverable batches. After each mutation, verify the comment and resulting issue status against the exact issue ID. The same approved batch must converge safely when retried after interruption. For SDK, settings, or source changes, make only the approved narrow change and run the relevant local checks. Do not deploy or release a fix unless the user separately authorises that step.

Stop the affected action on a permission error, target mismatch, unexpected status, partial failure, or broader suppression than the report described. Continue independent approved actions only when the failure cannot make them unsafe. Finish with an outcome table showing each approved action as completed, skipped, failed, or awaiting separate approval, plus direct links and any verification performed.
