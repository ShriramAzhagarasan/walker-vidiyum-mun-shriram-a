# MATERIALS.md — audit of the A5 materials

Headless read-only audit of every ShaderMaterial named in `CHANGE-BRIEF.md`, the shaders they bind, the textures those
shaders sample, every texture's `.import` settings, and the scene environment and lights that light them. Written before
`godot/tests/test_materials.gd`, which pins every row below. Nothing in this file is a change: it is what is on disk at
HEAD, cross-referenced against `CHANGE-BRIEF.md`.

Headless draws nothing, so this audit can only establish parsing, resource wiring, uniform contracts and import flags.
How the materials look under the slice's lights is a human check (CHANGE-BRIEF.md §1.7, §2.1).

---

## 1. Materials

### `godot/materials/night_skip.tres` (CHANGE-BRIEF.md §1.3)

| Field | Value | Source line |
|---|---|---|
| `type` | `ShaderMaterial` | `night_skip.tres:1` |
| `shader` | `res://shaders/night_skip.gdshader` | `night_skip.tres:3,6` |
| overridden uniforms | *(none)* — all three defaults come from the shader source | `night_skip.tres:5-7` |

Used on `HUD/StatusBar` (`godot/scenes/slice.tscn:275`). The driver (`HUD/StatusBar/NightSkipDriver`,
`slice.tscn:283-284`) writes `skip_amount` every frame; `skip_tint` and `tint_strength` are material-side (§1.3).

### `godot/materials/marble_dry.tres` (CHANGE-BRIEF.md §2.4)

| Field | Value | Source line |
|---|---|---|
| `type` | `ShaderMaterial` | `marble_dry.tres:1` |
| `shader` | `res://shaders/deck_marble.gdshader` | `marble_dry.tres:3,9` |
| `shader_parameter/albedo_tex` | `res://assets/textures/marble_01/marble_01_diff_2k.png` | `marble_dry.tres:4,10` |
| `shader_parameter/roughness_tex` | `res://assets/textures/marble_01/marble_01_rough_2k.png` | `marble_dry.tres:5,11` |
| `shader_parameter/normal_tex` | `res://assets/textures/marble_01/marble_01_nor_gl_2k.png` | `marble_dry.tres:6,12` |
| `shader_parameter/albedo_tint` | *(not set — shader default `vec4(1.0)`, white)* | — |
| `shader_parameter/tile_size_m` | *(not set — shader default `1.0`)* | — |
| `shader_parameter/roughness_scale` | *(not set — shader default `1.0`)* | — |
| `shader_parameter/specular_amount` | *(not set — shader default `0.5`)* | — |
| `shader_parameter/normal_depth` | *(not set — shader default `1.0`)* | — |

Used on `Deck/FloorWest`, `Deck/FloorEast`, `Deck/FloorFront` (`slice.tscn:102,107,117`) via `material_override`.
CHANGE-BRIEF.md §2.4 reads *"defaults (`roughness_scale 1.0`, `specular_amount 0.5`)"*; the material achieves this by not
overriding the uniforms rather than restating them. Both styles give the same runtime value.

### `godot/materials/marble_wet.tres` (CHANGE-BRIEF.md §2.4)

| Field | Value | Source line |
|---|---|---|
| `type` | `ShaderMaterial` | `marble_wet.tres:1` |
| `shader` | `res://shaders/deck_marble.gdshader` | `marble_wet.tres:3,9` |
| `shader_parameter/albedo_tex` | `res://assets/textures/marble_01/marble_01_diff_2k.png` | `marble_wet.tres:4,10` |
| `shader_parameter/roughness_tex` | `res://assets/textures/marble_01/marble_01_rough_2k.png` | `marble_wet.tres:5,11` |
| `shader_parameter/normal_tex` | `res://assets/textures/marble_01/marble_01_nor_gl_2k.png` | `marble_wet.tres:6,12` |
| `shader_parameter/roughness_scale` | `0.3` | `marble_wet.tres:13` |
| `shader_parameter/specular_amount` | `0.8` | `marble_wet.tres:14` |
| other `shader_parameter/*` | *(not set — defaults as above)* | — |

