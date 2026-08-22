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

## Separate before serialising shared state

When concurrent actors might share mutable state, first ask whether they need the same mutable object. If not, eliminate the shared write target. When sharing is a real invariant, enforce serialisation structurally with a lock, sequential phase, single writer, or atomic compare-and-swap.

1. Identify files, branches, keys, interfaces, or state objects that more than one actor can write.
2. Give independent facts separate owned files, keys, branches, or state directories. Merge them only at the read or reporting seam.
3. Use one serialised writer only when one canonical mutable object is truly required.

Two workers writing different fields in one `state.json` still share mutable state. Two owned state files do not. Instructions to "take turns" are not concurrency control.

If delegation is available and authorised, give each worker an isolated write target. Otherwise keep the work sequential.
