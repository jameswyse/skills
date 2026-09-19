---
name: design-it-twice
description: Compare alternative interfaces for a settled module design problem when several designs are requested.
---

# Design it twice

Ousterhout calls this "Design It Twice" because the first interface is unlikely to be the best. Compare genuinely different designs before committing to one.

Use the "engineering" skill. Read [Deep modules](../engineering/references/deep-modules.md) before framing the alternatives. Use the repository's documented domain vocabulary when it exists.

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

Read the engineering [delegation guidance](../engineering/references/execution.md#delegate-bounded-work). This workflow requests independent design work within the user's scope when delegation is available and permitted. Start with two distinct designs for a straightforward decision. Add another only when a meaningful trade-off remains unexplored or the user requests more alternatives.

When delegating, give each subagent the same factual technical brief and a different design constraint. Use fresh contexts when supported. Do not show them another design or the expected recommendation. When delegation is unavailable or restricted, develop the alternatives sequentially and disclose that they were not independently generated. Do not stop merely because subagents are unavailable.

Use these constraints unless the problem calls for a stronger distinction:

1. Minimise the interface. Aim for one to three entry points and maximise leverage per entry point.
2. Maximise supported variation and extension without moving implementation decisions into callers.
3. Optimise for the most common caller so the default case is trivial.
4. When remote or external dependencies matter, design around necessary ports and adapters.

Require each design to provide:

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

If implementation was already requested, continue with the recommended design when it fits the established constraints and authority. Ask only about unresolved decisions that would change the outcome or exceed that authority.
