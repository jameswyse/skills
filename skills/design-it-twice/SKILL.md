---
name: design-it-twice
description: "Design several genuinely different interfaces for a chosen module in parallel, compare their depth, locality, seam placement, and trade-offs, then recommend one. Use when the user asks for alternative interface designs, several distinct designs, or Design It Twice, or when another skill routes a settled design problem here. Do not use for routine implementation, broad codebase scans, or before the constraints are understood."
---

# Design it twice

Ousterhout calls this "Design It Twice" because the first interface is unlikely to be the best. Compare genuinely different designs before committing to one.

Apply `$engineering-practices`. Read [Deep modules](../engineering-practices/references/deep-modules.md) before framing the alternatives. Use the repository's documented domain vocabulary when it exists.

Do not change production code while comparing designs. If the user also requested implementation, finish the comparison and recommendation first.

## Establish the problem

Start only when the module and design problem are chosen. Read the current interface, callers, implementation, tests, and governing documentation until these facts are clear:

- The behaviour and constraints every design must preserve.
- The decisions the module should hide.
- The dependencies and their deep-module categories.
- The callers and tests that will cross the seam.
- The current problems the new interface must solve.

Explain this problem space to the user. Include a small illustrative type or code sketch when it makes the constraints concrete. The sketch must frame the information involved without proposing the winning interface.

## Produce independent designs

Spawn at least three subagents in parallel. Give each subagent the same factual technical brief and a different design constraint. Do not show them another design or the expected recommendation.

Use these constraints unless the problem calls for a stronger distinction:

1. Minimise the interface. Aim for one to three entry points and maximise leverage per entry point.
2. Maximise supported variation and extension without moving implementation decisions into callers.
3. Optimise for the most common caller so the default case is trivial.
4. When remote or external dependencies matter, design around necessary ports and adapters.

Require each subagent to provide:

1. The interface, including types, methods, parameters, invariants, ordering, and error modes.
2. A usage example for a representative caller.
3. The behaviour and decisions hidden inside the implementation.
4. The dependency and adapter strategy.
5. The testing strategy through the interface.
6. The trade-offs, including where depth, leverage, or locality remains weak.

Reject superficial variations. The designs must differ in where the seam sits, what callers know, how state or operations are represented, or which decisions the module owns.

## Compare and recommend

Present each design separately before comparing them. Use the same criteria for every design:

- Interface size and caller knowledge.
- Depth and leverage.
- Locality of decisions and change.
- Seam placement and dependency handling.
- Testability through the interface.
- Fit with current requirements and likely change.
- Total complexity across the affected system.

Recommend the strongest design and explain why it wins. Propose a hybrid when it combines compatible strengths without widening the interface or preserving two competing paths. Do not stop at a menu of options.
