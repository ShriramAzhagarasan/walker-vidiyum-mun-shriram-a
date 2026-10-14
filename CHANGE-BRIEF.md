# Change brief: Vidiyum Mun asset slice (A2)

*Revision 1, 2026-10-06, committed before any generation. Drafted by Claude from CONCEPT, STORYBOARD and CHARACTER-SHEET. Approach (2.5D, Telltale-style) chosen by Shriram. Later changes go in dated revisions at the bottom; this text is not rewritten.*

**Started from:** an empty Godot 4.7.2 project. Code conventions and the headless test-harness pattern were borrowed from Shriram's Assignment 1 project (`walker-jumpman-shriram-a`, itself based on nikbearbrown/walker-jumpman). No art, levels or characters are reused.

## 1. Asset list
All art is cel-shaded on a flat background, with the background removed afterwards. Files go in `godot/assets/`.

| ID | Asset | File in the project | Storyboard panels |
|---|---|---|---|
| CHAR-HARI-REF | Hari reference turnaround (front, 3/4, side, back) | `design/character/gen/hari-ref.png` (not in game) | all; source for every pose |
| CHAR-HARI-IDLE | Hari standing | `assets/art/hari/idle.png` | 2, 3 |
| CHAR-HARI-WALK | Hari mid-stride | `assets/art/hari/walk.png` | 3 |
| CHAR-HARI-TALK | Hari gesturing in dialogue | `assets/art/hari/talk.png` | 3, 8 |
| CHAR-HARI-PHONE | Hari on the call | `assets/art/hari/phone.png` | 2, 7 |
| CHAR-HARI-NOTES | Hari looking down at phone notes | `assets/art/hari/notes.png` | 4 |
| CHAR-HARI-OVERHEAR | Hari listening, leaning back | `assets/art/hari/overhear.png` | 4 |
| CHAR-HARI-STARTLED | Hari waking at 8 PM, hand on damp shirt | `assets/art/hari/startled.png` | 7 |
| CHAR-HARI-KEYS | Hari showing the keys | `assets/art/hari/keys.png` | 8 |
| CHAR-HARI-WHITEOUT | Hari shielding his eyes from the glare | `assets/art/hari/whiteout.png` | 6 |
| CHAR-HARI-RELIEF | Hari, hands on head | `assets/art/hari/relief.png` | 9 |
| NPC-MANI-IDLE | Manikandan leaning on the SUV | `assets/art/npc/manikandan.png` | 3, 5, 8 |
| NPC-MANI-PHONE | Manikandan on the phone to Selvam | `assets/art/npc/manikandan_phone.png` | 4 |
| NPC-ADVAY | Advay with his Bluetooth speaker | `assets/art/npc/advay.png` | 5 |
| NPC-KRISHNA | Krishna on the deck (ambient) | `assets/art/npc/krishna.png` | 2 |
| ENV-MARBLE | Tileable Italian marble floor texture | `assets/art/env/marble.png` | 2, 3, 4, 8 |
| ENV-VILLA | White glass villa facade, warm interior (backdrop) | `assets/art/env/villa.png` | 1, 2 |
| ENV-BEACH | The view past the railing: sea, rock shrine, old fence, village boats (backdrop) | `assets/art/env/beach_backdrop.png` | 1, 6, 9 |
| ENV-FIRE | Bonfire and burning-nets glow overlay | `assets/art/env/fire_glow.png` | 1, 9 |
| ENV-SUV | Generic large dark SUV, no logos (billboard prop) | `assets/art/env/suv.png` | 3, 5, 8 |
| SFX-PHONE-BUZZ | Phone vibrating on the 8 PM call | `assets/audio/sfx/phone_buzz.ogg` | 2, 7 |
| SFX-CLUE | Soft clue chime (small bell) | `assets/audio/sfx/clue_saved.ogg` | 4, 5, 8 |
| SFX-KEYS | Car keys jingling as they change hands | `assets/audio/sfx/keys_exchanged.ogg` | 5, 8 |
| SFX-DAWN-CRASH | Distant highway horn swelling into a brake screech | `assets/audio/sfx/dawn_crash.ogg` | 6 |
| SFX-SAFE-DAWN | Gentle waves and crows at first light | `assets/audio/sfx/safe_dawn.ogg` | 9 |
| MUS-PARTY | Party electronic dance loop | `assets/audio/music/party_loop.ogg` | 1, 2, 3, 5, 7 |
| MUS-GAANA | Village gaana-style loop (hand percussion, harmonium) | `assets/audio/music/gaana_loop.ogg` | 1, 7 |

