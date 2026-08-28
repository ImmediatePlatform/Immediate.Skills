# Testing patterns

Use `JobTestHarness` for deterministic integration-style tests of scheduling,
serialization, the Immediate.Handlers pipeline, storage transitions, retries,
recurring materialization, and graph workflows. Configure its services with the
generated `Add...Handlers` and `Add...Jobs` methods plus application dependencies.
Do not chain `ConfigureStorage` in the harness callback; the harness installs its
own in-memory provider and `FakeTimeProvider` after application registration.
The harness builds its provider with scope validation. Resolve a generated
scheduler from `harness.Services.CreateAsyncScope()`, not from the root provider.

Typical operations include `AssertEnqueuedAsync<TPayload>`, `GetJobAsync`,
`QueryJobsAsync`, `DrainAsync`, and the two `AdvanceTimeAndDrainAsync` overloads.
Use `RunThroughPipelineAsync<TPayload>` when a test must exercise behaviors and
the generated invoker. Graph helpers cover atomic commit, continuation release,
cascade skipping, and cancellation. `Batches` is an `IBatchScheduler` from
`Immediate.Jobs.Shared.Interfaces`; job and execution records are under
`Immediate.Jobs.Shared.Apis`.

The harness puts `CapturingJobStorage` behind the production generated
schedulers. `harness.Captures.FindJob(handle)` returns a captured `JobRecord`;
its typed identifier is `JobHandle`. Other snapshots cover continuations,
batches, dynamic additions, recurring mutations, and materializations. `Clear()`
clears the capture log without deleting durable in-memory state. Captures do not
prove handler execution, so retain at least one drained harness test for critical
jobs.

Test at-least-once consequences deliberately: arrange a retryable failure,
advance fake time through the retry, and assert that the application-side
idempotency mechanism prevents duplicate effects.

## Sources

- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
- Immediate.Dev: `Immediate.Jobs/delivery-guarantees.md`
- Immediate.Dev: `Immediate.Jobs/execution-context-and-behaviors.md`
- Immediate.Dev: `Immediate.Jobs/batches-and-continuations.md`
