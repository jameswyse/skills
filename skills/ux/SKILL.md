---
name: ux
description: Use when designing, building, or reviewing a user-facing interface, including interaction, visual design, accessibility, interface copy, and motion.
---

# UX

This skill owns experience, interaction, visual presentation, accessibility, interface copy, and motion decisions. "engineering" owns the implementation. Use the smallest set of installed specialist skills that covers the request, let the project's design rules override them, and when one is missing, continue without recreating it from memory.

## Experience first

The product is the experience. When implementation convenience conflicts with user delight, choose delight. The user is the person completing the task, so explain trade-offs from their seat. Foundational thinking governs the order of the work, and this section sets its target.

- Say no to features, controls, and options that don't earn their place, and ship fewer polished features instead of more rough ones.
- Improve the central workflow. Each feature should support it or be removed.
- When the user asked to explore a design, prototype before committing to production code.
- Refine transitions, alignment, spacing, feedback, and error states.

## Route the task

- For a generated HTML report, use "html-report".
- Three interface skills are user-invoked, so you can only recommend them, and only when one is installed and fits the request: `interface-review` reviews uncommitted changes, a branch, a commit range, or a pull request for interface quality. `variant` builds several genuinely different versions of one piece of UI behind a picker. `explain-interface` explains how a live interface or named visual effect was built, or reconstructs it from a screenshot.
- Give each design decision one owner, and load that skill before the edit it governs. Before writing or changing any user-facing text, load `better-writing`. Before changing a transition, animation, icon, or surface detail such as alignment, radius, or shadow, load `better-ui`, which owns motion values and behaviour. Before changing focus, keyboard behaviour, a transition, or an animation, load `better-accessibility`, which owns reduced-motion requirements.

## Avoid generated-page defaults

When the brief and the project's design rules leave a visual choice open, don't spend it on what generated pages reach for whatever the subject:

- The same typefaces: Inter, Roboto, Arial and system UI stacks, Geist and Space Grotesk for sans, and Instrument Serif, Fraunces and Playfair Display for serif display. Choose typefaces for this brief.
- Pill-shaped, fully rounded buttons and tags.

Use one when the brief or the project's design system calls for it.

## Verify native mobile controls on a device

Emulated touch and responsive modes don't show native mobile controls, such as date, time, and select pickers. When a change depends on how one behaves, ask me to check it on a real device before reporting the change done.
