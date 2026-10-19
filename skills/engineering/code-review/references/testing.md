# Testing

Tests protect observable behaviour through the interfaces callers use, and survive refactors, content edits, and wording changes that keep that behaviour.

## Apply the test gate first

Don't add a test because production code changed or coverage feels expected. Before adding one, complete this statement with concrete details:

> This test fails when [observable runtime behaviour] breaks at [caller or user seam], and its
> expected result comes from [independent requirement, specification, known result, or maintained fixture].

Also name a plausible defect it would catch. If you can't, improve the design or don't add the test. A check for file contents, source shape, an export, a mocked helper call, a current snapshot, or a type-system guarantee doesn't count.

Ask before encoding an unresolved choice that would set product policy or narrow supported behaviour.

## Design the test

- Choose the narrowest reliable level that observes the behaviour and gives a useful failure, by behaviour rather than file layout. Exercise and assert through the caller's interface. If ordinary behaviour can only be tested by reaching past it, reconsider the module shape.
- Derive expected values from a requirement, known literal, worked example, or independently maintained fixture, never from the implementation's own algorithm. A generated snapshot is authoritative only after a person or independent source has confirmed it.
- Use a property-based test with the repository's tool when an invariant, such as a round trip or idempotence, is clearer than examples.
- Don't turn a current deployment value, CMS entry, translation, message, generated ID, or incidental order into a requirement. Ask whether another valid value should break the application. If not, assert the rule instead of the value.

## Keep cost proportionate

Treat wall time, CPU, memory, I/O, process or browser startup, and DOM size as part of the design. Use the smallest workload and cheapest reliable seam that protects the guarantee. Don't render a whole application or large collection through a full UI when a smaller seam protects the same behaviour. When a test becomes flaky or slow under contention, remove work it doesn't need before raising a timeout or adding retries.

## Test smells

A smell is a lead, not an automatic rewrite.

- **Implementation-coupled test.** Calls private methods, asserts helper calls, or checks behaviour through generated types, file layout, CSS classes, database state, or another side channel.
- **Private mock.** A mock or spy exposes internal collaborators, call order, or call counts. Put doubles at real external seams.
- **Tautological oracle.** The expected value comes from the implementation's algorithm.
- **Frozen configuration.** Treats one valid configuration, content value, message, or order as the only valid result.
- **Static-proof test.** Repeats a guarantee the type system or static analysis already enforces.
- **Timing-dependent test.** Relies on real time, arbitrary delays, shared state, or uncontrolled scheduling.
- **Disproportionately expensive test.** Uses more time, processes, browsers, DOM, or data than its unique guarantee needs, such as a narrow invariant tested through the whole application, or timeouts raised to tolerate the work.
- **Edit-proof test.** Proves a line, file, or export exists without protecting behaviour.

Prefer no new test over one with a weak signal. When a change removes or splits a test, confirm that the other behaviour it covered is still covered. Don't weaken an existing assertion to match an incorrect implementation.
