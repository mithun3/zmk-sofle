# ZMK build, split, Studio, and flashing reference

Facts checked against ZMK 0.3.0 docs. Source links are relative to this file.

## Building with west

Source: [build-flash.mdx](../../../zmk/docs/docs/development/local-toolchain/build-flash.mdx)

- Board and shield: `west build -b nice_nano_v2 -- -DSHIELD=corne_left`.
- Pristine rebuild: add `-p`.
- Split halves: build each half into its own folder with `-d build/left` and `-d build/right`. Otherwise the second build overwrites the first.
- Permanent CMake arguments: `west config build.cmake-args -- -DSHIELD=...`.
- Kconfig on the command line: `-- -DCONFIG_ZMK_SLEEP=y`.
- External modules: `-DZMK_EXTRA_MODULES="<path>"`.
- Build a separate config directory: `-DZMK_CONFIG=<absolute path>`.

## CI build matrix

- `build.yaml` lists the targets. Each entry can set `board`, `shield`, `snippet`, `cmake-args`, and `artifact-name`.
- This repo calls `zmkfirmware/zmk/.github/workflows/build-user-config.yml@v0.3` from [.github/workflows/build.yml](../../../.github/workflows/build.yml). One `build.yaml` lists the targets for both keyboards.
- Pin the reusable workflow to a tag or commit. Pins are a decision (see the `zmk-sofle` skill).

## Split keyboards

Source: [split-keyboards.md](../../../zmk/docs/docs/features/split-keyboards.md)

- Central and peripheral roles. Central runs the keymap and talks to hosts. By convention, the left half is central.
- Kconfig: `CONFIG_ZMK_SPLIT=y` enables split. `CONFIG_ZMK_SPLIT_ROLE_CENTRAL` sets the central role. `CONFIG_ZMK_SPLIT_BLE_CENTRAL_PERIPHERALS` sets the peripheral count. See [config/split](../../../zmk/docs/docs/config/split.md).
- Transports: Bluetooth, or full-duplex wired UART (`zmk,wired-split`). Only one transport can be active. Wired supports one peripheral. The docs say half-duplex single-wire support is planned.
- Keymap-only changes: flashing the central half is usually enough.
- Source-locality behaviours such as resets run on the side that holds the binding. Combos run on the central side.
- Never insert or remove TRS or TRRS cables while a controller is powered. The docs warn of irreparable damage.

## ZMK Studio

Sources: [studio.md](../../../zmk/docs/docs/features/studio.md), [config/studio](../../../zmk/docs/docs/config/studio.md)

- Add the snippet `studio-rpc-usb-uart` to the build (`snippet:` in `build.yaml`, or `-S studio-rpc-usb-uart` locally).
- Enable `CONFIG_ZMK_STUDIO=y`, for example through `cmake-args`.
- Studio builds keep all behaviours (`ZMK_BEHAVIORS_KEEP_ALL`), so they are larger.
- Locking: `CONFIG_ZMK_STUDIO_LOCKING` defaults to `y`. The lock idle timeout defaults to 500 seconds.
- The snippet needs CDC-ACM console support. Boards that are composite (an in-tree board plus a shield) already have it.

## Keymap drawing

- `keymap-drawer` 0.18 or later can use zmk-helpers. Add `parse_config.zmk_additional_includes` to `keymap_drawer.config.yaml`.
- Without that setting, zmk-helpers macros break parsing.
- This repo's [draw workflow](../../../.github/workflows/draw.yml) runs on changes to `config/**`. It commits drawings, so it needs write permission.

## Flashing

Sources: [build-flash.mdx](../../../zmk/docs/docs/development/local-toolchain/build-flash.mdx), [flashing-issues](../../../zmk/docs/docs/troubleshooting/flashing-issues.md)

- UF2 boards: copy the `.uf2` file to the bootloader drive. The board reboots once the copy finishes.
- Other boards: `west flash` from the build folder. This is an owner-run step (see `zmk-flash-runbook`).
- Settings reset: a `settings_reset` build clears bonds. Use it when pairing breaks. This repo builds one per keyboard: `eyelash_sofle_settings_reset` and `corne_settings_reset`.
