# Testing HTML report format

Render the testing review as one static HTML file in the operating system's temporary directory. Use this light editorial system so the report matches the other codebase-review skills.

Load Tailwind from its CDN when the environment has network access. Load Mermaid only when a dependency graph, collection flow, or test observation path clarifies evidence. Use inline CSS and SVG when the report must work offline.

## Keep this page shell

Use the following shell. Preserve the stone page, centred `max-w-6xl` document, slate text, white section surfaces, indigo accent, restrained borders, small shadows, and `text-4xl` title.

```html
<!doctype html>
<html lang="en-AU">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Testing review for {{repository name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      .grid > * { min-width: 0; }
      a { overflow-wrap: anywhere; }
      code {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        overflow-wrap: anywhere;
      }
      :not(pre) > code {
        border: 1px solid #cbd5e1;
        border-radius: 0.25rem;
        background: #e2e8f0;
        color: #0f172a;
        padding: 0.125rem 0.35rem;
        font-size: 0.9em;
        font-weight: 600;
      }
      .surface { border: 1px solid #e2e8f0; background: #fff; box-shadow: 0 1px 2px rgb(15 23 42 / 0.06); }
      .callout { border-inline-start: 4px solid #4f46e5; background: #eef2ff; }
      .risk { border-inline-start: 4px solid #dc2626; background: #fef2f2; }
      .warning { border-inline-start: 4px solid #d97706; background: #fffbeb; }
      .table-wrap { overflow-x: auto; overscroll-behavior-inline: contain; }
      th { position: sticky; top: 0; background: #f8fafc; }
      .bar-track { overflow: hidden; border-radius: 9999px; background: #e2e8f0; }
      .bar-value { min-width: 0.25rem; height: 0.75rem; border-radius: inherit; background: #4f46e5; }
      @media print {
        th { position: static; }
        .no-print { display: none !important; }
      }
    </style>
  </head>
  <body class="bg-stone-50 font-sans text-slate-900">
    <main class="mx-auto max-w-6xl space-y-10 px-4 py-10 sm:px-6 lg:px-8">
      <header>...</header>
      <section id="review-boundary">...</section>
      <section id="inventory-completeness">...</section>
      <section id="verification-evidence">...</section>
      <section id="testing-stack">...</section>
      <section id="portfolio-summary">...</section>
      <section id="guarantee-map">...</section>
      <section id="removal-candidates">...</section>
      <section id="tests-to-improve">...</section>
      <section id="ranked-inventory">...</section>
      <section id="review-gaps">...</section>
    </main>
  </body>
</html>
```

Do not replace the shell with a dark theme, gradient page background, oversized title, dashboard grid, glass panels, or a row of large metric cards. Dark surfaces belong only to code fragments or a diagram element that needs contrast.

## Lead with scope and evidence

Show the repository name, review date, revision, working-tree state, and requested scope in the header. Keep the next three sections separate and full width.

**Review boundary.** List every major area with `Inspected`, `Excluded`, or `Review gap`. Name the code and integration paths included by a focused scope. A short method limitation belongs here only when it changes confidence.

**Inventory completeness.** Show these exact facts when available:

- static test files and declarations;
- native collector IDs;
- parameterised or generated IDs;
- skipped, todo, quarantined, and collection-failing tests;
- unresolved dynamic declarations, unreadable files, and unsupported DSLs;
- ledger rows accounted for, excluded, and unresolved.

State whether every collected test has a ranked row. Never label a sampled inventory as complete.

**Verification evidence.** Use a full-width table. Each row names the command or interaction, result, cache state when applicable, runtime or environment, and what it established. Add a `Not run` row for an important suite, browser, service, or platform that was not exercised. Source inspection and searches are review work, not verification commands.

## Assess the testing stack

Use one compact table with these columns:

| Tool or dependency | Current job | Configuration and use | Overlap or gap | Verdict |
| ------------------ | ----------- | --------------------- | -------------- | ------- |

Render `Keep` with a neutral indigo badge. Render `Improve` with amber. A replacement or new dependency needs a short callout that names the guarantee gap, determinism problem, diagnostic failure, or demonstrated suite cost it addresses. Preserve exact dependency names and versions. Do not include a generic list of newer releases.

Use a Mermaid dependency graph only when several runners, environments, or adapters overlap in a way the table cannot show quickly. Keep the graph beside the relevant explanation.

## Summarise the portfolio with exact counts

Use a compact text line for totals, such as `642 tests assessed · 18 Improve · 7 Removal candidates · 11 guarantee gaps`. These counts describe the report inventory, not codebase health.

Include two accessible horizontal bar charts:

1. Test count by `Essential`, `High`, `Supporting`, `Low`, and `Negative` value tier.
2. Test count by `Keep`, `Improve`, and `Removal candidate` verdict.

Each bar must show its label, exact count, and total in text. A width may show that count as a share of the assessed inventory. Do not call the width a coverage percentage. Pair each chart with a small text list or hidden data table so the values remain available to screen readers and when CSS does not load.

```html
<figure class="surface p-6" aria-labelledby="value-chart-title">
  <figcaption id="value-chart-title" class="text-lg font-semibold">Tests by value tier</figcaption>
  <div class="mt-5 space-y-4">
    <div>
      <div class="flex items-baseline justify-between gap-4 text-sm">
        <span class="font-medium">High</span>
        <span>84 of 126 tests</span>
      </div>
      <div class="bar-track mt-2" aria-hidden="true">
        <div class="bar-value" style="width: 66.67%"></div>
      </div>
    </div>
  </div>
</figure>
```

