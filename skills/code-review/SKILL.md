---
name: code-review
description: Use to review a code change before reporting it complete or opening a pull request, when asked to review a branch, PR, or diff, or to calibrate reviews against bot comments on past PRs.
---

# Three-axis code review

Review three axes and keep their findings apart. A change can pass one and fail another, so never merge or rerank findings across axes.

- **Standards**: repository rules and code smells.
- **Spec**: the originating request, issue, or PRD.
- **Correctness**: defects in the changed behaviour, including places outside the diff that it reaches.

## 1. Fix the scope

Run `python3 <skill-dir>/scripts/review_scope.py`, with `--base <ref>` when the user gave a fixed point. It writes `scope.diff`, `files.txt`, and `commits.txt` to a private packet directory and prints their paths as JSON. The diff runs from the merge base to a snapshot of the working tree, so commits, uncommitted changes, and untracked files form one scope. With no fixed point it reviews a dirty tree against `HEAD`, and a clean one against the pull request's base or the remote's only default branch. When it reports a bad ref or no unambiguous base, ask for a fixed point. The diff doesn't reach inside submodules, so run the script again inside each path listed under `dirty_submodules` and review that scope too. When `changed_files` is 0 and no submodule is dirty, report that there is nothing to review and stop.

Keep secrets and raw sensitive data away from reviewers. Redact them in `scope.diff` and review those hunks yourself.

**Spec.** The spec is what the change was asked to do, combined from every source that exists: the user's request for the change in this conversation, each ticket or issue that the request, the branch name, or a commit message references, which you look up, and a path the user supplied. A request only to review the change isn't a spec. Fall back to a matching Markdown file under `docs/` or `specs/` only when none of those exists. When the review runs before creating a pull request, add the drafted title and description, so every claim they make is a requirement. Write the spec to `<packet>/spec.md`. With no spec, skip the Spec axis and report "no spec available".

**Standards sources.** The repository's rule files come first and override everything below. The "engineering" skill's rules are the baseline. Then add what the diff touches:

- Code: the matching sections of [Code standards](references/code-standards.md), plus the engineering [Design](../engineering/references/design.md) reference for ownership, interface, or seam placement.
- Tests: [Testing](references/testing.md).
- Files or directories added, moved, renamed, split, merged, or deleted: [Codebase organisation and naming](references/organisation-and-naming.md).
- React code: the React Doctor section of Code standards.
- A trust boundary, authentication, authorisation, sensitive data, secrets, permissions, security configuration, or the dependency graph: security is part of Standards, scoped to the diff.

A named smell is a lead. Report it only with its concrete cost in the scoped diff.

## Another author's change

To review someone else's pull request and post or draft a comment on it, use "review-pr", which calls this skill.

When the change isn't the user's, use another-author mode, where the user's personal rules don't apply. Delegated reviewers load the user's global instructions, so state this mode at the top of every reviewer's manifest and in the verifier's and contrarian's briefs, and apply it to your own verification:

- Standards sources are the repository's rule files and the conventions in the touched files and their neighbours. The engineering baseline and named smells are reportable only when the repository's own code or rules support them.
- The spec comes from the pull request instead of this conversation. The linked ticket or issue holds the requirements, and the pull request's title and body are the author's claims to check against the change. Without a ticket or issue, the title and body are the spec.

## 2. Run the reviewers

Delegate every review, whatever its size.

Don't edit the checkout while reviewers or the verifier are running, because they read it and a changed tree makes their findings stale. Make fixes only after step 3 has verified and weighed the round's findings.

### Delegated review

Use "delegation" to route the reviewers. Its routing table names the models. In round one, Spec and Correctness each get two reviewers, one per model family, and Standards gets one.

