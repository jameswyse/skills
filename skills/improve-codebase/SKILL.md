---
name: improve-codebase
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
---

# Improve codebase

Find architectural friction and propose **deepening opportunities**, which are refactors that turn shallow modules into deep ones. The aim is testability and AI navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Call the Skill tool with "codebase-design" for the architecture vocabulary. It defines **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, and **locality**. It also defines the deletion test, "the interface is the test surface", and "one adapter means a hypothetical seam, two means a real seam". Use these terms exactly in every suggestion. Do not substitute "component", "service", "API", or "boundary".
- The domain language in the repository, if present, gives names to good seams.

## Process

### 1. Explore

**Scope the scan with YAGNI.** Deepening a module pays off by making future changes easier, so give extra weight to recently changed parts of the codebase. Decide *where* to look before scanning:

- If the user named a module, subsystem, or problem, start there and skip the inference below.
- Otherwise, inspect enough commit history with `git log --oneline` to find frequently changed files and areas. Start with those paths. Inspect more paths when changes are scattered without a clear centre.

Read the project's documentation or domain glossary first.

Then spawn an explorer subagent to inspect the codebase. Follow evidence from names, imports, callers, tests, and change history. Note where understanding becomes difficult:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted only for testability while the real bugs remain in caller coordination with no **locality**?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow. Would deleting it concentrate complexity or merely move it? A module earns its place when deletion would spread its complexity across callers.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the operating system's temporary directory so nothing enters the repository. Resolve the directory from `$TMPDIR`, falling back to `/tmp` on Unix or `%TEMP%` on Windows. Write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it with `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows. Tell the user the absolute path.

Use **Tailwind via CDN** for layout and styling. Use **Mermaid via CDN** when a graph, flow, or sequence communicates the structure clearly. Mix Mermaid with hand-crafted CSS and SVG visuals. Mermaid suits call graphs, dependencies, and sequences. Hand-built elements suit mass diagrams, cross-sections, and collapse animations. Give each candidate a **before-and-after visualisation**.

For each candidate, render a card with:

- **Files.** Name the files and modules involved.
- **Problem.** Explain why the current architecture is difficult to change or understand.
- **Solution.** Describe the proposed change in plain English.
- **Benefits.** Explain the locality, leverage, and testing gains.
- **Before-and-after diagram.** Draw a custom side-by-side comparison of the shallowness and proposed deepening.
- **Recommendation strength.** Render `Strong`, `Worth exploring`, or `Speculative` as a badge.

End the report with a **Top recommendation** section that names the first candidate to tackle and explains why.

**Use the repository's documented domain vocabulary for the domain and the `codebase-design` vocabulary for the architecture.** If the domain vocabulary defines "Order", write "the Order intake module", not "the FooBarHandler" or "the Order service".

**Documentation conflicts.** If a candidate contradicts a documented rule or ADR, include it only when the observed problem justifies reconsideration. Mark the conflict in a warning callout, such as _"Contradicts XYZ. Reconsider it because..."_ Do not list theoretical refactors that documentation already rules out.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do not propose interfaces yet. After writing the file, ask the user, "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, call the Skill tool with "grilling" to examine its constraints, dependencies, deepened module, seam contents, and surviving tests.

After the user confirms a decision, update the domain documentation during the same loop.

- When a deepened module uses a concept missing from the repository's domain vocabulary, add the term in the appropriate place.
- When the conversation sharpens a vague term, update the repository's domain vocabulary immediately.
- When the user rejects a candidate for a reason future reviews need, offer to record that reason in the documentation. Ask, _"Should I record this in the documentation so future architecture reviews do not suggest it again?"_ Skip temporary reasons such as "not worth it right now" and self-evident reasons.
- To explore alternative interfaces for the deepened module, call the Skill tool with "codebase-design" and use its design-it-twice parallel subagent pattern.
