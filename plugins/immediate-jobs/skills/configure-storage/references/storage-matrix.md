# Storage matrix

| Provider | Durable | Distributed | Recurring | Graph | Fair groups |
| --- | --- | --- | --- | --- | --- |
| In-memory | No | No | Yes | Yes | Yes |
| EF Core SQL | Yes | Optional | Yes | Yes | Yes |
| LinqToDB SQL | Yes | Optional | Yes | Yes | Yes |
| Redis | Yes | Always | Yes | No | No |

Topology and provider are separate choices. `InMemory` makes process memory
authoritative. `SingleServer` uses private memory with a synchronous SQL replica
and must have exactly one process. `Distributed` coordinates durable work across
one or more processes. Redis always selects distributed mode.

EF Core applications should normally own a dedicated jobs `DbContext`, call
`AddImmediateJobs` in model configuration, and create/apply its migrations.
LinqToDB applications own `DataOptions`, the database driver, and production
schema upgrades. Redis may own a connection created from configuration or use
an application-owned `IConnectionMultiplexer`; configure database and a stable
prefix without braces.

Provider initialization is idempotent startup, not production migration. Keep
provider and core packages on the same preview revision.

## Sources

- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/configuring-storage-providers.md`
- Immediate.Dev: `Immediate.Jobs/registration-and-hosting.md`
- Immediate.Dev: `Immediate.Jobs/api-reference.md`
