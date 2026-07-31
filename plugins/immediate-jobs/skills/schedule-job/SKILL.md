---
name: schedule-job
description: Enqueue or schedule an Immediate.Jobs job through its generated scoped Scheduler, including delayed and absolute execution, queue selection, fair-group dispatch, and NodaTime overloads. Use only with a verified restorable Immediate.Jobs preview package set; do not apply this preview API from memory.
---

# Schedule an Immediate job

Persist work through the generated typed scheduler and preserve scope, timing, and dispatch semantics.

## Workflow

1. Verify the exact Immediate.Jobs preview baseline and provider capabilities in the target solution.
2. Inspect the target job's generated scheduler, request type, queue, context extractors, and caller lifetime.
3. Read [scheduling-patterns.md](references/scheduling-patterns.md).
4. Inject `JobName.Scheduler` into scoped or transient callers. Create a service scope before resolving it from singleton code.
5. Choose enqueue, relative delay, or absolute instant based on the actual requirement; pass cancellation only for persistence of the scheduling operation.
6. Add a fair-group ID only when ordering by tenant or key is required and the configured provider supports fair acquisition.
7. Use the NodaTime companion package and registration before selecting `Duration` or `Instant` overloads.
8. Treat the returned `JobHandle` as opaque and distinguish successful persistence from successful execution.
9. Test the persisted schedule, timing boundary, group normalization, and caller scope.

## Guardrails

- Do not tell callers that cancelling the scheduling token cancels later execution.
- Do not resolve a generated scheduler directly from a singleton root provider; context capture may require scoped services.
- Do not use fair groups with Redis or without enabling fair queues. Group IDs are limited to 128 characters; whitespace means no group.
- Do not mix NodaTime payloads or overloads into a host that lacks the matching preview companion registration.

## Handoff

Report the selected API, intended execution instant, queue/group behavior, provider capability, scope ownership, returned handle use, and test evidence.
