# Route group patterns

Define a group and attach endpoints:

```csharp
[RouteGroup("api/orders")]
public sealed partial class Orders
{
    private static void CustomizeGroup(RouteGroupBuilder group)
        => group.RequireAuthorization("Orders").WithTags("Orders");
}

[Handler]
[MapGet("{id:guid}")]
[MapGroup<Orders>]
public static partial class GetOrder { }
```

`CustomizeGroup` is optional but, when present, must be exactly
`private static void CustomizeGroup(RouteGroupBuilder group)`. Other shapes are
ignored and report IAPI0011.

Nest groups through nested classes:

```csharp
[RouteGroup("api")]
public sealed partial class Api
{
    [RouteGroup("v1")]
    public sealed partial class V1
    {
        [RouteGroup("orders")]
        public sealed partial class Orders;
    }
}
```

Attach an endpoint to `[MapGroup<Api.V1.Orders>]`. The generator recursively
maps top-level groups from `MapXxxEndpoints()`.

Map an endpoint at the group root with an empty relative route:

```csharp
[Handler]
[MapGet("")]
[MapGroup<Orders>]
public static partial class GetOrders { }
```

Its runtime path is `api/orders`. The generated constant is deliberately the
plain join `api/orders/`; do not trim it in generated code or pretend that the
constant is normalized.

Each group receives a route constant for an endpoint with exactly one route.
Constants are a plain slash join and are not normalized; omit inconsistent
leading/trailing slashes if tests or link generation consume them.

When `CustomizeGroup` names an authorization policy, verify that the host
defines it. If the requested policy name exists but its requirements do not,
report that missing security decision instead of inventing claims or roles.

Registration tags flow from `MapXxxEndpoints` through groups. An unmatched
tagged parent skips the subtree; a matched parent does not bypass child or
endpoint checks. Align handler filters or the endpoint will map but fail to
resolve its generated handler.

## Sources

- Immediate.Dev: `Immediate.Apis/route-groups.md`
- Immediate.Dev: `Immediate.Apis/tagged-registration.md`
- Immediate.Dev: `Immediate.Apis/diagnostics.md`
- Immediate.Dev: `concepts/tags.md`
