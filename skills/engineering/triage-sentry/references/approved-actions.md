# Approved Sentry actions

Before any mutation, verify that the authenticated identity can access the exact `org/project` and that the proposed action plan names it. Carry forward approval only for the exact targets and actions covered.

## Process approved actions

Re-read the approved rows and verify the target before changing anything. Process only those rows. Identify each action with the report ID and numbered action, such as `2026-08-27T04:30Z/S-03`, and include that stable marker in its comment. If issue state or evidence has changed since the report, pause that action and show the difference instead of applying a stale decision.

Every terminal issue action requires a comment first. This includes resolve, archive, ignore, and merge. The comment should include:

- The classification and concise evidence.
- The likely cause and confidence, clearly marked as uncertain when appropriate.
- The approved next action and why.
- For noise or duplicates, the unarchive, re-open, or canonical-issue condition.

Use a dedicated CLI comment command if one becomes available. Otherwise inspect `sentry schema` for the supported issue-comment endpoint and use `sentry api`. If the CLI cannot create or verify the comment, use the browser fallback only within the tool, account, target, and action limits in the [skill entrypoint](../SKILL.md#tools-and-authority). Do not perform the terminal action if the preceding comment cannot be created and verified.

Before posting, search the issue's comments for the exact action marker. Reuse and verify an existing matching comment instead of posting a duplicate. Before each status change or merge, read the current state. Treat the desired state as this batch's success only when the matching action marker is also present. If another actor reached the desired state without that marker, pause and report the external or stale change. Apply only a still-pending transition with its verified marker. For a merge, verify both the canonical issue and each source issue before deciding whether the approved merge is pending or already complete.

If a comment request has an uncertain result and the marker is not yet observable, stop rather than post it again. Before an approved Sentry setting mutation, read the current setting and compare the relevant match rule, action, and scope with the approved desired state. Write only when that exact transition is pending. Before an SDK or source mutation, inspect the current source and working-tree diff for an equivalent rule. Treat an equivalent existing change as complete, and pause on a different overlapping rule or edit.

Apply actions in small, recoverable batches. After each mutation, verify the comment and resulting issue status against the exact issue ID. The same approved batch must converge safely when retried after interruption. For SDK, settings, or source changes, make only the approved narrow change and run the relevant local checks. Do not deploy or release a fix unless the user separately authorises that step.

Stop the affected action on a permission error, target mismatch, unexpected status, partial failure, or broader suppression than the report described. Continue independent approved actions only when the failure cannot make them unsafe. Finish with an outcome table showing each approved action as completed, skipped, failed, or awaiting separate approval, plus direct links and any verification performed.
