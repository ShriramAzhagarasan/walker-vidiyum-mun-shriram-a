# Change brief: Assignment 5, two shaders and their materials (A5)

*Revision 1, 2026-10-28, committed before either shader exists and before any build prompt.*
*The decisions are Shriram's, chosen in conversation with Claude on 2026-10-28 (the glow colour, both fade times, the
re-press rule, the pause rule, time scale, the marble texture, where the marble goes, and wet vs dry). Claude organized
them into this file and filled in the project facts. The parts marked **✍ Shriram** (the colour line, both prediction
tables and the short answers) are Shriram's. Shriram worked them out with **ChatGPT** as a calculation and explanation
aid (disclosed in SOURCES.md and FRICTIONAL.md), sent them in the chat, and Claude placed them here unchanged apart from
turning LaTeX into plain text. Claude recomputed every number independently and they match. Later changes go in dated revisions at the bottom; this text
is not rewritten.*

The A2/A3 briefs are archived in `design/briefs/CHANGE-BRIEF-A2-A3.md`.

---

## Part 1. Shader from code: "the night is slipping"

### 1.1 The state
- **What it communicates:** the night is being skipped. While the player holds **T**, the clock runs ×8 and anything that
  happens meanwhile goes unheard (GAME-BIBLE §7, *Time*). The player is trading knowledge for time, so the screen should
  say so clearly at a glance, not only through the small ">> x8" label.
- **Where it lives:** `LoopState.fast_forward` (`godot/autoload/loop_state.gd:43`), set every frame from the T action by
  `Controls` (`godot/autoload/controls.gd:27`).
- **The state, exactly:** `LoopState.fast_forward and LoopState.phase == LoopState.Phase.NIGHT`. This is the same
  condition the HUD already uses for ">> x8" (`godot/ui/hud.gd:26`), so the glow and the label always agree.

### 1.2 The object
Hari's **phone status bar**, top-left: the clock, signal bars, battery and "loop N" label, drawn today by `HUD/HUD`
(`godot/ui/hud.gd:41-48`). That node also draws the mute icons and the talk hint, so the status bar moves into its own
Control node and only that node gets the material. Nothing about how it looks changes while the uniform is 0.

### 1.3 The shader
- **Path:** `godot/shaders/night_skip.gdshader`
- **`shader_type canvas_item;`**, no `render_mode`. **No sampler uniforms.** The colour arrives in `COLOR` from the bar's
  own draw calls.

| Uniform | Type | Hint | Default | Set by |
|---|---|---|---|---|
| `skip_amount` | `float` | `hint_range(0.0, 1.0)` | `0.0` | the driver, every frame, from the state (rules 1.5) |
| `skip_tint` | `vec4` | `source_color` | `vec4(1.0, 0.60, 0.20, 1.0)` (sodium orange, `#FF9933`) | the material; never changed by code |
| `tint_strength` | `float` | `hint_range(0.0, 1.0)` | `0.5` | the material; never changed by code. It caps how far the bar moves toward orange, so the white clock text keeps contrast against the bar (1.6) |

- **Sodium orange** is the ECR streetlight colour (GAME-BIBLE §12) and sits beside the yellow ">> x8" (`ffd36b`) without clashing.
- **No `TIME`:** the glow is steady, not pulsing, so each capture shows exactly the value the driver set and can be compared
  with 1.8. `TIME` is global engine time and couldn't link the effect to the state anyway.
- **If the contrast in 1.8 comes out under 3:1** at `skip_amount = 1.0`, `tint_strength` drops to 0.4 in a dated revision.

### 1.4 ✍ Shriram: the colour line
*(One line inside `fragment()` that changes `COLOR`, in the `mix()` form of Chapter 6, which is the easiest to predict by
hand. Every prediction in 1.8 is computed from it.)*

```glsl
COLOR.rgb = mix(COLOR.rgb, skip_tint.rgb, skip_amount * tint_strength);
```
`tint_strength = 0.5` (Shriram: "to make the orange glow visible"), so the blend fraction is t = `skip_amount` × 0.5.
At full glow the bar moves halfway to orange; it never becomes pure orange.

