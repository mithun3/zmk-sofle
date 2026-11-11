# Copilot instructions

The full shared rules are in AGENTS.md at the repository root. The key rules:

- Never flash firmware, and never run `west flash`, nrfjprog, nrfutil, or dfu-util. Give the owner the steps.
- Never read or print secrets (`.env` files, keys, certificates, tokens).
- Do not edit `config/` or `boards/` unless the owner asks in this session. Propose diffs first.
- Count before quoting. Cite file paths and line numbers.
- Two keyboards share this repo: `config/eyelash_sofle.*` and `config/corne.*`. Both build on ZMK `v0.3` from one `build.yaml` and one `west.yml`.
- Skills are in `.github/skills`, which links to `.claude/skills`. Agents in `.github/agents` are generated. Edit `.claude/agents` and run the sync script.
- In Copilot, the read-only rule for agents is enforced by instructions only.
