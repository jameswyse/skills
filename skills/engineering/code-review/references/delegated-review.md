# Delegated review

Use after fixing the review scope and choosing independent reviewers. Follow the engineering skill's delegation rules.

For the delegated path, state which axes you are delegating and spawn the applicable agents in parallel. If the tool supports disabling parent-history inheritance, disable it for each agent. Give the agents read-only tasks.

## Choose the reviewers

The reviewers depend on who requested the review.

- A user-requested review is one where the review itself is the user's task: they invoked this skill or asked for a review of a branch, PR, or diff. Spawn the agents with the native subagent tool on the session's model.
- A self-check is a review of your own change before completion, as the engineering skill requires. A request to implement something and check the result is a self-check.

For a self-check, follow the engineering [Cross-provider delegation](../../engineering/references/cross-provider-delegation.md) reference and send one `delegate_task` per axis with `role: "review"`. Its fallback returns you to native subagents on the session's model. Name the reviewing provider and model, or the fallback reason, when stating the execution mode.

## Prepare the packet

Before spawning, write one frozen review packet from the scope captured in step 1. Use a private
temporary directory outside the repository with permissions limited to the current user. Give the
packet these manifests:

- The shared manifest contains status, the changed-file list, the diff, and complete untracked-file
  contents. If the review covers commits, include the commit list.
- The Standards manifest contains every standards source and the triggered sections of this
  skill's standards references.
- If a spec exists, the Spec manifest contains the spec text.

Keep secrets, credentials, and raw sensitive data out of the packet. If the scope contains such
data, redact it in the packet and record its path and digest. Review the raw item in the parent agent,
then confirm its digest before reporting. If a source could exceed the tool output limit, store it as
a separate packet file.

Give the Standards agent the shared and Standards manifests. If a Spec agent applies, give it the
shared and Spec manifests. Pass only the applicable packet paths and the agent's axis prompt. Remove
only the exact packet files after every applicable report has been verified, then remove empty
directories individually.

Each agent reviews only its assigned axis. It does not recapture Git state, run the full two-axis
workflow, or spawn more reviewers. State these limits in every agent's task prompt.

Keep every packet read below the tool output limit. If one result could truncate, split the read.
After a complete read succeeds, reopen only the cited lines needed to verify a candidate.

