# Test report: Vidiyum Mun asset slice

- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf · **OS:** macOS 26.6.2 (MacBook Pro M1 Pro, 16 GB) · **Renderer:** Forward+ (Metal)
- **Source revision tested (frozen for the film):** `e227f23` (main, 2026-10-07 16:40 EDT)
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
  - `evidence/shots/state_<state>_{right,left}.png` [SCRIPTED CAPTURE]: each state in engine, facing right and flipped left.
  - `design/character/poses-spec.png`: the spec.

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

| Panel | Slice evidence | Matches | Differences, and why |
|---|---|---|---|
| 1 Title, bird's-eye | `intro_title.png`, `intro_panel_1.png` | The villa, fence, village fire and ECR in one establishing frame, with the title. | A **design view**, made as a generated still with a slow zoom in the intro, not the 3D scene. |
| 2 8 PM Amma's call | `p02_amma_call.png` | PHONE pose, phone card, 8:00 PM clock, villa and string lights, dialogue | none significant |
| 3 Talk to Manikandan | `p03_gate_walk.png`, `p03_talk_manikandan.png` | WALK → TALK, Manikandan at the SUV, "E — Talk", gate framing | Not over-the-shoulder; the follow camera frames the SUV from the front-right. |
| 4 Clue saved | `p04_overhear.png`, `p04_clue_saved.png` | OVERHEAR during the call, then NOTES with the notes card | No close-up high-angle phone shot. The **HUD notes card** is the close-up. |
| 5 1:40 keys taken | `p05_keys_taken.png` | Advay with the speaker, caption, keys icon arcs to him | Not a low angle. Advay's line is a timed caption, not modal. |
| 6 Dawn failure | `p06_dawn_crash.png`, `p06_whiteout.png` | Music cut, horn, headlight sweep, shake, WHITEOUT pose, white-out | No Dutch tilt (shake instead). |
| 7 Loop 2 wake | `p07_loop2_wake.png` | STARTLED, damp shirt, "loop 2", D8 thoughts, the call again | No camera push-in. Revision 2 dialogue adds Hari's shock lines. |
| 8 Keys stay | `p08_choice.png`, `p08_keys_stay.png` | "Ask about Selvam" (only with both clues), KEYS pose, keys icon to Manikandan | none significant |
| 9 Safe dawn and end card | `p09_safe_dawn.png`, `p09_end_card.png` | RELIEF at the railing, dawn, beach and rock backdrop, end card in English and Tamil | Not a low angle from the sand; the railing camera looks out to sea instead. |

## 5. Sound events
| Check | Result |
|---|---|
| [AUTO] One request per occurrence, including rapid and held input (section 2) | PASS |
| [AUTO] 6 s Movie Maker capture of the real game: audio present | Mean −13.3 dB, music audible (before the −4 dB headroom change) |
| [HUMAN] Each of the 5 sounds heard once per event in real play | *(awaiting Shriram, playtest 4)* |

## 6. Music
| Check | Result |
|---|---|
| [AUTO] Seam check, 3 repetitions | PASS (section 2) |
| [AUTO] Pause (low-pass and −8 dB), stop at dawn, restart at 8 PM, stopped at the end card | Implemented in `sound_bank.gd`; the stop and restart are exercised by `test_sound_triggers` (music_playing flag) |
| [HUMAN] ≥ 3 repetitions in game without an audible click; does the gaana feel like Chennai (F8)? | *(awaiting Shriram)* |

## 7. Muted play
| Check | Result |
|---|---|
| [AUTO] Both buses muted → identical game outcome and event counts | PASS (section 2) |
| [HUMAN] Played with M and N muted: understandable? | *(awaiting Shriram)* |

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
| R10 | **Shriram, playtests 2–3:** backgrounds "not sitting right… slapped on"; the painted pool and railing in the backdrops duplicated the 3D ones; the gate camera sat 5.8 m off the deck, framing the plinth face and a bright wall | Backdrops regenerated without the painted pool or railing (rev2); characters tinted by the scene light; environment fill; gate camera moved onto the deck; wall night-toned; haze 0.011; box-built palms tried and removed | Better framing and integration; the cards still read as 2D when the camera turns (limitation) |

## 9. Limitations (honest)
1. **2.5D look:** characters, the SUV and both backdrops are flat generated images. When the camera turns they read as cards; the SUV can't be seen from another side. Natural character motion would need rigged 3D models. **Next step:** A3 (Blender MCP) builds the SUV, the rock shrine and the fence posts as real 3D props.
2. **OVERHEAR is close to IDLE in silhouette.** The dialogue panel and the overheard call carry the meaning.
3. **Walk cycle:** the generated "passing" frames failed (the model returned strides), so IDLE is the passing frame. The cycle reads as walking at game size but is visibly a 4-frame swap.
4. **The in-game camera** doesn't do the storyboard's special angles (section 4).
5. **Sound and music picks** were provisional, made from measured descriptors (Claude can't listen). Whether the gaana sounds like Chennai is pending Shriram's ears. The music model's non-commercial licence (MusicGen, CC-BY-NC) would need replacing for a commercial release.
6. **Intro arrival still:** Hari is shown driving, not riding pillion (prompt not followed), and that villa has a different design from the in-game villa (F11).
7. **The first 7 commits** carry the git identity `shrirampolarace` (Shriram's work config, by mistake). From `97b6e7f` onward, commits use `Shriram Alagarasan <azhagarasan.s@northeastern.edu>`.
