---
name: test-storage-provider
description: Test a custom Immediate.Jobs IJobStorage implementation with the packaged storage behavior catalog. Use for queue, recurring, graph, fair-queue, or replica provider fixtures; use test-job for application jobs.
---

# Test an Immediate job storage provider

Run the same storage behavior tests used by the built-in providers. The fixture
can use any test framework or provider implementation.

## Workflow

1. Verify that `Immediate.Jobs.Testing`, core, and provider packages restore at compatible versions.
2. Inspect the provider's normal public DI registration and the capability interfaces implemented by the resolved storage.
3. Read [conformance-suite.md](references/conformance-suite.md).
4. Declare one exact `StorageCapabilities` set. Include `Queue`. Add `Recurring`, `Graph`, `FairQueues`, or `Replica` only when the resolved type implements the matching public interface.
5. Build a fresh service provider per case. Register `Microsoft.Extensions.Time.Testing.FakeTimeProvider` as `TimeProvider` and resolve exactly one `IJobStorage`. Give each case a separate database, schema, key prefix, or similar data boundary.
6. Create one visible parameterized test case for every object returned by `JobStorageConformanceSuite.GetCases`. Store the case's `PersistedJobState` (jobs, batches, edges, and recurring schedules) in the isolated backend, then pass the service provider to `RunAsync`.
7. Keep fixtures safe for parallel execution. When cleanup needs the connection and backend identifier, return a wrapper that owns them along with the service provider. Dispose services before deleting the isolated data.
8. Keep provider-specific tests for schema upgrades, SQL or Redis details, connection ownership, and simulated backend failures.
9. Run the catalog on every supported provider and runtime combination. Report each failing case name, the expected flags, and the interfaces found at runtime.

## Guardrails

- Do not ignore `PersistedJobState`; cases that restore existing graphs or schedules fail without it.
- Do not skip individual packaged cases or advertise fewer capabilities than the resolved storage implements.
- Do not construct internal built-in storage types or use `InternalsVisibleTo`; test the public registration path.
- Do not share backend data between cases or use wall-clock sleeps for lease, retention, heartbeat, or recurring behavior.
- Do not advertise `Replica` for in-memory or Redis, or graph/fair-queue support for Redis.
- Do not treat a passing catalog as coverage for migrations, database-specific behavior, scripts, or connection lifecycle.

## Handoff

Report package revisions, provider registration, capability flags, data isolation,
fake-clock setup, test-runner setup, catalog results, provider-specific tests kept,
and any failing case names.
