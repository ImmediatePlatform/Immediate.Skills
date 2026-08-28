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
local queue depth, and active workers. The gauges cover only the current process,
so use provider snapshots for complete cluster totals. Worker logging scopes
include `JobName`, `QueueName`, `JobHandle`, and `Attempt`.

Each acquired attempt retains its outcome, worker, timing, trace/span IDs, and
failure text until its job or batch is removed. A telemetry-link callback receives
`Execution = null` for a job-level link and the exact `JobExecutionRecord` for an
attempt-level link. Use the execution record for one trace. Use
`context.Job.JobHandle.Value` for a log query across retries. Return null when a
link does not apply.

Dashboard JSON uses `jobHandle` and `batchHandle` string fields. Its item routes
use `{jobHandle}` and `{batchHandle}` parameters. Convert boundary strings with
`JobHandle.FromString` or `BatchHandle.FromString` before calling monitor APIs.

Chain `AddHealthCheck` from generated job registration. It combines scheduler
liveness and provider connectivity. Map a tag-filtered readiness endpoint and
return HTTP 503 for `Degraded` if the scheduler must be running before the app is
ready. It uses the same validated options as the worker and needs no separate
options registration.

Use scoped `JobMonitor` from `Immediate.Jobs.Shared.Apis` for reads and management
commands. Its read-only `IJobMonitor` interface lives in
`Immediate.Jobs.Shared.Interfaces` and resolves to the same scoped instance.
Apply authorization and paging to custom endpoints. Low-level execution history is available through
`IJobStorage.QueryJobExecutionsAsync` in `Immediate.Jobs.Shared.Storage`.

## Sources

- Immediate.Dev: `Immediate.Jobs/dashboard-and-monitoring.md`
- Immediate.Dev: `Immediate.Jobs/observability-and-health.md`
- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/api-reference.md`
