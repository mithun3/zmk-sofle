#!/usr/bin/env python3
"""Sync and validate the Claude customizations. Standard library only.

  python3 .claude/scripts/customizations.py sync    write Copilot mirrors and the skills symlink
  python3 .claude/scripts/customizations.py check   validate everything and run hook self-tests
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLAUDE = os.path.join(ROOT, ".claude")
SKILLS_DIR = os.path.join(CLAUDE, "skills")
AGENTS_DIR = os.path.join(CLAUDE, "agents")
HOOKS_DIR = os.path.join(CLAUDE, "hooks")
EVALS_DIR = os.path.join(CLAUDE, "evals")
GH_AGENTS = os.path.join(ROOT, ".github", "agents")
GH_SKILLS = os.path.join(ROOT, ".github", "skills")

CLAUDE_TOOLS = {"Read", "Grep", "Glob", "Bash", "Edit", "Write", "WebFetch", "WebSearch", "Agent"}
COPILOT_TOOLS = {
    "Read": "read", "Grep": "search", "Glob": "search", "Bash": "execute",
    "Edit": "edit", "Write": "edit", "WebFetch": "web", "WebSearch": "web", "Agent": "agent",
}
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")

# (script, payload, expected exit code). Payloads cover Claude and Copilot shapes.
HOOK_CASES = [
    ("readonly-bash-guard.py", {"tool_name": "Bash", "tool_input": {"command": "git status"}}, 0),
    ("readonly-bash-guard.py", {"tool_name": "Bash", "tool_input": {"command": "grep -r foo config | head -5"}}, 0),
    ("readonly-bash-guard.py", {"tool_name": "Bash", "tool_input": {"command": "west flash"}}, 2),
    ("readonly-bash-guard.py", {"tool_name": "Bash", "tool_input": {"command": "ls > out.txt"}}, 2),
    ("readonly-bash-guard.py", {"tool_name": "Bash", "tool_input": {"command": "find . -delete"}}, 2),
    ("readonly-bash-guard.py", {"tool_name": "Bash", "tool_input": {"command": "git push"}}, 2),
    ("readonly-bash-guard.py", "not json", 2),
    ("block-flash.py", {"tool_name": "Bash", "tool_input": {"command": "west flash"}}, 2),
    ("block-flash.py", {"tool_name": "Bash", "tool_input": {"command": "west build -b nice_nano_v2 -- -DSHIELD=corne_left"}}, 0),
    ("block-flash.py", {"tool_name": "Bash", "tool_input": {"command": "cp zmk.uf2 /Volumes/NICENANO/"}}, 2),
    ("block-flash.py", {"toolName": "run_in_terminal", "toolArgs": "{\"command\": \"nrfjprog --program x.hex\"}"}, 2),
    ("block-flash.py", {"tool_name": "Read", "tool_input": {"file_path": "config/eyelash_sofle.keymap"}}, 0),
    ("block-secret-access.py", {"tool_name": "Read", "tool_input": {"file_path": "/repo/.env"}}, 2),
    ("block-secret-access.py", {"tool_name": "Read", "tool_input": {"file_path": "config/eyelash_sofle.keymap"}}, 0),
    ("block-secret-access.py", {"tool_name": "Bash", "tool_input": {"command": "cat ~/.ssh/id_ed25519"}}, 2),
    ("block-secret-access.py", {"tool_name": "Glob", "tool_input": {"pattern": "**/*.pem"}}, 2),
]


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def split_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening '---'")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1:])
    raise ValueError("missing closing '---'")


def parse_frontmatter(text):
    """Parse the flat YAML subset used by this repo. Nested maps are kept as raw lines."""
    raw_lines, body = split_frontmatter(text)
    data = {}
    key = None
    for line in raw_lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            name, sep, value = line.partition(":")
            if not sep:
                raise ValueError(f"unparseable line: {line!r}")
            key = name.strip()
            value = value.strip()
            data[key] = {"_block": []} if value == "" else unquote(value)
        else:
            if key is None or not isinstance(data.get(key), dict):
                raise ValueError(f"indented line without a block: {line!r}")
            data[key]["_block"].append(line.strip())
    for name, value in list(data.items()):
        if isinstance(value, dict) and "_block" in value:
            items = value["_block"]
            if items and all(item.startswith("- ") for item in items):
                data[name] = [unquote(item[2:].strip()) for item in items]
            else:
                data[name] = {"_raw": items}
    return data, body


def split_tools(value):
    return [tool.strip() for tool in value.split(",") if tool.strip()] if isinstance(value, str) else []


def agent_files():
    return sorted(name for name in os.listdir(AGENTS_DIR) if name.endswith(".md"))


def skill_dirs():
    return sorted(name for name in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, name)))


def copilot_text(name, data, body):
    tools = []
    for tool in split_tools(data.get("tools", "")):
        mapped = COPILOT_TOOLS.get(tool)
        if mapped and mapped not in tools:
            tools.append(mapped)
    skills = data.get("skills") if isinstance(data.get("skills"), list) else []
    front = [
        "---",
        f"name: {name}",
        f'description: "{data.get("description", "")}"',
        "tools: [" + ", ".join(f"'{tool}'" for tool in tools) + "]",
    ]
    if skills:
        front.append("skills: [" + ", ".join(f"'{skill}'" for skill in skills) + "]")
    front.append("---")
    note = (
        f"<!-- Generated from .claude/agents/{name}.md by .claude/scripts/customizations.py. "
        "Edit the source. Copilot does not run the Claude Bash guard. -->"
    )
    return "\n".join(front) + "\n" + note + "\n\n" + body.lstrip("\n")


def ensure_symlink():
    target = os.path.join("..", ".claude", "skills")
    if os.path.islink(GH_SKILLS):
        if os.readlink(GH_SKILLS) != target:
            os.remove(GH_SKILLS)
            os.symlink(target, GH_SKILLS)
            return "fixed"
        return "ok"
    if os.path.exists(GH_SKILLS):
        raise SystemExit(".github/skills exists and is not a symlink; move it aside and rerun")
    os.symlink(target, GH_SKILLS)
    return "created"


def sync():
    os.makedirs(GH_AGENTS, exist_ok=True)
    written = []
    for filename in agent_files():
        name = filename[:-3]
        data, body = parse_frontmatter(read_text(os.path.join(AGENTS_DIR, filename)))
        if not data.get("description"):
            raise SystemExit(f"{filename}: missing description")
        write_text(os.path.join(GH_AGENTS, f"{name}.agent.md"), copilot_text(name, data, body))
        written.append(name)
    for stale in os.listdir(GH_AGENTS):
        if stale.endswith(".agent.md") and stale[: -len(".agent.md")] not in written:
            os.remove(os.path.join(GH_AGENTS, stale))
            print(f"removed stale mirror {stale}")
    print(f"synced {len(written)} agent mirror(s); .github/skills symlink {ensure_symlink()}")
    return 0


def check_links(path, errors):
    base = os.path.dirname(path)
    for target in LINK_RE.findall(read_text(path)):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        file_part = target.split("#", 1)[0]
        if file_part and not os.path.exists(os.path.normpath(os.path.join(base, file_part))):
            errors.append(f"{os.path.relpath(path, ROOT)}: broken link {target}")


def check_skills(errors):
    for name in skill_dirs():
        folder = os.path.join(SKILLS_DIR, name)
        path = os.path.join(folder, "SKILL.md")
        if not os.path.isfile(path):
            errors.append(f"skill {name}: missing SKILL.md")
            continue
        text = read_text(path)
        try:
            data, _ = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(f"skill {name}: frontmatter: {exc}")
            continue
        if data.get("name") != name or not NAME_RE.match(name):
            errors.append(f"skill {name}: name must equal the folder name and use lowercase, digits, hyphens")
        desc = data.get("description")
        if not isinstance(desc, str) or not desc.strip():
            errors.append(f"skill {name}: missing description")
        elif len(desc) > 1024 or '"' in desc:
            errors.append(f"skill {name}: description must be at most 1024 characters with no double quotes")
        if text.count("\n") + 1 >= 500:
            errors.append(f"skill {name}: SKILL.md must stay under 500 lines")
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".md"):
                check_links(os.path.join(folder, filename), errors)


def check_agents(errors):
    sources = set()
    for filename in agent_files():
        name = filename[:-3]
        sources.add(name)
        try:
            data, body = parse_frontmatter(read_text(os.path.join(AGENTS_DIR, filename)))
        except ValueError as exc:
            errors.append(f"agent {name}: frontmatter: {exc}")
            continue
        if data.get("name") != name or not NAME_RE.match(name):
            errors.append(f"agent {name}: name must equal the file name")
        desc = data.get("description")
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024 or '"' in desc:
            errors.append(f"agent {name}: description missing, too long, or contains double quotes")
            continue
        unknown = [tool for tool in split_tools(data.get("tools", "")) if tool not in CLAUDE_TOOLS]
        if unknown:
            errors.append(f"agent {name}: unknown tools {unknown}")
        for skill in data.get("skills") if isinstance(data.get("skills"), list) else []:
            if skill not in skill_dirs():
                errors.append(f"agent {name}: skill '{skill}' does not exist")
        hooks = data.get("hooks")
        if isinstance(hooks, dict):
            for script in re.findall(r"\.claude/hooks/([\w.-]+\.py)", "\n".join(hooks.get("_raw", []))):
                if not os.path.isfile(os.path.join(HOOKS_DIR, script)):
                    errors.append(f"agent {name}: hook script {script} is missing")
        if not os.path.isfile(os.path.join(EVALS_DIR, "agents", f"{name}.evals.json")):
            errors.append(f"agent {name}: missing evals/agents/{name}.evals.json")
        mirror = os.path.join(GH_AGENTS, f"{name}.agent.md")
        if not os.path.isfile(mirror):
            errors.append(f"agent {name}: missing Copilot mirror; run sync")
        elif read_text(mirror) != copilot_text(name, data, body):
            errors.append(f"agent {name}: Copilot mirror is out of date; run sync")
    if os.path.isdir(GH_AGENTS):
        for filename in os.listdir(GH_AGENTS):
            if filename.endswith(".agent.md") and filename[: -len(".agent.md")] not in sources:
                errors.append(f"orphan Copilot mirror {filename}")


def check_settings(errors):
    try:
        settings = json.loads(read_text(os.path.join(CLAUDE, "settings.json")))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"settings.json: {exc}")
        return
    deny = settings.get("permissions", {}).get("deny", [])
    if not deny or not all(isinstance(rule, str) for rule in deny):
        errors.append("settings.json: permissions.deny must be a non-empty list of strings")
    for groups in settings.get("hooks", {}).values():
        for group in groups:
            for hook in group.get("hooks", []):
                if hook.get("onFailure") not in (None, "block", "continue"):
                    errors.append(f"settings.json: unknown onFailure value {hook.get('onFailure')!r}")
                for arg in hook.get("args", []):
                    for script in re.findall(r"\.claude/hooks/([\w.-]+\.py)", arg):
                        if not os.path.isfile(os.path.join(HOOKS_DIR, script)):
                            errors.append(f"settings.json: hook script {script} is missing")


def check_evals(errors):
    for kind in ("agents", "skills"):
        folder = os.path.join(EVALS_DIR, kind)
        if not os.path.isdir(folder):
            errors.append(f"missing evals/{kind}")
            continue
        for filename in sorted(os.listdir(folder)):
            if not filename.endswith(".evals.json"):
                continue
            target = filename[: -len(".evals.json")]
            try:
                doc = json.loads(read_text(os.path.join(folder, filename)))
            except json.JSONDecodeError as exc:
                errors.append(f"evals/{kind}/{filename}: {exc}")
                continue
            key = "agent_name" if kind == "agents" else "skill_name"
            if doc.get(key) != target:
                errors.append(f"evals/{kind}/{filename}: {key} must be '{target}'")
            exists = os.path.isfile(os.path.join(AGENTS_DIR, f"{target}.md")) if kind == "agents" else os.path.isdir(os.path.join(SKILLS_DIR, target))
            if not exists:
                errors.append(f"evals/{kind}/{filename}: no matching {kind[:-1]} '{target}'")
            evals = doc.get("evals")
            if not isinstance(evals, list) or not evals:
                errors.append(f"evals/{kind}/{filename}: evals must be a non-empty list")
                continue
            for item in evals:
                if not isinstance(item, dict) or not all(k in item for k in ("id", "prompt", "expected_output", "files")):
                    errors.append(f"evals/{kind}/{filename}: each eval needs id, prompt, expected_output, files")
                elif not isinstance(item["id"], int) or not isinstance(item["files"], list):
                    errors.append(f"evals/{kind}/{filename}: id must be an int and files a list")
    for name in skill_dirs():
        if not os.path.isfile(os.path.join(EVALS_DIR, "skills", f"{name}.evals.json")):
            errors.append(f"skill {name}: missing evals/skills/{name}.evals.json")


def check_hooks(errors):
    for script, payload, expected in HOOK_CASES:
        body = payload if isinstance(payload, str) else json.dumps(payload)
        result = subprocess.run(
            [sys.executable, os.path.join(HOOKS_DIR, script)],
            input=body, capture_output=True, text=True, timeout=20,
        )
        if result.returncode != expected:
            errors.append(f"hook {script}: expected exit {expected}, got {result.returncode} for {body[:80]}")


def check_symlink(errors):
    if not os.path.islink(GH_SKILLS):
        errors.append(".github/skills is not a symlink; run sync")
    elif os.path.realpath(GH_SKILLS) != os.path.realpath(SKILLS_DIR):
        errors.append(".github/skills does not resolve to .claude/skills")


def check_sizes(warnings):
    for path in (os.path.join(ROOT, "AGENTS.md"), os.path.join(CLAUDE, "CLAUDE.md")):
        if os.path.isfile(path) and read_text(path).count("\n") >= 200:
            warnings.append(f"{os.path.relpath(path, ROOT)} is 200 lines or more")


def check():
    errors, warnings = [], []
    check_skills(errors)
    check_agents(errors)
    check_settings(errors)
    check_evals(errors)
    check_hooks(errors)
    check_symlink(errors)
    check_sizes(warnings)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print(f"OK: {len(skill_dirs())} skills, {len(agent_files())} agents, {len(HOOK_CASES)} hook cases")
    return 0


def main(argv):
    if len(argv) != 2 or argv[1] not in ("sync", "check"):
        print(__doc__.strip())
        return 2
    return sync() if argv[1] == "sync" else check()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
