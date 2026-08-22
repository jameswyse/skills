# Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [SKILL.md](SKILL.md): **module**, **interface**, **seam**, **adapter**.

## Dependency categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation and in-memory state with no I/O. Always deepen this cluster. Merge the modules and test directly through the new interface. No adapter is needed.

### 2. Local-substitutable

These dependencies have local test replacements, such as PGLite for Postgres or an in-memory filesystem. Deepen the cluster when the replacement exists. Test the deepened module with the replacement running in the test suite. Keep this seam internal. Do not add a port to the module's external interface.

### 3. Remote but owned through ports and adapters

These are your own services across a network seam, such as microservices or internal APIs. Define a **port**, which is an interface, at the seam. The deep module owns the logic. Inject the transport as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP, gRPC, or queue adapter.

Use this recommendation shape: *"Define a port at the seam. Implement an HTTP adapter for production and an in-memory adapter for testing. Keep the logic in one deep module even though it is deployed across a network."*

### 4. External and unowned

These are third-party services you do not control, such as Stripe or Twilio. The deepened module takes the external dependency as an injected port. Tests provide a mock adapter.

## Seam discipline

- **One adapter means a hypothetical seam. Two adapters means a real one.** Do not introduce a port unless at least two adapters are justified, usually for production and tests. A single-adapter seam is just indirection.
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface just because tests use them.

## Replace tests instead of layering them

- Old unit tests on shallow modules become waste once tests at the deepened module's interface exist. Delete them.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state.
- Tests should survive internal refactors, since they describe behaviour, not implementation. If a test has to change when the implementation changes, it's testing past the interface.
