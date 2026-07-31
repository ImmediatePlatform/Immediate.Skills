---
name: customize-endpoint
description: Customize an Immediate.Apis generated endpoint with delegate attributes, CustomizeEndpoint conventions, filters, rate limits, metadata, or TransformResult response conversion. Use when the endpoint already exists and substantial metadata or result behavior is the main task; use create-route-group for shared group conventions.
---

# Customize an Immediate endpoint

Choose the narrowest supported customization mechanism and verify the generator consumes it.

## Workflow

1. Inspect the target framework and package versions, handler response/nullability, existing customizer methods, OpenAPI stack, endpoint conventions, and package diagnostics.
2. Read [customization-patterns.md](references/customization-patterns.md).
3. Prefer attributes on `Handle`/`HandleAsync` for static delegate metadata.
4. Add one correctly shaped `CustomizeEndpoint` for builder APIs, filters, naming, rate limits, output caching, or conditional conventions.
5. Add one correctly shaped `TransformResult` only when converting the handler response to an HTTP result or status contract.
6. Avoid overlapping mechanisms that describe the same metadata. Preserve authorization ordering: generated authorization is applied before `CustomizeEndpoint`.
7. Build and inspect IAPI0004/IAPI0005; an invalid method is ignored. Run endpoint metadata and result tests.

## Boundaries

- Use `create-route-group` when the same convention belongs to a set of endpoints.
- Use `configure-openapi` for schema-ID policy or application-wide document setup.
- Keep business decisions in the handler; limit transformation to transport representation.

## Handoff

Report the chosen mechanism, exact generated effect, response/nullability contract, and verification result.
