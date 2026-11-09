# Change brief: Assignment 6, two particle effects (A6)

*Revision 1, 2026-11-08, committed before the first build prompt.*
*Authorship: Parts A–H are Shriram's: the intent, every value, every rule, every prediction, the budget and the
short answers. Shriram wrote them with **ChatGPT's help** (disclosed in SOURCES.md) and pasted them in the chat on
2026-11-08. Claude placed them unchanged, except for seven edits Shriram dictated after Claude's engine check (A size
curve `max_value`, billboard mode, one sentence removed, the scuff's position; B positions, fixed seeds, `cull_mask`)
and the second trigger frame in Part E, which Shriram chose from options. Shriram chose the two effects and the
retrigger rule from options Claude laid out. Claude wrote §0 (project facts, each checked in the files or in the
engine) and the headings, and chose no value, rule, prediction or budget. Later changes go in dated revisions at the
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

## Part A — Sand Scuff on Footsteps

### A.1 — The job

**1. What does the scuff tell the player?**

I want a small sand-and-dust scuff whenever Hari takes a step across the deck. It should make his movement feel connected to the ground, instead of looking like he is sliding across the marble.

At night, the deck has dark areas and patches of warm light. The scuff should give a small visual confirmation of each footfall without becoming distracting or covering clues.

There is no footstep signal yet. The effect should use the walked-distance tracking in Hari's movement code, with a footfall every **0.38 seconds of walking**. The exact script and variable should come from §0.

### A.2 — How it should look

**2. Timing**

The first frame should show a small, visible patch of dust directly under Hari's foot.

During the first **0.20 seconds**, it should spread outward and slightly upward. After that, it should slow down and fade.

The visible puff should mostly disappear by about **0.75 seconds**, with the last tiny grains gone by **1.15 seconds**.

Since Hari takes another step every 0.38 seconds, there can be several small scuffs at once.

**3. Contrast**

At the dark gate end, I want the main dust puff to be a light sandy beige so it stands out against the dark marble.

Under the warm bulbs, that same beige might blend into the brighter floor. To help with that, I want a second layer of slightly darker brown grains.

I don't want an extremely bright or glowing effect. It should look like ordinary dust catching the light. I will check both locations in the running game before deciding if the colours need adjusting.

**4. Size**

The scuff should stay around Hari's ankles, not reach his knees.

Hari is 1.75 metres tall. I want the dust to rise roughly **0.10–0.18 metres** at most and spread about **0.35–0.45 metres** across the floor.

It should be noticeable when watching him walk but still small compared with his body.

**5. Change over its life**

The dust begins as a warm beige with moderate transparency.

As it spreads, it becomes a little lighter, grows softer, and loses opacity. I want the cloud to expand first, then shrink slightly as it disappears.

The darker grains should start more visible, travel outward, and fade before becoming distracting.

**6. Variation**

Every step should look a little different.

I want some randomness in speed, size, direction, rotation, and colour. The colour should only vary slightly between beige and light brown, not turn into noticeably different colours.

**7. Layers**

I want two emitters inside one scuff scene:

- **SoftDust:** Ten soft particles that form the main cloud. This makes the footstep readable at a glance.
- **FineGrit:** Five smaller, darker particles that scatter outward. These add detail and help the effect remain visible against brighter marble.

Both start on the same footfall. Together, they should look like one small scuff rather than two separate effects.

### A.3 — Planned particle settings

**Node type:** Two `CPUParticles3D` emitters under one `FootstepScuff` root.

I'm choosing CPU particles because the scuff is small and only needs basic movement, gravity, colour, and scale changes. The moth effect will use GPU particles and turbulence, making the two effects technically different.

#### Emission

| Setting | SoftDust | FineGrit |
|---|---|---|
| `amount` | 10 | 5 |
| `one_shot` | `true` | `true` |
| `explosiveness` | 1.0 | 1.0 |
| `lifetime` | 1.15 s | 1.15 s |
| `emitting` initially | `false` | `false` |
| `emission_shape` | Box | Box |
| `emission_box_extents` | (0.08, 0.01, 0.05) m | (0.06, 0.01, 0.04) m |

The emitters should be placed about 0.03 metres above the floor. The boxes keep the particles close to the footprint instead of making them appear from a single identical point.

