# Architecture HTML report format

Build the report with the "html-report" skill. This file owns what the architecture report says. Write the body to `<tmpdir>/architecture-review-<timestamp>.body.html` and build `<tmpdir>/architecture-review-<timestamp>.html`.

## Sections

1. **Header.** Eyebrow `Architecture review`, the repository name as the title, then date, revision, working-tree state, and requested scope.
2. **Summary.** Answer in one or two sentences: how many candidates are worth doing and which to start with, naming the evidence that puts it first. Counts by strength, such as `Strong` and `Worth exploring`, plus coverage gaps when there are any.
3. **Candidates.** Qualified candidates, ranked, as the html-report skill lays out ranked items. The first is the `.lead-item` with a `Start here` badge.
4. **How this was checked.** A two-column table of major areas with a verdict badge each: `Candidate`, `No candidate`, or `Not verified` with the reason as a note. Follow it with the evidence that limits confidence, such as an ADR conflict or a test not run. Put the full list of callers, tests, and documents consulted in a closed `details.more`.

Do not calculate an architecture-health score. If no candidate qualifies, say so in the summary and keep only the checks section.

## Candidate

- **Title.** A short name for the deepening, such as "Deepen order intake behind one interface".
- **Badges.** Strength: `Strong` as `good`, `Worth exploring` as `warn`, `Speculative` as neutral. One dependency tag as neutral: `In-process`, `Local-substitutable`, `Remote and owned`, or `External and unowned`.
- **Proposal callout.** What the module absorbs and what callers stop knowing. Two or three bullets.
- **Fields.**
  - `Evidence`: the caller coordination, leaked knowledge, special cases, change pain, defects, or test gap that qualified it. Counts and similar shapes are supporting evidence only.
  - `Wins`: at most three bullets naming locality, depth, interface reduction, or a testing gain.
  - `Files`: exact files, modules, and symbols.
- **Conflict.** When the candidate contradicts an ADR or documented rule, add a `.callout.warn` titled with the document, stating the rule and why the evidence justifies reconsidering it.
- **Diagram.** A `.compare` with `Current` and `Proposed` figures. Give each a one-line caption that states the change in text.

Omit a separate "why it ranks here" field. The summary explains the first choice, and order explains the rest. Keep proposed interface signatures out of the report.

## Diagrams

Draw with the `.flow`, `.node`, `.module`, and `.layers` diagram classes.

- **Call flow.** A `.flow` of current steps, with `.node.leak` where knowledge crosses a seam. Explain every leak in the caption. The proposed side wraps the absorbed steps as `.node.faded` inside one `.module`.
- **Layered shallowness.** `.layers` with several thin bands for the current view and one `deep` band for the proposal.
- **Dependencies.** When the graph has branches or cycles those classes cannot show, list the edges that matter in a two-column table.

If a diagram needs a paragraph to be understood, redraw it.

## Wording

Use the terms from the [vocabulary](SKILL.md) exactly: `module`, `interface`, `implementation`, `depth`, `deep`, `shallow`, `seam`, `adapter`, and `locality`. Keep exact framework, protocol, repository, and domain names.

Write phrases such as "Order intake module is shallow. Its interface nearly matches the implementation." and "The deepened module gives 12 callers one interface." Do not write "easier to maintain" or "cleaner code".
