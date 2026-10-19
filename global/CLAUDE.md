@~/.agents/AGENTS.md

## Claude Code

When the imported instructions say to use a skill, call the Skill tool for that skill.
Call the Skill tool for "writing" for every response.
Call the Skill tool for "engineering" for software engineering work described above.
Call the Skill tool for "ux" for user-facing product and interface work described above.
For interface implementation, call the Skill tool for both "engineering" and "ux".

## T3 Code delegation

These rules apply in a thread I started on Opus 5.5. If you're a subagent or delegated task, or I started the thread on another model, do the work yourself. Also do trivial work yourself, such as a one-line fix or a quick lookup, instead of delegating it or starting a subagent.

- Taste work, such as writing code, designing architecture and building UI, stays on Opus. Subagents for it run on Opus at high effort.
- Code review is an exception to the do-it-yourself rules above. Outside subagents and delegated tasks, run it as the code-review skill describes, with both Sol and Opus reviewers in its first round.
- Delegate non-trivial debugging, deep dives through unfamiliar code, computer use and visual checks to Codex on GPT-6.1-Sol. Set its reasoning effort to high explicitly, and use the same permissions as the parent thread. It's cheap and I have plenty of usage, so don't skip delegation to save cost.
- Its nitpickiness is the point. Brief it with the goal, relevant context and a done condition. Ask it to report what it actually observed, without fixing anything or delegating further. Ask for the report as plain text in its final message, not an HTML page or a link, so you can read it without opening the child thread. You evaluate the findings and write the fix.
