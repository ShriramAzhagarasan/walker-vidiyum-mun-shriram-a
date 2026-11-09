# Fact check: every number and claim in the narration and on screen, with its source

All paths are relative to the repo root; game source at git `52fa183` (`evidence/source-revision.txt`).

| Beat | Claim | Source |
|---|---|---|
| B00 | config 128/128, 255/255; state 19/19, 63/63; GPU time not measurable | `logs/test_footstep_scuff_config_60fps.log` (last line), `logs/test_string_light_moths_config_60fps.log`, `logs/test_footstep_scuff_trigger_60fps.log`, `logs/test_string_light_moths_controller_60fps.log`; TEST-REPORT.md:486-489 |
| B00 | prompt is an illustrative reconstruction | labelled on screen; real prompts in `prompts/a6/prompt-*.txt` |
| B02 | A fires once per footfall | CHANGE-BRIEF.md:237 (verbatim on screen) |
| B02 | B only in NIGHT and before 1740 (5:00 AM) | CHANGE-BRIEF.md:287-288 (verbatim); `godot/effects/string_light_moths_controller.gd:58-59` |
| B02 | 2 × CPUParticles3D one-shot; 3 × GPUParticles3D + 3 attractors; turbulence; preprocess 2.4 s | `godot/effects/footstep_scuff.tscn:70-130`; `godot/effects/string_light_moths.tscn:51-60,64-140` |
| B03 | amount 10, one_shot, box emission; spread 80; speed 0.25-0.65 m/s; gravity, damping, scale curve, colour ramp; quad 0.12 m; billboard | `footstep_scuff.tscn:74-97` (excerpt 74-86 on screen), `:20` billboard_mode 3, `:23` quad size |
| B04 | r0 strip: puff from file 9, gone by file 34 (trig+25) | TUNING.md:22-28 and the r0 row at TUNING.md:49 (2.2 at +25); `captures/footstep_scuff/r0-dark/` |
| B04 | Shriram: size decent, visible on dark floor, way too fast | TUNING.md:17-20 |
| B05 | reads `_travel`; a contact every 0.84 m (2 × 0.42); new instance per contact; freed after 1.15 s | `godot/effects/footstep_scuff_trigger.gd:9-12,34-46` (excerpt 37-46 on screen) |
| B05 | at most four alive (ceil(1.15/0.38)), 60 particles | CHANGE-BRIEF.md:251-257 |
| B06 | scripted capture: up to three alive at once | `evidence/walk_effects_frames.txt` (column scuffs_alive, max 3); `tools/capture_walk_effects.gd` |
| B06 | Shriram: "it stays for a while and then disappears, that is natural" | TEST-REPORT.md:504 |
| B06 | no scuff on load / dialogue / idle / paused; exactly one per contact; 19/19 | `logs/test_footstep_scuff_trigger_60fps.log` (lines on screen); TEST-REPORT.md:444-451 |
| B07 | alpha 0.18→0.30 at 50 %, 0→0.15 at 70 %; Claude proposed, Shriram approved; lifetime unchanged | TUNING.md:34-37; CHANGE-BRIEF.md:735-738; `footstep_scuff.tscn:31-33` |
| B08 | predicted "about twice"; measured 1.36×; lasts ~1.0 s vs 0.67 s; stacked alpha; verdict keep | TUNING.md:39-65 |
| B09 | gradient alpha 1.0/0.4/0 at 0/0.6/1 → 0.85/0.3/0 at 0/0.45/1 | TUNING.md:86-87; `footstep_scuff.tscn:3-13` |
| B10 | cotton balls; back-leg position kept as a limitation; predicted a third to a half; measured 13-14 %; soft blobs; verdict | TUNING.md:75-106; CHANGE-BRIEF.md:745-746 |
| B11 | 12 per emitter × 3; lifetime 2.4; preprocess 2.4; attractor radius 1.0, strength 0.3 | `string_light_moths.tscn:68-81` (excerpt 69-81 on screen), `:83-89` attractor |
| B12 | "Claude's difference image found moths at all three spans from the first active frame": stated as Claude's reading, not as fact (narration revised 2026-11-08 ~21:05 at Shriram's request) | TUNING.md:122 (Claude's reading of r0) |
| B12 | "do you see dots there"; 1-3 px specks; pale villa wall, not dark sky | TUNING.md:117-127 |
| B13 | quad 0.07×0.045 → 0.21×0.135 m; ramp cream → umber; Claude proposed, Shriram approved | TUNING.md:129-130,147-148; `string_light_moths.tscn:12-14` (on screen), `:24-26` and CHANGE-BRIEF.md:749-751 (verbatim still `evidence/table_b_r2.png`) |
| B14 | r1: wing dots zoomed, still invisible live; r2 predicted dark shapes; came out faint grey smudges; prediction failed | TUNING.md:132-158 |
| B15 | Step 5 agent wrote the generator; squared falloff; 16 of 2560 texels > 0.8 alpha; r3 smoothstep | TUNING.md:160-169; commit `d5d60fb` (Step 5 agent build); `godot/tools/moth_texture.gd:31-35` |
| B16 | 794 texels; changed px at file 29 1379 → 5108; pale grey not dark; "it reads as moths" | TUNING.md:168,174-184 |
| B17 | attractor interaction; turbulence strength 0.45, scale 5, influence 0.12-0.30; CPU particles lack them | `string_light_moths.tscn:45-58` (excerpt 45-57 on screen); CHANGE-BRIEF.md:58 (§0: CPUParticles3D has no turbulence or attractor) |
| B18 | fixture capture made for the film; condition ends at frame 70; fade | `tools/run_captures.sh`; `godot/previews/string_light_moths_preview.gd:2-10`; capture `capture/moths_r3_preview.avi` |
| B19 | restart on edges; emitting only; hide after 2.4 s; reads LoopState | `string_light_moths_controller.gd:44-59` (excerpt 44-56 on screen) |
| B20 | 63/63; P freezes; hidden stops, shown restarts; T to 1740 stops then hides after 2.4 s | `logs/test_string_light_moths_controller_60fps.log` (lines on screen); TEST-REPORT.md:458-462 |
| B20 | Shriram: "they stay exactly where we paused" | TEST-REPORT.md:508 |
| B21 | Shriram converted and saved the shader in the editor | commit `9e7edec`; CLAUDE.md ownership note |
| B21 | line 232 mixes initial_linear_velocity_min/max; brief 0.06 / 0.28 | `godot/shaders/particles_generated.gdshader:10-11,232`; `string_light_moths.tscn:36-37` |
| B21 | line 434 turbulence mix by influence 0.12-0.30 | `particles_generated.gdshader:236,434`; `string_light_moths.tscn:57-58` |
| B21 | line 399 force = gravity; gravity (0,0,0) | `particles_generated.gdshader:399`; `string_light_moths.tscn:42` |
| B22 | A 128 checks, B 255 | config logs, last lines |
| B23 | M1: initial_velocity → initial_velocity_min reads 0.0, no load error, effect still fired, exit 1; M2 spread 30, exit 1 | `logs/a6-mutations/m1_godot3_name.log`, `m2_value_drift.log`; TEST-REPORT.md:434-440 |
| B24 | control 5.8 µs; A +13.2 µs; B +3.3 µs within noise; n = 300; budget 0.15 ms | `logs/cost_effects_60fps.log`; TEST-REPORT.md:466-479; CHANGE-BRIEF.md:671 |
| B24 | dummy renderer runs no GPU particle process | TEST-REPORT.md:478-479 |
| B24 | profiler GPU 0.0 ms every row, Metal, M1 Pro; not measurable; vsync off ~280 vs 260-270 fps; 0.13-0.28 ms both; not confirmed | TEST-REPORT.md:481-496; `evidence/a6/use-it/visual-profiler-*.png` |
| B25 | Step 1: error_max_turns 41/40; draft 124 lines > 120 | commit `41302d8`; `prompts/a6/session-1.jsonl` result event |
| B25 | Step 2 preview: reconstructed background, no fixed seed | commit `a17cc65` |
| B25 | ">= 3 scuffs" could not catch a double fire; exact check added | commit `c9a07cd`; TEST-REPORT.md:446-447 |
| B25 | moth texture mostly haze | TUNING.md:160-164 |
| B25 | plan called ambience a "feedback loop", drove amount_ratio; correction "emitting only" | `prompts/a6/session-6a.jsonl` line 32 ("feedback loop drives `amount_ratio` only"); `prompts/a6/prompt-6b.txt:2` |
| B25 | permission denials 1 · 4 · 5 · 16 · 1 · 4 (sessions 1, 2, 3b, 5, 6a, 6b) | result events in `prompts/a6/session-*.jsonl` |
| B25 | Claude overruled: r0 too fast; cotton balls from play; moths unseen three times | TEST-REPORT.md:513-520 |
| B26 | authorship (incl. ChatGPT helped plan the effect settings, SOURCES.md:154-155, added in commit 0d351c7 during this build) | CHANGE-BRIEF.md:3-11; SOURCES.md:147-160; commit messages ("approved by Shriram", "captured by Shriram") |
| B26 | all textures procedural; no external art | `footstep_scuff.tscn:3-13,35-45` (GradientTexture2D); `godot/tools/moth_texture.gd`; CHANGE-BRIEF.md:213,487 |
| B27 | Stop + Play again failed for the moths, not investigated | TEST-REPORT.md:507 |
| B27 | scuff lands at Hari's centre | CHANGE-BRIEF.md:745-746 |
