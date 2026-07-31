# Open generic patterns

Register one open descriptor:

```csharp
[RegisterTransient(ServiceType = typeof(IRepository<>))]
public sealed class Repository<T> : IRepository<T>;
```

This emits `IRepository<> -> Repository<>`; the container closes it for
`IRepository<Order>`, `IRepository<Customer>`, and compatible types. A bare
attribute on `Cache<T>` registers `Cache<>` as itself.

Register selected closed constructions instead:

```csharp
[RegisterScoped<IRepository<Order>, Repository<Order>>]
[RegisterScoped<IRepository<Customer>, Repository<Customer>>]
public sealed class Repository<T> : IRepository<T>;
```

A closed `ServiceType = typeof(IRepository<Order>)` is equivalent for one
construction.

Service and implementation arities must match and the closed implementation
must implement the requested service. Generic registration strategies include
only generic interfaces with the same arity, closed directly over the class's
own type parameters; add explicit attributes for skipped shapes.

MSDI cannot construct an open generic through an implementation factory.
Do not set `Factory` or `UseProxyFactory` on open generic registration. Closed
constructions may use them.

## Sources

- Immediate.Dev: `Immediate.Injections/open-generics.md`
- Immediate.Dev: `Immediate.Injections/registering-services.md`
- Immediate.Dev: `Immediate.Injections/registration-strategies.md`
- Immediate.Dev: `Immediate.Injections/diagnostics.md`