Use emerald only for the `Essential` or `Strong` status and verified passed results. Reserve red for demonstrated risk and `Negative` value. Use amber for weak evidence and `Improve`. Labels must carry the meaning without colour.

## Show the guarantee map

Use one table ordered by consequence and then evidence strength. Include:

| Guarantee | Authority and consequence | Owning code and observing seam | Protecting tests | Status | Gap or next check |
| --------- | ------------------------- | ------------------------------ | ---------------- | ------ | ----------------- |

Render `Strong`, `Partial`, `Indirect`, `None`, and `Unknown` as text badges. Make `None` and high-consequence `Partial` rows easy to find with a red or amber start border. Preserve `Unknown` as uncertainty. Do not silently treat it as `None`.

Above the table, include a compact status count or stacked bar. It shows guarantee-map composition only. Do not divide tested source files by total files or turn the statuses into a single score.

When a relationship is hard to explain in a row, add one focused visual after the table:

- a state diagram for unprotected legal and illegal transitions;
- a production path beside the path that tests exercise;
- a sequence diagram for an untested failure or recovery path;
- a small matrix for permission, configuration, browser, or protocol variants.

Use exact domain states and interfaces. Keep a text explanation next to every diagram.

## Make removal candidates prominent

Place removal candidates before the full inventory. Start with a direct conclusion. If no test meets the removal gate, say `No supported removal candidates` and explain the strongest near-candidate as an `Improve` item.

For each candidate, include:

- rank, test ID, file, and line;
- claimed guarantee;
- the missing unique value or false signal;
- demonstrated runtime, flakiness, maintenance, or diagnostic cost;
- the surviving test or other protection;
- the exact removal reasoning; and
- confidence and any check required before deletion.

Use a table for several candidates. Use a red start border only when the current test creates demonstrated false confidence or recurring cost. Do not use red merely because removal is proposed.

## Separate weak tests from removable tests

Show `Improve` tests in their own table. Include the test ID, shortcoming, affected guarantee, smallest repair, and expected evidence after repair. Use the exact smell name from the testing rubric when one applies.

Group repeated shortcomings only for the summary. Keep every affected test ID in the full inventory and link each grouped item back to its row.

## Include the complete ranked inventory

The full table is the audit trail. Sort it by ordinal rank. Include every assessed test and use these columns:

| Rank | Test ID and location | Guarantee and authority | Seam, oracle, and path | Unique value and justification | Shortcomings and cost | Tier and verdict |
| ---- | -------------------- | ----------------------- | ---------------------- | ------------------------------ | --------------------- | ---------------- |

Keep the explanation concise, but do not replace it with a score. Link the test ID to an in-report anchor. Preserve exact runtime IDs even when they are long.

Wrap the table in `.table-wrap` and give it a useful minimum width. The wrapper may scroll horizontally. The page itself must not. Repeat table headings when the browser prints across pages.

Add a labelled search field and verdict filter before the table when the inventory is large. Render every row in the HTML and use inline JavaScript only to hide non-matching rows. Without JavaScript, the complete rank order must remain visible.

```html
<div class="no-print grid gap-4 sm:grid-cols-[minmax(0,1fr)_14rem]">
  <label class="text-sm font-medium">
    Search tests
    <input id="test-search" class="mt-2 w-full border border-slate-300 bg-white px-3 py-2" type="search" />
  </label>
  <label class="text-sm font-medium">
    Verdict
    <select id="verdict-filter" class="mt-2 w-full border border-slate-300 bg-white px-3 py-2">
      <option value="">All verdicts</option>
      <option value="keep">Keep</option>
      <option value="improve">Improve</option>
      <option value="removal">Removal candidate</option>
    </select>
  </label>
</div>
```

The script must update a visible result count and preserve table headings. Do not add client-side pagination that makes rows unreachable by page search or assistive technology.

## End with honest review gaps

Name collection failures, unsupported test DSLs, unavailable services, unrun platforms, incomplete requirements, unresolved ownership, and areas excluded by the requested scope. State which verdicts each gap could change.

Do not turn ordinary source inspection into a generic method essay. The reader needs to know what remains uncertain and why.

## Check the rendered result

Apply the "ux" HTML-report verification to the final file, including screenshot inspection at a desktop width and at `320px`. Check these report-specific requirements:

- the document matches the light editorial shell;
- the browser console has no report-script or Mermaid errors;
- the page has no horizontal overflow;
- each table scrolls inside its wrapper;
- every collected test appears in the full inventory or the unresolved ledger;
- search and filters update the visible count, and the unfiltered state shows every row;
- charts show exact values in text;
- focus indicators, labels, headings, and status text remain clear; and
- print preview retains the complete inventory.

Fix observed defects before handoff. If visual inspection is unavailable, deliver the structurally checked report with `Visual verification not run` and the reason.

## Keep the language concrete

Write plain, concise English. Name the guarantee, source, seam, defect caught, missing case, and surviving protection. Avoid phrases such as "improve coverage", "best practice", "more robust", and "increase confidence" unless the next words state the exact behaviour and evidence.
