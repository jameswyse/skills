# Root-cause fixes

Trace problems to their source and fix them there. Symptom fixes accumulate, make the system harder to reason about, and leave the real defect in place.

## Scope follows the root cause

A requested outcome, not an anticipated file list, defines the working scope. When a small, reversible source fix requires adjacent consumer, test, type, configuration, fixture, or tooling changes, make them without pausing. A correct source fix that touches several consumers is preferable to a local workaround that keeps the diff narrow.

Search for the pattern, not only the reported instance. Fix minor, clearly equivalent instances when leaving them would preserve inconsistent behaviour. Continue ordinary implementation work when a nearby defect blocks the requested validation or would otherwise force compensating code.

Pause before a source fix that significantly changes the intended outcome, a public or external interface, data, dependencies, infrastructure, product risk, or the size of the work. State the root cause, the required expansion, and why a narrow workaround would make the system worse.

## Fix root causes

- Use a practical reproduction to verify the reported behaviour. When it is unavailable, distinguish source evidence and focused checks from the unverified original runtime symptom.
- Ask "why" until you reach the root cause.
- Resist guards that only silence a crash. A nil check around invalid state preserves the defect.
- If a workaround needs a paragraph-long comment, fix the code instead of explaining the workaround.
- Search for the same pattern and account for every instance. Fix equivalent minor instances now. Report instances whose repair needs a significantly larger change.
- When stuck, instrument. Read the actual error and state instead of guessing.
- Place validation and repair at the seam where invalid state enters. Do not scatter checks through consumers.
- Prefer repairing the authoritative type, structure, configuration, or source of truth and updating its consumers over adding downstream exceptions.

## Suspect state after a restart

Code does not change between runs. State does. When something fails after a restart, inspect persistent state first: configuration files, caches, lock files, and serialised state. If clearing a state file restores behaviour, prioritise state validation or reconciliation as the fix.
