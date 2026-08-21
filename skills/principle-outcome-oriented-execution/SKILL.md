---
name: principle-outcome-oriented-execution
description: "Apply during planned rewrites and migrations with explicit phase checkpoints. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code."
---

# Outcome-oriented execution

Optimise for the intended, verifiable end state rather than preserving smooth intermediate states.

**Why:** Keeping every intermediate step fully stable often creates temporary compatibility code that becomes long-lived debt. Converge on the target architecture and prove correctness at explicit verification checkpoints.

**Core rule:**
- Prioritise end-state integrity over transitional stability
- Intermediate breakage is acceptable when it is planned, scoped, and reversible
- Always run final verification before declaring done

**Guardrails:**
- Use this for planned rewrites and migrations with explicit phase checkpoints
- Declare where temporary breakage is acceptable
- Keep high-signal checks for actively touched areas while migrating
- Require full static and runtime verification at plan completion
