# Behavior patterns

Derive from `Behavior<TRequest,TResponse>`, override `HandleAsync`, and invoke
the inherited `Next`:

```csharp
public sealed class LoggingBehavior<TRequest, TResponse>(
    ILogger<LoggingBehavior<TRequest, TResponse>> logger
) : Behavior<TRequest, TResponse>
{
    public override async ValueTask<TResponse> HandleAsync(
        TRequest request,
        CancellationToken cancellationToken
    )
    {
        logger.LogInformation("Entering {Handler}", HandlerType.Name);
        var response = await Next(request, cancellationToken);
        logger.LogInformation("Exiting {Handler}", HandlerType.Name);
        return response;
    }
}
```

`HandlerType` is populated by generated code with the handler container type.

## Placement and order

Declare behaviors on the assembly, a handler, or a reusable custom attribute:

```csharp
[assembly: Behaviors(typeof(LoggingBehavior<,>), typeof(TransactionBehavior<,>))]
```

The first listed type is outermost: `A, B` runs `A -> B -> handler -> B -> A`.
A handler-level `[Behaviors]`, including one supplied by a bundle attribute,
replaces the assembly list rather than appending to it.

Reference generic behaviors unbound, for example
`typeof(LoggingBehavior<,>)`. Zero-, one-, and two-parameter behavior shapes
are supported. More than two generic parameters or closed generic references
are invalid.

## Selection constraints

Concrete class, record, and interface constraints select matching handlers:

```csharp
public sealed class AuditBehavior<TRequest, TResponse>(IAudit audit)
    : Behavior<TRequest, TResponse>
    where TRequest : IAuditable;
```

Do not use `class`, `struct`, `unmanaged`, `notnull`, or `new()` constraints;
the generator does not support them. Nullable annotations participate in
matching, so `IEnumerable<User>` and `IEnumerable<User>?` differ.

When a behavior does not run, check nullability, constraints, handler-level
replacement, handler tag filtering, and whether the behavior is abstract.
Inspect the generated `Handler` constructor: an attached behavior appears as a
constructor parameter. An abstract behavior reports `IHR0024` and prevents the
affected generated handler from being emitted.

Call `services.AddXxxHandlers()`. Each selected handler registers the concrete
behavior types in its generated pipeline with `TryAddTransient`; an earlier
explicit registration for the same closed service type wins.

## Sources

- Immediate.Dev: `Immediate.Handlers/creating-behaviors.md`
- Immediate.Dev: `Immediate.Handlers/diagnostics.md`
- Immediate.Dev: `concepts/handlers-and-behaviors.md`
