# Operations patterns

Map the dashboard as an administrative surface and require a named policy:

```csharp
app.MapImmediateJobsDashboard("/jobs", options =>
{
    options.RequireAuthorization("operations");
});
```

The surface includes payloads, errors, job and recurring mutations, SSE state,
server snapshots, and graph operations when supported. Without
`RequireAuthorization`, it is development-only and returns 403 elsewhere.

Export the `Immediate.Jobs` `ActivitySource` and `Meter`. Execution activities
are consumers linked to enqueue trace context. Metrics cover enqueue, success,
failure, retry, duration, local queue depth, and active workers. Worker logging
scopes include `JobName`, `QueueName`, `JobId`, and `Attempt`.

Register the health check returned by generated job registration. It combines
scheduler liveness and provider connectivity. Use durable monitoring snapshots
for cluster state; the observable gauges are local runtime observations.

Use scoped `IJobMonitor` for records and `IJobBatchMonitor` for graph-capable
providers. Apply paging and authorization to custom endpoints. Telemetry-link
factories should build HTTP(S) or dashboard-relative destinations from the
latest persisted attempt and return null when a link does not apply.

## Sources

- Immediate.Dev: `Immediate.Jobs/dashboard-and-monitoring.md`
- Immediate.Dev: `Immediate.Jobs/observability-and-health.md`
- Immediate.Dev: `Immediate.Jobs/choosing-storage.md`
- Immediate.Dev: `Immediate.Jobs/api-reference.md`
