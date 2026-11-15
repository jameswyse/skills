# Approved Sentry actions

Before any mutation, verify that the authenticated identity can access the exact `org/project` and that the approved plan names it. Process only the approved rows, for the exact targets and actions they cover. If an issue's state or evidence has changed since the report, pause that action and show the difference instead of applying a stale decision.

## Comment before every terminal action

Resolve, archive, ignore, and merge each need a comment first. Identify every action by the report ID and its number, such as `2026-08-27T04:30Z/S-03`, and put that marker in the comment with:

- the classification and concise evidence;
- the likely cause and confidence, marked as uncertain when it is;
- the approved next action and why;
- for noise or duplicates, the unarchive, re-open, or canonical-issue condition.

Post the comment with a dedicated CLI command if one exists, otherwise through the endpoint `sentry schema` shows with `sentry api`, otherwise through the browser within the entrypoint's tool limits. Don't take the terminal action when the comment can't be created and verified.

## Make each action safe to repeat

- Before posting, search the issue's comments for the exact marker, and reuse and verify a matching comment instead of posting a duplicate.
- When a comment request has an uncertain result and the marker isn't visible yet, stop instead of posting again.
- Before each status change or merge, read the current state. The desired state counts as this batch's success only when the marker is also present. If another actor reached it without the marker, pause and report the external change. For a merge, check the canonical issue and each source issue.
- Before a Sentry setting change, read the current setting, compare its match rule, action, and scope with the approved state, and write only when that exact transition is still pending.
- Before an SDK or source change, check the source and working-tree diff for an equivalent rule. Treat an equivalent change as complete, and pause on a different overlapping one.

Apply actions in small, recoverable batches that converge safely when retried after an interruption, and verify the comment and resulting status against the exact issue ID after each mutation. For SDK, settings, or source changes, make only the approved narrow change and run the relevant local checks. Don't deploy or release a fix unless the user separately authorises that.

Stop the affected action on a permission error, target mismatch, unexpected status, partial failure, or broader suppression than the report described, and continue the independent approved actions only when the failure can't make them unsafe. Finish with an outcome table that shows each approved action as completed, skipped, failed, or awaiting separate approval, with direct links and the verification performed.
