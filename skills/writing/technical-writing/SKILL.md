---
name: technical-writing
description: "Technical prose for developers and agents. Use when writing or reviewing documentation, READMEs, RFCs, ADRs, code comments, PR descriptions, commit messages, release notes, changelogs, runbooks, skills, AGENTS.md, CLAUDE.md, or linked agent instructions. Apply with the writing skill. Route by artefact inside. Do not use for product UI copy or ordinary chat."
---

# Technical writing

The goal is writing a tired engineer understands on the first read. Four layers get developer-facing prose there, one question each: what kind of document is this, how do sentences address the reader, how much does each sentence carry, and can any sentence be read two ways. Apply the relevant layers for the artefact below.

## Relationship to writing

Call the Skill tool for "writing" first. It is the baseline for every artefact this skill covers. This skill owns technical-document structure, developer terminology, instructions, and sentence clarity. When a rule here differs from the writing skill, follow this skill for the technical artefact.

The codebase is the word list. Write the real symbol, file, flag, or command name, not a synonym or a description of it.

Don't invent jargon. Use the words a developer would say out loud: "move", "delete", "a budget that only decreases", not "evacuate", "ratchet", or "endgame". A named pattern is fine when the doc says what it means the first time. Add new offenders and their replacements to the abstract-metaphor rule in the writing skill.

## Choose the artefact

Apply the shared sentence, terminology, and clarity rules in this file to every artefact in scope unless the relevant branch below takes scoped authority.

- For documentation, READMEs, RFCs, ADRs, and runbooks, also apply **Pick the mode first (Diátaxis)**.
- For code comments, PR descriptions, commit messages, release notes, and changelogs, skip Diátaxis.
- For skills, `AGENTS.md`, `CLAUDE.md`, and documents reached through agent context pointers, read [Agent instructions](references/agent-instructions.md) instead of applying Diátaxis. When the artefact is a skill, also read [Skill mechanics](references/skill-mechanics.md).

For agent artefacts, **Agent instructions** is the scoped authority. Preserve operational wording and leading words when a general prose rule would weaken a trigger, completion criterion, or other deliberate steering.

## Pick the mode first (Diátaxis)

One document, one mode. Two questions pick it: does the content inform action (doing) or understanding (thinking), and does it serve learning or work?

- Action + learning: **tutorial**.
- Action + work: **how-to**.
- Understanding + work: **reference**.
- Understanding + learning: **explanation**.

Use the compass on a whole document or on one sentence. Reach for it whenever you feel unsure what you are writing. Gut feel is often wrong here.

**Tutorial. Learning by doing.** You are the teacher. The learner's success is your job, not theirs. Open by saying what the learner will build, not what they will "learn". Every step produces a visible result, early and often. Tell them what they should see: the expected output, the prompt change, the log line. Cut explanation to one clause and a link. Teaching pauses break the lesson. Stay concrete. Write as "we", in commands: "First, do x. Now, do y."

**How-to. Steps to a goal.** Solve a problem a person has, not an operation the machine can perform. Assume competence. Skip teaching. Action only: no digressions, no background, no completeness for its own sake. Link those instead. Allow forks and judgement: "If you want x, do y." Name the guide by the task: "How to calibrate the radar array", not "Radar array calibration".

**Reference. Facts for lookup.** Describe. Only describe. No instruction, no persuasion, no opinion. Be dry, complete, and sure: state facts, options, limits, and errors with no hedging. Mirror the structure of the thing described, so code and docs can be navigated together. Put material where readers expect it. Generate from code where possible, so it stays true.

**Explanation. Understanding and why.** One bounded topic, readable away from the product. Each title should tolerate an implicit "About..." in front. Anchor on a real why question. Give context: design decisions, history, constraints, alternatives. Opinion is allowed here and nowhere else.

Don't mix modes: no reference tables inside a tutorial, no tutorial hand-holding inside reference, no arguing inside a how-to. Split and link instead.

Source: diataxis.fr, fetched 2026-07-18.

## Write sentences to the reader (Google developer style)

- Talk to the reader as "you", in the present tense. "Will" only for things that genuinely happen later.
- Say who does what: "the compiler checks", not "is checked". Passive is fine only when the actor is unknown or beside the point.
- Write instructions as commands: "Click Submit." State facts plainly. Never "should be done".
- Put the condition before the instruction: "To delete the document, click Delete." The reader skips what does not apply.
- Put the common case first. Exceptions after.
- Sound like a knowledgeable friend. No buzzwords, no figurative language, no "please" in instructions, and never "simply", "easy", or "quickly" in a procedure. If it were simple, the reader would not be here.
- Don't pre-announce ("we will soon support...") and don't start consecutive sentences with the same phrase.
- Read the awkward sentence aloud. If it stays awkward, rewrite it.
- Link with words that say where the link goes: the page title or a short description. Never "click here". Prefer a sentence of context on the page over a link off it.
- Headings carry the point, not just the topic ("Pick the mode first", not "Modes"). Sentence case. A task heading is a bare verb phrase ("Create an instance"). A concept heading is a noun phrase. One h1 per page, no skipped levels.
- Numbered lists for sequences, bullets for everything else. Introduce a list with a complete sentence. Keep items parallel.
- Code goes in code font. UI elements go in bold. Use serial commas. Drop "etc." and say up front that a list is partial.

