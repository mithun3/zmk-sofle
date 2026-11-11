---
name: zmk-sofle
description: "Eyelash Sofle split keyboard (nRF52840 halves) in this repo: 64-position matrix, layers BASE/LOWER/RAISE/ADJUST, pointing, underglow, encoder, nice-view-gem display, and its build targets. Use for any question about this keyboard's keymap, board, or build. Verified against files in this repo and ZMK 0.3.0."
metadata:
  zmk_version: "0.3.0"
  verified: "2026-11-11"
  sources: "config/, boards/arm/eyelash_sofle/, build.yaml, config/west.yml"
---

# Eyelash Sofle

This skill covers the Eyelash Sofle in this repository. For general ZMK behaviour, load `zmk-core`. Full facts with file and line references are in [reference.md](reference.md).

## Quick facts

- Two halves: `eyelash_sofle_left` (central) and `eyelash_sofle_right` (peripheral). Built on nRF52840 class hardware (confirm the SoC in the defconfig files, TBD).
- Matrix: 14 columns by 5 rows with `col-offset = 7` on the right half. That gives 64 key positions. The layout file has 64 entries, and every layer has 64 bindings.
- Layers: 0 BASE (`base_layer`), 1 LOWER (`lower_layer`), 2 RAISE (`raise_layer`), 3 ADJUST (`adjust_layer`). Layer 3 turns on when layers 1 and 2 are both active.
- Active keymap: `config/eyelash_sofle.keymap`. Kconfig: `config/eyelash_sofle.conf`.

## Layers in one line each

- BASE (0): alphas, numbers, `caps_lock` tap-dance (Shift, then Caps Word). Thumbs `&mo 1`, `&mo 2`. Sensor: volume up and down.
- LOWER (1): F-keys, navigation, media mute, mouse buttons, and mouse move on the inner right column. Sensor: scroll.
- RAISE (2): numpad, symbols, cursor keys. Sensor: scroll.
- ADJUST (3): Bluetooth profile select and clear, outputs (USB and BLE), RGB modes, `&bootloader`, `&sys_reset`, `&soft_off`. Sensor: scroll.

## Working rules for this board

1. Quote key positions as matrix indices. Use the table in [reference.md](reference.md#matrix-index-map). Do not reuse `zmk-helpers` `sofle.h` labels: they describe a 60-key layout.
2. Check that every layer keeps 64 bindings after an edit.
3. Positions 6, 19, 32, and 45 are the innermost right column. They are `&trans` on BASE and mouse-move bindings on LOWER, RAISE, and ADJUST.
4. No combos are defined. To add one, use a `combos` node in the keymap with matrix indices as `key-positions` (see `zmk-core`).
5. Keymap-only changes: the owner can flash just the left (central) half. Confirm this with the owner first.

## Known issues

- `draw.yml` calls a reusable workflow at `@main` and requests write permission. Pinning it to a release tag is an open decision for the owner.
- The board folder has no default keymap. The only keymap is `config/eyelash_sofle.keymap`.

## Pointers

- Matrix, pins, Kconfig, build matrix, layers, and community forks: [reference.md](reference.md).
- Build, split, Studio, and flashing details: `zmk-core` [reference-build-split-studio.md](../zmk-core/reference-build-split-studio.md).
- Manual flash checklist for the owner: `zmk-flash-runbook`.
