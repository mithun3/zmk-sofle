# Eyelash Sofle reference

Facts below were read from files in this repository unless marked TBD. Line references are approximate where noted.

## Matrix index map

Source: `zmk,matrix-transform` in [eyelash_sofle.dtsi](../../../boards/arm/eyelash_sofle/eyelash_sofle.dtsi). Index = position in the transform `map`, starting at 0. The matrix has 5 rows and 14 columns. Left half uses matrix columns 0–5. Right half uses matrix columns 7–13 (`col-offset = 7` in [eyelash_sofle_right.dts](../../../boards/arm/eyelash_sofle/eyelash_sofle_right.dts)).

| Row | Left (indices) | Right (indices) | Count |
| :- | :- | :- | :- |
| 0 | 0–5 | 6–12 | 13 |
| 1 | 13–18 | 19–25 | 13 |
| 2 | 26–31 | 32–38 | 13 |
| 3 | 39–44 | 45–51 | 13 |
| 4 (thumbs) | 52–57 | 58–63 | 12 |

Total: 64. The right half has 7 columns in rows 0–3 and 6 keys in row 4. Index 6 is the right half's first column, and so are 19, 32, and 45.

Layer use of the innermost right column, from [config/eyelash_sofle.keymap](../../../config/eyelash_sofle.keymap):

- BASE: index 6, 19, 32, 45 are `&trans`.
- LOWER, RAISE, ADJUST: index 6 is `&mmv MOVE_UP`, 19 is `MOVE_DOWN`, 32 is `MOVE_LEFT`, 45 is `MOVE_RIGHT`.

## Pins and hardware

From the board files:

- Matrix: `diode-direction = "col2row"`. Rows: gpio0.19, gpio0.8, gpio0.12, gpio0.11, gpio1.9 ([eyelash_sofle.dtsi](../../../boards/arm/eyelash_sofle/eyelash_sofle.dtsi)).
- Left columns (6): gpio0.3, 0.28, 0.30, 0.21, 0.23, 0.22 ([eyelash_sofle_left.dts](../../../boards/arm/eyelash_sofle/eyelash_sofle_left.dts)).
- Right columns (7): gpio0.22, 0.29, 0.3, 0.28, 0.30, 0.21, 0.23 ([eyelash_sofle_right.dts](../../../boards/arm/eyelash_sofle/eyelash_sofle_right.dts)).
- Left encoder (EC11): a = gpio1.10, b = gpio1.14, resolution 4, 40 steps. Enabled on the left only.
- External power control: gpio0.13, active high, 50 ms init delay.
- Battery: `zmk,battery-nrf-vddh`.
- Underglow: WS2812 strip, via `zmk,underglow`.
- Backlight: PWM channel 0 (`pwm0`).
- Flash partitions, the 32 kHz crystal, and `CONFIG_ZMK_EXT_POWER` are set in the board files.

## Kconfig

From [config/eyelash_sofle.conf](../../../config/eyelash_sofle.conf):

| Symbol | Value | Meaning |
| :- | :- | :- |
| `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT` | 3600000 | Sleep after one hour idle |
| `CONFIG_ZMK_SLEEP` | y | Sleep enabled |
| `CONFIG_ZMK_RGB_UNDERGLOW` | y | Underglow on, with external power |
| `CONFIG_ZMK_RGB_UNDERGLOW_BRT_MAX` | 90 | Maximum brightness |
| `CONFIG_ZMK_RGB_UNDERGLOW_ON_START` | n | Off at start |
| `CONFIG_ZMK_RGB_UNDERGLOW_HUE_START` | 160 | Starting hue |
| `CONFIG_ZMK_RGB_UNDERGLOW_EFF_START` | 3 | Starting effect |
| `CONFIG_EC11`, `CONFIG_EC11_TRIGGER_GLOBAL_THREAD` | y | Encoder driver |
| `CONFIG_ZMK_POINTING` | y | Pointing (mouse) support |
| `CONFIG_BT_CTLR_TX_PWR_PLUS_8` | y | Higher Bluetooth TX power |
| `CONFIG_ZMK_HID_REPORT_TYPE_NKRO` | n | NKRO off |
| `CONFIG_ZMK_BACKLIGHT` | y | Backlight on, start at 100, idle auto-off off |
| `CONFIG_ZMK_KSCAN_DEBOUNCE_PRESS_MS` and `_RELEASE_MS` | 8 and 8 | Debounce |
| `CONFIG_ZMK_DISPLAY` and `CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM` | y | Display with the nice-view-gem status screen |
| `CONFIG_NICE_VIEW_GEM_ANIMATION` | n | Right half shows a still frame, no animation |

