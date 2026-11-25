---
name: bake-off
description: Use when the user asks for options for a software design, or when an interface, architecture, or data model choice has several credible designs and would be costly to reverse. Not for names, copy, or visual design.
---

# Bake-off

The first design is unlikely to be the best, so compare genuinely different designs for the chosen problem before committing to one. Read the engineering [Design](../engineering/references/design.md) reference first, and use the repository's documented domain vocabulary.

Change no production code while comparing, even when the same request asks for implementation.

## Decide whether to run it

Run it when the user invokes it or asks for options for a software design. Names, copy, and visual design don't qualify. When they ask for options without naming this skill and the choice is small and cheap to reverse, write the designs yourself instead of delegating them.

Start it yourself only when you have read the code and both of these hold. Then tell the user in one line that you're running it and why, without asking.

- At least two different designs are still credible. A choice that the requirements, the repository's conventions, or an earlier decision by the user already settles doesn't qualify.
- The choice would be costly to reverse, because many callers or other teams' code will depend on it, or because it sets a stored data shape, the owner of important state, or the infrastructure the system runs on.

In a subagent or delegated task, follow the Design reference's rule for those instead.

## Establish the problem

Start only when the design problem is chosen: a module's interface, or an architecture or data model decision. Read the current design, its callers, implementation, tests, and governing documentation until you can state:

- the behaviour and constraints every design must preserve;
- the decisions the design should hide or give one owner;
- its dependencies and their categories from the Design reference;
- the callers, processes, and tests it will affect;
- the problems the new design must solve.

Put this problem space in the designers' brief, with a small type or code sketch when it makes the constraints concrete. The sketch frames the information involved without proposing the winning design. When the user invoked the skill or asked for options, explain the problem space to them too.

## Produce independent designs

Start with two designs for a straightforward decision. Add another only when a meaningful trade-off remains unexplored or the user asks. Give each designer the same factual brief, a different constraint, and a fresh context when the tool supports one, with no sight of another design or the answer you expect. Designers read the code and change nothing. Tell each one not to run this skill, start agents, or delegate, because the Design reference points here.

Alternate the designs between providers when T3's orchestration tools allow it, so they differ by model as well as by constraint. Give the first to a native subagent on the session's model, send the second cross-provider as "delegation" describes, with `role: "design"`, and keep alternating. When a cross-provider design falls back, or a user or repository rule forbids it, produce it on the session's provider. Name each design's provider when presenting it. Without delegation, develop the alternatives yourself in sequence and say that they weren't generated independently.

Reject designs that don't differ in where the seam sits, what callers know, how state or operations are represented, which decisions and state each module owns, or, for an architecture or data model, how it fails, recovers, or migrates. Unless the problem calls for a stronger distinction, use these constraints.

For an interface:

1. Minimise the interface. Aim for one to three entry points and put as much behaviour as possible behind each.
2. Maximise supported variation and extension without moving implementation decisions into callers.
3. Optimise for the most common caller so the default case is trivial.
4. When remote or external dependencies matter, design around the necessary ports and adapters.

Each interface design gives its types, invariants, ordering, and error modes, a usage example for a representative caller, what it hides, its dependency and adapter strategy, how it is tested through the interface, and its trade-offs, including where depth or locality stays weak.

For an architecture or data model:

1. Minimise moving parts. Add no process, store, or dependency that the system can do without.
2. Give each piece of state and its rules one owner, even when that moves code between modules.
3. Optimise for the most likely next change, taken from the requirements or the Git history.
4. When failure or migration is the main risk, design for partial failure, recovery, and a rollout that can be reversed at each step.

Each architecture or data model design gives its components and the owner of each piece of state, the core types or schema, the path of a representative operation, its failure and consistency behaviour, the migration from the current system, how it is tested, and its trade-offs, including what would be costly to reverse.

## Compare and recommend

Compare the designs on the same criteria: caller knowledge and interface size, depth, locality of decisions and change, seam placement and dependency handling, testability, fit with current requirements and likely change, and total complexity across the affected system. For an architecture or data model, add state ownership and consistency, failure and recovery, operating cost, and how far each migration step can be reversed.

Unless the choice is clear and cheap to undo, or you wrote the designs yourself for a small choice, run the contrarian check on your pick, as the Contrarian section of "delegation" describes. Its brief holds the problem space, each design with its usage example or representative operation and main trade-offs, and your comparison. In a run you started, when an advisor will review the same decision, send the advisor that brief instead, and run the contrarian check only if the consult is skipped or fails.

Recommend one design and say why it wins. Propose a hybrid when it combines compatible strengths without adding to what callers know or keeping two competing paths. Don't stop at a menu of options.

A finished bake-off replaces the engineering skill's pause rule for a stored data shape that isn't public. Writing a schema or migration is a two-way door, and running it on production data is a one-way door.

Finish by the first case that applies:

1. **The choice needs the user.** It exceeds your authority, or only they can make it, such as a public interface, product behaviour, new infrastructure, or a one-way door. Present the designs, the comparison, and your recommendation, and ask. Continue work that doesn't depend on the answer.
2. **The user asked for options without telling you to choose.** Present the same, and wait for their pick, even when the request goes on to implementation.
3. **Otherwise**, use the recommended design for the rest of the task. Implement it only when the task includes implementation. A request for a design, comparison, or recommendation ends with the same presentation. In your final account, list the choice, the rejected designs, and why they lost under "Decisions".
