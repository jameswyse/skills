---
name: design
description: "User-facing product and interface design router for UX, UI, interaction, visual presentation, accessibility, copy, and motion. Apply for interface design, implementation, or review. For implementation, also apply $engineering. For change reviews, ask the user to invoke $interface-review. For variants, ask the user to invoke $variant. For interface explanations, ask the user to invoke $explain-interface. Do not use for software architecture, APIs, schemas, modules, or data models."
---

# Design

Route user-facing product and interface work to the smallest installed specialist set that covers the request. External skills are optional. Apply their instructions when available, and continue without recreating a missing skill from memory.

For interface implementation, also apply `$engineering`. It owns implementation quality, architecture, data, types, tests, dependencies, and tooling. This skill owns experience, interaction, visual presentation, accessibility, interface copy, and motion decisions.

## Set the target

For product, UX, or feature-scope tradeoffs, read [Experience first](references/experience.md) before choosing what to build. It governs the intended experience. The specialist skills below govern execution within their domains.

## Route the task

Let project-specific design rules govern when they differ from an external skill.

### Interface skills

- `interface-review`: review uncommitted changes, a branch, a commit range, or a pull request for interface quality. This skill is user-invoked. If it fits and the user did not name it, ask them to invoke `$interface-review`.
- `better-interface`: review a whole screen, flow, feature, or repository. It routes the review to all installed `better-*` domain owners and consolidates their findings.
- `variant`: build several genuinely different versions of one piece of UI behind a picker. This skill is user-invoked. If it fits and the user did not name it, ask them to invoke `$variant`.
- `explain-interface`: explain how a live interface or named visual effect was built, or reconstruct it from a screenshot. This skill is user-invoked. If it fits and the user did not name it, ask them to invoke `$explain-interface`.
- `better-accessibility`: own accessibility, keyboard, focus, semantics, assistive technology, and reduced-motion requirements.
- `better-layout`: own structure, spacing, grouping, responsive layout, and spatial RTL.
- `better-writing`: own user-facing interface copy, terminology, voice, labels, errors, and empty states.
- `better-typography`: own typefaces, type scales, text rendering, wrapping, truncation, and text spacing.
- `better-colors`: own palettes, colour tokens, theming, gradients, semantic colour, and measured contrast pairs.
- `better-ui`: own general visual polish, surfaces, radii, shadows, icons, optical alignment, and motion when no animation skill has scoped authority.

### Animation skills

- `animate`: build a requested animation or transition.
- `review-animations`: review existing animation or motion code.
- `improve-animations`: audit motion across a codebase and write improvement plans.
- `find-animation-opportunities`: find places where motion would help and reject places where it would not.
- `animation-vocabulary`: name an animation or motion effect from a description.

For an animation-only request, use the selected animation skill as the sole motion and polish specialist. Add an interface skill only when the request also contains work in that skill's non-motion domain.

## Resolve overlap

Use one authority for each design decision.

- When motion is the explicit subject, the selected animation skill owns motion values and behaviour. Do not also apply `better-ui` motion rules.
- The relevant interface skills still own accessibility, layout, typography, colour, and interface copy. `better-accessibility` owns reduced-motion requirements.
- For a holistic interface review without an explicit motion focus, let `better-interface` and its `better-ui` handoff own motion within that review.
- Apply `$writing` as the prose baseline. For user-facing interface copy, let `better-writing` govern UX-copy decisions when it is available.
