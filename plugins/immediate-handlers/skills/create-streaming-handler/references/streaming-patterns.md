# Streaming patterns

Return `IAsyncEnumerable<TResponse>` from the single private handle method:

```csharp
[Handler]
public static partial class StreamOrders
{
    public sealed record Query;

    private static async IAsyncEnumerable<Order> HandleAsync(
        Query query,
        IOrderReader reader,
        [EnumeratorCancellation] CancellationToken cancellationToken
    )
    {
        await foreach (var order in reader.ReadAsync(cancellationToken))
            yield return order;
    }
}
```

The generated handler implements
`IStreamingHandler<StreamOrders.Query, Order>`. Consume it with
`await foreach` and pass cancellation using `WithCancellation` where needed.

Wrap the stream with `StreamingBehavior<TRequest,TResponse>`:

```csharp
public sealed class CountBehavior<TRequest, TResponse>(ILogger<CountBehavior<TRequest,TResponse>> log)
    : StreamingBehavior<TRequest, TResponse>
{
    public override async IAsyncEnumerable<TResponse> HandleAsync(
        TRequest request,
        [EnumeratorCancellation] CancellationToken cancellationToken
    )
    {
        var count = 0;
        await foreach (var item in Next(request, cancellationToken)
            .WithCancellation(cancellationToken))
        {
            count++;
            yield return item;
        }
        log.LogInformation("Streamed {Count} items", count);
    }
}
```

Streaming and non-streaming behaviors may appear in one `[Behaviors]` list;
the generator matches each kind only to the corresponding handler pipeline.
The same ordering, unbound generic, constraint, and registration rules used by
ordinary behaviors still apply.

## Sources

- Immediate.Dev: `Immediate.Handlers/streaming-handlers.md`
- Immediate.Dev: `Immediate.Handlers/attributes-and-interfaces.md`
- Immediate.Dev: `concepts/handlers-and-behaviors.md`
