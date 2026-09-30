# ImmediatePlatform skills roadmap

## Goal

Build a collection of small, application-facing skills derived from the
Immediate.Dev documentation. Each skill should complete one recognizable user
task, such as creating a handler or exposing an endpoint, rather than teaching
an entire package at once.

The first stable version should cover both the common application path and the
main extensibility points developers need once an application grows:

```text
handler -> validation -> API endpoint -> cache -> service registration
```

Immediate.Jobs follows as a separately versioned area. The current skills target
the published Immediate.Jobs 0.5.0 packages.

## Implementation status — 2026-07-30

The roadmap is implemented in this repository:

- Six independently installable stable plugins contain all 23 v0.1 skills:
  Handlers, APIs, Validations, Cache, Injections, and the cross-package Platform
  workflows.
- The Immediate.Jobs plugin contains all seven planned preview skills, uses
  version `0.1.0-preview.1`, disables implicit invocation for every skill, and
  remains `NOT_AVAILABLE`.
- Every skill has user-facing metadata, a concise procedural workflow, a
  focused bundled reference, and Immediate.Dev source traceability.
- `tests/activation-prompts.json` records direct, indirect, incomplete,
  negative, and edge prompts for all 30 skills. Repository validation requires
  exact coverage.
- Representative forward tests cover handler creation, route groups, and
  custom validator creation against isolated cookbook fixtures. Each edited
  fixture builds successfully; the handler fixture also passes a CLI smoke
  test.

The Jobs gate is deliberate and verified. At Immediate.Jobs source commit
`370e187cf3914ab90583d9725669fe38e026337c`, the repository has no release tags,
and the official NuGet flat-container endpoint
`https://api.nuget.org/v3-flatcontainer/immediate.jobs/index.json` returned 404
on 2026-07-30. The preview guidance is therefore authored from the checked-out
source/docs but is not offered for installation until a compatible package set
can be restored and forward-tested.

## Implementation update — 2026-08-12

- Immediate.Jobs guidance is synchronized through source commit
  `ee5f51d86e0056146f3955d0aeea80597ed86ccb`.
- The plugin now contains eight skills. `test-storage-provider` covers the packaged storage checks,
  while `test-job` remains focused on application jobs.
- The Jobs plugin version is `0.1.0-preview.2`. It remains `NOT_AVAILABLE`, and every preview skill
  still disables implicit invocation.
- The activation matrix now covers all 31 repository skills with the same five prompt categories.

## Implementation update, 2026-08-28

- Immediate.Jobs guidance is synchronized through merged source commit
  `32b7b8141e46b4c04dcd3177747ad045709bc5b2`.
- The Jobs skills now use the payload-first scheduler, typed continuation handles, unified monitor,
  dashboard options builder, capturing storage harness, and current handle member names.
- Worker, fair-queue, dashboard, and Redis guidance records both direct options configuration and
  `IConfiguration` binding.
- The Jobs plugin version is `0.1.0-preview.3`. It remains `NOT_AVAILABLE`, and every skill still
  disables implicit invocation.

## Implementation update, 2026-08-29

- Immediate.Jobs 0.5.0 is published on NuGet as a non-prerelease package set.
- The Jobs plugin version is `0.1.0`, and its marketplace entry is `AVAILABLE`.
- Preview labels and explicit-only policies are removed from all eight skills, so they use normal
  automatic discovery.
- Package compatibility checks remain because core, provider, dashboard, NodaTime, and testing
  packages must still use compatible versions.

## Naming and packaging

Use the conceptual namespace `$immediate.<area>:<subskill>`. Codex's actual
plugin and skill identifiers are kebab-cased, so implement that convention as
one plugin per area:

| Conceptual name | Literal Codex invocation | Plugin | Skill |
| --- | --- | --- | --- |
| `$immediate.handlers:create-handler` | `$immediate-handlers:create-handler` | `immediate-handlers` | `create-handler` |
| `$immediate.apis:create-endpoint` | `$immediate-apis:create-endpoint` | `immediate-apis` | `create-endpoint` |
| `$immediate.validations:validate-request` | `$immediate-validations:validate-request` | `immediate-validations` | `validate-request` |
| `$immediate.cache:cache-handler` | `$immediate-cache:cache-handler` | `immediate-cache` | `cache-handler` |
| `$immediate.injections:register-service` | `$immediate-injections:register-service` | `immediate-injections` | `register-service` |
| `$immediate.jobs:create-job` | `$immediate-jobs:create-job` | `immediate-jobs` | `create-job` |
| `$immediate.platform:build-vertical-slice` | `$immediate-platform:build-vertical-slice` | `immediate-platform` | `build-vertical-slice` |

