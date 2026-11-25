@~/.agents/AGENTS.md

## Claude Code

When the imported instructions say to use a skill, call the Skill tool for that skill.
Call the Skill tool for "engineering" for software engineering work described above.
Call the Skill tool for "ux" for user-facing product and interface work described above.
For interface implementation, call the Skill tool for both "engineering" and "ux".

## T3 Code delegation

These rules apply in a thread I started on Opus. If you're a subagent or delegated task, or I started the thread on another model, do the work yourself. Also do trivial work yourself, such as a one-line fix or a quick lookup, instead of delegating it or starting a subagent.

- Keep taste work, such as writing code, designing architecture and building UI, in this thread or in taste subagents.
- Code review and bake-offs are exceptions to the do-it-yourself rules above, and bake-offs to the taste rule. Outside subagents and delegated tasks, run them as the code-review and bake-off skills describe.
- Delegate investigations: non-trivial debugging, computer use and visual checks. They're cheap and I have plenty of usage, so don't skip delegation to save cost. The investigator's nitpickiness is the point. Evaluate its findings and write the fix yourself.
- Consult an advisor on complex or large tasks: once you've drafted the plan, again when new information forces a major change to it, and when a hard decision comes up mid-task, such as choosing a fix once an investigation finds the cause of a complex bug. Skip it for routine or small changes. Weigh its advice and make the decision yourself.

Before delegating, call the Skill tool for "delegation". Its routing table sets the provider, model and effort for each kind of work, and the rest covers permissions and the task prompt.
