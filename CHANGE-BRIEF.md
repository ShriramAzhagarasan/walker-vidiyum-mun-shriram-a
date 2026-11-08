# Change brief: Assignment 6, two particle effects (A6)

*Revision 1, 2026-11-08, committed before the first build prompt.*
*Authorship: everything marked **✍** is Shriram's: the intent, every value, every rule, every prediction, the budget and
the short answers. Shriram chose the two effects and the retrigger rule on 2026-11-08 from options Claude laid out.
Claude wrote §0 (project facts, each checked in the files or in the engine) and the empty headings, following the
assignment's list. Claude chose no value, rule, prediction or budget. Later changes go in dated revisions at the
bottom; this text is not rewritten.*

The A5 brief is at tag `a5` and archived in `design/briefs/CHANGE-BRIEF-A5.md`; the A2/A3 briefs are in
`design/briefs/CHANGE-BRIEF-A2-A3.md`.

---

## 0. Project facts (Claude, checked 2026-11-08)

**Engine.** Godot 4.7.2.stable.official.ed1daf0bf, Forward+ (`godot/project.godot:38`). Viewport 1280×720, stretch
`canvas_items` (`project.godot:31-34`). The game scene is `res://scenes/slice.tscn`. It is 3D, so both effects are 3D.

**Hari and the footstep event (Effect A).**
- Hari is a `CharacterBody3D` (`slice.tscn:236`, `godot/scenes/hari.gd`). He is 1.75 m tall and walks at 2.2 m/s
  (`godot/logic/hari_spec.gd:4,7`).
- Walk frames advance every `STRIDE_M = 0.42` m of travel (`hari.gd:11,69,72`). There are 4 frames (`walk_1..4.png`).
- The step bob is lowest, which is the foot contact, when `_travel / STRIDE_M` = 2k + 0.5 (`hari.gd:74-75`). That makes
  one footfall per 0.84 m, about every **0.38 s** at full speed.
- **No footstep signal exists today.** The trigger code in Step 3 has to detect the contact.
- `Story.hari_state` is `"WALK"` while moving (`godot/autoload/story.gd:25,60`). Movement stops while
  `Story.movement_locked()` (`hari.gd:43`).

**String lights (Effect B).** Built in code by `godot/scenes/deck_dressing.gd`:
- Poles stand at x = 6, 10, 14, 18 and z = −3.6 (`:11-12`).
- Seven bulbs per span sag between y = 3.1 and 2.65 at z ≈ −3.55 (`:39-41`).
- One warm `OmniLight3D` per span sits at x = 8, 12, 16, y = 2.7, z = −2.4. Its colour is (1.0, 0.66, 0.36), about
  2700 K (`:13,42-46`).

**Night, dawn, crash, pause.**
- `LoopState.phase` is one of `NIGHT, CRASH, SAFE_DAWN, ENDED` (`godot/autoload/loop_state.gd:18`).
- `clock_minutes` counts from midnight of the party day, so 8:00 PM = 1200 and 5:50 AM dawn = 1790 (`:21,30`).
- The sky starts to lighten at **1740 (5:00 AM)** (`godot/scenes/slice.gd:28`). The fire glow starts at 4:45 AM
  (`loop_state.gd:29`).
- A crash resets the loop to 8:00 PM after 4 s (`loop_state.gd:31,60-63`).
- P or Esc pauses the tree (`godot/logic/input_setup.gd:13`, `controls.gd:19-20`, `loop_state.gd:90-91`).

**Camera.** The deck preset sits 4.5 m from Hari and 1.9 m up, FOV 45° (`godot/scenes/camera_rig.gd:7`).

