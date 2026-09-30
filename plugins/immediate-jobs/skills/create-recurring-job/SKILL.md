---
name: create-recurring-job
description: Create declarative or dynamic Immediate.Jobs recurring schedules and trigger payloadless jobs by type or saved schedule name. Use for Cron expressions, RFC 5545 recurrence rules, IANA time zones, startup schedule merging, missed-run (misfire) handling, overlap policy, or NodaTime APIs.
---

# Create an Immediate recurring job

Define repeatable schedules while keeping persisted identity, startup merging, missed-run, and overlap semantics explicit.

## Workflow

1. Verify compatible Immediate.Jobs package versions and the intended provider's recurring capability. `OverlapPolicy.Queue` also needs graph capability.
2. Confirm that the job is payloadless. If each occurrence needs data, have it load current data by stable identifiers or reconsider the design.
3. Read [recurring-patterns.md](references/recurring-patterns.md).
4. Use code-defined `Cron` metadata for deployment-owned schedules and the generated typed scheduler for application-managed schedules. The scheduler persists its generated queue name with each schedule. Use `JobMonitor.TriggerRecurringAsync` when infrastructure must trigger a saved schedule by name.
5. Set an explicit stable job name. Use a five- or six-field Cron expression, a supported macro, or an RFC 5545 recurrence rule without `COUNT` or `UNTIL`, and an IANA time-zone ID; UTC is the default.
6. Select `MisfireHandlingMode`—`EnqueueOne` (default), `EnqueueAll`, or `EnqueueNone`—based on whether missed occurrences must each run, run once, or be dropped.
7. Select overlap behavior—skip, queue, or concurrent—based on duration and business correctness. Both `Skip` and `Queue` consider every unfinished run of the job, including manual triggers.
8. With a recurring-capable provider, account for the startup merge: unchanged code schedules keep their next run, last run, and paused state; changed ones recalculate the next run but stay paused if paused; a dynamic schedule with the same name becomes code-defined; removed code schedules are deleted; other dynamic schedules remain.
9. Use the NodaTime companion only after its matching registration is present on every worker.
10. Test the startup merge, queue preservation, next-run calculation, missed runs across a simulated restart, trigger-now behavior, overlap, pause/remove behavior where applicable, and time-zone edges.

## Guardrails

- Do not put Cron on a job with a payload request.
- Do not use Windows time-zone identifiers; persisted schedules use IANA identifiers.
- Do not use a recurrence rule that ends; `COUNT` or `UNTIL` is an analyzer error (`IJOB0007`) and throws for dynamic schedules.
- Do not use `OverlapPolicy.Queue` on Redis or other storage without graph capability; each due run fails and logs `RecurringMaterializationFailed`.
- Do not assume startup merging will remove dynamically managed schedules, and do not reuse a dynamic schedule name for a new code schedule unless the promotion is intended.
- Do not reference a generated `RecurringJobs` dispatcher; it no longer exists.
- Do not call generated registration without tags when the host must exclude tagged jobs; no tags registers every job.
- Do not silently change a production job name; recurring records and executions reference it.

## Handoff

Report the applicable items: ownership mode, stable name, host tags, Cron or recurrence rule and time zone, misfire mode, overlap policy, startup-merge consequences, provider capabilities, package versions, and deterministic test evidence.
