# Codebase organisation and naming

Treat the repository tree as an interface for maintainers. A developer should be able to predict where a capability lives, open that area, and follow its behaviour without holding unrelated parts of the system in mind.

## Organise around ownership

Group code that owns one body of knowledge and changes for the same reasons, using the repository's domain and capability language.

- Keep a capability's behaviour, types, adapters, presentation, and tests together when they change together.
- Put framework or provider code beside its only consumer. Move shared mechanism out only when several owners use it.
- Don't scatter one capability across technical directories merely to classify each file, and don't split a capability into execution phases, such as load, validate, and save, that callers must reconstruct.
- Keep small areas flat. Add a directory when it groups a coherent set a reader benefits from seeing together.
- Follow established conventions when they already make ownership clear. Don't impose a taxonomy such as layered architecture on every repository.

## Make paths predict their contents

Each path segment should narrow the reader's expectation of what the file contains and who owns it.

- Name a file after its specific concept, operation, or main export: `quoteEligibility.ts` over `policy.ts`. Match the basename to the main export where conventions allow.
- Don't use `Contract` or `Policy` as generic filename suffixes. Keep the word only when it's established domain or protocol vocabulary and the file owns that exact concept.
- Don't create files merely to group types or constants. When a separate support file has a reason to exist, prefer an honest name such as `types.ts` or `constants.ts`.
- Treat names such as `model`, `service`, `common`, `shared`, `helper`, and `utils` as prompts to look for a specific owner, not bans. With no clearer owner, prefer a small `utils` directory of specifically named files over loose support files.
- Keep sibling names in a recognisable pattern, and keep framework-mandated filenames such as route entrypoints.

## Make every path earn its place

Apply the deletion test to files and directories.

- A file earns its place when it owns behaviour, knowledge, or a supported interface. A file that only changes the import path makes the reader visit another location for nothing.
- Import directly from the authoritative module inside an application. Keep a re-exporting package entrypoint only when it defines a supported public interface.
- Keep a dispatcher when it centralises a real choice, invariant, or failure mode. Inline it when it only switches between imported functions for one caller.
- Keep a directory when its children form a coherent group. Flatten it when it adds a name and a navigation step without clarifying ownership.

File size and child count are signals, not verdicts.

## Keep companion files owned

Tests, stories, styles, fixtures, and generated artefacts need an obvious owner. Co-locate a companion with its owner when the repository allows it, and start its basename with the owner's: `Quote.history.test.tsx` belongs to `Quote.tsx`. Name a cross-module test after the combined behaviour and place it at the nearest common owner. After moving or deleting an implementation, find every companion that used its old basename or path.

## Inspect the finished tree

Before final verification, check `git diff --name-status` and the affected subtree, not only changed hunks:

1. The requested capability has an obvious route from its entrypoint to its implementation.
2. Every added or moved file and directory has a specific owner, a predictive name, and useful contents.
3. No obsolete paths, re-export-only leftovers, one-caller forwarding modules, or parallel implementations remain.
4. Companions still identify their owners, and siblings follow a recognisable pattern.
5. Architecture guidance matches any ownership rule the change altered.

Fix small adjacent problems within scope and report broader organisation problems separately.
