# Validation localization patterns

Built-in validator defaults support English and French and read
`CultureInfo.CurrentUICulture`. Change one use with the inherited `Message`
property:

```csharp
[GreaterThan(0, Message = "'{PropertyName}' must be positive; got {PropertyValue}.")]
public required int Id { get; init; }
```

Tokens are case-sensitive in attribute messages. Supported values include
`{PropertyName}`, `{PropertyValue}`, and `{XxxValue}`/`{XxxName}` based on
`ValidateProperty` parameter names. Standard .NET format suffixes are accepted.
Use `[Description("Customer number")]` to change the human display name.

Replace defaults globally by assigning the static configuration once:

```csharp
ValidationConfiguration.Localizer = myLocalizer;
```

Resource keys are validator type names such as `GreaterThanAttribute` and
`NotNullAttribute`. A `ResourceManagerStringLocalizer` follows current UI
culture, so ASP.NET Core request-localization middleware can select culture
without changing the static property. Supply all built-in keys or explicitly
fall back; a missing key otherwise renders as the key.

Custom validators opt in with:

```csharp
public static string DefaultMessage
    => ValidationConfiguration.Localizer[nameof(DivisibleByAttribute)].Value;
```

Explicit attribute messages, the root-null sentinel, and property display
names are not automatically localized. Machine paths such as
`Addresses[2].Street` stay separate from display text.

## Sources

- Immediate.Dev: `Immediate.Validations/localization.md`
- Immediate.Dev: `Immediate.Validations/custom-messages.md`
- Immediate.Dev: `Immediate.Validations/api-reference.md`
