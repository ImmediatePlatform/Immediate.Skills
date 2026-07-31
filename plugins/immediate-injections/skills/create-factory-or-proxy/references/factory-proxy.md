# Factory and proxy patterns

Custom construction names a static method on the attributed class:

```csharp
[RegisterTransient<IMyService>(Factory = nameof(Create))]
public sealed class MyService : IMyService
{
    public static MyService Create(IServiceProvider provider)
        => new(provider.GetRequiredService<IDependency>());
}
```

Unkeyed signature: `static TSelf Method(IServiceProvider)`. Keyed signature:
`static TSelf Method(IServiceProvider, object?)`. Use `nameof`; return the
attributed class itself.

Proxy an interface to a real concrete registration:

```csharp
[RegisterSingleton(
    RegistrationStrategy = RegistrationStrategy.SelfAndImplementedInterfaces,
    UseProxyFactory = true)]
public sealed class SharedService : IFirst, ISecond;
```

The self descriptor constructs `SharedService`; interface descriptors call
`GetRequiredService<SharedService>()`, so every service type returns one object.
A proxy-only interface registration requires another attribute or manual
registration for the concrete target.

Factory and proxy normally conflict. They may be combined when the effective
strategy is `SelfAndImplementedInterfaces`: the self descriptor uses the
factory and interfaces proxy to it. An assembly proxy default yields to an
attribute factory unless the attribute explicitly sets proxy behavior.

Do not proxy self, and do not use either mechanism for open generic targets.

## Sources

- Immediate.Dev: `Immediate.Injections/factories-and-proxies.md`
- Immediate.Dev: `Immediate.Injections/assembly-defaults.md`
- Immediate.Dev: `Immediate.Injections/diagnostics.md`