#### Process

| Setting | SoftDust | FineGrit |
|---|---|---|
| `direction` | (0, 1, 0) | (0, 1, 0) |
| `spread` | 80° | 85° |
| `initial_velocity_min` | 0.25 m/s | 0.35 m/s |
| `initial_velocity_max` | 0.65 m/s | 0.80 m/s |
| `gravity` | (0, -0.9, 0) | (0, -1.8, 0) |
| `damping_min` | 1.5 | 1.0 |
| `damping_max` | 2.5 | 2.0 |
| `scale_amount_min` | 0.8 | 0.7 |
| `scale_amount_max` | 1.2 | 1.3 |
| `hue_variation_min` | -0.02 | -0.02 |
| `hue_variation_max` | 0.02 | 0.02 |
| Initial rotation | 0–360° | 0–360° |
| Angular velocity | -40 to 40°/s | -60 to 60°/s |

**SoftDust colour and alpha curve**

- 0% life: warm beige `#D9C5A4`, alpha 0.55
- 20%: lighter beige `#E2D1B5`, alpha 0.45
- 50%: pale sand `#E5D8C5`, alpha 0.18
- 70%: same colour, alpha 0
- 100%: alpha 0

**FineGrit colour and alpha curve**

- 0% life: brown `#806448`, alpha 0.85
- 30%: lighter brown `#A1835B`, alpha 0.65
- 65%: light tan `#B89A71`, alpha 0.15
- 100%: alpha 0

**Size curve**

- SoftDust: scale multiplier 0.6 at birth, 1.3 at 25% life, 1.0 at 50%, and 0.4 at the end. The SoftDust `scale_amount_curve` resource's `max_value` = 1.3, so the planned peak multiplier of 1.3 isn't clipped.
- FineGrit: 1.0 at birth, 0.9 at 50%, and 0.2 at the end.

The puff becomes larger quickly, while the grains gradually get smaller.

#### Draw

| Setting | SoftDust | FineGrit |
|---|---|---|
| Mesh | `QuadMesh` | `QuadMesh` |
| Quad size | 0.12 × 0.12 m | 0.035 × 0.035 m |
| Texture | Procedural soft circular gradient | Procedural circular gradient |
| Material | `StandardMaterial3D` | `StandardMaterial3D` |
| Transparency | Alpha | Alpha |
| Blend mode | Mix / normal | Mix / normal |
| Shading | Unshaded | Unshaded |
| Billboard | `BaseMaterial3D.BILLBOARD_PARTICLES` | `BaseMaterial3D.BILLBOARD_PARTICLES` |
| Use vertex colour as albedo | `true` | `true` |

The texture should be created procedurally, so I don't need an external image. Its centre should be opaque and its edge transparent.

I want normal alpha blending, not additive blending, because this is dust rather than sparks or magic.

#### Node settings

| Setting | Value |
|---|---|
| `local_coords` | `false` on both emitters |
| `preprocess` | 0.0 s |
| `speed_scale` | 1.0 |
| `visibility_aabb` | AABB((-0.6, -0.1, -0.6), (1.2, 0.6, 1.2)) |
| Process mode | Pausable |
| Retrigger | New `FootstepScuff` instance per footfall |
| Cleanup | Free each instance after its particles finish |

`local_coords` is false because I want the dust to remain at the spot where Hari's foot landed. It should not follow him across the deck.

The proposed AABB should be checked against the actual particle bounds in the running preview.

### A.4 — Observable rules

**8. When does it fire?**

The scuff should fire once for every actual footfall while Hari is walking.

It must not fire when the scene first loads, while he is standing still, while movement is blocked by dialogue, or when the game is paused.

The movement code should track actual distance walked and trigger the effect when that distance reaches the next footfall threshold. It should only read movement state and must not change Hari's movement timing.

Every scuff should appear at Hari's world position projected onto the deck floor, with the emitter 0.03 m above the surface. No foot-bone tracking is required.

**9. What happens when steps overlap?**

I want overlapping bursts rather than restarting or ignoring the previous one.

Each burst lasts 1.15 seconds, and steps happen every 0.38 seconds.

`ceil(1.15 / 0.38) = 4`

So there can be **up to four scuff instances alive at once**.

Each instance contains 10 dust particles and 5 grit particles, giving a maximum configured capacity of:

