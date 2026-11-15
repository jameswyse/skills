# Codebase organisation and naming

The repository tree is an interface for maintainers, who should be able to predict where a capability lives. Follow established conventions when they already make ownership clear, and don't impose a taxonomy such as layered architecture.

## Ownership

- Keep a capability's behaviour, types, adapters, presentation, and tests together when they change together. Don't scatter it across technical directories or split it into execution phases, such as load, validate, and save, that callers must reconstruct.
- Put framework or provider code beside its only consumer, and move shared mechanism out only when several owners use it.
- Keep small areas flat. A directory must group a coherent set, not add a navigation step.

## Names

- Name a file after its specific concept, operation, or main export: `quoteEligibility.ts` over `policy.ts`. Match the basename to the main export where conventions allow.
- Don't use `Contract` or `Policy` as generic filename suffixes. Keep the word only when it's established domain or protocol vocabulary and the file owns that exact concept.
- Don't create files merely to group types or constants. A support file with a reason to exist gets an honest name such as `types.ts` or `constants.ts`.
- `model`, `service`, `common`, `shared`, `helper`, and `utils` are prompts to look for a specific owner, not bans. With no clearer owner, prefer a small `utils` directory of specifically named files.
- Keep sibling names in a recognisable pattern, and keep framework-mandated filenames.

## Every path earns its place

- A file earns its place when it owns behaviour, knowledge, or a supported interface. Delete one that only changes the import path. Import directly from the authoritative module, and keep a re-exporting entrypoint only when it defines a supported public interface.
- Keep a dispatcher that centralises a real choice, invariant, or failure mode, and inline one that only switches between imported functions for one caller.
- File size and child count are signals, not verdicts.

## Companion files

Co-locate tests, stories, styles, fixtures, and generated artefacts with their owner when the repository allows it, and start the basename with the owner's: `Quote.history.test.tsx` belongs to `Quote.tsx`. Name a cross-module test after the combined behaviour and place it at the nearest common owner. After moving or deleting an implementation, find every companion that used its old basename or path.

## Inspect the finished tree

Check `git diff --name-status` and the affected subtree, not only changed hunks. The capability has an obvious route from its entrypoint to its implementation. Every added or moved path has a specific owner, a predictive name, and useful contents. No obsolete path, re-export-only leftover, one-caller forwarding module, or parallel implementation remains. Companions still identify their owners. Architecture guidance matches any ownership rule the change altered. Fix small adjacent problems within scope and report broader ones separately.
