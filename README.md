# walker-vidiyum-mun-shriram-a: Vidiyum Mun (விடியும் முன், "Before Dawn")

**CSYE 7270 Fall 2026 · current submission: Assignment 6, Creating Particle Effects with Godot and Claude (tag `a6`; see
["Assignment 6"](#assignment-6-particle-effects-tag-a6)). The game began in Assignment 2 (art, sound and music);
Assignment 3 added Blender models, Assignment 5 shaders and materials.**
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
| **F10** (debug builds) | Vsync on/off, for the A6 FPS comparison only (no project-setting change). On a Mac: **fn+F10** |
| **F11** (debug builds) | Both A6 particle effects off/on, for the A6 price comparison. On a Mac: **fn+F11** |

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
These are the A2 suites, run without `--fixed-fps` on purpose: three of them measure wall-clock time (`Story._now()`)
and fail only when the frame rate is pinned (a known A2 limitation, kept out of A5's scope). The A5 tests run through
`scripts/run-test.sh` (section "Assignment 5" below). Results and the human playtest are in [TEST-REPORT.md](TEST-REPORT.md).

## Assignment 3: three Blender assets (tag `a3`)
Three game assets built from Blender's basic shapes by directing Claude through the **Blender MCP**, then exported as `.glb` and shown together in `godot/scenes/a3_showcase.tscn` beside Hari's 1.75 m billboard:
  - **The SUV:** 4.60 × 1.90 × 1.70 m, 456 triangles.
  - **The rock shrine:** the sea goddess in relief, with a brass lamp; 1.20 × 1.00 × 0.90 m, 266 triangles.
  - **A fence segment:** wooden posts and ropes; 2.40 × 0.12 × 2.10 m, 108 triangles.

  Each is at most 6 shapes. The final sizes come from brief revisions 2–3, which were driven by my inspection in Blender.
- **Versions:** Blender 5.2.2 LTS · Godot 4.7.2 · mcp-for-blender 2.1.9 · macOS.
- **Brief (committed before building):** [CHANGE-BRIEF.md](CHANGE-BRIEF.md), the "Assignment 3" section, plus `godot/tests/data/a3_brief.json`. Interface notes: [BLENDER-NOTES.md](BLENDER-NOTES.md).
- **Open the scene:** `"$GODOT" --path godot res://scenes/a3_showcase.tscn`. Drag or arrow keys orbit (including from behind and below), scroll zooms, 1/2/3 focus each asset, 0 shows all, H toggles Hari, L toggles labels.
- **Run the check:** `timeout 120 "$GODOT" --headless --path godot --script res://tests/check_a3_assets.gd --fixed-fps 60`, and its self-test `check_a3_selftest.gd`. Results: [TEST-REPORT.md](TEST-REPORT.md), section "Assignment 3".
- **Blender sources:** `blender/<asset>.blend` and the exact code Claude ran in `tools/blender/build_<asset>.py` (plus `export_glb.py`).
- **What this assignment added:** the three models and their sources, `scenes/a3_showcase.tscn` (with a flickering lamp light), the headless check `tests/check_a3_assets.gd` (**31/31 PASS**) and its self-test (**17/17**), and the A3 sections of every doc. My hand edit is in BLENDER-NOTES.md.
- **A3 film:** [claude-liam-vidiyum-mun-a3-gamedev.mp4](https://northeastern-my.sharepoint.com/:v:/g/personal/azhagarasan_s_northeastern_edu/IQA4dYF_0V_BSpYUUXYgVdkjAaIpfKV-HliF7n9IKG8jTEc?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=xe2yTl) (Northeastern OneDrive), 3840×2160, 30 fps, 4:21, SHA-256 `40e99c7d4e55ecb2b7e004f608e3c55bd43010fd8776b86c66e2f8ed66b3a91e`. It shows game source `81c1666`. Records: [youtube/claude-liam-vidiyum-mun-a3-gamedev/](youtube/claude-liam-vidiyum-mun-a3-gamedev/).
- **A3 known limitations:**
  - The assets are silhouettes, with no lettering on the sign.
  - The flame is static in the model; the flicker is a Godot light.
  - They aren't in the night slice yet.

  Full list in TEST-REPORT.md.

## Assignment 5: shaders and materials (tag `a5`)
Two shaders added to the night slice (`scenes/slice.tscn`), plus a hint experiment. The specification and Shriram's
predictions are in [CHANGE-BRIEF.md](CHANGE-BRIEF.md), written before any shader existed.
- **"The night is slipping"** (`godot/shaders/night_skip.gdshader`, `canvas_item`, hand-written by Shriram): while you
  **hold T** at night, Hari's phone status bar glows sodium orange, fading in over 0.25 s and out over 0.5 s.
  `ui/night_skip_driver.gd` sets `skip_amount` from `LoopState.fast_forward` and the phase, stepping by `delta`. The bar
  is now its own node (`ui/status_bar.gd`), so only it glows.
- **Marble deck** (`godot/shaders/deck_marble.gdshader`, `spatial`, written by Shriram with ChatGPT's help, disclosed in
  SOURCES.md): Poly Haven Marble 01 (CC0) as colour (`source_color`), roughness and an OpenGL normal map as data,
  world-XZ tiling, and 5 Inspector uniforms in 2 groups.
  - `materials/marble_dry.tres` (defaults) is on three deck floors.
  - `materials/marble_wet.tres` (roughness 0.3, specular 0.8: glossier) is on the strip at the pool's back edge.
- **Hint experiment:** `scenes/hint_experiment.tscn` shows one 3×1 grey strip (`tools/write_hint_strip.gd`) read with and
  without `source_color`. Captured 64/128/192 and 137/188/225, exactly as predicted.
- **Language notes:** [LANGUAGE-NOTES.md](LANGUAGE-NOTES.md), on `godot/shaders/standard_generated.gdshader`
  (a StandardMaterial3D converted in the editor; unused by the game).
- **Tests** (Godot on PATH; each writes `logs/<name>_<fps>fps.log`):
  ```bash
  ./scripts/run-test.sh test_night_skip.gd 30    # also 60 and 144: 33/33 each, real T presses, fades timed by delta
  ./scripts/run-test.sh test_materials.gd 60     # 156/156: hints, uniforms, materials, imports, formats, wiring
  ./scripts/run-test.sh normal_map_check.gd 60   # 11/11: curl-ratio convention check, calibrated on Floor Tiles 06
  ```
  Three mutations (deleted `;`, renamed uniform, removed `source_color`) each make their test exit 1. Results:
  [TEST-REPORT.md](TEST-REPORT.md), "Assignment 5".
- **Captures** (windowed, real renderer, scripted): `godot --path godot -s res://tools/capture_a5.gd -- <glow|hint|marble|sweep>`
  writes to `evidence/a5/` and prints measured pixels next to the predictions.
- **Docs:** [MATERIALS.md](godot/MATERIALS.md) (audit + review) · texture credits in
  [ATTRIBUTION.md](godot/assets/textures/marble_01/ATTRIBUTION.md).
- **A5 known limitations:**
  - Marble 01's normal map is very flat, so `normal_depth` barely changes the look (and the curl ratio is 0.637, not near 0).
  - The glow's on-screen contrast at full strength is 3.46:1. It passes 3:1, but it depends on the scene behind the
    semi-transparent bar.
  - The three A2 wall-clock tests still fail under `--fixed-fps` (unchanged, out of scope).
  - Opening the editor rewrites `project.godot`; this is restored after every session (TEST-REPORT A5.8).
- **Next step:** let the battery icon drain from orange to red as dawn approaches (Shriram's idea from the planning
  session), so the phone also warns how little night is left.
- **A5 film:** Brutalist `godot-gamedev` explainer (walker mode, Kokoro `am_onyx` "Liam" narration, local),
  3840×2160, 30 fps, **7:29**.
  - **Link (Northeastern OneDrive, added 2026-11-08 after tag `a5`):** [claude-liam-vidiyum-mun-a5-gamedev.mp4](https://northeastern-my.sharepoint.com/:v:/g/personal/azhagarasan_s_northeastern_edu/IQD90q52VjdmRJBluIZAo9vUAU37pY9d2Zg27ZZYxSRy7Yc?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=Utb4QS)
  - **File:** `claude-liam-vidiyum-mun-a5-gamedev.mp4` · **SHA-256:**
    `fb0d6a3800f34e313c3bd62bb0ad86bc43f766a50552657474c1d986ab196e46`
  - **Game-source revision shown:** `bb2c156`. Later commits change only docs and film records:
    `git diff bb2c156 a5 -- godot scripts` is empty.
  - **Film records:** [youtube/claude-liam-vidiyum-mun-a5-gamedev/](youtube/claude-liam-vidiyum-mun-a5-gamedev/): beat
    sheet, prompts, fact check, evidence and QC. `./art godot-gamedev --check` **PASS** (35 files, 7 exact excerpts, 7
    code→result pairs). Gate V on the final candidate: 0 BLOCKER, 0 MAJOR.
  - **Text-legibility gate (GATE T):** it flagged three beats where the "text" is inside real captures: petals and the
    orange bar in the `skip_amount = 2.0` capture, chairs in the playtest screenshot, and the light gizmo in the editor
    screenshot. Changing those pixels would alter the evidence, so the film was compiled directly. Approved by Shriram;
    reasons and boxed frames in `_qc/GATE-T-OVERRIDE.md`.
  - **Known flaws:** in B09 one code line is half cut off at the bottom of the code panel; B15's panel keeps the
    toolkit's fixed "GDD · DOCUMENT EXCERPT" label over shader lines (its subtitle says "Shader lines, verbatim").
  - **Revision 2 of the film (2026-11-01, ~20:20):** an independent grading pass found that B00 and B01 called all three
    shaders "hand-written", which overstated authorship (two were written with ChatGPT's help; see SOURCES.md). They
    now say "three shaders", and the B15 footer was un-clipped. The superseded export (SHA-256 `613d4ed5…af8`) is
    not the submitted film.

## Assignment 6: particle effects (tag `a6`)
Two particle effects added to the night slice (`scenes/slice.tscn`). Shriram's intent, values, predictions and budgets
are in [CHANGE-BRIEF.md](CHANGE-BRIEF.md), committed before the first build step. Every tuning revision, with its strips,
Claude's prediction and Shriram's verdict, is in [TUNING.md](TUNING.md).
- **Effect A, sand scuff on footsteps** (`effects/footstep_scuff.tscn`): two `CPUParticles3D`, SoftDust (10) and
  FineGrit (5), one-shot, 1.15 s.
  - **Event:** each foot contact while Hari walks. `effects/footstep_scuff_trigger.gd` reads Hari's walked distance
    (contact when `_travel / 0.42` crosses 2k + 0.5: one footfall per 0.84 m, about every 0.38 s at his 2.2 m/s walk) and
    never writes it. It never fires on load, while
    standing, in dialogue or while paused.
  - **Retrigger, overlap:** each footfall gets a new instance at Hari's floor position, freed after 1.15 s. At most 4
    are alive at once (60 particles).
- **Effect B, moths around the string lights** (`effects/string_light_moths.tscn`): three `GPUParticles3D` (12 each),
  each with a `GPUParticlesAttractorSphere3D`.
  - **Job:** ambience.
  - **Condition:** `LoopState.phase == NIGHT` and `clock_minutes < 1740` (before 5:00 AM).
    `effects/string_light_moths_controller.gd` polls it each frame and only reads game state.
  - **Features Effect A doesn't use:** turbulence, attractors, and a 2.4 s preprocess, so the group is already
    populated on its first frame.
  - **When the condition ends:** emission stops and the group is hidden 2.4 s later.
  - **Pause and hide:** pause freezes the moths. Hiding the group stops emission; showing it again restarts emission.
- **Textures:** procedural only.
  - The scuff uses `GradientTexture2D` resources inside the scene.
  - The moth is `effects/moth.png`, written by `tools/moth_texture.gd`. Regenerate it with
    `godot --headless --path godot -s res://tools/write_moth_texture.gd`.
- **Process shader:** `shaders/particles_generated.gdshader`, converted by Shriram in the editor from MothsWest's
  `ParticleProcessMaterial`; the game doesn't use it. Shriram's line references are in TEST-REPORT.md.
- **Tests** (`scripts/run-test.sh <file> <fps|realtime> [timeout]`, Godot on PATH; results in TEST-REPORT.md,
  "Assignment 6"):
  ```bash
  ./scripts/run-test.sh test_footstep_scuff_config.gd 60          # A: every emission/process/draw value read back
  ./scripts/run-test.sh test_footstep_scuff_trigger.gd 60         # A: real D/E/P keys; one scuff per footfall, overlap, never otherwise
  ./scripts/run-test.sh test_string_light_moths_config.gd 60      # B: turbulence, attractors, preprocess, draw, texture
  ./scripts/run-test.sh test_string_light_moths_controller.gd 60  # B: night/cutoff, pause, hide/show, real E/P/T keys
  ./scripts/run-test.sh cost_effects.gd 60 300                    # headless CPU price with an empty-scene control
  ./scripts/run-test.sh test_sound_triggers.gd realtime           # the three A2 wall-clock suites run in realtime mode
  ```
  Mutations: a Godot 3 name (`initial_velocity`) and a spread drift each make the configuration test exit 1.
- **Frame strips** (fixtures: the real slice, seeded, HUD hidden; a window opens):
  ```bash
  godot --path godot res://previews/footstep_scuff_preview.tscn --write-movie "$PWD/captures/x/frame.png" --fixed-fps 30 --quit-after 60 -- lit retrigger
  godot --path godot res://previews/string_light_moths_preview.tscn --write-movie "$PWD/captures/y/frame.png" --fixed-fps 30 --quit-after 150
  ```
  The kept strips are in `captures/footstep_scuff/` and `captures/string_light_moths/`.
- **Price** (TEST-REPORT A6.5–A6.6):
  - **Headless CPU:** Effect A at 4 bursts costs +13.2 µs per frame against the 0.15 ms budget. Effect B costs about 0,
    as expected for a GPU effect, because the headless renderer runs no particle process.
  - **GPU:** the Visual Profiler's GPU column read 0.0 ms on Metal / Apple M1 Pro, so GPU time could not be measured.
  - **FPS with vsync off:** about 280 with both effects off and 260–270 with both on, which is about 0.13–0.28 ms of
    whole-frame time (CPU and GPU together, not GPU time) for the two effects together. Whether each effect is within its
    0.20 ms budget is not confirmed.
- **A6 known limitations:**
  - GPU time per effect was not measured (see above).
  - The scuff lands at Hari's centre, which reads as behind his front foot. Shriram kept this (brief revision 3).
  - Stopping the game in the editor and pressing Play again "does not work" (Shriram's play check, TEST-REPORT A6.7). Not investigated.
  - Hari looks slightly above the floor: this is the A3 sprite and its shadow, out of scope for A6.
  - At r3 the moths read as pale grey, not the dark umber the r2 colour predicted (TUNING.md, Effect B).
  - The "Hari freed while the level persists" rule is not tested headless, because the slice itself needs Hari every
    frame.
  - Some Movie Maker strips stopped early when the window was closed; the kept frames are named in TUNING.md.
  - Opening the editor rewrites `project.godot` and `default_bus_layout.tres`; they were restored after every session.
- **A6 film:** Brutalist `godot-gamedev` explainer (walker mode, Liam narration), 3840×2160.
  - **Link (Northeastern OneDrive):** LINK-PENDING
  - **File:** `claude-liam-vidiyum-mun-a6-gamedev.mp4` · **SHA-256:** SHA-PENDING
  - **Game-source revision shown:** `52fa183`; `git diff 52fa183 a6 -- godot scripts` is empty

## Docs
[CONCEPT](CONCEPT.md) · [STORYBOARD](STORYBOARD.md) · [CHARACTER-SHEET](CHARACTER-SHEET.md) · [CHANGE-BRIEF](CHANGE-BRIEF.md) (A6; the earlier briefs are in [design/briefs/](design/briefs/)) · [TUNING](TUNING.md) · [DIALOGUE](DIALOGUE.md) · [ASSET-LOG](ASSET-LOG.md) · [SOURCES](SOURCES.md) · [FRICTIONAL](FRICTIONAL.md) · [TEST-REPORT](TEST-REPORT.md) · [MATERIALS](godot/MATERIALS.md) · [LANGUAGE-NOTES](LANGUAGE-NOTES.md) · my original story and decisions: [design/input/](design/input/)

## Known limitations
- **2.5D:** characters, the SUV and the backdrops are flat generated images in a 3D deck, so they read as cards when the camera turns. Natural character motion would need rigged 3D models. **Next step, written for A2:** build the SUV, the rock shrine and the fence as Blender models (done in A3).
- OVERHEAR's silhouette is close to IDLE. The walk cycle is a 4-frame swap (IDLE serves as the passing frame).
- The in-game camera doesn't reproduce the storyboard's special angles (see TEST-REPORT, section 4).
- Music (MusicGen) is CC-BY-NC: fine for coursework, not for a commercial release.
- Full list: [TEST-REPORT.md, section 9](TEST-REPORT.md).

## Film (Assignment 2)
Brutalist `godot-gamedev` explainer (walker mode, Liam narration), 3840×2160, 30 fps, **6:18**.
- **Link (Northeastern OneDrive):** [claude-liam-walker-vidiyum-mun-shriram-a-gamedev.mp4](https://northeastern-my.sharepoint.com/:v:/g/personal/azhagarasan_s_northeastern_edu/IQCsgk2bE-sbTo2EHyuUU-r5AQHG8865pDMU0TWLaO7khVw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=YVnmag)
- **File:** `claude-liam-walker-vidiyum-mun-shriram-a-gamedev.mp4` · **SHA-256:** `e948a875752d4e1f3745054ad4fc0921d9d2dfd81313ed0e5b832db8b06502fe`
- **Source revision shown:** `13f772c` (the game source is unchanged after it; later commits are docs and film records only)
- **Film records:** [youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev/](youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev/), containing the beat sheet, script and prompts (`PROMPTS.md`, `RIFF.md`), `FACTCHECK.md`, `SHOTLIST.md`, the evidence ledger (`gamedev-evidence.json`), capture logs, the capture driver and QC.
- `./art godot-gamedev --check` **PASS** (110 source files, 4 exact excerpts, 4 code→result pairs).
- **Text-legibility gate (GATE T):** it flagged small text that sits *inside* real game footage and reproduced generated images (the game's own HUD, raw generations, R1 screenshots), not the film's captions. The final compile ran the same `compile.py` step with every other gate on, and the reasons are documented in `youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev/_qc/GATE-T-OVERRIDE.md`.
