# Missed findings

Patterns that bot reviewers caught after this review passed a change, most frequent first. Check
each one against the scope. [Calibration](calibration.md) maintains this list.

- **Context scoping.** Trace tenant, site, account, and role restrictions through every query, cache
  key, and destructive operation. Check that configured roles apply everywhere they affect access or
  classification.
- **Claims the code doesn't keep.** A pull request description, docstring, error message, or name
  promises behaviour, such as once-only execution, immutable URLs, retries, preserved exclusions, or
  parity with the code it replaces, that only some paths implement.
- **References across edits and races.** Trace references through rename, delete, restore, and
  concurrent writes. Handle a record that disappears between the initial read and the write that
  depends on it.
- **Partial writes and external side effects.** Walk each failure point across database
  transactions and external storage. Look for partial commits, irreversible overwrites, orphaned
  objects, and lost cleanup before trusting an all-or-nothing or deletion claim.
- **Canonical values.** Validation, comparison, storage keys, and output must use the same
  normalised value, such as trimmed text, lower-cased UUIDs, decoded paths, or normalised domains.
  Padded input such as `" J "` must not pass a minimum-length check.
- **Static analysis by meaning.** Resolve bindings, aliases, callback ownership, and transparent
  wrappers before matching. Text matches, familiar identifier names, and blanket exemptions suppress
  real violations or flag unrelated code.
- **Absence and shape.** Treat sparse arrays, omitted fields, nulls, and empty collections as
  distinct. A transformation must keep metadata and must not turn "absent" or "matches nobody" into
  a value with a different meaning.
- **The consuming parser's rules.** Validate against how the browser, HTML parser, URL normaliser,
  or query language will interpret the value, not against suspicious source strings.
- **Lifecycle transitions.** Exercise repeated attempts, failed optimistic saves, external updates,
  reconnects, and calendar rollover. Counters keep their intended expiry, and date calculations use
  one timezone.
- **Parallel producers and consumers.** A changed format, tool, or dependency must agree with every
  other producer and reader, including Dockerfiles, CI workflows, scripts, fixtures, alternate entry
  points, editor settings, and consumers of the previous release.
- **Whole inputs and batches.** Check both bounds, every occurrence, allowed enum or status values,
  and collisions between records that are each valid alone. A dry run must enforce the constraints
  the real write does.
- **Retained content in migrations.** Keep supported legacy field names, validate references before a
  transformation erases them, and skip resolving data the migration discards.
- **Cache validity.** Check out-of-order completion, old response shapes, real cache bypasses, and
  validators for changed metadata. Identical bytes don't mean an unchanged filename.
- **The assembled application.** Check behaviour through the real middleware and environment,
  including preflight requests, conditional responses, and inherited settings that isolated handlers
  and fixtures omit.
- **Failure outcomes through every layer.** Follow an error through catches, callbacks, shell
  commands, and background work to the final response, log, and cleanup. A failure must not become
  success or remove an existing fallback.
- **Explicit pipeline order.** Enrich before filtering, exclude before counting, and sort explicitly
  wherever later steps depend on order. Database and filesystem enumeration order guarantees nothing.
- **Declared ranges the graph can't meet.** A runtime or engine range, such as `engines.node`, must
  satisfy every dependency's own range and every runtime feature the code uses, including commands
  that run TypeScript directly.
- **Security at the sink.** Check every serialisation path when hiding sensitive fields, since
  `toJSON` can expose non-enumerable properties, and check that adapters keep security settings such
  as TLS certificate verification.
- **Proportionate reads.** Look for duplicated round trips and expensive aggregation the result
  doesn't need, especially on public reads and after a mutation has committed.
