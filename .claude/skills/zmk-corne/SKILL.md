---
name: zmk-corne
description: "Corne (crkbd-style 42-key split) in this repo: nice_nano_v2 halves, stock corne_left and corne_right shields, nice_view, Studio on the left half, three layers BASE/LOWER/RAISE, and the key-count question. Use for questions about the Corne keymap, its config, or its build. Verified against files in this repo and ZMK 0.3.0."
metadata:
  zmk_version: "0.3.0"
  verified: "2026-11-11"
  sources: "config/corne.keymap, config/corne.conf, build.yaml, config/west.yml"
---

# Corne

This skill covers the Corne in this repository. For general ZMK behaviour, load `zmk-core`. Full facts are in [reference.md](reference.md).

## Quick facts

- Board: `nice_nano_v2` for both halves. The `corne` shield is stock ZMK, so this repo has no board files for it.
- Build targets in `build.yaml`: `corne_left` (`corne_left nice_view_adapter nice_view`, Studio snippet), `corne_right`, and `corne_settings_reset`.
- Keymap: `config/corne.keymap` with three layers: `base_layer` (BASE), `lower_layer` (LOWER, `&mo 1`), `raise_layer` (RAISE, `&mo 2`).
- Each layer has 42 bindings: three rows of 12 and a thumb row of 6. That matches the 42-key Corne spec (3×6 plus 3 thumbs per side).
- Config: `config/corne.conf` sets BT TX power, the display, and debounce. Studio is set per target in `build.yaml`.

## Working rules

1. Quote the key count as 42, unless the owner confirms another physical kit. The AliExpress listing says "61 keys", which conflicts with the 3×6 layout. Ask the owner (decision).
2. Check that each layer keeps 42 bindings after an edit.
3. The Corne and the Sofle share `config/west.yml` and ZMK `v0.3`. A change there affects both keyboards.
4. Studio is enabled on the left half only, through `snippet` and `cmake-args` in `build.yaml`. Locking is off.

## Pointers

- Facts, file references, and layer tables: [reference.md](reference.md).
- Build and Studio details: `zmk-core` [reference-build-split-studio.md](../zmk-core/reference-build-split-studio.md).
