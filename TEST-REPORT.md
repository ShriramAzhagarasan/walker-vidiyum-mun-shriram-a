# Test report: Vidiyum Mun asset slice

- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf · **OS:** macOS 26.6.2 (MacBook Pro M1 Pro, 16 GB) · **Renderer:** Forward+ (Metal)
- **Source revision tested (frozen for the film):** `13f772c` (main, 2026-10-07 ~17:00 EDT), refrozen after the R11 mix fix. A fresh clone of the earlier freeze `e227f23` imported with 0 errors and passed every check; the fresh-clone check is repeated on the final commit.
- **Labels:** **[AUTO]** = automated or scripted, run by Claude. **[HUMAN]** = played or listened to by Shriram, quoted in his words. **[SCRIPTED CAPTURE]** = screenshots made by `godot/tools/capture_shots.gd`, which sets the clock and position through the test API. They are not hand-played.

## 1. Startup and controls
| Check | Result |
|---|---|
| [AUTO] Fresh clone of `e227f23` from GitHub into an empty folder, then `godot --headless --path godot --import` | Exit 0, **0 error lines** |
| [AUTO] All 4 test scripts in that fresh clone | 86/86, 36/36, 13/13, 70/70 PASS (section 2) |
| [AUTO] `tools/check/loop_seam_check.py` in that fresh clone | PASS |
| [HUMAN] Ran the real game (`godot --path godot`): title → intro → slice; walking, talking, loop 2 | Shriram played the slice three times (playtests 1–3, section 8) and moved, talked and reached loop 2 with the intended keys. Playtest 1 turned out to be in a film-capture window (section 8, R6). |

## 2. Automated checks
| Check | Command | Result at `e227f23` |
|---|---|---|
| **Sound triggers**: exact count per event over a scripted two-loop run through the real input path, including 10 rapid E presses, a held E (40 echo events) and mashing during the crash. The run is repeated with both buses muted and must reach the same outcome. Also checks Hari's 10 states and their durations. | `godot --headless --path godot -s res://tests/test_sound_triggers.gd` | **86 checks, 0 failed.** phone_buzz 2 · clue_saved 3 · keys_exchanged 2 · dawn_crash 1 · safe_dawn 1, identical when muted |
| **Loop logic**: knowledge persists across the reset, per-loop flags reset, keys-safe prevents the crash, the choice needs both clues, dialogue ids present, **the loop-2 call differs from loop 1's** | `… -s res://tests/test_loop_logic.gd` | **36 checks, 0 failed** |
| **3D scene smoke test**: scene builds, movement locked during the call, walk speed, Hari's size and collision numbers | `… -s res://tests/test_slice_smoke.gd` | **13 checks, 0 failed** |
| **Asset presence**: all 10 Hari states, 4 NPC images, 5 environment textures, 5 SFX (per-sound length limits) and 2 music loops load from the submitted copy. Sprites have alpha, a transparent corner, and feet within 12 px of the bottom edge. | `… -s res://tests/test_assets_present.gd` | **70 checks, 0 failed** |
| **Music loop seams**: 3 repetitions; the sample step at each seam vs the in-loop 99.9th percentile, and RMS change < 6 dB | `python tools/check/loop_seam_check.py` | **PASS.** gaana 0.0094 vs 0.0926 (0.24 dB) · party 0.0401 vs 0.4224 (1.86 dB) |

**What these checks don't prove:**
- **The sound test** counts *requests* to SoundBank. It proves each event fires once, not that the right file is audible at a good level.
- **The seam check** proves there's no sample discontinuity, not that the loop is musically seamless (phrase, groove).
- **The asset test** proves the files exist, load and have the right shape, not that they look right.
- **The test API jumps the clock**, so these checks can't catch pacing or feel.

All of those need human eyes and ears (sections 5–8).

**Test changes, recorded so they aren't hidden:**
1. `test_assets_present`'s first version had a blanket 4 s SFX limit. That contradicted the design: the dawn crash is 5 s and the safe dawn is an 8 s bed. It now uses per-sound limits taken from CHANGE-BRIEF.
2. `test_loop_logic`'s loop-2 assertions changed because **Shriram changed the design** (loop 2 must react to the repeat). The new assertion is stricter: the loop-2 call must differ from loop 1's.
3. The same suite first failed when Hari's new thought line D9d used the NOTES pose. The test reserves NOTES for "a clue was saved", so the line was changed to IDLE. The test caught a real ambiguity in the visual language.

