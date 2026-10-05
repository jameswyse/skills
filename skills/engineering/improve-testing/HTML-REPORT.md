# Testing HTML report format

Build the report with the ux skill's [HTML reports](../ux/references/html-reports.md) guidance. It owns the design, components, build script, verification, and delivery. This file owns what the testing report says. Write the body to `<tmpdir>/testing-review-<timestamp>.body.html` and build `<tmpdir>/testing-review-<timestamp>.html`.

## Sections

1. **Header.** Eyebrow `Testing review`, the repository name as the title, then date, revision, working-tree state, and requested scope.
2. **Summary.** Answer in one or two sentences: the most consequential guarantee gap or removal, and what to do first. Counts: tests assessed, removal candidates, tests to improve, and guarantee gaps.
3. **Removal candidates.** Before anything else in the body.
4. **Guarantee gaps.** Weak and missing guarantees only.
5. **Tests to improve.**
6. **Testing stack.** Only the tools that need a change.
7. **Inventory.** Composition charts, then the full ranked inventory in a closed `details.more`.
8. **How this was checked.** Inventory completeness, verification, and review gaps.

## Removal candidates

Use one `.item` per candidate when there are five or fewer, ranked, with the first as the `.lead-item`. Use a table when there are more.

- **Title.** The test ID and what it claims to protect.
- **Badges.** Confidence, with `risk` only when the test creates demonstrated false confidence or recurring cost.
- **Callout.** The removal reasoning and the surviving protection, titled `Remove`.
- **Fields.** `Location` with file and line, `Missing value` for the absent unique value or false signal, `Cost` for demonstrated runtime, flakiness, maintenance, or diagnostic cost, and `Before deleting` for any required check.

If no test meets the removal gate, say `No supported removal candidates` and name the strongest near-candidate as an `Improve` item.

## Guarantee gaps

Use one table ordered by consequence, then evidence strength, with only `None`, `Partial`, `Indirect`, and `Unknown` rows:

| Guarantee | Consequence | Owning code and seam | Protecting tests | Status | Next check |
| --- | --- | --- | --- | --- | --- |

Render the status as a badge: `None` and high-consequence `Partial` as `risk`, other `Partial` and `Indirect` as `warn`, `Unknown` as neutral. Keep `Unknown` as uncertainty, not `None`. List `Strong` guarantees as one line beneath the table, not as rows.

Add one diagram after the table only when a gap is hard to state in a row, such as a state diagram of unprotected transitions or a `.compare` of the production path beside the path tests exercise.

## Tests to improve

Use a table with the test ID, shortcoming, affected guarantee, smallest repair, and evidence expected after the repair. Use the exact smell name from the testing rubric when one applies. Group repeated shortcomings into one row listing the affected test IDs, each linked to its inventory row.

## Testing stack

Use a table of tools and dependencies whose verdict is `Improve`, with current job, overlap or gap, and the change. A replacement or new dependency needs the guarantee gap, determinism problem, diagnostic failure, or measured suite cost it addresses. List the `Keep` tools, with exact versions, as one line beneath the table. When every tool is `Keep`, use that line alone.

## Inventory

Show two `.bars` charts: tests by value tier (`Essential`, `High`, `Supporting`, `Low`, `Negative`) and by verdict (`Keep`, `Improve`, `Removal candidate`). Each row prints its exact count, such as `84 of 642`. A bar width is a share of the assessed inventory, never a coverage percentage.

Put the full ranked inventory in a closed `details.more` whose summary names the total. Inside, add a `.filter` with text search and a verdict select, then a `wide` table sorted by rank with one row for every assessed test:

| Rank | Test ID and location | Guarantee | Seam and oracle | Unique value | Shortcomings and cost | Tier and verdict |
| --- | --- | --- | --- | --- | --- | --- |

Give each row an `id` for in-report links and a `data-verdict` value for the filter. Preserve exact runtime IDs. Render every row in the HTML.

## How this was checked

- **Completeness.** Static files and declarations, collector IDs, parameterised or generated IDs, skipped, todo, quarantined, and collection-failing tests, unresolved dynamic declarations, and ledger rows accounted for. State whether every collected test has a ranked row. Never call a sampled inventory complete.
- **Verification.** A table of each command, result badge, cache state, environment, and what it established. Add `Not run` rows for important suites, browsers, services, or platforms.
- **Review gaps.** Collection failures, unsupported DSLs, unavailable services, unrun platforms, and excluded areas, each with the verdicts it could change.

## Wording

Name the guarantee, source, seam, defect caught, missing case, and surviving protection. Avoid "improve coverage", "best practice", "more robust", and "increase confidence" unless the next words state the exact behaviour and evidence.

## Report-specific checks

In addition to the shared verification, confirm that every collected test appears in the inventory or the unresolved ledger, that the filter updates its count and the unfiltered table shows every row, and that wide tables scroll inside their wrappers.
