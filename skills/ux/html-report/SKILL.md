---
name: html-report
description: Use when a skill or the user asks for an HTML report, or when you have generated any HTML file the user should view.
---

# HTML report

A report serves an engineer deciding what to do next. They often read it in a T3 Code thread on another machine, sometimes in a narrow panel or on a phone. Lead with the answer, keep only what changes a decision, and let one shared design carry every report.

The calling workflow's format reference owns the sections and item content. This skill owns the structure, components, build, and delivery.

## Decide what goes in

Order every report the same way:

1. **Header.** Report type, subject, date, revision, working-tree state, and a one-line scope.
2. **Summary.** One or two sentences that answer the request and name the first thing to do. Follow with up to four counts.
3. **Ranked items.** The findings, candidates, or results, most important first. Mark the first actionable item `Start here`. It is the top recommendation; do not repeat it in a separate section.
4. **Secondary sections.** Follow-ups for other skills, remaining work, or near-misses.
5. **How this was checked.** Last and compact. Mark anything not exercised `Not verified`.

Within an item, put the action first, then the evidence that justifies it, then files and verification. Each item should read in under a minute.

## Keep it short

- Show at most five ranked items as cards and list the rest as table rows, unless the format reference says otherwise.
- Give an item at most four fields, each one or two lines.
- Prefer two-column tables: a name with an optional one-line note beneath it, then a short value or badge. Use a wider table only for an inventory inside `details.more`.
- Write the checks as a `Check` and `Result` table. Add a note only where the format reference asks for one or a result is not a plain pass.
- Put what a reader rarely needs, such as a full inventory or a list of kept entries, in a closed `details.more` at the end.

Cut:

- method narration, such as searches run, files opened, or tools used;
- a health score, coverage-style percentage, or metric card;
- a fact stated twice, including evidence restated as a benefit;
- a generic benefit such as "cleaner", "more maintainable", or "more robust";
- a note that says nothing changed;
- an empty section, or a section that only says "None".

When the review finds nothing worth doing, say so in the summary and keep only the checks section.

## Build the file

Write only the report body as an HTML fragment, then wrap it with the shared stylesheet. `<skill-dir>` is this skill's base directory.

```sh
python3 <skill-dir>/scripts/build_report.py --inline \
  --title "Architecture review · acme-web" \
  --input <tmpdir>/architecture-review-<timestamp>.body.html \
  --output <tmpdir>/architecture-review-<timestamp>.html
```

Resolve `<tmpdir>` from `$TMPDIR`, then `/tmp` on Unix or `%TEMP%` on Windows. `--inline` suits T3 Code's `html_render` tool: the page follows the thread's theme and drops its outer margins. Omit it when the report will be attached instead. The script prints the file's `path`, `name`, `mimeType`, and `sizeBytes` as JSON for delivery.

The script rejects a fragment that brings its own document or styles, uses a class the stylesheet does not define, sets an inline style other than a bar's `--value`, or contains a script, frame, event handler, or `javascript:` URL. Fix what it names and build again. The stylesheet fits every component to any width, including long paths and names, so a fragment that builds needs no preview or screenshot.

Treat repository names, paths, command output, traces, source excerpts, and diagram labels as untrusted text. HTML-escape each value, and never insert one as raw HTML, a link, a script, a style, or an event handler. The build checks keep the report to its components; they don't sanitise it.

## Components

Use only these components. If something seems to need a new one, use a table, list, or `.callout` instead. When changing the shared stylesheet itself, use the installed "better-layout", "better-typography", and "better-ui" skills.

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
        <dt>Evidence</dt><dd>...</dd>
        <dt>Files</dt><dd><ul class="files"><li>packages/orders/src/intake.ts</li></ul></dd>
        <dt>Verify</dt><dd><code>pnpm test --filter orders</code> ...</dd>
      </dl>
    </li>
  </ol>
</section>

