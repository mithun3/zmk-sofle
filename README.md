# zmk-sofle (eyelash_sofle)

Firmware configs for the eyelash Sofle split keyboard running ZMK. Includes custom board definitions, pointing device tuning, per-side builds, underglow/backlight, and a navigation-first layer stack.

## Hardware assumptions
- Sofle-derived split with eyelash_sofle left/right PCBs (see boards/arm/eyelash_sofle/*).
- Nice!Nano-class MCU (nRF52840) per half.
- EC11 rotary encoder(s) and optional sensor input for scrolling.
- WS2812 underglow, backlight support, optional external power.
- Nice-view-gem OLED display (custom status screen enabled).

## Repo layout
- boards/arm/eyelash_sofle/: board files (CMake, DTS, keymap for board builds).
- config/: primary ZMK config (eyelash_sofle.conf, keymap, combos.dtsi, west.yml).
- keymap-drawer/: YAML layouts for generating diagrams.
- build.yaml: CI/build helper matrix.

## Keymap overview (config/eyelash_sofle.keymap)
- Pointing: accelerated cursor and scroll (`mmv`, `msc`) with adjustable time-to-max.
- Layer stack (tri-layer: Lower + Raise => Adjust):
  - layer0 (Base): alphas, number row, thumbs = Lower (layer1) / Raise (layer2) with tri-layer Adjust (layer3) when both held; arrows removed to keep base clean.
  - layer1 (Lower: Nav/F-keys/RGB): F-keys, PgUp/PgDn/Home/End + arrows, RGB controls, mouse buttons, scroll encoder.
  - layer2 (Raise: BT/Utility/Numpad): BT select/clear, USB/BLE output toggle, numpad; feeding Adjust when combined with Lower.
  - layer3 (Adjust): symbols cluster; use this layer for infrequent/destructive actions (reset/bootloader/soft-off, currently on layer2—move here if desired).
- Tap dance: `caps_lock` toggles Shift/Caps Word (175 ms tapping-term).
- Sensor bindings: scroll encoder present on layers 1–3; volume inc/dec on base.
- Tri-layer support: `CONFIG_ZMK_CONDITIONAL_LAYERS=y` is set in config/eyelash_sofle.conf to enable the Lower+Raise=>Adjust logic.

## Combos (config/combos.dtsi)
- Fast combos: 18 ms term, 150 ms idle for tight chords (Escape, mouse, tab, leader, cut/copy/paste, bspc/del, brackets/paren pairs).
- Slow combos: 30 ms term, 50 ms idle for vertical symbol pairs (currency, math, slashes, pipes).
- If using home-row mods, consider relaxing the fast term to ~25–30 ms to avoid accidental fires.
- Ensure combos.dtsi is included in your build (e.g., via your shield or main .keymap include).

## Timing and input feel
- Debounce: 8 ms press/release (CONFIG_ZMK_KSCAN_DEBOUNCE_* in config/eyelash_sofle.conf). Lower to 4–5 ms if your switches/diodes are clean and you want snappier input.
- Tap dance: 175 ms on Caps/Shift toggle.
- Pointing defaults: cursor move 1200, scroll 25; cursor accel time-to-max 500 ms, scroll 100 ms; adjust to taste.
- Idle sleep: 60 minutes; NKRO disabled for compatibility; backlight starts on, underglow off by default with max brightness capped at 90.

## Build and flash
Prereqs: Zephyr SDK, west, ZMK source as a module. From repo root:

1) Initialize (once):
```
west init -l config
west update
```

2) Build left half:
```
west build -s zmk/app -b eyelash_sofle_left -d build/left -- -DZMK_CONFIG=${PWD}/config
```

3) Build right half:
```
west build -s zmk/app -b eyelash_sofle_right -d build/right -- -DZMK_CONFIG=${PWD}/config
```

4) Flash UF2: copy build/<side>/zephyr/zmk.uf2 to the respective half’s storage (bootloader mode). Use `west flash` if your bootloader supports it.

Notes:
- Adjust `-DZMK_CONFIG` if your config dir moves.
- If you prefer shield-style builds, adapt the `-DSHIELD=` flags to your setup.

## Keymap diagrams (optional)
- Edit the YAML in keymap-drawer/ (e.g., eyelash_sofle.yaml).
- Regenerate markdown/PNG using keymap-drawer CLI, pointing at your YAML.

## Recommended customizations
- Home-row mods: add `&mt`/`&hm` on alphas; keep timing consistent with combos.
- Safety: move `sys_reset`, `bootloader`, `soft_off` fully into Adjust-only chords (tri-layer is already present).
- Navigation: keep nav canonical on layer1; base stays transparent for HRMs or layer-taps.

## Troubleshooting
- Ghost taps: raise debounce or tap-hold timings; check switch/diode soldering.
- Missed combos: lengthen fast combo term to 25–30 ms; ensure combos.dtsi is included.
- Sluggish pointer: lower cursor time-to-max to ~250–300 ms; increase scroll accel if needed.
- Power draw: use underglow auto-off (USB/idle already enabled) and external power if driving many LEDs.

## License
MIT, following upstream ZMK community conventions.
