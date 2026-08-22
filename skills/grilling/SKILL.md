---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map the discussion as a **design tree**. Every decision branches into the decisions that depend on it.

Work the tree in **rounds**. The **frontier** contains every decision whose prerequisites are settled. These are the questions you can ask _now_ without guessing at answers you have not heard yet. Ask the whole frontier in one round. Number each question and give your recommended answer. Then wait for the user's answers before the next round.

Use this format for each round:

```
**Q1. <question title>**

<question body, which may contain several paragraphs or choices>

**Recommended answer**

<your recommended answer>

---

**Q2. <question title>**

<question body, which may contain several paragraphs or choices>

**Recommended answer**

<your recommended answer>
```

Each answered round reshapes the tree. Settled decisions push the frontier outward and unblock dependent questions. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment, such as a file or tool output, dispatch a subagent to find it. Do not ask the user for anything you can look up. Do not block on the result. A running exploration is an unsettled prerequisite, so only its dependent questions must wait. Ask the rest of the frontier now. The _decisions_ belong to the user. Put each decision to them and wait.

The session is done when the frontier is empty, every branch of the design tree has been visited, and no assumption remains unstated. Do not act until the user confirms that you have reached a shared understanding.
