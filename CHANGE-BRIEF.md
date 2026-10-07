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
