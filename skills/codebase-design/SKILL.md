---
name: codebase-design
description: Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
---

# Codebase design

Design **deep modules** with a lot of behaviour behind a small interface at a clean seam. Test them through that interface. Use this language and these principles wherever code is designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

## Glossary

Use these terms exactly. Do not substitute "component", "service", "API", or "boundary". Consistent language is the point.

**Module.** Anything with an interface and an implementation. The term works at any scale, including a function, class, package, or tier-spanning slice. _Avoid_ unit, component, and service.

**Interface.** Everything a caller must know to use the module correctly. This includes the type signature, invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_ API and signature because they refer only to the type-level surface.

**Implementation.** The code inside a module. This differs from **Adapter**. A Postgres repository can be a small adapter with a large implementation. An in-memory fake can be a large adapter with a small implementation. Use "adapter" when the seam is the topic and "implementation" otherwise.

**Depth.** Leverage at the interface. It measures how much behaviour a caller or test can exercise for each part of the interface it must learn. A module is **deep** when a large amount of behaviour sits behind a small interface. It is **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_. A place where you can alter behaviour without editing in that place. It is the *location* where a module's interface lives. Seam placement is a separate design decision from what goes behind it. _Avoid_ boundary because DDD already uses it for bounded contexts.

**Adapter.** A concrete thing that satisfies an interface at a seam. The term describes the *role* it fills, not what is inside.

**Leverage.** What callers get from depth. More capability for each part of the interface they learn. One implementation pays back across N call sites and M tests.

**Locality.** What maintainers get from depth. Changes, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. Fix once, fixed everywhere.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can contain small, mockable, swappable parts. Those parts are not part of the interface. A module can have **internal seams** private to its implementation and used by its own tests. It also has an **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

## Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Keep the interface small.** Fewer methods need fewer tests. Fewer parameters make test setup simpler.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Ousterhout's ratio of implementation lines to interface lines.** This rewards padding the implementation. We use depth as leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods.** This is too narrow. Interface here includes every fact a caller must know.
- **"Boundary".** DDD already uses this term for bounded contexts. Say **seam** or **interface**.

## Going deeper

- For **deepening a cluster given its dependencies**, read [DEEPENING.md](DEEPENING.md) for dependency categories, seam discipline, and replacement testing.
- For **exploring alternative interfaces**, read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md). It uses parallel subagents to design several distinct interfaces and compare their depth, locality, and seam placement.
