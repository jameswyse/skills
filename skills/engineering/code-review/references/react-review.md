# React review

For a scope that affects React code, apply these instructions to the Standards review in either mode:

- Check for a repository package script or project-local `react-doctor` executable.
- If one is already runnable, use it with the repository's existing configuration. Leave installs
  and upgrades outside the review.
- Return a concise execution summary with the command, version when available, scope or coverage,
  and counts.
- Return only diagnostics relevant to scoped findings or configuration candidates.
- If no runnable command exists, state that.

## Findings and configuration candidates

Include every React Doctor diagnostic that supports an issue in the scoped diff, with its location. Separately report confirmed recurring false positives or repository-accepted patterns. Name the diagnostic, explain why it is non-actionable, and propose the narrowest suppression that keeps actionable instances visible. Configuration candidates are not findings.

Verify each candidate against the diagnostic, code, and current configuration. If necessary, run the narrowest check that resolves uncertainty. Reject unsupported candidates and suppressions that could hide real issues.

After Standards and Spec, list supported candidates under `## React Doctor configuration`. Explain the repeated noise each would remove. Omit the section when there are none. Change configuration only when the user has authorised it; carry forward existing authority and otherwise ask about the concrete proposal.
