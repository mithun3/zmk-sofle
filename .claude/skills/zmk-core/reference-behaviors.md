# ZMK behaviour reference

Facts checked against ZMK 0.3.0 docs. Source links are relative to this file.

## Hold-taps

Source: [hold-tap.mdx](../../../zmk/docs/docs/keymaps/behaviors/hold-tap.mdx)

- `tapping-term-ms`: default 200 ms.
- Mod-tap presets default to the `hold-preferred` flavour. Layer-tap presets default to `tap-preferred`.
- Interrupt flavours:
  - `hold-preferred`: hold when the term expires or another key is pressed.
  - `balanced`: hold when the term expires, or when another key is both pressed and released while held.
  - `tap-preferred`: hold only when the term expires. Other keys within the term do not decide it.
  - `tap-unless-interrupted`: hold only when another key is pressed before the term expires. It inverts the term logic.
- `quick-tap-ms`: pressing a tapped hold-tap again within this window always produces the tap.
- `require-prior-idle-ms`: if a non-modifier key was pressed within this window before the hold-tap, the hold-tap resolves as a tap.
- Positional hold-tap: `hold-trigger-key-positions` lists the keys that may trigger a hold. Any other key pressed before the term expires gives a tap. `hold-trigger-on-release` delays that decision until the next key is released.
- Documented home-row example (`balanced`, 280 ms term, 175 ms quick-tap, 150 ms prior-idle, positional triggers on the opposite half): the same file, around lines 157–174.

## Mod-morph and tap-dance

- Mod-morph: [mod-morph.md](../../../zmk/docs/docs/keymaps/behaviors/mod-morph.md). Compatible `zmk,behavior-mod-morph`. Two bindings: the normal one and the morphed one. `mods` is a bitmask such as `(MOD_LSFT|MOD_RSFT)`. `keep-mods` keeps listed modifiers on the morphed key. Any listed modifier activates the morph. To require several modifiers, nest mod-morphs.
- Tap-dance: [tap-dance.mdx](../../../zmk/docs/docs/keymaps/behaviors/tap-dance.mdx). Compatible `zmk,behavior-tap-dance`. `tapping-term-ms` and a `bindings` list. The number of bindings is the maximum number of taps. Reaching the maximum fires the last binding at once.
- Sticky keys: [sticky-key.md](../../../zmk/docs/docs/keymaps/behaviors/sticky-key.md). `quick-release` deactivates on the next key press instead of release.

## Combos

Source: [combos.md](../../../zmk/docs/docs/keymaps/combos.md) and [config/combos.md](../../../zmk/docs/docs/config/combos.md)

- Node `compatible = "zmk,combos"`. Each child has `bindings`, `key-positions`, and optional `timeout-ms` (config default 50 ms), `require-prior-idle-ms`, `slow-release`, and `layers`.
- `layers = <-1>` (the default in config) means all layers. A list limits the combo to those layers.
- Partial overlaps and full overlaps are supported. Combos can bind any behaviour, not only `&kp`.
- `CONFIG_ZMK_COMBO_MAX_PRESSED_COMBOS` defaults to 4.
- Combos always invoke source-locality behaviours on the central half. See [split-keyboards](../../../zmk/docs/docs/features/split-keyboards.md#behaviors-with-locality).

## Layers

Source: [layers.md](../../../zmk/docs/docs/keymaps/behaviors/layers.md)

- `&mo N` (momentary), `&tog N` (toggle), `&to N`, and layer-tap.
- Active layers: the highest-valued active layer receives the event first. A behaviour can pass the event down.
- Conditional layers (tri-layer): `zmk,conditional-layers` with `if-layers` and `then-layer`. The Sofle uses it so that layers 1 and 2 together enable layer 3.
