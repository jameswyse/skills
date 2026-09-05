# Verification, review, and learning

Prove the result against the real artefact, then turn repeated corrections into mechanisms that prevent recurrence.

## Prove it works

Before running checks, identify the changed behaviours, the required repository checks, and the narrowest reliable observations that cover them. Name any remaining uncertainty that would justify broader verification. Keep this decision brief for a small change. A formatting or instruction edit needs checks suited to that artefact, not unrelated application execution.

After completing a change, ask: "How do I prove this actually works?" Check the real thing rather than a proxy, self-report, file timestamp, cached representation, or successful compilation alone.

- Build when relevant, but treat a build as necessary evidence rather than sufficient proof.
- Run the changed feature or operation and exercise its actual path.
- Check the input-to-output path needed to observe the changed behaviour.
- Exercise the full communication path when integration behaviour changed or a narrower check leaves a concrete uncertainty.
- Check process liveness directly rather than inferring it from derived state.
- Read the actual value rather than a derived or cached copy.
- Inspect the final diff and working state.
- When verification fails, check that the observation method measures the intended behaviour before changing the system again.

For delegated work, inspect the produced files, diff, logs, screenshots, or runtime behaviour. A delegate's summary reports intent, not proof.

Prefer a deterministic, repeatable command or script when the result is complex enough to justify one. Keep its output visible for review. Add or commit a lasting verification artefact only when the user authorised that work and future reviewers need it.

Before final verification, make a simplicity pass over the affected path. Remove concepts, state, branches, layers, dependencies, execution paths, and sources of truth that the finished design no longer needs. Confirm that the change did not merely move complexity into callers or retain a parallel path.

When the change added, moved, renamed, split, merged, or deleted files or directories, apply the finish pass in [Codebase organisation and naming](organisation-and-naming.md). Inspect the finished subtree, filenames, authoritative imports, and companion-file ownership.

Completion requires direct evidence for every significant behaviour change. State any path that could not be exercised and why.

Finish verification when required checks pass and the changed behaviours have adequate direct evidence. Repeat or broaden checks only after a relevant change, failure, stale result, or unresolved concern. Reuse an earlier result when its inputs and environment still apply. Do not rerun a successful check merely because another phase ended.

## Review the finished diff

Follow repository-specific review requirements first. Otherwise use the "code-review" skill before completion for changes to security boundaries, public interfaces, stored data or schemas, dependency migrations, cross-module behaviour, or tooling and instructions that govern consequential actions. Also use it when correctness remains uncertain after focused checks. A small, local change with established behaviour and adequate checks may use direct diff inspection instead. Explain that choice only when it affects confidence or differs from the user's requested review.

For explicit code-review requests, review both applicable axes even when the diff is small. The code-review skill chooses a proportionate delegated or sequential execution mode. Preserve comprehensive verification required for dependency migrations and sensitive changes.

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
