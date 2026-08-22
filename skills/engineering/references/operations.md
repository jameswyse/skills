# Reliable operations

Design state-changing operations for crashes, restarts, retries, and concurrent actors. Make the mechanism correct without relying on an instruction that every participant behaves perfectly.

## Make operations idempotent

Design an operation so it converges to the correct state regardless of how many times it runs or where it resumes. Every operation should answer: "What happens if this runs twice? What happens if the previous run crashed halfway?"

Useful patterns include:

- Convergent startup that discovers existing state, cleans stale artefacts, and adopts live sessions.
- Content-based cleanup that compares equivalence instead of creation order.
- Self-healing locks with owner or process liveness checks.
- Scheduling that respawns failed work cleanly and regenerates fresh input for each cycle.

Test the operation at each interruption point:

1. Run it twice in a row.
2. Interrupt it after each state change and run it again.
3. Confirm that each re-execution converges to the same end state.

If the result depends on leftover partial state, add reconciliation.

## Bound retries and transactions

Use an ordinary function call or a database transaction for work that completes within one process and one transactional boundary. Use a durable workflow only when progress, delays, or retries must survive process loss or redelivery.

- Keep database transactions short. Do not hold one open across a network call or long-running operation.
- Put safe, short-lived technical retries beside the external operation that owns them.
- Put application retry policy with the operation that understands whether another attempt is valid.
- Put crash-resistant retries in the durable workflow that records their progress.

Every retried mutation needs a concrete idempotency mechanism. Use an idempotency key, a natural unique constraint, a deduplication record, a guarded state transition, or a transactional outbox or inbox according to the system. Do not infer safety from a side effect that is only likely to succeed once.

## Own configuration and resources

Parse environment variables and configuration at startup or the earliest entry seam. Pass typed configuration into application code. Do not scatter environment access through the system.

Keep resource creation, use, and cleanup under an explicit owner. Avoid import-time I/O, connection creation, server startup, and handler registration outside a true entrypoint. Isolate mutable singletons when a framework requires them.

When behaviour depends on time or randomness, pass a clock, a random source, or an explicit value through the nearest useful interface. Keep the dependency local. Do not add an application-wide service when a function parameter is enough.

## Separate before serialising shared state

When concurrent actors might share mutable state, first ask whether they need the same mutable object. If not, eliminate the shared write target. When sharing is a real invariant, enforce serialisation structurally with a lock, sequential phase, single writer, or atomic compare-and-swap.

1. Identify files, branches, keys, interfaces, or state objects that more than one actor can write.
2. Give independent facts separate owned files, keys, branches, or state directories. Merge them only at the read or reporting seam.
3. Use one serialised writer only when one canonical mutable object is truly required.

Two workers writing different fields in one `state.json` still share mutable state. Two owned state files do not. Instructions to "take turns" are not concurrency control.

If delegation is available and authorised, give each worker an isolated write target. Otherwise keep the work sequential.
