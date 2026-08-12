# Storage conformance suite

The public test API is under `Immediate.Jobs.Testing`. Storage contracts and
capability flags are under `Immediate.Jobs.Shared.Storage`.

| Implemented interface | Capability flag | Behavior tested |
| --- | --- | --- |
| `IJobStorage` | `Queue` | Lifecycle, enqueue/acquire, leases, executions, queries, monitoring, mutations, retention, health, and disposal |
| `IRecurringJobStorage` | `Recurring` | Schedule lifecycle, reconciliation, due scanning, deduplication, materialization, and cleanup |
| `IJobGraphStorage` | `Graph` | Atomic batches, edges, triggers, fan-in, expansion, cancellation, deletion, and purge |
| `IFairQueueStorage` | `FairQueues` | Group rotation, noisy-neighbor ordering, ordinary-order fallback, and concurrent claims |
| `IJobStorageReplica` | `Replica` | Exact-ID acquisition, stale-worker protection, execution history, and restored records |

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
	await testCase.RunAsync(fixture.Services);
}
```

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