## 3. Character against the sheet
- **Evidence:**
  - `design/character/gen/poses-generated.jpg`: the generated states at one scale with the capsule over each.
  - `evidence/shots/state_<state>_{right,left}.jpg` [SCRIPTED CAPTURE]: each state in engine, facing right and flipped left.
  - `design/character/poses-spec.png`: the spec.

**Side by side (spec | generated image | in engine facing right | facing left):** ![sheet vs engine](evidence/comparisons/character-sheet-vs-engine.jpg)

| State | Spec pose | In engine (right / left) | Mismatch with the sheet or collision |
|---|---|---|---|
| IDLE | 1 | state_idle_right / _left | none |
| WALK | 2 | state_walk_right / _left; in play a 4-frame cycle | stride reaches past the capsule (fair: no hazards) |
| TALK | 3 | state_talk_* | the gesturing hand is outside the capsule |
| PHONE | 4 | state_phone_* | none (s301; s302's two phones were rejected) |
| NOTES | 5 | state_notes_* | none |
| OVERHEAR | 6 | state_overhear_* | **silhouette close to IDLE (F5 not fully solved)** |
| STARTLED | 7 | state_startled_* | flung arm is outside the capsule (shown ~1.2 s while locked) |
| KEYS | 8 | state_keys_* | the raised arm is above the capsule |
| WHITEOUT | 9 | state_whiteout_* | none |
| RELIEF | 10 | state_relief_* | elbows outside the capsule (end pose, no movement) |

**Orientation:** all art faces right; facing left is `flip_h` at runtime, driven by the screen-space direction of movement.

## 4. Storyboard against the slice
In-engine screenshots are [SCRIPTED CAPTURE] in `evidence/shots/`. The game's camera is a Telltale-style eye-level follow camera. **The special angles drawn in the storyboard (bird's-eye, over-the-shoulder, low, Dutch, close-up high) are not reproduced by the in-game camera.** Where a panel depends on one, the meaning is carried another way, as listed below.

**Side by side (storyboard panel | in-engine screenshot at `13f772c`):** ![storyboard vs slice](evidence/comparisons/storyboard-vs-slice.jpg)

| Panel | Slice evidence | Matches | Differences, and why |
|---|---|---|---|
| 1 Title, bird's-eye | `intro_title.jpg`, `intro_panel_1.jpg` | The villa, fence, village fire and ECR in one establishing frame, with the title. | A **design view**, made as a generated still with a slow zoom in the intro, not the 3D scene. |
| 2 8 PM Amma's call | `p02_amma_call.jpg` | PHONE pose, phone card, 8:00 PM clock, villa and string lights, dialogue | none significant |
| 3 Talk to Manikandan | `p03_gate_walk.jpg`, `p03_talk_manikandan.jpg` | WALK → TALK, Manikandan at the SUV, "E — Talk", gate framing | Not over-the-shoulder; the follow camera frames the SUV from the front-right. |
| 4 Clue saved | `p04_overhear.jpg`, `p04_clue_saved.jpg` | OVERHEAR during the call, then NOTES with the notes card | No close-up high-angle phone shot. The **HUD notes card** is the close-up. |
| 5 1:40 keys taken | `p05_keys_taken.jpg` | Advay with the speaker, caption, keys icon arcs to him | Not a low angle. Advay's line is a timed caption, not modal. |
| 6 Dawn failure | `p06_dawn_crash.jpg`, `p06_whiteout.jpg` | Music cut, horn, headlight sweep, shake, WHITEOUT pose, white-out | No Dutch tilt (shake instead). |
| 7 Loop 2 wake | `p07_loop2_wake.jpg` | STARTLED, damp shirt, "loop 2", D8 thoughts, the call again | No camera push-in. Revision 2 dialogue adds Hari's shock lines. |
| 8 Keys stay | `p08_choice.jpg`, `p08_keys_stay.jpg` | "Ask about Selvam" (only with both clues), KEYS pose, keys icon to Manikandan | none significant |
| 9 Safe dawn and end card | `p09_safe_dawn.jpg`, `p09_end_card.jpg` | RELIEF at the railing, dawn, beach and rock backdrop, end card in English and Tamil | Not a low angle from the sand; the railing camera looks out to sea instead. |

