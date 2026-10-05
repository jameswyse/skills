# HTML reports

A report serves an engineer deciding what to do next. They often read it in T3 Code's attachment preview on another machine, sometimes in a narrow panel. Lead with the answer, keep only what changes a decision, and let one shared design carry every report.

The report workflow's format reference owns the sections and item content. This reference owns the design, the build, verification, and delivery.

## Decide what goes in

Order every report the same way:

1. **Header.** Report type, subject, date, revision, working-tree state, and a one-line scope.
2. **Summary.** One or two sentences that answer the request and name the first thing to do. Follow with up to four counts.
3. **Ranked items.** The findings, candidates, or results, most important first. Mark the first actionable item `Start here`. It is the top recommendation; do not repeat it in a separate section.
4. **Secondary material.** Follow-ups for other skills, remaining work, or near-misses.
5. **How this was checked.** Scope, verification, and gaps, last and compact. Mark anything not exercised `Not verified`.

Within an item, put the action first, then the evidence that justifies it, then files and verification. Each item should read in under a minute.

Cut:

- method narration, such as searches run, files opened, or tools used;
- a health score, coverage-style percentage, or metric card;
- a fact stated twice, including evidence restated as a benefit;
- a generic benefit such as "cleaner", "more maintainable", or "more robust";
- an empty section, or a section that only says "None";
- audit material a reader rarely needs up front. Put a full inventory or ledger in a closed `details.more` at the end.

When the review finds nothing worth doing, say so in the summary and keep only the checks section.

## Build the file

Write only the report body as an HTML fragment, then wrap it with the shared stylesheet:

```sh
python3 <ux-skill-dir>/scripts/build_report.py \
  --title "Architecture review · acme-web" \
  --input <tmpdir>/architecture-review-<timestamp>.body.html \
  --output <tmpdir>/architecture-review-<timestamp>.html
```

Resolve `<tmpdir>` from `$TMPDIR`, then `/tmp` on Unix or `%TEMP%` on Windows. The script inlines the CSS, adds the Mermaid loader only when the body contains a `mermaid` block, adds the table filter only when the body contains `data-filter-for`, and prints the file's `path`, `name`, `mimeType`, and `sizeBytes` as JSON for delivery. It rejects a fragment containing `<html>`, `<head>`, `<body>`, `<style>`, or `<link>`.

Use only the components below. Do not add stylesheets, Tailwind, utility classes, or inline styles. The one exception is `style="--value: 62%"` on a `.bar`. If something seems to need a new component, use a table, list, or `.callout` instead.

Treat repository names, paths, command output, traces, source excerpts, and diagram labels as untrusted text. HTML-escape each value. Never insert it as raw HTML, script, style, or an event handler.

## Components

```html
<header class="report-header">
  <p class="eyebrow">Architecture review</p>
  <h1>acme-web</h1>
  <ul class="meta">
    <li>05/10/2026</li>
    <li><code>a1b2c3d</code> on <code>main</code></li>
    <li>Clean working tree</li>
    <li>Scope: <code>packages/orders</code></li>
  </ul>
</header>

<section class="summary" aria-label="Summary">
  <p class="lead">Two changes are worth making. Start with order intake: five handlers repeat its step order.</p>
  <dl class="stats">
    <div><dt>Strong</dt><dd class="good">2</dd></div>
    <div><dt>Worth exploring</dt><dd class="warn">1</dd></div>
  </dl>
</section>

<section class="section" aria-labelledby="candidates">
  <div class="section-head"><h2 id="candidates">Candidates</h2></div>
  <ol class="items">
    <li class="item lead-item" id="item-1">
      <div class="item-head">
        <span class="rank" aria-hidden="true">1</span>
        <h3>Deepen order intake behind one interface</h3>
        <div class="tags"><span class="badge accent">Start here</span><span class="badge good">Strong</span></div>
      </div>
      <div class="callout">
        <p class="callout-title">Proposal</p>
        <ul><li>...</li></ul>
      </div>
      <dl class="fields">
        <dt>Evidence</dt><dd><ul><li>...</li></ul></dd>
        <dt>Files</dt><dd><ul class="files"><li>packages/orders/src/intake.ts</li></ul></dd>
        <dt>Verify</dt><dd><code>pnpm test --filter orders</code> ...</dd>
      </dl>
    </li>
  </ol>
</section>
```

