---
name: add-manual-registration
description: Add or update Immediate.Injections RegisterServices methods that integrate hand-written AddHttpClient, AddDbContext, options, third-party, or other DI setup into generated AddXxxServices, including accepted signatures, tags, accessibility, ordering, duplicates, and INJ0001. Use when registration cannot be represented by class attributes.
---

# Add manual generated registration

Keep complex hand-written DI inside the assembly's single generated registration entry point.

## Workflow

1. Confirm an attribute registration, factory, or proxy cannot express the setup more clearly. Inspect the Immediate.Injections version, existing manual hooks, and registration order.
2. Read [manual-registration.md](references/manual-registration.md).
3. Add `[RegisterServices]` to an accessible static void method taking `IServiceCollection` and optionally `ReadOnlySpan<string>`.
4. Put options, HTTP clients, DbContexts, hosted services, or third-party extension calls inside the method.
5. If accepting tags, mirror the platform semantics: empty means all, and use explicit ordinal matching for selected slices.
6. Account for the method running after all attribute-generated registrations. Make duplicate behavior explicit.
7. Build, inspect generated calls, and resolve or exercise representative services for unfiltered and filtered registration.

## Guardrails

- Do not make the method async or return `IServiceCollection`.
- Use public or internal accessibility reachable from the generated root-namespace class; private may pass analysis and fail generated compilation.
- Do not depend on ordering among several manual methods.

## Handoff

Report why manual setup was required, method signature/accessibility, tag behavior, duplicate/order interaction, and verification.