**Models** (local, free; full details in SOURCES.md):
- **FLUX.2 [klein] 4B** (Apache 2.0, via mflux on Apple Silicon): text-to-image for the reference and environments, and reference-image editing for poses.
- **Z-Image-Turbo** (Apache 2.0): a second model to compare against.
- **Stable Audio Open 1.0** (Stability AI Community License): sound effects.
- **MusicGen stereo-medium** (CC-BY-NC 4.0): music.
- **rembg** with isnet-anime / BiRefNet: background removal.

## 2. Event-to-sound map
Game logic emits each event. `SoundBank` only listens: sound never changes game state, and a missing or muted file changes nothing.

| Sound | Exact trigger in code | Times per slice run (loop 1 + loop 2) | How double triggers are prevented |
|---|---|---|---|
| SFX-PHONE-BUZZ | `loop_started` when the clock is set to 8:00 PM at the start of each loop | 2 | Emitted once by the loop reset; the reset is guarded by a per-loop `started` flag |
| SFX-CLUE | `clue_saved(id)` only when a knowledge flag goes from false to true | loop 1: 2 (Selvam call, keys taken); loop 2: 1 (keys kept) | It fires on the state change, not on the interaction, so re-talking or a known clue makes no sound |
| SFX-KEYS | `keys_exchanged` at 1:40 when Advay takes the keys (loop 1), or when Manikandan agrees to keep them (loop 2) | 2 | The 1:40 timeline event has a one-shot flag per loop. The dialogue choice is consumed on selection. Interact is edge-triggered and latched while dialogue is open, so held or mashed E can't repeat it. |
| SFX-DAWN-CRASH | `dawn_failure` at ~5:50 AM if `KEYS_SAFE` is false | 1 | One-shot flag per loop. Input is locked during the white-out. |
| SFX-SAFE-DAWN | `dawn_safe` at dawn if `KEYS_SAFE` is true | 1 | One-shot flag. The slice ends right after. |

`SoundBank.trigger_counts` counts every request (even when the file is missing or the bus is muted). The automated test asserts these exact numbers.

## 3. Music behaviour
| Moment | Party loop | Gaana loop |
|---|---|---|
| 8:00 PM, loop start | starts from the top, full on the deck | starts, quiet on the deck |
| Walking toward the railing (x > 20 m) | fades down | fades up (the fence, heard) |
| After 3:00 AM | thins gradually (volume ramps down toward −12 dB by dawn) | unchanged |
| **Pause** (Esc/P) | low-pass filter on the Music bus and −8 dB; restored on resume | same (same bus) |
| **Failure** (dawn crash) | 0.5 s fade to silence *before* the horn | same |
| **Success** (a clue or the keys kept) | no change; the chime plays over the music | no change |
| **Safe dawn / end of slice** | already thinned; fades to silence at dawn and stays stopped through the end card | fades to silence and stays stopped |
| Restart (R) | restarts at loop 1, 8:00 PM | restarts |

**Mute:** **M** toggles the Music bus, **N** toggles the SFX bus. Both show HUD indicators.
**Loop cutting:** generate 30–47 s, detect the beats, cut on a bar boundary at a zero crossing, apply a short equal-power crossfade, and check by listening to at least three repetitions plus an automated seam-discontinuity measurement.

