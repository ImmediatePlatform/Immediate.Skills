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
Startup validates and reconciles code-defined schedules: unchanged definitions
preserve their next run, changed definitions recalculate it, and removed code
definitions are removed. Dynamic schedules are not removed by that process.

For application-owned schedules, omit declarative Cron and use the generated
`IRecurringJobScheduler` to add or update, remove, or trigger a named schedule.
Dynamic recurring schedules are also payloadless.

Choose overlap deliberately: `Skip` avoids concurrent occurrences, `Queue`
retains due occurrences, and `Concurrent` permits them to overlap. The NodaTime
companion adds typed time APIs and serializer metadata after registration.

## Sources

- Immediate.Dev: `Immediate.Jobs/recurring-jobs.md`
- Immediate.Dev: `Immediate.Jobs/nodatime.md`
- Immediate.Dev: `Immediate.Jobs/creating-jobs.md`
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
