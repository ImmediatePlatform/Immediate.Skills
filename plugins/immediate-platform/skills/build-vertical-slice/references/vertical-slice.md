# Vertical slice composition

Immediate.Handlers is the core. Immediate.Validations, Immediate.Apis, and
Immediate.Cache extend it. Immediate.Injections is independent.

Typical feature shape:

```text
Features/Orders/
  CreateOrder.cs       # request, response, handler, validation, endpoint
  GetOrder.cs          # query handler and endpoint
  GetOrderCache.cs     # optional query cache
```

Request flow:

```text
HTTP endpoint -> generated Handler -> outer behaviors -> validation ->
HandleBehavior -> feature method
```

Immediate.Cache wraps the entire generated handler on a miss, so a hit skips
every behavior and the method.

Startup commonly contains:

```csharp
services.AddMyAppBehaviors();
services.AddMyAppHandlers();
services.AddMemoryCache();       // only with Cache
services.AddMyAppCaches();       // only with Cache
services.AddMyAppServices();     // only with Injections

var app = builder.Build();
app.MapMyAppEndpoints();         // only with Apis
```

Immediate.Validations has no generated registration method; add
`ValidationBehavior<,>` to `[assembly: Behaviors(...)]`. Generated method names
use the assembly identifier.

Check installed versions. Released packages support net8.0-net10.0 in the
source baseline, but packages version independently. Treat the target project's
package API and generated output as authoritative.

## Sources

- Immediate.Dev: `getting-started/installation.md`
- Immediate.Dev: `getting-started/tutorial/*`
- Immediate.Dev: `concepts/handlers-and-behaviors.md`
- Immediate.Dev: `concepts/package-compatibility.md`
- Immediate.Dev: `cookbook/web-api.md`
- Immediate.Dev: `cookbook/blazor.md`
- Immediate.Dev: `cookbook/cli.md`
