---
name: show-me-your-work
description: "Keep a reviewable decision trail for long-running or unattended work. Use a TSV log with one row per decision, covering what, why, evidence, and result. Keep it local by default. Commit it when a reviewer needs the trail to trust the result. Use for autonomous or multi-phase runs, or work a human reviews after stepping away."
---

# Show me your work

For work a human reviews after the fact, a decision trail lets them reconstruct what was decided, why, and on what evidence, without rerunning the work or reading the whole transcript. Keep one canonical log so the trail is consistent and a future agent can find it.

## The format

Use one TSV file with one row per decision. GitHub renders TSV as a sortable table. Spreadsheets and `column -s$'\t' -t` can also read it, and one command can append a row. Keep cells on one line. Evidence is a pointer, not prose.

Copy `references/decision-log-template.tsv` (the header row) to start a clean log. Columns:

- **ts.** ISO8601 timestamp. The timeline axis.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words. If a principle drove it, say it plainly, such as `explored options first because this was hard to reverse`. Do not use a jargon tag.
- **evidence.** A link or path that proves it, such as a commit SHA, PR number, `file:line`, artefact, trace, or screenshot path. Never a paragraph.
- **result.** The outcome or predicate state, such as `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, or `open`.

A reviewer can read this plain example at a glance. It is for illustration only. Do not copy these rows into a real log.

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Logging a row

Write each entry the way you'd tell a teammate what you did. Plain words, concrete actions, no AI speak or abstract jargon. Apply `$writing` to log text too. A reviewer should understand each row without decoding it.

Use `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>` so rows stay well formed. The helper stamps `ts`, writes the header on first use, and strips stray tabs and newlines. It prefixes a cell that starts with `=`, `+`, `-`, or `@` with a single quote so a spreadsheet does not execute it as a formula. A bare `printf` can also append a row. Apply the same protection when cells contain generated or user-supplied text.

Log decision points and checkpoints, not every action. Examples include choosing a fork, completing a unit with its verification result, changing direction, reverting after a trigger, finding a blocker, or fixing a check. For loop runs, write one row per iteration. Skip trivial and self-evident actions.

## Where it lives

By default, the log is an uncommitted working artefact. Keep it at `decisions.tsv`, or `.audit/<task-slug>.tsv` when several efforts run at once, and leave it out of Git. Most work does not need a committed trail. The local log still records the run accurately and can be discarded afterwards.

Commit the log only when a reviewer needs the trail to trust an ambitious result. Examples include a large cross-language port or multi-week migration where the work must demonstrate confidence. A committed log renders as a table in the PR.

## Rules

- One row is one decision or checkpoint. If it doesn't fit on one line, the decision isn't crisp yet.
- Append-only. A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence produced by committed scripts over hand-made one-offs, so a reviewer can re-run it. Read [Verification and learning](../engineering/references/verification.md#encode-lessons-in-structure) when the evidence should become a lasting guardrail.

## Audit the log against the transcript

At the end of the run, check that the log is accurate before handing back. Read this run's transcript under the active workspace's `agent-transcripts/` directory. The system prompt names the path. Do not glob across `~/.cursor/projects/*/` because that reads unrelated private chats. Compare the log with what happened:

- Every row maps to a real action. Cut invented or aspirational entries.
- Each row's evidence resolves and shows what the row claims.
- A fork, pivot, or abandoned approach that shaped the work but isn't logged is a gap. Add it.
- Drop padding. If nobody would audit a row, it doesn't earn its place.

Fix the log, not the story. If the work diverged from what a row claims, the row is wrong.

## Cross-model review of the trail

Before handing back, you must spawn a subagent from a different model family than the one that did the work. Self-review is not a substitute for an independent perspective. The subagent reads the audit trail and the run's transcript, then flags what the user should examine. It does not redo the work. It looks for weak or risky decisions.

- Decisions logged with weak or absent evidence.
- Verification steps skipped or claimed without proof in the transcript.
- Choices that look risky in hindsight, such as premature decisions, unjustified scope expansion, or changes that hide a symptom.
- Gaps the user would otherwise miss on a casual skim.

Every reply for a run that produced a trail ends with an "Attention" section. Put the reviewer's model on its own line as `reviewed by <model>`, then list each flag with a reference to specific rows or moments. "No flags" is a valid value. The model name alone is not. The self-audit checks whether the log is accurate. This review identifies what the user should still scrutinise.

## Reviewing the trail

Read from top to bottom, follow the evidence pointers, and check a sample. GitHub renders a committed TSV as a table. `column -s$'\t' -t decisions.tsv` renders it in a terminal. A row with missing evidence or an unverified result exposes a gap.

## Composing this skill

Other skills route their audit trail here instead of inventing one. Reference this skill by name and let it own the format. Do not restate the columns.
