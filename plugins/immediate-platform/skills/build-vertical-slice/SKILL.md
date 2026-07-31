---
name: build-vertical-slice
description: Build or update a complete ImmediatePlatform vertical slice spanning an Immediate.Handlers command/query, optional Immediate.Validations rules, Immediate.Apis endpoint, Immediate.Injections service registration, optional Immediate.Cache integration, startup registration, and focused tests. Use for end-to-end feature requests rather than one package-specific edit.
---

# Build an Immediate vertical slice

Implement one cohesive feature across the selected ImmediatePlatform packages without losing package-specific semantics.

## Workflow

1. Read repository instructions and inspect project boundaries, target frameworks, package versions, neighboring slices, persistence, authorization, registration, and tests.
2. Read [vertical-slice.md](references/vertical-slice.md).
3. Define the feature's request, response, handler dependencies, and transactional boundary first.
4. Add generated validation when inputs have enforceable preconditions. Position validation and other behaviors deliberately.
5. Add an API endpoint only for externally reachable features. Model binding, authorization, route grouping, and transport result separately from handler business logic.
6. Register supporting services with Immediate.Injections when the application already uses it.
7. Add Immediate.Cache only for repeatable value-returning reads with a clear key and invalidation path; make the target handler sealed/non-static.
8. Update startup in dependency order and use the assembly's actual generated identifier.
9. Add focused unit/integration tests for handler logic, validation, HTTP contract, and cache invalidation as applicable. Build the affected solution/project.

## Guardrails

- Adopt only packages needed by the feature; ImmediatePlatform packages are independently optional.
- Keep the skill self-contained; do not require package plugins to be installed.
- Preserve the established slice layout and public contracts.
- Do not add caching without a mutation invalidation strategy or assume cache hits run behaviors.

## Handoff

Summarize the slice files, package contributions, generated startup methods, request-to-response path, and all build/test evidence.
