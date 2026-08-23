---
name: improve-codebase-architecture
description: Review an entire codebase for deep-module and seam improvements, present them in a visual HTML report, then grill through the selected candidate. Use recent changes or a specific repository area only when the user explicitly requests that scope.
---

# Improve codebase architecture

Find architectural friction and propose **deepening opportunities**, which are refactors that turn shallow modules into deep ones. The aim is testability and AI navigability.

Apply `$engineering`. Read [Deep modules](../engineering/references/deep-modules.md) before assessing candidates. This workflow uses the project's domain model and the deep-module vocabulary:

- Use **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, and **locality** as the deep-module reference defines them. Apply the deletion test before calling a module shallow. Classify dependencies before recommending a seam or adapter.
- The domain language in the repository, if present, gives names to good seams.

## Process

### 1. Establish the scope

Review the entire codebase by default. Inventory the repository's projects, packages, entrypoints, domain areas, tests, and configuration. Inspect every major area at a useful level before ranking candidates. State any area that the review could not inspect as a coverage gap.

Use a narrower scope only when the user explicitly requests one:

- If the user asks to review recent changes or commits, inspect the requested history and the affected paths.
- If the user names a repository area, module, subsystem, or problem, inspect that area and the callers or dependencies needed to judge it.

Do not use Git history, the current issue, or the working tree to narrow an unqualified invocation. Inspect the working tree only to preserve unrelated work and describe the reviewed state.

Read the project's instructions, documentation, architecture guidance, ADRs, and domain glossary before exploring the code.

### 2. Explore

Then spawn an explorer subagent to inspect the codebase. Follow evidence from names, imports, callers, tests, configuration, and documentation. Note where understanding becomes difficult:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted only for testability while the real bugs remain in caller coordination with no **locality**?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow. Would deleting it concentrate complexity or merely move it? A module earns its place when deletion would spread its complexity across callers.

### 3. Present candidates as an HTML report

Write one HTML file to the operating system's temporary directory so nothing enters the repository. Resolve the directory from `$TMPDIR`, falling back to `/tmp` on Unix or `%TEMP%` on Windows. Write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it with `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows. Tell the user the absolute path.

The report is one static HTML file. When network access is available, load Tailwind and Mermaid from CDNs. Use Mermaid when a graph, flow, or sequence communicates the structure clearly. Without network access, use inline CSS and SVG. Mix Mermaid with hand-crafted CSS and SVG visuals when each suits a different relationship. Mermaid suits call graphs, dependencies, and sequences. Hand-built elements suit mass diagrams, cross-sections, and call-graph collapse. Give each candidate a **before-and-after visualisation**.

Order the report for an engineer choosing what to explore:

1. Header and repository state.
2. Full-width review boundary and evidence or verification.
3. Compact candidate counts and the top recommendation.
4. Ranked candidates.
5. Remaining coverage gaps.

The review boundary states the requested scope, major areas inspected, sampled or excluded areas, and coverage gaps. Evidence or verification names the inspected callers, tests, documentation, deletion-test result, and any commands or runtime paths that affect confidence. Keep both sections full width and separate.

For each candidate, render a card with:

- **Files.** Name the files and modules involved.
- **Problem.** Explain why the current architecture is difficult to change or understand.
- **Proposed deepening.** Highlight the proposed change in plain English.
- **Benefits.** Explain the locality, leverage, and testing gains.
- **Before-and-after diagram.** Draw a full-width side-by-side comparison of the shallowness and proposed deepening.
- **Recommendation strength.** Render `Strong`, `Worth exploring`, or `Speculative` as a badge.

Place a compact horizontal **Top recommendation** before the candidate cards. Name the first candidate to explore, explain why it comes first, and link to the full candidate. Keep diagrams in the candidate card.

**Use the repository's documented domain vocabulary for the domain and the deep-module vocabulary for the architecture.** Preserve exact framework, protocol, domain, and symbol names. When `module` names the architectural concept, write "the Order intake module". When the report names an existing `OrderService` symbol, keep `OrderService`.

**Documentation conflicts.** If a candidate contradicts a documented rule or ADR, include it only when the observed problem justifies reconsideration. Mark the conflict in a warning callout, such as _"Contradicts XYZ. Reconsider it because..."_ Do not list theoretical refactors that documentation already rules out.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do not propose interfaces yet. After writing the file, ask the user, "Which of these would you like to explore?"

### 4. Grilling loop

Once the user picks a candidate, apply `$grilling` to examine its constraints, dependencies, deepened module, seam contents, and surviving tests.

After the user confirms a decision, offer to update the domain documentation during the same loop. The decision does not itself authorise file changes. Update documentation only when the user asks you to record it.

- When a deepened module uses a concept missing from the repository's domain vocabulary, offer to add the term in the appropriate place.
- When the conversation sharpens a vague term, offer to update the repository's domain vocabulary.
- When the user rejects a candidate for a reason future reviews need, offer to record that reason in the documentation. Ask, _"Should I record this in the documentation so future architecture reviews do not suggest it again?"_ Skip temporary reasons such as "not worth it right now" and self-evident reasons.
- When the candidate needs a new interface with several credible shapes, offer Design It Twice before converging. If the user accepts or directly requests alternatives, apply `$design-it-twice`.
