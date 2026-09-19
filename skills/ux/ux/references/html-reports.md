# HTML reports

Use this guidance for generated HTML reports alongside the report workflow's own format reference. Read that reference before writing the page. Preserve its scaffold and component classes; fill the content rather than inventing another page design. If an offline report needs inline CSS, reproduce the same hierarchy, spacing, surfaces, and responsive behaviour. Specialist guidance should improve the report within those requirements.

## Preserve layout and reading order

- Keep scope and evidence, recommendations, findings, and gaps in the order required by the report. Use spacing and heading hierarchy to distinguish them.
- Preserve the document width, page padding, section spacing, type scale, and restrained palette. Bound prose line lengths and keep small metadata distinct from body text.
- Let grid and flex children shrink with `min-width: 0`. Use `minmax(0, 1fr)` or equivalent for flexible grid tracks. Preserve explicit minimums only where the layout stacks before they stop fitting.
- Wrap long paths, URLs, and identifiers with `overflow-wrap: anywhere`. Keep code and wide tables in their own horizontally scrolling containers. Do not hide page overflow to conceal a layout defect.
- Stack comparisons in reading order on narrow screens. Preserve their text labels, and let diagrams grow rather than clipping labels.

## Verify the report itself

Render the final file in an available, permitted browser at a desktop width and at `320px`. Inspect screenshots of the header, a representative finding or result, and the densest table, code comparison, or diagram. Check the DOM and console for overflow, missing styles, failed diagrams, and report-script errors. A successful HTML parser, application test suite, or command that opens the file does not establish visual quality.

Confirm readable hierarchy and spacing, bounded code and table scrolling, visible labels and focus, and working internal links and any filters. Use the report's longest real paths and labels, not short placeholders. Apply its domain-specific checks too. Fix observed defects and recheck the affected views before handoff.

If browser inspection is unavailable or blocked, perform source and structural checks, deliver the report, and explicitly state `Visual verification not run` with the reason. Preserve browser restrictions; do not claim a rendered pass from source inspection or stop the rest of the authorised work solely because this check is unavailable.
