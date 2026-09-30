# Immediate.Skills

Team-maintained agent skills for building applications with the
[Immediate.Platform](https://github.com/ImmediatePlatform) libraries.

The repository is a Git-backed plugin marketplace for both Codex and Claude Code.
Its skills describe how to consume Immediate libraries in applications; library
maintenance workflows belong in their respective source repositories.

## Repository layout

```text
.agents/plugins/marketplace.json     # Codex marketplace
.claude-plugin/marketplace.json      # Claude Code marketplace
plugins/
  immediate-platform/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    skills/
  immediate-handlers/
  immediate-apis/
  immediate-validations/
  immediate-cache/
  immediate-injections/
  immediate-jobs/
scripts/validate.py
```

The packages are separate plugins so teams can install only the Immediate
libraries they use. `immediate-platform` contains cross-package workflows, and
`immediate-jobs` follows the independently versioned Immediate.Jobs releases.

## Install

Both agents read the same `skills/` directories, so a skill behaves the same in
either tool.

### Claude Code

Add this repository as a marketplace, then install one or more package plugins:

```sh
claude plugin marketplace add ImmediatePlatform/Immediate.Skills
claude plugin install immediate-handlers@immediate
claude plugin install immediate-apis@immediate
claude plugin install immediate-validations@immediate
claude plugin install immediate-cache@immediate
claude plugin install immediate-injections@immediate
claude plugin install immediate-jobs@immediate
claude plugin install immediate-platform@immediate
```

The same commands work inside a session as `/plugin marketplace add ...` and
`/plugin install ...`, or browse the marketplace with `/plugin`. Skills load
automatically when relevant and can be invoked directly, for example
`/immediate-handlers:create-handler`. Run `claude plugin marketplace update
immediate` to pick up later published versions.

To share the marketplace with a team, add it to the project's
`.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "immediate": {
      "source": { "source": "github", "repo": "ImmediatePlatform/Immediate.Skills" }
    }
  },
  "enabledPlugins": {
    "immediate-handlers@immediate": true
  }
}
```

### Codex

Add this repository as a marketplace, then install one or more package plugins:

```sh
codex plugin marketplace add ImmediatePlatform/Immediate.Skills --ref main
codex plugin add immediate-handlers@immediate
codex plugin add immediate-apis@immediate
codex plugin add immediate-validations@immediate
codex plugin add immediate-cache@immediate
codex plugin add immediate-injections@immediate
codex plugin add immediate-jobs@immediate
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
plugin keeps matching `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`
manifests, and every skill must contain `SKILL.md` and `agents/openai.yaml`; optional `references/`,
`scripts/`, and `assets/` directories belong inside that skill.

Use `$skill-creator` in Codex when creating or substantially revising a skill.
Keep skills focused on application-facing workflows and validate the repository
before opening a pull request:

```sh
python3 scripts/validate.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the publishing checklist.
