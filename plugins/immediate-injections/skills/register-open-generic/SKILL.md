---
name: register-open-generic
description: Add or update Immediate.Injections open-generic or selected closed-generic registrations, including explicit service types, arity and assignability rules, strategy filtering, lifetimes, unsupported factories or proxies, and resolution tests. Use when a generic implementation should be closed by Microsoft DI.
---

# Register an open generic

Generate the intended open or closed descriptor without relying on unsupported delegate factories.

## Workflow

1. Inspect the Immediate.Injections version, generic arity, constraints, implemented interfaces, consumers, lifetime safety, existing closed registrations, and package diagnostics.
2. Read [open-generics.md](references/open-generics.md).
3. Decide whether every closed construction should resolve or only a finite explicit set.
4. For open interface registration, use non-generic `ServiceType = typeof(IService<>)`; for self, use a bare lifetime attribute.
5. For selected closed types, use the two-type-argument attribute or a closed `ServiceType` and repeat per construction.
6. Avoid `Factory` and `UseProxyFactory` on open generic targets.
7. Build and resolve at least two representative closed types for an open registration, including constrained/invalid types when relevant.

## Guardrails

- Match service and implementation generic arity.
- Strategy discovery on generic classes includes only compatible interfaces with the same arity closed over the class's own parameters.
- Do not assume a non-generic or differently shaped interface will be included automatically.

## Handoff

Report open versus closed scope, emitted descriptor types, skipped interfaces, unsupported mechanisms avoided, and resolution tests.
