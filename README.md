# zmk-config

ZMK firmware config for two split keyboards. Both build from this repo on ZMK `v0.3`.

## Keyboards

| | Eyelash Sofle | Corne |
| :- | :- | :- |
| Name used everywhere | `eyelash_sofle` | `corne` |
| Hardware | Custom nRF52840 board (files in `boards/`) | `nice_nano_v2` with the stock ZMK `corne` shield |
| Keys | 64 | 42 |
| Keymap | `config/eyelash_sofle.keymap` | `config/corne.keymap` |
| Settings | `config/eyelash_sofle.conf` | `config/corne.conf` |
| Layers | BASE, LOWER, RAISE, ADJUST (LOWER + RAISE) | BASE, LOWER, RAISE |
| Extras | Encoder, mouse keys, RGB underglow, backlight | none |

ZMK picks each keyboard's `.keymap` and `.conf` by name, so the two never mix.

## Repo layout

```
build.yaml                 what CI builds: left, right, settings reset per keyboard
config/
  west.yml                 ZMK version and modules, shared by both keyboards
  eyelash_sofle.keymap     Sofle keys
  eyelash_sofle.conf       Sofle settings
  eyelash_sofle.json       Sofle physical layout for the drawing
  corne.keymap             Corne keys
  corne.conf               Corne settings
boards/arm/eyelash_sofle/  Sofle board definition (the Corne needs none)
keymap-drawer/             generated drawings, one per keyboard
keymap_drawer.config.yaml  drawing style
```

## Changing a keymap

1. Edit `config/<keyboard>.keymap`. Keep 64 bindings per Sofle layer and 42 per Corne layer.
2. Push. GitHub Actions builds the firmware and redraws `keymap-drawer/<keyboard>.svg`.
3. Download the `firmware` artifact from the Actions run and flash it.

## Firmware files

| Keyboard | Left (central, ZMK Studio) | Right | Settings reset |
| :- | :- | :- | :- |
| Sofle | `eyelash_sofle_left.uf2` | `eyelash_sofle_right.uf2` | `eyelash_sofle_settings_reset.uf2` |
| Corne | `corne_left.uf2` | `corne_right.uf2` | `corne_settings_reset.uf2` |

## Flashing

1. Put one half into its bootloader (double-tap reset). A USB drive appears.
2. Copy that half's `.uf2` file to the drive. The half reboots when the copy finishes.
3. Repeat for the other half.

A keymap-only change usually needs just the left half. If the halves stop pairing, flash the settings reset file to both halves, then the normal firmware, then pair again.

## ZMK Studio

The left half of each keyboard is built with [ZMK Studio](https://zmk.studio) support over USB, unlocked. Changes saved from Studio override the keymap file until you choose "Restore stock settings" in Studio.

## Display screens

All four halves use the [nice-view-gem](https://github.com/M165437/nice-view-gem) screen with its animation turned off.

- Left half: layer, Bluetooth profile, USB or BLE output, battery, typing speed.
- Right half: battery, link to the left half, and a still image that changes on each restart.

The screen is chosen by the last word on each `shield:` line in `build.yaml` and is fixed when the firmware is built. `nice_view` gives the stock ZMK screen instead.

## Local builds

See the [ZMK local build docs](https://zmk.dev/docs/development/local-toolchain/build-flash). Pass `-DZMK_CONFIG=<this repo>/config` and `-DZMK_EXTRA_MODULES=<this repo>`.

## License

MIT, following upstream ZMK conventions.
