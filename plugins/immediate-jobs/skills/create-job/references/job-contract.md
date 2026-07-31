# Job contract

```csharp
[Handler, Job(Name = "send-order-receipt", MaxAttempts = 5)]
public sealed partial class SendOrderReceipt(OrdersDbContext db)
{
    public sealed record Command(Guid OrderId);

    private async ValueTask HandleAsync(
        Command command,
        CancellationToken cancellationToken)
    {
        // Make the side effect safe to repeat for command.OrderId.
    }
}
```

The job type must be non-nested and partial. The handler shape is a private
instance `HandleAsync`; the request is first and cancellation token last.
Payloadless jobs use `EmptyJobRequest` and are the only jobs eligible for a
declarative Cron schedule.

Payloads and captured context are persisted JSON. Keep them small and use
source-generatable shapes. A job name is a durable discriminator, not display
text. Set it explicitly before production and do not reuse it for a different
payload contract.

Default policies are three attempts, no timeout, unlimited job-level
concurrency, exponential jittered backoff with a five-second base, and overlap
skip. Select overrides from application requirements rather than copying them.

Register the generated pieces independently:

```csharp
services.AddMyAppBehaviors();
services.AddMyAppHandlers();
services.AddMyAppJobs(options => options.UseInMemory());
```

Align registration tags across handlers and jobs. The generated scheduler is
scoped, the runtime is singleton, and each attempt receives a fresh scope.

## Sources

- Immediate.Dev: `Immediate.Jobs/creating-jobs.md`
- Immediate.Dev: `Immediate.Jobs/delivery-guarantees.md`
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
- Immediate.Dev: `Immediate.Jobs/execution-context-and-behaviors.md`
