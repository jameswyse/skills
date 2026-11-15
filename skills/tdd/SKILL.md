---
name: tdd
description: Use for explicit TDD requests or a bug fix with a clear, cheap regression-test path.
---

# TDD bug fix

Write the smallest regression test that would have caught the bug, at the closest existing test seam for the broken path. It encodes the intended behaviour, not the current implementation, fails before the fix, and passes after it. Read the code-review [Testing](../code-review/references/testing.md) reference first.

1. Run the test before fixing and confirm it fails for the intended reason. If it passes or fails for another reason, correct the test first.
2. Make the smallest production change that fixes the behaviour, then rerun the test and the adjacent checks.
3. When the fix covers several behaviours, work in vertical slices: one failing test, the code that makes it pass, then the next.

When a failing test would need broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, or large fixture churn, say why before fixing and use the closest executable check instead, such as a targeted script or a scripted reproduction. Don't build test infrastructure for a small fix.

Report the failing-before check and the failure it produced, the passing-after run, and any check you used instead of a test and why.
