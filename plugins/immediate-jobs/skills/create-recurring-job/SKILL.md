---
name: create-recurring-job
description: Create declarative or dynamic Immediate.Jobs recurring schedules and trigger payloadless jobs by type or stable name. Use for Cron, IANA time zones, startup reconciliation, overlap policy, or NodaTime APIs after verifying compatible preview packages.
---

# Create an Immediate recurring job

Define repeatable schedules while keeping persisted identity, reconciliation, and overlap semantics explicit.

## Workflow

1. Verify the checked-out Immediate.Jobs preview versions and the intended provider's recurring capability.
2. Confirm that the job is payloadless. If each occurrence needs data, have it load current data by stable identifiers or reconsider the design.
3. Read [recurring-patterns.md](references/recurring-patterns.md).
4. Use code-defined Cron metadata for deployment-owned schedules and the generated typed scheduler for application-managed schedules. The scheduler persists its generated queue name with each schedule. Use the root-namespace `RecurringJobs` dispatcher when infrastructure must trigger a payloadless job by stable name.
5. Set an explicit stable job name, validate five- or six-field Cron syntax, and use an IANA time-zone ID; UTC is the default.
6. Select overlap behavior—skip, queue, or concurrent—based on duration and business correctness.
7. With a recurring-capable provider, account for startup reconciliation: changed code schedules recalculate their next run, removed code schedules are deleted, and dynamic schedules remain.
8. Use the NodaTime companion only after its matching registration is present on every worker.
9. Test reconciliation, queue preservation, next-run calculation, trigger-now behavior, overlap, pause/remove behavior where applicable, and time-zone edges. For name-based dispatch, also test unknown names and tag-filtered registration.

## Guardrails

- Do not put Cron on a job with a payload request.
- Do not use Windows time-zone identifiers; persisted schedules use IANA identifiers.
- Do not assume a startup reconciliation will remove dynamically managed schedules.
- Do not pass a dynamic schedule name to `RecurringJobs.TriggerNowAsync`; it accepts the job's case-sensitive `[Job(Name = ...)]` identity and does not return a `JobHandle`.
- Do not call generated registration without tags when the host must exclude tagged jobs; no tags registers every job.
- Do not silently change a production job name; recurring records and executions reference it.

## Handoff

Report the applicable items: ownership mode, stable name, host tags, Cron and time zone, overlap policy, reconciliation consequences, provider support, preview revisions, and deterministic test evidence.
