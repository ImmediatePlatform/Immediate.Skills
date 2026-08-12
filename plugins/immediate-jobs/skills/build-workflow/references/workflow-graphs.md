# Workflow graphs

`IBatchScheduler.Begin()` creates an in-memory `Batch` buffer. The interface is in
`Immediate.Jobs.Shared.Interfaces`; `Batch`, handles, and continuation enums are in
`Immediate.Jobs.Shared`. Generated schedulers
add roots with `AddToBatch` or `AddToBatchAt` and dependencies with
`ScheduleAfterAsync`. `CommitAsync` writes the complete graph atomically and may
be called once. Disposal before commit abandons the buffer.

One parent plus one child forms a chain. Several children from one handle form
fan-out. Pass multiple parent handles to form fan-in. A continuation trigger
controls release: `Success` requires all parents to succeed, `Failure` requires
terminal parents with at least one failure, and `Complete` accepts any terminal
outcome. Unsatisfied conditional continuations and ineligible descendants become
terminal `Skipped` records; skipped branches do not fail an otherwise successful
batch.

Once commit begins, a network or storage error can leave the outcome unknown.
Do not reuse the closed batch. Check for duplicates in application code before
building another graph.

`IBatchScheduler.CancelAsync(BatchHandle)` durably cancels every non-terminal
member of a committed batch. It does not forcibly stop handler code already
running. If that handler finishes later, its result cannot replace the recorded
cancellation.

A running job whose request implements `IJobRequest` receives `JobDetails`.
Generated scheduling can add work beside current continuations, before them, or
detached from the batch. Expansion is valid only during the active attempt and
requires graph capability except for detached work.

Monitor with `IBatchMonitor` or the secured dashboard graph views.

## Sources

- Immediate.Dev: `Immediate.Jobs/batches-and-continuations.md`
- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/dashboard-and-monitoring.md`
- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