## 4. Build plan (Godot)
Claude proposed this; Shriram approved the 2.5D approach (2026-10-06).
- **Logic layer** (no visuals; tested headless): `LoopState`/clock, knowledge flags, timeline events, dialogue data (`data/dialogue.json`), `SoundBank`, mute and pause.
- **Presentation layer:** `scenes/slice.tscn` (Node3D) with:
  - the marble deck (≈26 m along X), the pool, villa and beach backdrops, string lights (OmniLight3D), and a WorldEnvironment whose sky follows the clock;
  - Hari as a CharacterBody3D with a billboard `Sprite3D`, NPC billboards, and a Telltale-style follow camera with per-zone framing presets;
  - a HUD (clock, phone card, clue card, dialogue, mute indicators, pause, white-out, end card).
- **Controls:**
  - **WASD/arrows:** move.
  - **E/Space:** interact or advance.
  - **Hold T:** fast-forward the night.
  - **Esc/P:** pause. **M / N:** mute music / SFX.
  - **R:** restart after the end.
- **Tests:** `tests/test_sound_triggers.gd` (exact trigger counts over a scripted two-loop sequence, with rapid and held input, and with muted buses giving the same outcome) and `tests/test_loop_logic.gd`.

## 5. Predicted failure cases and how each gets checked
| # | Prediction | How it gets checked |
|---|---|---|
| F1 | **Pose drift:** poses derived from the reference change the face, the hair or (most likely) the **check pattern and colours** of the shirt. | A contact sheet of all poses beside CHAR-HARI-REF at in-game size (300 px); the consistency-rules checklist per pose; rejections logged. |
| F2 | **Hands and props break:** extra fingers, a melted phone, keys that aren't keys. | Judge at 300 px (detail invisible at game size is acceptable); regenerate or edit if the prop's purpose is lost. |
| F3 | **Billboards look wrong in 3D:** feet float or sink, sprites clip into the railing, an unshaded sprite glows too bright against the night lighting. | In-engine screenshots per zone; feet-at-y=0 check; apply a clock-driven modulate tint to sprites if they glow. |
| F4 | **Hari disappears against the background:** the white villa behind him or the dark sea past the railing. | Palette contrast table (≥ 3:1 for one large shirt value on each background); an automated contrast check on in-engine screenshots around Hari's bounding box. |
| F5 | **Similar silhouettes:** IDLE, PHONE and OVERHEAR are hard to tell apart at gate framing (208 px), as the silhouette test already shows. | Generation rules (elbow out for PHONE, lean-back and head turn for OVERHEAR); the HUD phone card as a twin; a muted playtest. |
| F6 | **A sound fires twice:** mashed or held E re-opens dialogue, a known clue chimes again, a timeline event refires after unpausing. | `test_sound_triggers.gd` asserts exact counts with 10 rapid presses and a held press; manual rapid-press playtest. |
| F7 | **The music loop clicks or jumps at the seam:** MusicGen tempo drift makes the bar boundary unclear. | Beat tracking plus a zero-crossing cut, then an automated seam check (sample-step and RMS jump at the seam). Listen to 3+ repetitions in Godot. |
| F8 | **The gaana sounds generic or not Chennai:** the music model has seen little of this genre. | Shriram listens and judges against the pillar *The night belongs to Chennai*. Rejections logged; fall back to percussion-only, or to one loop, with the limitation stated. |
| F9 | **Background removal damage:** it eats hair edges or the shirt check, or leaves a green fringe. | View each cutout on black and on white at 2×; fix with alpha-matting settings or a manual cleanup, and record the edit. |
| F10 | **Unreadable when muted:** without the horn, the dawn failure looks like a random white flash. | Muted playtest by Shriram; the headlight sweep, shake and caption must carry the meaning. |

---

## Revision 2 (2026-10-07, after generation and Shriram's playtest 1)
Driven by observations, not planned in revision 1:

