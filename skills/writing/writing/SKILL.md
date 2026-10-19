---
name: writing
description: Draft or edit documents, reports, and other substantial prose, or review prose against my preferences.
---

# Writing

My global instructions hold the baseline writing rules, including the banned wording. They live in this repository's `global/AGENTS.md`, installed as `~/.agents/AGENTS.md`. This skill adds guidance for substantial drafting and editing. Specialist skills govern document structure and domain requirements, and these prose rules still apply to the text they produce. Existing source style alone isn't a reason to keep a pattern in newly written prose.

For user-facing interface copy, use "better-writing" when available. For developer documents and agent instructions, use "technical-writing".

## Write naturally

Vary sentence length naturally. Use "I" when giving a judgement or describing your work, and state an opinion when the evidence supports it. Match the tone to the conversation without adding forced personality. Shortening should remove repetition and filler while preserving reasoning, useful detail, and uncertainty.

## Prose preferences

- State the action, fact, mechanism, or measured effect. Split dense sentences, keep names consistent, and remove redundant qualifiers and adverbs.
- Remove promotional language, vague attribution, and formulaic challenges. Name sources when needed. Preserve useful uncertainty.
- Avoid forced groups of three, synonym cycling, false ranges, fancy substitutes for "is", and "not just X, but Y" framing. Cut trailing phrases that add no evidence.
- Replace abstract metaphors with the concrete concept. Name how something persists instead of saying "durable", and name the actual verification instead of "smoke test". Keep established technical terms when that exact property is the subject.

## Final check

Before completing a written artefact, check it against the global writing rules and these preferences. Rewrite each violation, then check again after the last edit. Keep this check silent.

## Detailed editing

For substantial drafting, an explicit prose edit, or a recurring wording problem, read the relevant sections of [Editing examples](references/editing.md).
