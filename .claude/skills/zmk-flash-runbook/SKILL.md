---
name: zmk-flash-runbook
description: "Manual checklist for flashing Eyelash Sofle or Corne halves after a build: choosing which half to flash, UF2 copy, owner-run west flash, settings_reset for pairing trouble, and post-flash checks. Use only when the owner asks how to flash, recover pairing, or roll back. The agent prints the steps and never runs flash commands."
disable-model-invocation: true
metadata:
  zmk_version: "0.3.0"
  verified: "2026-11-11"
  sources: "zmk/docs/docs/development/local-toolchain/build-flash.mdx, zmk/docs/docs/troubleshooting/flashing-issues.md, build.yaml"
---

# Flash runbook (owner-run)

The agent prints these steps. The owner runs them. Never run flash commands from an agent session (see [AGENTS.md](../../../AGENTS.md)).

## Before you start

1. Decide what must be flashed:
   - Keymap or Kconfig change only: the left (central) half is usually enough. The split docs say so for keymap changes.
   - Board, shield, or Studio change: flash both halves.
   - Pairing trouble: flash the `settings_reset` build on the affected half, then the normal builds on both halves.
2. Confirm the artifact. CI artifacts come from `build.yaml`. Each keyboard has three: `<keyboard>_left` (with Studio), `<keyboard>_right`, and `<keyboard>_settings_reset`, where `<keyboard>` is `eyelash_sofle` or `corne`. Local builds go in `build/left` and `build/right`.
3. Keep both halves charged or on USB while you flash.

## UF2 path

1. Put the half into its bootloader. The method is board-specific. Double-tapping reset is common on nice!nano-class boards, and the `&bootloader` binding on the ADJUST layer works if the half is still responding (TBD confirm for this board).
2. A removable drive appears. Copy the `.uf2` file to it.
3. Wait for the drive to disconnect. The board reboots by itself. A macOS Finder error (code -36 or 100093) can appear after a successful copy. It is normally harmless ([flashing-issues](../../../zmk/docs/docs/troubleshooting/flashing-issues.md)).
4. Repeat for the other half if the change touches both halves.

## west path (owner runs in a terminal)

1. From the matching build folder, run `west flash`. The runner is set by the board's `board.cmake` (TBD confirm the runner for this board).
2. Keep one build folder per half so the other half's UF2 is not overwritten ([build-flash](../../../zmk/docs/docs/development/local-toolchain/build-flash.mdx)).

## Pairing recovery

1. Flash the keyboard's `<keyboard>_settings_reset` build to the affected half, or to both halves after a ZMK version change.
2. Flash the normal left build.
3. Flash the normal right build.
4. Power both halves and check that they pair.

## After flashing

- Both halves connect. The status screen shows.
- Every layer produces the expected output. Check ADJUST keys in particular.
- Studio connects if the Studio build was flashed.
- Note the commit and the artifact name. Never record secrets.

## Rollback

Flash the last known good CI artifact for each half, using the same steps.
