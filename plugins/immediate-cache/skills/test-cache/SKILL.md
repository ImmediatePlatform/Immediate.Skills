---
name: test-cache
description: Add or update tests for an Immediate.Cache generated cache using a real ServiceCollection, IMemoryCache, generated cache registration, generated or fake handlers, and deterministic concurrency controls. Use to verify hits, misses, keys, priming, invalidation, expiration, coalescing, cancellation, or TransformValue retries.
---

# Test an Immediate cache

Exercise the real cache implementation rather than mocking away the behavior under test.

## Workflow

1. Inspect the Immediate.Cache and Immediate.Handlers versions, test framework, fixture lifetimes, assembly identifiers, cache/handler assembly, existing fakes, and cancellation conventions.
2. Read [cache-testing.md](references/cache-testing.md).
3. Build a fresh `ServiceCollection`/provider with memory cache, generated caches, and either generated handlers or a controlled `IHandler<,>` fake.
4. Resolve the concrete cache and assert behavior through its public methods. Inspect `IMemoryCache` only for key existence, not stored response value.
5. Prove handler execution or bypass with a counter/flag/fake response.
6. Use a `TaskCompletionSource` or equivalent deterministic gate for coalescing, caller cancellation, in-flight invalidation, and optimistic-transform retries.
7. Dispose providers and avoid cross-test singleton cache reuse.
8. Run focused tests repeatedly to detect timing flakiness.

## Guardrails

- Call generated registration methods from the assembly that declares the handlers/caches, not from the test assembly name.
- Avoid arbitrary delays for concurrency tests.
- Assert reference equality only where coalesced callers are documented to share a response instance.

## Handoff

Report composition, controlled fake/gate, behaviors proven, concurrency determinism, and test command result.
