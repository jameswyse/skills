---
name: design-from-foundations
description: "Design the core types, data structures, state ownership and work sequence before implementation."
---

# Design from foundations

Choose the foundations that make the requested behaviour straightforward without locking in speculative decisions.

## Shape the design

- Define the core types and data shapes, then trace how each caller reads or changes them.
- Match structures to the dominant access paths. Make invalid states unrepresentable where the language permits it.
- Identify state ownership. If concurrent actors can change the same state, isolate their writes or define explicit serialisation.
- Remove in-scope dead weight before adding scaffolding.
- Put foundations that benefit every later phase before feature work, such as shared types or necessary test infrastructure.

## Keep it proportional

Converge types and data models, but keep repeated code when an abstraction would encode guesses rather than established behaviour. Prefer explicit coordination inside one coherent abstraction over special cases spread across callers.

State the chosen foundation, rejected alternatives and implementation sequence. If the user asked for implementation, build from that foundation. Otherwise stop at the design.
