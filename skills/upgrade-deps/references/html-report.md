# Upgrade HTML report

Fill in the template below and build it with the "html-report" skill. This file owns what the
upgrade report says. Write the body to `<run-dir>/upgrade-report.body.html` and build
`<run-dir>/upgrade-report.html`. Keep the template's structure.

## Keep it short

- Leave out the summary counts. The tables carry them.
- Write one line per note. Note a migration, a removed patch, a hold, or a failure.
- Put companion packages that share a version and reason in one row, such as
  `@storybook/* 10.6.3 (7 packages)`.
- When a family's packages have different versions, give each version line its own row.
- Put patch updates without a note in one final `Patch updates` row whose note lists each package
  with its old and new versions.
- Show the Node.js and pnpm rows only when their version changed, and list the files updated and any
  pnpm migration in the note. Report an available major not adopted under Remaining.

## Template

```html
<header class="report-header">
  <p class="eyebrow">Dependency upgrade</p>
  <h1>REPO</h1>
  <ul class="meta">
    <li>DD/MM/YYYY</li>
    <li><code>REV</code> on <code>BRANCH</code></li>
    <li>Complete | Blocked: SHORT REASON</li>
    <li>Uncommitted | Committed | Pushed</li>
  </ul>
</header>

<section class="summary" aria-label="Summary">
  <p class="lead">ONE OR TWO SENTENCES: OUTCOME, HEADLINE UPGRADES, SECURITY FIXES.</p>
</section>

<section class="section" aria-labelledby="exceptions">
  <div class="section-head"><h2 id="exceptions">Release-age exceptions</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Package</th><th>Eligible</th></tr></thead>
    <tbody>
      <tr><td><code>PACKAGE@VERSION</code><div class="small muted">REASON</div></td><td class="nowrap">DD/MM</td></tr>
    </tbody>
  </table></div>
</section>

<section class="section" aria-labelledby="upgrades">
  <div class="section-head"><h2 id="upgrades">Upgrades</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Package</th><th>Version</th></tr></thead>
    <tbody>
      <tr><td>Node.js<div class="small muted">FILES UPDATED</div></td><td class="nowrap">OLD → NEW</td></tr>
      <tr><td>pnpm<div class="small muted">FILES UPDATED</div></td><td class="nowrap">OLD → NEW</td></tr>
      <tr><td>PACKAGES <span class="badge">Major</span><div class="small muted">MIGRATION NOTE</div></td><td class="nowrap">OLD → NEW</td></tr>
      <tr><td>PACKAGE <span class="badge good">Security</span><div class="small muted">Fixes GHSA-…</div></td><td class="nowrap">OLD → NEW</td></tr>
      <tr><td>OWNER/ACTION</td><td class="nowrap">OLD → NEW</td></tr>
      <tr><td>Patch updates<div class="small muted">PACKAGE OLD → NEW, PACKAGE OLD → NEW</div></td><td class="nowrap">COUNT</td></tr>
    </tbody>
  </table></div>
</section>

<section class="section" aria-labelledby="policy">
  <div class="section-head"><h2 id="policy">Policy changes</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Entry</th><th>Change</th></tr></thead>
    <tbody>
      <tr><td>ENTRY<div class="small muted">REASON. Remove when CONDITION</div></td><td><span class="badge warn">Added</span></td></tr>
      <tr><td>ENTRY<div class="small muted">REASON</div></td><td><span class="badge good">Removed</span></td></tr>
    </tbody>
  </table></div>
  <details class="more">
    <summary>COUNT kept entries</summary>
    <ul>
      <li>ENTRY: EVIDENCE IT IS STILL NEEDED. Remove when CONDITION</li>
    </ul>
  </details>
</section>

<section class="section" aria-labelledby="remaining">
  <div class="section-head"><h2 id="remaining">Remaining</h2></div>
  <ul>
    <li>ITEM: WHY IT REMAINS. Unblocks when CONDITION.</li>
    <li>Deferred until the next run: PACKAGE VERSION, PACKAGE VERSION.</li>
  </ul>
</section>

<section class="section" aria-labelledby="checks">
  <div class="section-head"><h2 id="checks">How this was checked</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Check</th><th>Result</th></tr></thead>
    <tbody>
      <tr><td><code>COMMAND</code></td><td><span class="badge good">Pass</span></td></tr>
      <tr><td><code>COMMAND</code><div class="small muted">WHAT FAILED</div></td><td><span class="badge risk">Fail</span></td></tr>
      <tr><td>CHECK<div class="small muted">REASON</div></td><td><span class="badge warn">Not verified</span></td></tr>
    </tbody>
  </table></div>
</section>
```

Policy changes cover holds, overrides, patches, audit ignores, release-age exclusions, and build
permissions. Under How this was checked, include the code review, and add an `Upstream` row naming
any commits that landed during the run.