| Change | Why (evidence) | Where |
|---|---|---|
| **Title screen + intro motion comic** (4 generated 16:9 stills: INTRO-1-ECR, INTRO-2-ROCK, INTRO-3-ARRIVAL from reference B, INTRO-4-DAWN; captions; Esc skips; cuts to 8 PM) | Shriram asked for an intro that explains the story before play. It also brings storyboard panel 1 (the title view) into the slice. | `godot/scenes/intro.gd`; `assets/art/intro/` |
| **Walk cycle** (walk_1 stride s302 · walk_2 passing = IDLE · walk_3 stride WALK-B s322 · walk_4 passing), advanced by distance travelled, with the step bob low on contact and high on passing | Playtest 1: "feels too fake… looks so static… he is just sliding". The generated WALK-PASS frames came back as strides, so IDLE serves as the passing frame. | `godot/scenes/hari.gd` |
| **Motion feel:** acceleration 9 m/s², deceleration 14 m/s², idle breathing, turn squash, blob shadows, anti-aliased sprite edges | Same playtest | `hari.gd`, `blob_shadow.gd`, `billboard_art.gd` |
| **Physics interpolation**; the camera follows the interpolated transform | Stutter: the camera read a 60 Hz position every render frame | `project.godot`, `camera_rig.gd` |
| **Environment fill:** a raised stucco plinth under the deck, sand down to the beach, a compound wall with a gate and warm lamps | Playtest screenshots showed the sky's flat ground colour past every deck edge | `godot/scenes/environment_fill.gd` |
| **PHONE image s302 → s301** | Shriram's screenshot showed two phones (a second one at the far ear) | `assets/art/hari/phone.png` |
| **Music −4 dB headroom** | The party loop peaks at 0 dBFS | `autoload/sound_bank.gd` |
| **SFX scheduler:** EDM DPM-Solver++ | Stable Audio Open's default sampler crashed and the first workaround produced silence | `tools/gen/gen_audio.py` |

**New predicted failure, F11:** the intro's generated stills may not match the in-game art (Hari's face drifts in INTRO-3; the villa doesn't match ENV-VILLA). Check: the stills side by side with the reference and the villa backdrop at full screen. Shriram judges.

---

# Change brief: Assignment 3, three Blender assets (A3)

*Revision 1, 2026-10-12, written after Shriram's "Learn the window" session and committed **before any asset is built**. Drafted by Claude from the A2 game's own numbers (`logic/hari_spec.gd`, `scenes/fallback_prop.gd`, `scenes/slice.tscn`). The asset choice is Shriram's: these are the three models the A2 README named as the A3 next step. Later changes go in dated revisions below; this text is not rewritten.*

**Tools:** Blender 5.2.2 LTS (the chapter used 5.1.2), Godot 4.7.2, MCP for Blender (`uvx mcp-for-blender`, version recorded when installed), macOS. Blender is Z-up, 1 unit = 1 m; Godot is Y-up, metres. The glTF exporter's **+Y Up** converts the axes, so nothing is rescaled.

**Shared rules for all three:**
- Each asset gets its own `.blend` and is built around **Blender's world origin**, with its base on the floor (Z = 0) there.
- Rotation and scale are **applied** before export (sidebar shows rotation 0,0,0 and scale 1,1,1).
- At most **6 basic shapes**, flat Principled BSDF colours, no textures, sculpting, rigging or animation.
- **Front faces +X** in both Blender and Godot, matching the game's existing SUV stand-in (headlights at +X in `fallback_prop.gd`).
- Size reference: **Hari is 1.75 m tall** (sprite) with a 1.70 m collision capsule, feet at y = 0.

