# Handler patterns

## Required shape

- Mark one namespace-level `partial` class with `[Handler]`; handler containers cannot be nested.
- Declare exactly one private method named `Handle` or `HandleAsync`.
- Put the request in the first parameter.
- Return `ValueTask`, `ValueTask<TResponse>`, or `IAsyncEnumerable<TResponse>`. `Task` and `Task<T>` are invalid.
- Put `CancellationToken` last when present.

## Dependency choices

Use a static handler when dependencies read clearly as method parameters:

```csharp
[Handler]
public static partial class GetOrder
{
    public sealed record Query(Guid Id);

    private static ValueTask<Order?> HandleAsync(
        Query query,
        IOrderRepository repository,
        CancellationToken cancellationToken
    ) => repository.GetAsync(query.Id, cancellationToken);
}
```

Place dependencies between the request and token. Their attributes, including
`[FromKeyedServices]`, are copied to the generated constructor.

Use a sealed handler when constructor injection is clearer:

```csharp
[Handler]
public sealed partial class GetOrder(IOrderRepository repository)
{
    public sealed record Query(Guid Id);

    private ValueTask<Order?> HandleAsync(
        Query query,
        CancellationToken cancellationToken
    ) => repository.GetAsync(query.Id, cancellationToken);
}
```

An instance handle method accepts only the request and optional token;
dependencies belong in the primary constructor. Consume `GetOrder.Handler`,
not `GetOrder`, because direct container use bypasses behaviors.

## Registration and consumption

Call the assembly-generated `services.AddXxxHandlers()` method. Its identifier
comes from the assembly name unless overridden with
`[assembly: ImmediateAssemblyIdentifier("...")]`.

Inject `GetOrder.Handler` when the consumer can reference the slice, or
`IHandler<GetOrder.Query, Order?>` across a boundary. A bare `ValueTask` command
implements `IHandler<TRequest, ValueTuple>`.

Common diagnostic mappings:

- IHR0001: add exactly one handle method.
- IHR0002: replace `Task` with an appropriate `ValueTask` shape.
- IHR0010/IHR0011: keep one private candidate.
- IHR0014/IHR0015: fix request/token placement; instance handlers cannot take method dependencies.
- IHR0016/IHR0018/IHR0019: align sealed-instance or static shape.
- IHR0022: consume the generated `Handler`, not the sealed container.

## Sources

- Immediate.Dev: `Immediate.Handlers/creating-handlers.md`
- Immediate.Dev: `Immediate.Handlers/handler-dependencies.md`
- Immediate.Dev: `Immediate.Handlers/registration.md`
- Immediate.Dev: `Immediate.Handlers/diagnostics.md`
