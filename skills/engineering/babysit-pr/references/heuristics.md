# CI and review decisions

Use these criteria at the relevant step of the main skill's monitoring loop.
Its authority rules and stopping conditions also apply here.

## CI failures

Inspect failed-job logs before classifying a failure. A failed job can be diagnosed before its
workflow finishes; see [failed log inspection](github-api-notes.md#failed-log-inspection).

Treat a failure as branch-related when logs connect it to the PR's changes, for example:

- Compilation, type checking, lint, or static analysis failures introduced by the branch.
- Deterministic test failures in changed code.
- Snapshot changes caused by the branch's interface or text changes.
- A changed build script or configuration causing a reproducible failure.

Treat a failure as likely flaky or unrelated when the evidence points to an external or transient
cause, for example:

- DNS, network, or registry timeouts while fetching dependencies.
- Runner provisioning failures or GitHub Actions outages.
- Service rate limits or temporary API failures.
- Nondeterministic failures in unrelated integration tests with known flake patterns.

If the classification is unclear, make one focused diagnosis attempt before deciding whether to
retry. State the uncertainty if the logs remain inconclusive; do not assume that every failure
is flaky or caused by the branch.

Use a code fix only for a branch-related failure. For a likely flaky or unrelated failure, use
`retry_failed_checks` to determine whether failed jobs are eligible for a retry. The watcher waits
for the current checks to finish and enforces the configured retry budget for the head SHA.
If checks are pending and there is no failed job to inspect, wait. If a persistent failure cannot
be retried safely, report the blocker under the main skill's stopping conditions.

## Review feedback

Address feedback when it is technically correct, actionable on the PR branch, consistent with
the user's intent, and possible to fix without unrelated refactoring.

Report ambiguous requests, disagreements, and unresolved product decisions in chat. Provide a
suggested response when a comment needs an answer rather than a code change. Apply the main
skill's reply-authorisation rule before posting it. Continue independent monitoring while the
dependent action awaits a decision.

Inspect fresh thread state before responding or resolving. Skip your own handled replies and
resolved feedback unless a new unresolved follow-up needs attention. Preserve unrelated work;
if overlapping local changes make the proposed edit unsafe, isolate the fix or ask for direction.
