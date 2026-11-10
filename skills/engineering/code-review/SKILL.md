---
name: code-review
description: Review a branch, PR, working-tree diff, or changes since a fixed point against standards, the request, and correctness, or calibrate reviews against bot comments on past PRs.
---

# Three-axis code review

Review three axes separately. **Standards** covers repository rules and code smells. **Spec** covers
the originating request, issue, or PRD. **Correctness** covers defects in the changed behaviour,
including places outside the diff that it reaches. A change can pass any axis and fail another. Do
not merge or rerank findings across axes.

Use the "engineering" skill as the baseline for code, tests, dependencies, package
management, and developer tooling. This skill owns the detailed standards. Choose them from the
reviewed behaviour. The author does not need to have read them for the result to meet them:

- For code, read the sections of [Code standards](references/code-standards.md) that the diff
  touches: machinery and reader load, domain modelling, types and seams, failures, reliable
  operations, migrations, security, and named smells. For ownership, interface
  compression, or seam placement, also read the engineering [Design](../engineering/references/design.md)
  reference.
- When the scope contains tests, read [Testing](references/testing.md) and use its named test smells.
- When the scope adds, moves, renames, splits, merges, or deletes files or directories, read
  [Codebase organisation and naming](references/organisation-and-naming.md). Apply it to the
  affected subtree, authoritative imports, naming patterns, and companion-file ownership.

Do not load every section for a small diff.

Treat security as part of Standards when the diff changes a trust boundary, authentication,
authorisation, sensitive data, secret handling, permissions, security configuration, or the
dependency graph. Keep this check scoped to the diff and the context needed to verify it. Recommend
the user-invoked "improve-security" skill only when the user requests a dedicated security review.

## Another author's change

To review someone else's pull request and post or draft a comment on it, use "pull-request-reviews",
which calls this skill.

When the change isn't the user's, use another-author mode, where the user's personal rules don't
apply. Delegated reviewers load the user's global instructions, so state this mode at the top of the
Standards manifest and in every reviewer, verifier, and contrarian prompt, and apply it to your own
verification:

- Standards sources are the repository's rule files and the conventions in the touched files and
  their neighbours. The engineering baseline and named smells are leads, reportable only when the
  repository's own code or rules support them.
- The linked ticket or issue holds the requirements, and the pull request's title and body are the
  author's claims to check against the change. Without a ticket or issue, the title and body are the
  spec.

## 1. Fix the scope

- When the user supplies a fixed point, verify it with `git rev-parse`, capture
  `git diff <ref>...HEAD` once, and note `git log <ref>..HEAD --oneline`. If the working tree is
  dirty, also capture `git diff HEAD` and the complete contents of untracked files from
  `git status --short`. Review the committed and working-tree diffs as one scope without
  double-counting overlapping findings.
- When no fixed point exists and the working tree is dirty, use `git diff HEAD` plus the complete
  contents of untracked files from `git status --short`.
- When no fixed point exists and the working tree is clean, resolve the comparison branch from
  current PR metadata when available. Otherwise use the remote default branch from
  `refs/remotes/*/HEAD` when exactly one is available. Verify the resolved ref, then capture
  `git diff <base>...HEAD` and
  `git log <base>..HEAD --oneline` once. If no unambiguous base exists, ask for a fixed point.
- For a bad ref or ambiguous base, stop and ask for a valid scope. For a verified empty diff, report
  that there are no changes to review and stop.

For working-tree reviews, the user request is the spec. Otherwise find it in order from issue
references in commit messages, a user-supplied path, then a matching Markdown file under `docs/` or
`specs/`. When the review runs before creating a pull request, add the drafted title and description
to the spec, so every claim they make is a requirement. If no spec exists, skip the Spec agent and
report "no spec available".

Standards sources are repository files that define how code is written, the engineering skill,
and the triggered standards references above. Repository rules override the baseline. Treat named
smells as leads and report only a concrete cost in the scoped diff.

## 2. Run the reviewers

Start the ledger described in [Run report](references/run-report.md) before the first reviewer runs.
Delegate every review, whatever its size. Run each applicable axis on its first-round review models
in parallel, as [Delegated review](references/delegated-review.md) describes. Read it before
preparing the packet. Only when delegation is unavailable or restricted, inspect the axes
sequentially in the primary agent with the captured scope and the axis prompts below, keeping each
axis's notes separate, and still run the Codex CLI reviewer that Delegated review describes. State
which mode was used and why.

### Standards agent

When the scope affects React code, read the React Doctor section of [Code standards](references/code-standards.md) for tool use, diagnostic evidence, and configuration candidates.

Ask:

> Report by file and hunk:
> 1. Every documented-standard violation, citing the rule and its source.
> 2. Every named smell from the Code standards reference, naming it and quoting the hunk.
> 3. Every named test smell from the Testing reference when the scope contains tests.
> Separate hard documented breaches from baseline judgement calls. Repository rules override the
> baseline. Skip other tooling-enforced issues.
> Put the highest-impact findings first. Return all supported findings concisely. If the tool output limit would
> truncate the report, return the first batch and state how many supported findings remain.

### Spec agent

Ask:

