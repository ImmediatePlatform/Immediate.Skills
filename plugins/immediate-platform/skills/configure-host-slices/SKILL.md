---
name: configure-host-slices
description: Configure tagged multi-host registration across Immediate.Handlers, Immediate.Apis, Immediate.Injections, and preview Immediate.Jobs, including tag declarations, generated call signatures, untagged-item behavior, route-group propagation, and matching handler/job filters. Use when one assembly serves web, worker, admin, test, or other host slices.
---

# Configure Immediate host slices

Coordinate one tag model across package generators and prove each host receives exactly the intended additive slice.

## Workflow

1. Inventory target frameworks, package versions, hosts, assemblies, handlers, endpoints/groups, injection registrations, jobs, and generated startup calls.
2. Read [host-tags.md](references/host-tags.md).
3. Define a small, case-stable tag vocabulary based on host capabilities.
4. Tag package items consistently. Decide explicitly which untagged items are shared infrastructure.
5. Pass matching filters to handler, endpoint, service, and job generated methods. Pass handler tags by name when using its default lifetime.
6. For endpoint groups, account for tag checks at every ancestor and endpoint.
7. For Jobs, apply the same selected tags to jobs and handlers; Jobs registration does not register handlers.
8. Build every host and add service/route/job inventory tests. Detect accidentally untagged items.

## Guardrails

- Tags are additive filters, not strict deny lists. No tags registers everything; untagged items always register.
- Matching is ordinal and case-sensitive, with any-tag semantics.
- Use separate assemblies when strict exclusion cannot tolerate an accidentally untagged item.
- Behaviors and job queue definitions have package-specific unfiltered behavior; document it.

## Handoff

Provide a host-to-tag matrix, shared untagged inventory, generated call sites, known non-filtered registrations, and host isolation test results.
