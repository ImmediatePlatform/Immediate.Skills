---
name: localize-validation
description: Localize or globally customize Immediate.Validations messages with built-in cultures, validator Message templates, Description display names, a custom IStringLocalizer, resource keys, and per-request UI culture. Use for application-wide message language or wording; use validate-request for the validation rules themselves.
---

# Localize validation messages

Configure one stable message catalogue while preserving culture selection and property-path semantics.

## Workflow

1. Inspect the Immediate.Validations and localization package versions, current middleware, supported cultures, resource conventions, message overrides, and custom validators.
2. Read [localization-patterns.md](references/localization-patterns.md).
3. Decide whether the task needs one attribute's `Message`, a display name, built-in culture selection, or a replacement global localizer.
4. For a replacement catalogue, provide every validator key or implement a deliberate fallback and assign `ValidationConfiguration.Localizer` once during startup.
5. Keep per-request variation in `CultureInfo.CurrentUICulture`; do not mutate the static localizer per request.
6. Make custom validators read their defaults from the same configuration when localization is required.
7. Test at least the default and one alternate culture, missing keys, formatted tokens, nested/indexed property paths, and explicit message overrides.

## Guardrails

- Explicit `Message` values are literals and are not localized by the global catalogue.
- Keep `ValidationError.PropertyName` as the stable machine path; localize only human-readable messages/display names.
- Remember that root-null sentinel text is not localized.

## Handoff

Report catalogue source, supported cultures, fallback behavior, startup assignment, non-localized exceptions, and culture-test results.
