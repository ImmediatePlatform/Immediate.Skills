# Request validation patterns

Create a target:

```csharp
[Validate]
public sealed partial record CreateOrder : IValidationTarget<CreateOrder>
{
    [NotEmpty]
    public required string CustomerNumber { get; init; }

    [GreaterThan(0)]
    public required decimal Total { get; init; }
}
```

The generator examines public, non-static, settable properties declared on the
type. For positional records, target the generated property:
`[property: MaxLength(50)] string Name`.

Non-nullable reference properties receive an implicit `NotNull` check unless
`[AllowNull]` opts out. Nullable references are unchecked unless explicitly
validated. Enum and nullable-enum properties receive automatic `EnumValue`.

Built-ins include `Empty`, `NotEmpty`, `NotNull`, equality/comparison variants,
`Length`, `MinLength`, `MaxLength`, `Match`, `EnumValue`, and `OneOf`. Bounds on
the length validators are inclusive. Use `nameof(Member)` for supported target
parameters that compare with another property, field, or parameterless method.

Nested `[Validate]` targets recurse automatically. Arrays and types implementing
`ICollection<T>` or `IReadOnlyCollection<T>` are traversed; `IEnumerable<T>` is
not. Paths look like `Address.Street`, `Addresses[2].Street`, and nested indexes.
Use `[element: NotEmpty]` when the validator should apply to elements rather
than the collection.

For handlers, register the constrained behavior:

```csharp
[assembly: Behaviors(typeof(ValidationBehavior<,>))]
```

It attaches only when the request implements `IValidationTarget<TRequest>` and
throws before `Next`. Behavior order controls which outer concerns observe the
failure. A handler-level `[Behaviors]` replaces the assembly list, so repeat the
validation behavior there when required.

Outside handlers, call `T.Validate(instance)`, inspect `IsValid`/`Errors`, or
use `ValidationException.ThrowIfInvalid(instance)`.

## Sources

- Immediate.Dev: `Immediate.Validations/creating-validators.md`
- Immediate.Dev: `Immediate.Validations/built-in-validators.md`
- Immediate.Dev: `Immediate.Validations/nested-and-collection-validation.md`
- Immediate.Dev: `Immediate.Validations/additional-validations.md`
- Immediate.Dev: `Immediate.Validations/validating-instances.md`
- Immediate.Dev: `Immediate.Validations/immediate-handlers-integration.md`
