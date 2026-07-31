---
name: configure-openapi
description: Configure OpenAPI for Immediate.Apis endpoints, including unique schema identifiers for nested Query, Command, and Response types, Swashbuckle or Microsoft.AspNetCore.OpenApi setup, Scalar integration, and generated endpoint descriptions. Use for schema collisions or document-wide OpenAPI behavior, not ordinary endpoint creation.
---

# Configure Immediate OpenAPI

Fix schema identity and document generated endpoints using the web application's chosen OpenAPI stack.

## Workflow

1. Identify the actual OpenAPI generator and versions in the project. Reproduce the collision or missing metadata before changing configuration.
2. Read [openapi-patterns.md](references/openapi-patterns.md).
3. Choose one unique, deterministic schema-ID strategy compatible with existing clients. Preserve established document IDs when possible.
4. Configure Swashbuckle with `CustomSchemaIds`, or configure built-in OpenAPI with `CreateSchemaReferenceId`; do not mix their knobs.
5. Add endpoint descriptions through copied handle attributes or a correctly shaped `CustomizeEndpoint`.
6. Enable XML documentation only if the project wants comments included and accepts the build-output change.
7. Generate or request the OpenAPI document and verify uniqueness, routes, status codes, security, and client-generator compatibility.

## Guardrails

- Prefer a one-time schema configuration over moving every nested request type solely to avoid collisions.
- Avoid changing schema IDs casually in a published API because generated client type names may change.
- Keep Scalar optional; it is a viewer for built-in OpenAPI, not the schema-ID mechanism.

## Handoff

Report the OpenAPI stack, old collision, selected ID format, affected client compatibility, and generated-document verification.
