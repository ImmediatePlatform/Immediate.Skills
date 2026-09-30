# Storage matrix

| Provider | Durable | Distributed | Recurring | Graph | Fair groups | Replica |
| --- | --- | --- | --- | --- | --- | --- |
| In-memory | No | No | Yes | Yes | Yes | No |
| EF Core SQL | Yes | Optional | Yes | Yes | Yes | Yes |
| LinqToDB SQL | Yes | Optional | Yes | Yes | Yes | Yes |
| Redis | Yes | Always | Yes | No | No | No |

Provider and process mode are separate choices. `InMemory` keeps work only in
the current process. `SingleServer` keeps the active queue in memory and copies
changes to durable SQL; exactly one scheduler process may use it. `Distributed`
uses durable storage as the shared source for one or more processes. Redis always
selects distributed mode. The number of worker processes or deployment replicas
is a host setting, not an Immediate.Jobs option.

Generated registration accepts tags and returns `IImmediateJobsBuilder`. Configure
runtime options, fair queues, storage, IDs, and health through separate fluent
operations:

```csharp
builder.Services.AddMyAppJobs(tags: ["worker"])
	.ConfigureWorkers(options => options.WorkerCount = 16)
	.UseFairQueues(options => options.Configure(fair =>
		fair.GroupRoundRobin = true))
	.ConfigureStorage(storage => storage
		.UseEntityFrameworkCore<JobsDbContext>()
		.UseDistributed())
	.AddHealthCheck(tags: ["ready"]);
```

`ConfigureWorkers` and `UseFairQueues` accept `OptionsBuilder<T>` callbacks. Bind
an explicit `IConfiguration` section with `Bind`, or resolve the registered
configuration with `BindConfiguration(sectionPath)`. `UseFairQueues` registers
`Enabled = true` before it invokes the callback. A bound `Enabled` value applies
afterward, so omit it or set it to `true` when fairness must remain enabled.
`ConfigureStorage` must be called exactly once; omitting it fails options
validation when the host starts.
Selecting a durable provider without `UseSingleServer` or `UseDistributed`
defaults to single-server mode. Built-in provider extensions target
`IImmediateJobsStorageBuilder`; applications do not construct their storage types
directly.

EF Core applications should normally own a dedicated jobs `DbContext`, call
`AddImmediateJobs` in model configuration, register it with
`AddDbContextFactory<TContext>`, and create/apply its migrations. The storage
extension resolves `IDbContextFactory<TContext>`. LinqToDB applications own
`DataOptions`, the database driver, and production schema upgrades. Redis may
own a connection created from configuration or use an application-owned
`IConnectionMultiplexer`; configure database and a stable prefix without braces.
`ConfigureRedis` accepts either a direct options callback or an
`OptionsBuilder<RedisJobStorageOptions>` callback for `IConfiguration` binding.

Worker options that matter for sizing:

| Option | Default | Meaning |
| --- | --- | --- |
| `WorkerCount` | `Clamp(ProcessorCount * 4, 8, 32)` | Workers per node; the parallel job limit. |
| `MaxAcquisitionCount` | same as `WorkerCount` | Running plus claimed-but-waiting jobs per node; raise it above `WorkerCount` to keep workers busy with a longer `PollingInterval`. Below `WorkerCount` it becomes the parallel limit. |
| `PollingInterval` | 1 second | Delay between acquisition passes. |
| `ServerTimeout` | 10 seconds | Heartbeat silence before a node is considered dead; heartbeats run every third. |
| `LeaseDuration` | 1 minute | Claim lease; renewed every third by a separate loop. |

`AddHealthCheck(name)` registers two checks with the same tags and failure
status: `{name}-storage` for provider connectivity and `{name}-service` for a
started worker with a heartbeat within `ServerTimeout`. Map a readiness endpoint
with a predicate for the tag. The service check reports the failure status until
the worker starts, and always reports healthy under `DisableWorkers()`. The
checks and worker use the same validated options; no extra options registration
is required. `DisableWorkers()` still initializes storage and merges code-defined
recurring schedules.

Schema changes in recent previews: the EF Core server table gained required
`ExpiresAt` and `Details` columns (indexed by `ExpiresAt`), so add a migration
after upgrading; LinqToDB now stores timestamps in date-and-time columns instead
of 64-bit integers, so recreate schemas created by an earlier preview.

Provider initialization is idempotent startup, not production migration. Keep
provider and core packages on compatible versions. A custom provider starts
with `IJobStorage`. Add `IRecurringJobStorage`, `IJobGraphStorage`,
`IFairQueueStorage`, or `IJobStorageReplica` only when every method follows that
interface's rules. Test the public DI registration with
`JobStorageConformanceSuite`; use `$immediate-jobs:test-storage-provider` for the
fixture workflow.

## Sources

- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/configuring-storage-providers.md`
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
- Immediate.Dev: `Immediate.Jobs/testing-jobs.md`
- Immediate.Dev: `Immediate.Jobs/api-reference.md`
- Immediate.Dev: `Immediate.Jobs/observability-and-health.md`
