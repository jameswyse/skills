# Testing

Tests protect observable behaviour through the interfaces callers use, and survive refactors, content edits, and wording changes that keep that behaviour.

## Apply the test gate first

Every new test must pass the [test gate](../../engineering/SKILL.md#test-gate) in the "engineering" skill, including its one type-level exception.

## Design the test

- Observe the behaviour through the caller's interface at the narrowest reliable level. If ordinary behaviour can only be tested by reaching past it, reconsider the module shape.
- Derive expected values from a requirement, known literal, worked example, or independently maintained fixture, never from the implementation's own algorithm. A generated snapshot is authoritative only after a person or independent source has confirmed it.
- Don't turn a current deployment value, CMS entry, translation, message, generated ID, or incidental order into a requirement. If another valid value shouldn't break the application, assert the rule instead of the value.
- Use a property-based test with the repository's tool when an invariant, such as a round trip or idempotence, is clearer than examples.
- Keep the cost proportionate. Don't render a whole application or large collection when a smaller seam protects the same behaviour, and remove work a slow or flaky test doesn't need before raising a timeout or adding retries.
- When no bug fix has already shown a new test failing, and it protects failure-prone logic such as dates, validation, mappings, state transitions, or a security boundary, confirm it can fail: temporarily remove the guard or shift the boundary, watch the test fail, then restore the code.
- When a change removes or splits a test, confirm the other behaviour it covered is still covered. Don't weaken an assertion to match an incorrect implementation.

## Test smells

A smell is a lead, not an automatic rewrite.

- **Implementation-coupled test.** Calls private methods, asserts helper calls, or checks behaviour through generated types, file layout, CSS classes, database state, or another side channel.
- **Private mock.** A mock or spy exposes internal collaborators, call order, or call counts. Put doubles at real external seams.
- **Tautological oracle.** The expected value comes from the implementation's algorithm, or the test asserts that a fake returns what the test configured it to return.
- **Unreachable assertion.** Assertions run only inside a loop, callback, or branch that may run zero times, so the test passes without checking anything.
- **Frozen configuration.** Treats one valid configuration, content value, message, or order as the only valid result.
- **Static-proof test.** Repeats a guarantee the type system or static analysis already enforces, or asserts compiler diagnostic text or positions.
- **Timing-dependent test.** Relies on real time, arbitrary delays, shared state, or uncontrolled scheduling.
- **Disproportionately expensive test.** Uses more time, processes, browsers, DOM, or data than its unique guarantee needs.
- **Edit-proof test.** Proves a line, file, or export exists, or that removed code stays gone, without protecting behaviour.
- **Duplicate guard.** Another test already protects the same behaviour through the same seam, so this one adds cost without catching a different defect. Keep the stronger one.
- **Test-only hook.** Production code exists only so tests can reach in, such as an exported `_resetCacheForTests` or a branch on a test flag. Test through the interface, and remove the hook along with the tests that needed it.
