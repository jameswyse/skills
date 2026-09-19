# Deep modules

Use this reference when assessing module depth, compressing an interface, placing a seam, choosing adapters, or deciding where tests should observe behaviour. Deepening is a design option, not the default.

## Use the vocabulary precisely

Use these terms when they name the concepts below. Preserve established framework, protocol, and domain terms when those names are exact. A React component remains a component, and an HTTP API remains an API.

**Module.** Anything with an interface and an implementation. The term works at any scale, including a function, class, package, or tier-spanning slice.

**Interface.** Everything a caller must know to use the module correctly. This includes the type signature, invariants, ordering constraints, error modes, required configuration, and performance characteristics. The TypeScript `interface` keyword or a list of public methods names only part of it.

**Implementation.** The code inside a module. This differs from an adapter. Use "adapter" when the seam and the role of a concrete implementation are the subject. Use "implementation" for what is inside the module.

**Depth.** Leverage at the interface. It measures how much useful behaviour a caller or test can exercise for each part of the interface it must learn. A module is **deep** when substantial behaviour sits behind a small interface. It is **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_. A place where behaviour can vary without editing the code at that place. It is where a module's interface lives. Seam placement is a separate decision from what belongs behind it. Use "bounded context" for the DDD concept rather than using "boundary" for both.

**Adapter.** A concrete thing that satisfies an interface at a seam. The term describes the role it fills, not the amount of code inside it.

**Port.** An interface at a remote or external seam. Production and test adapters can satisfy the same port.

**Leverage.** What callers get from depth. One implementation provides more capability for each part of the interface callers learn.

**Locality.** What maintainers get from depth. Changes, bugs, knowledge, and verification concentrate in one module rather than spreading across callers.

## Decide whether the module should be deeper

Apply the **deletion test** before proposing a deepening. Imagine deleting the module:

- If its complexity disappears, the module was probably a pass-through.
- If its decisions and coordination reappear across callers, the module was earning its place.

Look for evidence that a deeper module would remove total complexity:

- Callers repeat the same decisions, ordering, validation, or recovery.
- Understanding one concept requires tracing many shallow modules.
- The interface exposes nearly every implementation choice.
- Bugs arise in coordination between callers and helpers.
- Tests must reproduce caller coordination or reach through the interface.
- The same area changes often and knowledge remains scattered.

Do not deepen a cluster merely because it is in-process, has a test replacement, contains several files, or could support a new abstraction. Prefer clear local code when the current shape is easy to understand and change.

## Design the interface

Aim for a small interface that hides substantial decisions. Reduce the number of methods, parameters, states, ordering rules, and implementation facts that callers must learn. Move repeated coordination behind the interface without hiding complexity that callers still need to control.

A deep module can contain internal seams used by its implementation and tests. Keep those seams private. Expose only the external seam that callers need.

The interface includes every fact callers depend on. A short type signature can still describe a shallow module when callers must also learn hidden ordering, configuration, failure, or lifecycle rules.

## Classify dependencies after the candidate earns deepening

The dependency category determines how to implement and test a chosen deepening. It does not justify the deepening by itself.

### In-process

Pure computation and in-memory state need no adapter. Merge the cluster when the deletion test and caller evidence support it. Test directly through the new interface.

### Local-substitutable

Use a local replacement such as PGLite or an in-memory filesystem inside the module's tests. Keep the replacement seam internal unless callers genuinely need to choose the dependency. The existence of a replacement does not justify an external port.

### Remote and owned

For a service you control across a network seam, define a port when the transport genuinely varies or must be replaced in tests. Keep domain behaviour in the deep module. Use an HTTP, gRPC, or queue adapter in production and an in-memory adapter in tests.

### External and unowned

For a third-party service, inject a port at the existing external seam. Keep vendor representations inside the production adapter. Use a focused fake or mock adapter in tests.

## Judge whether a seam is real

Justify a seam through required variation or an external system that changes independently. Adapter count alone does not establish that need.

- Two necessary implementations are evidence that the seam is real.
- An existing network, storage, or third-party seam is real because the external system varies independently.
- A fake created only to make a new port look justified is not a second requirement.
- A single production adapter behind an interface that no caller needs to vary is usually indirection.

## Reuse adapters before adding another seam

Inspect existing adapters and services before creating one. Prefer these choices in order:

1. Reuse a cohesive adapter through the narrow type that the consumer needs.
2. Extend the adapter when the new operation belongs to the same capability and changes for the same reason.
3. Create another adapter when reuse would mix unrelated capabilities, expose provider details, or add caller coordination.

At a real external seam, define the port in the consumer's language. Keep its inputs, outputs, and failures in application or domain terms. A wider concrete adapter can satisfy a narrow consumer-owned type. Do not split one cohesive adapter into one-method wrappers.

## Test through the interface

The **interface is the test surface**. Protect observable outcomes through the same seam callers use. Tests should survive an internal refactor that preserves behaviour.

When deepening replaces shallow modules:

1. Write tests for the preserved behaviour through the new interface.
2. Confirm that the replacement tests cover the old observable cases.
3. Delete old tests that assert superseded helpers, coordination, or internal state.
4. Retain an internal test only when it protects an independently useful algorithm or diagnostic that the interface tests cannot identify clearly.

If ordinary behaviour can be tested only by reaching past the interface, reconsider the module shape or what the interface exposes.

## Reject misleading measures

- Do not measure depth by implementation lines divided by interface lines. That rewards padding the implementation. Measure the behaviour and decisions hidden for callers.
- Do not equate depth with size. A small function can be deep, and a large package can be shallow.
- Do not add a seam for hypothetical replacement. Variation must already exist or follow from a required external system.
