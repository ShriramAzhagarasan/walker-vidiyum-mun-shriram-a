# CAPTURE — Vidiyum Mun gamedev film

## Method
| Item | Value |
|---|---|
| Game | `walker-vidiyum-mun-shriram-a/godot` (Godot 4.7.2.stable.official.ed1daf0bf, Forward+ / Metal, Apple M1 Pro) |
| Build id | `tools/source_snapshot.py` content hash of `godot/` (excluding `.godot/`). Final value written into `beat_sheet.json → metadata.game.build_id` at the freeze. |
| Method | **scripted-input**, not a human playtest |
| Recorder | Godot Movie Maker: `--write-movie capture/run-01.avi --fixed-fps 30 --resolution 3840x2160` (offline render, ~24 % of real time; **not** evidence of real-time FPS) |
| Raw output | MJPEG (quality 0.9) + PCM s16le 48 kHz stereo AVI, native 3840×2160 |
| Derived | `capture/run-01.mp4` (H.264 CRF 12, video only), `capture/run-01.wav` (lossless PCM from the AVI), `capture/run-01-av.mp4` (H.264 + AAC 320k, for viewing) |
| Input log | `capture/run-01-inputs.jsonl`: every key event the driver sent and every observed game event, against the rendered frame (`t = frame / 30`) |

## Isolated harness copy
`capture-project/` = `rsync` of `godot/` (excluding `.godot/`), refreshed by `tools/prepare_capture_copy.sh`. It differs from the game in exactly two ways:
1. `project.godot`: `window_width/height_override = 3840×2160`, `window/size/no_focus = true` (the capture window can never take keyboard focus) and `[editor] movie_writer/mjpeg_quality = 0.9`. The 3D viewport therefore renders natively at 4K; the HUD (1280×720 logical, `canvas_items` stretch) scales 3×.
2. `capture_driver.gd` added. No game file is modified.

## The driver's rules (`capture-project/capture_driver.gd`)
- Instantiates the project's main scene (`run/main_scene` = `res://scenes/intro.tscn`) as the current scene. At the title it presses **Enter once**; the four intro panels then run on their own timers (`intro.gd PANEL_SECONDS 6.5`) and the intro changes scene to `slice.tscn`, whose `_ready()` starts loop 1 as in normal play. The driver waits for that scene change.
- Plays only through `Input.parse_input_event(InputEventKey)` with the physical keycodes bound in `logic/input_setup.gd`: **D/A/W/S** walk (chosen each frame from the camera's basis, because movement is camera-relative), **E** talk/advance, **W/S** move the choice cursor, **P** pause, **T held** = the game's own fast-forward (×8, `LoopState.FAST_FORWARD`). The film says so on screen.
- Observes position, clock and phase to decide *when* to press; never teleports, sets the clock, sets state or calls any `test_*` API.
- `InputMonitor` fails the take if any key or mouse event reaches the game that the driver did not send (a real keyboard press, OS key repeat, a click).
- If the OS releases held keys on focus loss, a held walking/T key is re-pressed and logged (`input_reassert`).
- At the end it asserts: `SoundBank.trigger_counts == {phone_buzz 2, clue_saved 3, keys_exchanged 2, dawn_crash 1, safe_dawn 1}`, all ten Hari states shown, end card reached in loop 2, and (final take) all five SFX files loaded. Then `CAPTURE OK`, exit 0; otherwise `CAPTURE FAIL: <reason>`, exit 1.

## Route (one continuous take)
Title (3 s) → Enter → intro panels 1–4 (gaana music; dawn horn on panel 4) → "…and Hari wakes up at 8 PM. Again." → slice.
Loop 1: Amma's call (PHONE) → walk to Krishna, talk (WALK, TALK) → railing (music crossfade) → P pause / P resume → hold T, walk back to the SUV → release at 1:21 AM → E: overhear Manikandan's call (OVERHEAR → clue, NOTES) → wait at 1× to 1:40 (Advay takes the keys: keys + clue) → hold T to 5:44 on the deck → dawn at 1× (dawn_crash, white-out, WHITEOUT) → loop 2 reset.
Loop 2: STARTLED + the 9-line repeat call (2.4 s per line) → walk to the SUV → E: choice, S then W (cursor), E: Ask about Selvam → 4 lines → keys stay (KEYS, keys + clue) → hold T to 1:35, 1:40 at 1× (Advay refused, no keys sound) → hold T, walk to the railing, release 5:44 → safe dawn (RELIEF, sunrise) → end card.

## Audio in the film
- Clip audio is stripped by `compile.py`; each beat's sound is its `audio_file`.
- Narrated gameplay beats: narration + the slice's own audio from **the same frames** of `capture/run-01.wav`, at **−20 dB** under the voice (faded out over any HELD FRAME).
- **B14 "Game audio, no narration"**: the slice's own audio alone, same frames, at **−8 dB** (the party loop peaks at 0 dBFS in the raw mix; −8 dB matches the narration loudness). No narration over it.
- The outro card has no game audio.

## Takes so far (PHASE 1)
| Take | Result | Notes |
|---|---|---|
| `probe-4k` (12:18–12:21) | **Contaminated, discarded.** | Driver crashed at init (`SoundBank` not ready), so it never pressed a key; the capture window still had keyboard focus and **a person played it** (log shows E presses, walking, Krishna talk). Movie Maker ran at 22 % of real time and sends audio to the file, not the speakers. Fixes: `no_focus`, `InputMonitor`, setup moved after the first frames. It did prove 4K Forward+ + PCM audio (mean −14.2 dB, peak 0.0 dB). AVI deleted. |
| `validate-720` (12:24–12:35) | `CAPTURE OK frames=4601 (153.4 s)`, counts 2/3/2/1/1, 10/10 states, 0 foreign events, 0 re-presses | Name is historical: the project override wins over `--resolution`, so it is native 3840×2160. Run with `allow_missing_sfx` (SFX not yet delivered): music only. Used to plan clip ranges and test the pipeline; **not** film footage. Build = pre-freeze. |
| `superseded-e227f23/run-01` | `CAPTURE OK frames=5798`, 2/3/2/1/1, 0 foreign | First final take on `e227f23`. Superseded: playtest 4 found the SFX masked by the music (R11). Not used. |
| `run-01` | see `capture/run-01.log`, `run-01-sfx-levels.json` | Frozen build `13f772c` (R11 mix), all five SFX loaded. **The film's footage.** |