### 1.5 Observable rules
| # | Rule |
|---|---|
| R1 | `skip_amount` is **0.0** whenever the state is false and has been for at least 0.5 s, and **1.0** when it has been true for at least 0.25 s. |
| R2 | **Fade in: 0.25 s** from 0.0 to 1.0. **Fade out: 0.5 s** from 1.0 to 0.0. Linear in game time. Tolerance **± one frame period** (1/30, 1/60 or 1/144 s). |
| R3 | The same durations at **30, 60 and 144 fps**: the driver steps by `delta`, never by frame count. |
| R4 | **Re-press mid-fade (continue):** if the state turns true while fading out, the value turns around **from where it is** and rises at the fade-in rate. No jump, no restart from 0. |
| R5 | **State ends mid-fade-in:** the value turns around from where it is and falls at the fade-out rate (from 0.6 it reaches 0 after 0.6 × 0.5 = 0.3 s). |
| R6 | **`Engine.time_scale`:** durations are in **scaled game time** (the driver uses `_process` `delta`), like the night clock. At `time_scale = 0.5` the fade-in takes 0.5 s of real time. |
| R7 | **Paused tree:** the value **freezes** (driver `process_mode = PROCESS_MODE_PAUSABLE`) and resumes on unpause. Note: `Controls` stops updating `fast_forward` while paused (`controls.gd:25-27`), so a T held at the moment of pausing leaves the state true. The glow stays frozen until the first unpaused frame updates it. |
| R8 | **Instances:** there is one status bar, so one material. The material is not shared with any other node. |
| R9 | **Other phases:** outside `Phase.NIGHT` (crash, safe dawn, end card) the state is false, so the glow fades out even if T is held. |

### 1.6 Boundaries
Unchanged: movement, input mapping, `Controls`, `LoopState` and `Story` logic and timings, the night clock rate, every
existing test and its expectations, every other HUD element (mute icons, talk hint, toasts, dialogue, white-out), and every
3D object. Presentation code may read `LoopState`; it never writes it. The existing wall-clock timing in `Story._now()`
(`autoload/story.gd:203`, see commit `18cdc12`) is a known A2 limitation and is **not** fixed in A5.

**Contrast:** at full glow the bar background moves toward orange while the clock text stays white-ish. Compute the
text-to-bar contrast ratio at `skip_amount` = 0 and 1 (✍ in 1.8), and keep it ≥ 3:1.

### 1.7 Evidence split
| Rule | Machine (headless) | Human (eyes) |
|---|---|---|
| Shader parses, uniform names and types | `get_shader_uniform_list()` on the material; defaults read from the shader source text | — |
| R1, R2, R3 | new test: hold T through real input, sample `skip_amount` every frame from a high-`process_priority` node, at 30/60/144 fps | — |
| R4, R5 | same test: release and re-press T mid-fade; assert no jump, and assert the turn-around slope | — |
| R6 | same test with `Engine.time_scale = 0.5` | — |
| R7 | same test: pause mid-fade, step frames, assert the value is unchanged | — |
| R9 | same test: crash phase with T held, assert it falls to 0 | — |
| Colour at 0 / 0.5 / 1 | — | in-engine captures (debug key), pixels sampled against 1.8 |
| `hint_range` and code | — | capture with `skip_amount = 2.0` set from code |
| Reads as "skipping" in play | — | my playtest: hold T several times in a real run |

### 1.8 ✍ Shriram: controlled inputs and predicted values
Uniform values **0.0, 0.5, 1.0** (with `skip_tint` and `tint_strength` at their defaults). Capture with the clock held.
HDR 2D is off (`project.godot`), so 2D blending happens on the stored sRGB values. Each pixel's colour as drawn is
the `COLOR` that arrives in `fragment()`, before blending over the 3D scene.

| Named pixel (viewport px) | What's drawn there | 0.0 | 0.5 | 1.0 |
|---|---|---|---|---|
Predicted colour out of `fragment()`, 8-bit RGB, before blending:

| Named pixel (viewport px) | What's drawn there | 0.0 | 0.5 | 1.0 |
|---|---|---|---|---|
| **P1 battery fill** (200, 31) | `Color(1, 1, 1, 0.95)` (`hud.gd:47`) | (255, 255, 255) | (255, 230, 204) | (255, 204, 153) |
| **P2 bar background** (300, 46) | `Color(0.04, 0.04, 0.08, 0.6)` over the scene (`hud.gd:42`); the scene pixel behind is measured in the 0.0 capture | (10, 10, 20) | (71, 46, 28) | (133, 82, 36) |

**Working.** Orange = (1.0, 0.6, 0.2). t = `skip_amount` × 0.5. New = Start + (Orange − Start) × t, per channel, then × 255.
- **P1, white (1, 1, 1):**
  - 0.0: t = 0 → (1, 1, 1) → (255, 255, 255).
  - 0.5: t = 0.25 → R = 1 + (1 − 1)·0.25 = 1; G = 1 + (0.6 − 1)·0.25 = 0.9; B = 1 + (0.2 − 1)·0.25 = 0.8 → (255, 229.5, 204) → (255, 230, 204).
  - 1.0: t = 0.5 → G = 1 + (0.6 − 1)·0.5 = 0.8; B = 1 + (0.2 − 1)·0.5 = 0.6 → (255, 204, 153).
