---
name: create-custom-validator
description: Create or update a custom Immediate.Validations ValidatorAttribute, including the ValidateProperty contract, configurable constructor/property values, TargetType member references, nullable inputs, message tokens, localization, analyzer diagnostics, and focused validator tests. Use when built-in validators cannot express the rule.
---

# Create a custom validator

Implement the analyzer-enforced validator contract precisely and keep the rule reusable and side-effect free.

## Workflow

1. Confirm no built-in validator or `AdditionalValidations` rule better fits the request. A domain-named wrapper around built-in semantics is justified only when reuse, domain vocabulary, configuration, or a shared message is an explicit requirement. Inspect project naming, localization, and target property types.
2. Read [custom-validator-contract.md](references/custom-validator-contract.md).
3. Derive a sealed attribute from `ValidatorAttribute` with at most one non-static constructor.
4. Implement exactly one `public static bool ValidateProperty` method. Make its first parameter define the supported target type.
5. Mirror every configurable constructor parameter or settable property with a case-insensitively matching method parameter and compatible required/default semantics. Define how invalid attribute configuration behaves and test boundary values.
6. Add `public static string` or `public const string DefaultMessage`. Use supported tokens and the localizer when the default should vary by culture.
7. Add `[TargetType]` only for same-as-property values or arrays and member-reference resolution.
8. Build with analyzer warnings treated seriously, then test compatible/incompatible targets, default/required options, invalid configuration, null behavior, member references, and rendered messages. Use an existing test project when available; do not invent a broad test project solely for the skill unless requested, and report a build-only verification gap explicitly.

## Guardrails

- Keep the validation method pure; generated code calls the static method directly.
- A non-nullable first parameter runs only after the generated null check succeeds. Make it nullable only when the validator must see the raw null value before that check; compose ordinary required-string rules with `[NotEmpty]`.
- Do not add multiple `ValidateProperty` overloads or constructors.
- Prefer `AdditionalValidations` for a one-off model-specific rule rather than publishing a broadly named attribute.

## Handoff

Report the target type domain, configurable arguments, null policy, message tokens/localization, diagnostics addressed, and test evidence.