Used on `Deck/FloorBack` (`slice.tscn:112`) via `material_override`. Matches §2.4 (wet is `0.3` / `0.8`).

### `godot/materials/hint_a_source_color.tres` (CHANGE-BRIEF.md §2.5)

| Field | Value | Source line |
|---|---|---|
| `type` | `ShaderMaterial` | `hint_a_source_color.tres:1` |
| `shader` | `res://shaders/hint_experiment.gdshader` | `hint_a_source_color.tres:3,7` |
| `shader_parameter/strip_as_colour` | `res://assets/textures/hint_strip_3x1.png` | `hint_a_source_color.tres:4,8` |
| `shader_parameter/strip_as_data` | `res://assets/textures/hint_strip_3x1.png` | `hint_a_source_color.tres:4,9` |
| `shader_parameter/use_source_color` | `true` | `hint_a_source_color.tres:10` |

Used on `QuadA` (`hint_experiment.tscn:32`).

### `godot/materials/hint_b_no_hint.tres` (CHANGE-BRIEF.md §2.5)

| Field | Value | Source line |
|---|---|---|
| `type` | `ShaderMaterial` | `hint_b_no_hint.tres:1` |
| `shader` | `res://shaders/hint_experiment.gdshader` | `hint_b_no_hint.tres:3,7` |
| `shader_parameter/strip_as_colour` | `res://assets/textures/hint_strip_3x1.png` | `hint_b_no_hint.tres:4,8` |
| `shader_parameter/strip_as_data` | `res://assets/textures/hint_strip_3x1.png` | `hint_b_no_hint.tres:4,9` |
| `shader_parameter/use_source_color` | `false` | `hint_b_no_hint.tres:10` |

Used on `QuadB` (`hint_experiment.tscn:37`).

---

## 2. Samplers, their hints, and the textures each material binds

Hints are read verbatim from the shader source. `source_color` makes Godot decode sRGB → linear on sample.

### `godot/shaders/deck_marble.gdshader`

| Sampler | Hints in source | `marble_dry` binds | `marble_wet` binds |
|---|---|---|---|
| `albedo_tex` | `source_color, filter_linear_mipmap, repeat_enable` (`deck_marble.gdshader:5`) | `marble_01_diff_2k.png` | `marble_01_diff_2k.png` |
| `roughness_tex` | `filter_linear_mipmap, repeat_enable` (`deck_marble.gdshader:10`) | `marble_01_rough_2k.png` | `marble_01_rough_2k.png` |
| `normal_tex` | `hint_normal, filter_linear_mipmap, repeat_enable` (`deck_marble.gdshader:11`) | `marble_01_nor_gl_2k.png` | `marble_01_nor_gl_2k.png` |

Non-sampler uniforms declared in `deck_marble.gdshader`:

| Uniform | Hint / range | Default | `marble_dry` sets | `marble_wet` sets |
|---|---|---|---|---|
| `albedo_tint` : `vec4` | `source_color` (`:6`) | `vec4(1.0)` | — | — |
| `tile_size_m` : `float` | `hint_range(0.25, 4.0)` (`:7`) | `1.0` | — | — |
| `roughness_scale` : `float` | `hint_range(0.0, 2.0)` (`:12`) | `1.0` | — | `0.3` |
| `specular_amount` : `float` | `hint_range(0.0, 1.0)` (`:13`) | `0.5` | — | `0.8` |
| `normal_depth` : `float` | `hint_range(0.0, 2.0)` (`:14`) | `1.0` | — | — |

### `godot/shaders/hint_experiment.gdshader`