## 5. Sound events
| Check | Result |
|---|---|
| [AUTO] One request per occurrence, including rapid and held input (section 2) | PASS |
| [AUTO] 6 s Movie Maker capture of the real game: audio present | Mean −13.3 dB, music audible (before the −4 dB headroom change) |
| [HUMAN] Playtest 4 (Shriram, verbatim): "muting mutes the sound but pressing n does nothing to the sfx and i cant hear anything" | **FAIL → fixed (R11).** The SFX (RMS about −20 dBFS) were masked by the music (party RMS about −19 dBFS after −4 dB). |
| [AUTO] After R11: Movie Maker capture of the real game at the 8 PM loop start | Phone-buzz window (0–2.4 s) **−15.0 dB** vs music-only (4–8.5 s) **−25.2 dB**: the buzz is **+10.2 dB** above the music |
| [HUMAN] Playtest 5 after R11 (Shriram): "yes it works, all's good now" | **PASS**: each sound heard in real play; N mutes the effects |
| [AUTO] `test_audio_mix.gd`: music headroom ≤ −8 dB, ducking engages on an SFX and not when SFX is muted, N toggles SFX, M toggles Music, a muted SFX is still counted | **10 checks, 0 failed** |

## 6. Music
| Check | Result |
|---|---|
| [AUTO] Seam check, 3 repetitions | PASS (section 2) |
| [AUTO] Pause (low-pass and −8 dB), stop at dawn, restart at 8 PM, stopped at the end card | Implemented in `sound_bank.gd`; the stop and restart are exercised by `test_sound_triggers` (music_playing flag) |
| [HUMAN] Shriram heard the music in the real game ("muting mutes the sound") and approved the audio picks ("yes everything is okay") | Approved. A dedicated gaana-authenticity verdict (F8) wasn't given separately. |

## 7. Muted play
| Check | Result |
|---|---|
| [AUTO] Both buses muted → identical game outcome and event counts | PASS (section 2) |
| [HUMAN] Shriram, playtest 4: "muting mutes the sound" (M); his overall verdict "yes everything is okay" answered the muted-readability question as well | M confirmed. N was inaudible before R11 (the effects were masked). **Playtest 5 re-check after R11 (Shriram, verbatim): "yes it works, all's good now"**: SFX audible, N/M work, muted play OK |

## 8. Inspect-and-revise cycles
| # | Observation (evidence) | Change | Result |
|---|---|---|---|
| R1 | In-engine screenshots: the night read as lavender dusk; the white marble washed out (`evidence/revisions/R1-lighting-before.jpg`) | Night ambient `1b1a3c` → `100f26`, moonlight 0.25 → 0.08, string lights 1.6 → 2.8 | Warm light pools; the sky reads as night (`R1-lighting-after.jpg`) |
| R2 | Generated OVERHEAR came back as a hand at the ear, the same silhouette as PHONE (F5) | Prompt revised (head over the shoulder, hands down, no phone) | No longer PHONE, but now close to IDLE (limitation) |
| R3 | Generated WHITEOUT had a painted sun-flare | Prompt revised ("no light effects, no lens flare") | Clean |
| R4 | Screenshot p05: Advay hidden behind Manikandan; playtest 2: Advay walking through Hari | `ADVAY_AT_CAR` beside Manikandan; deck target moved to the far side | Fixed |
| R5 | Capture: the white-out stuck after a fast reset | `whiteout.gd` kills the running crash tween on reset | Fixed |
| R6 | **Shriram, playtest 1:** "the motion… feels too fake… looks so static… no lag… i don't hear any music" | Motion: a walk cycle by distance, accel/decel, step bob, breathing, turn squash, blob shadows, physics interpolation. Music: a Movie Maker capture showed music present. The film's capture log showed **playtest 1 happened in a capture window** (22 % speed, audio routed to the file). | Capture windows are now no_focus and fail the take on any foreign input. Motion improved (playtests 2–3). |
| R7 | Stable Audio Open output was **silent** (all-NaN) after a sampler workaround; caught by a level check | EDM DPM-Solver++ scheduler | Audible SFX |
| R8 | **Shriram's playtest screenshot:** Hari holding two phones (PHONE s302) | Swapped to s301 | Fixed |
| R9 | **Shriram, playtest 2:** "in loop 2 the dialogues seem repeated, since he's in shock…" | Loop-2 lines D8–D9d, K2–K3; a test asserts loop 2 ≠ loop 1 | Fixed |
| R11 | **Shriram, playtest 4:** "pressing n does nothing to the sfx and i cant hear anything". Measured: SFX RMS ≈ −20 dBFS vs music ≈ −19 dBFS, so the effects were masked | SFX loudness-normalised to −14…−17 dBFS RMS with a tanh soft limit at −1 dBFS; music −4 → −10 dB; music ducks −9 dB (60 ms attack, 0.7 s release) while an audible SFX plays; new `test_audio_mix.gd` | Buzz +10.2 dB over the music in an engine capture; 10/10 mix checks |
| R10 | **Shriram, playtests 2–3:** backgrounds "not sitting right… slapped on"; the painted pool and railing in the backdrops duplicated the 3D ones; the gate camera sat 5.8 m off the deck, framing the plinth face and a bright wall | Backdrops regenerated without the painted pool or railing (rev2); characters tinted by the scene light; environment fill; gate camera moved onto the deck; wall night-toned; haze 0.011; box-built palms tried and removed | Better framing and integration; the cards still read as 2D when the camera turns (limitation) |

