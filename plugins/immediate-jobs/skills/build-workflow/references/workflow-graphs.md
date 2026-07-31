# Workflow graphs

`IJobBatchScheduler.Begin()` creates an in-memory buffer. Generated schedulers
add roots with `AddToBatch` or `AddToBatchAt` and dependencies with
`ScheduleAfterAsync`. `CommitAsync` writes the complete graph atomically and may
be called once. Disposal before commit abandons the buffer.

One parent plus one child forms a chain. Several children from one handle form
fan-out. Pass multiple parent handles to form fan-in. A continuation trigger
controls release: `Success` requires all parents to succeed, `Failure` requires
terminal parents with at least one failure, and `Complete` accepts any terminal
outcome. Unsatisfied continuations are cascade-cancelled as documented.

Once commit begins, a failed response can leave the durable outcome unknown.
Do not reuse the closed batch; use application-level deduplication before
building another graph.

A running job whose request implements `IJobRequest` receives `JobDetails`.
Generated scheduling can add work beside current continuations, before them, or
detached from the batch. Expansion is valid only during the active attempt and
requires graph capability except for detached work.

Monitor with `IJobBatchMonitor` or the secured dashboard graph views.

## Sources

- Immediate.Dev: `Immediate.Jobs/batches-and-continuations.md`
- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/dashboard-and-monitoring.md`
- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
