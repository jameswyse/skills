# Cross-provider delegation

Use when a skill sends work to a model from the other provider through T3 Code's orchestration tools. The calling skill decides whether the work goes cross-provider. This reference covers choosing the target, calling it, and falling back.

## Choose the target

Call `orchestrator_capabilities`. Its `inheritedProviderInstanceId` and `inheritedModel` identify the session, so do not rely on your own model name. Tool names may carry a prefix such as `mcp__t3-code__`.

| Session                                     | Target provider | Target model       |
| ------------------------------------------- | --------------- | ------------------ |
| `claudeAgent` running a Fable or Opus model | `codex`         | Newest listed Sol  |
| `codex` running an Astra or Sol model       | `claudeAgent`   | Newest listed Opus |

Pick the highest-versioned model of that family from the target provider's `models` list instead of a remembered ID. For any other session model, keep the calling skill's same-provider path.

Always request High reasoning effort. T3's default effort setting is unreliable, so set it explicitly through `target.options` with the option ID the catalogue advertises for that model, such as `reasoningEffort` for Codex or `effort` for Claude, and the value `high`.

## Delegate

- Call `delegate_task` once per independent piece of work with `mode: "async"`, issuing all calls in the same step, and keep each returned `taskId`. Avoid `mode: "wait"`, which blocks each call until its child finishes. A harness that runs tool calls one at a time then runs the tasks in series.
- Each child's completion arrives as a notification. Finish any independent work, then end the turn instead of polling `task_status` or starting a watcher. Continue the calling skill once every task has completed or failed.
- Give each call a distinct `clientRequestId`, stable across retries of that call, and set `role` to match the work.
- Set `interactionMode` to `default`, because `plan` mode is deprecated. Leave `runtimeMode` unset so it inherits.
- The child receives only the task prompt, not the conversation or your loaded skills. Write a self-contained prompt with the objective, the relevant paths, and the expected report. The child runs in the same checkout as the parent and can read a private packet directory under the temporary directory.
- When the work is read-only, state in the prompt that the child must not modify files, run formatters, create commits, or change Git state.
- State in every prompt that the child must not start agents or subagents, delegate work, or apply cross-provider routing itself. The child loads the same skills, so without this it can delegate back to the parent's provider.

## Fall back

Use the calling skill's same-provider path when the T3 tools are absent, the target provider reports `canRunCrossProviderChildTask: false`, its catalogue lacks the target family, or the delegation fails. Report the provider and model that did the work, or the reason for the fallback.

Treat the child's report as leads under the calling skill's verification rules.
