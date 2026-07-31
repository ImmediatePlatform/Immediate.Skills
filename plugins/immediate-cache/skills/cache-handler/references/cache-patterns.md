# Cache patterns

The target must be a non-static `[Handler]` returning `ValueTask<T>`:

```csharp
[CacheFor<GetOrder>]
public sealed partial class GetOrderCache
{
    protected override string TransformKey(GetOrder.Query request)
        => $"GetOrder:{request.Id}";
}
```

The generator derives `ApplicationCache<TRequest,TResponse>` and its constructor.
A static target is silently skipped and usually surfaces as CS0115 on
`TransformKey`; make the handler sealed/instance. Bare `ValueTask` commands
cannot be cached.

Register all three layers:

```csharp
services.AddMemoryCache();
services.AddApplicationHandlers();
services.AddApplicationCaches();
```

Inject the concrete cache. `GetValue(request, token)` returns a hit or creates a
scope, resolves `IHandler<,>`, runs the whole behavior pipeline, and stores the
response. Concurrent misses for one key share one execution. A caller token
cancels only that caller's wait, not shared execution. Failures reach all
waiters but are not cached.

`SetValue(request, response)` primes or replaces a value and completes waiters.
`RemoveValue(request)` clears the response; during execution it cancels and
restarts the handler while existing waiters continue waiting. Both return void.

Expose `TransformValue` through a purpose-built public cache method for
read-modify-write. It retries if another operation changed the value, so the
transformer may run repeatedly and must have no external side effects.

Keys share the application's `IMemoryCache`; prefix them per cache and include
all response-affecting request fields. All behavior is per process.

## Sources

- Immediate.Dev: `Immediate.Cache/creating-a-cache.md`
- Immediate.Dev: `Immediate.Cache/reading-and-writing.md`
- Immediate.Dev: `Immediate.Cache/how-it-works.md`
- Immediate.Dev: `Immediate.Cache/diagnostics.md`
