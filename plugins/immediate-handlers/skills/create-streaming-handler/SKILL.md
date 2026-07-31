---
name: create-streaming-handler
description: Create or update an Immediate.Handlers streaming handler returning an async enumerable, consume the generated streaming pipeline, or add a typed streaming behavior. Use for incremental result streaming and streaming pipeline concerns; do not use for ordinary ValueTask handlers or HTTP response mechanics alone.
---

# Create a streaming handler

Implement an `IAsyncEnumerable<T>` handler without losing cancellation or behavior semantics.

## Workflow

1. Inspect the package version, neighboring handler conventions, the consumer's streaming API, and existing `[Behaviors]` declarations.
2. Read [streaming-patterns.md](references/streaming-patterns.md).
3. Create a valid `[Handler]` container whose private handle method returns `IAsyncEnumerable<TResponse>`.
4. Apply `[EnumeratorCancellation]` to iterator cancellation tokens and pass the token through async enumeration and dependencies.
5. Consume the generated `X.Handler` or `IStreamingHandler<TRequest,TResponse>` and enumerate with cancellation.
6. For cross-cutting streaming logic, derive from `StreamingBehavior<,>`, enumerate `Next`, and re-yield items. Keep ordinary and streaming behaviors in the same `[Behaviors]` list only when each base class matches its intended pipeline.
7. Register handlers and behaviors with the generated methods.
8. Build and test partial enumeration, cancellation, exception propagation, and item ordering.

## Boundaries

- Do not buffer the sequence into a collection unless the requested behavior explicitly requires buffering.
- Do not substitute an ordinary `Behavior<,>` for a streaming behavior; matching is separate.
- Leave ASP.NET streaming response format and endpoint metadata to the API workflow unless requested together.

## Handoff

Report the element type, cancellation path, generated consumer type, attached streaming behaviors, and focused test result.
