# Skill mechanics

This is the skill-specific branch of [Agent instructions](agent-instructions.md). It covers frontmatter, invocation choice, and router skills. The universal writing guidance remains in [Agent instructions](agent-instructions.md).

## Invocation

Two choices trade the two loads:

- A **model-invoked** skill keeps a `description`, so the agent can invoke it autonomously and other skills can reach it. You can still type its name. Model invocation always includes user invocation. A description adds agent discovery without removing human access. The description is the skill's top-level context pointer and stays loaded at all times. This permanent context load buys discoverability. A model-invoked skill can also hold shared reference that several skills need. Write a model-facing description that carries the trigger branches. The pointer-writing rules in `SKILL.md` apply in full.
- A **user-invoked** skill keeps its description out of the agent's reach. Only a human typing its name can invoke it, and no other skill can. This removes context load but spends cognitive load because the human must remember the skill exists.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must. If it only ever fires by hand, make it user-invoked and pay no context load.

Shared reference needed by two user-invoked skills can live in neither because one cannot invoke the other. Put it in a plain file outside the skill system that either skill can point to.

## Splitting by invocation

The sequence rules for splitting live in `SKILL.md`. For invocation, split off a model-invoked skill when a distinct leading word should trigger it independently or when another skill must reach it. Use a trigger word that appears in real prompts. The new always-loaded description adds context load, so independent reach must justify that cost.

## Router skills

When user-invoked skills become hard to remember, use a **router skill**. This single user-invoked skill names the others and explains when to use each one. The human then remembers one skill instead of many. A router can only suggest another user-invoked skill. It cannot invoke one because those skills have no agent-visible description.
