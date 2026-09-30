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
source-generatable shapes. Generated metadata supports nullable value types and
public constructor, `init`, optional, and `required` property shapes. Avoid
interfaces, abstract members, and unsupported collection graphs. A job name is
part of the stored data, not display text. Set it explicitly before production
and do not reuse it for a different payload shape.

A request that implements `IJobRequest` receives `JobDetails` during execution.
Its typed identifiers are `JobHandle` and optional `BatchHandle`. Read their
`Value` only when an idempotency store or another boundary requires a string.

Default policies are three attempts, no timeout, unlimited job-level
concurrency, exponential jittered backoff with a five-second base, overlap skip,
and `MisfireHandlingMode.EnqueueOne` for recurring jobs. Queue concurrency, job
concurrency, and the node-wide `WorkerCount` and `MaxAcquisitionCount` all apply.
Select overrides from application requirements rather than copying them.

Register the generated pieces independently:

```csharp
services.AddMyAppHandlers();
services.AddMyAppJobs()
	.ConfigureStorage(storage => storage.UseInMemory());
```

Both generated methods live in the project's root namespace. Import it from
top-level startup code. `AddMyAppHandlers` registers the concrete behavior
dependencies that apply to each selected handler; there is no separate behavior
registration call. Align tags across handlers and jobs. The generated scheduler
is scoped, the runtime is singleton, and each attempt receives a fresh scope.
Repeated generated registration does not add another worker or duplicate job
descriptors, but storage may be configured only once.

`ConfigureWorkers` accepts a direct `ImmediateJobsOptions` callback or an
`OptionsBuilder<ImmediateJobsOptions>` callback. The latter can call `Bind` with
an `IConfiguration` section or `BindConfiguration` with a section path.

## Sources

- Immediate.Dev: `Immediate.Jobs/creating-jobs.md`
- Immediate.Dev: `Immediate.Jobs/delivery-guarantees.md`
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
- Immediate.Dev: `Immediate.Jobs/execution-context-and-behaviors.md`
