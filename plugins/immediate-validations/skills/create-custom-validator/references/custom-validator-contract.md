# Custom validator contract

A minimal validator:

```csharp
public sealed class DivisibleByAttribute(int divisor) : ValidatorAttribute
{
    public static bool ValidateProperty(int target, int divisor)
        => divisor != 0 && target % divisor == 0;

    public static string DefaultMessage
        => "'{PropertyName}' must be divisible by {DivisorValue}.";
}
```

Contract:

- Derive from `ValidatorAttribute` and declare at most one non-static constructor.
- Declare exactly one `public static bool ValidateProperty`.
- Use its first parameter to define applicable property types. A generic method
  may constrain the accepted types.
- Declare `DefaultMessage` as a public static string property or public const
  string field.
- Mirror each constructor parameter or settable attribute property in the
  validation method by case-insensitive name and assignable type.
- Make an attribute property `required`, or give the corresponding validation
  parameter a default, when no constructor value supplies it.

Validate constructor and property configuration as part of the rule or its
tests. Decide explicitly what negative, reversed, empty, or otherwise invalid
options mean; the generator verifies contract shape, not every domain-specific
relationship between option values.

Use `[TargetType] object`, `string`, or their arrays when an attribute argument
must have the validated property's actual type:

```csharp
public sealed class NotEqualToAttribute([TargetType] object comparison)
    : ValidatorAttribute
{
    public static bool ValidateProperty<T>(T target, T comparison)
        => !EqualityComparer<T>.Default.Equals(target, comparison);

    public static string DefaultMessage
        => "'{PropertyName}' must not equal {ComparisonValue}.";
}
```

This also enables `nameof(...)` to resolve to a real member access. Use `params`
on both the attribute and validation method for a variable list.

By default, a null property fails the generated null check and later validators
do not run. A nullable first `ValidateProperty` parameter opts that validator
into running before the null check. Keep the first parameter non-nullable when
`[NotEmpty]` or the ordinary null check should own required-value behavior.

Default messages support `{PropertyName}`, `{PropertyValue}`, and
`{XxxValue}`/`{XxxName}` for each additional method parameter. To localize a
custom default, return
`ValidationConfiguration.Localizer[nameof(MyAttribute)].Value`.

Key diagnostics IV0001-IV0010 describe missing/static/duplicate methods,
return type, argument pairing, constructor count, and missing message. IV0014,
IV0015, and IV0017 cover target and referenced-member incompatibilities.

## Sources

- Immediate.Dev: `Immediate.Validations/custom-validators.md`
- Immediate.Dev: `Immediate.Validations/custom-messages.md`
- Immediate.Dev: `Immediate.Validations/diagnostics.md`
- Immediate.Dev: `Immediate.Validations/api-reference.md`
