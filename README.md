# Immediate.Skills

Team-maintained agent skills for building applications with the
[Immediate.Platform](https://github.com/ImmediatePlatform) libraries.

The repository is a Git-backed Codex plugin marketplace. Its skills describe how
to consume Immediate libraries in applications; library maintenance workflows
belong in their respective source repositories.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/
  immediate-platform/
    .codex-plugin/plugin.json
    skills/
  immediate-handlers/
  immediate-apis/
  immediate-validations/
  immediate-cache/
  immediate-injections/
  immediate-jobs/
scripts/validate.py
```

The stable packages are separate plugins so teams can install only the
Immediate libraries they use. `immediate-platform` contains cross-package
workflows. `immediate-jobs` is independently versioned and remains unavailable
while Immediate.Jobs itself is an unreleased preview.

## Install

Add this repository as a marketplace, then install one or more package plugins:

```sh
codex plugin marketplace add ImmediatePlatform/Immediate.Skills --ref main
codex plugin add immediate-handlers@immediate
codex plugin add immediate-apis@immediate
codex plugin add immediate-validations@immediate
codex plugin add immediate-cache@immediate
codex plugin add immediate-injections@immediate
codex plugin add immediate-platform@immediate
```

Each plugin exposes focused invocations such as
`$immediate-handlers:create-handler` or
`$immediate-validations:create-custom-validator`. Installing one package
plugin does not require any of the others.

Run `codex plugin marketplace upgrade immediate` to pick up later published
versions, then reinstall the plugin when required by Codex.

## Contribute

Add each skill under `plugins/<package-plugin>/skills/<skill-name>/`. Every
skill must contain `SKILL.md` and `agents/openai.yaml`; optional `references/`,
`scripts/`, and `assets/` directories belong inside that skill.

Use `$skill-creator` in Codex when creating or substantially revising a skill.
Keep skills focused on application-facing workflows and validate the repository
before opening a pull request:

```sh
python3 scripts/validate.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the publishing checklist.
