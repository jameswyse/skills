---
name: upgrade-deps
description: Use when asked to upgrade all dependencies of a pnpm project, including the Node.js and pnpm toolchain and GitHub Actions. Not for bumping one package.
---

# Upgrade dependencies

Upgrade the whole pnpm project to the newest compatible stable dependency set. The repository's instructions, workspace definition, manifests, and lockfile are the sources of truth. The request authorises the local changes the upgrade needs. It doesn't authorise a commit, push, publication, deployment, or unrelated cleanup.

## Done when

- Node.js and pnpm run the latest release of their current major lines, and every source that names either version agrees.
- The root project and every package selected by `pnpm-workspace.yaml` have been inventoried.
- Every outdated dependency and GitHub Action is at its resolved target, under a verified compatibility hold, or a release that appeared or became eligible after the targets were resolved.
- Every audit finding is fixed, development ones included.
- The dependency-policy entries the new graph affects are current, with no proven-stale entry left.
- The repository's full verification command passes. Without one, every available format, lint, typecheck, build, and test check passes.
- "code-review" has reviewed the complete change, and its actionable findings are fixed and rechecked.
- The final outdated scan, peer check, frozen-lockfile install, and audit pass.

When the environment prevents a required check, or an advisory has no safe fix, report the run as blocked instead of complete.

## 1. Prepare

- Preserve every unrelated staged, unstaged, and untracked change.
- Check the command help and current documentation for the pnpm version you will run before relying on version-specific flags or fields.
- When the branch tracks an upstream, fetch it and fast-forward with `git merge --ff-only` before changing anything. If it has diverged or the fast-forward fails, report that and continue on the local branch.
- If the repository uses Yarn or npm, ask once whether to migrate it to pnpm first. If the user agrees, follow [Migrate to pnpm](references/pnpm-migration.md) before continuing. Otherwise stop.
- Work on the packages `pnpm-workspace.yaml` selects, not arbitrary nested `package.json` files, and account for the root separately.
- Resolve and install under the committed workspace policy. Never bypass registry routing, trust policy, package selection, patches, release age, or build policy to make an update pass.
- Keep logs and scratch output in one run directory under `$TMPDIR`, and remove it after delivering the report.

## 2. Update Node.js and pnpm

Before the inventory, update each to the latest release in its current major line without asking, and activate both so the inventory, lockfile, and checks run under them. Read [Node.js and pnpm toolchain](references/runtime-toolchain.md) before changing a pin. Adopt a new major only when the user asked for it or approves it. Otherwise report the available major and its support status.

## 3. Inventory and resolve targets once

Inventory every manifest dependency field, catalog, alias, Git or tarball dependency, patch, and workspace protocol, every policy entry (`overrides`, `packageExtensions`, `peerDependencyRules`, `update.ignoreDeps`, audit and release-age exceptions, build permissions, and the Dependabot or Renovate holds that mirror them), outdated direct and transitive resolutions including stable majors, vulnerabilities at the lowest audit severity, and GitHub Actions in workflows, reusable workflows, and composite actions. A non-zero exit for outdated dependencies is data, not a failure. Record registry errors and unresolved private dependencies as coverage gaps.

Resolve every target once per run, GitHub Actions included. This inventory and the step 2 versions set the targets, and step 4's transitive refresh finalises them before the first full verification. After that, "latest" means the resolved target. A release that appears or becomes eligible later waits for the next run and is reported.

## 4. Upgrade the compatible set

Target the latest stable releases, majors included. Dependency majors need no approval, unlike the Node.js and pnpm majors in step 2. Leave intentional prerelease pins and non-registry sources alone unless repository evidence shows they should move.

- Upgrade related package families together, derived from peer ranges, release notes, and the dependency graph.
- Preserve exact pins, range operators, aliases, catalogs, and workspace protocols unless the migration needs a different declaration. Keep shared versions in an existing catalog, and move one in when several packages need it aligned.
- Prefer updating the responsible direct dependency over forcing a transitive child.
- Read the official migration guidance for each major and apply the changes it requires. A failure is migration evidence, so fix the incompatibility at its source before introducing a hold.
- Fix what the upgrade causes or exposes in the same change: renamed or removed configuration keys, dependencies made unused, and new deprecation, lint, or type warnings. Remove a dependency only when usage and verification prove it safe.
- Stop and ask only when the newest release needs a product, public-interface, deployment, or architecture decision outside maintenance work.

After each updater command, revert what the upgrade didn't need:

- catalog entries or ranges moved for a package in `update.ignoreDeps` or under a hold;
- range operators changed against the repository's style or `savePrefix`;
- companion ranges loosened, such as an `@types/node` range that leaves the runtime's major line;
- GitHub Action refs switched between tags and commit SHAs, or version comments duplicated.

Type packages are companions, not targets. Keep `@types/*` on the runtime package's API line, with an application's `@types/node` on its deployed Node.js major and a published library's on its minimum supported one, and drop a type package the runtime package now replaces. Don't narrow `peerDependencies` to the installed version. Update the development dependency that exercises the peer, verify the supported range, and widen or move it only when the package truly supports it.

