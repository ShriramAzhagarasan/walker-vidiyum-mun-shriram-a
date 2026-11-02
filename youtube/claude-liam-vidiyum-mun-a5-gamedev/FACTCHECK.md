# Fact check: every number and claim in the narration, with its source

| Beat | Claim | Source |
|---|---|---|
| B00/B01 | three shaders (no authorship claim in these beats; "hand-written" removed 2026-11-01 because deck_marble and hint_experiment were written with ChatGPT's help) | `godot/shaders/night_skip.gdshader`, `deck_marble.gdshader`, `hint_experiment.gdshader` |
| B02 | T at night runs the clock ×8; events go unheard | CHANGE-BRIEF.md §1.1; GAME-BIBLE §7 |
| B02 | the state and the colour line | CHANGE-BRIEF.md lines 24 and 53 (verbatim on screen) |
| B02 | four deck floors: three dry, one wet | CHANGE-BRIEF.md §2.1, §2.4; `slice.tscn` material_override |
| B03 | canvas_item, three uniforms, colour line at line 8 | `godot/shaders/night_skip.gdshader` lines 1–9 (verbatim) |
| B04 | P1 at 1.0 predicted on screen (249, 197, 147), captured the same; all within 1 per channel; 2.0 gives pure orange, not clamped | TEST-REPORT.md A5.4 (rows on screen); `evidence/a5/glow_skip_*.png` |
| B05 | reads fast_forward during Phase.NIGHT; move_toward by delta; 0.25 s in, 0.5 s out | `godot/ui/night_skip_driver.gd` lines 8–9, 20–28 |
| B06 | 8 frames to full glow, 15 to fade at 30 fps | `evidence/glow_motion_frames.txt` (per-frame skip_amount from the movie-maker run) |
| B06 | fade-in 0.25 s within one frame at 30/60/144 (0.2667 / 0.2500 / 0.2500 s); fade-out 0.5 s | `logs/test_night_skip_{30,60,144}fps.log` (lines on screen) |
| B07 | one file, greys 64/128/192, two samplers, a bool | `godot/shaders/hint_experiment.gdshader` 5–15; `godot/tools/write_hint_strip.gd` |
| B08 | predicted 64/128/192 and 137/188/225; captured the same | CHANGE-BRIEF.md lines 202–205; TEST-REPORT.md lines 295–298 |
| B09 | source_color on albedo; roughness and normal map without; hint_normal; five ranged uniforms, two groups; world XZ UVs | `godot/shaders/deck_marble.gdshader` 4–16 and 25 |
| B10 | sweep observations (tile size clear, specular clear, roughness less, normal depth barely) | TEST-REPORT.md A5.7 ("Observed by Claude from the captures; checked by Shriram") |
| B11 | wet: same shader, same textures, roughness 0.3, specular 0.8; dry sets none | `godot/materials/marble_wet.tres` 8–14; `marble_dry.tres` |
| B12 | shader × 0.3 darkened all four floors; red tint on wet changed only the back strip; both undone | TEST-REPORT.md A5.8; `evidence/a5/human/checkA_*`, `checkB_*` |
| B13 | shader_type/render_mode lines 3–4; source_color on line 7; hint_roughness_normal on 19; range on normal_scale (20) | `godot/shaders/standard_generated.gdshader` 3–20; LANGUAGE-NOTES.md |
| B14 | camera and light added by the capture script; material as generated | `tools/capture_standard_sphere.gd` |
| B15 | gen :7 ≈ own :5; gen :19 ≈ own :11 | both files (verbatim on screen); LANGUAGE-NOTES.md Q6 |
| B16 | set-then-get raises no error for an undeclared name; test asserts the uniform list | `godot/tests/test_night_skip.gd` 83–90; TEST-REPORT.md A5.2 |
| B17 | m1: SHADER ERROR, 4 fail; m2: 2 fail, 22 rule checks pass; m3: material test fails; exit 1 each, restored | `logs/mutations/*.log` (lines on screen); TEST-REPORT.md A5.2 |
| B18 | CLAUDE.md draft: wrong floor lines, 2 tests missing | FRICTIONAL.md (CLAUDE.md review); commit `1ccf2ff` |
| B18 | audit: "~2700 K", finding B wrong, substring hint check; fixed by an assertion | godot/MATERIALS.md "Review"; commit `b8179c3` |
| B18 | audit agent tried git checkout ×2 and git restore ×1 on project.godot; all denied | `prompts/a5/session-3.jsonl` permission_denials; FRICTIONAL.md |
| B18 | Claude's own curl formula replaced by the course's | FRICTIONAL.md (2026-10-29 entry) |
| B03/B19 | night_skip.gdshader typed by Shriram; colour line from the brief, worked out with ChatGPT's help | coordinator wording 2026-11-01; SOURCES.md |
| B19 | deck_marble.gdshader and hint_experiment.gdshader: written by Shriram with ChatGPT's help (learning shaders for the first time), from Claude's slot outline | coordinator's final wording 2026-11-01 (`A5_AUTHOR_PART2`, `A5_AUTHOR_PART2_SPOKEN` in tools/author_sheet.py); SOURCES.md |
| B19 | Claude proposed options, organised the brief's prose, gave a slot outline for the Part 2 shaders; ChatGPT: prediction maths | SOURCES.md; FRICTIONAL.md |
| B19 | LANGUAGE-NOTES: Shriram's own words; an earlier draft was paraphrased by ChatGPT | coordinator wording 2026-11-01 (Shriram rewriting the answers in their own words); earlier draft: commit `bd1c458`, SOURCES.md |
| B19 | textures by Rob Tuytel, CC0; source revision `bb2c156` (spoken "B B two C one five six"): the last commit touching godot/ or scripts/; later commits are docs only (`git diff --stat bb2c156 HEAD -- godot scripts` empty) | `godot/assets/textures/marble_01/ATTRIBUTION.md`; `evidence/source-revision.txt` / `A5_FILM_REV` |
| B20 | curl 0.637; contrast 3.46:1; next step battery orange → red | TEST-REPORT.md A5.5, A5.4; README A5 "Next step" |
