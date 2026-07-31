---
name: create-recurring-job
description: Create declarative or dynamic Immediate.Jobs recurring schedules with payloadless jobs, Cron and IANA time zones, startup reconciliation, overlap policy, and optional NodaTime APIs. Use only after verifying a compatible restorable Immediate.Jobs preview package set.
---

# Create an Immediate recurring job

Define repeatable schedules while keeping persisted identity, reconciliation, and overlap semantics explicit.

## Workflow

1. Verify the checked-out Immediate.Jobs preview versions and the intended provider's recurring capability.
2. Confirm that the job is payloadless. If each occurrence needs data, have it load current data by stable identifiers or reconsider the design.
3. Read [recurring-patterns.md](references/recurring-patterns.md).
4. Choose code-defined Cron metadata for a schedule owned by deployment, or the generated dynamic recurring scheduler for application-managed schedules.
5. Set an explicit stable job name, validate five- or six-field Cron syntax, and use an IANA time-zone ID; UTC is the default.
6. Select overlap behavior—skip, queue, or concurrent—based on duration and business correctness.
7. Account for startup reconciliation: changed code schedules recalculate their next run, removed code schedules are deleted, and dynamic schedules remain.
8. Use the NodaTime companion only after its matching registration is present on every worker.
9. Test reconciliation, next-run calculation, trigger-now behavior, overlap, pause/remove behavior where applicable, and time-zone edges.

## Guardrails

- Do not put Cron on a job with a payload request.
- Do not use Windows time-zone identifiers; persisted schedules use IANA identifiers.
- Do not assume a startup reconciliation will remove dynamically managed schedules.
- Do not silently change a production job name; recurring records and executions reference it.

## Handoff

Report ownership mode, stable name, Cron and time zone, overlap policy, reconciliation consequences, provider support, preview revisions, and deterministic test evidence.
