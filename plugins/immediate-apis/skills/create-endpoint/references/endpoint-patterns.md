# Endpoint patterns

Apply `[Handler]` and one of `[MapGet]`, `[MapPost]`, `[MapPut]`,
`[MapPatch]`, `[MapDelete]`, or `[MapMethod]`:

```csharp
[Handler]
[MapGet("/orders/{id:guid}")]
public static partial class GetOrder
{
    public sealed record Query
    {
        [FromRoute]
        public required Guid Id { get; init; }
    }

    internal static Results<Ok<Order>, NotFound> TransformResult(Order? result)
        => result is null ? TypedResults.NotFound() : TypedResults.Ok(result);

    private static ValueTask<Order?> HandleAsync(
        Query query,
        IOrderReader reader,
        CancellationToken cancellationToken
    ) => reader.GetAsync(query.Id, cancellationToken);
}
```

## Binding order

The first matching rule wins:

1. A recognized binding attribute on the handle method's request parameter.
2. Any request property of type `IFormFile` selects `[FromForm]`.
3. A declared request property with `[FromBody]`, `[FromForm]`, `[FromHeader]`,
   `[FromQuery]`, or `[FromRoute]` selects `[AsParameters]`.
4. Post/put/patch select `[FromBody]`; get/delete/`MapMethod` select
   `[AsParameters]`.

Only properties declared directly on the request type affect inference.
`MapMethod` uses its attribute kind, not the supplied verb string. Add an
explicit `[FromBody]` to its request parameter when needed.

## Authorization and registration

`[Authorize]` supports the default policy or a named policy through its
constructor/`Policy`. Roles and authentication-scheme named arguments are not
translated; define an ASP.NET Core policy instead. `[AllowAnonymous]` wins if
both are present, so remove the conflict.

Call `app.MapXxxEndpoints(prefix, tags...)`. The method returns the prefix
`RouteGroupBuilder`, allowing assembly-wide conventions. Ensure the matching
generated handlers were registered in DI.

`TransformResult` must be `internal static`, return non-void, and accept exactly
the handler response type including nullability. A command returning bare
`ValueTask` uses a parameterless transform.

## Sources

- Immediate.Dev: `Immediate.Apis/creating-endpoints.md`
- Immediate.Dev: `Immediate.Apis/binding-request-data.md`
- Immediate.Dev: `Immediate.Apis/authorization.md`
- Immediate.Dev: `Immediate.Apis/customizing-endpoints.md`
- Immediate.Dev: `Immediate.Apis/diagnostics.md`
