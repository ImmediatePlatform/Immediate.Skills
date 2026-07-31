---
name: create-route-group
description: Create or update an Immediate.Apis RouteGroup and attach generated endpoints with the generic MapGroup attribute, including nested prefixes, CustomizeGroup conventions, tags, generated route constants, and registration. Use when several endpoints share routing or policy; do not use for an assembly-wide prefix alone.
---

# Create an Immediate route group

Group related endpoints without creating malformed composed routes or mismatched host filters.

## Workflow

1. Inspect the target framework, Immediate.Apis and Immediate.Handlers versions, existing group hierarchy, route style, authorization and metadata conventions, tag vocabulary, and endpoint/handler registration filters.
2. Read [route-group-patterns.md](references/route-group-patterns.md).
3. Define a `partial` class with `[RouteGroup("segment")]`.
4. Attach endpoints using `[MapGroup<TGroup>]`; point to the innermost valid group.
5. Nest groups as nested C# classes when prefixes must compose.
6. Add one correctly shaped `CustomizeGroup` for shared conventions. Resolve every named authorization policy from existing host configuration; if its semantics are absent, attach no invented policy definition and report the missing application decision.
7. Normalize route segment slashes when generated route constants will be used. Use an empty endpoint route for the group root and account for its documented trailing slash in the generated constant.
8. Coordinate group/endpoint tags with matching handler tags and mapping filters.
9. Build and run route, authorization, and filtered-registration tests.

## Guardrails

- `CustomizeGroup` must be private; unlike endpoint customization, internal is invalid.
- If the installed packages do not expose route groups, report the mismatch and the compatible migration required. Do not silently upgrade the application's package graph.
- Do not invent claims, roles, or assertions for a named authorization policy that the host has not defined.
- Do not call group mapping methods manually; `MapXxxEndpoints()` maps top-level groups recursively.
- A tagged parent that does not match skips its entire subtree. An endpoint's own tag check still applies after its parents match.

## Handoff

Report the composed route tree, shared conventions, selected tags, route constants, and endpoint mapping evidence.
