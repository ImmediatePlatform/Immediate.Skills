---
name: register-keyed-service
description: Add or update keyed Immediate.Injections registrations with ServiceKey, keyed resolution or FromKeyedServices, optional unkeyed access, keyed factories, duplicate behavior, and tests. Use when several implementations share a service type and are selected by a compile-time key; use register-service for ordinary unkeyed DI.
---

# Register a keyed service

Generate keyed descriptors whose registration and resolution keys are type- and value-consistent.

## Workflow

1. Inspect the target framework, Immediate.Injections version, current key vocabulary/types, service consumers, lifetime, duplicate policy, and existing keyed/unkeyed descriptors.
2. Read [keyed-services.md](references/keyed-services.md).
3. Apply the intended registration attribute with a compile-time `ServiceKey`.
4. Resolve through `[FromKeyedServices]` for fixed dependencies or keyed service-provider APIs for runtime selection.
5. Add a separate unkeyed registration only when both access paths are required. Decide whether independent instances are acceptable; use a proxy for shared identity.
6. For a keyed factory, use the keyed factory signature and treat the supplied key as runtime input.
7. Build and test every supported key, missing/wrong keys, unkeyed behavior, lifetime, and duplicate interaction.

## Guardrails

- A keyed descriptor is not also unkeyed.
- Key comparison uses `Equals`; enum, string, and numeric values with similar text are different.
- `ServiceKey = null` is emitted as unkeyed.
- Keep keys stable when other assemblies or configuration select them.

## Handoff

Report key type/values, keyed and unkeyed descriptors, resolution mechanism, identity semantics, and tests.