- **P2, dark bar (0.04, 0.04, 0.08):**
  - 0.0: t = 0 → (10.2, 10.2, 20.4) → (10, 10, 20).
  - 0.5: t = 0.25 → R = 0.04 + 0.96·0.25 = 0.28; G = 0.04 + 0.56·0.25 = 0.18; B = 0.08 + 0.12·0.25 = 0.11 → (71.4, 45.9, 28.05) → (71, 46, 28). (I first wrote 72; 71.4 rounds to 71.)
  - 1.0: t = 0.5 → R = 0.52; G = 0.32; B = 0.14 → (132.6, 81.6, 35.7) → (133, 82, 36).

**What the screen shows (transparency).** Both pixels are drawn with alpha, so the capture shows a blend:
- **P2** = 0.6 × P2 + 0.4 × background, i.e. 0.6·(0.04, 0.04, 0.08), 0.6·(0.28, 0.18, 0.11) and 0.6·(0.52, 0.32, 0.14), each + 0.4 × background. The background is measured from the 0.0 capture.
- **P1** = 0.95 × P1 + 0.05 × the bar pixel behind it, at all three values.

**Assumption:** `skip_tint` arrives unconverted as (1.0, 0.6, 0.2) because HDR 2D is off; the capture checks this. These are
predictions, not measurements; rounding or rendering differences of about ±1 per channel may occur.

**Contrast ratio**, clock text/battery vs bar, using the colours before transparency (sRGB decode, then relative luminance
L = 0.2126 R + 0.7152 G + 0.0722 B, ratio = (L_light + 0.05) / (L_dark + 0.05)):

| State | Battery L | Bar L | Ratio | ≥ 3:1 |
|---|---|---|---|---|
| No glow (0.0): (255, 255, 255) vs (10.2, 10.2, 20.4) | 1.0000 | 0.00339 | **19.67:1** | pass |
| Full glow (1.0): (255, 204, 153) vs (132.6, 81.6, 35.7) | 0.66746 | 0.11054 | **4.47:1** | pass |

So `tint_strength = 0.5` stays. The capture checks the real on-screen contrast, which also depends on transparency and the
scene behind the bar.

### 1.9 Failure cases
| # | Prediction | Check |
|---|---|---|
| F1 | The fade counts frames, so it lasts 2× longer at 30 fps than at 60 | per-frame samples at 30/60/144; durations within one frame |
| F2 | A re-press snaps to 0 (restart) instead of continuing | test R4: no single-frame drop greater than one fade-in step |
| F3 | The material sits on the whole HUD, so the mute icons glow too | capture: the SFX label pixel is unchanged at 1.0; test asserts the material is on the status-bar node only |
| F4 | A renamed uniform: the driver writes a name the shader doesn't declare, which raises no error | uniform-list assertion (mutation 2) |
| F5 | The glow keeps fading during pause | test R7 |

---

## Part 2. Textured shader: the marble deck (dry and wet)

### 2.1 The object and lighting
- **Dry marble:** the deck floors `Deck/FloorWest`, `FloorEast`, `FloorFront` in `godot/scenes/slice.tscn`. Today each is a
  `StandardMaterial3D` built in code by `godot/scenes/textured_surface.gd` from the generated `marble.png`.
- **Wet marble:** `Deck/FloorBack`, the thin strip at the pool's back edge.
- **Lighting I judge under:** the slice at a held clock time of **10:00 PM**, under the string lights and the pool glow,
  with the slice's own environment (Filmic tonemap `tonemap_mode = 2` and glow on, `slice.tscn:31-32`). For close
  comparisons I switch glow off and say so. No SSAO is set in the slice.
- The four planes are different sizes (their `uv_tiles` today are 4×8, 10×8, 7×0.8 and 7×4.8, `slice.tscn:100-124`), so the
  shader takes its UVs from **world XZ**. That way one material tiles at the same scale on every plane.

### 2.2 Textures
Poly Haven **Marble 01** (`marble_01`) by Rob Tuytel, CC0, 2K PNG: <https://polyhaven.com/a/marble_01>.
Credits go in `godot/assets/textures/marble_01/ATTRIBUTION.md`.

