# Node.js and pnpm toolchain

Read this reference before changing a Node.js or pnpm pin.

## Select compatible targets

- Use a user-specified version when one was provided.
- Otherwise select the latest stable Node.js release in the pinned major line, and the latest stable
  pnpm release in its pinned major line that supports that Node.js version.
- Confirm that each exact version is published for every consumer, such as the Docker image tag,
  setup action, and deployment runtime. If one consumer lacks it, select the newest version that
  all consumers provide and report the gap.
- Adopt a new major only when the main skill allows it, and read its official migration guidance
  first.
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

Deployment configuration can live in another repository, such as infrastructure or deployment
templates that this repository's documentation, CI, or scripts name. Report the versions it pins
and any mismatch. Change it only when the user authorises work in that repository.

## Preserve each declaration's meaning

- Update exact local, CI, container, and deployment pins to the selected version.
- Keep compatibility declarations as truthful ranges. Do not turn `engines.node` into an exact pin
  when the package supports a range.
- For a published package, keep the minimum supported Node.js version represented in its engine
  range and test matrix.
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
5. If the dependency inventory already ran under the old version, repeat it because the new
   resolver may expose different peers, build scripts, release-age exclusions, or transitive
   versions.

## Confirm consistency

Search the repository again for each old version literal. Every remaining match must be
intentional, such as a changelog entry or a published library's minimum supported version. Then run
the main skill's full verification sequence under the new versions. When a container image changed,
build it if the environment can; otherwise report the image build as not verified.

