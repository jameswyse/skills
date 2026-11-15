---
name: ux
description: Use when designing, building, or reviewing a user-facing interface, including interaction, visual design, accessibility, interface copy, and motion.
---

# UX

Route user-facing product and interface work to the smallest installed specialist set that covers the request. External skills are optional. Apply their instructions when available, and continue without recreating a missing skill from memory.

For interface implementation, use the "engineering" skill. It owns implementation quality, architecture, data, types, tests, dependencies, and tooling. This skill owns experience, interaction, visual presentation, accessibility, interface copy, and motion decisions.

## Set the target

For product, UX, or feature-scope tradeoffs, read [Experience first](references/experience.md) before choosing what to build. It governs the intended experience. The specialist skills below govern execution within their domains.

## Route the task

Let project-specific design rules govern when they differ from an external skill.

### HTML reports

For a generated HTML report, use the "html-report" skill.

### Interface skills

The `interface-review`, `variant`, and `explain-interface` skills are user-invoked. Recommend one only when it is available and its workflow matches the request. Otherwise continue with installed specialists that cover the requested domains.

- `interface-review`: review uncommitted changes, a branch, a commit range, or a pull request for interface quality.
- `better-interface`: review a whole screen, flow, feature, or repository. It routes the review to all installed `better-*` domain owners and consolidates their findings.
- `variant`: build several genuinely different versions of one piece of UI behind a picker.
- `explain-interface`: explain how a live interface or named visual effect was built, or reconstruct it from a screenshot.
- `better-accessibility`: own accessibility, keyboard, focus, semantics, assistive technology, and reduced-motion requirements.
- `better-layout`: own structure, spacing, grouping, responsive layout, and spatial RTL.
- `better-writing`: own user-facing interface copy, terminology, voice, labels, errors, and empty states.
- `better-typography`: own typefaces, type scales, text rendering, wrapping, truncation, and text spacing.
- `better-colors`: own palettes, colour tokens, theming, gradients, semantic colour, and measured contrast pairs.
- `better-ui`: own general visual polish, surfaces, radii, shadows, icons, optical alignment, and motion.

## Resolve overlap

Use one authority for each design decision.

- `better-ui` owns motion values and behaviour. `better-accessibility` owns reduced-motion requirements.
- For user-facing interface copy, let `better-writing` govern UX-copy decisions when it is available.

## Avoid generated-page defaults

When the brief and the project's design rules leave a visual choice open, don't spend it on what generated pages reach for whatever the subject:

- The same typefaces: Inter, Roboto, Arial and system UI stacks, Geist and Space Grotesk for sans, and Instrument Serif, Fraunces and Playfair Display for serif display. Choose typefaces for this brief.
- Pill-shaped, fully rounded buttons and tags.

Use one when the brief or the project's design system calls for it.

## Verify native mobile controls on a device

Emulated touch and responsive modes don't show native mobile controls, such as date, time, and select pickers. When a change depends on how one behaves, ask me to check it on a real device before reporting the change done.