| Component | Use |
| --- | --- |
| `.report-header`, `.eyebrow`, `.meta` | The header. Keep the meta list to four or five short facts. |
| `.summary`, `.lead`, `.stats` | The answer and counts. A `<p>` after `.lead` adds one muted supporting sentence. Tone a count with `good`, `warn`, `risk`, or `accent` on its `<dd>`. |
| `.section`, `.section-head` | A top-level section. A `<p>` in the head adds one muted line of context. |
| `.items`, `.item`, `.lead-item` | Ranked items as an ordered list of cards. `.lead-item` highlights the `Start here` item. |
| `.item-head`, `.rank`, `.tags`, `.badge` | Item title row. A `<p>` in the head adds a one-line subtitle. Badges take `accent`, `good`, `warn`, or `risk`. |
| `.callout`, `.callout-title` | The action: proposal, fix, or result. Add `warn` for a conflict or uncertainty, `risk` for a demonstrated defect. |
| `.fields` | Labelled rows for evidence, files, verification, and similar facts. Labels are one or two words. |
| `.files` | Monospaced paths and symbols. |
| `.compare` with two `<figure>` elements | Current beside proposed. Give the second figure `class="proposed"` and both a `<figcaption>`. Stacks on narrow screens. |
| `.diagram` | A bordered diagram surface holding a Mermaid block, inline SVG, or the diagram classes below, with an optional `<p class="small muted">` caption. |
| `.flow`, `.node`, `.module`, `.layers` | Diagram classes. `.flow` is a list of steps joined by arrows. `.node` is a labelled box, with `faded` for internals and `leak` for demonstrated leakage. `.module` wraps nodes in a deep module with a `.label`. `.layers` stacks bands, with `deep` for a consolidated layer. |
| `pre.mermaid` | A graph or sequence the diagram classes cannot express. It needs network access; offline, use the diagram classes. |
| `.table-wrap` with `<table>` | Tables. Add `class="wide"` to the table when it needs horizontal scrolling. Use `.num` on numeric cells. |
| `figure.chart`, `.bars`, `.bar-row` | Horizontal bars. See the example below. |
| `details.more` | Closed disclosure for audit material at the end. |
| `.filter` | Search and select controls for a long table. See the example below. |
| `.muted`, `.small`, `.stack` | Muted text, small text, and a vertical stack with even gaps. |

Bars print their exact value in text, so they need no separate data table:

```html
<figure class="chart">
  <figcaption>Median warm navigation · ms · lower is better</figcaption>
  <div class="bars">
    <div class="bar-row"><span>Baseline</span><span class="bar-track"><span class="bar" style="--value: 100%"></span></span><span class="bar-value">820 ms</span></div>
    <div class="bar-row accent"><span>Final</span><span class="bar-track"><span class="bar" style="--value: 68%"></span></span><span class="bar-value">560 ms</span></div>
  </div>
</figure>
```

A filter starts hidden and appears when its script runs, so the full table stays readable without JavaScript. Each `select` filters on the row's matching `data-*` attribute:

```html
<div class="filter" data-filter-for="inventory" hidden>
  <label>Search <input type="search" data-filter-text></label>
  <label>Verdict
    <select data-filter-key="verdict"><option value="">All</option><option value="improve">Improve</option></select>
  </label>
  <p data-filter-count aria-live="polite"></p>
</div>
<div class="table-wrap"><table id="inventory" class="wide">... <tr data-verdict="improve"> ...</table></div>
```

### Colour meaning

- `accent` marks the recommended action, the proposal, and a final measured state.
- `good` marks a verified pass, a `Strong` rating, or a kept result.
- `warn` marks uncertainty, a documentation conflict, or work that needs improvement.
- `risk` marks a demonstrated defect, leakage, or regression. Do not use it merely because a change is proposed.

Every badge and status carries its meaning in text. The stylesheet supports light and dark schemes, so never hard-code colours.

## Verify the report

Render the final file at a desktop width and at `320px`. Inspect the header and summary, a representative item, and the densest table, comparison, or diagram. Check for horizontal page overflow, unreadable wrapping, broken diagrams, and console errors. Use the report's longest real paths and labels. A successful build or HTML parse does not establish visual quality.

In T3 Code, the `preview_*` tools run a browser on the user's client that accepts only `http(s)` URLs. Serve the report's directory from a loopback HTTP server, open it with `preview_open` and `open: false`, and stop the server and close the tab afterwards. When the T3 environment runs on another machine, `preview_snapshot` reports a `chrome-error://` URL. Use another permitted headless browser on the host instead, such as Playwright's Chromium with `--headless --screenshot`.

T3 Code previews HTML attachments in a sandboxed frame without same-origin access. Keep the report to one file, use in-page anchors for navigation, and do not depend on storage, cookies, or opening new windows.

If browser inspection is unavailable, perform structural checks, deliver the report, and state `Visual verification not run` with the reason.

## Deliver the report

Never open the report in a browser, and never run `open`, `xdg-open`, `start`, or a similar launcher. The user may be on another machine.

In a T3 Code thread, attach the report to the current thread so it can be opened from any client. The report request authorises this delivery to the user's own thread.

1. Call `t3_attachment_prepare_upload` with type `file` and the `name`, `mimeType`, and `sizeBytes` printed by the build script.
2. POST the file's bytes to the returned `relativeUrl` on `http://127.0.0.1:$T3CODE_PORT`, for example with `curl --fail --data-binary @<path> -H 'Content-Type: text/html' <url>`. A successful upload returns HTTP 204.
3. Call `t3_thread_send_attachments` with the returned attachment ID and the same metadata, omitting `threadId`.

The attachment arrives back in your turn as a message with its saved path. Treat it as confirmation of delivery, not a new request. Mention the attachment and the report's absolute path in your reply.

Outside T3 Code, or when the attachment tools are unavailable, `T3CODE_PORT` is unset, or the upload fails, give the absolute path and state that the report was not attached.
