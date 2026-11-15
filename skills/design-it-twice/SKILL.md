---
name: design-it-twice
description: Compare several different interface designs for a module before committing to one.
disable-model-invocation: true
---

# Design it twice

The first interface is unlikely to be the best, so compare genuinely different designs for the chosen module before committing to one. Read the engineering [Design](../engineering/references/design.md) reference first, and use the repository's documented domain vocabulary.

Change no production code while comparing, even when the same request asks for implementation. Finish the comparison and recommendation first, then continue with the recommended design when it fits the established constraints and authority.

## Establish the problem

Start only when the module and the design problem are chosen. Read the current interface, callers, implementation, tests, and governing documentation until you can state:

- the behaviour and constraints every design must preserve;
- the decisions the module should hide;
- its dependencies and their categories from the Design reference;
- the callers and tests that will cross the seam;
- the problems the new interface must solve.

Explain this problem space to the user, with a small type or code sketch when it makes the constraints concrete. The sketch frames the information involved without proposing the winning interface.

## Produce independent designs

Start with two designs for a straightforward decision. Add another only when a meaningful trade-off remains unexplored or the user asks. Give each designer the same factual brief, a different constraint, and a fresh context when the tool supports one, with no sight of another design or the answer you expect. Designers read the code and change nothing.

Alternate the designs between providers when T3's orchestration tools allow it, so they differ by model as well as by constraint. Give the first to a native subagent on the session's model, send the second through the engineering [Cross-provider delegation](../engineering/references/cross-provider-delegation.md) reference with `role: "design"`, and keep alternating. When a cross-provider design falls back, produce it on the session's provider. Name each design's provider when presenting it. Without delegation, develop the alternatives yourself in sequence and say that they weren't generated independently.

Use these constraints unless the problem calls for a stronger distinction:

1. Minimise the interface. Aim for one to three entry points and put as much behaviour as possible behind each.
2. Maximise supported variation and extension without moving implementation decisions into callers.
3. Optimise for the most common caller so the default case is trivial.
4. When remote or external dependencies matter, design around the necessary ports and adapters.

Each design gives its interface, with types, invariants, ordering, and error modes, a usage example for a representative caller, what it hides, its dependency and adapter strategy, how it is tested through the interface, and its trade-offs, including where depth or locality stays weak. Reject designs that don't differ in where the seam sits, what callers know, how state or operations are represented, or which decisions the module owns.

## Compare and recommend

Present each design, then compare them on the same criteria: interface size and caller knowledge, depth, locality of decisions and change, seam placement and dependency handling, testability through the interface, fit with current requirements and likely change, and total complexity across the affected system.

Unless the choice is clear and cheap to undo, ask a contrarian to argue against your pick, as the [Cross-provider delegation](../engineering/references/cross-provider-delegation.md#contrarian) reference describes. Give it the problem space, each design's interface, usage example, and main trade-offs, and your comparison.

Recommend one design and say why it wins. Propose a hybrid when it combines compatible strengths without widening the interface or keeping two competing paths. Don't stop at a menu of options. Ask only about unresolved decisions that would change the outcome or exceed your authority.
