---
name: principle-prove-it-works
description: "Apply after changing code, configuration, data, or external state, before declaring done. Verify against the real artefact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
---

# Prove it works

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles."

**Why:** Unverified work has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) feels cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

**Pattern:** After completing any task, ask: "how do I prove this actually works?"

Check the real thing, not a proxy:
- Check process liveness directly, not indirectly through derived state
- Read the actual value, not a cached or derived representation
- When verification fails, suspect the observation method before suspecting the system

Code and features:
1. Build it (necessary but not sufficient)
2. Run it and exercise the actual feature path
3. Check the full chain: does data flow from input to output?
4. For integrations, test the full communication path end-to-end

Delegation: trust artefacts, not self-reports.
When verifying delegated work, inspect the actual output artefact (git diff, file contents, runtime behaviour), not the delegate's summary. Agents report what they intended, not always what happened.

## Script the check when you can

The strongest proof is a deterministic script that re-runs the same comparison, not a one-time eyeball. Write the script, run it, and keep its output as an artefact a reviewer can re-run instead of trusting your word. A script comparing the old and new compiled output catches what a glance misses.

Keep the artefact visible for the human. Commit it only for large or complex work where the trail has to be auditable later, such as a big port or migration. Use `$show-me-your-work` when the task needs that durable trail. Most work just needs the artefact visible, not committed.
