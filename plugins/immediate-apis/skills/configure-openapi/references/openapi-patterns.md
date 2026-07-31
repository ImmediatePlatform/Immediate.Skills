# OpenAPI patterns

Nested handler types often share simple names such as `Command`, so default
schema IDs collide.

For Swashbuckle, derive IDs from full CLR names and normalize `+`:

```csharp
services.AddSwaggerGen(options =>
{
    options.CustomSchemaIds(type =>
        type.FullName?.Replace("+", ".", StringComparison.Ordinal));
});
```

For `Microsoft.AspNetCore.OpenApi`, configure the different API:

```csharp
services.AddOpenApi(options =>
    options.CreateSchemaReferenceId = jsonType =>
        jsonType.Type.IsNested
            ? $"{jsonType.Type.DeclaringType!.Name}+{jsonType.Type.Name}"
            : OpenApiOptions.CreateDefaultSchemaReferenceId(jsonType));
```

Then map the document as the application already expects. Scalar may display
it with `MapScalarApiReference()` when `Scalar.AspNetCore` is installed.

Describe generated endpoints with attributes copied from `Handle`/`HandleAsync`
or a `CustomizeEndpoint` method using `WithSummary`, `WithDescription`,
`ProducesValidationProblem`, `WithOpenApi`, and related minimal-API APIs. XML
comments flow into the document when normal ASP.NET Core XML documentation is
enabled.

An alternative is to use uniquely named top-level request/response types.
Choose this only when it matches the codebase's slice organization and public
schema naming strategy.

## Sources

- Immediate.Dev: `Immediate.Apis/openapi.md`
- Immediate.Dev: `Immediate.Handlers/openapi-and-swashbuckle.md`
- Immediate.Dev: `Immediate.Apis/customizing-endpoints.md`
