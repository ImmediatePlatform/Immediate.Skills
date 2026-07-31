---
name: create-factory-or-proxy
description: Configure Immediate.Injections Factory or UseProxyFactory construction, including keyed and unkeyed factory signatures, shared-instance interface forwarding, SelfAndImplementedInterfaces, assembly defaults, and INJ factory/proxy diagnostics. Use when normal implementation-type construction is insufficient or several service types must share one instance.
---

# Create an injection factory or proxy

Choose custom construction or forwarding deliberately and prove the target registration exists.

## Workflow

1. Inspect the Immediate.Injections version, required construction logic, service/implementation types, keys, lifetime, identity requirements, assembly defaults, and generic status.
2. Read [factory-proxy.md](references/factory-proxy.md).
3. Use `Factory = nameof(Method)` when the attributed class must construct itself through a static method.
4. Use `UseProxyFactory = true` when a service descriptor should resolve an already registered implementation.
5. For one instance behind self and interfaces, register self for real and proxy interface registrations, commonly through `SelfAndImplementedInterfaces`.
6. Combine factory and proxy only in the supported self-plus-interfaces shape.
7. Build and test concrete/interface reference identity, lifetime, missing target failure, keyed resolution, and factory invocation.

## Guardrails

- A proxy does not register its implementation; ensure a real target descriptor exists.
- Never proxy a type to itself.
- Do not use factories/proxies for open generic registrations.
- Keep factory return type exactly the attributed class and use the keyed signature only for keyed registrations.

## Handoff

Report construction path, real/proxy descriptors, lifetime and identity, factory signature, and resolution tests.
