---
name: redesign-from-first-principles
description: "Redesign an existing system around a new requirement as a foundational assumption, then carry that design through every affected part."
---

# Redesign from first principles

Treat the new requirement as if it had existed when the system was first designed.

1. Read the affected implementation, types, tests, documentation and examples until the current design and its constraints are clear.
2. Describe the design you would choose if the new requirement were foundational. Keep existing constraints that still matter, rather than preserving structure only because it already exists.
3. Compare the target design with the current one and identify the smallest coherent migration.
4. Carry the requirement through every affected reference, including types, tests, documentation, examples and rationale where present.
5. Verify that the finished design expresses the requirement directly rather than through caller coordination or a special-case layer.

Match the deliverable to the user's request. Produce the design for an analysis or review request. Implement it only when the user asked for a change.
