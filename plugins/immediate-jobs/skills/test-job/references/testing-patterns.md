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

`harness.Storage` is the `CapturingJobStorage` behind the production generated
schedulers (the former `Captures` property was removed).
`harness.Storage.FindJob(handle)` returns a captured `JobRecord`; its typed
identifier is `JobHandle`. Other snapshots cover continuations, batches, dynamic
additions, recurring mutations, and materializations (including any `Queue`
overlap dependencies), in call order. `RecurringSchedules` is a dictionary of the
saved schedules keyed by name. `Clear()` clears the capture log without deleting
durable in-memory state. `LoadPersistedJobState` seeds jobs, batches, edges, and
recurring schedules before a test. The class is unsealed with virtual storage
methods, so a test can derive from it to inject failures or delays. Captures do
not prove handler execution, so retain at least one drained harness test for
critical jobs.

Pass `Action<ImmediateJobsOptions>` as the last constructor argument to change
worker options; the harness uses one worker by default. `ResetScheduler()`
rebuilds `Services`, `Batches`, and `Scheduler` while keeping `Storage` and
`TimeProvider`, simulating a restart:

```csharp
await harness.DrainAsync(token);
harness.TimeProvider.Advance(TimeSpan.FromMinutes(17));
harness.ResetScheduler();
await harness.DrainAsync(token);
Assert.Single(
	harness.Storage.RecurringMaterializations,
	m => m.Schedule.Name == "cleanup-sessions" && m.Job.State == JobState.Pending);
```

The first drain after a reset merges code-defined schedules again and applies
each job's `MisfireHandlingMode` to occurrences missed while time advanced.

Test at-least-once consequences deliberately: arrange a retryable failure,
advance fake time through the retry, and assert that the application-side
idempotency mechanism prevents duplicate effects.

## Sources

- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
- Immediate.Dev: `Immediate.Jobs/delivery-guarantees.md`
- Immediate.Dev: `Immediate.Jobs/execution-context-and-behaviors.md`
- Immediate.Dev: `Immediate.Jobs/batches-and-continuations.md`
