---
name: create-handler
description: Create or update an Immediate.Handlers command, query, or request handler, including its request and response types, dependency shape, generated Handler consumption, registration, and common IHR diagnostics. Use for ordinary non-streaming handler implementation; use create-behavior for pipeline concerns and create-streaming-handler for IAsyncEnumerable results.
---

# Create an Immediate handler

Create a valid application-facing handler while preserving the target repository's conventions.

## Workflow

1. Read the nearest repository instructions and inspect the project file, target framework, Immediate.Handlers package version, nullable settings, neighboring handlers, and registration entry point.
2. Read [handler-patterns.md](references/handler-patterns.md) before choosing the handler shape.
3. Define one namespace-level `partial` class marked `[Handler]`. Preserve the repository's request/response placement and naming conventions.
4. Choose a static handler with method-injected dependencies or a sealed handler with constructor-injected dependencies. Do not change styles without a concrete reason.
5. Implement exactly one private `Handle` or `HandleAsync` method. Put the request first, an optional cancellation token last, and return `ValueTask`, `ValueTask<T>`, or `IAsyncEnumerable<T>` only.
6. Consume the generated `X.Handler` or `IHandler<TRequest,TResponse>`; never inject a sealed handler container directly.
7. Add or confirm `AddXxxHandlers()` registration. Do not add endpoint, validation, cache, or job concerns unless the user requested the integrated change.
8. Build the narrowest project and run focused tests. Treat analyzer diagnostics and missing generated members as failures to investigate.

## Decision rules

- Keep commands returning bare `ValueTask`; the generated response becomes `ValueTuple`.
- Prefer a trailing `CancellationToken` unless the surrounding code intentionally suppresses IHR0012.
- Preserve nested request/response types unless OpenAPI schema naming or project conventions require top-level types.
- When converting IHR0019, move static dependency parameters to a sealed primary constructor and keep the handle method's request/token signature.
- Resolve ambiguity from the checked-out package API and generated output rather than assuming the latest documentation matches an older application.
- If the requested handler shape is unavailable in the installed version, report the incompatible package boundary before changing package versions or generated registration calls.

## Handoff

Report the handler shape, generated type consumers should use, registration changed, and build/test result. Call out any package-version or generated-code mismatch that remains.
