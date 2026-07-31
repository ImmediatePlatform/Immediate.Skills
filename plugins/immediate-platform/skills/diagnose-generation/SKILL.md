---
name: diagnose-generation
description: Diagnose ImmediatePlatform source-generation, analyzer, generated registration, assembly identifier, DI resolution, missing member, behavior attachment, cache override, endpoint mapping, or OpenAPI failures when ownership spans packages or is unclear. Use for investigation and evidence-backed fixes across Immediate packages; prefer a focused package skill for ordinary implementation.
---

# Diagnose Immediate generation

Trace failures from annotated source through analyzer decisions, generated C#, registration, and runtime resolution.

## Workflow

1. Reproduce the narrowest build/runtime failure and capture exact diagnostic IDs, compiler text, stack trace, target framework, language version, and package versions.
2. Read [generation-diagnostics.md](references/generation-diagnostics.md).
3. Identify the expected generator from the annotated source and generated file prefix.
4. Inspect analyzer diagnostics before runtime DI. Fix non-configurable shape errors rather than suppressing them.
5. Inspect the generated per-type file and assembly registration/mapping file. Verify the type was discovered, its inferred types/constraints/binding are correct, and its registration call exists.
6. Derive the assembly identifier and compare every startup method name/call.
7. Trace DI from generated consumer to behavior/handler/cache/job dependencies and lifetimes.
8. Check cross-package seams: endpoint-to-handler filters, validation behavior replacement, cache static targets/scoped dependencies, OpenAPI nested schema IDs, and Jobs handler registration.
9. Apply the smallest source/configuration fix, rebuild, and verify the original symptom plus a regression test where practical.

## Guardrails

- Do not edit generated files; change annotated source or configuration.
- Do not assume a missing member means a stale IDE. Prove whether generation emitted or skipped it.
- Multi-target projects may run different Roslyn builds; reproduce per target when behavior differs.

## Handoff

Report the failing layer, decisive generated/analyzer evidence, root cause, source fix, and reproduction result.
