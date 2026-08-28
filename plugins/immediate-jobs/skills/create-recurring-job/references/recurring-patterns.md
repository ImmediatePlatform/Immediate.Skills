# Recurring patterns

A code-owned recurring schedule belongs on a payloadless declaration:

```csharp
[Handler]
[Job(
    Name = "rebuild-search-index",
    Cron = "0 */15 * * * *",
    TimeZone = "Europe/Vienna",
    OverlapPolicy = OverlapPolicy.Skip)]
public sealed partial class RebuildSearchIndex
{
    private ValueTask HandleAsync(EmptyJobRequest request, CancellationToken token)
        => ValueTask.CompletedTask;
}
```

Cron accepts five or six fields and defaults to UTC. Time-zone IDs are IANA.
With recurring-capable storage, startup validates and reconciles code-defined
schedules: unchanged definitions preserve their next run, changed definitions
recalculate it, and removed code definitions are removed. Dynamic schedules are
not removed by that process. Queue-only custom storage skips reconciliation.

For application-owned schedules, omit declarative Cron and use the generated
`IRecurringJobScheduler` from `Immediate.Jobs.Shared.Interfaces` to add or
update, remove, or trigger a named schedule. Dynamic recurring schedules are
also payloadless. The saved schedule includes the job's generated `QueueName`,
so occurrences use the queue selected by `[UsesQueue<TQueue>]`.

Every assembly also generates a singleton `RecurringJobs` dispatcher in the
project's root namespace. Use `TriggerNowAsync(jobName)` when infrastructure
selects a payloadless job by its stable `[Job(Name = ...)]` identity. Matching is
case-sensitive. This is a job name, not a dynamic schedule name. An unknown name
fails before scope creation. A known job that registration tags excluded fails
when its scheduler cannot be resolved. Both throw `ImmediateJobException` and
the dispatcher does not return the new `JobHandle`; use the typed scheduler when
the handle matters. The typed scheduler's `TriggerNowAsync` returns `JobHandle`;
the raw identifier is available through `Value`. Payload-bearing jobs are not in
the dispatcher.

Generated registration called without tags includes every tagged job. To create
a host slice, pass a non-empty tag list to both handler and job registration.
Untagged jobs are always included, and any matching tag includes a multi-tag job.

Choose overlap deliberately: `Skip` records the occurrence as terminal
`Skipped` history, `Queue` retains due occurrences but runs one at a time, and
`Concurrent` permits overlap. The NodaTime companion adds typed time APIs and
serializer metadata after registration.

Use scoped `JobMonitor` to pause, resume, or trigger a saved schedule by its
schedule name. This is separate from `RecurringJobs.TriggerNowAsync`, which
takes the stable job name.

## Sources

- Immediate.Dev: `Immediate.Jobs/recurring-jobs.md`
- Immediate.Dev: `Immediate.Jobs/nodatime.md`
- Immediate.Dev: `Immediate.Jobs/creating-jobs.md`
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
