---
name: register-service
description: Add or update ordinary Immediate.Injections registrations using RegisterSingleton, RegisterScoped, or RegisterTransient, including service type selection, registration and duplicate strategies, assembly defaults, tags, AddXxxServices startup integration, lifetime safety, and common INJ diagnostics. Use for non-keyed, non-generic everyday DI registration.
---

# Register an Immediate service

Generate an intentional Microsoft DI descriptor set without surprising duplicate instances or lifetime capture.

## Workflow

1. Inspect the service dependencies, consumer types, existing registrations/order, assembly defaults, tags, package version, and generated method name.
2. Read [service-registration.md](references/service-registration.md).
3. Choose singleton, scoped, or transient from actual state/dependency lifetimes.
4. Choose the smallest attribute form: bare self registration, generic service type, explicit `ServiceType`, or a computed registration strategy.
5. Select `DuplicateStrategy` from the intended interaction with hand-written and module registrations.
6. Apply assembly defaults only when they express a real assembly-wide convention; keep exceptional settings on the attribute.
7. Add or confirm one `AddXxxServices()` startup call with appropriate tags.
8. Build, inspect analyzer output, and resolve every intended service type. For singleton multi-interface identity, route to the proxy workflow.

## Guardrails

- `ServiceType` and `RegistrationStrategy` are mutually exclusive.
- Registering one implementation under multiple service types normally creates independent descriptors and potentially independent singleton instances.
- Do not change lifetime merely to make validation pass; fix captive dependency design.
- Use the focused keyed, open-generic, factory/proxy, or manual skill when that mechanism is central.

## Handoff

Report lifetime, emitted service types, duplicate policy, assembly default/tag interaction, generated method, and resolution/build result.