This requires changing the current single-plugin layout into an area-oriented
marketplace. Keep `immediate-platform` for workflows that genuinely cross
package boundaries; do not use it as a container for every package-specific
skill.

The abbreviated layout becomes:

```text
plugins/
  immediate-platform/
    skills/
      build-vertical-slice/
  immediate-handlers/
    skills/
      create-handler/
      create-behavior/
  immediate-apis/
    skills/
      create-endpoint/
  immediate-validations/
    skills/
      validate-request/
  immediate-cache/
    skills/
      cache-handler/
  immediate-injections/
    skills/
      register-service/
  immediate-jobs/
    skills/
      create-job/
```

The combined `plugin-name:skill-name` identifier must remain at most 64
characters. Prefer short, verb-led subskill names.

### Distribution model

Treat the package plugin as the installation and versioning unit, and the
subskill as the invocation unit:

- A user who works only with Immediate.Handlers installs
  `immediate-handlers@immediate`; they do not need to install the API, Cache,
  Injections, Validations, Jobs, or cross-package plugins.
- Installing `immediate-handlers` makes its focused workflows available, but a
  user still selects only the needed one, such as
  `$immediate-handlers:create-behavior`.
- Codex initially sees skill names and descriptions. The full `SKILL.md` body
  and its references are loaded only when that skill is selected, so bundling
  related package workflows does not load every package guide into each task.
- Version and publish each package plugin independently. A change to an API
  workflow should not require a new Handlers or Injections plugin release.
- Keep every package skill self-contained enough to work when it is the only
  Immediate plugin installed. For example, `create-endpoint` may verify that
  the application has an appropriate handler, but it must not require the
  `immediate-handlers` plugin to be installed.
- Offer `immediate-platform` separately for users who want integrated vertical
  slices, multi-host coordination, or cross-package diagnostics.

Do not create one plugin per subskill. That would make every workflow
independently installable, but would turn the first stable version into 23
separate marketplace installations and version streams. Package-level plugins
provide useful opt-in granularity while keeping related workflows discoverable
and maintainable.

## First stable version: core application workflows

These are the foundational skills to implement first. Together they reproduce
the stable Immediate.Dev tutorial as reusable editing workflows. They are only
the first implementation wave within v0.1; the additional stable workflows in
the next section are also required before the first version is complete.

### 1. `$immediate-handlers:create-handler`

**User goal:** Add or update an Immediate.Handlers command, query, or
request/response handler and wire it into dependency injection.

**Include:**

- Static and sealed handler shapes.
- `Handle` and `HandleAsync` rules, commands with implicit responses, and
  cancellation tokens.
- Request, response, and dependency placement.
- Generated `Handler` consumption and `AddXxxHandlers` registration.
- A short diagnostic checklist for invalid handler shapes and DI resolution.

**Keep out:** Behaviors, streaming, HTTP mapping, validation rules, and job
metadata. Route those to their own skills.

**Primary docs:**

- `Immediate.Handlers/creating-handlers.md`
- `Immediate.Handlers/handler-dependencies.md`
- `Immediate.Handlers/registration.md`
- `Immediate.Handlers/diagnostics.md`
- `getting-started/tutorial/first-handler.md`

**Representative prompts:**

- "Create a query handler that loads an order by ID."
- "Convert this static handler to constructor injection."
- "Fix IHR0019 in this handler."

### 2. `$immediate-apis:create-endpoint`

**User goal:** Expose an Immediate.Handlers handler as an ASP.NET Core minimal
API endpoint.

**Include:**

- Verb attributes, routes, route parameters, constraints, and multiple routes.
- Request-data binding inference and explicit binding overrides.
- `TransformResult`, common endpoint metadata, and basic authorization.
- `MapXxxEndpoints` registration.
- Validation exceptions rendered as HTTP `ProblemDetails` when validations are
  already in use.

**Keep out:** Advanced route-group design, broad OpenAPI configuration, and
handler implementation beyond the changes required to map the endpoint.