## 9. Limitations (honest)
1. **2.5D look:** characters, the SUV and both backdrops are flat generated images. When the camera turns they read as cards; the SUV can't be seen from another side. Natural character motion would need rigged 3D models. **Next step:** A3 (Blender MCP) builds the SUV, the rock shrine and the fence posts as real 3D props.
2. **OVERHEAR is close to IDLE in silhouette.** The dialogue panel and the overheard call carry the meaning.
3. **Walk cycle:** the generated "passing" frames failed (the model returned strides), so IDLE is the passing frame. The cycle reads as walking at game size but is visibly a 4-frame swap.
4. **The in-game camera** doesn't do the storyboard's special angles (section 4).
5. **Sound and music picks** were provisional, made from measured descriptors (Claude can't listen). Whether the gaana sounds like Chennai is pending Shriram's ears. The music model's non-commercial licence (MusicGen, CC-BY-NC) would need replacing for a commercial release.
6. **Intro arrival still:** Hari is shown driving, not riding pillion (prompt not followed), and that villa has a different design from the in-game villa (F11).
7. **The first 7 commits** carry the git identity `shrirampolarace` (Shriram's work config, by mistake). From `97b6e7f` onward, commits use `Shriram Alagarasan <azhagarasan.s@northeastern.edu>`.

---

# Assignment 3: three Blender assets

**Versions:** Blender 5.2.2 LTS (the chapter used 5.1.2) · Godot 4.7.2.stable.official.ed1daf0bf · mcp-for-blender 2.1.9 (add-on panel: "Addon 1.8") · uv 0.12.21 · macOS (Apple M1 Pro).
**Check commands** (run from the repo root; `timeout` is GNU coreutils 9.12):
```bash
G=~/Downloads/Godot.app/Contents/MacOS/Godot          # where Godot lives on this Mac
timeout 120 "$G" --headless --path godot --script res://tests/check_a3_selftest.gd --fixed-fps 60   # the check can fail
timeout 120 "$G" --headless --path godot --script res://tests/check_a3_assets.gd   --fixed-fps 60   # the real assets vs the brief
```

| Check | Result | Evidence |
|---|---|---|
| Interface notes | **Done.** Six parts in Shriram's own words, plus their own screenshot | [BLENDER-NOTES.md](BLENDER-NOTES.md) |
| The check can fail (self-test) | **PASS 17/17** (after the stand-in fix below). Every predicted failure (A3-F1…F7) is caught on BoxMesh stand-ins | `godot/tests/check_a3_selftest.gd` |
| Baseline before assets | **FAIL 3/3** (no `.glb` yet). The expected honest starting point | `evidence/a3/check-a3-1792019299.json` |
| Size (Blender vs brief vs Godot bounding box) | **PASS, all three** (table below; within ±5 %, in fact exact to the millimetre) | `evidence/a3/check-a3-1792111213.json` |
| Upright and node scale 1,1,1 | **PASS.** Godot Y extent = briefed height; all 8 nodes per asset at scale (1, 1, 1); root basis identity | same |
| Origin (sits on the floor, measured from mesh vertices) | **PASS.** Lowest mesh vertex y = +0.0000 m for each; origin under the footprint centre | same; `godot/tests/a3_measure.gd` |
| Triangle count (Blender vs Godot, vs budget) | **PASS.** SUV 456 / 456 (≤ 480), shrine 266 / 266 (≤ 280), fence 108 / 108 (≤ 120); course limit 500 | Blender: `tools/blender/build_*.py` results; Godot: check |
| Shape count (≤ 6 basic shapes) | **PASS.** 6 mesh nodes each | check |
| Colours survive export | **PASS.** Every briefed colour found within ±0.04 (SUV 11, shrine 8, fence 3) | check |
| SUV front faces +X | **PASS.** Cabin centre x = −0.575 m | check |
| Imports and appears in `scenes/a3_showcase.tscn` | **PASS.** `godot --headless --path godot --import` reimported all three with no errors; the scene opens with no errors and shows the three beside Hari's 1.75 m billboard | `evidence/a3/godot-*.png` (engine screenshots) |
| **HUMAN CHECK: look** (Shriram orbited each asset in the running scene, including behind and below) | **Done, Shriram's words below** | below |
| What Claude got wrong | **Nine things, listed below**, each caught by a measurement, a `look`, a screenshot or Shriram | below |

**Final numbers (2026-10-15 20:44, brief revision 3):**

| Asset | Brief W × D × H (m) | Blender, measured from vertices | Godot headless bounding box (x × y-up × z) | Triangles | Shapes |
|---|---|---|---|---|---|
| SUV | 4.60 × 1.90 × 1.70 | 4.600 × 1.900 × 1.700, lowest z 0.000 | 4.600 × 1.700 × 1.900, lowest y 0.0000 | 456 (≤ 480) | 6 |
| Rock shrine | 1.20 × 1.00 × 0.90 | 1.200 × 1.000 × 0.900, lowest z 0.000 | 1.200 × 0.900 × 1.000, lowest y 0.0000 | 266 (≤ 280) | 6 |
| Fence segment | 2.40 × 0.12 × 2.10 | 2.400 × 0.120 × 2.100, lowest z 0.000 | 2.400 × 2.100 × 0.120, lowest y 0.0000 | 108 (≤ 120) | 6 |

Blender is Z-up and Godot is Y-up: the glTF exporter's +Y Up swaps the axes, so Blender's depth (Y) becomes Godot's Z and the height moves to Y with no rescale. The Blender column comes from the read-only measurement call at the end of each build (`tools/blender/build_*.py`), which reads the same numbers the sidebar's Dimensions show, but per asset rather than per part.

**Inspect-and-revise cycles (all from observation; full code history in `tools/blender/`, brief revisions 2 and 3 in CHANGE-BRIEF.md):**
1. **SUV, build 1 → 2** (`18b3c9c` → `18d683e`). Build 1 matched revision 1 exactly (4.60 × 1.90 × 1.85 m, 200 tris). Shriram, in Blender: *"the suv in this blender should resemble a modern mercedes or a bmw suv, the one on blender looks pretty basic"*. Build 2: long glasshouse, raked windscreen, light bars, silver wheels, 1.70 m.
2. **SUV, build 2 → 3** (`1863c9b`). Shriram asked for a windscreen, four doors, separate windows, an opening tailgate with a handle, a grille, individual headlights, fog lamps and an exhaust. Build 3 does it with faces and flat colours on the same 6 shapes; the wheels dropped from 12 to 10 segments to stay under 500 triangles.
3. **SUV, build 3 → 4** (`09a9c16`). Shriram: *"the sides of the suv doesn't look good and proper, it is not equal sized,a dn that doesn;t look like a speartion, fix that"*. Equal 1.05 m doors, 3.5 cm near-black seams centred on the A, B and C pillars (measured seam centres x = −1.05, 0.00, +1.05).
4. **Shrine.** Revision 1's saffron box and cone roof contradicted the story bible (*"just a rock, with no building"*); Shriram chose the lore, then asked for the goddess on the rock and a reachable lamp with a real flame. Result: a relief goddess (saree silhouette, gold girdle, crown) on a sea-blue wave band in an arched niche, a brass lamp holder and teardrop flame on the sand at the front.
5. **Fence.** Revision 1's steel fence didn't match the A2 beach art; Shriram chose wooden posts and ropes.
6. **In Godot** (`f93ec6e`): the engine screenshot `evidence/a3/godot-shrine-front-BEFORE-facing-suv.png` showed the goddess facing the SUV's tail 1.3 m away. The showcase now turns the shrine's *slot* −90° (the asset keeps an identity transform, so the check still holds) and adds a flickering lamp light, since the model itself can't animate.

**HUMAN CHECK: look**: Shriram ran the showcase, pressed 1/2/3 and orbited each asset, including behind and below, beside Hari's billboard. Shriram's words, verbatim (typos included):
- **Fence:** *"this fence might be small , but this will be the one in the middle and there will be abunch of long fences surrounding it to cover the full lenth of the house so the villagers won't be able to enter, and the other things will be electrecuted as well, which is why it looks small, and because of the limitation, it was not able to say private porterty so i added a red rectangle in the middle"* (Claude built the sign; Shriram moved it to the middle in the hand edit).
- **SUV:** *"the suv is perfect for its colour and everyhting but in reality when i design it will be much better as it will not be refined to these shapes and it will look like a regular suv and not rectangle like this, with the wheels and everything bu t i'ms atisfied how it kookes given the conditons"*
- **Shrine:** *"the shrine actually looks great and it depicts the goddes on the rocka dn the flame on the side looks great too, in future i will work on getting the goddess right nd making it much more look realistic"*
- No missing faces or wrong colours were reported. No other person has looked at the scene; none is claimed.

**What Claude got wrong (each caught, each logged where it happened):**
1. The brief priced an icosphere at "subdivisions 1" as 80 triangles. In Blender that's the bare 20-triangle icosahedron; 80 needs subdivisions 2 (corrected in revision 2).
2. The rock first measured 1.141 m long, not 1.20: an icosphere doesn't reach its radius along X. Caught by `get_scene_info`; stretched to 1.200 (shrine call 1b).
3. SUV build 2: "raise the nose and tail" raised the whole underside, because a cube only has corner vertices (kept, disclosed).
4. SUV build 2: the silver wheel face didn't apply on the first wheel; caught with `look`, fixed (call 3b). Cause: material indices set before the mesh had material slots.
5. SUV build 3: door seams too thin and dark, front door longer than the pillars implied. Caught by Shriram (cycle 3).
6. Fence: the sign first floated between the ropes, touching nothing. Caught with `look`, moved onto the middle rope (call 6b).
7. Export: reading the exporter's format list returned an empty list (dynamic enum); then opening a `.blend` inside the same call lost the window context the exporter needs. Fixed by passing `"GLB"` and opening and exporting in separate calls (`tools/blender/export_glb.py`).
8. Godot showcase: the goddess faced the SUV (cycle 6).
9. The self-test's "correct" fence stand-in kept revision 1's steel colours after the brief changed, so it failed 1 of 17. The assertion was kept; the stand-in now uses revision 3's colours (`81c1666`). A green report would have been easy to get by deleting the colour row; that wasn't done.

**Shriram's hand edit** is recorded in [BLENDER-NOTES.md](BLENDER-NOTES.md). The check also caught it mid-way: with the sign dragged by eye to y = −0.085, the fence measured **0.16 m deep instead of 0.12** (a 33 % size failure) and the scene had **8 shapes** after the duplicates. Both were fixed by Shriram before the export.

**What the check does and does not show:** it measures what arrived in Godot: mesh-vertex bounding box, node scales, the lowest vertex height, triangles, mesh count and albedo colours. It cannot tell whether an asset reads as an SUV, a shrine or a fence, whether its colours suit the night lighting, or whether it fits the game's cel-shaded style. Those are Shriram's human checks. Shape count is inferred from mesh nodes, so objects joined in Blender would hide it.

**Known limitations:** each asset is a silhouette of at most 6 basic shapes (no wheel arches, mirrors or door handles on the SUV; a figure, not a portrait, for the goddess); the sign can't carry lettering without a painted texture; the flame is static in the model (the flicker is a Godot light); the assets sit in the A3 showcase, not yet in the A2 night slice, so they haven't been judged under the game's night lighting; the triangle and shape counts trust Godot's mesh nodes (objects joined in Blender would hide the shape count).