| Sampler | Hints in source | `hint_a_source_color` binds | `hint_b_no_hint` binds |
|---|---|---|---|
| `strip_as_colour` | `source_color, filter_nearest` (`hint_experiment.gdshader:5`) | `hint_strip_3x1.png` | `hint_strip_3x1.png` |
| `strip_as_data` | `filter_nearest` (`hint_experiment.gdshader:6`) | `hint_strip_3x1.png` | `hint_strip_3x1.png` |

Non-sampler uniform:

| Uniform | Default | `hint_a_source_color` sets | `hint_b_no_hint` sets |
|---|---|---|---|
| `use_source_color` : `bool` (`:8`) | `false` | `true` | `false` |

### `godot/shaders/night_skip.gdshader`

No samplers (`night_skip.gdshader:1-9`): the bar's draw colour arrives in `COLOR`. Non-sampler uniforms declared in the
source:

| Uniform | Hint | Default | `night_skip.tres` sets |
|---|---|---|---|
| `skip_amount` : `float` | `hint_range(0.0, 1.0)` (`:3`) | `0.0` | — (driver writes it) |
| `skip_tint` : `vec4` | `source_color` (`:4`) | `vec4(1.0, 0.6, 0.2, 1.0)` | — |
| `tint_strength` : `float` | `hint_range(0.0, 1.0)` (`:5`) | `0.5` | — |

---

## 3. Texture import settings (from the `.import` files)

| File | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | Matches CHANGE-BRIEF |
|---|---|---|---|---|
| `marble_01_diff_2k.png` | `2` (VRAM Compressed) | `2` (Disabled) | `true` | §2.2 ✓ (`marble_01_diff_2k.png.import:19,25,27`) |
| `marble_01_rough_2k.png` | `2` (VRAM Compressed) | `2` (Disabled) | `true` | §2.2 ✓ (`marble_01_rough_2k.png.import:19,25,27`) |
| `marble_01_nor_gl_2k.png` | `2` (VRAM Compressed) | `1` (Enable) | `true` | §2.2 ✓ (`marble_01_nor_gl_2k.png.import:19,25,27`) |
| `marble_01_nor_dx_2k.png` | `0` (Lossless) | `2` (Disabled) | `false` | §2.2 ✓, calibration only (`marble_01_nor_dx_2k.png.import:18,24,26`) |
| `hint_strip_3x1.png` | `0` (Lossless) | `2` (Disabled) | `false` | §2.5 ✓ (`hint_strip_3x1.png.import:18,24,26`) |

All five also have `detect_3d/compress_to=0` so the editor cannot rewrite the compression on first 3D use (F9,
`ATTRIBUTION.md:12-13`).

---

### Formats measured after import *(added in review)*

`get_image().get_format()` on this machine (macOS, desktop import), pinned by `test_materials.gd`:

| File | Format | What it confirms |
|---|---|---|
| `marble_01_diff_2k.png` | `FORMAT_DXT1` (17), mipmaps | `compress/mode = 2` is VRAM Compressed |
| `marble_01_rough_2k.png` | `FORMAT_DXT1` (17), mipmaps | as above |
| `marble_01_nor_gl_2k.png` | `FORMAT_RGTC_RG` (21), mipmaps | `compress/normal_map = 1` is Enable: two-channel normal compression |
| `marble_01_nor_dx_2k.png` | `FORMAT_RGB8` (4), no mipmaps, uncompressed | `compress/mode = 0` is Lossless |
| `hint_strip_3x1.png` | `FORMAT_RGB8` (4), no mipmaps, uncompressed | as above |

Engine constants checked the same way: `Environment.TONE_MAPPER_FILMIC = 2`, `TONE_MAPPER_LINEAR = 0`, `BG_COLOR = 1`,
`BG_SKY = 2`, `AMBIENT_SOURCE_COLOR = 2`, `Camera3D.PROJECTION_ORTHOGONAL = 1`.

---

