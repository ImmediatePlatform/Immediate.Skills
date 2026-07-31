---
name: configure-storage
description: Choose and configure Immediate.Jobs in-memory, Entity Framework Core, LinqToDB, Redis, or custom storage with the correct topology, capabilities, schema ownership, and lifecycle. Use only against mutually compatible restorable preview provider and core packages.
---

# Configure Immediate job storage

Choose durability and capabilities together, then make schema and connection ownership explicit.

## Workflow

1. Verify that every Immediate.Jobs core, provider, dashboard, NodaTime, and testing package restores at the same compatible preview revision.
2. Determine durability, process count, failover, graph, recurring, and fair-queue requirements.
3. Read [storage-matrix.md](references/storage-matrix.md).
4. Choose in-memory for disposable single-process work, single-server SQL for one durable process, distributed SQL for scale-out/full capabilities, or Redis for distributed queue and recurring work without graphs or fair groups.
5. Configure the provider and topology explicitly. Never point two processes at the same single-server replica.
6. For EF Core, prefer an application-owned dedicated jobs `DbContext`, map the jobs model, and own migrations. For LinqToDB, own `DataOptions`, the driver, and production schema evolution.
7. For Redis, decide connection ownership, database, and key prefix; avoid braces in the prefix.
8. Register health checks, exercise provider initialization, and test the required capability—not just connectivity.
9. Document migration, rollback, backup, and preview upgrade ownership.

## Guardrails

- Do not use `EnsureCreated` or the LinqToDB fresh-schema helper as a production migration strategy.
- Do not promise batches, continuations, or fair groups on Redis.
- Do not select single-server mode for multiple processes or high-availability failover.
- Do not implement a custom provider unless its atomic claim, lease, recurring, graph, paging, initialization, and disposal contracts can be honored.

## Handoff

Report topology, provider/capabilities, package revisions, schema and connection owner, migration path, health check, unsupported features, and verification evidence.
