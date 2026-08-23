---
name: improve-codebase-architecture
description: Review an entire codebase for deep-module and seam improvements, present them in a visual HTML report, then grill through the selected candidate. Use recent changes or a specific repository area only when the user explicitly requests that scope.
---

# Improve codebase architecture

Find architectural friction and propose **deepening opportunities**, which are refactors that turn shallow modules into deep ones. The aim is testability and AI navigability.

Apply `$engineering`. Read [Deep modules](../engineering/references/deep-modules.md) before assessing candidates. This workflow uses the project's domain model and the deep-module vocabulary:

- Use **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, and **locality** as the deep-module reference defines them. Apply the deletion test before calling a module shallow. Classify dependencies before recommending a seam or adapter.
- The domain language in the repository, if present, gives names to good seams.

Recommend `$improve-codebase-organisation` when the primary problem is tree navigation, file or directory naming, companion-file ownership, or shallow filesystem structure without a qualified deepening. Organisation evidence may support an architecture candidate, but it does not bypass the qualification gate.

## Process

### 1. Establish the scope

Review the entire codebase by default. Inventory the repository's projects, packages, entrypoints, domain areas, tests, and configuration. Derive major areas from the repository's own application, package, domain, capability, and entrypoint boundaries rather than arbitrary folder or file counts. Turn that inventory into a coverage map. Each major area must end with one of these verdicts:

- A candidate passed the qualification gate below.
- The area was inspected and no candidate passed, with a short reason.
- The area remains a coverage gap, with the missing evidence named.

Use a narrower scope only when the user explicitly requests one:

- If the user asks to review recent changes or commits, inspect the requested history and the affected paths.
- If the user names a repository area, module, subsystem, or problem, inspect that area and the callers or dependencies needed to judge it.

Whole-codebase scope does not require equal inspection depth. Use Git history, recurring defects, test gaps, operational pain, and documented follow-ups to prioritise deep inspection and rank candidates. These signals guide attention but do not exclude quieter areas that have strong current evidence. Do not let the current issue or working tree define the bounds of an unqualified review. Inspect the working tree to preserve unrelated work and describe the reviewed state.

Read the project's instructions, documentation, architecture guidance, ADRs, and domain glossary before exploring the code.

### 2. Explore and qualify

Start with a fresh discovery pass. If prior architecture reports or recent review findings are available, treat their candidates as leads rather than the current frontier. After fresh discovery, compare each prior `Strong` or `Worth exploring` candidate with the current code. Mark it as resolved, retained, or rejected, and cite the evidence for that judgement.

For a whole-codebase review, partition exploration into coherent areas such as product domains, platform code, integrations, authoring tools, and shared packages. When delegation is available and authorised, give separate explorers non-overlapping areas. Otherwise inspect one area at a time and record its verdict before moving on. Independently verify the strongest candidates and their callers before ranking them.

Follow evidence from names, imports, callers, tests, configuration, documentation, and change history. Note where understanding becomes difficult:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted only for testability while the real bugs remain in caller coordination with no **locality**?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply this qualification gate to each proposed deepening:

1. **Current evidence.** Show repeated caller decisions, ordering, validation, recovery, leaked implementation knowledge, coordination defects, or tests that reproduce caller coordination. File counts and similar shapes are supporting evidence only.
2. **Current structure test.** For an existing module, apply the deletion test to that module. For a missing owner, trace the required decisions and ordering across current callers. Show that the same knowledge is repeated or changes together. Do not pass a candidate by inventing a module and then observing that deleting it would restore today's duplication.
3. **Interface reduction.** Name the facts, states, ordering rules, or failure handling that callers would stop knowing, without designing a signature. Confirm that the proposal reduces total interface knowledge rather than moving it.
4. **Stable ownership.** Show that the proposed module owns one coherent body of domain or application knowledge. Treat repetition-only schema or configuration consolidation as an observation unless the repeated code changes together because it represents one decision.
5. **Observable seam.** Name the callers and the behaviour that tests could protect through the proposed interface.

Reject a candidate that does not pass the gate. Do not fill a candidate quota.

Group or explicitly compare candidates that would own overlapping decisions. Do not present competing owners for the same coordination unless choosing between them is the useful question.

Rank the remaining candidates by observed maintenance pain, caller knowledge removed, user or operational impact, improvement to the test surface, net complexity reduction, confidence, and implementation risk. Use qualitative evidence rather than a numeric architecture score. A `Strong` candidate has direct evidence of current coordination and a credible owner. Use `Worth exploring` when important evidence or the owner remains uncertain. Use `Speculative` only when the uncertainty itself is useful to show, and never let it displace a qualified candidate.

### 3. Present candidates as an HTML report

