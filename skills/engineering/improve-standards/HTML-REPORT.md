# Standards HTML report format

Build the report with the ux skill's [HTML reports](../ux/references/html-reports.md) guidance. It owns the design, components, build script, verification, and delivery. This file owns what the standards report says. Write the body to `<tmpdir>/standards-review-<timestamp>.body.html` and build `<tmpdir>/standards-review-<timestamp>.html`.

## Sections

1. **Header.** Eyebrow `Engineering standards review`, the repository name as the title, then date, revision, working-tree state, and requested scope.
2. **Summary.** Answer in one or two sentences: how many improvements are worth making and which to start with, naming its effect. Counts by strength.
3. **Findings.** One `.item` per candidate, ranked. The first is the `.lead-item` with a `Start here` badge.
4. **Follow-ups.** Only when present: a short list of module-depth, seam, or interface observations for the user-invoked "improve-architecture" skill, and tree, placement, or naming observations for "improve-organisation". One line each, unranked.
5. **How this was checked.** The declared and active Node.js and package-manager versions and whether they matched. Then a checks table with the command or interaction, result badge, `Fresh` or `Cached`, and what it established. Add a `Not run` row for each important build, runtime, browser, or integration path that was skipped. Follow it with areas sampled or excluded when they limit what the findings can claim.

Searches, documentation reading, and source inspection are review work, not checks. A Turbo task count needs its command and what the tasks verified. Never label the codebase `Clean` from partial checks. If no candidate is worth doing, say so in the summary and keep only the checks section.

## Finding

- **Title.** The improvement, such as "Derive completion from one state".
- **Badges.** Strength: `Strong` as `good`, `Worth exploring` as `warn`, `Speculative` as neutral. Effort `Small`, `Medium`, or `Large` and risk `Low`, `Medium`, or `High` as neutral, with demonstrated `High` risk as `risk`.
- **Fix callout.** The smallest coherent source fix, ending with what it removes, prevents, or makes verifiable. Use bullets when the fix has parts.
- **Fields.**
  - `Standard`: the exact repository rule, engineering skill section, or engineering reference. Never cite the engineering skill without the rule.
  - `Evidence`: only the fragment, tool result, or repeated pattern that proves the problem.
  - `Files`: exact files and symbols.
  - `Verify`: the focused command and the behaviour it observes.
- **Comparison.** For a local code change, a `.compare` of exact current code beside a concrete proposed excerpt, each limited to the lines that show the changed decision. Omit it for operational, dependency, cross-cutting, or uncertain changes where an excerpt would misrepresent the work.

Use a diagram only when a relationship is clearer drawn than written:

- several duplicated values feeding one owner, as a `.flow` into a `.module`;
- representable invalid states, as a small table of current and legal combinations;
- a failure, lifecycle, or retry path, as a Mermaid sequence diagram;
- a test path that bypasses production behaviour, as two `.flow` rows in a `.compare`.

## Wording

State the observed problem and the source fix. Name the removed branch, consolidated source of truth, prevented invalid state, improved failure context, or verified behaviour. Avoid "cleaner code", "better practice", and "more maintainable". Keep exact paths, symbols, commands, and package names.
