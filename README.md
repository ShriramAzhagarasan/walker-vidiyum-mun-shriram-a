# walker-vidiyum-mun-shriram-a: Vidiyum Mun (விடியும் முன், "Before Dawn")

**CSYE 7270 Fall 2026 · Assignment 2: Generate Art, Sound, and Music for Your Game**
**Student:** Shriram Alagarasan · **Engine:** Godot 4.7.2.stable.official (macOS) · **Renderer:** Forward+

A time-loop mystery at the last party on a rich family's illegally fenced beach on ECR, Chennai. You play Hari, a middle-class engineering student. Every dawn ends in tragedy and he wakes at 8 PM again, keeping only what he learned. This repo holds the **asset slice**: one playable 2.5D scene (Telltale-style 3D deck, generated cel-shaded characters) that proves the generated art, sound effects and music work together in the engine.

## Started from
An **empty Godot 4.7.2 project**. GDScript conventions and the headless test pattern were borrowed from my Assignment 1 repo [walker-jumpman-shriram-a](https://github.com/ShriramAzhagarasan/walker-jumpman-shriram-a), which was based on [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) by Nik Bear Brown. No art, levels or characters from either are reused.

## Run it
1. Install [Godot 4.7.2](https://godotengine.org/download) (standard build, no .NET needed).
2. Clone this repo and import once (this builds the `.godot/` cache, which isn't committed):
   ```bash
   GODOT=/Applications/Godot.app/Contents/MacOS/Godot   # adjust to your install
   "$GODOT" --headless --path godot --import
   ```
3. Run: `"$GODOT" --path godot`, or open `godot/project.godot` in the editor and press **F5**. It opens on the **title screen**: press **Enter** for the ~30 s intro (Enter skips a panel, **Esc** skips the intro), then the slice starts at 8 PM.

## Controls
| Key | Action |
|---|---|
| **W A S D** / arrow keys | Walk (camera-relative) |
| **E** / **Space** | Talk, advance dialogue, pick a choice (W/S to move between choices) |
| **Hold T** | Fast-forward the night (×8) |
| **Esc** / **P** | Pause (music is muffled while paused) |
| **M** | Mute or unmute **music** |
| **N** | Mute or unmute **sound effects** |
| **R** | Restart from loop 1 (after the end card) |
| **Enter / Esc** | Title: start the intro / skip the intro |

## What the slice demonstrates
- **Hari in 10 states**, one static generated image per state (idle, walk, talk, phone, notes, overhear, startled, keys, white-out, relief). He faces the way he walks (the image flips at runtime). Collision is a 0.28 × 1.70 m capsule.
- **A generated environment:** a white glass villa, Italian marble, the beach view with the rock shrine, the fence and village boats, a fire overlay, the SUV. **Generated non-player characters:** Manikandan (2 states), Advay, Krishna.
- **Five generated sound effects on real game events:** Amma's call buzz (loop start), clue chime (new knowledge only), keys (they change hands), dawn horn and screech (failure), waves and crows (safe dawn). Each fires exactly once per event (automated test).
- **Two generated music loops** (party dance music and village gaana) that crossfade as you walk toward the fence, thin out after 3 AM, muffle on pause, stop at dawn, and restart at 8 PM.
- **The core loop, once:** loop 1 earns two clues; loop 2 uses them to keep the car keys with Manikandan, and the end card follows.
- **A title screen and intro motion comic** (4 generated stills, story captions) that set up the story, then cut to 8 PM. It covers storyboard panel 1.
- **Loop 2 isn't a replay:** Hari wakes in shock and notices people repeating themselves word for word.
- **Readable when muted:** every sound has a visual twin (phone card, notes card, keys icon, headlights and white-out, sunrise).

## Tests
```bash
"$GODOT" --headless --path godot -s res://tests/test_assets_present.gd   # every generated asset is present and well-formed (70 checks)
"$GODOT" --headless --path godot -s res://tests/test_audio_mix.gd        # music under SFX, ducking, N/M mute toggles (10 checks)
"$GODOT" --headless --path godot -s res://tests/test_sound_triggers.gd   # exact per-event sound counts over a scripted 2-loop run
"$GODOT" --headless --path godot -s res://tests/test_loop_logic.gd       # knowledge persists, flags reset, keys-safe prevents the crash
"$GODOT" --headless --path godot -s res://tests/test_slice_smoke.gd      # the 3D scene builds with all nodes
python3 tools/check/loop_seam_check.py                                   # music loop seams (needs numpy + soundfile)
```
Results and the human playtest are in [TEST-REPORT.md](TEST-REPORT.md).

## Docs
[CONCEPT](CONCEPT.md) · [STORYBOARD](STORYBOARD.md) · [CHARACTER-SHEET](CHARACTER-SHEET.md) · [CHANGE-BRIEF](CHANGE-BRIEF.md) · [DIALOGUE](DIALOGUE.md) · [ASSET-LOG](ASSET-LOG.md) · [SOURCES](SOURCES.md) · [FRICTIONAL](FRICTIONAL.md) · [TEST-REPORT](TEST-REPORT.md) · my original story and decisions: [design/input/](design/input/)

## Known limitations
- **2.5D:** characters, the SUV and the backdrops are flat generated images in a 3D deck, so they read as cards when the camera turns. Natural character motion would need rigged 3D models. **Next step (A3):** build the SUV, the rock shrine and the fence as Blender models.
- OVERHEAR's silhouette is close to IDLE. The walk cycle is a 4-frame swap (IDLE serves as the passing frame).
- The in-game camera doesn't reproduce the storyboard's special angles (see TEST-REPORT, section 4).
- Music (MusicGen) is CC-BY-NC: fine for coursework, not for a commercial release.
- Full list: [TEST-REPORT.md, section 9](TEST-REPORT.md).

## Film
Brutalist `godot-gamedev` explainer (walker mode, Liam narration), 3840×2160, 30 fps, **6:18**.
- **Link (Northeastern OneDrive):** [claude-liam-walker-vidiyum-mun-shriram-a-gamedev.mp4](https://northeastern-my.sharepoint.com/:v:/g/personal/azhagarasan_s_northeastern_edu/IQCsgk2bE-sbTo2EHyuUU-r5AQHG8865pDMU0TWLaO7khVw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=YVnmag)
- **File:** `claude-liam-walker-vidiyum-mun-shriram-a-gamedev.mp4` · **SHA-256:** `e948a875752d4e1f3745054ad4fc0921d9d2dfd81313ed0e5b832db8b06502fe`
- **Source revision shown:** `13f772c` (the game source is unchanged after it; later commits are docs and film records only)
- **Film records:** [youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev/](youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev/), containing the beat sheet, script and prompts (`PROMPTS.md`, `RIFF.md`), `FACTCHECK.md`, `SHOTLIST.md`, the evidence ledger (`gamedev-evidence.json`), capture logs, the capture driver and QC.
- `./art godot-gamedev --check` **PASS** (110 source files, 4 exact excerpts, 4 code→result pairs).
- **Text-legibility gate (GATE T):** it flagged small text that sits *inside* real game footage and reproduced generated images (the game's own HUD, raw generations, R1 screenshots), not the film's captions. The final compile ran the same `compile.py` step with every other gate on, and the reasons are documented in `youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev/_qc/GATE-T-OVERRIDE.md`.