| File | Role | What its numbers mean | Sampled as | compress/mode | compress/normal_map | mipmaps/generate |
|---|---|---|---|---|---|---|
| `marble_01_diff_2k.png` | albedo | sRGB-encoded colour | **colour**, `source_color` | 2 (VRAM Compressed) | 2 (Disabled) | true |
| `marble_01_rough_2k.png` | roughness | linear 0–1 roughness per texel (grey) | **data**, no `source_color` | 2 (VRAM Compressed) | 2 (Disabled) | true |
| `marble_01_nor_gl_2k.png` | normal map, **OpenGL** convention (Godot's) | tangent-space normal, xyz packed as 0.5 + 0.5·n | **data**, `hint_normal` | 2 (VRAM Compressed) | 1 (Enable) | true |
| `marble_01_nor_dx_2k.png` | calibration only (DirectX convention) | same, green flipped | not used by a material | 0 (Lossless) | 2 (Disabled) | false |

Curl-check calibration pair: Marble 01 is polished and its normal map is **very flat**, which the assignment warns drifts
toward 1. So I also calibrate on **Floor Tiles 06** (`floor_tiles_06`, Rob Tuytel, CC0) `nor_gl` + `nor_dx`, which have
strong grout relief. Calibration files live under `godot/tests/data/curl/` and are not used in the game.

### 2.3 Shader and uniforms
- **Path:** `godot/shaders/deck_marble.gdshader`, `shader_type spatial;`, default (lit) render mode.
- Samplers: `albedo_tex` (`source_color`, `filter_linear_mipmap`, `repeat_enable`), `roughness_tex` (no `source_color`,
  `filter_linear_mipmap`, `repeat_enable`), `normal_tex` (`hint_normal`, `filter_linear_mipmap`, `repeat_enable`).

| Group | Uniform | Type | Hint / range | Default | What changes on screen across the range |
|---|---|---|---|---|---|
| `surface` | `albedo_tint` | `vec4` | `source_color` | white | multiplies the marble colour; darker or warmer stone |
| `surface` | `tile_size_m` | `float` | `hint_range(0.25, 4.0)` | `1.0` | metres per texture repeat: small values give busy veins, large ones stretched veins |
| `finish` | `roughness_scale` | `float` | `hint_range(0.0, 2.0)` | `1.0` | 0 = mirror-glossy highlights of the string lights; 2 = chalky, no highlights |
| `finish` | `specular_amount` | `float` | `hint_range(0.0, 1.0)` | `0.5` | strength of the highlight at grazing angles |
| `finish` | `normal_depth` | `float` | `hint_range(0.0, 2.0)` | `1.0` | 0 = flat; 2 = deep vein relief |

### 2.4 The two materials
| Material | Used on | Differs in | Why |
|---|---|---|---|
| `godot/materials/marble_dry.tres` | FloorWest, FloorEast, FloorFront | defaults (`roughness_scale 1.0`, `specular_amount 0.5`) | the family's polished Italian marble |
| `godot/materials/marble_wet.tres` | FloorBack (pool edge) | **`roughness_scale 0.3`, `specular_amount 0.8`** | water on the stone makes it glossier: sharper, brighter highlights of the string lights (Shriram's choice: "glossier") |

### 2.5 The hint experiment
- `godot/tools/write_hint_strip.gd` writes `godot/assets/textures/hint_strip_3x1.png`: three texels of greys **64, 128,
  192**. Imported `compress/mode = 0` (Lossless), `mipmaps/generate = false`.
- `godot/shaders/hint_experiment.gdshader`: `spatial`, `render_mode unshaded`. Two samplers bound to that one file: one with
  `source_color, filter_nearest`, one with `filter_nearest` only. A `bool` uniform picks which writes `ALBEDO`.
- Two materials (one per bool) on two camera-facing quads in `godot/scenes/hint_experiment.tscn`. The WorldEnvironment has
  a **Linear** tonemap, exposure 1.0, and glow, fog and adjustments off. Renderer: Forward+.

✍ **Predicted displayed 8-bit value of each band** (show the encode() working):

| Quad | band 64 | band 128 | band 192 |
|---|---|---|---|
| A: `source_color` | 64 | 128 | 192 |
| B: no hint | 137 | 188 | 225 |

**Working.**
- **Quad A:** Godot decodes the sRGB value to linear, and the display encodes it back. The two operations reverse each
  other, so the file's values come back unchanged.
- **Quad B:** the value reaches the shader as stored (x = grey/255) and is encoded as if it were linear,
  `encode(x) = 1.055·x^(1/2.4) − 0.055`, then × 255:
  - 64: x = 0.25098 → **137**
  - 128: x = 0.50196 → **188**
  - 192: x = 0.75294 → **225**

**Which quad shows the file's values unchanged, and why:** Quad A preserves the original greys (64, 128, 192) because
`source_color` makes Godot decode sRGB into linear colour, and the final screen encoding reverses that conversion. Quad B
appears brighter because its values are encoded without first being decoded.

### 2.6 Failure cases
| # | Prediction | Check |
|---|---|---|
| F6 | `roughness_tex` sampled with `source_color`, so roughness is decoded like colour and comes out wrong | material test reads hints from the shader source |
| F7 | `albedo_tex` without `source_color`: washed-out, too bright marble | material test; mutation 3 (remove `source_color`) must exit 1 |
| F8 | The normal map imported without `compress/normal_map = 1`, or in the DirectX convention, so the veins look inverted | `.import` assertions; curl ratio under both conventions |
| F9 | The editor rewrites an import setting on first open | `git status` after the first editor session; any diff explained |
| F10 | Marble tiles at different scales on different planes | world-XZ UVs; my eyes at the plane seams |

---

## Part 3. ✍ Shriram: short answers (predictions, to check in Use It)
*Shriram's answers, worked out with ChatGPT's help (see SOURCES.md), and checked by Claude. Additions made after
Claude's check are marked.*

1. **Renderer, and what it rules out.** Forward+: `renderer/rendering_method="forward_plus"` in `godot/project.godot`
   (Shriram read it there).  none of the listed features
   are ruled out. Decals and compute shaders need Forward+ or Mobile, and VoxelGI, SDFGI and SSIL need Forward+, which
   this project has. The cost is reach: Forward+ needs a desktop-class GPU (Vulkan, Metal or D3D12), and a web or
   low-end export would need Compatibility. The hint-experiment predictions assume Forward+ or Mobile, so they hold.
2. **What colour arrives in `fragment()`.** The `COLOR` value will be the original colour used in `draw_rect`, because
   the rectangle has no actual image texture. Godot uses a white texture, so multiplying it by the draw colour keeps the
   original colour. The tempting alternative is answer 3.
3. **`texture(TEXTURE, UV)` instead of `COLOR`.** Every pixel would become white (1.0, 1.0, 1.0), because it only samples
   the default white texture and ignores the rectangle's original draw colour. *(Added after Claude's check:)* alpha
   would also become 1.0, so the 60%-transparent bar would turn into a solid opaque white block.
4. **Spatial: `ALBEDO` and `COLOR`.** If I don't write anything to `ALBEDO`, its default colour is white (1.0, 1.0, 1.0).
   In a spatial shader, `COLOR` contains the mesh's vertex colours rather than the CanvasItem draw colour. (Source: the
   Godot documentation's spatial shader built-ins page; to re-check against the 4.7 docs, since this project runs
   4.7.2.)
