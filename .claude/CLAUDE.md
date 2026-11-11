@../AGENTS.md

## Claude Code notes

- Shared rules are in AGENTS.md (imported above). Keep this file to Claude-only behaviour.
- The read-only Bash guard is declared in the `zmk-*` agent frontmatter. It applies only inside those agents, so normal sessions can still build.
- Project hooks in `.claude/settings.json` use `onFailure: "block"`. That needs Claude Code v2.1.295 or later and `python3` on PATH.
- Hooks in project subagents run only after the workspace is trusted.
- After editing skills, agents, hooks, settings, or evals, run `python3 .claude/scripts/customizations.py check`.