Source: developers.google.com/style, fetched 2026-07-18.

## Make statements load one at a time (STE rules)

- One instruction per sentence. One thought per sentence everywhere else.
- Split instructions longer than about 20 words and other sentences longer than about 25.
- Put the warning or condition before the step it guards: "If hot oil touches your skin, injuries can occur."
- Keep "the" and "a": "Remove backup file" reads two ways. "Remove the backup file" reads one.
- Give each word one meaning and one job, then keep it. If "check" means inspect, don't also use it for restrain.
- Pick one word per action and stick to it: "start", not "start" here and "initiate" there.
- Write procedures as direct commands, never as narration and never in the passive: "Install the component", not "the component must be installed".
- Avoid "-ing" words where you can. They take too many grammatical jobs and breed misreadings.

Source: asd-ste100.org (Issue 9, 2025), fetched 2026-07-18. The numbered rules and dictionary live in the spec PDF. The principles above are the transferable core.

## Leave no sentence open to two readings (Global English)

- Keep words like "only" and "not" next to the word they change: "only fails on growth" and "fails only on growth" say different things.
- Break up long noun strings: "the proto import budget check script" becomes "the script that checks the proto-import budget".
- Make every "it", "they", and "this" point at one obvious thing. Repeat the noun when in doubt. Never use "this" or "which" to point at a whole clause.
- Don't drop verbs: "Phase 1 moves the converters and Phase 2 the runtime" leaves Phase 2 without one. Give it one.
- Keep the small words that show structure. "Ensure that the switch is off" keeps "that" because it makes the sentence parse one way. Never trade clarity for word count.
- Repeat the article in a series when it prevents a misread: "the client and the host", not "the client and host", when they are two things.
- Say which parts "and" or "or" joins when a sentence can group two ways. "Both...and", "either...or", and "if...then" are free disambiguators.
- Use full stops, not semicolons. Replace an em dash with a new sentence.
- Make text in parentheses a full grammatical unit or its own sentence. Never form plurals with "(s)".
- No slashes: write "a, b, or both" instead of "a/b" or "and/or".
- Call each thing by one name, everywhere. A doc that says "the gate", "the ratchet", and "the budget check" for one thing teaches three things. Rewording an unchanged sentence between edits costs the same way: don't churn what didn't change.
- Skip idioms, colloquialisms, Latin abbreviations, and metaphors. A non-native reader, a translator, and an agent all parse plain constructions best.

Source: Kohl, The Global English Style Guide (SAS Press). Guideline text fetched from the Internet Archive and the SAS sample chapter, 2026-07-18.

## Voice and repo specifics

- The writing skill owns the catalogue of slop patterns: AI vocabulary, filler, hedging, and formatting tells.
- PR descriptions and commit messages are writing too. Every layer except Diátaxis applies to them.
- Product UI strings are not documentation. Use your product's copy guidelines for those.
- For Markdown files committed to the repository, put one space inside each table pipe. Pad every cell and separator so the column boundaries align in plain text.
- Indent code snippets with spaces. Write real paths and real symbols. Make every count or tree claim true at the commit that lands it, and include the command that regenerates it.

## Worked example

Before:

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it's important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

After:

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.

The fixes, by layer: "configuration is performed" becomes "`budget.mjs` reads", so someone does something (Google). "Ratchet" goes away. The script's real filename does the naming (jargon rule). The five-noun string breaks up into plain clauses (Global English). The writing skill deletes the hedge "note that it's important to remember". The failure condition moves ahead of the step it explains (STE). The buried "should only be done when lowering" becomes a command with "only" next to its verb (STE). "If exceeded" gets a subject: the count (Global English).

## Review checklist

Apply to any prose this skill covers. Item 1 applies only to developer document sets:

1. Is each file one Diátaxis mode, with links where modes meet?
2. Is every instruction written as a command, with its condition in front?
3. Does any sentence carry two instructions or two thoughts? Split it.
4. Is "only" next to the word it changes? Does every "it" point at one thing? Does every clause keep its verb?
5. Does each thing have exactly one name across the docs?
6. Would a developer say these words out loud? Replace invented metaphors and fancy synonyms with the plain word or the real symbol name.
7. Are all symbols, paths, and counts real at this commit, with the commands that regenerate the counts?
