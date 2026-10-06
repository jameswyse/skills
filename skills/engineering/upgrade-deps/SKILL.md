---
name: upgrade-deps
description: Upgrade every dependency, the Node.js and pnpm toolchain, and GitHub Actions when a comprehensive dependency upgrade is requested.
---

# Upgrade dependencies

Upgrade the complete pnpm project to the newest compatible stable dependency set. Call the Skill
tool for "engineering". Treat repository instructions, the workspace definition, the manifests,
and the lockfile as the sources of truth.

The request authorises local changes required to complete the upgrade. It does not authorise a
commit, push, publication, deployment, or unrelated cleanup.

## Completion criteria

Finish only when all of these conditions hold:

- Node.js and pnpm run the latest release of their current major lines, and every source that
  names either version agrees.
- The root project and every package selected by `pnpm-workspace.yaml` have been inventoried.
- Every outdated dependency and GitHub Action is updated or has a verified compatibility hold.
- Every audit finding is fixed. A locally patched and verified advisory may be ignored only as
  described below.
- The dependency-policy entries affected by the new graph are current and no proven-stale entries
  remain.
- Every repository-provided full verification command passes. If none exists, all available format,
  lint, typecheck, build, and test checks pass.
- The "code-review" skill has reviewed the complete change, every verified finding has been fixed,
  and the affected checks have been repeated.
- The final outdated scan, available peer check, frozen-lockfile install, and audit pass. If the
  environment prevents a required check, report the run as blocked instead of complete.

## 1. Establish the scope

1. Read the applicable repository instructions and inspect the working tree. Preserve every
   unrelated staged, unstaged, and untracked change.
2. When the current branch tracks an upstream, fetch it. If the branch is behind, fast-forward it
   with `git merge --ff-only` before changing anything. If it has diverged or the fast-forward
   fails, report that and continue on the local branch.
3. Confirm that the repository uses pnpm. If it uses Yarn or npm, ask once whether to migrate it to
   pnpm first. If the user agrees, follow [Migrate to pnpm](references/pnpm-migration.md) before
   continuing. Otherwise stop.
4. Run from the workspace root. Use the `packages` selection in `pnpm-workspace.yaml`. Do not scan
   arbitrary nested `package.json` files. Account for the root separately instead of assuming that
   one recursive command included it.
5. Inspect the command help and current official documentation for the pnpm version you will run
   before relying on version-specific flags or configuration fields.
6. Resolve and install under the committed workspace policy. Do not bypass registry routing, trust
   policy, package selection, patches, release age, or build policy to make an update pass.
7. Record the repository's canonical focused checks and full verification command. Inspect its
   changeset or release-note policy for published workspace packages.
8. Keep logs, scratch output, and report files in one run directory under `$TMPDIR`. Remove it
   after delivering the report.

## 2. Update Node.js and pnpm

Before the dependency inventory, compare the pinned Node.js and pnpm versions with current stable
releases from official sources. Update each to the latest release in its current major line without
asking, then activate both so the inventory, lockfile, and checks run under the new versions. Read
[Node.js and pnpm toolchain](references/runtime-toolchain.md) before changing any pin.

Adopt a new Node.js or pnpm major only when the user requested it or approves it. Otherwise report
the available major and its support status.

## 3. Inventory before changing

Build one inventory that covers:

- Every manifest dependency field in the root and selected workspace packages.
- Catalogs, aliases, Git dependencies, tarball dependencies, patches, and workspace protocols.
- `overrides`, `packageExtensions`, `peerDependencyRules`, `update.ignoreDeps`, audit exceptions,
  release-age exceptions, and dependency build permissions.
- Outdated direct and transitive resolutions, including stable major releases.
- Known vulnerabilities at the lowest audit severity.
- GitHub Actions in workflows, reusable workflows, and composite actions.
- Existing Dependabot or Renovate holds that correspond to dependency policy.

Use machine-readable output where the installed pnpm version supports it. Treat non-zero
"outdated dependencies found" exits as data, not command failures. Record registry errors and
unresolved private dependencies as coverage gaps.

## 4. Upgrade the compatible set

Target the latest stable releases, including major versions. Respect intentional prerelease pins
and non-registry sources unless the repository evidence shows that they should move.

- Upgrade related package families together. Derive each family from peer ranges, release notes,
  and the dependency graph instead of a hard-coded package list.