> Report missing or partial requirements, unrequested behaviour or scope creep, and apparently
> implemented requirements whose implementation looks wrong. Quote the relevant spec
> line for every finding. Return all supported findings concisely. If the tool output limit would
> truncate the report, return the first batch and state how many supported findings remain.

### Correctness agent

Ask:

> Find defects in the changed behaviour. Trace each changed path from its inputs to its outputs and
> side effects, including empty, whitespace-padded, boundary, malformed, duplicate, and concurrent
> inputs, failure and retry paths, and differences between supported runtime or dependency versions.
> Search the checkout beyond the diff for every caller, configuration, build, deployment, and CI
> file the changed behaviour reaches, and report places that now disagree with it. Check every
> pattern in the [Missed findings](references/missed-findings.md) reference. For each defect, give
> the file and line, a concrete input or state that triggers it, how likely that is in real use, and
> the wrong result. Skip standards and style issues. Return all supported findings concisely. If
> the tool output limit would truncate the report, return the first batch and state how many
> supported findings remain.

## 3. Verify and report

Treat every report as a lead, not proof. Request any remaining batches and read the verifier's
evidence from [Delegated review](references/delegated-review.md) when it ran. Then verify every
candidate finding yourself:

1. Re-open the cited hunk and its surrounding context.
2. Read the cited rule or spec line from its source.
3. Confirm the concrete correctness, maintenance, or requirement impact. For a Correctness finding,
   confirm that the triggering input or state can occur.
4. Reject findings that are unsupported, duplicated, outside the fixed scope, or already handled.

Then weigh each verified finding before recommending a fix. For a Correctness finding, judge how
likely its trigger is in real use, how much harm it causes when it happens, and how much complexity
the fix adds. For a Standards finding, judge its maintenance cost against the fix's complexity. A
Correctness or Standards finding whose expected harm doesn't justify the fix's complexity is an
accepted risk, such as a rare edge case or race that would need locking, retries, or defensive
branches. Report it with that reasoning instead of fixing it. Security issues, data loss, and data
corruption weigh heavily even when unlikely. A Spec finding is never an accepted risk. When its fix
looks disproportionate, report it as a decision for the user.

Every other verified finding is actionable, apart from a Spec finding left for the user to decide.
Give each actionable finding a priority:

- `P0`: a security issue, data loss, data corruption, or outage that normal use can reach.
- `P1`: any other wrong behaviour or missed requirement in real use.
- `P2`: a problem with limited or rare effect, or a maintenance cost worth fixing.
- `P3`: wording, naming, formatting, and other changes with no behavioural or requirement effect.

Ask a contrarian to argue back each rejected finding that would be `P0` or `P1` if it were real,
and each accepted risk involving security, data loss, or data corruption, as the engineering
[Cross-provider delegation](../engineering/references/cross-provider-delegation.md#contrarian)
reference describes. Give it each item with its quoted evidence and your reason. Skip duplicates and
items the evidence plainly refutes.

Make one final pass over the complete scope for high-risk correctness or security issues the agents
missed. Present actionable findings and Spec decisions in your own words under `## Standards`,
`## Spec`, and `## Correctness`, and accepted risks under `## Accepted risks`. Merge duplicates
within an axis, including the same finding from several reviewers, but do not merge or rerank
findings across axes.

Give each presented item an ID, numbered in the order presented: `F1` for an actionable finding,
`Q1` for a Spec decision, and `R1` for an accepted risk. A later round keeps an item's ID and
continues after the highest number used. Start each item with its ID, its priority when it has one,
and every reviewer that reported it, as named in the run report or "Primary", such as
`F1 [P1] GPT-6.1-Sol, Claude Fable 5.2`.

End with the run report.

## 4. Repeat after fixes

When the task authorises fixing findings, first snapshot the working tree from the repository root,
so a later round can review only the fixes:

```bash
cp "$(git rev-parse --git-path index)" <packet>/before.index
GIT_INDEX_FILE=<packet>/before.index git add -A
GIT_INDEX_FILE=<packet>/before.index git write-tree
```

Keep the printed tree ID. Then fix every actionable finding, rerun the checks the fixes affect, and
continue with the rest while a Spec decision waits for the user. When the spec includes a drafted
pull request description, update it to match the fixes. Stop when the round had no actionable
finding above `P3`. `P3` fixes don't need another round.

Otherwise run a narrower round on the fixes. Take the same snapshot into `after.index`, and capture
`git diff <before-tree> <after-tree>` as the fix diff. Send one later-round reviewer per applicable
axis the fix diff, the full current diff for context, and the earlier findings with their outcomes:
fixed, accepted as a risk, or rejected with a reason. Ask reviewers to raise an accepted risk or
rejected finding again only with new evidence. Later rounds use only the later-round model from
Delegated review's routing and skip the Codex CLI, the verifier, and the contrarian. When that model can't run, use Delegated review's replacement rule. Verify and weigh
the findings as in step 3.

Run at most three rounds per task, counting every round even when the scope grows. If the third
round still has actionable findings above `P3`, fix them and report that those fixes had no
independent review.

## Calibrate against bot comments

When asked to calibrate reviews, or to check what bot reviewers caught that this review missed, read
[Calibration](references/calibration.md).
