# Storage conformance suite

The public test API is under `Immediate.Jobs.Testing`. Storage contracts and
capability flags are under `Immediate.Jobs.Shared.Storage`.

| Implemented interface | Capability flag | Behavior tested |
| --- | --- | --- |
| `IJobStorage` | `Queue` | Lifecycle, enqueue/acquire, leases, executions, queries, monitoring, mutations, retention, health, and disposal |
| `IRecurringJobStorage` | `Recurring` | Schedule lifecycle, `MergeRecurringSchedulesListAsync` startup merge, due scanning, deduplication, materialization with overlap dependencies, and cleanup |
| `IJobGraphStorage` | `Graph` | Atomic batches, edges, triggers, delayed release, fan-in, expansion, cancellation, deletion, and purge |
| `IFairQueueStorage` | `FairQueues` | Group rotation, noisy-neighbor ordering, ordinary-order fallback, and concurrent claims |
| `IJobStorageReplica` | `Replica` | Exact-handle acquisition, stale-worker protection, execution history, and restored records |

`GetCases` always includes `Queue` and adds optional suites from one flag set.
Each `RunAsync` resolves exactly one `IJobStorage`. Before checking behavior, it
confirms that the implemented interfaces match the full flag set.

```csharp
using Immediate.Jobs.Shared.Storage;
using Immediate.Jobs.Testing;
using Microsoft.Extensions.Time.Testing;

private const StorageCapabilities Capabilities =
	StorageCapabilities.Queue |
	StorageCapabilities.Recurring;

public static TheoryData<JobStorageConformanceTestCase> Cases =>
	[.. JobStorageConformanceSuite.GetCases(Capabilities)];

[Theory]
[MemberData(nameof(Cases))]
public async Task StorageConforms(JobStorageConformanceTestCase testCase)
{
	await using var fixture = await AcmeStorageFixture.CreateAsync();
	await fixture.SeedAsync(testCase.PersistedJobState);
	await testCase.RunAsync(fixture.Services);
}
```

`PersistedJobState` lists the `Jobs`, `Batches`, `Edges`, and
`RecurringSchedules` a case expects to exist before it runs, such as an existing
batch graph to restore. Most cases have empty lists. The built-in providers
expose `LoadPersistedJobState` for this; a custom fixture can insert rows
directly.

Provider contracts to honor beyond the older surface:
`QueryNonCompletedJobsAsync(jobName)` returns every non-final job with that name
(used by overlap policies); `MergeRecurringSchedulesListAsync` receives the full
code-defined list once per start and must add, preserve unchanged, recalculate
changed (keeping `LastRunAt` and paused state), promote matching dynamic
schedules, and remove missing code schedules in one operation; and
`MaterializeRecurringAsync` must save its optional `dependencies` edges with the
new `AwaitingContinuation` run.

Give every case separate backend data by using a new database, schema, key prefix,
or similar boundary. `FakeTimeProvider` is in `Microsoft.Extensions.Time.Testing`
and comes from the `Microsoft.Extensions.TimeProvider.Testing` package. Register
it as `TimeProvider` before using the provider's public registration extension.
Build the service provider with scope and build validation when possible. The
provider must support concurrent calls against that data.

When cleanup needs the connection and backend identifier, have the fixture wrap
them together with the service provider as shown above. Dispose the provider
before deleting its isolated data. This keeps cleanup possible without sharing
data between cases.

Expose cases separately in xUnit, NUnit, MSTest, or another runner. Do not wrap
them in one combined test: the stable case name shows exactly what failed.
The catalog deliberately has no dependency on a runner, ORM, driver,
Testcontainers, or Redis client.

Built-in capability claims are:

- in-memory: queue, recurring, graph, and fair queues;
- EF Core and LinqToDB: queue, recurring, graph, fair queues, and replica;
- Redis: queue and recurring.

## Sources

- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/api-reference.md`
