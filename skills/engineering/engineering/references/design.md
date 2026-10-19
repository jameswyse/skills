# Design

Use this reference before a substantial architecture, state, schema, or module-boundary decision, and when judging module depth, placing a seam, choosing adapters, or deciding where tests should observe behaviour. The "code-review" skill's [Code standards](../../code-review/references/code-standards.md) judge the finished result.

## Redesign from the requirement

When a new requirement challenges the current design, design as if the requirement had existed from the start. Keep constraints that still matter, not structure that merely exists. Describe the core types and data shapes the requirement calls for, trace how each caller reads and changes them, then find the smallest coherent migration from the current design. The result should express the requirement through its types, state ownership, and interfaces, not through caller coordination or a special-case layer.

When producing a design, state the chosen foundation, the rejected alternatives, and the implementation sequence.

## Decide whether a module should be deeper

Apply the **deletion test**: imagine deleting the module. If its complexity disappears, it was a pass-through. If its decisions and coordination reappear across callers, it earns its place.

Deepen when callers repeat the same decisions, ordering, validation, or recovery, when bugs arise in coordination between callers and helpers, or when tests must reproduce caller coordination. Don't deepen a cluster merely because it's in-process, has a test replacement, or spans several files. Prefer clear local code when the current shape is easy to change.

A deep module can have internal seams for its implementation and tests. Keep them private and expose only the seam callers need.

## Classify dependencies after the candidate earns deepening

The category decides how to implement and test a chosen deepening. It doesn't justify the deepening.

- **In-process.** Pure computation and in-memory state need no adapter. Test directly through the new interface.
- **Local-substitutable.** Use a local replacement such as PGLite or an in-memory filesystem inside the module's tests, and keep that seam internal. A replacement's existence doesn't justify an external port.
- **Remote and owned.** For a service you control across a network seam, define a port only when the transport varies or must be replaced in tests. Use an HTTP, gRPC, or queue adapter in production and an in-memory adapter in tests.
- **External and unowned.** For a third-party service, put a port at the existing external seam, keep vendor representations inside the production adapter, and use a focused fake in tests.

## Judge whether a seam is real

A seam needs required variation or an external system that changes independently. Two necessary implementations, or an existing network, storage, or third-party boundary, make a seam real. A fake created only to justify a new port is not a second requirement, and a single production adapter behind an interface no caller varies is usually indirection.

Seams expose domain concepts, not wire, storage, or SDK representations. Define ports in the consumer's language, with domain inputs, outputs, and failures. Before adding an adapter, reuse a cohesive one through the narrow type the consumer needs, or extend it when the operation changes for the same reason. Don't split one cohesive adapter into one-method wrappers.

## Test through the interface

The interface is the test surface. When deepening replaces shallow modules, write tests for the preserved behaviour through the new interface, confirm they cover the old observable cases, and delete tests of superseded helpers and internal state. Keep an internal test only for an independently useful algorithm the interface tests can't diagnose clearly.
