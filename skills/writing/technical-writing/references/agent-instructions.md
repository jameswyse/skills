# Agent instructions

This reference covers any document an agent consumes, including a skill, an `AGENTS.md` or `CLAUDE.md` file, and a document reached by a pointer. Packaging differs, but the writing does not. Describe the required outcome, authority, and completion evidence. Prescribe a fixed process only when the sequence prevents a concrete failure.

When the document you're writing is a skill, read [`skill-mechanics.md`](skill-mechanics.md) for frontmatter, invocation choice, and router skills.

## Context pointers

A **context pointer** is a reference held in the agent's context that names some out-of-context material and encodes the condition for reaching it. A skill's description is one. A line in `AGENTS.md` that names a document is another. The pointer must make the relevant task recognisable before the target is read. Check ambiguous triggers against realistic requests before adding more instructions.

A pointer does two jobs. It states what the material is and lists the **branches** that should trigger reaching it. A branch is a distinct case the document handles, so different runs take different paths through it. Every word of an always-loaded pointer costs on every turn, so it earns even harder pruning than the body:

- **Front-load the task.** State the action and condition before implementation detail.
- **One trigger per branch.** Synonyms that rename a single branch are one branch written twice. Collapse them and keep only genuinely distinct branches.
- **Cut identity the body already carries.**

## The two loads

Every document and pointer you add spends one of two budgets:

- **Context load.** This is the cost of material that remains in the agent's window, such as an `AGENTS.md` line or skill description. It spends tokens and attention every turn whether or not it fires.
- **Cognitive load.** This is the cost to the human of remembering which documents exist and when to use them. The human is the index. This cost buys human agency. Spend it where human judgement matters and remove it where it does not.

Material reached only through a pointer avoids context load apart from the pointer's own line. Material with no pointer relies entirely on cognitive load.

## Information hierarchy

A document contains two types of content. **Steps** are the ordered actions the agent performs. **Reference** contains definitions, rules, and facts consulted on demand. A document may contain only steps, only reference, or both. The core decision is where each piece sits on the **information hierarchy**, ranked by how soon the agent needs it:

1. **In-file step** is the primary tier: what the agent does, in order.
2. **In-file reference** is consulted on demand. A review's rules can form a valid flat peer set where every rule sits at the same level.
3. **Disclosed reference** sits in a separate file and loads only when its context pointer fires. It may be a sibling file or an external reference that any document can point to.

Push too little down and the top becomes too long. Push too much and you hide material the agent needs. That tension drives the decision.

**Progressive disclosure** moves material to a lower level by placing it outside the main file and behind a pointer. This keeps the top legible and protects the hierarchy. Branching is the cleanest disclosure test. Inline what every branch needs, and put behind a pointer what only some branches reach. In a document with steps, reference material that should be disclosed can bury the steps and make attention unreliable.

**Co-location** is the within-file companion. The hierarchy decides _how far down_ a piece sits. Co-location decides _what sits beside it_ once there. Keep a concept's definition, rules, and caveats under one heading so reading one part brings its neighbours with it. The document should read like documentation written for the agent. Grouped material reads that way, while scattered material does not. This differs from duplication. Duplication repeats one meaning in two places, while scattering fragments one meaning across many.

**Sprawl** means a document is too long even when every line is current and unique. Excess length weakens attention and adds more text to maintain. Use the information hierarchy to put reference behind pointers and split by branch or sequence. Each path should carry only what it needs.

## Completion criteria

Define observable completion for the requested outcome. Distinguish a verified result, a provisional conclusion, and work blocked by missing access or a consequential decision. Keep criteria proportional to the task. Require exhaustive coverage only when the user's request or the risk warrants it.

Carry existing authorisation through later phases. A review-only request ends with findings. A request that includes implementation continues through the authorised changes and verification. Ask only for missing decisions or actions outside that authority, and continue independent work while waiting.

## When to split

Split by a real branch, such as diagnosis versus an authorised fix, or sequential versus delegated review. Keep shared constraints in the entrypoint and branch-specific mechanics in the reference. Give each link a clear trigger. A short, self-contained workflow may need no split.

For invocation choices, see [Skill mechanics](skill-mechanics.md).

## Prompting hypotheses

Claims that leading words improve retrieval, negation encourages forbidden behaviour, or hiding later phases improves persistence depend on the model and task. Treat them as hypotheses, not universal requirements.

Use familiar terminology when it conveys the intended meaning, and prefer a direct positive instruction when it is clearer. Preserve explicit prohibitions, personal preferences, and authority boundaries. Do not replace a precise condition with a metaphor merely to shorten it.

Evaluate changes against realistic tasks with the model, tools, fixtures, and other instructions held fixed. Inspect actual tool traces and outcomes, including unnecessary pauses, unsupported claims, correctness, and cost. A shorter prompt or one successful run does not establish better behaviour.

## Pruning

- Keep each meaning in a **single source of truth**, one authoritative place where changing the behaviour takes one edit. **Duplication** repeats the same meaning in several places. It costs maintenance and tokens, and gives the meaning more prominence than its real rank. Repeat a short term only when it helps identify the same concept.
- Treat the **environment** as a source of truth too. Examples include `package.json` scripts, configuration files, the directory layout, and `--help` output. A document that restates this information is a **cache** and earns its load only when the lookup is expensive. Cache what the agent cannot find by looking, such as an unwritten convention, the reason behind a choice, or a hidden problem. Leave one-file and one-command lookups to the environment, where they cannot go stale.
- Check every line for **relevance**. Does it still affect what the document does? A line loses relevance when it does not affect the task or when the behaviour it describes changes. Move a conditional branch behind a pointer when only some paths need it. Shorter documents are easier to keep relevant. Without pruning, stale instructions accumulate because adding feels safe and removing feels risky.
- Hunt **no-ops** sentence by sentence. An instruction the model already obeys by default spends context without changing behaviour. The test asks whether the instruction changes behaviour from the default. This is model-relative, not reader-relative, so settle disagreements by running the document. Delete a sentence that fails the test instead of trimming it. Apply the same test to leading words. Replace a generic virtue such as _be thorough_ with the observable work or completion criterion it stands for.
