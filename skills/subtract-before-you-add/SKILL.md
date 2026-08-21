---
name: subtract-before-you-add
description: "Simplify the in-scope system before an addition, refactor or rewrite by removing dead weight and redundant paths, then build on the smaller base."
---

# Subtract before you add

Simplify the part of the system being changed before building on it.

## Subtract

- Identify dead code, redundant paths, unused abstractions, duplicate validation and references with no distinct content.
- Establish evidence that each candidate is unused or superseded. Account for its callers before removal.
- Remove only items inside the authorised scope. Preserve compatibility paths until their consumers have moved and their removal is part of the request.
- Verify the simpler baseline before adding new behaviour.

## Add

Build the requested behaviour on the smaller design. Use observed requirements rather than speculative edge cases. Add validators, parsers, guards or migration paths only when a real boundary or supported behaviour requires them.

The result should provide the requested capability with less or equal structural complexity than adding it to the original design would have required.
