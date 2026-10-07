# FACTCHECK — every claim, its source

Paths are relative to the game repo root. **RE-VERIFY** = may change at the code freeze; re-check before Kokoro/renders.
Code excerpts are not listed here: `tools/author_sheet.py` copies them verbatim by anchor and `./art godot-gamedev --check` verifies text, lines and hashes.

| Beat | Claim | Source |
|---|---|---|
| B00 | Prompt is an illustrative reconstruction, not a transcript | Labelled on screen; real requests: `design/input/SHRIRAM-DECISIONS.md` |
| B00 | Every picture and sound came from a local model | `SOURCES.md` l.6–13 (all models local, M1 Pro); `CHANGE-BRIEF.md` l.40–45 |
| B00 out | 10 Hari states; 5 SFX events; 2 music loops; loop 1 clues, loop 2 keys | `README.md` l.32–36 |
| B01 | One spec / model / pick / edits / function chain | B04–B08 sources below |
| B01 | Five sounds each fire once per event | `CHANGE-BRIEF.md` §2 l.50–58; `TEST-REPORT.md` l.16; capture driver summary |
| B02 | Concept in plain terms; four pillars (spoken) | `CONCEPT.md` l.6, l.19–22 |
| B02 | Title screen + intro motion comic is the game's main scene, real capture | `godot/project.godot` `run/main_scene=res://scenes/intro.tscn`; `scenes/intro.gd`; capture log (Enter once, panels on `PANEL_SECONDS` timers) |
| B03 | Scripted keyboard input | `CAPTURE.md`, `capture/run-01-inputs.jsonl` |
| B03 | 8 PM, loop 1; buzz = Amma; PHONE pose; "studying at Krishna's place" | `autoload/loop_state.gd` `start_loop` (phone_buzz); `data/dialogue.json` amma_call_first (hari_state PHONE, line D1b); `DIALOGUE.md` D1b |
| B04 | Spec committed before generation | `CHARACTER-SHEET.md` l.3; git `72c3169` "Commit design before any generation" |
| B04 | Ten states, PHONE #4: phone to ear, elbow out, eyes away (he's lying) | `CHARACTER-SHEET.md` l.32 (row shown verbatim) |
| B04 | Silhouette risk IDLE/PHONE/OVERHEAR at 208 px; rule elbow out | `CHARACTER-SHEET.md` l.21; `CHANGE-BRIEF.md` F5 l.97 |
| B04 | Spec image is code-drawn, not model output | `CHARACTER-SHEET.md` l.4; `tools/design/draw_character_sheet.py` |
| B05 | Exact prompt text (identical for seeds 301 and 302) | `gen/log.jsonl` CHAR-HARI-PHONE seed 301 row (rendered from the row by `tools/make_trace_images.py`; copy in `evidence/asset-trace/phone-s301-log-row.json`) |
| B05 | Edit from the reference; FLUX.2 [klein] 4B; local | same row: `model flux2-klein-4b`, `edit_refs [design/character/gen/hari-ref.png]`; `SOURCES.md` l.9 |
| B05 | Reference = Shriram's pick B | `design/input/SHRIRAM-DECISIONS.md` l.19; `gen/decisions.json` CHAR-HARI-REF_klein_s102 |
| B05 | Seeds 301/302, 768×1344, 8-bit | `gen/log.jsonl` rows 15–16 (`seed`, `width`, `height`, `quantize: 8`) |
| B06 | s302 was wired in first | `gen/edit_log.jsonl` l.5 (02:29, src s302 → phone.png) |
| B06 | Shriram spotted a second phone at the far ear in a playtest screenshot; s302 rejected | `gen/decisions.json` CHAR-HARI-PHONE_klein_s302 (`by: Shriram (playtest screenshot) / Claude`, reason "two phones … Shriram's screenshot 13:00"); visible in the raw (circle added) |
| B06 | s301 (one phone) is in the build: proposed by Claude, approved by Shriram | `gen/decisions.json` CHAR-HARI-PHONE_klein_s301 (`by: Claude (proposed) · approved by Shriram 2026-10-07`); `design/input/SHRIRAM-DECISIONS.md` l.24 ("yes everything is okay"); `gen/edit_log.jsonl` l.50 |
| B07 | rembg isnet-anime, alpha<16→0, largest region, trim bbox (181, 53, 608, 1318), 680 px Lanczos, padded centred on legs | `gen/edit_log.jsonl` l.50 (all six steps shown verbatim on the board) |
| B07 | Floor shadow removed with the background | Visual: raw s302 vs `phone.png` (board B-edit) |
| B07 | "My reading": mirrors around its centre → feet stay put | Interpretation, labelled as such; `scenes/billboard_art.gd` `centered = true`; `scenes/hari.gd` `sprite.flip_h = _facing_left` |
| B08 | lowercases the state → `<state>.png` | `scenes/hari.gd` `_show_state` (excerpt) |
| B08 | Image sized to exactly 1.75 m | `scenes/billboard_art.gd` l.34 `pixel_size = height_m / float(texture.get_height())`; `logic/hari_spec.gd` l.4 `HEIGHT_M := 1.75`; `scenes/hari.gd` `sprite.height_m = Spec.HEIGHT_M` |
| B08 | Label only when art missing | `scenes/hari.gd` `label.visible = not sprite.has_art` |
| B09 | PHONE→IDLE at call end, WALK, TALK at Krishna | `capture/run-01-inputs.jsonl` `hari_state` rows |
| B09 | 4 walk frames stepped by distance travelled | `godot/assets/art/hari/walk_1..4.png`; `scenes/hari.gd` `STRIDE_M := 0.42`, `_walk_frames`, `int(_travel / STRIDE_M) % _walk_frames.size()` |
| B10 | One flag per event, reset each loop; Advay once at 1:40; dawn once at 5:50 | `autoload/loop_state.gd` `_set_clock` (excerpt), `_reset_loop_flags`, l.27 `ADVAY_TIME`, l.30 `DAWN_TIME` |
| B10 | T = 8× clock, same checks | `autoload/loop_state.gd` l.24 `FAST_FORWARD := 8.0`, `_process` → `_set_clock`; `autoload/controls.gd` `ls.fast_forward = Input.is_action_pressed("fast_forward")` |
| B11 | Driver holds the real T key; 1:21 overhear; clue; 1:40 Advay takes keys at 1×; jingle; second clue | `capture/run-01-inputs.jsonl` (input T rows, `sfx_event` rows, `advay_arrived took_keys true`) |
| B12 | SoundBank connects to logic signals, never changes state; missing/muted file changes nothing | `autoload/sound_bank.gd` header l.1–4 + excerpt; `CHANGE-BRIEF.md` l.48 |
| B13 | Test mashes E ten times, holds it, counts requests; 2/3/2/1/1; same muted | `tests/test_sound_triggers.gd`; `TEST-REPORT.md` l.16; `evidence/tests/test_sound_triggers.txt` (real stdout, re-run at freeze) |
| B13 | Driver counted the same | `capture/run-01-inputs.jsonl` `summary.counts` |
| B13 | Can't tell whether they sound right | `TEST-REPORT.md` l.22 |
| B14 | Game audio only | `mp3/game/B14.wav` = `capture/run-01.wav` same frames, −8 dB |
| B15 | Horn and screech never seen | `CONCEPT.md` l.49; `CHANGE-BRIEF.md` SFX-DAWN-CRASH |
| B15 | Hari in shock; the call repeats word for word | `data/dialogue.json` amma_call_repeat D8–D9d ("Same call. Same words."); Shriram's playtest note "loop 2 dialogue repeated, he should be in shock" (coordinator brief) |
| B15 | Choice exists because both clues known (loop ≥ 2, before 1:40) | `autoload/loop_state.gd` `ask_selvam_available` |
| B15 | Keys kept → KEYS pose, jingle, third note | `loop_state.gd` `ask_about_selvam`; `story.gd` `_on_keys_exchanged`; capture log |
| B16 | 1:40 refusal, no jingle because keys didn't move | `loop_state.gd` `_advay_arrives` (KEYS_SAFE → `advay_arrived(false)`, no `keys_exchanged`); `dialogue.json` captions.advay_refused |
| B16 | Safe dawn: waves and crows, RELIEF, sunrise, end card "…but someone is missing" | `CHANGE-BRIEF.md` SFX-SAFE-DAWN; `story.gd` `_on_safe_dawn`; `slice.gd` `_on_safe_dawn`; `dialogue.json` end_card |
| B17 | Early screenshots read as lavender dusk | `TEST-REPORT.md` §8 R1 l.45 |
| B17 | Ambient → 100f26, moonlight → 0.08 | `scenes/slice.gd` SKY_KEYS 1290.0 row (excerpt); before values from `TEST-REPORT.md` l.45 |
| B17 | String lights 2.8 in the deck script | `scenes/deck_dressing.gd` l.44 |
| B18 | Before/after screenshots are scripted (test API) | `evidence/revisions/R1-lighting-*.jpg`; `tools/capture_shots.gd` header |
| B18 | Hari unshaded, colours unchanged | `scenes/billboard_art.gd` l.16 `shaded = false` |
| B19 | Test results on cards | `evidence/tests/summary.json` + `*.txt` (stdout of each test, re-run on the frozen copy); seam check PASS per `TEST-REPORT.md` l.19 / `tools/check/loop_seam_check.py` |
| B19 | Four playtests; notes (motion too static; loop 2 repeated; backgrounds slapped on; effects inaudible) drove revisions | `design/input/SHRIRAM-DECISIONS.md` l.21–24; `TEST-REPORT.md` l.78, R11 l.107 |
| B19 | Audio-mix test added at the refreeze | `tests/test_audio_mix.gd`; `evidence/tests/test_audio_mix.txt` (10/10) |
| B19 | Not proven: audible/mix; musical seam; clock jumps | `TEST-REPORT.md` l.21–24 |
| B20 | Shriram: reference B (his own pick); 4 playtests; approved Claude's other picks and the dialogue | `SHRIRAM-DECISIONS.md` l.19, l.24; `gen/decisions.json` (`approved by Shriram` rows) |
| B20 | Who did what | `SOURCES.md` l.23–30; `design/input/SHRIRAM-DECISIONS.md` l.17–19 |
| B20 | Model per asset; Z-Image comparison only | `SOURCES.md` l.9–13; `CHANGE-BRIEF.md` l.40–45 |
| B20 | Build snapshot id | `tools/source_snapshot.py` output |
| B21 | Billboard characters and the SUV read as 2D when the camera turns | `FRICTIONAL.md` (playtest 3 notes, "still unresolved"); coordinator brief |
| B21 | Next (A3): Blender models for the SUV, rock and fence | `FRICTIONAL.md` / coordinator brief (stated next step) |
| B21 | Muted-play legibility uncertain | `CHANGE-BRIEF.md` F10; `TEST-REPORT.md` §7 (human, pending) |
| B23 | Exact title | `beat_sheet.json → metadata.title` |

## Corrections applied while drafting
- "124.5 s each" → "about 2 min each": the two seeds took 128.2 s and 124.5 s.
- Dropped "one still per state" from the verdict: a walk cycle is being added at the freeze.
- PHONE changed from s302 to s301 at 13:01 after Shriram's screenshot; the trace follows s301. Claude proposed it; Shriram approved all picks at ~16:55.
- Source refrozen at `13f772c` (R11 audio mix fix) after the first final take on `e227f23`; that take is kept in `capture/superseded-e227f23/` and is not used.
- Verdict limit changed from OVERHEAR to the 2D-billboard limitation stated for the freeze.
