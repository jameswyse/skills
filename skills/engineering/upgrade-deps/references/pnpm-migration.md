# Migrate to pnpm

Finish the migration and verify it before upgrading anything, so migration failures stay separate from upgrade failures.

1. Record the current package manager and version, including whether Yarn uses Plug'n'Play, and find everything that depends on it: the lockfile, `workspaces`, `resolutions` or `overrides`, `packageManager` or `devEngines` pins, `.yarnrc*`, `.yarn/`, `.pnp.*`, registry and authentication settings, and every script, Git hook, CI workflow and cache, Dockerfile, deployment template, and document that runs `yarn`, `npm`, or `npx`.
2. Create `pnpm-workspace.yaml` from the `workspaces` field when one exists, and change internal dependency references to the `workspace:` protocol.
3. Run `pnpm import` to generate `pnpm-lock.yaml` from the existing lockfile, so the first install keeps the resolved versions. Then remove the old lockfile.
4. Move Yarn `resolutions` and npm `overrides` into pnpm `overrides`. Pin pnpm the way the repository pins its other tools, translate registry settings, and remove Yarn-only configuration and directories.
5. Install. pnpm doesn't hoist undeclared dependencies, so declare each missing import in the package that uses it instead of enabling hoisting. Review every dependency build script under the main skill's build-permission rule.
6. Replace package-manager commands everywhere step 1 found them, using the CI provider's pnpm setup and cache support.
7. Run the full verification sequence, then continue with the main skill from the Node.js and pnpm update.

Report the migration separately from the upgrade, and suggest committing it on its own.