Studio is not in this file. It is set per target in `build.yaml`.

Pointing tuning in [config/eyelash_sofle.keymap](../../../config/eyelash_sofle.keymap): `ZMK_POINTING_DEFAULT_MOVE_VAL` 1200, `ZMK_POINTING_DEFAULT_SCRL_VAL` 25, move time-to-max 500 ms, scroll time-to-max 100 ms.

## Build matrix

From [build.yaml](../../../build.yaml):

1. `eyelash_sofle_left`: board `eyelash_sofle_left` with shield `nice_view_gem`, snippet `studio-rpc-usb-uart`, cmake args `-DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_STUDIO_LOCKING=n`.
2. `eyelash_sofle_right`: board `eyelash_sofle_right` with shield `nice_view_gem`.
3. `eyelash_sofle_settings_reset`: board `eyelash_sofle_left` with shield `settings_reset`.

The file also holds the three Corne targets (see `zmk-corne`).

Both halves have a display. The `nice_view_spi` bus is defined in the shared [eyelash_sofle.dtsi](../../../boards/arm/eyelash_sofle/eyelash_sofle.dtsi), and `CONFIG_ZMK_DISPLAY=y` in the `.conf` applies to both halves.

## West manifest

From [config/west.yml](../../../config/west.yml):

- Remotes: `zmkfirmware` and `m165437` (`https://github.com/M165437`).
- ZMK: `revision: v0.3`, import `app/west.yml`. Matches the local tree VERSION 0.3.0.
- nice-view-gem: `revision: v0.3.0`. Its `main` branch targets ZMK main. Both keyboards use it.
- `self.path: config`.
- The manifest is shared with the Corne.

## Layers

From [config/eyelash_sofle.keymap](../../../config/eyelash_sofle.keymap):

- Layer 0 BASE (`base_layer`), layer 1 LOWER (`lower_layer`), layer 2 RAISE (`raise_layer`), layer 3 ADJUST (`adjust_layer`).
- `tri_layer` conditional: `if-layers = <1 2>`, `then-layer = <3>`.
- `caps_lock` tap-dance: first tap `&kp LSHFT`, second `&caps_word`.
- `scroll_encoder`: `&msc SCRL_DOWN` and `SCRL_UP`, with a 100 ms tap.
- Each layer has 64 bindings, counted per row (13, 13, 13, 13, 12).

## Combos

No combos are defined. An unused `config/combos.dtsi` (36-key labels and zmk-helpers macros that this board does not have) was deleted when the Corne was merged in. New combos go in a `combos` node in the keymap and use the matrix indices above.

## Community references

These were reviewed in this pass. Licences and maintenance were not all checked (TBD).

- Upstream of the board files: a741725193/zmk-sofle (fork of tokyo2006/zmk-config-sofle, with DYA Studio support added 2026-06).
- Sofle and Eyelash configs: apclark31/sofle-v2, tobiasbueschel/zmk-sofle-keyboard, eff1e8f5/zmk-sofle-dongle, infused-kim/zmk-config-sofle (encoder, display, and underglow tuning), and eyelash configs by kokosbjarne, cybardev, sutamura, kylephillipsau, azumafuji, reykjavik13, kskthedeveloper, carlosedp.
- Tooling: urob/zmk-helpers v0.3.0 (MIT), caksoylar/keymap-drawer v0.23.0 (MIT), M165437/nice-view-gem v0.3.0 (MIT).
- Corresponding hardware reference: the Corne spec is in `zmk-corne` (see that skill).

## Shopping-listing claims

The AliExpress listing says "61-key" for the Sofle. The files show 64 positions, so use the files.