## A3-1. The SUV (`suv`)
- **What it is:** the black SUV whose keys decide whether dawn ends in a crash: Manikandan leans on it, the headlights white out the screen. It replaces A2's flat SUV card and placeholder boxes.
- **Where:** the driveway beside the deck, at the existing `SUV` node in `slice.tscn`.
- **Size (W × D × H, m): 4.60 (length, X) × 1.90 (width, Y) × 1.85 (height, Z).** Why: the footprint matches the deck's existing SUV collider (4.6 × 1.9), so Hari can't walk through it, and the roof sits just above Hari's 1.75 m head, which is what a Fortuner-class SUV looks like beside a person.
- **Origin:** centre of the underside (the point between the four tyre contact patches), so the tyres sit on the floor when placed at y = 0.
- **Look (6 shapes):** chassis box, a narrower cabin box set back from the front, four short cylinder wheels (12 segments). Body `#2e2d38`, cabin glass `#7d93b8`, tyres `#15141a` (the A2 stand-in's colours, so it reads as the same car).
- **Budget: 250 triangles.** Two boxes (12 each) + four 12-segment cylinders (44 each) = 200, with 50 spare for one correction. A default 32-segment cylinder would cost 124 each and blow the budget.

## A3-2. The rock shrine (`rock_shrine`)
- **What it is:** the small roadside shrine on the rock that the fishermen have always prayed to, now behind the fence: the story's reason the fence is an injustice (intro panel 2).
- **Where:** on the beach past the railing, near the fence line (it is currently painted into `beach_backdrop.png`).
- **Size: 1.20 (X) × 1.00 (Y) × 1.50 (Z) m.** Why: a waist-to-chest-high shrine for someone kneeling, with its roof tip below Hari's 1.75 m head, so it reads as small and humble beside the villa.
- **Origin:** centre of the rock's underside, so it sits on the sand.
- **Look (5 shapes):** a flattened low-poly rock (icosphere, subdivisions 1), a whitewashed plinth box, a small saffron shrine box, a red cone roof (8 segments), a brass lamp cylinder (8 segments). Rock `#6f6a63`, plinth `#e8e2d4`, shrine `#d9822b`, roof `#b23a2a`, lamp `#c9a24a`.
- **Budget: 200 triangles.** Icosphere 80 + two boxes 24 + cone 14 + lamp cylinder 28 = 146. A default UV sphere (960 triangles) alone would be nearly double the course limit.

## A3-3. The fence segment (`fence_segment`)
- **What it is:** one panel of the illegal fence the rich family put across the public beach: the story's central injustice, and the visual line between the party and the village.
- **Where:** along the beach edge, repeated end to end.
- **Size: 2.40 (X) × 0.12 (Y) × 2.10 (Z) m.** Why: 2.10 m is taller than Hari (1.75 m), so it reads as a barrier he can't step over, and a 2.4 m panel tiles evenly.
- **Origin:** centre of the underside, so a row of panels is just `x = i × 2.40`.
- **Look (6 shapes):** two square posts, two horizontal rails, a red warning sign, and a thin wire along the top (6-segment cylinder). Posts and rails galvanised grey `#8a8f96`, sign `#c0392b`, wire `#3a3d42`.
- **Budget: 100 triangles.** Five boxes (60) + a 6-segment wire cylinder (20) = 80.

## A3 predicted failure cases and how each gets checked
| ID | Prediction | Check |
|---|---|---|
| A3-F1 | An asset arrives **lying on its side** (Z-up vs Y-up confusion, or +Y Up off) | The check script reports which axis is tallest and whether it is Godot's Y; I also look at it in the Godot scene |
| A3-F2 | **Wrong size by ×10 or ×100** (centimetre scene units, or unapplied scale) | Godot bounding box vs this brief, ±5 %; the Blender sidebar dimensions are recorded beside both |
| A3-F3 | **Origin in the middle**, so it floats half-sunk or hovers | Check: the mesh's lowest point is at y = 0 ± 1 cm, measured from the **mesh**, not a collider (the chapter's floor check passed on its own collider); then I place it on the floor and look |
| A3-F4 | **Scale not applied** in Blender, so the Godot node scale isn't 1, 1, 1 | Check: node scale = (1, 1, 1); Blender sidebar shows scale 1 after applying |
| A3-F5 | Claude builds **more detail than asked** (default 32-segment cylinders, a 960-triangle sphere, extra parts) | Triangle count per asset (Blender scene statistics and the Godot mesh) vs each budget; shape count ≤ 6 |
| A3-F6 | A **colour doesn't survive the export** (e.g. arrives white or grey) | Check: each surface's albedo vs the brief's hex, within a small tolerance; then I look under the scene light |
| A3-F7 | The SUV **faces backwards** (front at −X) | Check: the cabin's centre is behind the chassis centre (x < 0), as specified; I also look |
| A3-F8 | **The MCP server won't connect** | A 2-hour time box with every step and exact error logged in FRICTIONAL.md; then the script route (Blender with no window, `--python-exit-code 1`) |
