# Submission

*(Earlier submission notes are in git at tags `a3` and `a5`.)*

- **Assignment:** Assignment 6 - Creating Particle Effects with Godot and Claude
- **Student:** Shriram Alagarasan (azhagarasan.s@northeastern.edu)
- **Project name:** walker-vidiyum-mun-shriram-a, *Vidiyum Mun* (விடியும் முன், "Before Dawn")
- **GitHub repository URL:** https://github.com/ShriramAzhagarasan/walker-vidiyum-mun-shriram-a
- **Git tag and submitted commit SHA:** tag `a6`. The Canvas submission note gives the submitted commit's SHA, because a
  commit can't contain its own SHA.
- **Game-source revision shown in the film:** `52fa183`. Later commits change only docs and film records:
  `git diff 52fa183 a6 -- godot scripts` is empty.
- **Godot version, renderer, and operating system:** Godot 4.7.2.stable.official.ed1daf0bf · Forward+ (Metal) ·
  macOS 26.6.2
- **GPU used for the GPU price:** Apple M1 Pro (Apple7), integrated, in an editor Play run at 1278×719.
- **Effect A: event, node type, retrigger rule:**
  - **Event:** a sand scuff on each of Hari's footfalls while he walks. The trigger follows walked distance, not time.
    It fires when Hari's `_travel / 0.42` crosses 2k + 0.5, which is one footfall per 0.84 m. At his walk speed of
    2.2 m/s (`hari_spec.gd`) that is about every 0.38 s. It never fires on load, while he stands, during dialogue, or
    while the game is paused.
  - **Node type:** two `CPUParticles3D` (SoftDust 10, FineGrit 5) under one `FootstepScuff` root.
  - **Retrigger rule:** overlap. Each footfall gets a new instance, freed after 1.15 s, with at most 4 alive
    (60 particles).
- **Effect B: job, condition, node type, feature Effect A doesn't use:**
  - **Job:** ambience, moths around the deck's string lights.
  - **Condition:** `LoopState.phase == NIGHT and LoopState.clock_minutes < 1740` (before 5:00 AM).
  - **Node type:** three `GPUParticles3D` (12 each) with a `ParticleProcessMaterial`.
  - **Features Effect A doesn't use:** turbulence and a `GPUParticlesAttractorSphere3D` per emitter, plus a 2.4 s
    preprocess.
- **Budgets, and the price each is compared on:**
  - **Effect A:** budget ≤ 0.15 ms per frame of headless CPU, measured at +13.2 µs (4 bursts, against an empty-scene
    control), so within budget. Its GPU budget is ≤ 0.20 ms.
  - **Effect B:** budget ≤ 0.20 ms of GPU time. Its headless CPU price is about 0 by construction.
  - **GPU time:** under Metal the Visual Profiler's GPU column read 0.0 ms on every row. Under Vulkan
    (`--rendering-driver vulkan` as a run argument only) it reports times: whole-frame GPU 2.1–6.0 ms. In the one clean
    same-view pair (standing, set 2) effects on vs off differ by −0.04 ms, and the other standing pair gives +0.57 ms.
    Single frames vary more than the effects cost. The walking pairs changed camera view, so they give no figure for A
    (TEST-REPORT A6.6b).
  - **FPS with vsync off (F10):** about 280 with both effects off and 260–270 with both on. That is a change of about
    0.13–0.28 ms in whole-frame time (CPU and GPU together) for the two effects combined. It is an estimate of total
    frame-time change, **not GPU time**, and it can't be split per effect. The per-effect GPU budgets are therefore
    **not confirmed** (TEST-REPORT A6.5–A6.6).
- **Texture sources and licences:** procedural only, no external images.
  - The scuff uses `GradientTexture2D` resources inside `godot/effects/footstep_scuff.tscn`.
  - The moth silhouette `godot/effects/moth.png` is written by `godot/tools/moth_texture.gd` (an agent wrote it; Claude
    revised it at B r3).
  - The A5 marble textures (Poly Haven, CC0) are unchanged; their credits are in
    `godot/assets/textures/marble_01/ATTRIBUTION.md`.
- **Final film URL and filename:** https://northeastern-my.sharepoint.com/:v:/g/personal/azhagarasan_s_northeastern_edu/IQBrxjoQcIr2Q5C-1fTgM_91AUrknWszjWF3JATjHzR9XA4?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=5dr6ux · `claude-liam-vidiyum-mun-a6-gamedev.mp4` (3840×2160, 30 fps, 7:19; revision 2: B24 adds the Vulkan GPU result)
- **Final film SHA-256:** `e823205ef799c340a6f9b8289dd2fe038107ca0f95ad1e373af2b003ef99e547`
- **Summary of my work:**
  - **The brief:** I chose both effects and the overlap rule. I wrote CHANGE-BRIEF.md Parts A–H (intent, every value,
    the rules, the frame and failure predictions, the prices and budgets, and the six answers) before the first build
    step, with ChatGPT's help on the wording, the structure, planning the effect settings and the price predictions
    (SOURCES.md). After Claude's
    engine check I dictated seven corrections.
  - **Agent plans:** I approved the agents' plans with corrections, two for the trigger and three for the moth
    controller.
  - **Hands-on work:** I ran both mutations, captured every frame strip, and converted the process shader in the editor.
  - **Tuning:** I gave every tuning verdict from play. A r0, "way too fast", drove r1, and I overruled Claude's timing
    reading of that strip. My verdict on A r2 was "not like cotton balls", and on B r3 "it reads as moths".
  - **Play checks and the GPU price:** I did the play checks (pause, hide/show, dawn, darkest and lightest floor) and
    read the GPU price.
  - **My own writing:** the process-shader notes (after ChatGPT explained the shader to me) and my FRICTIONAL.md
    reflection (an earlier draft was ChatGPT-assisted).
  - **Claude's part:** Claude wrote §0 of the brief, the CLAUDE.md review, the prompts and reviews of the scoped agent
    sessions (`prompts/a6/`), the previews, the debug keys and the tuning proposals, and made the film (Brutalist `godot-gamedev`, Kokoro "Liam" narration).
    I watched the final export and approved the one text-gate override. The agents
    built the effect scenes, trigger, controller, tests and cost script. Full split in SOURCES.md and FRICTIONAL.md.
- **Known limitations:**
  - GPU time per effect wasn't resolved. Metal reported 0.0 ms. Vulkan single-frame readings vary more than the
    effects cost, and the FPS comparison gives only the whole-frame change (see Budgets).
  - The scuff lands at Hari's centre, so it reads as behind his front foot. I kept this.
  - Stopping the game in the editor and pressing Play again "does not work" (Shriram's play check, TEST-REPORT A6.7). Not investigated.
  - Hari looks slightly above the floor. That's the A3 sprite and shadow, out of scope.
  - The r3 moths read pale grey, not the predicted dark umber.
  - The "Hari freed while the level persists" rule is not tested headless.
  - Some strips stopped early when the capture window was closed.
  - The Godot editor rewrites `project.godot` and `default_bus_layout.tres`; they were restored after every session.
  - Headless tests prove configuration and state rules, not the look.
- **Changed games since Assignment 2:** no.
