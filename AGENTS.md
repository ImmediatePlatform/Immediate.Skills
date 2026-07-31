# Immediate.Skills repository guidance

This repository distributes team-maintained skills for consuming the
Immediate.Platform libraries in application code.

## Scope

- Add application-facing workflows for Immediate.Apis, Immediate.Handlers,
  Immediate.Injections, Immediate.Jobs, and related libraries.
- Keep library implementation, release, analyzer, generator, and build-matrix
  maintenance guidance in the corresponding source repository.
- Keep each skill focused on one coherent task and follow the Agent Skills
  `SKILL.md` format.

## Layout

- Put skills under `plugins/<package-plugin>/skills/<skill-name>/`.
- Keep each plugin manifest at `plugins/<package-plugin>/.codex-plugin/plugin.json`.
- Use `immediate-platform` only for workflows that coordinate more than one
  package. Keep package skills usable when no other Immediate plugin is installed.
- Keep the team marketplace at `.agents/plugins/marketplace.json`.

## Changes

- Use `$skill-creator` when creating or substantially updating a skill.
- Increment only the affected plugin's semantic version when publishing skill changes.
- Leave marketplace installation as `NOT_AVAILABLE` until at least one complete
  skill exists; use `AVAILABLE` for team releases.
- Keep unreleased or non-restorable preview package plugins `NOT_AVAILABLE` and
  disable implicit invocation in their skills.
- Maintain the five activation-prompt categories for every skill and forward-test
  representative application edits after substantial revisions.
- Run `python3 scripts/validate.py` after every structural or metadata change.
