---
name: configure-registration
description: Configure Immediate.Handlers dependency-injection registration, including assembly-generated methods, handler lifetimes, behavior registration, single-handler test registration, and tagged host subsets. Use when Program.cs registration, lifetime selection, tags, assembly identifiers, or missing handler services are the main concern.
---

# Configure handler registration

Register the intended handlers and behaviors with lifetimes and host filters that match the application boundary.

## Workflow

1. Inspect the host, assembly boundaries, generated method names, existing service registrations, handler attributes, and package/language versions.
2. Read [registration-patterns.md](references/registration-patterns.md).
3. Call `AddXxxBehaviors()` when any selected handler pipeline references behaviors, then call `AddXxxHandlers()`.
4. Choose the default handler lifetime from dependency lifetimes and host conventions. Preserve any per-handler lifetime override.
5. For a single test handler, prefer `X.AddHandlers(services)` and explicitly register any behaviors it needs.
6. For multi-host assemblies, define a consistent tag vocabulary and pass the intended tags at each registration call. Verify the untagged-handler rule does not leak unwanted handlers.
7. Build the host or focused fixture and resolve representative concrete and interface handler services.

## Guardrails

- Remember that behavior registrations are transient and are not filtered by handler tags.
- Do not expect a tag to hide a handler from an unfiltered call; no tags means register everything.
- Treat untagged handlers as shared by every filtered call. Use separate assemblies for strict isolation when tags cannot express the boundary safely.
- Pass handler tags by name when leaving the lifetime at its default.

## Handoff

Report generated methods, chosen lifetimes, selected tags, always-included untagged handlers, and service-resolution/build evidence.
