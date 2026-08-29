---
name: test-job
description: Test Immediate.Jobs declarations, scheduling, cancellation, retries, timing, context, recurring work, and workflow graphs with the testing harness and captured storage writes. Use test-storage-provider for custom storage.
---

# Test an Immediate job

Prove persisted and execution behavior without relying on real time or a live worker race.

## Workflow

1. Verify that `Immediate.Jobs.Testing` is compatible with the restored core package.
2. Identify whether the test needs full pipeline execution or only inspection of captured storage writes.
3. Read [testing-patterns.md](references/testing-patterns.md).
4. Configure `JobTestHarness` with the same generated handler/job registration and required dependencies as production, but do not call `ConfigureStorage`; the harness installs in-memory storage and fake time. Create an async service scope before resolving a generated scheduler because schedulers are scoped and the harness validates scopes.
5. Use its fake time provider and drain methods for delayed, retry, timeout, and recurring behavior.
6. Assert the enqueued record before draining when schedule shape matters; query the durable record or graph after execution.
7. Inspect `harness.Captures` when the subject only needs to request work. Use `FindJob`, `FindBatch`, or the ordered capture snapshots, and query durable state when cancellation or execution matters.
8. Exercise idempotency or retry behavior explicitly for side-effecting jobs.
9. Build and run the focused tests, then run the relevant project suite.

## Guardrails

- Do not use `Task.Delay`, wall-clock sleeps, or timing races when fake time can drive the runtime deterministically.
- Do not substitute direct handler invocation when the behavior pipeline, serialization, restored context, or retry boundary is under test.
- Do not mistake a captured storage write for proof that a worker can deserialize and execute it.
- Do not combine incompatible versions of core, providers, and testing helpers.
- Do not use this workflow to claim a custom `IJobStorage` is correct; use `$immediate-jobs:test-storage-provider` and its packaged conformance cases.

## Handoff

Report the tested boundary, harness registrations, time advancement, record/graph assertions, retry or idempotency evidence, and test results.