<section class="section" aria-labelledby="checks">
  <div class="section-head"><h2 id="checks">How this was checked</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Check</th><th>Result</th></tr></thead>
    <tbody>
      <tr><td><code>pnpm verify</code></td><td><span class="badge good">Pass</span></td></tr>
      <tr><td>Browser flow<div class="small muted">No staging credentials</div></td><td><span class="badge warn">Not verified</span></td></tr>
    </tbody>
  </table></div>
</section>
```

| Component | Use |
| --- | --- |
| `.report-header`, `.eyebrow`, `.meta` | The header. Keep the meta list to four or five short facts. |
| `.summary`, `.lead`, `.stats` | The answer and counts. Tone a count with `good`, `warn`, `risk`, or `accent` on its `<dd>`. |
| `.section`, `.section-head` | A top-level section. A `<p>` in the head adds one muted line of context. |
| `.items`, `.item`, `.lead-item` | Ranked items as an ordered list of cards. `.lead-item` highlights the `Start here` item. |
| `.item-head`, `.rank`, `.tags`, `.badge` | Item title row. Badges take `accent`, `good`, `warn`, or `risk`. |
| `.callout`, `.callout-title` | The action: proposal, fix, or result. Add `warn` for a conflict or uncertainty, `risk` for a demonstrated defect. |
| `.fields` | Labelled rows for evidence, files, verification, and similar facts. Labels are one or two words. |
| `.files` | Monospaced paths and symbols. |
| `.compare` with two `<figure>` elements | Current beside proposed. Give the second figure `class="proposed"` and both a `<figcaption>`. Stacks on narrow screens. |
| `.diagram` | A bordered surface holding the diagram classes below, with an optional `<p class="small muted">` caption. |
| `.flow`, `.node`, `.module`, `.layers` | Diagram classes. `.flow` is a list of steps joined by arrows. `.node` is a labelled box, with `faded` for internals and `leak` for demonstrated leakage. `.module` wraps nodes in a deep module with a `.label`. `.layers` stacks bands, with `deep` for a consolidated layer. |
| `.table-wrap` with `<table>` | Tables. A `<div class="small muted">` after a cell's text adds a one-line note. Use `.nowrap` on short cells such as versions and `.num` on numeric cells. Add `class="wide"` to a table with more than three columns, so it scrolls inside its wrapper. |
| `figure.chart`, `.bars`, `.bar-row` | Horizontal bars. See the example below. |
| `details.more` | Closed disclosure for reference lists at the end. |
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


## Deliver the report

Deliver another skill's HTML file the same way. When the build script didn't produce it, take its `name` and `sizeBytes` from the file and use `text/html` as its `mimeType`.

Never open the report in a browser, and never run `open`, `xdg-open`, `start`, or a similar launcher. The user may be on another machine.

When T3 Code's `html_render` tool is available, pass the document as `html` with `height` `2000`, before writing the final reply. Do not also attach it. The reader sees the page above the reply, so the reply adds only what the page does not say and does not announce it.

Otherwise, in a T3 Code thread, attach the report to the current thread so it can be opened from any client. The report request authorises this delivery to the user's own thread.

1. Call `t3_attachment_prepare_upload` with type `file` and the `name`, `mimeType`, and `sizeBytes` printed by the build script.
2. POST the file's bytes to the returned `relativeUrl` on `http://127.0.0.1:$T3CODE_PORT`, for example with `curl --fail --data-binary @<path> -H 'Content-Type: text/html' <url>`. A successful upload returns HTTP 204.
3. Call `t3_thread_send_attachments` with the returned attachment ID and the same metadata, omitting `threadId`.

The attachment arrives back in your turn as a message with its saved path. Treat it as confirmation of delivery, not a new request. Mention the attachment and the report's absolute path in your reply.

T3 Code previews attachments in a sandboxed frame, so keep the report to one file and use in-page anchors for navigation.

Outside T3 Code, or when the attachment tools are unavailable, `T3CODE_PORT` is unset, or the upload fails, give the absolute path and state that the report was not attached.