- Preserve exact pins, range operators, aliases, catalogs, and workspace protocols unless the
  migration requires a different declaration.
- Keep shared versions in an existing catalog. Move a version into the catalog when several
  workspace packages need it aligned and the repository already uses catalogs for that purpose.
- Prefer updating the responsible direct dependency over forcing a transitive child.
- Read official migration guidance for each major upgrade. Apply required source, configuration,
  generated-file, and durable-test changes.
- Treat upgrade failures as migration evidence. Diagnose and fix the incompatibility at its source
  before introducing a hold.
- Fix what the upgrade causes or exposes as part of the same change: configuration keys for removed
  or renamed tool options, dependencies the new versions make unused, new deprecation warnings, and
  new lint or type warnings. Remove a dependency only when usage and verification prove that the
  removal is safe. Report anything that needs more than a local fix.

Review the diff after each updater command and revert changes the upgrade did not need:

- Catalog entries or manifest ranges moved for a package in `update.ignoreDeps` or under a hold.
- Range operators changed against the repository's existing style or `savePrefix`.
- Companion ranges loosened, such as an `@types/node` range that leaves the runtime's major line.
- GitHub Action refs switched between tags and commit SHAs, or version comments duplicated.

Treat type packages as companions, not independent targets:

- Match a companion `@types/*` package to the runtime package and its supported API line.
- Remove a companion type package when the runtime package now supplies the required types.
- For an application, keep `@types/node` on the deployed Node.js major and update it to the latest
  release in that line.
- For a published library, align `@types/node` with the minimum supported Node.js runtime so newer
  APIs cannot enter by accident.

Treat `peerDependencies` as compatibility declarations. Do not narrow them to the newly installed
version. Update the development dependency that exercises the peer, verify the supported range,
and widen or move the peer range only when the package can truthfully support it.

If the newest release requires a product, public-interface, deployment, or architecture decision
outside the requested maintenance work, stop and ask. Otherwise complete the source migration.

Finish the graph before the first full verification, so that run covers the final lockfile.
Refresh transitive resolutions within their declared ranges with `pnpm update -r`, run
`pnpm dedupe`, and confirm that `pnpm dedupe --check` passes.

## 5. Handle compatibility holds

Use a hold only after the latest release has failed a relevant build, test, runtime check, or
documented compatibility requirement.

- Pin the narrowest working version.
- Scope `update.ignoreDeps`, `peerDependencyRules`, `overrides`, and dependency-bot ignores to the
  actual incompatible package or parent-child edge.
- Record the reason and removal condition in the commit message and final report, not in a code
  comment.
- Re-evaluate every existing hold and local patch during each run. Check current upstream release
  notes and compatibility documentation, then retest against the latest release. Do not carry a
  hold forward from earlier reports, run notes, or commit messages. Remove it as soon as a
  compatible release passes verification.
- Update parent-version selectors when their parent package moves.

Do not hide a peer warning until the installed combination has been verified. Do not use an
override to conceal an incompatible major version.

## 6. Use release-age exceptions

Preserve `minimumReleaseAge` exactly. Never reduce, remove, or temporarily bypass it. By default,
select the newest release that satisfies it, and report a newer release that is still too young with
the date it becomes eligible. Do not wait for a release to age. List these releases in the first
progress update after the inventory, so the user can request an exception before verification
starts.

Add an exact `package@version` entry to `minimumReleaseAgeExclude` without asking when a release
younger than the threshold:

- fixes an audit finding; or
- unblocks other upgrades, or lets you remove an override, patch, hold, or other policy entry.

In these cases, prefer the exception to an override or local patch. Include the platform-specific
and companion packages that the release requires, and nothing else. Never add a package pattern or
an unversioned name. Inspect any exclusions that a mutating audit fix adds, and keep only those that
this section allows.

Use `minimumReleaseAgeExcludePrune` when the pnpm version supports it and a shared lockfile covers
the whole workspace. Otherwise remove stale exact exclusions only after the new lockfile proves that
no selected workspace package resolves them. Also remove an exact exclusion whose version is now
older than the threshold, because it no longer changes resolution. Keep intentional package
patterns.

## 7. Clear every audit finding

Run the full dependency audit at the lowest severity, plus a production-only audit for reporting.
Fix development findings as well as production findings.

