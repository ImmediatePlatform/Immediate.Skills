# Skill test evidence

`activation-prompts.json` is the activation-boundary matrix. Every skill owns
exactly five prompt shapes:

- `direct` names the literal `$plugin:skill` identity.
- `indirect` describes the complete task without naming the skill.
- `incomplete` checks discovery from a short but recognizable request.
- `negative` belongs to a neighboring workflow and should not select the skill.
- `edge` exercises an important boundary or failure mode.

`python3 scripts/validate.py` checks exact skill coverage and the shape of every
case. Human or agent evaluation is still required to assess semantic routing;
the JSON file is test input, not a claim that string matching proves activation.

## Forward tests — 2026-07-30

Three fresh-agent edits were run in isolated copies of the Immediate.Dev
cookbook. The copies are disposable and are not committed here.

| Skill | Fixture/request | Result | Guidance refined from the test |
| --- | --- | --- | --- |
| `$immediate-handlers:create-handler` | CLI query with constructor-injected cryptographic RNG and configurable count | Build 0 warnings/errors; smoke run returned the requested count | Report old-package incompatibility before upgrading or changing the requested handler shape. |
| `$immediate-apis:create-route-group` | Put four Todo endpoints under an authorized `api/todos` group | Generated mapping verified; build 0 warnings/errors | Coordinate package upgrades, document the root constant's trailing slash, and do not invent missing policy semantics. |
| `$immediate-validations:create-custom-validator` | Reusable configurable Todo title validator | Analyzer/compiler build 0 warnings/errors | Clarify built-in overlap, invalid configuration, null composition, and evidence when no test project exists. |

The first two cookbook fixtures used older package generations that did not
contain the requested APIs. Their successful experimental upgrades proved the
current documented shapes, while the production skills now treat dependency
upgrades as a separately reported application decision.

## Cross-skill audits — 2026-07-30

- Activation review evaluated all five cases for all 30 skills. Nine initial
  neighbor collisions were narrowed; re-review found no residual collision in
  those cases.
- Package-isolation review checked 30 skill links and all seven manifests. No
  missing, external, cross-plugin, or symlinked resource dependency exists.
- Documentation review resolved 111 exact Immediate.Dev citations and
  spot-checked high-risk APIs against docs and source. Three Jobs API-name
  errors found by that review were corrected before release gating.

## Immediate.Jobs forward tests — 2026-08-12

Three fresh agents used the updated preview skills without editing either
repository. Their answers were checked against Immediate.Jobs source commit
`ee5f51d86e0056146f3955d0aeea80597ed86ccb`.

| Skill | Scenario | Result | Guidance refined from the test |
| --- | --- | --- | --- |
| `$immediate-jobs:test-storage-provider` | xUnit catalog for a custom Redis provider with queue and recurring support | Correctly selected `Queue | Recurring` and produced one test row per case | Name the fake-time namespace/package and keep connection, data identifier, service provider, and cleanup in one fixture. |
| `$immediate-jobs:configure-storage` | EF Core across three worker processes with bound options, fair queues, and readiness | Correctly selected distributed mode and fluent configuration | Require `AddDbContextFactory`, tag-filter readiness mapping, and the `ee5f51d` health-check options bridge. |
| `$immediate-jobs:create-recurring-job` | Trigger a payloadless job by stable name when tags exclude some jobs | Correctly used generated `RecurringJobs` and stable job identity | State no-tag registration semantics, case-sensitive names, failure timing, payloadless scope, and provider-qualified reconciliation. |

## Immediate.Jobs forward tests, 2026-08-28

Three fresh agents used the revised preview skills without editing either
repository. Their answers were checked against Immediate.Jobs source commit
`32b7b8141e46b4c04dcd3177747ad045709bc5b2`.

| Skill | Scenario | Result | Guidance refined from the test |
| --- | --- | --- | --- |
| `$immediate-jobs:build-workflow` | Open-batch fan-in followed by a delayed durable continuation with mixed job and batch parents | Correctly used synchronous batch scheduling, typed handles, one commit, and `ScheduleAfterAsync` | Document exact argument order, distinguish the second durable write from the atomic commit, and state that in-memory graphs do not survive process loss. |
| `$immediate-jobs:configure-storage` and `$immediate-jobs:operate-jobs` | Distributed EF Core workers with configuration binding, fair queues, health, dashboard authorization, and telemetry links | Correctly selected distributed mode and the current fluent APIs | Explain that bound `FairQueueOptions.Enabled` applies after `UseFairQueues`, and keep deployment replica count outside Immediate.Jobs options. |
| `$immediate-jobs:test-job` | Delayed grouped scheduling, captured-write assertions, fake-time draining, and durable-state checks | Correctly used the generated scheduler, `Captures`, fake time, and harness queries | Resolve scoped schedulers through an async scope and clarify that `Clear()` removes capture history without deleting durable in-memory state. |
