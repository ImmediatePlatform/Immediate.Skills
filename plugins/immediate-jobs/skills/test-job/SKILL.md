---
name: test-job
description: Test Immediate.Jobs declarations, scheduling, retries, timing, context, recurring work, and workflow graphs with the preview testing harness or capture-only schedulers. Use when adding deterministic job tests against an explicitly verified Immediate.Jobs.Testing preview version.
---

# Test an Immediate job

Prove persisted and execution behavior without relying on real time or a live worker race.

## Workflow

1. Verify that `Immediate.Jobs.Testing` matches the restored core preview revision.
2. Identify whether the test needs full pipeline execution or only scheduling capture.
3. Read [testing-patterns.md](references/testing-patterns.md).
4. Configure `JobTestHarness` with the same generated handler/job registration and required dependencies as production.
5. Use its fake time provider and drain methods for delayed, retry, timeout, and recurring behavior.
6. Assert the enqueued record before draining when schedule shape matters; query the durable record or graph after execution.
7. Use capture-only job or recurring schedulers for unit tests whose subject merely requests work and should not run it.
8. Exercise idempotency or retry behavior explicitly for side-effecting jobs.
9. Build and run the focused tests, then run the relevant project suite.

## Guardrails

- Do not use `Task.Delay`, wall-clock sleeps, or timing races when fake time can drive the runtime deterministically.
- Do not substitute direct handler invocation when the behavior pipeline, serialization, restored context, or retry boundary is under test.
- Do not mistake a captured scheduling request for proof that a worker can deserialize and execute it.
- Do not combine mismatched preview revisions of core, providers, and testing helpers.

## Handoff

Report the tested boundary, harness registrations, time advancement, record/graph assertions, retry or idempotency evidence, and test results.
