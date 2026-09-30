# Recurring patterns

A code-owned recurring schedule belongs on a payloadless declaration:

```csharp
[Handler]
[Job(
    Name = "rebuild-search-index",
    Cron = "0 */15 * * * *",
    TimeZone = "Europe/Vienna",
    OverlapPolicy = OverlapPolicy.Skip,
    MisfireHandlingMode = MisfireHandlingMode.EnqueueOne)]
public sealed partial class RebuildSearchIndex
{
    private ValueTask HandleAsync(EmptyJobRequest request, CancellationToken token)
        => ValueTask.CompletedTask;
}
```

## Schedule formats

`Cron` (and the dynamic `cron` argument) accepts:

- five-field Cron with minute precision, such as `*/15 * * * *`;
- six-field Cron with seconds first, such as `0 */15 * * * *`;
- the macros `@yearly`/`@annually`, `@monthly`, `@weekly`, `@daily`/`@midnight`,
  and `@hourly`;
- an RFC 5545 recurrence-rule body, such as
  `FREQ=WEEKLY;BYDAY=MO;BYHOUR=6;BYMINUTE=0`.

A recurrence rule must repeat forever: `COUNT` or `UNTIL` is analyzer error
`IJOB0007` on `[Job]` and throws `ImmediateJobException` when a dynamic schedule
is saved. A schedule with no future occurrence also throws. Time zones default to
UTC and must be IANA IDs.

## Startup merge

With recurring-capable storage, startup merges every code-defined schedule in
one storage operation:

- new code schedules are added;
- unchanged Cron and time zone keep `NextRunAt`, `LastRunAt`, and paused state,
  including an occurrence that became due while the app was stopped;
- a changed Cron or time zone recalculates `NextRunAt` from now but keeps
  `LastRunAt` and paused state;
- a dynamic schedule with the same name is promoted to code-defined instead of
  duplicated;
- code schedules no longer in code are removed; other dynamic schedules stay.

Queue-only custom storage skips the merge. The merge also runs when workers are
disabled with `DisableWorkers()`.

## Missed runs

`MisfireHandlingMode` controls occurrences missed while no scheduler was running:

| Mode                   | Missed occurrences                                           |
| ---------------------- | ------------------------------------------------------------ |
| `EnqueueOne` (default) | One run due now for all missed occurrences.                  |
| `EnqueueAll`           | One run per missed occurrence, in order.                     |
| `EnqueueNone`          | No runs; the schedule moves to its next future occurrence.   |

The schedule then continues from its next future occurrence. The worker logs a
`RecurringOccurrencesMissed` warning. The job's mode also applies to dynamic
schedules that run it. Test it with `JobTestHarness.ResetScheduler()` after
advancing fake time.

## Overlap

Overlap checks every unfinished run of the job, including manual triggers:
`Skip` records the new occurrence as terminal `Skipped` history, `Queue` saves it
as a continuation of the latest unfinished run so runs never overlap, and
`Concurrent` permits overlap. `Queue` needs graph storage; Redis lacks it, so
queued schedules fail to materialize there and log
`RecurringMaterializationFailed`.

## Dynamic schedules and triggers

For application-owned schedules, omit declarative Cron and use the generated
`IRecurringJobScheduler` from `Immediate.Jobs.Shared.Interfaces` to add or
update, remove, or trigger a named schedule. Dynamic recurring schedules are
also payloadless. The saved schedule includes the job's generated `QueueName`,
so occurrences use the queue selected by `[UsesQueue<TQueue>]`.

The typed scheduler's `TriggerNowAsync` returns a `JobHandle`; the raw identifier
is available through `Value`. Use the singleton `JobMonitor` to pause, resume, or
trigger a saved schedule by its schedule name. For a code-defined schedule, the
schedule name is the job name; a dynamic schedule may use a different name.
Neither trigger moves the next occurrence. The generated `RecurringJobs`
dispatcher was removed; do not reference it.

Generated registration called without tags includes every tagged job. To create
a host slice, pass a non-empty tag list to both handler and job registration.
Untagged jobs are always included, and any matching tag includes a multi-tag job.
The NodaTime companion adds typed time APIs and serializer metadata after
registration.

## Sources

- Immediate.Dev: `Immediate.Jobs/recurring-jobs.md`
- Immediate.Dev: `Immediate.Jobs/nodatime.md`
- Immediate.Dev: `Immediate.Jobs/creating-jobs.md`
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
