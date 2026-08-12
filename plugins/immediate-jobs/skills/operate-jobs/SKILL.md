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
4. Call `AddImmediateJobsDashboard` before building the app. Map it under an operator-only path with a named authorization policy. Protect every UI, JSON, SSE, retry, run-now, cancel, delete, pause, trigger, and graph action.
5. Export the `Immediate.Jobs` activity source and meter. Include structured logging scopes.
6. Register the scheduler/provider health check and map it to the appropriate readiness surface.
7. Add trace/log links using the exact retained execution when a link targets one attempt; use the job ID for links that span retries. Hide links when required identifiers are absent.
8. Import `Immediate.Jobs.Shared.Interfaces`; use scoped `IJobMonitor` and, only with graph capability, `IBatchMonitor` for custom status endpoints with authorization and paging.
9. Test access and policy enforcement outside development. Also cover provider outages, mutation preconditions, unsupported graph routes, SSE reconnection, and redaction.

## Guardrails

- Do not map an unprotected production dashboard. Without explicit authorization, non-development requests are denied by design.
- Do not expose job payloads, exceptions, identifiers, or mutation endpoints to ordinary application users.
- Do not interpret `queue.depth` or `workers.active` gauges as authoritative cluster totals; use provider monitoring snapshots.
- Do not expose graph operations for a provider without graph capability.

## Handoff

Report the authorization policy, mapped prefix, exposed controls, telemetry exporters/links, health semantics, sensitive-data treatment, provider limitations, preview revisions, and tests.