**Primary docs:**

- `Immediate.Apis/creating-endpoints.md`
- `Immediate.Apis/binding-request-data.md`
- `Immediate.Apis/customizing-endpoints.md`
- `Immediate.Apis/authorization.md`
- `Immediate.Validations/handling-failures.md`
- `getting-started/tutorial/exposing-endpoints.md`

**Representative prompts:**

- "Expose this query at GET /orders/{id}."
- "Bind the tenant ID from a header and the query from the body."
- "Return 201 with a Location header from this command."

### 3. `$immediate-validations:validate-request`

**User goal:** Add compile-time validation to a request or domain input and
integrate it with the handler pipeline when applicable.

**Include:**

- `[Validate]`, `IValidationTarget<T>`, and the built-in validators.
- Nested objects and collection validation.
- Direct validation, `ThrowIfInvalid`, and additional imperative validations.
- `ValidationBehavior<,>` ordering and registration.
- Failure handling and custom messages needed for the request being edited.

**Keep out:** Authoring a new validator attribute and application-wide
localization. Those have different inputs and success criteria.

**Primary docs:**

- `Immediate.Validations/creating-validators.md`
- `Immediate.Validations/built-in-validators.md`
- `Immediate.Validations/nested-and-collection-validation.md`
- `Immediate.Validations/additional-validations.md`
- `Immediate.Validations/validating-instances.md`
- `Immediate.Validations/immediate-handlers-integration.md`
- `Immediate.Validations/handling-failures.md`
- `getting-started/tutorial/adding-validation.md`

**Representative prompts:**

- "Validate this CreateInvoice command."
- "Add validation for every line item and preserve indexed error paths."
- "Run validation before my authorization behavior."

### 4. `$immediate-injections:register-service`

**User goal:** Replace or add hand-written Microsoft DI registrations with
Immediate.Injections attributes.

**Include:**

- Singleton, scoped, and transient registrations.
- Interface registration and the common registration strategies.
- Duplicate strategies and assembly-wide defaults when relevant.
- Generated `AddXxxServices` registration.
- A check that the chosen lifetime is valid for the service's dependencies.

**Keep out:** Keyed services, open generics, factories, proxies, and migrations
from another auto-registration library.

**Primary docs:**

- `Immediate.Injections/registering-services.md`
- `Immediate.Injections/registration-strategies.md`
- `Immediate.Injections/assembly-defaults.md`
- `Immediate.Injections/diagnostics.md`
- `getting-started/tutorial/dependency-injection.md`

**Representative prompts:**

- "Register this repository as scoped behind its interface."
- "Replace these AddSingleton calls with Immediate.Injections."
- "Keep the existing registration when this module is loaded twice."

### 5. `$immediate-cache:cache-handler`

**User goal:** Add an Immediate.Cache wrapper around a query handler and keep
the cache correct when data changes.

**Include:**

- Cache declaration, key transformation, registration, and `AddMemoryCache`.
- Read-through behavior and request coalescing.
- Invalidation from write handlers with `SetValue` and `RemoveValue`.
- `TransformValue` for appropriate read-modify-write cases.
- The fact that a hit skips the entire handler behavior pipeline.

**Keep out:** Exhaustive cache-entry tuning and test-harness construction.

**Primary docs:**

- `Immediate.Cache/creating-a-cache.md`
- `Immediate.Cache/reading-and-writing.md`
- `Immediate.Cache/how-it-works.md`
- `Immediate.Cache/diagnostics.md`
- `getting-started/tutorial/caching.md`

**Representative prompts:**

- "Cache GetProduct by product ID."
- "Invalidate the product cache after UpdateProduct succeeds."
- "Update the cached response without reloading it."

### 6. `$immediate-platform:build-vertical-slice`

**User goal:** Build one complete vertical slice spanning a handler, optional
validation, an API endpoint, registrations, and optional caching.

Implement this after the five atomic skills. It should coordinate their rules,
not duplicate every package reference. It is the entry point for prompts such
as "add a complete CreateOrder feature" where selecting only one package skill
would leave the application incomplete.

**Primary docs:**

- `getting-started/installation.md`
- `getting-started/tutorial/*`
- `concepts/handlers-and-behaviors.md`
- `cookbook/web-api.md`
- `cookbook/blazor.md`
- `cookbook/cli.md`

