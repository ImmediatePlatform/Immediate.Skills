# Manual registration patterns

Accepted shapes:

```csharp
[RegisterServices]
internal static void Register(IServiceCollection services)
{
    services.AddHttpClient<TodoApiClient>();
    services.AddDbContext<TodoDbContext>();
}

[RegisterServices]
internal static void RegisterWorkers(
    IServiceCollection services,
    ReadOnlySpan<string> tags)
{
    if (tags.Length != 0 && !tags.Contains("worker"))
        return;
    services.AddHostedService<OutboxWorker>();
}
```

The method must be static, non-async, return void, and accept exactly
`IServiceCollection` with optional second `ReadOnlySpan<string>`. Make it public
or internal and place it where the generated root-namespace registration class
can call it.

The generator passes the raw tags; it does not filter manual methods. Preserve
the shared meaning that an empty list registers everything.

Every valid `[RegisterServices]` method runs, with no declared ordering. Manual
methods run last inside `AddXxxServices`, after scoped, singleton, and transient
attribute-driven registrations. Account for that when calling Add, TryAdd, or
Replace and avoid relying on collection order across generated groups.

## Sources

- Immediate.Dev: `Immediate.Injections/manual-registration.md`
- Immediate.Dev: `Immediate.Injections/how-it-works.md`
- Immediate.Dev: `Immediate.Injections/diagnostics.md`
- Immediate.Dev: `concepts/tags.md`
