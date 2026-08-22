# Testing

Use tests to protect observable behaviour through interfaces that callers use. A durable test
survives changes to implementation, configurable content, and wording when the behaviour remains
the same.

## Define what the test protects

Before writing a test, identify:

- The observable behaviour or invariant.
- The seam where a caller or user observes it.
- The authoritative source for the expected behaviour.
- The valid alternatives that must continue to work.

Proceed without asking when these facts are clear from requirements and established behaviour. Ask
the user before encoding an ambiguous choice that would set product policy, narrow supported
behaviour, or establish a disputed seam.

Choose the narrowest reliable test level that can observe the behaviour and produce a useful
failure. Use a unit, component, integration, or end-to-end test according to the behaviour, not the
implementation's file layout. Give each test one logical behaviour. Several assertions are fine
when they describe one outcome.

Exercise the same interface that callers use and assert the result through that interface. Test an
internal algorithm separately only when it has useful behaviour or diagnostics that interface
tests cannot identify clearly. If ordinary behaviour can be tested only by reaching through the
interface, reconsider the module shape. Read [Deep modules](deep-modules.md) when the interface or
seam is in question.

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
- **Edit-proof test.** The test proves that a line, file, export, or other edit exists without
  protecting behaviour. Replace it with an observable outcome or remove it.

Prefer no new test over one whose signal is weak or whose maintenance cost exceeds the behaviour it
protects. Remove tests for superseded internals when replacement tests protect the same observable
behaviour. Do not weaken an existing assertion merely to match an incorrect implementation.
