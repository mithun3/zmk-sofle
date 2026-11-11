# .claude: ZMK Sofle and Corne customizations

This folder is the single source of truth for skills, agents, hooks, settings, and evals. It is used by Claude Code and by VS Code (Copilot harness).

## Layout

```
.claude/
  CLAUDE.md              Claude-only notes (imports ../AGENTS.md)
  settings.json          permission deny rules and PreToolUse hooks
  skills/                zmk-core, zmk-sofle, zmk-corne, zmk-flash-runbook
  agents/                zmk-keymap-designer, zmk-build-troubleshooter, zmk-change-reviewer
  hooks/                 _payload.py, readonly-bash-guard.py, block-flash.py, block-secret-access.py
  scripts/customizations.py   sync (Copilot mirrors) and check (validation and hook self-tests)
  evals/agents/ and evals/skills/   eval prompts with expected outputs
```

## Commands

- `python3 .claude/scripts/customizations.py sync`: regenerates `.github/agents/*.agent.md` and checks the `.github/skills` symlink.
- `python3 .claude/scripts/customizations.py check`: validates frontmatter, links, tools, mirrors, JSON, and runs hook self-tests.

## Adding a skill

1. Create `skills/<name>/SKILL.md`. `name` must equal the folder name. `description` is one line, quoted, and under 1024 characters.
2. Keep SKILL.md under 500 lines. Put detail in reference files and link them with relative paths.
3. Add `evals/skills/<name>.evals.json`.
4. Run `check`.

## Adding an agent

1. Create `agents/<name>.md` in Claude format. Allowed tools: Read, Grep, Glob, Bash, Edit, Write, WebFetch, WebSearch, Agent.
2. Run `sync`, then `check`.
3. Add `evals/agents/<name>.evals.json`.

## Interop notes

- Skills: VS Code reads `.claude/skills` in Local sessions. `.github/skills` is a symlink for the Copilot CLI and app.
- Agents: VS Code lists `.claude/agents` (Claude format). `.github/agents` holds the generated Copilot format.
- Hooks: Claude reads `settings.json` hooks. The Copilot harness is documented to read `.claude/settings.json` hooks too. Confirm in a Copilot session before relying on it.
- Requirements: Claude Code v2.1.295 or later, and `python3`.
