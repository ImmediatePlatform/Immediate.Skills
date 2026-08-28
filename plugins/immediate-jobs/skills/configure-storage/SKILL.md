---
name: configure-storage
description: Configure Immediate.Jobs in-memory, Entity Framework Core, LinqToDB, Redis, or custom storage through the fluent builder. Use when choosing process mode, supported features, schema ownership, or lifecycle. Requires compatible preview packages.
---

# Configure Immediate job storage

Choose durability and capabilities together, then make schema and connection ownership explicit.

## Workflow

1. Verify that every Immediate.Jobs core, provider, dashboard, NodaTime, and testing package restores at the same compatible preview revision.
2. Determine durability, process count, failover, graph, recurring, and fair-queue requirements.
3. Read [storage-matrix.md](references/storage-matrix.md).
4. Choose in-memory for disposable single-process work, single-server SQL for one durable process, distributed SQL for scale-out/full capabilities, or Redis for distributed queue and recurring work without graphs or fair groups.
5. Call generated `AddXxxJobs(tags)`, which returns `IImmediateJobsBuilder`. Configure worker or fair-queue options in code or bind their `OptionsBuilder<T>` callbacks to `IConfiguration`. When binding fair queues, verify that an explicit `Enabled` value does not disable them. Chain `ConfigureStorage` exactly once, select the provider, and choose `UseSingleServer` or `UseDistributed`; Redis chooses distributed mode itself.
6. For EF Core, prefer an application-owned dedicated jobs `DbContext`, map the jobs model, and own migrations. For LinqToDB, own `DataOptions`, the driver, and production schema evolution.
7. For Redis, decide connection ownership, database, and key prefix; avoid braces in the prefix. Configure options directly or bind `RedisJobStorageOptions` from `IConfiguration`.
8. Chain `AddHealthCheck` and map a tag-filtered readiness endpoint. Exercise provider initialization and the required capability, not just connectivity.
9. For a custom provider, use `$immediate-jobs:test-storage-provider` to run the packaged tests that match its supported features.
10. Document migration, rollback, backup, and preview upgrade ownership.

## Guardrails

- Do not use `EnsureCreated` or the LinqToDB fresh-schema helper as a production migration strategy.
- Do not promise batches, continuations, or fair groups on Redis.
- Do not select single-server mode for multiple processes or high-availability failover.
- Do not omit `ConfigureStorage`, call it twice, or instantiate built-in provider implementation types directly; use their storage-builder extensions.
- Do not implement a custom provider unless its atomic claim, lease, recurring, graph, paging, initialization, and disposal contracts can be honored.

## Handoff

Report topology, provider/capabilities, bound configuration sections, package revisions, schema and connection owner, migration path, health check, unsupported features, and verification evidence.
