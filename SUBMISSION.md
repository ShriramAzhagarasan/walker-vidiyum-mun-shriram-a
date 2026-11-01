# Submission

*(The A3 submission note is in git at tag `a3`.)*

- **Assignment:** Assignment 5 - Shaders, Materials, and the Godot Shading Language
- **Student:** Shriram Alagarasan (azhagarasan.s@northeastern.edu)
- **Project name:** walker-vidiyum-mun-shriram-a, *Vidiyum Mun* (விடியும் முன், "Before Dawn")
- **GitHub repository URL:** https://github.com/ShriramAzhagarasan/walker-vidiyum-mun-shriram-a
- **Git tag and submitted commit SHA:** tag `a5`. The submitted commit's SHA is given in the Canvas submission note,
  because a commit can't contain its own SHA.
- **Game-source revision shown in the film:** `FILL-AFTER-RENDER`. Later commits change only docs and film records;
  `git diff <that revision> a5 -- godot scripts` is empty.
- **Godot version, renderer, and operating system:** Godot 4.7.2.stable.official.ed1daf0bf · Forward+ · macOS 26.6.2
  (Apple M1 Pro)
- **Game state the shader from code communicates:** the night is being skipped. While the player holds **T** at night
  (`LoopState.fast_forward and LoopState.phase == Phase.NIGHT`), the clock runs ×8 and anything said meanwhile goes
  unheard. Hari's phone status bar glows sodium orange (`skip_amount` 0→1 in 0.25 s, 1→0 in 0.5 s, game time), so the
  player sees they are trading knowledge for time.
- **3D object and scene given the textured shader:** the four deck floor planes in the night slice
  (`godot/scenes/slice.tscn`).
  - `marble_dry.tres` is on `Deck/FloorWest`, `FloorEast` and `FloorFront`.
  - `marble_wet.tres` (glossier: `roughness_scale 0.3`, `specular_amount 0.8`) is on `Deck/FloorBack`, the strip at the
    pool's back edge.
  - Both use `godot/shaders/deck_marble.gdshader`.
- **Texture sources and licences:** Poly Haven **Marble 01** and **Floor Tiles 06** (calibration only) by Rob Tuytel, CC0
  1.0, <https://polyhaven.com/a/marble_01>, <https://polyhaven.com/a/floor_tiles_06>. The hint strip is written by
  `godot/tools/write_hint_strip.gd`. Credits: `godot/assets/textures/marble_01/ATTRIBUTION.md`, SOURCES.md.
- **Final film URL and filename:** `FILL-AFTER-UPLOAD`
- **Final film SHA-256:** `FILL-AFTER-RENDER`
- **Summary of my work:**
  - I chose the state, the object, the sodium-orange colour, both fade times, and the re-press, pause and time-scale
    rules. I also chose the marble, where it goes, and that the pool edge is wet (glossier).
  - I committed those choices, my colour line, my pixel and hint-experiment predictions and my short answers in
    CHANGE-BRIEF.md before any shader existed. I used ChatGPT to help with the prediction maths and the sRGB
    explanations (disclosed in SOURCES.md).
  - I hand-wrote `night_skip.gdshader`. I wrote `deck_marble.gdshader` and `hint_experiment.gdshader` with ChatGPT's help,
    since I'm learning shaders for the first time (disclosed in SOURCES.md).
  - I converted a StandardMaterial3D in the editor. I wrote LANGUAGE-NOTES.md, including the annotation of the generated
    shader, in my own words. An earlier draft was paraphrased by ChatGPT.
  - I ran all three mutations by hand and did the human checks: the shader edit changed all four floors, the material
    edit changed only the wet strip, and I playtested the glow and the seams.
  - Claude wrote the driver, the tests, the capture tool, the material wiring, the audit review and the film. A scoped
    agent wrote the audit. Every capture matched my predictions: the hint quads exactly, the glow within 1 per channel.
  - Full split in SOURCES.md and FRICTIONAL.md.
- **Known limitations:**
  - Marble 01's normal map is very flat: `normal_depth` barely shows, and the curl ratio (0.637) is direction-only.
  - The glow's real on-screen contrast at full strength is 3.46:1. It passes 3:1, but it depends on the scene behind the
    60 % bar.
  - The three A2 wall-clock tests still fail under `--fixed-fps`; this is unchanged and out of scope.
  - Opening the Godot editor rewrites `project.godot` and re-saves the scenes; these files were restored after every
    session (TEST-REPORT A5.8).
  - The captures are scripted: values set from code, tree paused.
- **Changed games since Assignment 2:** no.
