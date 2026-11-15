---
name: tdd
description: Use for explicit TDD requests or a bug fix with a clear, cheap regression-test path.
---

# TDD bug fix

Make the broken behaviour executable before changing production code: a focused regression test that fails before the fix and passes after it. Use the "engineering" skill, and read the code-review [Testing](../code-review/references/testing.md) reference before writing the test.

1. Write the smallest test that would have caught the bug, at the closest existing test seam for that path. It encodes the intended behaviour, not the current implementation.
2. Run it before fixing and confirm it fails for the intended reason. If it passes or fails for another reason, correct the test first.
3. Make the smallest production change that fixes the behaviour, then rerun the test and the adjacent checks.

When the fix covers several behaviours, work in vertical slices: one failing test, the code that makes it pass, then the next. Writing every test first commits to imagined behaviour before the implementation teaches you anything.

When a failing test would need broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, or large fixture churn, say why before fixing and use the closest executable check instead, such as a targeted script or a scripted reproduction. Don't build test infrastructure for a small fix.

Report the failing-before check and the failure it produced, the passing-after run, and any check you used instead of a test and why.
