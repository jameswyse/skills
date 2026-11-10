# Cross-provider delegation

Use when a skill or the global instructions send work to another model through T3 Code's orchestration tools. The caller decides whether the work goes cross-provider. This reference routes each kind of delegated work to a provider, model, and effort, then covers calling the target and falling back. Its last sections cover a Fable advisor and a contrarian check from a third provider.

## Route the work

Call `orchestrator_capabilities`. Its `inheritedProviderInstanceId` and `inheritedModel` identify the session, so do not rely on your own model name. When the T3 tools are absent, use your own model name instead. Tool names may carry a prefix such as `mcp__t3-code__`.

| Work                                                                     | Provider                       | Model                                                                     | Effort                      |
| ------------------------------------------------------------------------ | ------------------------------ | ------------------------------------------------------------------------- | --------------------------- |
| Taste subagents: code, architecture, and UI                              | Same provider, native subagent | Newest Opus                                                               | High                        |
| An advisor on a plan or decision in a complex or large task              | Same provider, native subagent | Newest Fable                                                              | High                        |
| Investigations: non-trivial debugging, computer use, and visual checks   | `codex`                        | Newest listed Sol                                                         | High                        |
| A skill's cross-provider step from a `claudeAgent` Fable or Opus session | `codex`                        | Newest listed Sol                                                         | High                        |
| A skill's cross-provider step from a `codex` Astra or Sol session        | `claudeAgent`                  | Newest listed Opus                                                        | High                        |
| First-round code review, Spec and Correctness axes                       | `codex` and `claudeAgent`      | Newest listed Sol, plus Fable from an Opus session or Opus from any other | High                        |
| First-round Standards review, verifier, and later rounds                 | `codex`                        | Newest listed Sol                                                         | High                        |
| A contrarian check                                                       | `cursor`                       | Newest listed Grok                                                        | High, 256K context, Fast on |

Pick the highest-versioned model of that family from the target provider's `models` list instead of a remembered ID. When a native subagent tool can't select the model, use `delegate_task` on the same provider. For a cross-provider step from any other session model, keep the caller's same-provider path. First-round Spec and Correctness review calls both providers, including the session's own, and code-review's Delegated review reference covers replacements.

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

## Advisor

Use when the global instructions ask for a Fable advisor on a plan you've drafted or a decision you face. They decide when to ask.

- Route it as the table above describes, with the model set to Fable and the effort to `high`. When the native subagent tool can't select Fable, use `delegate_task` on the same provider and set the effort through `target.options`.
- Follow the Delegate rules above with `role: "review"`, and state that the work is read-only. Give it the goal and constraints, your draft plan or the decision with your leaning, the alternatives you rejected and why, and the relevant paths. Ask for the biggest risks, a simpler approach if one exists, and its recommendation with reasons, and to say your approach holds instead of inventing changes. On a repeat consult in the same task, also give it its earlier advice and what has changed since.
- Skip the advisor when you're a delegated task or subagent, the session already runs on Fable, the catalogue lacks Fable, or the call fails. Don't substitute another model, because the advisor exists for Fable's judgement. Report that the advisor was skipped and why.

## Contrarian

Use when a calling skill asks a contrarian to argue against a judgement you've made. The calling skill decides which judgements qualify, keeping to those where a wrong call would be costly. Grok is slow, so send every qualifying item in one call, and skip the check when none qualifies.

- Route it as the table above describes. Set the effort to `high`, the context window to `256k` and Fast to `true` through `target.options`, with the option IDs the catalogue advertises for that model, such as `reasoning_effort`, `contextWindow` and `fastMode` for Grok 4.7. Set all three, because an unset option takes the catalogue default, and Cursor rejects the default 500K context through T3 with "Invalid parameters for registry model".
- Follow the Delegate rules above with `role: "review"`. Keep the brief short, because exploring is what makes it slow. Give it the judgement, your reasoning, and the evidence quoted inline, such as the few lines of code, spec, or output each item rests on, instead of packet paths. Keep secrets and sensitive data out of the quotes. List the most relevant files by absolute path, and ask it to argue from the brief first and to open or search files only to test a specific objection. Ask it to make the strongest evidence-based case against each part of the judgement in at most three sentences per part, without restating the brief, and to answer "no real objection" for a part where it finds none instead of inventing one.
- Skip the check instead of falling back when you're a delegated task or subagent, delegation is restricted, the session already runs on Cursor, or a Fall back condition above applies. Cursor usage is limited, so don't retry a failed call. Don't substitute another model either, because the check needs a model family that took no part in the judgement. Report that the check was skipped and why.
