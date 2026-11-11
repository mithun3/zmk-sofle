# AGENTS.md

Shared instructions for coding agents (Claude Code, GitHub Copilot, Codex) working in this repository.

## Scope

- This repo is the ZMK user config for two split keyboards: the Eyelash Sofle (custom nRF52840 board) and the Corne (`nice_nano_v2` with the stock `corne` shield).
- Both keyboards share `config/west.yml`, `build.yaml`, and ZMK `v0.3`. A change to a shared file affects both.
- `zmk/` and `modules/` are local ZMK and Zephyr checkouts. Treat them as read-only references. `zmk/docs/docs` is the version-matched documentation for ZMK 0.3.0.

## Hard rules

- Do not flash firmware. No `west flash`, nrfjprog, nrfutil, dfu-util, picotool, or copying `.uf2` files to a bootloader volume. Give the owner the steps instead (skill `zmk-flash-runbook`).
- Do not read, print, or commit secrets: `.env` files, private keys, certificates, tokens, or credential files.
- Do not change files under `config/`, `boards/`, or `build.yaml` unless the owner asks for that change in the current session. Propose a diff first.
- Count before you quote. Use grep or wc, and cite file paths with line numbers.
- Mark anything you have not checked as TBD.
- Code comments: one short line, and only for facts the code cannot show.

## Where things are

- `config/<keyboard>.keymap` and `config/<keyboard>.conf`: one pair per keyboard, named `eyelash_sofle` and `corne`. `config/west.yml`: west manifest.
- `boards/arm/eyelash_sofle/`: Sofle board files. The 64-position matrix transform is in `eyelash_sofle.dtsi`. The Corne uses stock ZMK files and has none here.
- `build.yaml`: CI build matrix, three targets per keyboard (left, right, settings reset). `keymap_drawer.config.yaml` and `keymap-drawer/`: drawings.
- `.claude/`: canonical skills, agents, hooks, settings, and evals.
- `.github/skills` (symlink) and `.github/agents/*.agent.md` (generated): Copilot views of the canonical files.

## Skills and agents

- Skills: `zmk-core` (ZMK behaviours, Kconfig, split, Studio, build), `zmk-sofle` (the Sofle), `zmk-corne` (the Corne), `zmk-flash-runbook` (manual, owner-run checklist).
- Agents: `zmk-keymap-designer` (proposes keymap diffs), `zmk-build-troubleshooter` (read-only diagnosis), `zmk-change-reviewer` (read-only review).
- Edit the canonical files in `.claude/`. Then run `python3 .claude/scripts/customizations.py sync` and `python3 .claude/scripts/customizations.py check`.

## Verification

- Run the check command before reporting a change as complete.
- Firmware behaviour is verified by the owner: CI build or local west build, then a hardware test.
