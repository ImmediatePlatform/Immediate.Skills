---
name: operate-jobs
description: Secure, monitor, and operate Immediate.Jobs with the dashboard, programmatic monitors, OpenTelemetry, structured logs, health checks, retry and recurring controls, and batch graph actions. Use only after verifying the complete preview package and provider baseline.
---

# Operate Immediate jobs

Expose enough operational control to diagnose work without leaking payloads or overstating local telemetry.

## Workflow

1. Verify compatible Jobs, provider, and dashboard preview revisions plus the storage capabilities in use.
2. Identify operators, sensitive payload/error fields, authorization policy, telemetry destinations, retention, and incident actions.
3. Read [operations-patterns.md](references/operations-patterns.md).
4. Chain `AddImmediateJobsDashboard` from generated job registration, configure it directly or bind its `OptionsBuilder<T>` callback to `IConfiguration` before building the app, and map it under an operator-only path with a named authorization policy. Protect every UI, JSON, SSE, retry, run-now, cancel, delete, pause, trigger, and graph action.
5. Export the `Immediate.Jobs` activity source and meter. Include structured logging scopes.
6. Register the scheduler/provider health check and map it to the appropriate readiness surface.
7. Add trace/log links using the exact retained execution when a link targets one attempt. Use `context.Job.JobHandle` for links that span retries and read its `Value` only when the destination needs a string.
8. Use scoped `JobMonitor` for reads and management commands. Depend on its read-only `IJobMonitor` interface when a component needs no mutations. Batch reads return `null` without graph capability.
9. Test access and policy enforcement outside development. Also cover provider outages, mutation preconditions, unsupported graph routes, SSE reconnection, and redaction.

## Guardrails

- Do not map an unprotected production dashboard. Without explicit authorization, non-development requests are denied by design.
- Do not expose job payloads, exceptions, identifiers, or mutation endpoints to ordinary application users.
- Do not interpret `queue.depth` or `workers.active` gauges as authoritative cluster totals; use provider monitoring snapshots.
- Do not expose graph operations for a provider without graph capability.

## Handoff

Report the authorization policy, mapped prefix, exposed controls, telemetry exporters/links, health semantics, sensitive-data treatment, provider limitations, preview revisions, and tests.
