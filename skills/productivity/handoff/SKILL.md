---
name: handoff
description: "Compact the current conversation into a copy-ready handoff for another agent. Use when the user asks to transfer work to a new session or agent. Return the handoff in chat unless the user explicitly requests a file."
---

# Handoff

Give a fresh agent enough context to continue the work without replaying the conversation.

## Assemble the handoff

- Start with the current objective and the completion criteria.
- Record the current state, including completed work, verification evidence, work in progress, and work that remains.
- Preserve settled decisions, user-approved wording, constraints, authority boundaries, and consequential assumptions.
- Record accepted corrections and the current objective they produced. Mark superseded decisions or evidence so the next agent does not revive them.
- For pending questions and running tools or delegated tasks, include the question or job ID, owner, dependencies, known status, and supported way to collect or cancel the work. Distinguish a requested cancellation from a confirmed one. State when a fresh session cannot access the job; do not imply that transferring the handoff transfers execution.
- Name the working directory, branch, dirty working-tree state, relevant files and symbols, and useful commands when known.
- Reference existing plans, specifications, ADRs, issues, commits, diffs, and other artefacts by path or URL. Summarise only the context needed to use them.
- Put remaining steps in dependency order. Include blockers, risks, open questions, and failed approaches that the next agent must not repeat.
- Suggest available skills only when they would help the next agent. State why each one applies.
- Distinguish verified facts from assumptions and proposals. Mark information that may be stale.
- Remove secrets, credentials, tokens, and sensitive personal information. Replace a necessary redaction with a descriptive placeholder.

If the user names the next session's focus, shape the handoff around that focus. Do not expand the task beyond the user's authority.

## Return a copy-ready block by default

Wrap the complete handoff in a four-backtick Markdown code block labelled `md`. Put no prose outside the block. This fence lets the handoff contain ordinary three-backtick code blocks.

Use these headings when they contain useful information:

- `# Handoff`
- `## Objective`
- `## Current state`
- `## Decisions and constraints`
- `## Completed and verified`
- `## Remaining work`
- `## Working context`
- `## Suggested skills`
- `## Risks and unknowns`

Do not create or edit a file in the default mode.

## Write a file only when requested

When the user explicitly asks for a handoff document or file, write Markdown to the requested path. If the user does not give a path, write `handoff-<timestamp>.md` in the operating system's temporary directory. Reply with the absolute path and a concise summary. Include the full handoff in chat only when the user also requests it.
