# Review smells

Smells are evidence to investigate, not automatic refactoring instructions. Confirm the concrete
maintenance or correctness cost in the diff, then report the smallest coherent response. Every
baseline finding is a labelled judgement call:

- **Mysterious Name.** A name hides what it does or holds. Rename it. If no honest name exists,
  clarify the design.
- **Duplicated Code.** The same logic shape recurs. Share one owner when the copies express the same
  stable rule and must change together. Keep repetition when an abstraction would encode guesses.
- **Feature Envy.** A method reaches into another object's data more than its own. Move the behaviour
  only when the other module owns the knowledge it needs.
- **Data Clumps.** The same fields or parameters travel together. Introduce one type when they form
  a domain concept or share an invariant.
- **Primitive Obsession.** Interchangeable primitives represent distinct domain concepts. Add a
  semantic type when it prevents invalid mixing or centralises validation.
- **Repeated Switches.** The same decision over one domain type recurs. Put the rule in one owner,
  such as a domain model, map, registry, or polymorphic implementation.
- **Ternaryception.** A ternary is nested inside a ternary that is already nested. One level of
  nesting is fine. Beyond that, replace the expression with named branches, a lookup, or a switch.
- **Shotgun Surgery.** One logical change requires scattered edits. Gather what changes together.
- **Divergent Change.** One module changes for unrelated bodies of knowledge. Split it only when the
  result has stronger cohesion and less total reader load.
- **Speculative Generality.** Unused abstraction, parameters, or hooks anticipate unasked needs.
  Delete or inline them.
- **Message Chains.** Callers must understand a long `a.b().c().d()` chain. Move the required
  knowledge to its owner or expose a direct operation when that reduces coupling.
- **Middle Man.** A module mainly delegates. Apply the deletion test. Remove it when its complexity
  disappears, but keep an interface that hides real decisions or coordination.
- **Refused Bequest.** A subtype ignores inherited behaviour or violates the base type's
  expectations. Prefer composition when inheritance does not describe a valid substitution.
- **Unnecessary Complexity.** The change adds concepts, state, branches, layers, dependencies, or
  execution paths that its behaviour and constraints do not require. Name the concrete maintenance
  or correctness cost and the smallest coherent alternative. Do not flag essential domain complexity
  or mere line count.

