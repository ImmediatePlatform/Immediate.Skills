---
name: cache-handler
description: Create or update an Immediate.Cache wrapper for a value-returning Immediate.Handlers handler, including key design, AddMemoryCache/AddXxxCaches registration, read-through access, invalidation, priming, TransformValue updates, concurrency, and common IC diagnostics. Use for handler caching behavior; use configure-entry for expiration, size, priority, and eviction callbacks.
---

# Cache an Immediate handler

Add a process-local cache whose key, invalidation, and concurrency semantics remain correct as the feature changes.

## Workflow

1. Inspect the target handler, request/response types, static versus sealed shape, mutation handlers, DI registration, deployment topology, and package versions.
2. Read [cache-patterns.md](references/cache-patterns.md).
3. Confirm the target is a non-static `[Handler]` returning `ValueTask<TResponse>`. Convert a static handler to a sealed instance shape when caching is required.
4. Create one top-level sealed partial cache class with `[CacheFor<THandler>]` and a deterministic `TransformKey` containing every request value that affects the response.
5. Add `AddMemoryCache()`, handler/behavior registration, and `AddXxxCaches()`.
6. Replace direct reads with the concrete cache's `GetValue` only where cache semantics are desired.
7. Update successful writes to call `SetValue`, `RemoveValue`, or a purpose-built `TransformValue` wrapper. Keep transformers pure and idempotent.
8. Test misses, hits, invalidation/priming, failure retry, concurrent coalescing, and cancellation. Account for multi-process deployments explicitly.

## Guardrails

- Never inject scoped dependencies into the singleton cache class; keep them on the handler.
- Remember that a cache hit skips the handler and every behavior.
- `SetValue` and `RemoveValue` return void.
- Use a distributed design instead when cross-instance consistency is required; Immediate.Cache uses `IMemoryCache` only.

## Handoff

Report key shape, registration, read/write integration, invalidation semantics, process boundary, and focused test results.