- **Call rules.** Send one `delegate_task` per axis and model with `role: "review"`, all in the same step, including the one for the session's own provider, following that skill's Delegate section.
- **Replacement rule.** When the T3 tools are absent, a provider can't run a child task, the catalogue lacks a model, or a call fails, run the missing reviewers as native subagents without the parent's history. A replaced Claude reviewer runs on the other Claude model when the tool can select it and it didn't just fail. Every other replacement runs on the session's model. A replacement must be a model that isn't already reviewing that axis. When none is available, run the axis with one reviewer and say so in the run report.
- **No delegation at all.** Review the axes yourself, one at a time, with separate notes, and say in the report that the review ran without delegation and why.
- **Codex CLI.** When `codex` is installed, also run it in the background in every mode, as an extra reviewer whose findings go to whichever axis they belong to:

  ```bash
  codex review --base <base> -c 'sandbox_mode="read-only"' --disable multi_agent \
    -c 'developer_instructions="Review this change directly. Do not use the code-review skill, run codex review, start agents, or delegate."' \
    > <packet>/codex-review-base.txt 2> <packet>/codex-review-base.log
  ```

  Use `--uncommitted` in place of `--base <base>` for a working-tree scope, with files named `codex-review-uncommitted`, and run both with their own files when the scope has both. In another-author mode, append that mode's rules to `developer_instructions`. Read only the `.txt` output. Stop it 30 minutes after the other reviewers, or your own review, finish, and record that it didn't complete.

### Brief each reviewer

Give each reviewer a manifest: its axis, the packet path, the paths of its sources, the axis instruction, the priority definitions from step 3, and the reply format. Standards reads the standards sources, Spec reads `spec.md`, and Correctness reads [Missed findings](references/missed-findings.md). State that the reviewer covers only its axis, may read the checkout beyond the packet to trace what the change reaches, and must not modify files or Git state, recapture the scope, run this skill, or start agents. Put those prohibitions in the reviewer's task prompt itself, ahead of the manifest path, for a native subagent too.

- **Standards.** Report every breach of a documented rule, citing the rule and its source, and every named smell from the Code standards and Testing references, quoting the hunk. Mark each as a documented breach or a judgement call. Repository rules override the baseline. Skip what tooling enforces.
- **Spec.** Report missing or partial requirements, unrequested behaviour or scope creep, and requirements whose implementation looks wrong. Quote the spec line for each.
- **Correctness.** Trace each changed path from its inputs to its outputs and side effects, through empty, whitespace-padded, boundary, malformed, duplicate, and concurrent inputs, failure and retry paths, and differences between supported runtime or dependency versions. Search beyond the diff for every caller, configuration, build, deployment, and CI file the change reaches, and report places that now disagree with it. Check every Missed findings pattern. For each defect give the input or state that triggers it, how likely that is in real use, and the wrong result. Skip standards and style.

Reply format, most important first:

```text
1. [P1] src/orders/total.ts:42 One-line claim.
   Evidence: the rule or spec line quoted, or the trigger and the wrong result.
VERDICT: FINDINGS 3
```

A reviewer with nothing to report replies `VERDICT: CLEAN`. When a reply lists fewer findings than its count, ask for the rest. A reply without a verdict line, a timeout, or a failure is not a clean review.

### Gather verification evidence

Once every report is in, send all the candidates to the verifier the routing table names, in one `delegate_task` with `role: "review"`. Ask it to reproduce or refute each one against the checkout with read-only commands, and to report its evidence and verdict, how likely the trigger is in real use, the harm when it happens, and the complexity of the smallest fix. When the verifier can't run, gather this evidence yourself.

## 3. Verify and report

Every report is a lead, including the verifier's. Verify each candidate yourself:

1. Re-open the cited hunk and its surrounding context.
2. Read the cited rule or spec line from its source.
3. Confirm the concrete correctness, maintenance, or requirement impact. For a Correctness finding, confirm that the triggering input or state can occur.
4. Reject findings that are unsupported, duplicated, outside the scope, or already handled.

Then weigh each verified finding. For Correctness, judge how likely the trigger is in real use, the harm when it happens, and the complexity the fix adds. For Standards, judge the maintenance cost against the fix's complexity. A Correctness or Standards finding whose expected harm doesn't justify the fix is an accepted risk, such as a rare race that would need locking, retries, or defensive branches. Report it with that reasoning instead of fixing it. Security issues, data loss, and data corruption weigh heavily even when unlikely. A Spec finding is never an accepted risk. When its fix looks disproportionate, report it as a decision for the user.

Every other verified finding is actionable, apart from a Spec finding left for the user to decide. Give each actionable finding a priority:

- `P0`: a security issue, data loss, data corruption, or outage that normal use can reach.
- `P1`: any other wrong behaviour or missed requirement that ordinary use reaches.
- `P2`: wrong behaviour that only rare or unusual use reaches, or a maintenance cost worth fixing.
- `P3`: wording, naming, formatting, and other changes with no behavioural or requirement effect.

