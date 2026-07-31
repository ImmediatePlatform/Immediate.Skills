# Cache entry options

The default is a five-minute sliding expiration. Override it on the generated
cache class:

```csharp
protected override MemoryCacheEntryOptions GetCacheEntryOptions()
    => new()
    {
        AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1),
        Priority = CacheItemPriority.High,
        Size = 1,
    };
```

All normal `MemoryCacheEntryOptions` features are available: absolute and
sliding expiration, priority, size, expiration tokens, and post-eviction
callbacks. Return `new()` for no expiration.

The method runs once for a key when the first `GetValue`, `SetValue`,
`RemoveValue`, or `TransformValue` creates its internal entry. It takes no
request, so one cache class has one policy. Split caches/handlers if policies
must differ.

If `AddMemoryCache(options => options.SizeLimit = ...)` configures a size limit,
every generated cache entry must set `Size` or entry creation throws.

Eviction callbacks receive Immediate.Cache's internal state wrapper, not
`TResponse`; use the key, reason, state, logging, and metrics only. Expiration
removes the wrapper and the next read creates a fresh execution slot.

The generated base class is fixed. Share policy through a plain helper that
returns `MemoryCacheEntryOptions`, not through another base class.

## Sources

- Immediate.Dev: `Immediate.Cache/cache-entry-options.md`
- Immediate.Dev: `Immediate.Cache/api-reference.md`
