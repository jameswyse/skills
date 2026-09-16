# Execution and migration

Break multi-step work into verifiable units and converge on the intended end state without leaving transitional complexity behind.

## Proceed with reversible work

Apply the governing authority rules. Continue when the remaining decisions are minor, reversible, and covered by the requested outcome.

- Infer ordinary implementation details from the request, repository conventions, and current evidence.
- Perform read-only checks and normal implementation steps inside the authorised scope.
- State consequential assumptions in a progress update.
- Preserve unrelated work and keep changes easy to review or reverse.
- Present completed work and identify any decisions still open.

Reversibility does not grant permission. Stop when a choice significantly changes the intended result, authority is missing, or an action affects external systems or people beyond the request. Publishing, messaging, committing, pushing, deleting data, and modifying unrelated files require authorisation.

## Track pending work and corrections

For work spanning several steps or running jobs, keep a compact task record in the conversation. Use an existing authorised task file when one exists. Record only the current objective and completion criteria, authority, accepted corrections, consequential assumptions, pending questions, and running jobs with their IDs and dependencies. Mark superseded evidence and checks that need repeating. Preserve this record across compaction or handoff without creating a repository file merely to track a task.

When the runtime exposes asynchronous tools, start independent lookups and checks early, then continue work that does not need their results. A launched job is pending until its actual output establishes success or failure. Use the runtime's supported result and wait mechanisms. If asynchronous execution is unavailable, run the same dependencies sequentially. Skill instructions cannot enable an unsupported runtime capability.

When the user adds a correction or requirement during work:

1. Update the objective, authority, and remaining steps. Treat a side question as part of the conversation unless the user cancels or replaces the task.
2. Identify affected jobs, delegated tasks, decisions, and verification evidence.
3. Cancel obsolete work when the runtime supports cancellation, and tell affected workers what changed. A steering message does not itself cancel tools or undo completed actions.
4. Treat late results from superseded work as stale. Reuse them only after checking that their inputs and assumptions still apply.
5. Resume unaffected authorised work. Await any required answer before taking dependent action.

Before completion, collect and verify all required job results. Account for cancelled, failed, or still-running work and any effects it may have had. Do not claim that work will continue after the turn unless the runtime actually supports that execution and its status is known.

## Delegate bounded work

When an applicable workflow requests delegation, that request covers only work already within the user's task. Follow user and runtime restrictions on delegation. If permission is absent, tools are unavailable, or coordination would cost more than it saves, continue sequentially without a new approval pause.

Delegate when an independent question, distinct design, or substantial review area would benefit from a separate investigation. Keep a small, coherent change local when a direct check can resolve it. Use the smallest useful worker set; add workers only for distinct work that remains.

Give each worker the objective, bounded scope, completion evidence, relevant source paths, authority limits, and ownership. Use a fresh context for independent judgement when supported. Omit a suggested verdict. For writable work, give workers isolated write targets as [Reliable operations](operations.md) requires. Keep shared-state mutations serialised.

The primary agent owns user communication, integration, and verification. Send accepted corrections to affected workers. Inspect their artefacts and underlying evidence before accepting findings or claiming completion. Workers must not expand scope, contact unrelated agents, or recursively delegate unless the task and runtime permit it.

## Sequence verifiable units

Order work as small units that each end in a check. A break caught in the unit that caused it is cheap to localise. A break caught after a batch is buried beneath later work.

For a sweep, migration, or run of similar edits:

- Choose the smallest unit that reaches a meaningful verification point.
- Start from a known state, make one coherent change, run its check, and then advance.
- Keep checkpoints green under normal execution.
- When a planned migration needs temporary breakage, declare the affected interval in advance. Keep high-signal checks for the area being changed, and return to a fully verified state at the next explicit checkpoint.
- Do not create compatibility code merely to make every intermediate line compile when the declared checkpoint can verify the real end state.

When the user has authorised commits or pull requests, order them so a reviewer can replay the reasoning. A failing regression test followed by its fix is one useful shape. Other useful sequences include subtraction before reshape, baseline before treatment, and foundation before feature. Do not create commits or pull requests merely because this ordering would be useful.

## Migrate callers and remove the legacy path

When a new internal interface is the chosen design, migrate its callers and remove the old path in the same change wave.

- Inventory callers, migrate them, and delete the old internal interface.
- Treat temporary adapters as exceptional and time-limited, not as the default architecture.
- Carry the chosen design through every affected expression, including types, tests, documentation, examples, and recorded rationale.
- Update tests to protect the new observable behaviour.
- Delete tests that only protect the old implementation path.

Apply this only when no external users require backward compatibility, the project can absorb coordinated internal changes, and the new interface is part of an authorised simplification or refactor. Preserving both paths creates dual-path complexity and makes the codebase append-only.

## Converge on the outcome

Optimise for the intended, verifiable end state instead of preserving every intermediate state. Planned, scoped, and reversible intermediate breakage is acceptable between declared checkpoints. At the end state, complete required repository checks and direct verification of the changed behaviours under [Verification, review, and learning](verification.md). Broaden checks only when the change or remaining uncertainty justifies them.