Finish the graph before the first full verification: `pnpm update -r`, `pnpm dedupe`, then `pnpm dedupe --check`.

## 5. Compatibility holds

Hold a package only after its latest release has failed a relevant build, test, runtime check, or documented compatibility requirement.

- Pin the narrowest working version, and scope every ignore, peer rule, and override to the incompatible package or parent-child edge. Update parent-version selectors when the parent moves.
- Record the reason and removal condition in the commit message and final report, not in a code comment.
- Re-evaluate every existing hold and local patch on each run against current release notes and a retest of the latest release. Don't carry one forward from earlier reports, notes, or commit messages.
- Don't hide a peer warning until the installed combination is verified, and don't use an override to conceal an incompatible major.

## 6. Release-age exceptions

Never reduce, remove, or bypass `minimumReleaseAge`. Select the newest release that satisfies it, and report a newer one that is still too young with the date it becomes eligible. Don't wait for it. List these in the first progress update after the inventory, without pausing, so the user can ask for an exception before verification starts.

Add an exact `package@version` entry to `minimumReleaseAgeExclude` without asking when a too-young release fixes an audit finding, unblocks other upgrades, or lets you remove an override, patch, hold, or other policy entry. Prefer this to an override or local patch. Include the platform-specific and companion packages that release requires and nothing else, never a pattern or an unversioned name. Apply the same test to exclusions a mutating audit fix adds.

Remove an exact exclusion once the new lockfile proves no selected package resolves it, or its version is older than the threshold. Use `minimumReleaseAgeExcludePrune` when the pnpm version supports it and one lockfile covers the workspace. Keep intentional package patterns.

## 7. Audit findings

Run the full audit at the lowest severity, plus a production-only audit for reporting. Fix each finding with the first of these that works: upgrade or remove the vulnerable direct dependency, upgrade the parent that brings in a vulnerable transitive one, update the lockfile resolution when the declared ranges already admit a fix, add the narrowest compatible override when no installable ancestor admits the fix, apply a local patch from a verified upstream fix when no installable fixed release exists, or replace the dependency when nothing else gives a safe graph. When the fixed release in the first three is too young, add its release-age exception instead of moving on to an override.

An audit ignore is valid only when a committed local patch contains the verified fix and the scanner can't recognise patched contents. Map the advisory to the patch, add a focused regression test when the behaviour has a practical local seam, and remove both once an upstream fix is installable. Never ignore an advisory because it is development-only or unreachable, and treat an audit registry error as an incomplete audit.

## 8. Dependency policy

Review every policy entry the new graph affects. Use the field names the pinned pnpm version supports. Remove an entry only when the resolved graph and verification prove it stale, and drop a security override once upstream ranges resolve a fixed release. Keep Dependabot or Renovate rules consistent with the active holds, and leave their schedules, groups, and version strategy alone.

A new dependency lifecycle script is an execution-permission boundary. Inspect the exact package, version, source, and script, and ask before granting a build permission the existing policy doesn't already cover for that package. A denied build can be recorded without running it when the dependency works without the script.

## 9. GitHub Actions

Update every external action in workflows, reusable workflows, and composite actions, through pnpm's GitHub Actions support when the pinned version has it, otherwise from each action's official repository. Preserve the repository's tag or commit-SHA policy, report private or enterprise-hosted actions whose refs can't be resolved, and keep the bots' `github-actions` section current.

## 10. Verify and review

Run focused checks after risky compatibility groups so a failure stays attributable. Then follow the repository's documented finish order, or this one:

1. The affected focused checks.
2. A frozen-lockfile install and the available peer check.
3. The full verification command, including production builds and full tests when it provides them.
4. "code-review" against the complete working-tree change, fixing every actionable finding.
5. After review fixes, the checks whose inputs changed. Repeat full verification when repository policy requires it, the graph changed, or the uncertainty spans the project.
6. `git diff --check`, the recursive outdated scan with GitHub Actions, the full audit, and the production audit. Report releases newer than the resolved targets instead of upgrading them.
7. Fetch the upstream again and report commits that landed during the run.

Create a changeset or release note only when the repository requires one for the changed dependency or peer declaration.

## 11. Report

Lead with the outcome: complete or blocked, the headline upgrades and security fixes, and whether the changes are uncommitted. Put every release-age exception straight after that, with its `package@version`, reason, and the date it ages past the threshold. Then name:

- the upgraded families with old and new versions, and their source migrations;
- Node.js and pnpm updates, the files that name them, and majors not adopted;
- every retained hold with its evidence and removal condition;
- overrides, patches, audit ignores, and build permissions, including those removed;
- GitHub Actions changes and unresolved private actions;
- the exact verification commands, their results, and any platform or environment not covered;
- every remaining outdated item or blocker, including releases deferred to the next run.

When T3 Code's `html_render` tool is available, show the report inline with the "html-report" skill and the template in [HTML report](references/html-report.md). Otherwise give it as Markdown in the final reply.
