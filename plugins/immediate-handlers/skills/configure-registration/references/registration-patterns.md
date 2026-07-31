# Handler registration patterns

Register assembly-wide generated services:

```csharp
services.AddApplicationBehaviors();
services.AddApplicationHandlers();
```

`Application` is derived from the assembly name, with `.`, spaces, and `-`
removed, unless `[assembly: ImmediateAssemblyIdentifier("...")]` overrides it.

`AddXxxHandlers` defaults to `ServiceLifetime.Scoped` and accepts another
default:

```csharp
services.AddApplicationHandlers(ServiceLifetime.Transient);
```

`[Handler(ServiceLifetime.Singleton)]` overrides the call-wide lifetime for
that handler. Generated registrations include the concrete `X.Handler`, the
matching `IHandler<,>` or `IStreamingHandler<,>`, `X.HandleBehavior`, and the
container for sealed handlers. Behaviors are always `TryAddTransient`.

Register one handler in a focused test with `X.AddHandlers(services)`. This
does not register its behaviors.

## Tags

Declare tags on the handler and filter at registration:

```csharp
[Handler(Tags = ["worker"])]
public static partial class RebuildIndex { }

services.AddApplicationHandlers(tags: "worker");
```

Rules:

1. No tags registers every handler, including tagged handlers.
2. Untagged handlers are always included in filtered calls.
3. Matching uses ordinal, case-sensitive equality and any requested tag may match.
4. `AddXxxBehaviors()` has no tag filter.

On C# 13+, generated tag parameters use `params ReadOnlySpan<string>`; older
language versions use `params string[]`. Loose arguments and collection
expressions work at either call site.

## Sources

- Immediate.Dev: `Immediate.Handlers/registration.md`
- Immediate.Dev: `Immediate.Handlers/tagged-registration.md`
- Immediate.Dev: `concepts/tags.md`
- Immediate.Dev: `concepts/assembly-identifier.md`
