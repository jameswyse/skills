# Delegated review

Use after fixing the review scope. Brief each reviewer as the engineering skill's delegation rules
describe.

## Choose the reviewers

These are the first round's reviewers. Later rounds use the narrower set in code-review step 4.

Run each applicable axis on the first-round models the routing table of the engineering
[Cross-provider delegation](../../engineering/references/cross-provider-delegation.md) reference
assigns it. Spec and Correctness each get two independent reviewers, one per model family. Standards
gets one, because in late October 2026 a second family's Standards reviewer had the highest
rejection rate and no confirmed finding the others missed. Call `delegate_task` once per axis and
model with `role: "review"`, including for the model from the session's own provider. Follow that
reference's call rules and issue every call in the same step.

Add the extra Correctness reviewer the routing table assigns, with the Correctness prompt plus one
instruction: give every [Missed findings](missed-findings.md) pattern a verdict in turn, saying
whether it applies and what it found.

When the T3 tools are absent or a provider can't run a child task, replace the missing reviewers
with the native subagent tool on the session's model, with parent-history inheritance disabled when
the tool supports it. When stating the execution mode, name the provider and model behind each
reviewer and the reason for any replacement.

When the `codex` command is available, also run the Codex CLI review in the background as an extra
reviewer. Write its final message and its log to separate packet files:

```bash
codex review --base <base> -c 'sandbox_mode="read-only"' --disable multi_agent \
  -c 'developer_instructions="Review this change directly. Do not use the code-review skill, run codex review, start agents, or delegate."' \
  > <packet>/codex-review-base.txt 2> <packet>/codex-review-base.log
```

In another-author mode, append that mode's rules to `developer_instructions`. For a working-tree
scope, use `--uncommitted` instead of `--base <base>` and name the files
`codex-review-uncommitted`. For a scope with both, run each with its own files. The read-only
sandbox and disabled subagents stop it from starting this workflow again. Read only the `.txt` files
with the other reports before verifying. Start a 30-minute limit when the other reviewers or your
own sequential review finish. If it's still running then, stop it and note that it didn't complete.
Treat its findings as leads for whichever axis they belong to.

## Prepare the packet

Before spawning, write one frozen review packet from the scope captured in step 1. Use a private
temporary directory outside the repository with permissions limited to the current user. Give the
packet these manifests:

- The shared manifest contains status, the changed-file list, the diff, and complete untracked-file
  contents. If the review covers commits, include the commit list.
- The Standards manifest contains every standards source and the triggered sections of this
  skill's standards references.
- If a spec exists, the Spec manifest contains the spec text.
- The Correctness manifest contains the [Missed findings](missed-findings.md) reference.
- From the second round onwards, every manifest also contains a prior-findings file listing each
  earlier verified or rejected finding, its axis, and its outcome or rejection reason.

Keep secrets, credentials, and raw sensitive data out of the packet. If the scope contains such
data, redact it in the packet and record its path and digest. Review the raw item in the parent agent,
then confirm its digest before reporting. If a source could exceed the tool output limit, store it as
a separate packet file.

Give each reviewer the shared manifest and its axis manifest. Pass only the applicable packet paths
and the axis prompt. Give each round's `delegate_task` calls new `clientRequestId` values. Remove
only the exact packet files after every applicable report, including the contrarian's, has been
verified, then remove empty directories individually.

Each reviewer reviews only its assigned axis. It may read the checkout beyond the packet to trace
callers, configuration, and other code the change reaches, but must not modify files or Git state. It
does not recapture Git state, run the full review workflow, or spawn more reviewers. State these
limits in every reviewer's task prompt.

Keep every packet read below the tool output limit. If one result could truncate, split the read.
After a complete read succeeds, reopen only the cited lines needed to verify a candidate.

## Gather verification evidence

Once every report is in, send all candidate findings to the verifier model the routing table assigns
in one `delegate_task` with `role: "review"` and the same call rules. Ask it to reproduce or refute
each candidate against the checkout with read-only commands, and to report for each one its evidence
and verdict, how likely the trigger is in real use, the harm when it happens, and the complexity of
the smallest fix. Treat its report as evidence for verification. You still make each call. When the
verifier can't run, under the cross-provider reference's fallback conditions, gather this evidence
yourself.
