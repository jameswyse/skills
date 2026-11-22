---
name: writing
description: Use when drafting, editing, or reviewing prose other people will read, such as documents, reports, READMEs, ADRs, runbooks, emails, messages, commit messages, release notes, and comments on pull requests, issues or tickets, or when writing or reviewing a skill or agent instructions such as AGENTS.md. For a pull request's title or description, use open-pr.
---

# Writing

Skills that own a document type, such as open-pr, govern its structure and domain requirements, and these prose rules still apply to the text they produce. For user-facing interface copy, use "better-writing" when available. Existing source style alone isn't a reason to keep a pattern in newly written prose.

## Write naturally

Vary sentence length naturally. Use "I" when giving a judgement or describing your work, and state an opinion when the evidence supports it. Match the tone to the conversation without adding forced personality. Shortening should remove repetition and filler while preserving reasoning, useful detail, and uncertainty.

## Prose preferences

- State the action, fact, mechanism, or measured effect. Split dense sentences, keep names consistent, and remove redundant qualifiers and adverbs.
- Remove promotional language, vague attribution, and formulaic challenges. Name sources when needed. Preserve useful uncertainty.
- Avoid forced groups of three, synonym cycling, false ranges, fancy substitutes for "is", and "not just X, but Y" framing. Cut trailing phrases that add no evidence.
- Replace abstract metaphors with the concrete concept. Name how something persists instead of saying "durable", and name the actual verification instead of "smoke test". Keep established technical terms when that exact property is the subject.

## Technical writing

Keep the real symbol, path, flag, command, and domain name. Preserve operational wording when a general style rule would weaken a trigger, authority boundary, or completion condition. State who does what, put conditions before instructions, and use one name for each concept. Keep claims about code and verification tied to inspected evidence. Introduce specialised terms when readers need them, and avoid invented jargon.

For Markdown committed to a repository, put one space inside each table pipe and pad cells and separators so columns align. Indent code snippets with spaces. Verify paths, symbols, and counts; include a regeneration command for structural inventories that need maintaining.

## Choose the relevant guidance

Read each reference whose condition applies before drafting. A short comment, commit message, or release note needs none.

- For substantial drafting, an explicit prose edit, or a recurring wording problem, read the relevant sections of [Editing examples](references/editing.md).
- For skills, `AGENTS.md`, `CLAUDE.md`, and linked agent instructions, read [Agent instructions](references/agent-instructions.md). When creating a skill, changing its description, invocation, or the skills a router names, or splitting or merging skills, also read [Skill mechanics](references/skill-mechanics.md). Skip Document structure and Developer prose editing for these artefacts.
- For documentation, READMEs, RFCs, ADRs, or runbooks whose structure needs work, read [Document structure](references/document-structure.md).
- For substantial developer prose or a detailed clarity review, read [Developer prose editing](references/developer-prose.md).

## Final check

Before completing a written artefact, check it against the global writing rules and these preferences. For technical text, also check for ambiguous references, unsupported claims, and wording that changes the intended behaviour, and preserve exact user and source requirements. Rewrite each violation, then check again after the last edit. Keep this check silent.
