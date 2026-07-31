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
4. Add the dashboard package and map it beneath an administrative prefix with a named authorization policy. Treat every UI, JSON, SSE, retry, delete, pause, trigger, and graph action as privileged.
5. Export the `Immediate.Jobs` activity source and meter. Include structured logging scopes.
6. Register the scheduler/provider health check and map it to the appropriate readiness surface.
7. Add trace/log links using persisted execution metadata; hide links when the latest attempt lacks suitable identifiers.
8. Use scoped `IJobMonitor` and, only with graph capability, `IJobBatchMonitor` for custom status endpoints with authorization and paging.
9. Test non-development access, policy enforcement, provider outages, retry/delete preconditions, unsupported graph routes, SSE reconnect behavior, and redaction expectations.

## Guardrails

- Do not map an unprotected production dashboard. Without explicit authorization, non-development requests are denied by design.
- Do not expose job payloads, exceptions, identifiers, or mutation endpoints to ordinary application users.
- Do not interpret `queue.depth` or `workers.active` gauges as authoritative cluster totals; use provider monitoring snapshots.
- Do not expose graph operations for a provider without graph capability.

## Handoff

Report the authorization policy, mapped prefix, exposed controls, telemetry exporters/links, health semantics, sensitive-data treatment, provider limitations, preview revisions, and tests.
