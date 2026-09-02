# Verification, review, and learning

Prove the result against the real artefact, then turn repeated corrections into mechanisms that prevent recurrence.

## Prove it works

After completing a change, ask: "How do I prove this actually works?" Check the real thing rather than a proxy, self-report, file timestamp, cached representation, or successful compilation alone.

- Build when relevant, but treat a build as necessary evidence rather than sufficient proof.
- Run the changed feature or operation and exercise its actual path.
- Check the full input-to-output chain.
- Test integrations through the full communication path when access permits.
- Check process liveness directly rather than inferring it from derived state.
- Read the actual value rather than a derived or cached copy.
- Inspect the final diff and working state.
- When verification fails, check that the observation method measures the intended behaviour before changing the system again.

For delegated work, inspect the produced files, diff, logs, screenshots, or runtime behaviour. A delegate's summary reports intent, not proof.

Prefer a deterministic, repeatable command or script when the result is complex enough to justify one. Keep its output visible for review. Add or commit a lasting verification artefact only when the user authorised that work and future reviewers need it.

Before final verification, make a simplicity pass over the affected path. Remove concepts, state, branches, layers, dependencies, execution paths, and sources of truth that the finished design no longer needs. Confirm that the change did not merely move complexity into callers or retain a parallel path.

When the change added, moved, renamed, split, merged, or deleted files or directories, apply the finish pass in [Codebase organisation and naming](organisation-and-naming.md). Inspect the finished subtree, filenames, authoritative imports, and companion-file ownership.

Completion requires direct evidence for every significant behaviour change. State any path that could not be exercised and why.

## Review the finished diff

Repository-specific review instructions may replace or refine this step. Otherwise, when the "code-review" skill is available and the change warrants independent review, call the Skill tool for "code-review" on the finished diff. Treat changes to observable behaviour, tests, public interfaces, stored data or schemas, dependencies, security boundaries, developer tooling, or module structure as warranting review. Do this before declaring the implementation complete. A formatting-only or similarly mechanical change may rely on the repository's normal checks when those checks directly cover its risk.

Resolve verified findings that fall within the authorised change. Report findings that require broader scope. Repeat the review after fixes that substantially change the diff. Also repeat it when repository instructions require a clean review loop.

## Encode lessons in structure

When a correction, failure, or instruction repeats, encode the lesson in a mechanism instead of adding more prose. Text requires every future reader to notice, remember, and comply. Types, metadata, lint rules, canonical helpers, runtime checks, and scripts enforce the rule without cooperation.

When the same correction appears again:

1. Ask whether a type, data model, schema, lint rule, banned operation, metadata flag, canonical helper, runtime check, or script can prevent it.
2. Choose the strongest suitable mechanism: an unrepresentable state, then a compile-time or CI check, then a canonical helper, then a runtime check.
3. Within the authorised scope, implement the mechanism and remove the redundant instruction.
4. If the mechanism requires a significantly broader change, report the concrete follow-up. Do not add a local workaround in its place.
5. If the rule genuinely requires judgement, keep one prominent instruction and include the failure mode that makes it necessary.

Capture each correction and route it to the right layer. A one-off belongs in the task record. A recurring fix belongs in code or tooling. A systemic behaviour belongs in the relevant skill or policy. Close the loop instead of merely saying that the lesson will be remembered.

Avoid three incomplete responses to a lesson:

- Acknowledging the correction without recording or applying it.
- Recording a rule without moving it to the layer that can enforce it.
- Fixing one instance while leaving the recurring pattern intact.
