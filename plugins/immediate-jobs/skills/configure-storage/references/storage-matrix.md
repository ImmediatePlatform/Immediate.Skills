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
selects distributed mode.

Generated registration accepts tags and returns `ImmediateJobsBuilder`. Configure
runtime options, fair queues, storage, IDs, and health through separate fluent
operations:

```csharp
services.AddMyAppJobs(tags: ["worker"])
	.Configure(options => options.MaxParallelJobs = 16)
	.UseFairQueues(fair => fair.GroupRoundRobin = true)
	.ConfigureStorage(storage => storage
		.UseEntityFrameworkCore<JobsDbContext>()
		.UseDistributed())
	.AddHealthCheck(tags: ["ready"]);
```

`Configure` also accepts an `IConfiguration` section or section path.
`UseFairQueues` has matching overloads and always enables fairness.
`ConfigureStorage` may be called once. Omitting it selects in-memory storage.
Selecting a durable provider without `UseSingleServer` or `UseDistributed`
defaults to single-server mode. Built-in provider extensions target
`ImmediateJobsStorageBuilder`; applications do not construct their storage types
directly.

EF Core applications should normally own a dedicated jobs `DbContext`, call
`AddImmediateJobs` in model configuration, register it with
`AddDbContextFactory<TContext>`, and create/apply its migrations. The storage
extension resolves `IDbContextFactory<TContext>`. LinqToDB applications own
`DataOptions`, the database driver, and production schema upgrades. Redis may
own a connection created from configuration or use an application-owned
`IConnectionMultiplexer`; configure database and a stable prefix without braces.

Map a readiness endpoint with a predicate for the tag passed to `AddHealthCheck`.
Map `HealthStatus.Degraded` to HTTP 503 if readiness must stay closed until the
scheduler starts. At source revision `ee5f51d`, also bridge the options registration
until the health-check constructor is fixed:

```csharp
services.AddSingleton<ImmediateJobsOptions>(provider =>
	provider.GetRequiredService<IOptions<ImmediateJobsOptions>>().Value);
```

Provider initialization is idempotent startup, not production migration. Keep
provider and core packages on the same preview revision. A custom provider starts
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