`4 × (10 + 5) = 60 particles`

This is the planned upper bound, not a measured rendered count.

**10. What happens if Hari's node is freed?**

The scuff should be created under a separate effects container in the active level, not as a child that depends on Hari staying alive.

If Hari's node is freed, an existing scuff should finish fading at the original footfall position. No new scuffs should be created.

If the entire level is unloaded, its effects container can be freed normally.

This keeps the presentation effect separate from the gameplay object's lifetime.

---

## Part B — Moths Around the String Lights

### B.1 — The job

**1. What do the moths tell the player?**

I want a few moths flying around the string lights on the deck at night. The purpose is to make the environment feel more alive, especially when Hari is walking around and trying to understand what happened before dawn.

The moths are not meant to warn the player or give any gameplay advantage. They are just a small environmental detail that makes the warm lights feel like they belong in a real outdoor setting.

**When they appear**

The moths should only appear when:

- The game phase is `NIGHT`.
- The game clock is before 5:00 AM, represented as minute `1740` on the extended overnight clock.
- The string-light area is visible and the level is active.

When the game reaches 5:00 AM or leaves the night phase, new moths should stop spawning and the remaining ones should fade away.

**Special feature**

I'm choosing both **turbulence and a weak attractor**.

Turbulence gives the moths irregular movement, so they don't fly in straight lines. The attractor gently pulls them toward the lights without making them stick to the bulbs.

Effect A doesn't use either feature. This is why I'm using `GPUParticles3D` with a `ParticleProcessMaterial` for Effect B.

### B.2 — How it should look

**1. Timing**

Unlike the footstep scuff, the moths should not appear as a sudden burst.

I want them to already be flying around the lights when the player enters the night scene. I'll use preprocessing so they are visible from the first rendered frame.

Each moth should live for around **2.4 seconds**, with a short fade-in at the beginning, irregular flying during most of its life, and a fade-out near the end.

New moths should keep appearing gradually, so the group looks continuous rather than disappearing and restarting.

**2. Contrast**

Against the near-black sky, the moths should be small pale cream shapes. They need to be visible, but not so bright that they look like glowing sparks.

Near the warm bulbs, the moths should be a little darker than the light itself. I want their small wing shapes to remain visible instead of becoming white dots that blend into the bulbs.

The main colours should be cream, light beige and a slightly darker brown in the centre.

**3. Size**

Hari is 1.75 metres tall, so the moths need to be tiny compared with him.

I want each moth to have a visible wingspan of around **0.05–0.08 metres**.

They should stay within roughly one metre of their bulbs. They should look like small insects flying around lights, not large butterflies.

**4. Change over life**

A moth should start small and transparent, become visible quickly, and keep roughly the same size while flying.

During the last part of its life, it should become more transparent and slightly smaller before disappearing.

Its colour should stay mostly pale cream. I don't want big colour changes because that would make it look like a magical particle effect instead of a moth.

**5. Variation**

Each moth should move differently.

I want random starting positions, small differences in speed and size, slightly different cream and beige colours, and different rotations.

The turbulence should make them change direction naturally. Some moths should move close to the bulb, while others drift a little farther away.

I don't want all of them following the same circular path.

**6. Layers and emitters**

I want three emitters, with one group of moths near each string-light section.

Each emitter has the same general settings, but a different random seed so the three groups don't move identically.

I don't want extra glowing particles or sparkles. The moth sprite itself should include two small wings and a darker body.

This keeps the effect simple and prevents it from becoming too distracting.

### B.3 — Planned particle settings

**Node type:** `GPUParticles3D`, using a `ParticleProcessMaterial`.

There will be three GPU particle emitters inside one `StringLightMoths` root. Each emitter gets a nearby `GPUParticlesAttractorSphere3D`.

The intended emitter positions are based on the three gaps between the string-light supports:

| Emitter | Planned world position |
|---|---|
| `MothsWest` | (8.0, 2.85, -3.4) |
| `MothsMiddle` | (12.0, 2.85, -3.4) |
| `MothsEast` | (16.0, 2.85, -3.4) |

These positions should be checked against the actual bulb positions recorded in §0 before building.

#### Emission settings