Use this order:

1. Upgrade or remove the vulnerable direct dependency.
2. Upgrade the direct parent that brings in a vulnerable transitive dependency.
3. Update the transitive lockfile resolution when its declared ranges already admit a fix.
4. Add the narrowest compatible override when no installable ancestor admits the fix.
5. Apply a local patch from a verified upstream fix when no installable fixed release exists.
6. Replace the dependency when none of the earlier options can produce a safe graph.

When a fixed release in the first three options is younger than the release-age threshold, add its
exception as described above instead of moving to an override or patch.

An audit ignore is valid only when a committed local patch contains the verified advisory fix and
the scanner cannot recognise patched package contents. Map the advisory to that patch and add a
focused regression test when the behaviour has a practical local seam. Remove both the patch and
the ignore when an upstream fixed release becomes installable.

Never ignore an unfixed advisory merely because it is development-only or unreachable in the
current application. If no safe fix exists, report the run as blocked instead of claiming success.
Treat an audit registry error as an incomplete audit.

## 8. Reconcile dependency policy

Review every dependency-management entry affected by the new graph. This includes catalogs,
overrides, patches, package extensions, peer rules, update ignores, audit ignores, release-age
exclusions, and build permissions.

- Use the field names supported by the project's pinned pnpm version. Migrate deprecated fields
  only when the target pnpm version supports their replacements.
- Remove an entry only when the resolved graph and relevant verification prove it stale.
- Keep security overrides narrow and remove them when upstream ranges resolve a fixed release.
- Keep Dependabot or Renovate rules consistent with the active holds. Remove stale bot ignores.
- Preserve dependency-bot schedules, groups, and global version strategy unless the user asks to
  change the maintenance policy.
- Do not rewrite unrelated workspace settings as part of dependency maintenance.

Treat new dependency lifecycle scripts as an execution-permission boundary. Inspect the exact
package, version, source, and script before changing `allowBuilds` or an equivalent field. Ask before
granting a new build permission unless the existing repository policy already covers that exact
package. A denied build may be recorded without executing it when the dependency works without the
script.

## 9. Update GitHub Actions

Update every external action used by workflows, reusable workflows, and composite actions. Use
pnpm's GitHub Actions support when the pinned version provides it. Otherwise resolve releases from
the action's official repository.

Preserve the repository's tag or commit-SHA policy. Report private or enterprise-hosted actions whose
refs cannot be resolved. Keep the `github-actions` section of Dependabot or Renovate current when one
exists.

## 10. Verify and review

Run focused checks after risky compatibility groups so a failure remains attributable. Then follow
the repository's documented finish order. If the repository defines no order, use this sequence:

1. Run the affected focused checks.
2. Run a frozen-lockfile install and the available peer check.
3. Run the repository's canonical full verification command, including production builds and full
   tests when that command provides them.
4. Use the "code-review" skill against the complete working-tree change. Fix every verified finding.
5. After review fixes, repeat checks whose inputs changed or whose results are stale. Repeat the full
   verification command when repository policy requires it, the dependency graph changed, or the
   remaining uncertainty spans the project. Reuse successful results for unchanged inputs.
6. Run `git diff --check`, the recursive outdated scan with GitHub Actions, the full audit, and the
   production audit.
7. Fetch the upstream again and report any commits that landed during the run.

Create a changeset or release note only when the repository requires one for the changed dependency
or peer declaration.

## 11. Report the result

Lead with the outcome: complete or blocked, the headline upgrades and security fixes, and whether
the changes are uncommitted. Put every release-age exception directly after that summary, with its
`package@version`, publication date, reason, and the date it ages past the threshold. Then name:

- The upgraded dependency families, with old and new versions, and their source migrations.
- Applied Node.js and pnpm updates, the files that name them, and available majors not adopted.
- Every retained hold, its evidence, and its removal condition.
- Overrides, patches, audit ignores, and build permissions, including those removed.
- GitHub Actions changes and unresolved private actions.
- The exact verification commands, their results, and any platform or environment not covered.
- Every intentionally remaining outdated item or blocker.

When T3 Code's `html_render` tool is available, show the report inline. Use "ux" and its HTML-report
guidance for the design, build, verification, and delivery, and read
[HTML report](references/html-report.md) for the content. Otherwise give the report as Markdown in
the final reply.
