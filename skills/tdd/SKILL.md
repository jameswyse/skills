---
name: tdd
description: "Use only when the user explicitly asks for TDD, a failing test, or a regression test, or when the bug has an obvious cheap local test target. Skip when the test path is unclear, expensive, integration-heavy, or not requested."
---

# TDD bug fix

When fixing a bug with a clear, cheap test path, make the broken behaviour executable before changing production code. The goal is a focused regression test that fails before the fix and passes after it.

Do not force a test when it would be impractical. If the available test would require broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, vague reproduction steps, or large unrelated fixture churn, skip adding a new test and use the closest useful verification instead.

## Workflow

1. **Understand the bug.** Identify the intended behaviour, current behaviour, affected path, and smallest observable reproduction.
2. **Choose the narrowest executable check.** Prefer the closest unit, component, integration, or regression test already used for that codepath. If no practical test path is obvious, do not create one from scratch just to satisfy the workflow.
3. **Write the failing test first.** Add the smallest focused test that would have caught the bug. The test should encode intended behaviour, not mirror the current implementation.
4. **Run the new test before fixing.** Confirm it fails for the intended reason. If it passes or fails for an unrelated reason, correct the test or reproduction before editing the implementation.
5. **Fix the bug.** Make the smallest production change that satisfies the intended behaviour while preserving nearby behaviour and interfaces.
6. **Rerun the regression test.** Confirm the test now passes.
7. **Run nearby validation.** Run relevant adjacent tests, type checks, lint, or scenario checks when the change has broader risk.

## If a failing test is impractical

Do not silently skip the regression step. Before fixing, explicitly explain why a failing test is impossible or not worth the cost, then choose the closest executable regression check available. Examples include a targeted script, manual reproduction command, browser automation, snapshot comparison, log assertion, or focused integration check.

Prefer no new test over a bad test. A bad test is one that mostly tests mocks, encodes current implementation details, depends on timing or unrelated global state, needs expensive infrastructure for a small fix, or would be deleted immediately after proving the fix.

## Guardrails

- Do not change tests merely to match a wrong implementation.
- Do not weaken existing assertions unless the expected behaviour has genuinely changed and the reason is clear.
- Keep the regression test focused on the bug. Avoid broad fixture churn or unrelated coverage expansion.
- Do not add tests when the practical signal is weak. Use manual or scripted verification and say why.
- If the bug is flaky, make the test deterministic where possible and document the signal being locked down.
- If the bug exposes a broader class of failures, first add the focused regression path, then consider additional sibling coverage.

## Seams: where tests go

A **seam** is where a module's interface lives. Test through that interface to observe behaviour without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

When the interface itself is in question, read `$engineering-practices`' [Deep modules](../engineering-practices/references/deep-modules.md) reference. It owns the module, interface, depth, seam, adapter, leverage, and locality vocabulary.

## Anti-patterns

- **Implementation-coupled.** The test mocks internal collaborators, calls private methods, or verifies through a side channel. Querying the database instead of using the interface is one example. The test breaks during a refactor even though behaviour has not changed.
- **Tautological.** The assertion recomputes the expected value in the same way as the code, so it passes by construction and can never disagree. Examples include `expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand with the same algorithm, or a constant asserted equal to itself. Expected values must come from an independent source, such as a known-good literal, worked example, or specification.
- **Horizontal slicing.** This means writing all tests first, then all implementation. Bulk tests verify _imagined_ behaviour. They test the _shape_ of things rather than user-facing behaviour, stop responding to real changes, and commit to a test structure before the implementation is understood. Work in **vertical slices** instead. Add one test, add one implementation, then repeat. Each test is a **tracer bullet** that responds to what the last cycle taught you.

## Final response

Report the evidence, not just the outcome:

- Name the failing-before test or executable check and the failure it produced.
- Name the passing-after test run and any nearby validation performed.
- If failing-before evidence could not be demonstrated, state why and describe the closest regression check used instead.
