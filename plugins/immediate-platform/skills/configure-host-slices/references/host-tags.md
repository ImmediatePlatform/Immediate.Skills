# Cross-package tags

Shared rules:

1. Calling a generated method without tags includes every tagged and untagged item.
2. A filtered call always includes untagged items.
3. Matching is ordinal, case-sensitive equality with no wildcards.
4. An item matches when any of its tags matches any requested tag.

Example:

```csharp
[Handler(Tags = ["worker"])]
public sealed partial class ProcessOutbox;

[MapGet("api/orders", Tags = ["web"])]
public sealed partial class GetOrders;

[RegisterScoped(Tags = ["worker"])]
public sealed class OutboxProcessor;

services.AddAppHandlers(tags: "worker");
services.AddAppServices("worker");
app.MapAppEndpoints(tags: ["web"]);
```

`AddXxxHandlers` accepts lifetime before tags. `MapXxxEndpoints` accepts prefix
before tags. `AddXxxJobs` accepts options before tags. C# 13+ may emit
`params ReadOnlySpan<string>` and older language versions `params string[]`;
ordinary calls are the same.

Endpoint group tags flow downward. An unmatched tagged group skips its subtree;
matched groups still allow endpoint-level filtering. Handler tags must align
with endpoint tags or mapped endpoints may fail DI resolution.

Behaviors are not tag-filtered. Preview job queue definitions are assembly-wide;
selected jobs still require matching handler registration.

## Sources

- Immediate.Dev: `concepts/tags.md`
- Immediate.Dev: package tagged-registration guides
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