## First stable version: extensibility workflows

The first version should also include the following focused skills. They are
separate because their triggers, inputs, and success criteria differ from the
foundational workflows above. This gives v0.1 a total of 23 skills across the
six stable-area plugins.

### Immediate.Handlers

| Skill | User goal | Primary docs |
| --- | --- | --- |
| `$immediate-handlers:create-behavior` | Add an ordered cross-cutting pipeline behavior, select handlers with generic constraints, and register the behavior. | `Immediate.Handlers/creating-behaviors.md`, `concepts/handlers-and-behaviors.md` |
| `$immediate-handlers:create-streaming-handler` | Create or update an `IAsyncEnumerable<T>` handler and any matching streaming behaviors. | `Immediate.Handlers/streaming-handlers.md`, `Immediate.Handlers/attributes-and-interfaces.md` |
| `$immediate-handlers:configure-registration` | Choose lifetimes, register one handler or a subset, and apply handler tags without accidentally broadening a host. | `Immediate.Handlers/registration.md`, `Immediate.Handlers/tagged-registration.md`, `concepts/tags.md` |

`create-behavior` must explain that the first behavior listed is outermost,
handler-level `[Behaviors]` replaces rather than extends the assembly list, and
generic constraints determine whether a behavior is generated into a pipeline.

### Immediate.Apis

| Skill | User goal | Primary docs |
| --- | --- | --- |
| `$immediate-apis:customize-endpoint` | Add rich endpoint metadata, conventions, or response transformations with attributes, `CustomizeEndpoint`, and `TransformResult`. | `Immediate.Apis/customizing-endpoints.md`, `Immediate.Apis/attributes-reference.md` |
| `$immediate-apis:create-route-group` | Share route prefixes and conventions across related endpoints with `[RouteGroup]` and `[MapGroup]`. | `Immediate.Apis/route-groups.md`, `Immediate.Apis/tagged-registration.md` |
| `$immediate-apis:configure-openapi` | Resolve nested-type schema ID collisions and describe generated endpoints for Swashbuckle or Microsoft OpenAPI/Scalar. | `Immediate.Apis/openapi.md`, `Immediate.Handlers/openapi-and-swashbuckle.md` |

`create-endpoint` continues to own basic binding, authorization, metadata, and
result transformation needed while exposing one handler. Route-group design,
substantial endpoint customization, and application-wide OpenAPI changes route
to the narrower skills above.

### Immediate.Validations

| Skill | User goal | Primary docs |
| --- | --- | --- |
| `$immediate-validations:create-custom-validator` | Implement a validator attribute, its validation method contract, `TargetType`, messages, and analyzer-required shape. | `Immediate.Validations/custom-validators.md`, `Immediate.Validations/diagnostics.md`, `Immediate.Validations/api-reference.md` |
| `$immediate-validations:localize-validation` | Configure built-in or custom validation messages with `IStringLocalizer` and supported cultures. | `Immediate.Validations/localization.md`, `Immediate.Validations/custom-messages.md` |
| `$immediate-validations:handle-failure` | Translate `ValidationException` consistently in HTTP or non-HTTP applications without losing property errors. | `Immediate.Validations/handling-failures.md`, `Immediate.Validations/api-reference.md` |

`create-custom-validator` is part of v0.1 because it is a distinct extension
contract enforced primarily by analyzers; folding it into `validate-request`
would make both activation and implementation less reliable.

### Immediate.Cache

| Skill | User goal | Primary docs |
| --- | --- | --- |
| `$immediate-cache:configure-entry` | Tune expiration, size, priority, and eviction callbacks for a generated cache. | `Immediate.Cache/cache-entry-options.md`, `Immediate.Cache/api-reference.md` |
| `$immediate-cache:test-cache` | Compose a real service collection and test generated caches, handlers, invalidation, and cache-hit behavior. | `Immediate.Cache/testing-caches.md`, `Immediate.Cache/how-it-works.md` |

### Immediate.Injections