| Setting | Value per emitter |
|---|---|
| `amount` | 12 |
| `amount_ratio` | 1.0 |
| `one_shot` | `false` |
| `explosiveness` | 0.0 |
| `randomness` | 0.4 |
| `lifetime` | 2.4 seconds |
| `emission_shape` | `EMISSION_SHAPE_BOX` |
| `emission_box_extents` | Vector3(0.65, 0.30, 0.40) |
| `preprocess` | 2.4 seconds |
| `fixed_fps` | 30 |
| `speed_scale` | 1.0 |
| `use_fixed_seed` | `false` in the actual effect scene. Only the preview copies use `true` |
| Seeds | 101, 202 and 303 (preview copies only) |

The emission box allows moths to start around the light instead of all appearing from one point.

Preprocessing should fill the scene with moths before the first visible frame. This is a prediction that needs to be confirmed using the preview capture.

#### Process settings

| Setting | Value |
|---|---|
| `direction` | Vector3(0, 1, 0) |
| `spread` | 85° |
| `initial_velocity_min` | 0.06 m/s |
| `initial_velocity_max` | 0.28 m/s |
| `gravity` | Vector3(0, 0, 0) |
| `damping_min` | 0.12 |
| `damping_max` | 0.35 |
| `scale_min` | 0.7 |
| `scale_max` | 1.2 |
| `angle_min` | -35° |
| `angle_max` | 35° |
| `angular_velocity_min` | -110°/s |
| `angular_velocity_max` | 110°/s |
| `hue_variation_min` | -0.03 |
| `hue_variation_max` | 0.03 |
| `attractor_interaction_enabled` | `true` |

The zero gravity lets them float in different directions. The attractor and turbulence should produce their wandering movement instead of gravity pulling them down.

**Scale curve (`scale_curve`)**

| Life progress | Scale multiplier |
|---|---|
| 0% | 0.7 |
| 15% | 1.0 |
| 75% | 1.0 |
| 100% | 0.6 |

**Colour and alpha ramp (`color_ramp`)**

| Life progress | Colour | Alpha |
|---|---|---|
| 0% | `#D8CAB0` | 0.0 |
| 15% | `#E9DFC9` | 0.8 |
| 70% | `#EFE6D2` | 0.7 |
| 100% | `#D8CAB0` | 0.0 |

The moths should fade into view, stay visible for most of their life, and disappear smoothly.

#### Turbulence settings

| Setting | Value |
|---|---|
| `turbulence_enabled` | `true` |
| `turbulence_noise_strength` | 0.45 |
| `turbulence_noise_scale` | 5.0 |
| `turbulence_noise_speed` | Vector3(0.15, 0.08, 0.12) |
| `turbulence_noise_speed_random` | 0.2 |
| `turbulence_influence_min` | 0.12 |
| `turbulence_influence_max` | 0.30 |
| `turbulence_initial_displacement_min` | 0.0 |
| `turbulence_initial_displacement_max` | 0.06 |

I want gentle but noticeable direction changes. If the turbulence makes them shake too quickly or fly too far from the bulbs, I will reduce its strength during tuning.

#### Attractor settings

Each moth emitter gets one `GPUParticlesAttractorSphere3D` near its bulb.

| Setting | Value |
|---|---|
| Position | Same X/Z as its emitter, Y = 2.85 |
| `radius` | 1.0 m |
| `strength` | 0.30 |
| `attenuation` | 1.0 |
| `directionality` | 0.0 |
| `cull_mask` | 4294967295 (all layers). This is the Godot 4.7 default, and the attractor won't affect Effect A's CPU particles |

The positive strength should gently pull moths toward the light. The turbulence should prevent them from moving directly into the centre and staying there.

The particle material must have attractor interaction enabled, and the visibility bounds must include the region in which attraction occurs.

#### Draw settings

| Setting | Value |
|---|---|
| Mesh | `QuadMesh` |
| Base quad size | 0.07 × 0.045 m |
| Texture | Procedurally generated moth silhouette |
| Main colour | Pale beige |
| Body colour | Muted dark brown |
| Material | `StandardMaterial3D` |
| Transparency | Alpha |
| Blend mode | Normal / Mix |
| Shading | Unshaded |
| Billboard mode | Particle billboard |
| `vertex_color_use_as_albedo` | `true` |

