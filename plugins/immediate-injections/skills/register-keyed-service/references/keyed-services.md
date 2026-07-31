# Keyed service patterns

```csharp
[RegisterScoped<INotificationSender>(ServiceKey = "email")]
public sealed class EmailSender : INotificationSender;

[RegisterScoped<INotificationSender>(ServiceKey = "sms")]
public sealed class SmsSender : INotificationSender;
```

Resolve a fixed key with
`[FromKeyedServices("email")] INotificationSender sender`, or select dynamically
with `GetRequiredKeyedService<INotificationSender>(key)`.

A keyed registration is unavailable from ordinary `GetService<T>()`. Apply a
second unkeyed attribute when both forms are needed. Those are independent
descriptors; use a real self registration plus a proxy when identity must be
shared.

Keys may be strings, constants, enum members, numbers, or other valid attribute
constants. Resolve with the same value/type. `ServiceKey = null` means no key.

A keyed factory declared on the attributed class has this shape:

```csharp
public static MyService Create(IServiceProvider provider, object? serviceKey)
    => new(serviceKey);
```

The second argument is the key requested by the caller, not necessarily the
attribute's declared key. An unkeyed factory accepts only `IServiceProvider`.

## Sources

- Immediate.Dev: `Immediate.Injections/keyed-services.md`
- Immediate.Dev: `Immediate.Injections/factories-and-proxies.md`
- Immediate.Dev: `Immediate.Injections/diagnostics.md`
