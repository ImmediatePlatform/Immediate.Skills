---
name: create-endpoint
description: Expose an Immediate.Handlers handler as an Immediate.Apis generated ASP.NET Core minimal API endpoint, including verb and route selection, request binding, basic authorization, result transformation, and MapXxxEndpoints registration. Use for one endpoint; route substantial customization, route groups, or application-wide OpenAPI work to their focused skills.
---

# Create an Immediate API endpoint

Map one handler to a correct HTTP contract while preserving application conventions.

## Workflow

1. Inspect the web project, Immediate.Apis and Immediate.Handlers versions, neighboring endpoints, route conventions, authorization policies, registration, and expected response contract.
2. Read [endpoint-patterns.md](references/endpoint-patterns.md).
3. Confirm the class is a valid `[Handler]`, then apply exactly one map attribute with one or more routes.
4. Model route, query, header, form, and body values on the request type. Add property or handle-parameter binding attributes only when inference does not express the contract.
5. Apply `[Authorize]` with policies or `[AllowAnonymous]` deliberately. Never leave both attributes on the class.
6. Use a small `TransformResult` when status/result conversion is intrinsic to this endpoint. Route richer metadata or filters to `customize-endpoint`.
7. Confirm handler DI registration and call `app.MapXxxEndpoints()` with the intended prefix/tags.
8. Build and run focused endpoint tests covering binding, authorization, status, and duplicate routes.

## Guardrails

- Use `[MapPost]`, `[MapPut]`, or `[MapPatch]` for normal body inference; `[MapMethod("POST", ...)]` does not infer body binding.
- Do not apply multiple map attributes to one class; only the first is read.
- Do not make one endpoint handler depend directly on another endpoint handler. Extract shared application logic.
- Keep the endpoint skill independently usable even when the Handlers plugin is not installed.

## Handoff

Report verb/routes, effective binding, authorization, response shape, generated mapping method, and endpoint/build test results.
