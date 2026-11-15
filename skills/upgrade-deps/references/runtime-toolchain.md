# Node.js and pnpm toolchain

## Select the targets

- Use a version the user specified. Otherwise take the latest stable Node.js release in the pinned major line, and the latest stable pnpm release in its pinned major line that supports that Node.js version.
- Confirm that each exact version is published for every consumer, such as the Docker image tag, setup action, and deployment runtime. If one lacks it, select the newest version all consumers provide and report the gap.
- Before adopting a major the main skill allows, read its official migration guidance.
- Check that the chosen Node.js distribution still provides the Corepack behaviour the repository expects.

## Update every source of truth

Find every place that names either version: version-manager files, `package.json` `engines`, `devEngines`, and `packageManager`, `pnpm-workspace.yaml`, Dockerfiles, devcontainers, buildspecs, CI matrices, setup actions, deployment manifests, Corepack and cache-key commands, documentation, and `@types/node` declarations. Then search for copied literals and judge each match by meaning.

- Update exact local, CI, container, and deployment pins to the selected version, together with setup-action inputs, image tags, and documentation.
- Keep compatibility declarations as truthful ranges. Don't turn `engines.node` into an exact pin when the package supports a range, and keep a published package's minimum supported Node.js in its engine range and test matrix.
- Keep `packageManager` reproducible, with its exact pnpm version and integrity metadata when the repository uses them.
- Change hosted-runner labels only when the user asked for that or the new toolchain requires it.
- When deployment configuration lives in another repository, report the versions it pins and any mismatch. Change it only when the user authorises work there.

## Adopt a new pnpm version

1. Update the authoritative pin and activate that exact version through the repository's Corepack or setup mechanism.
2. Run the new version's configuration migration when required, inspect every generated change, and preserve repository policy. Replace deprecated workspace fields only when the new version documents the replacement.
3. Regenerate the lockfile with the selected version.
4. Repeat any dependency inventory that ran under the old version, because the new resolver may expose different peers, build scripts, release-age exclusions, or transitive versions.

## Confirm consistency

Every remaining match for an old version literal must be intentional, such as a changelog entry or a published library's minimum supported version. Run the main skill's full verification under the new versions. When a container image changed, build it if the environment can, or report the image build as not verified.
