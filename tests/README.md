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
