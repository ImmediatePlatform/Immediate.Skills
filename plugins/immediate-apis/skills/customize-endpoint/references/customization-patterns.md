# Endpoint customization patterns

Use three mechanisms from least to most procedural.

## Handle method attributes

Attributes on the handle method are copied to the generated endpoint delegate,
including constructor and named arguments. Prefer this for static metadata such
as `[ProducesResponseType]`.

## CustomizeEndpoint

Use exactly one `private` or `internal` static void method taking
`RouteHandlerBuilder` or `IEndpointConventionBuilder`:

```csharp
internal static void CustomizeEndpoint(RouteHandlerBuilder endpoint)
    => endpoint
        .WithName("GetOrder")
        .WithDescription("Returns an order")
        .ProducesValidationProblem()
        .RequireRateLimiting("api");
```

Use `RouteHandlerBuilder` for route-specific extension methods. The generator
calls the method once per registered route after authorization conventions.
Wrong accessibility, return type, parameter, instance modifier, or multiple
overloads produces IAPI0004 and the customization is ignored.

## TransformResult

Use `internal static` only. Return a non-void transport result and accept one
parameter matching the handler response including nullable annotations:

```csharp
internal static Results<Ok<Order>, NotFound> TransformResult(Order? result)
    => result is null ? TypedResults.NotFound() : TypedResults.Ok(result);
```

For bare `ValueTask` commands, accept no parameters. An invalid signature
produces IAPI0005 and raw handler output remains.

Use attributes for static metadata, `CustomizeEndpoint` for builder behavior,
`TransformResult` for response conversion, and route groups for shared policy.

## Sources

- Immediate.Dev: `Immediate.Apis/customizing-endpoints.md`
- Immediate.Dev: `Immediate.Apis/attributes-reference.md`
- Immediate.Dev: `Immediate.Apis/diagnostics.md`
