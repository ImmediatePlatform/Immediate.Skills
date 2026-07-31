# Cache testing patterns

Compose real services:

```csharp
var services = new ServiceCollection();
services.AddMemoryCache();
services.AddApplicationCaches();
services.AddApplicationHandlers();
await using var provider = services.BuildServiceProvider();

var cache = provider.GetRequiredService<GetOrderCache>();
```

The generated method names come from the assembly declaring the cache and
handler, not the test assembly. Cache classes are singletons, so use a fresh
provider per test or fixture isolation boundary.

Alternatively omit `AddXxxHandlers()` and register a controlled scoped fake:

```csharp
services.AddScoped<IHandler<GetOrder.Query, Order>, FakeGetOrderHandler>();
```

Assert `GetValue` results and execution counts. Use
`IMemoryCache.TryGetValue(expectedKey, out _)` only to prove key creation; the
stored value is an internal wrapper.

Test `SetValue` bypass, `RemoveValue` re-execution, failure-not-cached, and
expiration. For concurrency, block a fake handler on a manually controlled
`TaskCompletionSource`, start multiple reads, assert they remain pending,
release once, and prove one execution serves both. Use the same gate around a
transformer, modify the value concurrently, and prove the transformer retries.

## Sources

- Immediate.Dev: `Immediate.Cache/testing-caches.md`
- Immediate.Dev: `Immediate.Cache/reading-and-writing.md`
- Immediate.Dev: `Immediate.Cache/how-it-works.md`
