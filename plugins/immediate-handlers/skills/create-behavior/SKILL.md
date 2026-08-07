---
name: create-behavior
description: Create or update an ordinary Immediate.Handlers pipeline behavior for logging, validation, transactions, authorization, telemetry, or another cross-cutting concern. Use when behavior ordering, generic constraints, reusable behavior bundles, DI registration, or a behavior that does not run must be handled; use create-streaming-handler for streaming behaviors.
---

# Create an Immediate behavior

Build a compile-time-selected pipeline behavior and prove that it attaches to the intended handlers.

## Workflow

1. Inspect existing `[Behaviors]` declarations, behavior base classes, request/response types, nullable annotations, DI registration, and package version.
2. Read [behavior-patterns.md](references/behavior-patterns.md).
3. Implement `Behavior<TRequest,TResponse>` and override `HandleAsync`. Call `Next` exactly where the wrapped pipeline should execute.
4. Decide placement deliberately: assembly-wide, handler-specific, or a reusable attribute bundle.
5. Order the list from outermost to innermost. Preserve required global behaviors when adding a handler-level list because that list replaces the assembly list.
6. Use supported concrete type constraints to select handlers. Verify nullability and fixed request/response types match.
7. Confirm `AddXxxHandlers()` is called. It registers each selected handler's concrete behavior dependencies as transient services.
8. Build and inspect the generated handler constructor when attachment is uncertain. Run focused behavior-order and short-circuit tests.

## Boundaries

- Use `create-streaming-handler` for `StreamingBehavior<,>` and `IAsyncEnumerable<T>` pipelines.
- Keep request validation in the Immediate.Validations workflow unless implementing an alternative validation behavior was explicitly requested.
- Treat tags as handler filters. Behavior registration follows the selected handlers rather than accepting a separate tag filter.

## Handoff

Report the placement, effective outer-to-inner order, matching constraint, registration, and evidence that the intended generated pipelines contain the behavior.
