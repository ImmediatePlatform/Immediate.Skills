---
name: configure-entry
description: Configure Immediate.Cache MemoryCacheEntryOptions for expiration, size, priority, tokens, or eviction callbacks by overriding GetCacheEntryOptions. Use when cache policy, memory limits, or eviction behavior is the main task; use cache-handler to create the cache or change read/write integration.
---

# Configure an Immediate cache entry

Choose a per-cache-class memory policy consistent with freshness, memory limits, and observability requirements.

## Workflow

1. Inspect the Immediate.Cache version, existing `AddMemoryCache` configuration, size limits, cache usage, freshness requirements, deployment topology, and eviction instrumentation.
2. Read [entry-options.md](references/entry-options.md).
3. Override `GetCacheEntryOptions()` on the partial cache class and return a fresh options instance.
4. Select sliding, absolute, combined, or no expiration deliberately. Add size whenever the shared memory cache has a size limit.
5. Use callbacks only for logging/metrics; never cast their value to the handler response.
6. Share policies through helper factories rather than adding another cache base class.
7. Test expiration with controlled time where possible, size-limit behavior, callback metadata, and re-execution after eviction.

## Guardrails

- The method runs once when each key's internal entry is first created and receives no request, so it cannot vary policy per key.
- An empty options object means no expiration; the package default otherwise is five-minute sliding expiration.
- Avoid unbounded entries unless the key cardinality and memory budget are demonstrably bounded.

## Handoff

Report expiration/size policy, why it fits the data, callback limitations, and eviction/reload test evidence.
