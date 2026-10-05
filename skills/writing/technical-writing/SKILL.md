---
name: technical-writing
description: Write or review developer documentation, commit messages, skills, and agent instructions.
---

# Technical writing

Use "writing" as the prose baseline. This skill owns developer-document structure and technical clarity. Keep the real symbol, path, flag, command, and domain name. Preserve operational wording when a general style rule would weaken a trigger, authority boundary, or completion condition.

## Choose the relevant guidance

- For skills, `AGENTS.md`, `CLAUDE.md`, and linked agent instructions, read [Agent instructions](references/agent-instructions.md). For a skill, also read [Skill mechanics](references/skill-mechanics.md). Skip the developer-prose references for these artefacts.
- For documentation, READMEs, RFCs, ADRs, or runbooks whose structure needs work, read [Document structure](references/document-structure.md).
- For substantial developer prose or a detailed clarity review, read [Developer prose editing](references/developer-prose.md).
- For a short comment, commit message, or release note, use the baseline and the rules below. Load a reference only when the task needs it.
- For a pull request's title or description, use "pull-requests".

Product UI copy belongs to "better-writing" when available. Ordinary chat does not require this skill.

## Keep technical prose precise

State who does what, put conditions before instructions, and use one name for each concept. Keep claims about code and verification tied to inspected evidence. Introduce specialised terms when readers need them, and avoid invented jargon.

For Markdown committed to a repository, put one space inside each table pipe and pad cells and separators so columns align. Indent code snippets with spaces. Verify paths, symbols, and counts; include a regeneration command for structural inventories that need maintaining.

Check the completed text for ambiguous references, unsupported claims, and wording that changes the intended behaviour. Preserve exact user and source requirements.
