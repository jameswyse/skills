# Upgrade HTML report format

Build the report with the ux skill's [HTML reports](../../ux/references/html-reports.md) guidance and
its `--inline` option. It owns the design, components, build script, verification, and delivery.
This file owns what the upgrade report says. Write the body to
`<run-dir>/upgrade-report.body.html` and build `<run-dir>/upgrade-report.html`.

The report has no ranked items, so it has no `Start here` badge. Omit any section with nothing to
report.

## Sections

1. **Header.** Eyebrow `Dependency upgrade`, the repository name as the title, then the date,
   revision and branch, `Complete` or `Blocked`, and whether the changes are uncommitted.
2. **Summary.** One or two sentences with the outcome, the headline upgrades, and the security
   fixes. Up to four counts, such as packages upgraded as `accent`, advisories fixed as `good`, and
   release-age exceptions and holds as `warn`.
3. **Release-age exceptions.** A table with `package@version`, publication date, reason, and the
   date it ages past the threshold. When there are none, say so in the summary instead.
4. **Upgrades.** A table with one row per package family: its packages, old and new versions,
   and a note naming the migration. Badge a major upgrade `Major` as neutral and a security fix
   `Security` as `good`. When patch-only updates outnumber the rest, move them into a closed
   `details.more`.
5. **Toolchain.** `.fields` rows for Node.js and pnpm with old and new versions, the files updated
   as `.files`, and available majors not adopted. Include a pnpm migration here when one ran.
6. **Policy.** A table of holds, overrides, patches, audit ignores, and build permissions, each
   `Added`, `Kept`, or `Removed`, with its reason and removal condition.
7. **Remaining.** Outdated items and blockers, each with the reason it remains and what would
   unblock it.
8. **How this was checked.** A table of each verification command and its result, as `good` for
   a pass and `risk` for a failure. Mark checks that could not run `Not verified` with the reason,
   and name upstream commits that landed during the run.

Put versions in `.nowrap` cells.
