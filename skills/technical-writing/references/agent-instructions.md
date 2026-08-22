# Agent instructions

This reference covers any document an agent consumes, including a skill, an `AGENTS.md` or `CLAUDE.md` file, and a document reached by a pointer. Packaging differs, but the writing does not. The same instructions make the agent follow the same _process_ each run without forcing the same output.

When the document you're writing is a skill, read [`skill-mechanics.md`](skill-mechanics.md) for frontmatter, invocation choice, and router skills.

## Context pointers

A **context pointer** is a reference held in the agent's context that names some out-of-context material and encodes the condition for reaching it. A skill's description is one. A line in `AGENTS.md` that names a document is another. The pointer's _wording_, not its target, decides when the agent reaches the material and how reliably. A must-have target behind a weakly worded pointer is a variance bug. Sharpen the wording first, and inline the material only if sharpening fails.

A pointer does two jobs. It states what the material is and lists the **branches** that should trigger reaching it. A branch is a distinct case the document handles, so different runs take different paths through it. Every word of an always-loaded pointer costs on every turn, so it earns even harder pruning than the body:

- **Front-load the leading word.** The pointer is where it does its triggering work.
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

## Steps and completion criteria

Every step ends on a **completion criterion**, the condition that tells the agent the work is done. Two properties make it a lever:

- **Clarity.** Can the agent tell done from not done? A vague bound such as "understanding reached" invites **premature completion**, where the step ends before it is genuinely done. The visible **post-completion steps** create pressure to move on. Defend against that pressure by sharpening the bound first. If the bound remains irreducibly fuzzy and you observe the rush, split the sequence to hide later steps. Hiding works only across a separate context, such as a hand-off or subagent dispatch. An inline call leaves the later steps in context.
- **Demand.** This is how much the criterion requires. "Every modified model accounted for" forces more thorough work than "produce a change list". Demand drives **legwork**, the investigation performed within the work. Demand is not limited to steps. "Every rule applied" can bind flat reference just as "every step done" binds a sequence, so an all-reference document can still require exhaustive work.

The strongest criteria are both checkable and exhaustive.

## When to split

Splitting one document into two spends one of the two loads, so split only when the cut earns it:

- **By sequence.** Split a run of steps where the post-completion steps tempt the agent to rush the current one. Keeping them out of view drives more legwork on the current task. The reverse also applies. Merging sequences exposes later steps and can invite premature completion.
- **By invocation**, skill-specific: see [`skill-mechanics.md`](skill-mechanics.md).

## Leading words

A **leading word** is a compact concept already present in the model's pretraining that the agent thinks with while running the document. Examples include _lesson_, _fog of war_, and _tracer bullets_. Repeating the token, not its definition, anchors a region of behaviour in few tokens by using knowledge the model already holds. A new term can work when clearly defined, but it brings no prior knowledge. Prefer an existing term.

It anchors twice. In the body, it anchors _execution_. The agent reaches for the same behaviour every time the word appears. In a pointer, it anchors _invocation_. When the same word appears in prompts, documentation, and the codebase, the agent links that language to the material and reaches it more reliably.

Hunt for opportunities to refactor with leading words. A triad spelled out at three sites, a pointer spending a sentence to gesture at one idea. Each is a passage begging to collapse into a single token:

- "fast, deterministic, low-overhead" → _tight_, as in "a tight loop".
- "a loop you believe in" → _red_. This turns a fuzzy gate into a binary observable state. The loop goes _red_ on the bug, or it does not.

You win twice: fewer tokens, and a sharper hook for the agent to hang its thinking on. Assume every document is carrying restatements that leading words retire. Go find them.

**Negation** is the failure mode beside this lever. Steering by prohibition puts the forbidden behaviour in context and can make it more available. In "Don't think of an elephant", the negation is weaker than the activated concept, so the ban can partly read as an instruction. Prompt the **positive**. State the target behaviour, such as "write one-line comments", so the banned one is never spoken. Keep a prohibition only when a hard guardrail cannot be phrased positively. Pair it with the positive target so attention lands on what to do.

## Pruning

- Keep each meaning in a **single source of truth**, one authoritative place where changing the behaviour takes one edit. **Duplication** repeats the same meaning in several places. It costs maintenance and tokens, and gives the meaning more prominence than its real rank. A leading word does the inverse by repeating a token on purpose without repeating its definition.
- Treat the **environment** as a source of truth too. Examples include `package.json` scripts, configuration files, the directory layout, and `--help` output. A document that restates this information is a **cache** and earns its load only when the lookup is expensive. Cache what the agent cannot find by looking, such as an unwritten convention, the reason behind a choice, or a hidden problem. Leave one-file and one-command lookups to the environment, where they cannot go stale.
- Check every line for **relevance**. Does it still affect what the document does? A line loses relevance when it does not affect the task or when the behaviour it describes changes. Move a conditional branch behind a pointer when only some paths need it. Shorter documents are easier to keep relevant. Without pruning, stale instructions accumulate because adding feels safe and removing feels risky.
- Hunt **no-ops** sentence by sentence. An instruction the model already obeys by default spends context without changing behaviour. The test asks whether the instruction changes behaviour from the default. This is model-relative, not reader-relative, so settle disagreements by running the document. Delete a sentence that fails the test instead of trimming it. Apply the same test to leading words. Replace a weak term such as _be thorough_ with a stronger one such as _relentless_ when the stronger term changes behaviour.
