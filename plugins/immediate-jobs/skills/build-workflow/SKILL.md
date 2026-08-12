---
name: build-workflow
description: Build Immediate.Jobs atomic batches, chains, fan-out and fan-in continuations, failure triggers, and runtime graph expansion. Use only with a verified SQL or in-memory graph-capable Immediate.Jobs preview provider; Redis cannot execute these workflows.
---

# Build an Immediate job workflow

Persist dependency graphs atomically and make their failure and expansion behavior visible.

## Workflow

1. Verify the core/provider preview revisions and confirm `IJobGraphStorage` capability. Stop if the target uses Redis.
2. Model the graph, continuation triggers, idempotency keys, and expected cascade behavior before writing scheduling code.
3. Read [workflow-graphs.md](references/workflow-graphs.md).
4. Import `Immediate.Jobs.Shared.Interfaces` and resolve scoped `IBatchScheduler` plus each generated job scheduler.
5. Begin and asynchronously dispose a batch; add roots and continuations, then commit once. Prefer `RunAsync` when its commit-on-success shape fits.
6. Use a single handle for a chain, several children for fan-out, and a span of parent handles for fan-in.
7. Select `Success`, `Failure`, or `Complete` triggers explicitly.
8. For runtime expansion, implement `IJobRequest`, use the populated `JobDetails` only during the active attempt, and choose detached, beside, or before-existing-continuations semantics.
9. Test failure before commit and an unknown outcome after a commit error. Also cover graph shape, trigger behavior, conditional `Skipped` branches, explicit cancellation, and monitoring output.

## Guardrails

- Do not use graph APIs with Redis; it supports queues and recurring schedules but not batches or continuations.
- Do not retry a `Batch` after commit starts. A transport failure can make the durable outcome unknown.
- Do not mix duplicate parents or handles from unrelated open batches.
- Do not use `JobDetails` outside its active execution attempt or treat batch disposal as an implicit commit.

## Handoff

Report provider capability, graph shape, continuation triggers, commit/idempotency strategy, runtime expansion semantics, monitoring path, preview versions, and test evidence.
