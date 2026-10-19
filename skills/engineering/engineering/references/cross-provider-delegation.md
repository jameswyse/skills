# Cross-provider delegation

Use when a skill or the global instructions send work to another model through T3 Code's orchestration tools. The caller decides whether the work goes cross-provider. This reference routes each kind of delegated work to a provider, model, and effort, then covers calling the target and falling back. Its last section covers a contrarian check from a third provider.

## Route the work

Call `orchestrator_capabilities`. Its `inheritedProviderInstanceId` and `inheritedModel` identify the session, so do not rely on your own model name. Tool names may carry a prefix such as `mcp__t3-code__`.

| Work                                                                                    | Provider                       | Model                      | Effort             |
| --------------------------------------------------------------------------------------- | ------------------------------ | -------------------------- | ------------------ |
| Taste subagents: code, architecture, and UI                                             | Same provider, native subagent | Newest Opus                | High               |
| Investigations: non-trivial debugging, unfamiliar code, computer use, and visual checks | `codex`                        | Newest listed Sol          | High               |
| A skill's cross-provider step from a `claudeAgent` Fable or Opus session                | `codex`                        | Newest listed Sol          | High               |
| A skill's cross-provider step from a `codex` Astra or Sol session                       | `claudeAgent`                  | Newest listed Opus         | High               |
| First-round code review, each axis                                                      | `codex` and `claudeAgent`      | Newest listed Sol and Opus | High               |
| The extra Correctness reviewer, the verifier, and later review rounds                   | `codex`                        | Newest listed Sol          | High               |
| A contrarian check                                                                      | `cursor`                       | Newest listed Grok         | Catalogue defaults |

Pick the highest-versioned model of that family from the target provider's `models` list instead of a remembered ID. When a native subagent tool can't select the model, use `delegate_task` on the same provider. For any other session model, keep the caller's same-provider path. First-round code review calls both providers, including the session's own, and code-review's Delegated review reference covers replacements.

T3's default effort setting is unreliable, so set High explicitly through `target.options` with the option ID the catalogue advertises for that model, such as `reasoningEffort` for Codex or `effort` for Claude, and the value `high`.

## Delegate

- Call `delegate_task` once per independent piece of work with `mode: "async"`, issuing all calls in the same step, and keep each returned `taskId`. Avoid `mode: "wait"`, which blocks each call until its child finishes. A harness that runs tool calls one at a time then runs the tasks in series.
- Each child's completion arrives as a notification. Finish any independent work, then end the turn instead of polling `task_status` or starting a watcher. Continue the calling skill once every task has completed or failed.
- Give each call a distinct `clientRequestId`, stable across retries of that call, and set `role` to match the work.
- Set `interactionMode` to `default`, because `plan` mode is deprecated.
- Set `runtimeMode` to `inherit` so the child runs under the parent thread's permission mode. Never request a different runtime mode, even when a broader one would let the child finish without approval prompts.
- The child receives only the task prompt, not the conversation or your loaded skills. Write a self-contained prompt with the objective, the relevant context and paths, a done condition, and the expected report. For an investigation, ask it to report what it actually observed without fixing anything. Ask for the report as plain text in the child's final message, not an HTML page or a link. Only the final message returns to you, and reading the child thread instead fills your context. The child runs in the same checkout as the parent and can read a private packet directory under the temporary directory.
- When the work is read-only, state in the prompt that the child must not modify files, run formatters, create commits, or change Git state.
- State in every prompt that the child must not start agents or subagents, delegate work, or apply cross-provider routing itself. The child loads the same skills, so without this it can delegate back to the parent's provider.

## Fall back

Use the caller's same-provider path when the T3 tools are absent, the target provider reports `canRunCrossProviderChildTask: false`, its catalogue lacks the target family, or the delegation fails. Report the provider and model that did the work, or the reason for the fallback.

Treat the child's report as leads under the calling skill's verification rules.

## Contrarian

Use when a calling skill asks a contrarian to argue against a judgement you've made. The calling skill decides when to ask and what the judgement covers.

- Route it as the table above describes, setting every option the catalogue lists for that Grok model to its default value. Cursor's plan fixes each model's settings and rejects a call that leaves them unset.
- Follow the Delegate rules above with `role: "review"`. Give it the judgement, your reasoning and evidence, and the relevant paths. Ask it to make the strongest evidence-based case against each part of the judgement, and to answer "no real objection" for a part where it finds none instead of inventing one.
- Skip the check instead of falling back when you're a delegated task or subagent, delegation is restricted, the session already runs on Cursor, or a Fall back condition above applies. Cursor usage is limited, so don't retry a failed call. Don't substitute another model either, because the check needs a model family that took no part in the judgement. Report that the check was skipped and why.