Ask a contrarian to argue back each rejected finding that would be `P0` or `P1` if it were real, and each accepted risk involving security, data loss, or data corruption, as the Contrarian section of "delegation" describes. Skip duplicates and items the evidence plainly refutes.

Make one final pass over the whole scope yourself for high-risk correctness or security issues the reviewers missed.

Present actionable findings and Spec decisions in your own words under `## Standards`, `## Spec`, and `## Correctness`, and accepted risks under `## Accepted risks`. Merge duplicates within an axis. Number the items in the order presented: `F1` for an actionable finding, `Q1` for a Spec decision, `R1` for an accepted risk. A later round keeps an item's ID and continues after the highest number used. Start each item with its ID, its priority when it has one, and every reviewer that reported it, such as `F1 [P1] GPT-6.2-Astra, Codex CLI`. Use "Primary" for your own final pass.

End with the run report.

## 4. Repeat after fixes

When the task authorises fixes, fix every actionable finding and rerun the checks the fixes affect. Keep going while a Spec decision waits for the user, and update a drafted pull request description to match the fixes. Then decide whether another round runs, up to three rounds per review, counting every round even when the scope grows:

- Round two runs when round one had an actionable finding above `P3`.
- Round three runs only when round two had an actionable `P0` or `P1`.

`P3` fixes need no further round. When fixes for findings above `P3` get no further round, report that those fixes had no independent review.

For a later round, run `review_scope.py --packet <packet>`. It refreshes `scope.diff` and writes `fixes.diff` with only the changes since the previous round. Send each applicable axis to its own reviewer, never one reviewer for several axes, on the later-round model from the routing table or its replacement under the replacement rule. Give each reviewer `fixes.diff`, the full `scope.diff` for context, and the earlier findings with their outcomes: fixed, accepted as a risk, or rejected with a reason. Ask them to check that each fix resolves its finding, to report defects in `fixes.diff`, to report anything outside `fixes.diff` only when it would be `P0` or `P1`, and to raise an accepted risk or rejected finding again only with new evidence. Later rounds skip the Codex CLI, the verifier, and the contrarian, so verify and weigh the findings yourself.

After each round's fixes, cut any code the actionable findings don't need, such as extra guards, options, or helpers, and rerun the checks it affects. Never accept a finding just to end the loop. When you have rejected a finding twice and it is raised again, stop arguing it and report both sides as a decision for the user, numbered as a `Q` item under its axis.

A separate change later in the task, which the global rule says needs its own review, starts a new review at round one. Delete the packet directory when the review ends.

## Run report

Keep a ledger from the first reviewer onwards: each candidate finding with its axis, every reviewer that reported it, and its outcome. End the review with this table and one line of outcomes, and put both in your reply to the user, even when a pull request description also carries them:

```markdown
| Round | Reviewer         | Standards | Spec  | Correctness |
| ----- | ---------------- | --------- | ----- | ----------- |
| 1     | GPT-6.2-Sol      | 3 / 1     | 2 / 0 | -           |
| 1     | GPT-6.2-Astra    | -         | -     | 4 / 3       |
| 1     | Claude Fable 5.2 | -         | 1 / 0 | 4 / 2       |
| 1     | Codex CLI        | 0 / 0     | 0 / 0 | 2 / 1       |
| 2     | GPT-6.2-Sol      | -         | -     | 1 / 0       |
| Bot 1 | Copilot          | 1 / 0     | 0 / 0 | 2 / 1       |

Cells show reported / verified. Verifier GPT-6.2-Sol confirmed 6 and refuted 9. Contrarian Grok 4.7
reversed 1 rejection. Actionable: Standards 1, Spec 0, Correctness 3. Worst: P1, unlocked price
saved. Accepted risks 1.
```

- One row per reviewer per round, with "-" for an axis it didn't review. "Primary" gets no row. Keep to these columns.
- Verified counts the findings that survived as actionable or accepted risks. A finding several reviewers reported counts for each of them.
- File findings from an all-axes reviewer, such as the Codex CLI or a review bot, under the axis each belongs to.
- Name each reviewer by provider and model, with failures, timeouts, and replacements and their reasons in the reviewer cell, and say why the contrarian was skipped when it was.
- When this skill's verification weighs review-bot comments, such as in a bot review, record each bot's rounds as "Bot 1", "Bot 2", and so on.

## Calibrate against bot comments

When asked to calibrate reviews, or to check what bot reviewers caught that this review missed, read [Calibration](references/calibration.md).
