# Workflow graphs

`IBatchScheduler.Begin()` creates an in-memory `Batch` buffer. The interface is in
`Immediate.Jobs.Shared.Interfaces`; `Batch`, handles, and continuation enums are in
`Immediate.Jobs.Shared`. Generated schedulers add roots with synchronous
`Enqueue(payload, batch)` or `Schedule(payload, batch, delayOrTime)`. Add
dependencies with synchronous `ScheduleAfter`. These methods return a
`BatchJobHandle` tied to that open batch. `CommitAsync` writes the complete graph
atomically and may be called once. Disposal before commit abandons the buffer.

`BatchJobHandle.JobHandle` returns the durable handle only after commit. Reading
it earlier throws. Use `JobHandle.Value` or `BatchHandle.Value` only when a raw
string must cross an HTTP, database, or message boundary.

One parent plus one child forms a chain. Several children from one handle form
fan-out. Pass an `IReadOnlyList<BatchJobHandle>` to form fan-in. A continuation trigger
controls release: `Success` requires all parents to succeed, `Failure` requires
terminal parents with at least one failure, and `Complete` accepts any terminal
outcome. Unsatisfied conditional continuations and ineligible descendants become
terminal `Skipped` records; skipped branches do not fail an otherwise successful
batch.

Outside an open batch, `ScheduleAfterAsync` accepts one durable
`ContinuationHandle` or a list containing any mix of `JobHandle` and
`BatchHandle`. `IBatchScheduler.Begin` can also make a follow-up batch wait for
one or several committed batches. Delayed continuation overloads start their
delay after every parent reaches the required outcome, not when the child is
created.

```csharp
await using var batch = batches.Begin();
var root = import.Enqueue(new(importId), batch);
var left = transform.ScheduleAfter(new(importId), root);
var right = validate.ScheduleAfter(new(importId), root);
_ = publish.ScheduleAfter(new(importId), [left, right]);

BatchHandle committed = await batch.CommitAsync(cancellationToken);
JobHandle notification = await notify.ScheduleAfterAsync(
	new(importId),
	[committed, existingJob],
	TimeSpan.FromMinutes(5),
	ContinuationTrigger.Success,
	cancellationToken
);
```

The argument order is payload, parent or parent list, optional delay, trigger,
then cancellation. The final `ScheduleAfterAsync` call is a second durable write,
not part of the earlier atomic commit. If guaranteed attachment matters, give the
operation an idempotency or reconciliation path.

Once commit begins, a network or storage error can leave the outcome unknown.
Do not reuse the closed batch. Check for duplicates in application code before
building another graph.

In-memory storage implements graph behavior but loses it when the process exits.
Use a SQL provider when the workflow itself must survive process loss.

`IBatchScheduler.CancelAsync(BatchHandle)` durably cancels every non-terminal
member of a committed batch. It does not forcibly stop handler code already
running. If that handler finishes later, its result cannot replace the recorded
cancellation.

A running job whose request implements `IJobRequest` receives `JobDetails`.
Generated scheduling can add work beside current continuations, before them, or
detached from the batch. Expansion is valid only during the active attempt and
requires graph capability except for detached work.

Read batch status, members, and graphs with scoped `JobMonitor` or its read-only
`IJobMonitor` interface. Use the secured dashboard for operator-facing graph views.

## Sources

- Immediate.Dev: `Immediate.Jobs/batches-and-continuations.md`
- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/dashboard-and-monitoring.md`
- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
