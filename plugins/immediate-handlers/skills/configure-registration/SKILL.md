---
name: configure-registration
description: Configure Immediate.Handlers dependency-injection registration, including assembly-generated methods, handler lifetimes, behavior registration, single-handler test registration, and tagged host subsets. Use when Program.cs registration, lifetime selection, tags, assembly identifiers, or missing handler services are the main concern.
---

# Configure handler registration

Register the intended handlers and behaviors with lifetimes and host filters that match the application boundary.

## Workflow

1. Inspect the host, assembly boundaries, generated method names, existing service registrations, handler attributes, and package/language versions.
2. Read [registration-patterns.md](references/registration-patterns.md).
3. Call `AddXxxHandlers()`. It registers each selected handler and the concrete behavior dependencies in that handler's generated pipeline.
4. Choose the default handler lifetime from dependency lifetimes and host conventions. Preserve any per-handler lifetime override.
5. For a single test handler, prefer `X.AddHandlers(services)`; it also registers that handler's concrete behavior dependencies.
6. For multi-host assemblies, define a consistent tag vocabulary and pass the intended tags at each registration call. Verify the untagged-handler rule does not leak unwanted handlers.
7. Build the host or focused fixture and resolve representative concrete and interface handler services.

## Guardrails

- Remember that generated behavior registrations are transient and follow handler selection; a behavior used only by an excluded tagged handler is not registered.
- Do not expect a tag to hide a handler from an unfiltered call; no tags means register everything.
- Treat untagged handlers as shared by every filtered call. Use separate assemblies for strict isolation when tags cannot express the boundary safely.
- Pass handler tags by name when leaving the lifetime at its default.

## Handoff

Report generated methods, chosen lifetimes, selected tags, always-included untagged handlers, and service-resolution/build evidence.