**Background.**
- The deck floor is dark marble (A5's `marble_dry`/`marble_wet`), lit warm under the string lights between x ≈ 4 and 21
  (`slice.gd:208`) and cool-dark elsewhere.
- The sky is near-black navy until 5:00 AM (`slice.gd:24-28`).
- The darkest stretch is the gate end (x < 5). The lightest is the deck right under the bulbs and the pool glow.

**Node types available in this build** (checked with `get_property_list()` on 4.7.2):
- `GPUParticles3D` has `amount_ratio`, `use_fixed_seed`, `seed`, `preprocess`, `visibility_aabb`, `trail_enabled`
  and `sub_emitter`.
- `CPUParticles3D` has **no** `amount_ratio`, turbulence or attractor.
- `GPUParticlesAttractorSphere3D` exists (`radius`, `strength`, `attenuation`, `directionality`).
- `ParticleProcessMaterial` has `initial_velocity_min/_max`, `scale_min/_max`, `scale_curve`, `color_ramp`,
  `alpha_curve`, `hue_variation_min/_max`, `damping_min/_max` and the `turbulence_*` properties.
- `StandardMaterial3D` has `vertex_color_use_as_albedo`, `transparency`, `billboard_mode` (`BILLBOARD_PARTICLES` = 3)
  and `blend_mode`.

**Godot 3 names in this build.**
- `scale_random` does not exist.
- `initial_velocity` and `scale` exist only as editor-only `Vector2` aliases (usage 12, not stored).
- Setting `initial_velocity = 5.0` the Godot 3 way leaves `initial_velocity_min/_max` at their default 0.
- The scene loads without an error either way.

**Pause behaviour.** A `GPUParticles3D` whose `can_process()` is false stops advancing while the tree is paused. Headless
can observe `can_process()`, `emitting` and `visible`, never the frozen picture.

---

## Part A. Effect A: sand scuff on Hari's footsteps

### A.1 The job ✍
<!-- What it tells the player, and why the player needs it. The script and variable/signal that hold the event
(see §0: there is no signal yet). -->

### A.2 How it reads (intent) ✍
<!-- Timing phases with rough durations (first frame / outward / dissipation). Contrast against the darkest and lightest
real backgrounds (§0). Scale against Hari (1.75 m). Change over life (colour, alpha, scale). Variation (velocity,
scale, hue, rotation). Each emitter and its job. -->

### A.3 Settings ✍
Node type (CPU or GPU, 3D) and why:

| Emitter | Group | Property (Godot 4 name) | Value |
|---|---|---|---|
| | emission | `amount` | |
| | emission | `one_shot` | |
| | emission | `explosiveness` | |
| | emission | `lifetime` | |
| | emission | `emission_shape` (+ radius or extents) | |
| | process | `direction`, `spread` | |
| | process | `initial_velocity_min` / `initial_velocity_max` | |
| | process | `gravity` | |
| | process | `damping_min` / `damping_max` | |
| | process | `scale_min` / `scale_max`, `scale_curve` | |
| | process | `color_ramp` (colour and alpha over life) | |
| | process | variation: `hue_variation_*`, `angle_*` | |
| | draw | `draw_pass_1` mesh and size | |
| | draw | material: texture, `vertex_color_use_as_albedo`, `transparency`, `blend_mode`, `billboard_mode` | |
| | node | `local_coords` (and why) | |
| | node | `visibility_aabb`: generated, or set and checked | |
| | node | `preprocess` | |

### A.4 Observable rules ✍
<!-- Fires on every footfall the retrigger rule allows, never otherwise (including scene load, standing still, talking,
paused), at the foot's position. Retrigger rule: OVERLAP (chosen 2026-11-08), with the most bursts alive at once.
What happens if the node it would follow is freed on the same event. -->

---

## Part B. Effect B: moths at the string lights (ambience)

### B.1 The job ✍
<!-- What it tells the player. The script and variables that hold the condition. Job: ambience. The process or draw
feature it uses that Effect A doesn't (e.g. turbulence, an attractor, a box emission shape, preprocess). -->

### B.2 How it reads (intent) ✍
<!-- Same six headings as A.2. -->

### B.3 Settings ✍
Node type and why:

| Emitter | Group | Property (Godot 4 name) | Value |
|---|---|---|---|
| | emission | `amount`, `one_shot`, `explosiveness`, `lifetime` | |
| | emission | `emission_shape` + extents | |
| | process | `direction`, `spread`, `initial_velocity_min/_max`, `gravity`, `damping_min/_max` | |
| | process | the B-only feature (e.g. `turbulence_enabled`, `turbulence_noise_strength`, `turbulence_noise_scale`; or attractor `radius`/`strength`) | |
| | process | `scale_min/_max`, `scale_curve`, `color_ramp` | |
| | draw | mesh, material, texture, `blend_mode`, `billboard_mode` | |
| | node | `local_coords`, `visibility_aabb`, `preprocess` | |

### B.4 Observable rules ✍
<!-- Starts when its condition begins, stops when it ends. What it does while the tree is paused, and while it is hidden.
What it shows on the first frame after the scene loads. -->

---

## Part C. Boundaries ✍
<!-- What stays unchanged: collision, movement, input, the state machine and its timings, existing tests and their
expectations, the A5 shaders and every other object. Presentation code reads game state and never writes it. -->

## Part D. Evidence split ✍
<!-- For each rule in A.4 and B.4: headless test, frame strip, or your eyes in the running game, and how. -->

## Part E. Frame strips ✍
<!-- Background of each preview (a real stretch of the slice). Effect A: trigger frame 10, then frames 12, 15, 20, 30
and 50 at 30 fps; say what each should show. Effect B: frames for starting, steady state and after the condition
ends. -->

## Part F. Predicted failures ✍
<!-- At least three, each with the check that would catch it. -->

## Part G. Price predictions and budget ✍
| Effect | Peak particle count | Predicted headless CPU price | Predicted GPU time | Budget, and which price it is compared on |
|---|---|---|---|---|
| A | | | | |
| B | | | | |

## Part H. Short answers ✍
1. Which node type does each effect use, and which features in this brief does it lack (class reference for 4.7)?
2. With `local_coords` as set, what does Effect A do if its parent moves after the event?
3. Under the retrigger rule, how many Effect A bursts can be alive at once, and what peak particle count does that give?
4. What will a headless run report as the cost of a GPU effect, and why? With vsync on, what would FPS read with the
   effect off and on?
5. What does Effect B show on the first frame after its scene loads, with preprocess and without it? While the tree is
   paused? While the node is hidden?
6. Which settings in this brief belong to emission, which to process, and which to draw?
