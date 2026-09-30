# Operations patterns

Register the dashboard before building the app, then map it under an operator-only
path with a named policy:

```csharp
builder.Services.AddMyAppJobs()
	.ConfigureStorage(storage => storage.UseInMemory())
	.AddImmediateJobsDashboard()
	.ConfigureDashboard(options => options.AuthorizationPolicy = "operations");

app.MapImmediateJobsDashboard("/jobs");
```

The surface includes payloads, errors, retained execution history, SSE state,
server snapshots, job and recurring mutations, and graph operations when the
provider supports them. Without an `AuthorizationPolicy`, it is available only
in the `Development` environment and returns 403 elsewhere. Set
`RestrictToDevelopmentEnvironment = false` only for a trusted custom development
environment. A named authorization policy replaces that environment check.

`ConfigureDashboard` also accepts an
`OptionsBuilder<ImmediateJobsDashboardOptions>` callback. Bind an explicit
`IConfiguration` section with `Bind`, or use `BindConfiguration` with its path.

Operators can retry terminal failures, move scheduled work to `Pending` with
Run now, cancel non-terminal jobs or batches, and pause, resume, or trigger
recurring schedules. Cancellation is stored, but it does not forcibly stop
handler code already running. If that handler finishes later, its result cannot
replace the recorded cancellation.

Export the `Immediate.Jobs` activity source and meter. Execution traces link back
to the enqueue trace. Metrics cover enqueue, success, failure, retry, duration,
`acquisition.count` (running plus claimed-but-waiting jobs on the node, capped by
`MaxAcquisitionCount`), and `workers.active`. The gauges cover only the current
process, so use provider snapshots for complete cluster totals. Worker logging
scopes include `JobName`, `QueueName`, `JobHandle`, and `Attempt`.

Every log event has a stable ID and a package-prefixed event name, such as
`Immediate.Jobs.Shared.LeaseRenewalFailed`,
`Immediate.Jobs.Shared.RecurringMaterializationFailed`, or
`Immediate.Jobs.Shared.RecurringOccurrencesMissed`. IDs start at 11000 for the
core runtime, 11500 for EF Core, 11600 for LinqToDB, and 11700 for Redis.
Storage calls log at `Debug`; enable it only while diagnosing.

Each acquired attempt retains its outcome, worker, timing, trace/span IDs, and
failure text until its job or batch is removed. A telemetry-link callback receives
`Execution = null` for a job-level link and the exact `JobExecutionRecord` for an
attempt-level link. Use the execution record for one trace. Use
`context.Job.JobHandle.Value` for a log query across retries. Return null when a
link does not apply.

Dashboard JSON uses `jobHandle` and `batchHandle` string fields. Its item routes
use `{jobHandle}` and `{batchHandle}` parameters. Convert boundary strings with
`JobHandle.FromString` or `BatchHandle.FromString` before calling monitor APIs.

Chain `AddHealthCheck(name)` from generated job registration. It registers
`{name}-storage` (provider connectivity, with capability data) and
`{name}-service` (worker started and heartbeat within `ServerTimeout`, 10 seconds
by default); both share the tags and failure status. The service check reports
the failure status until the worker starts and always reports healthy under
`DisableWorkers()`. Map a tag-filtered readiness endpoint. The checks use the same
validated options as the worker and need no separate options registration.

Monitoring snapshots list only nodes whose heartbeat is within their own
`ServerTimeout`. Each `JobServerSnapshot` includes `Workers` (zero-based worker ID,
current `JobHandle`, attempt, and start time), plus `Acquisition` and
`LeaseRenewal` loop snapshots with last success/failure times and
`ConsecutiveFailures`. The dashboard Servers view shows each worker as a slot
linked to its running job and lists busy workers.

Use the singleton `JobMonitor` from `Immediate.Jobs.Shared.Apis` for reads and
management commands. Its read-only `IJobMonitor` interface lives in
`Immediate.Jobs.Shared.Interfaces` and resolves to the same singleton instance.
Graph edges from `GetBatchGraphAsync` and `JobStatus.DependsOn` are
`JobContinuationEdge` records.
Apply authorization and paging to custom endpoints. Low-level execution history is available through
`IJobStorage.QueryJobExecutionsAsync` in `Immediate.Jobs.Shared.Storage`.

## Sources

- Immediate.Dev: `Immediate.Jobs/dashboard-and-monitoring.md`
- Immediate.Dev: `Immediate.Jobs/observability-and-health.md`
- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/api-reference.md`