Before writing HTML, read [HTML-REPORT.md](HTML-REPORT.md) in full. Start from its scaffold and preserve its page shell, colour system, type scale, section surfaces, and spacing. Treat that file as a visual contract, not design inspiration. Add custom CSS only inside an architecture diagram when the scaffold cannot express the relationship.

Write one HTML file to the operating system's temporary directory so nothing enters the repository. Resolve the directory from `$TMPDIR`, falling back to `/tmp` on Unix or `%TEMP%` on Windows. Write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it with `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows. Tell the user the absolute path.

The report is one static HTML file. When network access is available, load Tailwind and Mermaid from CDNs. Use Mermaid when a graph, flow, or sequence communicates the structure clearly. Without network access, use inline CSS and SVG. Mix Mermaid with hand-crafted CSS and SVG visuals when each suits a different relationship. Mermaid suits call graphs, dependencies, and sequences. Hand-built elements suit mass diagrams, cross-sections, and call-graph collapse. Keep custom diagram styling local to the diagram. Give each candidate a **before-and-after visualisation**.

Order the report for an engineer choosing what to explore:

1. Header and repository state.
2. Full-width review boundary and evidence or verification.
3. Compact candidate counts and the top recommendation.
4. Ranked candidates.
5. Remaining coverage gaps.

The review boundary states the requested scope and the coverage-map verdict for each major area. Evidence or verification names the inspected callers, tests, documentation, current-structure test result, and any commands or runtime paths that affect confidence. Include change or defect signals and a prior-candidate comparison when available. Keep both sections full width, separate, and single-column inside. Use one description list or table instead of a grid of mini-cards.

For each candidate, render a card with:

- **Files.** Name the files and modules involved.
- **Current evidence.** Use short bullets to name the caller coordination, leaked knowledge, change pain, defects, or test gap that passed the qualification gate.
- **Problem.** Explain why the current architecture is difficult to change or understand.
- **Proposed deepening.** Highlight the proposed change in plain English.
- **Benefits.** Explain the locality, leverage, and testing gains.
- **Why it ranks here.** State why this candidate outranks or follows the others.
- **Before-and-after diagram.** Draw a full-width side-by-side comparison of the shallowness and proposed deepening.
- **Recommendation strength.** Render `Strong`, `Worth exploring`, or `Speculative` as a badge.

Place a compact horizontal **Top recommendation** before the candidate cards. Name the first candidate to explore, explain which ranking evidence puts it first, and link to the full candidate. Keep diagrams in the candidate card.

Use the same light editorial system as the standards report: a stone page, a centred `max-w-6xl` document, slate text, white section surfaces, an indigo accent, restrained borders, and small shadows. Keep the header title at `text-4xl`. Use a compact text line for candidate counts. Repository inventory may support the review, but do not turn file counts or test counts into dashboard metrics.

Do not replace the visual system with a dark theme, gradient page background, oversized display title, full-viewport dashboard, glass panels, or metric-card row. Dark surfaces belong only to code blocks and individual diagram elements.

**Use the repository's documented domain vocabulary for the domain and the deep-module vocabulary for the architecture.** Preserve exact framework, protocol, domain, and symbol names. When `module` names the architectural concept, write "the Order intake module". When the report names an existing `OrderService` symbol, keep `OrderService`.

**Documentation conflicts.** If a candidate contradicts a documented rule or ADR, include it only when the observed problem justifies reconsideration. Mark the conflict in a warning callout, such as _"Contradicts XYZ. Reconsider it because..."_ Do not list theoretical refactors that documentation already rules out.

Do not propose interfaces yet. After writing the file, ask the user, "Which of these would you like to explore?"

Before handoff, inspect the rendered report at a desktop width and at `320px`. Confirm that it matches the HTML report visual contract, the page has no horizontal overflow, the review boundary and evidence remain single-column, candidate columns stack in reading order, and diagrams remain legible. Fix the report before opening it for the user when any check fails.

### 4. Grilling loop

Once the user picks a candidate, apply `$grilling` to examine its constraints, dependencies, deepened module, seam contents, and surviving tests.

After the user confirms a decision, offer to update the domain documentation during the same loop. The decision does not itself authorise file changes. Update documentation only when the user asks you to record it.

- When a deepened module uses a concept missing from the repository's domain vocabulary, offer to add the term in the appropriate place.
- When the conversation sharpens a vague term, offer to update the repository's domain vocabulary.
- When the user rejects a candidate for a reason future reviews need, offer to record that reason in the documentation. Ask, _"Should I record this in the documentation so future architecture reviews do not suggest it again?"_ Skip temporary reasons such as "not worth it right now" and self-evident reasons.
- When the candidate needs a new interface with several credible shapes, offer Design It Twice before converging. If the user accepts or directly requests alternatives, apply `$design-it-twice`.
