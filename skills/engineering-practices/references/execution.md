# Execution and migration

Break multi-step work into verifiable units and converge on the intended end state without leaving transitional complexity behind.

## Proceed with reversible work

Continue when the remaining decisions are minor, reversible, and covered by the requested outcome.

- Infer ordinary implementation details from the request, repository conventions, and current evidence.
- Perform read-only checks and normal implementation steps inside the authorised scope.
- State consequential assumptions in a progress update.
- Preserve unrelated work and keep changes easy to review or reverse.
- Present completed work and identify any decisions still open.

Reversibility does not grant permission. Stop when a choice significantly changes the intended result, authority is missing, or an action affects external systems or people beyond the request. Publishing, messaging, committing, pushing, deleting data, and modifying unrelated files require authorisation.

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

Optimise for the intended, verifiable end state instead of preserving every intermediate state. Planned, scoped, and reversible intermediate breakage is acceptable between declared checkpoints. Require full static and runtime verification when the plan reaches its end state.