| Skill | User goal | Primary docs |
| --- | --- | --- |
| `$immediate-injections:register-keyed-service` | Add and resolve several implementations under distinct DI keys. | `Immediate.Injections/keyed-services.md`, `Immediate.Injections/attributes-reference.md` |
| `$immediate-injections:register-open-generic` | Register an open generic service and select the intended service types and lifetime. | `Immediate.Injections/open-generics.md`, `Immediate.Injections/registration-strategies.md` |
| `$immediate-injections:create-factory-or-proxy` | Construct a service with a factory or forward one registration through a proxy safely. | `Immediate.Injections/factories-and-proxies.md` |
| `$immediate-injections:add-manual-registration` | Join necessary hand-written registrations to the generated `AddXxxServices` method. | `Immediate.Injections/manual-registration.md`, `Immediate.Injections/how-it-works.md` |

### Cross-package platform skills

| Skill | User goal | Primary docs |
| --- | --- | --- |
| `$immediate-platform:configure-host-slices` | Coordinate tags across handlers, endpoints, services, and later jobs in multi-host assemblies. | `concepts/tags.md` and each stable package's tagged-registration guide |
| `$immediate-platform:diagnose-generation` | Investigate generated output, assembly identifiers, analyzer diagnostics, OpenAPI collisions, and DI failures when the owning package is unclear. | `concepts/source-generation.md`, `concepts/assembly-identifier.md`, package diagnostics and `how-it-works` guides |

Do not initially create one `fix-diagnostics` skill per package. The core skills
should handle common diagnostics for the workflow they own, while
`diagnose-generation` handles cross-package or unclear failures. Split out a
package diagnostic skill later only if real usage shows a distinct trigger.

## Immediate.Jobs release

The Jobs plugin is available after all eight skills were implemented and tested
against the restorable Immediate.Jobs 0.5.0 packages. Keep its package version
checks because companion packages and providers must remain compatible.

The Jobs skills were implemented in this order:

| Order | Skill | Goal | Primary docs |
| --- | --- | --- | --- |
| 1 | `$immediate-jobs:create-job` | Declare payload or payloadless jobs, stable names, retries, timeouts, registration, and idempotent handling. | `creating-jobs`, `registration-and-hosting`, `delivery-guarantees` |
| 2 | `$immediate-jobs:schedule-job` | Enqueue immediate, delayed, absolute, and fair-group work with generated schedulers. | `enqueueing-and-scheduling`, `queues-and-fairness` |
| 3 | `$immediate-jobs:test-job` | Test scheduling and execution with fake time, draining, captures, and workflow assertions. | `testing-jobs` |
| 4 | `$immediate-jobs:create-recurring-job` | Define cron schedules, time zones, overlap policy, reconciliation, and manual triggers. | `recurring-jobs`, `nodatime` |
| 5 | `$immediate-jobs:build-workflow` | Build atomic batches, continuations, chains, fan-out/fan-in, and dynamic expansion. | `batches-and-continuations` |
| 6 | `$immediate-jobs:configure-storage` | Choose and configure in-memory, EF Core, LinqToDB, or Redis storage with clear capability tradeoffs. | `choosing-storage`, `configuring-storage-providers` |
| 7 | `$immediate-jobs:operate-jobs` | Secure monitoring, add observability and health checks, and reason about worker lifecycle and delivery guarantees. | `dashboard-and-monitoring`, `observability-and-health`, `delivery-guarantees` |
| 8 | `$immediate-jobs:test-storage-provider` | Run the public storage checks against an isolated custom-provider fixture. | `testing-jobs`, `choosing-storage`, `api-reference` |

`create-job` must explicitly guard the two most consequential pitfalls from the
docs: Jobs registration does not replace Handlers registration, and delivery is
at least once, so handlers must be idempotent.

## Later candidates

Only add these after representative user requests justify them:

- `$immediate-platform:migrate-application` for migrations from MediatR,
  FluentValidation, Injectio, or AutoRegisterInject. The existing docs cover
  these unevenly, so one broad migration skill would otherwise overpromise.
- `$immediate-platform:implement-pub-sub` for the documented flexible
  publish-subscribe pattern.
- `$immediate-platform:scaffold-application` for complete Web API, Blazor, CLI,
  or full-stack VSA applications. Start with `build-vertical-slice`; a whole-app
  scaffold needs stronger templates and broader forward testing.
- Package-specific diagnostic skills if activation data shows that users ask
  by diagnostic ID more often than by the task they were performing.

## Authoring pattern for every skill

Each skill should contain only the resources it needs:

