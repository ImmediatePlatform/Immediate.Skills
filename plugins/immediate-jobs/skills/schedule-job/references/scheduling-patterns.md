# Scheduling patterns

Resolve the generated scoped scheduler and call the typed method that expresses
the timing requirement:

```csharp
JobHandle now = await scheduler.EnqueueAsync(new(orderId), cancellationToken);
JobHandle later = await scheduler.ScheduleAsync(
    new(orderId), TimeSpan.FromMinutes(10), cancellationToken);
JobHandle exact = await scheduler.ScheduleAsync(
    new(orderId), runAt, cancellationToken);
```

These calls report that persistence succeeded, not that the job ran. Their
cancellation token cancels only the storage operation. `JobHandle` is an opaque
durable identity suitable for dependencies and monitoring. Its `Value` property
contains the raw string for an HTTP, database, or message boundary. Convert an
incoming string with `JobHandle.FromString`.

Fair overloads accept a group ID for round-robin acquisition across active
groups. Enable fair queues from the registration builder and use a provider that
supports them:

```csharp
services.AddMyAppJobs()
	.UseFairQueues()
	.ConfigureStorage(storage => storage.UseInMemory());
```

`UseFairQueues` also accepts an `OptionsBuilder<FairQueueOptions>` callback. Bind
it to `IConfiguration` when fairness settings belong to host configuration, and
ensure a bound `Enabled` value remains `true`.

Whitespace normalizes to no group and identifiers longer than 128 characters
are rejected. Redis does not implement fair acquisition.

Generated schedulers are scoped because enqueue-time context extractors may
read scoped tenant or request state. Singleton callers must create a scope.

Use `scheduler.CancelAsync(handle, cancellationToken)` for a non-terminal
invocation. The token cancels only that storage operation. The recorded
cancellation does not forcibly stop handler code already running. If the handler
finishes later, its result cannot replace the cancelled state.

The `Immediate.Jobs.NodaTime` companion adds `Duration`, `Instant`, and
`DateTimeZone` support after the fixed `AddImmediateJobsNodaTime()` extension is
called. Keep all workers on compatible time-zone data and package revisions.

## Sources

- Immediate.Dev: `Immediate.Jobs/enqueueing-and-scheduling.md`
- Immediate.Dev: `Immediate.Jobs/queues-and-fairness.md`
- Immediate.Dev: `Immediate.Jobs/execution-context-and-behaviors.md`
- Immediate.Dev: `Immediate.Jobs/nodatime.md`
