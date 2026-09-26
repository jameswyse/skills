# Codebase organisation and naming

Treat the repository tree as an interface for maintainers. A developer should be able to predict where a capability lives, open that area, and follow its behaviour without carrying unrelated parts of the system in mind.

## Organise around ownership

Use the repository's domain and capability language as the primary organising vocabulary. Group code that owns one body of knowledge and changes for the same reasons.

- Keep a capability's behaviour, types, provider adapters, presentation, and tests together when they change together.
- Put framework and provider code beside its consumer when only that consumer needs it. Move shared mechanism out only when several owners genuinely use it.
- Reserve global technical directories for application-wide mechanism with clear consumers. Do not scatter one capability across technical categories merely to classify each file.
- Keep small areas flat. Add a directory when it groups a coherent set that a reader benefits from seeing together.
- Follow repository conventions when they already make ownership clear. Change an established layout only when the new structure reduces total reader work.

Do not impose domain-driven design, layered architecture, or another taxonomy on every repository. Use the simplest grouping that makes ownership and navigation obvious.

## Make paths predict their contents

Read a path from left to right. Each segment should narrow the reader's expectation of what the file contains and who owns it.

- Name a behaviour or implementation file after its specific concept, operation, or main export. Prefer `quoteEligibility.ts` to `policy.ts` and `CmsBlock.ts` to `model.ts`.
- Do not use `Contract` or `Policy` as generic filename suffixes. Names such as `paymentContract.ts` and `paymentPolicy.ts` hide whether the file contains types, constants, validation, configuration, or behaviour. Preserve the word only when it is established domain or external-protocol vocabulary and the file owns that exact concept.
- Do not create or split files merely to group types or constants. Keep them with their owner when practical. When a separate support file already has a clear reason to exist and no more specific concept names it, prefer an honest contents-based name such as `types.ts` or `constants.ts` over a generic `*Contract` or `*Policy` name.
- Treat unqualified names such as `model`, `service`, `common`, `shared`, `helper`, and `utils` as prompts to look for a more specific owner, not as bans. Keep one when it is the clearest honest grouping available.
- When no clearer owner exists, prefer a small `utils` or similar directory with specifically named files over leaving several support files loose in a top-level grouping directory. Move a file out when a better owner emerges, and split the directory if its contents form clearer groups.
- Match the basename of a primary implementation to its main export when language and framework conventions permit it.
- Use recognisable patterns across siblings. A reader who understands one member of a family should be able to predict the others.
- Preserve framework-mandated filenames such as route entrypoints. Use the surrounding directories and owned modules to supply the missing context.

If a reader cannot make a useful prediction from a path, improve the name or the ownership before adding documentation that explains the surprise.

## Make every path earn its place

Apply the deletion test to files and directories as well as modules.

- A file earns its place when it owns behaviour, knowledge, or a supported interface. A file that only changes the import path usually makes the reader visit another location without hiding anything.
- Prefer direct imports from the authoritative module inside an application. Keep a package entrypoint that re-exports symbols when it defines a supported public interface and protects consumers from internal layout.
- Keep a dispatcher when it centralises a real choice, invariant, ordering rule, or failure mode. Inline it when it only switches between imported functions for one caller.
- Keep a directory when its children form a coherent group. Flatten it when the directory adds a name and a navigation step without clarifying ownership.
- Keep a small module when deleting it would scatter decisions or coordination. Combine it when deletion removes the concept entirely.
- Organise around one body of knowledge instead of splitting a capability into execution phases that callers must reconstruct.

File size and child count are signals, not verdicts. Confirm what a path owns and what deleting it would do before changing it.

## Keep companion files owned

Tests, stories, styles, fixtures, and generated artefacts should have an obvious owner.

- Co-locate a companion with its owner when the repository convention permits it.
- Start the companion basename with the owner's basename. `Quote.history.test.tsx` clearly belongs to `Quote.tsx`.
- Name a cross-module or integration test after the combined behaviour and place it at the nearest common owner.
- After moving or deleting an implementation, find every companion that used its old basename or path.
- Treat a companion without a matching owner as a candidate. Inspect framework conventions and cross-module intent before calling it orphaned.

Automate owner checks only when the repository can express its valid exceptions. A noisy rule teaches maintainers to ignore the result.

## Inspect the tree before changing it

Before implementation:

1. Inspect the affected subtree, its entrypoints, its sibling names, and any architecture guidance.
2. Identify the module that owns the requested behaviour and the reason that module changes.
3. Trace one representative path from entrypoint to outcome. Note each directory a maintainer must leave to understand it.
4. Search for an existing owner before creating another file, directory, type, adapter, or helper.
5. Choose a destination whose path predicts the new responsibility. Confirm that a new layer removes more reader work than it adds.

Keep this inspection proportional to the task. Review the affected area and the callers needed to judge it. Do not turn a small change into an unrequested repository-wide reorganisation.

## Reconsider the structure during the change

Revisit the layout when implementation reveals a different owner, repeated coordination, an unexpected second consumer, or a file that no longer has independent meaning.

When an authorised internal refactor chooses a new location, migrate callers and remove the old path in the same change. Retain a forwarding entrypoint only for a real compatibility requirement.

## Inspect the finished tree

Before final verification:

1. Inspect the complete affected subtree and `git diff --name-status`, not only changed hunks.
2. Start at the repository tree and confirm that the requested capability has an obvious route from its entrypoint to its implementation.
3. Check every added or moved file and directory for a specific owner, a predictive name, and useful contents.
4. Remove obsolete paths, re-export-only leftovers, one-caller forwarding modules, and parallel implementations that the change no longer needs.
5. Find tests, stories, styles, fixtures, and generated artefacts whose basename or path no longer identifies an owner.
6. Compare sibling filenames and exports for a recognisable pattern.
7. Update architecture guidance when the authorised change alters a documented ownership rule.

Fix small adjacent problems when they are within scope and make the result coherent. Report broader organisation problems separately.
