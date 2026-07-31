---
name: validate-request
description: Add or update Immediate.Validations rules on a request or domain input, including the validation-target interface, built-in validators, nullable and enum behavior, nested objects, collections, AdditionalValidations, direct validation, and ValidationBehavior integration. Use for applying validation; use create-custom-validator to define a new validator attribute.
---

# Validate a request

Generate validation that matches the model's nullability, nesting, collection, and handler-pipeline semantics.

## Workflow

1. Inspect the type hierarchy, nullable settings, property shapes, existing validation messages, handler behaviors, and Immediate.Validations version.
2. Read [request-validation.md](references/request-validation.md).
3. Mark the target `partial` with `[Validate]` and declare `IValidationTarget<TSelf>`. Make enclosing types partial when the target is nested.
4. Apply compatible built-in validators to public settable properties. Account for automatic non-nullable-reference and enum checks.
5. Model nested validation and collection element rules deliberately; do not rely on `IEnumerable<T>` traversal.
6. Use member references through `nameof(...)` for comparisons and `AdditionalValidations` for imperative cross-property rules that attributes cannot express.
7. Choose direct `Validate`/`ThrowIfInvalid` or add `ValidationBehavior<,>` to the handler pipeline. Preserve it in handler-level behavior overrides.
8. Test valid, boundary, null, nested, collection-index, and cross-property cases. Assert property paths as well as messages.

## Guardrails

- Use `[property: ...]` targets on positional-record parameters.
- Do not add explicit `[NotNull]` to non-nullable value types.
- Keep validation deterministic and side-effect free.
- Route application-wide localization and exception translation to their focused skills.

## Handoff

Report generated targets, implicit checks, explicit rules, execution path, property-path behavior, and focused test results.
