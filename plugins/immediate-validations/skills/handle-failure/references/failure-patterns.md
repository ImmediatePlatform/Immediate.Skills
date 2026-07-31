# Validation failure patterns

`ValidationException` exposes `Title` and `Errors`. Each `ValidationError` has
`PropertyName` and `ErrorMessage`. Map it once at the host boundary:

```csharp
services.AddProblemDetails(options =>
    options.CustomizeProblemDetails = context =>
    {
        if (context.Exception is not ValidationException exception)
            return;

        context.ProblemDetails = new ValidationProblemDetails(
            exception.Errors
                .GroupBy(error => error.PropertyName, StringComparer.OrdinalIgnoreCase)
                .ToDictionary(
                    group => group.Key,
                    group => group.Select(error => error.ErrorMessage).ToArray(),
                    StringComparer.OrdinalIgnoreCase))
        {
            Status = StatusCodes.Status400BadRequest,
            Title = exception.Title,
        };

        context.HttpContext.Response.StatusCode = StatusCodes.Status400BadRequest;
    });
```

Ensure `UseExceptionHandler()` or the development exception page is in the
pipeline; otherwise the ProblemDetails customizer does not receive the
exception.

Property names are machine paths: `Address.Street`,
`Addresses[2].Street`, and `.self` for a null root. Message display names are
separate. Preserve all messages for a repeated path.

For clients requiring camelCase, split the path on `.` and transform each
segment, preserving bracketed indexes. Outside ASP.NET Core, catch and map the
ordinary exception or avoid exception flow by calling `Validate` and inspecting
`ValidationResult.IsValid`/`Errors`.

## Sources

- Immediate.Dev: `Immediate.Validations/handling-failures.md`
- Immediate.Dev: `Immediate.Validations/nested-and-collection-validation.md`
- Immediate.Dev: `Immediate.Validations/api-reference.md`
