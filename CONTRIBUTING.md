# Contributing

## Add a skill

1. Select the package plugin that owns the workflow, or `immediate-platform`
   for a genuinely cross-package task. Create
   `plugins/<plugin>/skills/<skill-name>/SKILL.md` using a lowercase,
   hyphenated, action-oriented name.
2. Put precise triggering guidance in the frontmatter `description`.
3. Keep the main workflow concise. Put detailed, selectively loaded material in
   `references/` and deterministic helpers in `scripts/`.
4. Add `agents/openai.yaml` with user-facing display metadata.
5. Add direct, indirect, incomplete, negative, and edge prompts to
   `tests/activation-prompts.json` and test a realistic edit with a fresh agent.
6. Run `python3 scripts/validate.py`.

Do not add library release procedures, generator maintenance instructions, or
repository-specific build matrices here. Keep those instructions with the
library source repository.

## Publish plugin changes

1. Ensure every changed skill and its package-isolation checks are ready for
   team use.
2. Increment only the affected plugin manifest using semantic versioning.
3. Change that marketplace entry from `NOT_AVAILABLE` to `AVAILABLE` only when
   its release gate passes. Keep preview plugins independently gated.
4. Run `python3 scripts/validate.py`.
5. Merge the change and create a matching Git tag when a stable version should
   be pinned by consumers.

Do not add an empty or unfinished skill to make the plugin installable.

## Preview packages

Preview skills must identify their package baseline and failure mode, disable
implicit invocation when the API is not generally available, and stay
`NOT_AVAILABLE` until the documented packages can be restored and forward
tested together. Do not let a preview plugin block stable package releases.
