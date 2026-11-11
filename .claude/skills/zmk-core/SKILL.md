---
name: zmk-core
description: "ZMK firmware fundamentals: keymap anatomy, behaviours (hold-tap, mod-morph, tap-dance, layers, combos), Kconfig and devicetree, split keyboards, ZMK Studio, and building or flashing with west and GitHub Actions. Use for any ZMK keymap, config, or build question that is not specific to one board. Verified against ZMK 0.3.0."
metadata:
  zmk_version: "0.3.0"
  verified: "2026-11-11"
  sources: "zmk/docs/docs, zmk/app"
---

# ZMK core

Use this skill for ZMK questions that apply to any board. Board facts live in `zmk-sofle` and `zmk-corne`. Facts here were checked against the local ZMK 0.3.0 tree: [zmk/docs/docs](../../../zmk/docs/docs) and [zmk/app](../../../zmk/app).

## Keymap anatomy

- Include `behaviors.dtsi` and `dt-bindings/zmk/keys.h` first, then any helper headers. Everything else sits under one root node.
- Optional `combos` node with `compatible = "zmk,combos"`. See [combos](../../../zmk/docs/docs/keymaps/combos.md).
- `keymap` node with `compatible = "zmk,keymap"`. Each layer has `bindings`, and optionally `display-name` and `sensor-bindings`.
- Layers are numbered from 0 in definition order. Use `#define` names (for example `#define LOWER 1`) so that `&mo LOWER` reads clearly. See [layers](../../../zmk/docs/docs/keymaps/behaviors/layers.md).
- Each layer's `bindings` needs one entry per key position in the board's `zmk,matrix-transform`. The keymap arrays are sized from that transform in [keymap.c](../../../zmk/app/src/keymap.c). Count the entries before you call a keymap valid.
- Positions are sequential in the transform's `map`, starting at 0. Combos and hold-tap position lists use the same numbers.

## Bindings

| Binding | Behaviour | Notes |
| :- | :- | :- |
| `&kp KEY` | Key press | Keycode names come from `dt-bindings/zmk/keys.h` |
| `&mt MODS KEY` | Mod-tap | Hold-tap preset: modifiers on hold, keycode on tap |
| `&mo N` | Momentary layer | Layer while held |
| `&tog N` | Toggle layer | Press to toggle |
| `&trans` | Transparent | Falls through to the next active layer |
| `&bt BT_SEL n`, `BT_CLR`, `BT_CLR_ALL` | Bluetooth profiles | [bluetooth](../../../zmk/docs/docs/keymaps/behaviors/bluetooth.md) |
| `&out OUT_USB`, `OUT_BLE` | Output selection | [outputs](../../../zmk/docs/docs/keymaps/behaviors/outputs.md) |
| `&sys_reset`, `&bootloader` | Reset | Source-specific on split boards: affects the side with the binding. [reset](../../../zmk/docs/docs/keymaps/behaviors/reset.md) |
| `&caps_word` | Caps word | [caps-word](../../../zmk/docs/docs/keymaps/behaviors/caps-word.md) |
| `&rgb_ug RGB_ON` and friends | Underglow | [underglow](../../../zmk/docs/docs/keymaps/behaviors/underglow.md) |

Pointing keys (`&mmv`, `&msc`, `&mkp`) and sensor bindings (`&inc_dec_kp`, `&scroll_encoder`) appear in the Sofle keymap. See [reference-behaviors.md](reference-behaviors.md) for details.

## Behaviours that need care

- Hold-tap defaults and interrupt flavours, plus positional hold-tap: [reference-behaviors.md](reference-behaviors.md#hold-taps).
- Mod-morph (two bindings chosen by `mods`) and tap-dance (the number of bindings is the number of taps): [reference-behaviors.md](reference-behaviors.md#mod-morph-and-tap-dance).
- Combos: `key-positions` are matrix positions, not labels. Combos run before the keymap and fire on the central half. See [reference-behaviors.md](reference-behaviors.md#combos).

## Kconfig and devicetree

- Kconfig symbols go in the user `.conf` file. An undefined symbol is a build error or warning, so remove symbols that the tree does not define.
- Devicetree (`.dtsi`, `.keymap`) describes boards and keymaps. Board files set the matrix, kscan, and encoders.
- Config reference pages are in [zmk/docs/docs/config](../../../zmk/docs/docs/config).

## Build, split, Studio, and flashing

See [reference-build-split-studio.md](reference-build-split-studio.md) for `west build`, the `build.yaml` matrix, split roles and transports, Studio locking, keymap drawing, and flashing.

## Troubleshooting pointers

- "zmk,keymap not found" during build: check that the keymap file exists and has `compatible = "zmk,keymap"`. See [building-issues](../../../zmk/docs/docs/troubleshooting/building-issues.md).
- Copy errors on macOS Finder (codes -36 and 100093) can appear after a successful UF2 copy. See [flashing-issues](../../../zmk/docs/docs/troubleshooting/flashing-issues.md).
