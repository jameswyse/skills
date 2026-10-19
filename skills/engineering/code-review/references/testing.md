# Testing

Use tests to protect observable behaviour through interfaces that callers use. A durable test
survives changes to implementation, configurable content, and wording when the behaviour remains
the same.

## Apply the test gate first

Do not add a test merely because production code changed, a file was added, or coverage feels
expected. Before adding a test, be able to complete this statement with concrete details:

> This test fails when [observable runtime behaviour] breaks at [caller or user seam], and its
> expected result comes from [independent requirement, specification, known result, or maintained fixture].

Also name a plausible defect in runtime behaviour that the test would catch. If the statement or
defect is unclear, improve the design or do not add the test. A check for file contents, source
shape, an export, a mocked helper call, a current snapshot, or a type-system guarantee is not a
substitute for observable behaviour.

## Define what the test protects

Identify the valid alternatives the test must preserve. Proceed when the test gate and those
alternatives are clear from requirements and established behaviour. Ask before encoding an
unresolved choice that would set product policy, narrow supported behaviour, or establish a
disputed seam.

Choose the narrowest reliable test level that can observe the behaviour and produce a useful
failure. Use a unit, component, integration, or end-to-end test according to the behaviour, not the
implementation's file layout. Give each test one logical behaviour. Several assertions are fine
when they describe one outcome.

Exercise the same interface that callers use and assert the result through that interface. Test an
internal algorithm separately only when it has useful behaviour or diagnostics that interface
tests cannot identify clearly. If ordinary behaviour can be tested only by reaching through the
interface, reconsider the module shape. Read the engineering
[Design](../../engineering/references/design.md) reference when the interface or seam is in question.

## Keep execution cost proportionate

Treat wall time, CPU, memory, I/O, process or browser startup, DOM size, and external resource use
as part of the test design. Exercise the smallest workload and cheapest reliable seam that still
protects the stated guarantee and catches its plausible defect. Do not render a whole application
or large collection through a full UI when a smaller runtime seam protects the same guarantee. Do
not repeat expensive setup across adjacent tests when one scenario can protect the same logical
outcome with useful diagnostics.

Use timings, CI failures, retries, timeouts, memory exhaustion, and worker crashes as strong cost
evidence. During implementation and review, also inspect obvious multiplicative work and consider
how fixture growth and suite concurrency will affect it. Do not impose a universal duration or
data-size threshold. Browser, integration, large-data, and performance tests can justify higher
cost when their execution level or scale is part of the guarantee.

When a test becomes flaky or times out under contention, first remove work that the guarantee does
not need and isolate shared-resource contention. A larger timeout or more retries does not correct
disproportionate work and can make the full suite slower and less stable.

## Use an independent oracle

Derive expected values from a requirement, specification, known literal, worked example, or
independently maintained fixture. Do not recompute the expected result with the implementation's
algorithm. That test can pass by construction even when both calculations are wrong.

```typescript
// Recomputes the implementation's result.
test("calculates the total", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, item) => sum + item.price, 0);

  expect(calculateTotal(items)).toBe(expected);
});

// Uses a known result from the requirement.
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

A generated snapshot is not an independent oracle merely because it lives in another file. Treat
it as authoritative only after a person or an independent source has established that it is the
intended result.

## Use properties when the rule is general

Use a property-based test when an invariant is clearer than a list of examples. Good candidates
include parsers, smart constructors, normalisation, serialisation round trips, state transitions,
and idempotence. Use the repository's established property-test tool.

Define the property from an independent requirement. Generated inputs do not make an oracle
independent when the test repeats the implementation's algorithm. Keep focused examples for
important failures and edge cases that need clear diagnostics.

## Preserve valid alternatives

Do not turn a current deployment value, CMS entry, translation, message, generated identifier, or
incidental order into a requirement. Assert the semantic role, state, structure, or invariant that
the source actually owns. Pin an exact value only when an authoritative requirement defines it.

Ask whether another valid value should break the application. If the answer is no, do not assert
the current value.

```typescript
test.each(["https://service.example.test/api", "http://127.0.0.1:3100/fixture"])(
  "accepts a valid configured endpoint",
  (endpoint) => {
    expect(readEndpoint({ ENDPOINT: endpoint })).toBe(endpoint);
  },
);
```

## Keep tests deterministic

- Control time, randomness, generated identifiers, network responses, and concurrent work when
  they affect the result.
- Wait for an observable condition instead of an arbitrary delay.
- Isolate mutable global state and restore it after the test.
- Remove order dependence between tests.
- Use the closest stable replacement for an external system. Do not replace the behaviour under
  test with mocks.

## Reject test smells

Use these names during implementation and review. A smell is evidence to investigate, not an
automatic reason to rewrite a test.

- **Implementation-coupled test.** The test calls private methods, inspects private state, asserts
  helper calls, or verifies behaviour through generated types, file layout, CSS classes, database
  state, or another side channel. Refactor it to observe the behaviour through the caller's seam.
- **Private mock.** A mock or spy exposes internal collaborators, call order, or call counts. Put
  test doubles at real external seams. Assert an interaction only when the interaction itself is
  required behaviour, such as one externally visible side effect.
- **Tautological oracle.** The expected value comes from the same algorithm as the implementation.
  Replace it with an independent result.
- **Frozen configuration.** The test treats one valid configuration, content value, message, or
  order as the only valid result. Assert the rule and its supported alternatives.
- **Static-proof test.** The test repeats a guarantee already enforced by the type system or static
  analysis. Delete it unless runtime behaviour differs.
- **Timing-dependent test.** The test relies on real time, arbitrary delays, shared state, or
  uncontrolled scheduling. Control the source of variation or wait for the resulting condition.
- **Disproportionately expensive test.** The test consumes wall time, CPU, memory, I/O, processes,
  browsers, DOM nodes, or external resources beyond what its unique guarantee needs. Warning signs
  include exercising a narrow invariant through a whole application or full UI, pushing a large or
  growing collection through an expensive seam, repeating heavyweight setup for overlapping
  assertions, and increasing timeouts or retries to tolerate the work. Confirm the cost or scaling
  risk and the guarantee, then reduce the workload, use a cheaper reliable seam, or combine an
  overlapping scenario without weakening behaviour or diagnostics. Do not flag a justified costly
  test from scale alone.
- **Edit-proof test.** The test proves that a line, file, export, or other edit exists without
  protecting behaviour. Replace it with an observable outcome or remove it.

Prefer no new test over one whose signal is weak or whose maintenance cost exceeds the behaviour it
protects. Code changes do not require a matching test change when existing tests already protect
the behaviour or the change has no meaningful runtime behaviour to exercise. Remove tests for
superseded internals when replacement tests protect the same observable behaviour. When a change
removes, quarantines, or splits a test, confirm that the other behaviour it covered is still
covered. Keep any check the repository requires, such as a migration read-back test. Do not weaken
an existing assertion merely to match an incorrect implementation.
