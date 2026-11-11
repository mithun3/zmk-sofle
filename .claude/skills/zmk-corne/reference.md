# Corne reference

Facts read from files in this repository unless marked TBD. The config was merged from the former `zmk-corne` repo at commit `9ff07cd`.

## Files

- [build.yaml](../../../build.yaml): board `nice_nano_v2`. Targets:
  - `corne_left`: `corne_left nice_view_adapter nice_view`, snippet `studio-rpc-usb-uart`, cmake args `-DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_STUDIO_LOCKING=n`.
  - `corne_right`: `corne_right nice_view_adapter nice_view`.
  - `corne_settings_reset`: `settings_reset`.
- [config/west.yml](../../../config/west.yml): shared with the Sofle. `zmk` at `revision: v0.3`.
- [config/corne.conf](../../../config/corne.conf):
  - `CONFIG_BT_CTLR_TX_PWR_PLUS_8=y`
  - `CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION=n`
  - `CONFIG_ZMK_DISPLAY=y`
  - `CONFIG_ZMK_KSCAN_DEBOUNCE_PRESS_MS=1` and `CONFIG_ZMK_KSCAN_DEBOUNCE_RELEASE_MS=20`
- [config/corne.keymap](../../../config/corne.keymap): three layers.

The keyboard name "Corne" comes from the shield's default. The settings-reset build does not load `corne.conf`.

## Layers and counts

| Layer | Display name | Rows | Bindings | Notes |
| :- | :- | :- | :- | :- |
| `base_layer` | BASE | 12 + 12 + 12 + 6 | 42 | Alphas, `&mo 1` and `&mo 2` on thumbs |
| `lower_layer` | LOWER | 12 + 12 + 12 + 6 | 42 | Number row, `&bt BT_CLR` and `&bt BT_SEL 0..4`, arrow keys |
| `raise_layer` | RAISE | 12 + 12 + 12 + 6 | 42 | Shifted symbols, brackets, and operators |

Re-count after any edit.

## Key count

- The standard Corne (crkbd, foostan/crkbd README) is 3×6 column-staggered keys plus 3 thumb keys per side, which is 42.
- The AliExpress Corne listing says "61 keys". The keymap has 42 bindings per layer, so the listing is not reliable. Confirm the physical kit (TBD).

## Notes

- No combos or hold-taps are defined. Behaviour is plain `&kp`, `&mo`, `&bt`, and `&trans`.
- There is no underglow on this board.
- Before the merge the Corne tracked ZMK `main`. After moving to `v0.3`, flash `corne_settings_reset` to both halves once, then the firmware, then pair again (owner-run).
