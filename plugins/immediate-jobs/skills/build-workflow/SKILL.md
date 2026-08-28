---
name: build-workflow
description: Build Immediate.Jobs atomic batches, durable continuations, fan-out and fan-in graphs, delayed release, and runtime expansion. Use only with a verified SQL or in-memory graph-capable preview provider; Redis cannot execute these workflows.
---

# Build an Immediate job workflow

Persist dependency graphs atomically and make their failure and expansion behavior visible.

## Workflow

1. Verify the core/provider preview revisions and confirm `IJobGraphStorage` capability. Stop if the target uses Redis.
2. Model the graph, continuation triggers, post-release delays, idempotency keys, and expected cascade behavior before writing scheduling code. Decide which jobs must share the atomic batch write and which may be attached later as a separate durable continuation.
3. Read [workflow-graphs.md](references/workflow-graphs.md).
4. Import `Immediate.Jobs.Shared.Interfaces` and resolve scoped `IBatchScheduler` plus each generated job scheduler.
5. Begin and asynchronously dispose a batch. Add roots with synchronous `Enqueue` or `Schedule`, add dependencies with synchronous `ScheduleAfter`, then commit once. Prefer `RunAsync` when its commit-on-success shape fits.
6. Use one `BatchJobHandle` for a chain, several children for fan-out, and an `IReadOnlyList<BatchJobHandle>` for fan-in inside the open batch. Use `ScheduleAfterAsync` with durable `JobHandle` and `BatchHandle` parents outside it.
7. Select `Success`, `Failure`, or `Complete` explicitly. A continuation delay begins only after every parent reaches the required outcome.
8. For runtime expansion, implement `IJobRequest`, use the populated `JobDetails` only during the active attempt, and choose detached, beside, or before-existing-continuations semantics.
9. Test failure before commit and an unknown outcome after a commit error. Also cover graph shape, trigger and delay behavior, conditional `Skipped` branches, explicit cancellation, and `JobMonitor` output.

## Guardrails

- Do not use graph APIs with Redis; it supports queues and recurring schedules but not batches or continuations.
- Do not retry a `Batch` after commit starts. A transport failure can make the durable outcome unknown.
- Do not treat `ScheduleAfterAsync` after `CommitAsync` as part of the atomic batch write. Reconcile the second write when the workflow requires guaranteed attachment.
- Do not mix duplicate parents or handles from unrelated open batches.
- Do not read `BatchJobHandle.JobHandle` before the batch commits or pass a `BatchJobHandle` across the open-batch boundary.
- Do not use `JobDetails` outside its active execution attempt or treat batch disposal as an implicit commit.

## Handoff

Report provider capability, graph shape, continuation triggers and delays, commit/idempotency strategy, runtime expansion semantics, monitoring path, preview versions, and test evidence.