5. **A frame-counting fade.** At 60 FPS, a 0.25-second fade takes 15 frames. If I use the same 15 frames at 30 FPS, it
   takes 0.5 seconds, and at 144 FPS about 0.104 seconds. This shows why using delta time is better than counting frames.
6. **Default vs current value.** The default value is defined in the shader code, while the current uniform value is
   stored in the ShaderMaterial. If two objects share the same material and I change that uniform, both objects get the
   updated value.
7. **Does `hint_range` clamp a value set from code?** My prediction is that `hint_range` only controls the slider range
   in the Inspector and doesn't clamp values assigned through code. So if I set `skip_amount` to 2.0, I expect the
   shader to receive 2.0, even though the slider range ends at 1.0.

---

## Revision 2, 2026-11-01 (Claude, recording deviations found in review; the text above is unchanged)
- **§2.2 import settings:** every A5 texture also has `detect_3d/compress_to=0`, which §2.2 doesn't list. It stops the
  editor changing a Lossless texture to VRAM on first use in 3D (F9). No editor session rewrote an `.import` file
  (TEST-REPORT A5.8). Pinned by `test_materials.gd`.
- **§2.1 lighting:** the slice also has fog on (`fog_density 0.011`, `slice.tscn:38-40`), which tints the far floor. It
  is part of the light the marble is judged under (MATERIALS.md finding K). Not changed.
- **§1.8:** the header of the prediction table appears twice (an editing slip). The table under it is the one used.
- **§1.8 on-screen check:** the background behind P2 was measured from a capture with the bar hidden (TEST-REPORT A5.4).
  The predictions out of `fragment()` are unchanged.
