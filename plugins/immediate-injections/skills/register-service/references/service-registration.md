# Service registration patterns

Use `RegisterSingleton`, `RegisterScoped`, or `RegisterTransient`:

```csharp
[RegisterScoped<IOrderRepository>]
public sealed class OrderRepository : IOrderRepository;
```

A bare attribute registers the class as itself. The one-generic-argument form
registers only `TService`. The non-generic form accepts either `ServiceType` for
one explicit type or `RegistrationStrategy` for a set; never set both.

Strategies:

- `Self`: attributed class only.
- `ImplementedInterfaces`: every implemented interface, excluding disposable
  interfaces under current behavior.
- `SelfAndImplementedInterfaces`: self plus interfaces.

Separate descriptors normally create separate instances even for singleton
registrations. Use proxy registration when one object must back all interfaces.

Duplicate strategies map directly to collection operations:

- `Append`: add unconditionally (default).
- `Skip`: `TryAdd`, keeping an earlier service-type registration.
- `Replace`: replace the first earlier descriptor only.

Assembly defaults may provide registration strategy, duplicate strategy, and
proxy behavior. Attribute values win. An explicit `ServiceType` does not inherit
the assembly registration strategy.

Call `services.AddXxxServices(tags...)`. The assembly identifier derives from
the assembly name unless overridden. No tags applies everything; untagged
registrations are always included in filtered calls.

## Sources

- Immediate.Dev: `Immediate.Injections/registering-services.md`
- Immediate.Dev: `Immediate.Injections/registration-strategies.md`
- Immediate.Dev: `Immediate.Injections/assembly-defaults.md`
- Immediate.Dev: `Immediate.Injections/diagnostics.md`
