# Testing patterns

Use `JobTestHarness` for deterministic integration-style tests of scheduling,
serialization, the Immediate.Handlers pipeline, storage transitions, retries,
recurring materialization, and graph workflows. Configure its services with the
generated `Add...Handlers` and `Add...Jobs` methods plus application dependencies.

Typical operations include asserting that a typed scheduler persisted work,
calling `DrainAsync`, advancing fake time with `AdvanceTimeAndDrainAsync`, and
querying records or graphs after execution. Use
`RunThroughPipelineAsync<TPayload>` when the
test must exercise behaviors and the generated invoker.

Use `CaptureOnlyJobScheduler` when a unit under test only needs to request
background work. Inspect `Captures` or `Last` and clear them between phases.
Use the recurring capture equivalent for dynamic schedule commands. Capture
helpers do not prove serialization or worker execution, so retain at least one
harness test for critical jobs.

Test at-least-once consequences deliberately: arrange a retryable failure,
advance fake time through the retry, and assert that the application-side
idempotency mechanism prevents duplicate effects.

## Sources

- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
- Immediate.Dev: `Immediate.Jobs/delivery-guarantees.md`
- Immediate.Dev: `Immediate.Jobs/execution-context-and-behaviors.md`
- Immediate.Dev: `Immediate.Jobs/batches-and-continuations.md`
