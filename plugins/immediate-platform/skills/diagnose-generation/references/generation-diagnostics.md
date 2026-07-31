# Generation diagnostics

Generated prefixes:

| Package | Per type | Assembly level |
| --- | --- | --- |
| Handlers | `IH.*.g.cs` | `IH.ServiceCollectionExtensions.g.cs` |
| APIs | `IA.*.g.cs` | `IA.MapEndpoints.g.cs` |
| Validations | `IV.*.g.cs` | none |
| Cache | `IC.*.g.cs` | `IC.ServiceCollectionExtensions.g.cs` |
| Injections | none | `II.*.g.cs` |
| Jobs preview | `IJ.*.g.cs` | `IJ.ServiceCollectionExtensions.g.cs` |

Inspect generated files through the IDE or temporarily enable
`EmitCompilerGeneratedFiles` to a project-local intermediate path. Never edit
the output.

Generated registration names use the assembly name with dots/spaces removed,
unless a valid `[assembly: ImmediateAssemblyIdentifier("Name")]` changes every
package's identifier together. Invalid identifiers fall back to the default.

Common cross-package checks:

- A handler must satisfy its exact method shape before downstream generators can use it.
- A behavior may be filtered by constraints/nullability or replaced by a handler-level list.
- An endpoint and its handler must both survive tag filtering.
- A cache targeting a static handler emits no base type; caches require memory cache and handler registration.
- Injection attributes may be faded when a specific INJ error causes registration to be dropped.
- Nested request types need unique OpenAPI schema IDs.
- Jobs require both `AddXxxJobs` and `AddXxxHandlers`.

Build per target framework in multi-target projects because different SDK/Roslyn
generator builds may run. Use checked-out package APIs and emitted code as the
final evidence when latest docs and installed versions differ.

## Sources

- Immediate.Dev: `concepts/source-generation.md`
- Immediate.Dev: `concepts/assembly-identifier.md`
- Immediate.Dev: `concepts/package-compatibility.md`
- Immediate.Dev: each package's `diagnostics.md` and `how-it-works.md`
