---
name: improve-architecture
description: Audit module depth and architectural seams when requested, across the codebase or a named area.
disable-model-invocation: true
---

# Improve architecture

Find architectural friction and propose **deepening opportunities**, which are refactors that turn shallow modules into deep ones. The aim is testability and AI navigability.

Use the "engineering" skill. Read [Deep modules](../engineering/references/deep-modules.md) before assessing candidates. This workflow uses the project's domain model and the deep-module vocabulary:

- Use **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, and **locality** as the deep-module reference defines them. Apply the deletion test before calling a module shallow. Classify dependencies before recommending a seam or adapter.
- The domain language in the repository, if present, gives names to good seams.

Recommend the user-invoked "improve-organisation" skill when the primary problem is tree navigation, file or directory naming, companion-file ownership, or shallow filesystem structure without a qualified deepening. Organisation evidence may support an architecture candidate, but it does not bypass the qualification gate.

Before naming a proposed module or path, read [Codebase organisation and naming](../engineering/references/organisation-and-naming.md). A `*Contract` or `*Policy` file that only gathers types, constants, schemas, configuration, or flags is an organisation change, not a deepening opportunity.

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

For the report itself, use "ux", including its HTML-report guidance and installed design specialists. Before writing HTML, read [HTML-REPORT.md](HTML-REPORT.md) in full. It owns the scaffold, report contents, visual rules, output location, and render checks. Preserve the scope and coverage verdicts, evidence, ranked candidates, and remaining gaps. Verify the rendered report before presenting its absolute path, or state why visual verification could not run.

If a candidate contradicts a documented rule or ADR, include it only when observed evidence justifies reconsideration. Explain the conflict and reason in the report. Keep exact repository and domain names.

Keep proposed module interface design out of the discovery report. After a review-only request, ask which candidate the user wants to explore. If design or implementation is already authorised and the evidence identifies a candidate within that scope, continue. Ask only when the choice changes the intended outcome or exceeds that authority.

### 4. Grilling loop

For a selected candidate, resolve constraints, dependencies, module ownership, seam contents, and surviving tests from repository evidence. Use the "grilling" skill when the user requests an interview or consequential dependent decisions remain. Preserve its explicit interview pauses in that mode. When those decisions are already settled, proceed with the authorised design or implementation without requiring a new interview.

After the user confirms a decision, record it only when the request covers documentation changes. A discussion-only decision does not itself authorise file changes. During authorised implementation, update affected documentation when needed to keep the change coherent; do not request the same authority again.

- When a deepened module uses a concept missing from the repository's domain vocabulary, offer to add the term in the appropriate place.
- When the conversation sharpens a vague term, offer to update the repository's domain vocabulary.
- When the user rejects a candidate for a reason future reviews need, offer to record that reason in the documentation. Ask, _"Should I record this in the documentation so future architecture reviews do not suggest it again?"_ Skip temporary reasons such as "not worth it right now" and self-evident reasons.
- When the candidate needs a new interface with several credible shapes, offer Design It Twice before converging. If the user accepts or directly requests alternatives, use the "design-it-twice" skill.