## 4. Lights and environment that change the look

### Slice (`godot/scenes/slice.tscn`) — the lighting the dry/wet marble is judged under (§2.1)

| Node | Type | Settings | Line |
|---|---|---|---|
| `WorldEnvironment/Env` | `Environment` | `background_mode = 2` (Sky); `ambient_light_source = 2`, `ambient_light_color (0.16, 0.16, 0.3)`, `ambient_light_energy 1.0`; **`tonemap_mode = 2` (Filmic)**, tonemap_exposure default `1.0`; **`glow_enabled = true`**; `fog_enabled = true`, `fog_light_color (0.2, 0.18, 0.36)`, `fog_density 0.011` | `:30-40` |
| `SkyLight` | `DirectionalLight3D` | `rotation (-55°, 35°, 0)`; `light_color (0.56, 0.63, 1)`; `light_energy 0.3`; shadows on | `:84-88` |
| `Deck/PoolGlow` | `OmniLight3D` | `position (12.5, 0.4, -2)`; `light_color (0.3, 0.85, 1)`; `light_energy 1.2`; `omni_range 5.0` | `:127-131` |
| `Backdrops/FireLight` | `OmniLight3D` | `light_energy 0.0` (off at 10:00 PM) | `:187-191` |
| `SUV/Headlights` | `SpotLight3D` | `light_energy 0.0` (off at 10:00 PM) | `:200-206` |
| String lights (×3) | `OmniLight3D`, added in code by `deck_dressing.gd:42-47` | `light_color = STRING_LIGHT_COLOR (1.0, 0.66, 0.36)` (`deck_dressing.gd:13`); `light_energy 2.8`; `omni_range 7.0`; one per gap between `LIGHT_XS = [6, 10, 14, 18]`, at `y = 2.7`, `z = -3.6 + 1.2` | `deck_dressing.gd:11-13, 42-47` |

The brief's **10:00 PM** judgement light (§2.1) is the SkyLight + the string lights + the pool glow, under Filmic tone
mapping with glow on. No SSAO is set.

### Hint-experiment (`godot/scenes/hint_experiment.tscn`) — unlit (§2.5)

| Field | Value | Line |
|---|---|---|
| `Environment` | `background_mode = 1` (Color), `background_color (0, 0, 0)` | `:7-8` |
| `tonemap_mode` | `0` (**Linear**) | `:9` |
| `tonemap_exposure` | `1.0` | `:10` |
| `glow_enabled` | `false` | `:11` |
| `fog_enabled` | `false` | `:12` |
| `adjustment_enabled` | `false` | `:13` |
| lights | *none* (the shader is `render_mode unshaded`, `hint_experiment.gdshader:3`) | — |
| Camera | orthographic (`projection = 1`), `size 3.0`, forward `(0, 0, 5)` | `:23-27` |

---

## 5. Findings

Nothing on disk contradicts CHANGE-BRIEF.md; this section lists the small things worth pinning in the test anyway.

