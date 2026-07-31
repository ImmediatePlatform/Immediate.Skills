---
name: handle-failure
description: Translate Immediate.Validations ValidationException failures into ASP.NET Core ValidationProblemDetails or an equivalent non-HTTP error contract while preserving grouped property paths and messages. Use when validation already executes and transport-level failure handling, middleware, status codes, or client field mapping is the main task.
---

# Handle validation failures

Translate generated validation failures once at the application boundary without discarding structured error paths.

## Workflow

1. Inspect the Immediate.Validations and host package versions, how validation executes, the exception/error pipeline, existing ProblemDetails configuration, client error schema, naming policy, and tests.
2. Read [failure-patterns.md](references/failure-patterns.md).
3. Catch or customize only `ValidationException` at the appropriate boundary. Preserve unrelated exception handling.
4. Group `ValidationError` records by `PropertyName`, retaining every `ErrorMessage` per key.
5. For ASP.NET Core, emit HTTP 400 `ValidationProblemDetails`, set the response status, and ensure exception-handler middleware supplies the exception to the customizer.
6. For non-HTTP flows, map to the application's structured result or call `Validate` directly when exceptions are undesirable.
7. Test multiple errors on one property, nested/indexed paths, `.self`, casing transforms, and non-validation exceptions.

## Guardrails

- Do not flatten property paths into display names; clients need stable paths for field mapping.
- If camel-casing paths, transform dot-separated segments without corrupting indexes.
- Do not leak exception details for unrelated server errors.

## Handoff

Report boundary/middleware, status and error schema, path casing, preservation of multiple messages, and integration-test result.
