# Preserve PR babysitting behaviour

Use this checklist when revising `babysit-pr`. Its repeated persistence instructions protect
against premature completion. Retain reminders at the start, after a push, and at the decision
to stop. Reducing word count alone does not demonstrate an improvement.

## Upstream reasons

The imported source is frozen at `a8c36ca6d265800c1b2c67d19d3583e23dee8382`.
These earlier changes explain safeguards that the local revision retains:

- [Review monitoring fix](https://github.com/openai/codex/commit/0fe873ad5f4d) prioritised new review
  feedback over CI work and kept open, merge-ready PRs under observation for later feedback.
- [CI diagnostics and guardrails](https://github.com/openai/codex/commit/c39824c2fd47) added early
  failed-job log inspection, confirmation for human replies, and protection against unrelated fixes.
- [GitHub mutation policy](https://github.com/openai/codex/commit/f3a807497590) responded to unwanted
  interactions with other humans' review threads. Code fixes and human communication need separate
  authority; a thread involving another human must stay untouched unless explicitly authorised.
- [Pending review fix](https://github.com/openai/codex/commit/a770e5b8470d) prevented action on draft
  review comments while preserving their eligibility after publication.

The local authority rules carry forward existing user instructions. They replace repeated approval
requests and blanket stops for unrelated work with pauses limited to the affected action.
This is an intentional local adjustment, not a claim that upstream approval wording was redundant.

## Scenario checklist

For each scenario, compare the previous and proposed instructions against the expected decisions.
For agent evaluation, provide staged snapshots and fake GitHub, Git, and watcher tools in an isolated
fixture. Keep these expected decisions out of the task agent's context. Never use a live PR to test
writes. Follow [the evaluation procedure](README.md) for frozen revisions, repeated runs, trace
capture, and explicit `not_exercised` results when the necessary runtime is unavailable.

| Scenario                       | Expected decision                                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------------- |
| Open PR becomes merge-ready    | Continue at the base interval; handle later published feedback before CI work.                             |
| Review fix has been pushed     | Restart the paused watcher in the same task with the same state file; keep one active watcher.             |
| Reviewer has a pending review  | Ignore the review and its inline comments without marking them seen; inspect them after publication.       |
| Review fix and retry coincide  | Handle review feedback first; skip a retry for a SHA about to be replaced.                                  |
| Job fails before workflow ends | Inspect that job's logs immediately; do not wait for workflow completion to diagnose it.                    |
| Unrelated infrastructure fault | Do not patch tests or infrastructure; retry only when eligible and authorised.                             |
| Retry budget is exhausted      | Report the persistent failure and stop; never reset state or bypass accounting with a direct rerun.        |
| A human comment needs a reply  | Carry forward explicit reply authority or prepare the exact response for confirmation; keep monitoring.   |
| Another human joins a thread   | Leave its comments and resolution untouched unless explicitly authorised to act on that thread.            |
| Own reply or resolved feedback | Avoid duplicate replies and redundant fixes; inspect new unresolved follow-up feedback.                    |
| Worktree has unrelated edits   | Preserve them and isolate the fix; ask only when overlap prevents safe editing.                            |
| PR closes with feedback queued | Stop immediately without applying stale review actions.                                                   |
| Watcher remains active         | Consume its output; do not claim completion or leave an unattended process after a final response.          |
| User requests one snapshot     | Run once, report observed state, and finish without claiming ongoing monitoring.                            |
| Product decision is pending    | Pause the dependent action and continue independent monitoring; do not guess the answer.                   |

## Verification limits

`scripts/test-skills` includes the upstream watcher tests for review ordering, pending-review
publication, open merge-ready polling, and failed-job log endpoints. These tests exercise the
Python implementation. They do not execute `SKILL.md` or prove that an agent follows it.

A manual scenario review checks for missing or contradictory instructions. Report it separately
from observed agent runs. The editorial revision received a manual scenario review and script
checks; repeated agent comparisons and live monitoring were not exercised. Do not claim measured
behavioural equivalence from metadata validation, shorter text, or passing script tests.