The moth texture should have two simple wings and a small darker centre. It can be generated with a short GDScript and committed with its source, so no external artwork is required.

I want the wings to be recognizable in the preview but not overly detailed. The moths should look like tiny moving shapes, not bright glowing squares.

#### Node settings

| Setting | Value |
|---|---|
| `local_coords` | `false` |
| `preprocess` | 2.4 seconds |
| `visibility_aabb` | AABB((-1.5, -1.1, -1.5), (3.0, 2.2, 3.0)) |
| `process_mode` | Pausable |
| `emitting` | Controlled by the night condition |
| `visible` | Controlled by the active/hidden state |
| `one_shot` | `false` |
| `speed_scale` | 1.0 |
| `trail_enabled` | `false` |

`local_coords` is false because the moths should fly in world space around the lights. They should not suddenly shift position if their emitter node moves.

The AABB is a planned starting value. It needs to be checked using the actual rendered motion so particles aren't unexpectedly culled.

### B.4 — Observable rules

**1. When does the effect start?**

When the scene is active, the game is in `NIGHT`, and the extended clock is before minute 1740, all three emitters should be active.

If the scene loads during that condition, the moths should already appear populated on the first rendered frame because of preprocessing.

The exact clock variable must come from §0. The particle controller may read the game state but must not change it.

**2. When does the effect stop?**

At 5:00 AM or whenever the phase stops being `NIGHT`, all three emitters should set `emitting = false`.

Existing moths may finish fading over their remaining lifetime of up to 2.4 seconds. After that, the group should be hidden.

I prefer this over making every moth disappear instantly, because a short fade feels more natural.

**3. What happens when the game is paused?**

The moths should freeze in place when the game is paused.

They should not continue flying or spawning while the clock and player are paused.

The particle nodes should use pausable processing and resume from the same state when the game continues.

**4. What happens when the area is hidden?**

If the moth group or its area is intentionally hidden, all three emitters should become invisible and stop emitting.

When the area becomes visible again, the controller checks the night condition.

If the condition is still active, the emitters should restart with preprocessing so the player sees a populated group rather than waiting for new moths to appear.

If the condition is no longer active, they stay hidden.

**5. What happens on the first frame after loading?**

If the scene loads at night before 5:00 AM, I expect the moths to already be visible around the bulbs.

If the scene loads during daytime or after the cutoff, there should be no moths, not even for one frame.

The controller should initialize visibility and emission from the current game state before the scene's first rendered frame.

**6. How many moths can exist?**

Each emitter has an `amount` of 12, with three emitters.

Maximum configured particle capacity:

`3 × 12 = 36 moths`

This should be enough to make the string lights feel alive without filling the entire screen.

The real visible count may be lower because individual particles fade in and out. The GPU performance impact will be measured separately.

### Expected result

I want the final effect to feel subtle. When Hari walks near the string lights, there should be a few pale moths drifting irregularly around the bulbs. Some should move closer to the light while others wander a little farther away.

From a distance, the player should mainly notice that something small is moving around the lights. The moths should add atmosphere without distracting from the story, dialogue, or objects the player needs to inspect.

---

## C. Boundaries

The particle effects are only visual additions to Vidiyum Mun.

- Do not change Hari's movement, the 0.38-second walking step interval, collision, or input.
- Do not change the clock, night phases, dialogue, story logic, or existing test expectations.
- Do not edit any Assignment 5 shaders or their materials.
- Particle controllers may read the current game state but must never change it.
- Keep particle scenes and test code separate from existing gameplay logic.

## D. Evidence split

| Rule | How I will check it |
|---|---|
| A fires on every actual footfall | Headless state test using real movement |
| A does not fire on load, standing still, dialogue, or pause | Headless state test |
| A appears at Hari's floor position | Headless position assertion, then visual check |
| A allows overlapping bursts | Headless test with two steps within one lifetime |
| A survives Hari being freed | Headless lifetime/cleanup test |
| A has the planned emission, process, and draw settings | Configuration read-back test |
| A looks like ankle-high dust in dark and bright areas | Frame strips and my in-game check |
| B activates only during NIGHT before minute 1740 | Headless state test |
| B stops emitting when the condition ends | Headless state test |
| B freezes while paused | State test and visual check |
| B handles hiding and showing correctly | State test and frame strip |
| B is populated on its first active frame | Movie Maker frame strip |
| B stays near the bulbs without becoming distracting | Frame strip and in-game check |
| B has the planned turbulence, attractor, and draw settings | Configuration read-back test |