```text
<skill-name>/
  SKILL.md
  agents/
    openai.yaml
  references/          # only when details do not fit cleanly in SKILL.md
```

Use this authoring contract:

1. Put the user goal, concrete triggers, and important exclusions in the
   frontmatter `description`.
2. Keep `SKILL.md` procedural and concise: inspect the project, choose the
   supported pattern, edit the code, register generated services, build, and
   report the result.
3. Distill only the relevant Immediate.Dev material into references. Do not
   copy the entire package manual into every skill or depend on the
   Immediate.Dev checkout being present after installation.
4. Record the source Immediate.Dev pages at the bottom of each reference so
   updates remain traceable.
5. Prefer instruction-only skills initially. Add scripts only when repeated
   implementation shows a deterministic helper is safer than ordinary code
   editing.
6. Inspect the target project's framework, package versions, generated method
   names, nullable settings, and existing patterns before making changes.
7. Treat the checked-out application's code and installed package version as
   authoritative when they differ from prerelease or newer documentation. Call
   out the mismatch instead of silently writing incompatible code.
8. Verify edits with the narrowest relevant build or tests. Analyzer warnings
   and generated-code failures are part of the result, not incidental output.

## Validation and release gates

A skill is ready only when all of these pass:

1. **Structure:** `SKILL.md` frontmatter, directory name, and
   `agents/openai.yaml` are valid.
2. **Activation:** Test direct, indirect, incomplete, negative, and edge-case
   prompts. Closely related skills must not all activate for the same simple
   request.
3. **Forward test:** Give the skill and a realistic application request to a
   fresh agent without the expected answer. Review the resulting patch rather
   than only its prose.
4. **Compilation:** Build the edited fixture or cookbook application and run
   focused tests where available.
5. **Documentation traceability:** Confirm every prescribed API is supported
   by the mapped Immediate.Dev pages and by the package version under test.
6. **Repository validation:** Run `python3 scripts/validate.py` after every
   structural or metadata change.
7. **Publishing:** Increment only the affected plugin's semantic version. Mark
   that marketplace entry `AVAILABLE` only after it contains at least one
   complete skill. Gate any plugin whose documented package baseline cannot be
   restored.
8. **Package isolation:** Test each package plugin with no other Immediate
   plugin installed. Its skills may recognize related application code, but
   must not depend on another plugin's instructions or bundled references.

For the first stable version, use the Immediate.Dev Todo tutorial and Web API
cookbook as the main end-to-end positive fixtures. Add focused fixtures for
behaviors, streaming, route groups, custom validators, keyed/open-generic
registrations, and cache tests. Add at least one negative activation prompt
from a neighboring area for each skill, such as ensuring `create-handler` does
not own an endpoint-only request.

## Implementation sequence

1. Confirm the existing repository validator covers multiple area plugins, then
   add the new plugins to the marketplace.
2. Scaffold the five stable area plugins, leaving them `NOT_AVAILABLE` while
   empty.
3. Implement and forward-test `create-handler` as the pilot skill.
4. Complete the Handlers family with `create-behavior`,
   `create-streaming-handler`, and `configure-registration`.
5. Implement `validate-request`, `create-custom-validator`,
   `localize-validation`, and `handle-failure`.
6. Implement the APIs family: `create-endpoint`, `customize-endpoint`,
   `create-route-group`, and `configure-openapi`. Test the Handler, Validation,
   and API skills together on several vertical slices.
7. Implement the Injections and Cache families, including their v0.1
   extensibility and testing skills.
8. Implement `build-vertical-slice`, `configure-host-slices`, and
   `diagnose-generation` using the proven atomic boundaries.
9. Run activation tests across all 23 skills, forward-test representative
   editing tasks, test every package plugin in isolation, and compile every
   changed fixture.
10. Publish only the stable plugins that pass their individual release gates.
11. Add post-v0.1 skills based on observed demand.
12. Publish the Jobs plugin after its 0.5.0 package and API baseline restores
   and the representative workflows pass their release checks.

## Source baseline

This plan is based on the checked-out documentation under
`Immediate.Dev/src/content/docs`, especially the getting-started tutorial, the
six package guides, the shared concepts, and the cookbook examples. The naming
layout also follows Codex's documented `plugin-name:skill-name` identity and
kebab-case plugin naming rules.
