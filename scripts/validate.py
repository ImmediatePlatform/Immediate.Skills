#!/usr/bin/env python3
"""Validate the Immediate.Skills marketplace, plugins, and skill metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
ACTIVATION_PATH = ROOT / "tests" / "activation-prompts.json"
IMMEDIATE_DOCS = ROOT.parent / "Immediate.Dev" / "src" / "content" / "docs"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLUGIN_NAME = SKILL_NAME
TODO_MARKERS = ("[TODO", "TODO:")
ACTIVATION_CASES = {"direct", "indirect", "incomplete", "negative", "edge"}


def load_json(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing {path.relative_to(ROOT)}")
        return None
    except json.JSONDecodeError as error:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {error}")
        return None

    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return None
    return value


def require_string(
    value: dict[str, object], key: str, location: str, errors: list[str]
) -> str | None:
    result = value.get(key)
    if not isinstance(result, str) or not result.strip():
        errors.append(f"{location}.{key} must be a non-empty string")
        return None
    return result


def yaml_string(content: str, key: str) -> str | None:
    match = re.search(
        rf'^\s*{re.escape(key)}:\s*[\'\"](?P<value>[^\'\"]+)[\'\"]\s*$',
        content,
        re.MULTILINE,
    )
    return match.group("value").strip() if match is not None else None


def validate_skill(
    plugin_name: str, skill_dir: Path, preview: bool, errors: list[str]
) -> None:
    skill_file = skill_dir / "SKILL.md"
    location = skill_dir.relative_to(ROOT)
    if not skill_file.is_file():
        errors.append(f"{location} is missing SKILL.md")
        return

    content = skill_file.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if frontmatter is None:
        errors.append(f"{location}/SKILL.md has invalid YAML frontmatter delimiters")
        return

    body = frontmatter.group("body")
    keys = re.findall(r"^([A-Za-z0-9_-]+):", body, re.MULTILINE)
    if sorted(keys) != ["description", "name"]:
        errors.append(f"{location}/SKILL.md frontmatter must contain only name and description")
    name_match = re.search(r"^name:\s*['\"]?([^'\"\n]+)['\"]?\s*$", body, re.MULTILINE)
    description_match = re.search(
        r"^description:\s*['\"]?([^'\"\n]+)['\"]?\s*$", body, re.MULTILINE
    )
    if name_match is None:
        errors.append(f"{location}/SKILL.md is missing a single-line name")
    else:
        name = name_match.group(1).strip()
        if name != skill_dir.name:
            errors.append(f"{location}/SKILL.md name must match its directory")
        if len(name) > 64 or SKILL_NAME.fullmatch(name) is None:
            errors.append(f"{location}/SKILL.md name must be valid lowercase hyphen-case")
    if description_match is None or not description_match.group(1).strip():
        errors.append(f"{location}/SKILL.md is missing a single-line description")
    elif len(description_match.group(1).strip()) < 40:
        errors.append(f"{location}/SKILL.md description is too short to trigger reliably")

    instructions = content[frontmatter.end() :].strip()
    if len(instructions) < 200:
        errors.append(f"{location}/SKILL.md instructions are incomplete")
    if any(marker in content for marker in TODO_MARKERS):
        errors.append(f"{location}/SKILL.md contains a TODO placeholder")

    identity = f"{plugin_name}:{skill_dir.name}"
    if len(identity) > 64:
        errors.append(f"{location} combined identity {identity!r} exceeds 64 characters")

    agent_file = skill_dir / "agents" / "openai.yaml"
    try:
        agent_content = agent_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"{location} is missing agents/openai.yaml")
    else:
        display_name = yaml_string(agent_content, "display_name")
        short_description = yaml_string(agent_content, "short_description")
        default_prompt = yaml_string(agent_content, "default_prompt")
        if display_name is None:
            errors.append(f"{location}/agents/openai.yaml is missing display_name")
        if short_description is None or not 25 <= len(short_description) <= 64:
            errors.append(
                f"{location}/agents/openai.yaml short_description must be 25-64 characters"
            )
        if default_prompt is None or f"${identity}" not in default_prompt:
            errors.append(
                f"{location}/agents/openai.yaml default_prompt must mention ${identity}"
            )
        if any(marker in agent_content for marker in TODO_MARKERS):
            errors.append(f"{location}/agents/openai.yaml contains a TODO placeholder")
        if preview and not re.search(
            r"^\s*allow_implicit_invocation:\s*false\s*$",
            agent_content,
            re.MULTILINE,
        ):
            errors.append(
                f"{location}/agents/openai.yaml must disable implicit invocation for preview APIs"
            )

    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        reference_files = sorted(references_dir.glob("*.md"))
        if not reference_files:
            errors.append(f"{location}/references must contain a Markdown reference or be removed")
        for reference_file in reference_files:
            reference = reference_file.read_text(encoding="utf-8")
            if "Immediate.Dev:" not in reference:
                errors.append(
                    f"{reference_file.relative_to(ROOT)} must record its Immediate.Dev sources"
                )
            if IMMEDIATE_DOCS.is_dir():
                for source in re.findall(r"Immediate\.Dev: `([^`]+)`", reference):
                    if "*" not in source and not (IMMEDIATE_DOCS / source).is_file():
                        errors.append(
                            f"{reference_file.relative_to(ROOT)} references missing Immediate.Dev/{source}"
                        )


def validate_plugin(plugin_dir: Path, errors: list[str]) -> str | None:
    location = plugin_dir.relative_to(ROOT)
    manifest = load_json(plugin_dir / ".codex-plugin" / "plugin.json", errors)
    if manifest is None:
        return None

    name = require_string(manifest, "name", str(location), errors)
    version = require_string(manifest, "version", str(location), errors)
    require_string(manifest, "description", str(location), errors)
    if name is not None and name != plugin_dir.name:
        errors.append(f"{location} name must match its directory")
    if name is not None and (
        len(name) > 64 or PLUGIN_NAME.fullmatch(name) is None
    ):
        errors.append(f"{location} name must be valid lowercase hyphen-case")
    if version is not None and SEMVER.fullmatch(version) is None:
        errors.append(f"{location} version must use semantic versioning")
    if manifest.get("skills") != "./skills/":
        errors.append(f"{location} skills must be ./skills/")

    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        errors.append(f"{location} is missing its skills directory")
        return version
    preview = version is not None and "-" in version
    for child in sorted(skills_dir.iterdir()):
        if child.name.startswith("."):
            continue
        if child.is_dir():
            validate_skill(plugin_dir.name, child, preview, errors)
        else:
            errors.append(f"{child.relative_to(ROOT)} must be inside a skill directory")
    return version


def validate_activation_prompts(identities: set[str], errors: list[str]) -> None:
    matrix = load_json(ACTIVATION_PATH, errors)
    if matrix is None:
        return

    matrix_identities = set(matrix)
    for identity in sorted(identities - matrix_identities):
        errors.append(f"tests/activation-prompts.json is missing {identity}")
    for identity in sorted(matrix_identities - identities):
        errors.append(f"tests/activation-prompts.json references unknown {identity}")

    for identity, cases in matrix.items():
        location = f"activation prompt {identity}"
        if not isinstance(cases, dict):
            errors.append(f"{location} must be an object")
            continue
        case_names = set(cases)
        if case_names != ACTIVATION_CASES:
            errors.append(
                f"{location} must contain exactly {', '.join(sorted(ACTIVATION_CASES))}"
            )
        for case_name in ACTIVATION_CASES:
            prompt = cases.get(case_name)
            if not isinstance(prompt, str) or len(prompt.strip()) < 12:
                errors.append(f"{location}.{case_name} must be a useful prompt")
        direct = cases.get("direct")
        if isinstance(direct, str) and f"${identity}" not in direct:
            errors.append(f"{location}.direct must name ${identity}")
        negative = cases.get("negative")
        if isinstance(negative, str) and f"${identity}" in negative:
            errors.append(f"{location}.negative must not name ${identity}")


def main() -> int:
    errors: list[str] = []
    marketplace = load_json(MARKETPLACE_PATH, errors)
    plugins_root = ROOT / "plugins"

    marketplace_names: list[str] = []
    installation_by_name: dict[str, str] = {}
    if marketplace is not None:
        require_string(marketplace, "name", "marketplace", errors)
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            errors.append("marketplace.plugins must be an array")
        else:
            for index, entry in enumerate(entries):
                location = f"marketplace.plugins[{index}]"
                if not isinstance(entry, dict):
                    errors.append(f"{location} must be an object")
                    continue
                name = require_string(entry, "name", location, errors)
                if name is not None:
                    marketplace_names.append(name)
                source = entry.get("source")
                if not isinstance(source, dict) or source.get("source") != "local":
                    errors.append(f"{location}.source must describe a local plugin")
                    continue
                path = source.get("path")
                expected = f"./plugins/{name}" if name is not None else None
                if path != expected:
                    errors.append(f"{location}.source.path must be {expected}")
                policy = entry.get("policy")
                if not isinstance(policy, dict):
                    errors.append(f"{location}.policy must be an object")
                elif policy.get("installation") not in {
                    "AVAILABLE",
                    "INSTALLED_BY_DEFAULT",
                    "NOT_AVAILABLE",
                }:
                    errors.append(f"{location}.policy.installation is invalid")
                elif policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
                    errors.append(f"{location}.policy.authentication is invalid")
                elif name is not None:
                    installation_by_name[name] = str(policy.get("installation"))
                if entry.get("category") != "Developer Tools":
                    errors.append(f"{location}.category must be Developer Tools")

        duplicates = sorted(
            name for name in set(marketplace_names) if marketplace_names.count(name) > 1
        )
        for name in duplicates:
            errors.append(f"marketplace contains duplicate plugin {name}")

    if not plugins_root.is_dir():
        errors.append("Missing plugins directory")
    else:
        plugin_dirs = sorted(path for path in plugins_root.iterdir() if path.is_dir())
        plugin_names = [path.name for path in plugin_dirs]
        missing_entries = sorted(set(plugin_names) - set(marketplace_names))
        missing_plugins = sorted(set(marketplace_names) - set(plugin_names))
        for name in missing_entries:
            errors.append(f"plugins/{name} is missing from the marketplace")
        for name in missing_plugins:
            errors.append(f"marketplace references missing plugins/{name}")
        for plugin_dir in plugin_dirs:
            if plugin_dir.is_dir():
                version = validate_plugin(plugin_dir, errors)
                installation = installation_by_name.get(plugin_dir.name)
                has_skills = any((plugin_dir / "skills").glob("*/SKILL.md"))
                if version is not None and "-" in version:
                    if installation != "NOT_AVAILABLE":
                        errors.append(
                            f"preview plugin {plugin_dir.name} must remain NOT_AVAILABLE"
                        )
                elif has_skills and installation == "NOT_AVAILABLE":
                    errors.append(
                        f"stable plugin {plugin_dir.name} has complete skills but is NOT_AVAILABLE"
                    )

        identities = {
            f"{plugin_dir.name}:{skill_file.parent.name}"
            for plugin_dir in plugin_dirs
            for skill_file in (plugin_dir / "skills").glob("*/SKILL.md")
        }
        validate_activation_prompts(identities, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Immediate.Skills validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