A headless test can verify node configuration and gameplay conditions, but it cannot prove that the particles actually look correct.

## E. Frame-strip predictions

All frame predictions below assume a 30 FPS Movie Maker capture.

### Effect A — Sand scuff

Use the real deck background near the dark gate, then repeat the preview under the warm string lights.

The preview triggers one footstep at frame 10.

*(Added 2026-11-08 before commit, Shriram's choice:)* With the preview's retrigger export on, a second footstep
triggers at **frame 21**, 11 frames (0.37 s, one real step) after the first, while the first scuff is still alive.

| Frame | Predicted appearance |
|---|---|
| 10 | A small beige puff and a few darker grains appear at ground level |
| 12 | Dust begins spreading outward while remaining clearly visible |
| 15 | Main puff is wider, with fine grit moving slightly farther out |
| 20 | Dust has spread and started fading; the grains are becoming less visible |
| 30 | Only faint remaining particles should be visible |
| 50 | The entire scuff should be gone |

The effect should remain small compared with Hari and not rise above his ankles.

### Effect B — Moths

Use the real string-light background, including the dark sky and warm bulbs.

For the preview, begin in the active night condition with preprocessing enabled, then switch to the inactive condition at frame 70.

| Frame | Predicted appearance |
|---|---|
| 10 | Moths are already visible around the bulbs because of preprocessing |
| 30 | Several moths are flying irregularly, with different positions and rotations |
| 70 | The night condition ends; new particles stop being emitted |
| 85 | Some existing moths may still be fading away |
| 145 | All moths should be gone |

A second preview should start outside the night condition and confirm that no moths appear on frame one.

## F. Predicted failures

| Predicted problem | Check that should catch it |
|---|---|
| A's scale curve clips the planned 1.3 peak | Configuration test checks the Curve's maximum; frame strip checks size |
| A's particles follow Hari instead of remaining where he stepped | Headless check of `local_coords`, followed by a moving-camera visual check |
| A's particles appear as flat squares or fail to rotate properly | Draw-material read-back and frame strip |
| B's moths appear too far in front of the bulbs | Position read-back and real-scene frame strip |
| B's visibility AABB cuts off drifting moths | Frame-strip comparison at the edge of their movement |
| B's colour or alpha ramp is invisible because vertex colour is not used | Material read-back and visual inspection |
| B appears during daytime or on the wrong first frame | State test and first-frame capture |
| A Godot 3 property name silently leaves a setting at its default | Configuration test with a deliberate invalid-name mutation |

I will keep these as predictions until the tests and real captures confirm or reject them.

## G. Performance prices and budgets

These are **predicted prices before implementation**, not measured results.

| Metric | Effect A: Sand scuff | Effect B: Moths |
|---|---|---|
| Particle node | `CPUParticles3D` | `GPUParticles3D` |
| Emitters | 2 per burst | 3 continuous |
| Peak instances | 4 bursts | 3 emitters |
| Peak configured particles | 60 | 36 |
| Predicted extra headless CPU time | 0.04 ms/frame | 0.005 ms/frame |
| Predicted extra GPU time | 0.03 ms/frame | 0.06 ms/frame |
| Headless CPU budget | ≤0.15 ms/frame | Not the primary budget |
| GPU budget | ≤0.20 ms/frame | ≤0.20 ms/frame |

For A, I will compare the measured headless CPU time against the empty-scene control and the 0.15 ms budget. I will also measure its GPU cost.

For B, the important measurement is GPU time from Godot's Visual Profiler, compared with the 0.20 ms budget. Its headless CPU cost can be close to zero because headless Godot does not actually render or simulate GPU particles in the same way as a real GPU run.

Both effects will be measured with the effects enabled and disabled under otherwise identical conditions. I will record the actual numbers even if they exceed these predictions.

## H. Six technical answers

### 1. Which node types did I choose, and what features do they lack?

I chose `CPUParticles3D` for the sand scuff because it only needs basic movement, gravity, fading, and scaling.

For the moths, I chose `GPUParticles3D` because I want turbulence and attractor interaction. These are features my CPU particle effect doesn't support.

### 2. What happens when the parent moves?

Both effects have `local_coords = false`.

This means particles that have already spawned remain in world space instead of moving with their emitter. The scuff stays where Hari stepped, and the moths continue moving around their spawn area even if the emitter node moves.

### 3. How many bursts can overlap, and what is the peak count?

The scuff lifetime is 1.15 seconds, and Hari takes a step every 0.38 seconds.

`ceil(1.15 / 0.38) = 4`

So up to four bursts can overlap.

Each burst has 15 particles, giving a peak configured capacity of 60 particles.

For the moths, three emitters with 12 particles each give a capacity of 36.

### 4. What does a GPU effect cost in a headless test, and what does FPS show with vsync enabled?

A GPU effect can show almost no extra headless CPU cost because the headless test does not draw and process its GPU particles on a real graphics card.

With vsync enabled, FPS often remains at the monitor's refresh rate until the workload causes frames to miss their deadlines. This can hide small performance differences.

That is why I need the Visual Profiler's GPU time, not just FPS.

### 5. What should B show on its first frame, while paused, and while hidden?

With 2.4 seconds of preprocessing, the moths should already be spread around the bulbs on the first active rendered frame.

Without preprocessing, the scene begins with few or no moths, and they gradually appear as the emitter runs.

When the game is paused, the moths should freeze. When the area is hidden, emission stops and the effect isn't displayed. If the area becomes visible while the night condition is still active, the effect should restart and populate again.

### 6. Which settings belong to emission, process, and draw?

**Emission** determines when and where particles appear. It includes `amount`, `one_shot`, `lifetime`, `explosiveness`, and emission shape.

**Process** determines how particles move and change. It includes velocity, gravity, damping, spread, turbulence, scale curves, and colour ramps.

**Draw** determines what the particles look like. It includes the quad mesh, texture, transparency, blend mode, and billboard material.

Separating these helped me understand that a particle effect can trigger correctly while still looking wrong because of its process or draw configuration.

---

## Revision 2, 2026-11-08 (Effect A tuning r1, kept by Shriram; the text above is unchanged)
- **§A.3 SoftDust colour and alpha curve:** alpha at 50 % life 0.18 → **0.30**, at 70 % life 0 → **0.15** (colours and
  offsets unchanged; 100 % stays 0). So the "visible puff should mostly disappear by about 0.75 seconds" in §A.2 now
  reads "by about 1.0 s". Reason: Shriram's verdict in play, "the timing was way too fast". Record: TUNING.md, Effect A
  r1. The lifetime (1.15 s), the overlap rule (at most 4 alive) and the 60-particle peak are unchanged.

## Revision 3, 2026-11-08 (tuning, approved by Shriram; the text above is unchanged)
- **§A.3 Draw, SoftDust texture** (Effect A r2, kept): the procedural soft circular gradient is alpha 0.85 at the centre,
  0.30 at 45 % of the radius and 0 at the edge (was 1.0 out to 60 %, 0.4, 0). Reason: Shriram saw "cotton balls" in play.
- **§B.3 Draw, base quad size** (Effect B r1): 0.07 × 0.045 m → **0.21 × 0.135 m**. Reason: at the real camera distance
  the moths were 1–3 px specks Shriram could not see. Verdict pending at the time of this revision (TUNING.md, Effect B).
- **§A.4 #8 position:** the scuff lands at Hari's centre, which reads as behind the front foot while walking; Shriram
  kept this and records it as a known limitation.

## Revision 4, 2026-11-08 (Effect B tuning, approved by Shriram; the text above is unchanged)
- **§B.3 colour and alpha ramp** (r2): colours dark umber #3B2F25 (0 %, 100 %) and #4A3B2E (15 %, 70 %); alphas
  unchanged. §B.2's "pale cream shapes" no longer holds: the bulbs hang in front of the pale villa wall and lit windows,
  not the dark sky.
- **§B.3 draw, texture** (r3): the procedurally generated moth silhouette has solid wings and body with a narrow soft
  edge (at least 700 of 2560 texels above 0.8 alpha). The r1 quad size (0.21 × 0.135 m, revision 3) stays.
- Shriram's verdict on r3: "it reads as moths". Record: TUNING.md, Effect B r1–r3.
