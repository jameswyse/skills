# Migrate to pnpm

Read this reference after the user agrees to migrate a Yarn or npm project to pnpm. Finish the
migration and verify it before upgrading anything, so migration failures stay separate from upgrade
failures.

## Inventory the current setup

Record the package manager and its version, including whether Yarn uses Plug'n'Play. Find every
place that depends on it:

- The lockfile, `workspaces` field, `resolutions` or `overrides`, and `packageManager` or
  `devEngines` pins.
- `.yarnrc`, `.yarnrc.yml`, `.yarn/`, `.pnp.*`, and registry or authentication settings in
  `.npmrc`.
- Package scripts, Git hooks, CI workflows and caches, Dockerfiles, deployment templates, and
  documentation that run `yarn`, `npm`, or `npx`.

## Migrate

1. Create `pnpm-workspace.yaml` from the `workspaces` field when one exists. Change internal
   dependency references to the `workspace:` protocol.
2. Run `pnpm import` to generate `pnpm-lock.yaml` from the existing lockfile, so the first install
   keeps the resolved versions. Then remove the old lockfile.
3. Move Yarn `resolutions` and npm `overrides` into pnpm `overrides`.
4. Pin pnpm the way the repository pins its other tools, and translate registry settings into
   `.npmrc` or `pnpm-workspace.yaml`. Remove Yarn-only configuration and directories.
5. Install. pnpm does not hoist undeclared dependencies, so declare each missing import in the
   package that uses it instead of enabling hoisting. Review every dependency build script under the
   main skill's build-permission rules.
6. Replace package-manager commands in scripts, hooks, CI, container builds, deployment templates,
   and documentation. Use the CI provider's pnpm setup and cache support.
7. Run the full verification sequence. Then continue with the main skill from Node.js and pnpm
   updates.

Report the migration separately from the upgrade in the final report, and suggest committing it on
its own.