| # | Finding | Evidence |
|---|---|---|
| A | Both marble materials point at the same shader resource, and at the OpenGL normal map (not DX). | `marble_dry.tres:3,6`, `marble_wet.tres:3,6` |
| B | `marble_dry.tres` is shared by the three dry floors (`FloorWest`, `FloorEast`, `FloorFront`); `marble_wet.tres` is used by `FloorBack` only. CHANGE-BRIEF.md R8 is about the night-skip material only; sharing is intended here. | `slice.tscn:102,107,117` |
| C | `marble_dry.tres` sets no `shader_parameter/*` beyond the three textures. CHANGE-BRIEF.md §2.4 reads *"defaults"*, so this is correct: the dry values are the shader defaults at `deck_marble.gdshader:7,12,13,14`, and a change to a default there changes the dry floors but not the wet one's two overrides. | `marble_dry.tres:8-12` |
| D | Both hint materials bind `hint_strip_3x1.png` to **both** samplers even though `use_source_color` picks one branch. Harmless (the unused sampler just holds a reference), but worth noting: a per-material binding would only ever read one path. | `hint_a_source_color.tres:8-10`, `hint_b_no_hint.tres:8-10` |
| E | `strip_as_data` has no `source_color` **and** no other hint; `strip_as_colour` has `source_color` with the same filter. This is what §2.5 requires. | `hint_experiment.gdshader:5-6` |
| F | `marble_01_rough_2k.png` is sampled without `source_color` on `roughness_tex` (so values are read linearly, as the brief wants, F6). | `deck_marble.gdshader:10` |
| G | `marble_01_nor_dx_2k.png` is imported Lossless with no mipmaps and is not referenced by any `.tres` — calibration only, consistent with §2.2. | `marble_01_nor_dx_2k.png.import:18,26`, grep over `godot/materials/*.tres` |
| H | `hint_strip_3x1.png` is imported Lossless with no mipmaps (§2.5), using `filter_nearest` in the shader, so the three texels will not be averaged across the band boundaries. | `hint_strip_3x1.png.import:18,26`, `hint_experiment.gdshader:5-6` |
| I | The slice environment is Filmic with glow on; the hint-experiment environment is Linear with glow and adjustments off. The hint-experiment predictions in §2.5 assume Linear + exposure 1.0; the file matches. | `slice.tscn:36-37`, `hint_experiment.tscn:9-13` |
| J | No material under `godot/materials/` references the DX normal (`marble_01_nor_dx_2k.png`). Pinned by the test so a future hand-edit cannot swap conventions silently. | grep over `godot/materials/*.tres` |
| K | *(Added in review.)* The slice has **fog on** (`fog_enabled = true`, `fog_density 0.011`), but CHANGE-BRIEF.md §2.1's lighting statement names only Filmic tone mapping and glow. Fog tints the far floor toward `fog_light_color`, so it is part of the light the marble is judged under. Recorded, not changed. | `slice.tscn:38-40` |

---

## 6. Attribution

From CHANGE-BRIEF.md §2.2 (checked by Shriram, not rewritten here):

- **Marble 01** (`marble_01`) by Rob Tuytel — CC0 1.0 — <https://polyhaven.com/a/marble_01>.
  Files: `marble_01_diff_2k.png`, `marble_01_rough_2k.png`, `marble_01_nor_gl_2k.png`, `marble_01_nor_dx_2k.png`
  (2K PNG). Credits live in `godot/assets/textures/marble_01/ATTRIBUTION.md`.
- **Floor Tiles 06** (`floor_tiles_06`) by Rob Tuytel — CC0 1.0 — <https://polyhaven.com/a/floor_tiles_06>.
  Files: `floor_tiles_06_nor_gl_2k.png`, `floor_tiles_06_nor_dx_2k.png` under `godot/tests/data/curl/`, calibration
  only for the normal-map curl check (§2.2, F8); a `.gdignore` keeps Godot from importing them.

CC0 needs no attribution; it is given anyway. Files are unmodified.

---

## Review (Claude, 2026-11-01)

The sections above are the agent's audit (commit `a1acfaa`); the review changed only the lines marked here.
- Every integer enum was looked up by measurement (formats and engine constants above). All the audit's enum names were correct.
- Deleted "~2700 K" for the string lights: nobody measured a colour temperature.
- Finding B said *both* marble materials are shared by the three dry floors; only `marble_dry` is.
- Finding C's last clause was confused; rewritten.
- Added finding K (fog on in the slice, not in brief §2.1).
- `test_materials.gd`: its hint checks were substring matches, so `source_color` added to `roughness_tex`,
  `normal_tex` or `strip_as_data` (F6) still passed. Added a no-`source_color` check per data sampler, the format
  checks above, and the slice environment (Filmic, glow, fog). 145 → 156 checks, all PASS.
