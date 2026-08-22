# Node.js and pnpm toolchain

Read this reference only after a Node.js or pnpm upgrade has been authorised.

## Select compatible targets

- Use a user-specified version when one was provided.
- For Node.js, update to the latest patch of the current supported line by default. If a newer LTS
  major exists, ask before adopting that major unless the user already requested it.
- For pnpm, select the latest stable release that supports the target Node.js version and the
  repository's required features.
- Read the official migration guidance before adopting a new Node.js or pnpm major.
- Check whether the chosen Node.js distribution still provides the Corepack behaviour that the
  repository expects.

## Find every source of truth

Search the full selected workspace and deployment configuration. Inspect at least:

- `.node-version`, `.nvmrc`, `.tool-versions`, mise configuration, and Volta configuration.
- `package.json` files for `engines`, `devEngines`, `packageManager`, and tool-specific pins.
- `pnpm-workspace.yaml` for Node.js execution settings and version-dependent pnpm fields.
- Dockerfiles, devcontainers, buildspecs, CI matrices, setup actions, and deployment manifests.
- Corepack, pnpm setup, cache-key, and package-manager commands in scripts and automation.
- Documentation that states supported or required versions.
- `@types/node` declarations in manifests and catalogs.

Use repository searches to find copied literals after locating the known sources. Inspect each
match semantically. Do not replace unrelated numbers that happen to equal the old version.

## Preserve each declaration's meaning

- Update exact local, CI, container, and deployment pins to the selected version.
- Keep compatibility declarations as truthful ranges. Do not turn `engines.node` into an exact pin
  when the package supports a range.
- For a published package, keep the minimum supported Node.js version represented in its engine
  range and test matrix.
- Align `@types/node` with the minimum runtime for a library and the deployed runtime for an
  application.
- Keep `packageManager` reproducible. Update its exact pnpm version and integrity metadata when the
  repository uses them.
- Update setup-action inputs, Docker image tags, buildspec runtimes, and documentation together.
- Change hosted-runner labels only when the user requested that infrastructure update or the new
  toolchain requires it.

## Adopt a new pnpm version

1. Update the authoritative pnpm pin and activate that exact version through the repository's
   established Corepack or setup mechanism.
2. Run the new pnpm version's configuration migration when required. Inspect every generated
   change and preserve repository policy.
3. Replace deprecated workspace fields only when the new version documents the replacement.
4. Regenerate the lockfile with the selected pnpm version. Do not hand-edit the lockfile version.
5. Repeat the complete dependency inventory because the new resolver may expose different peers,
   build scripts, release-age exclusions, or transitive versions.

Finish by confirming that every runtime source names a compatible version and by running the main
skill's full verification sequence.

