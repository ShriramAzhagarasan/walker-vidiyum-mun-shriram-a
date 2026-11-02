# Sources and provenance

Game source shown: git `bb2c156`, the last commit touching godot/ or scripts/ (later commits are docs only; recorded in `evidence/source-revision.txt`); godot/ content snapshot in beat_sheet.json `metadata.game.build_id`.

## Engine evidence (real renderer unless marked headless)
| File | What | How it was made | SHA-256 |
|---|---|---|---|
| `evidence/a5/glow_skip_0_0.png` | scripted capture | `godot/tools/capture_a5.gd` (windowed, values set from code) | `f5c207751c16d56a…` |
| `evidence/a5/glow_skip_0_5.png` | scripted capture | `godot/tools/capture_a5.gd` (windowed, values set from code) | `97cfdc4141b8df97…` |
| `evidence/a5/glow_skip_1_0.png` | scripted capture | `godot/tools/capture_a5.gd` (windowed, values set from code) | `860d0e86a0724c80…` |
| `evidence/a5/glow_skip_2_0.png` | scripted capture | `godot/tools/capture_a5.gd` (windowed, values set from code) | `0737aaa25a118de6…` |
| `evidence/a5/hint_quads.png` | scripted capture | `godot/tools/capture_a5.gd` (windowed, values set from code) | `873791912560a27b…` |
| `evidence/a5/marble_10pm_glow_on.png` | scripted capture | `godot/tools/capture_a5.gd` (windowed, values set from code) | `6c6a1072226c56b8…` |
| `evidence/a5/sweep_sheet.png` | scripted capture | `godot/tools/capture_a5.gd` (windowed, values set from code) | `e3d8247d01cecb35…` |
| `evidence/a5/human/checkA_shader_edit_x0.3_all_floors_dark.png` | Shriram's own screenshot | Godot editor / F5 playtest, 2026-11-01 | `38c44f03963d5a09…` |
| `evidence/a5/human/checkB_wet_tint_red_only_back_strip.png` | Shriram's own screenshot | Godot editor / F5 playtest, 2026-11-01 | `72dd3b94303adfab…` |
| `evidence/a5/human/checkC_playtest_T_held_x8.png` | Shriram's own screenshot | Godot editor / F5 playtest, 2026-11-01 | `c73531e3dc18e234…` |
| `youtube/claude-liam-vidiyum-mun-a5-gamedev/capture/glow_motion.avi` (not in git) | scripted motion capture | Godot movie maker, `tools/capture_glow_motion.gd`, T via Input.parse_input_event, 30 fps, 1280×720 | `5d386809b57bac25…` |
| `youtube/claude-liam-vidiyum-mun-a5-gamedev/evidence/glow_motion_frames.txt` | per-frame skip_amount of that run | same run | `b5501cde1fc77fbf…` |
| `youtube/claude-liam-vidiyum-mun-a5-gamedev/evidence/standard_generated_sphere.png` | scripted capture | `tools/capture_standard_sphere.gd` (camera + light added at runtime, nothing saved) | `c825ba3715ac1f6e…` |
| `logs/test_night_skip_30fps.log` | headless log (verbatim lines rendered in `evidence/terminal_*.png`) | `scripts/run-test.sh` | `925feda49bc08fe3…` |
| `logs/test_night_skip_60fps.log` | headless log (verbatim lines rendered in `evidence/terminal_*.png`) | `scripts/run-test.sh` | `97c6d587c5526ce3…` |
| `logs/test_night_skip_144fps.log` | headless log (verbatim lines rendered in `evidence/terminal_*.png`) | `scripts/run-test.sh` | `a5cab1e03687eb13…` |
| `logs/mutations/m1_semicolon_deleted_60fps.log` | headless log (verbatim lines rendered in `evidence/terminal_*.png`) | `scripts/run-test.sh` | `d065216cae535ec6…` |
| `logs/mutations/m2_uniform_renamed_60fps.log` | headless log (verbatim lines rendered in `evidence/terminal_*.png`) | `scripts/run-test.sh` | `87b1e5746ad15cdb…` |
| `logs/mutations/m3_source_color_removed_60fps.log` | headless log (verbatim lines rendered in `evidence/terminal_*.png`) | `scripts/run-test.sh` | `9ad9187e14f62f89…` |

## Textures (in the game, shown in the film)
- Marble 01 (`marble_01`) by Rob Tuytel, Poly Haven, CC0 1.0: <https://polyhaven.com/a/marble_01>.
- Floor Tiles 06 (`floor_tiles_06`) by Rob Tuytel, Poly Haven, CC0 1.0 (curl calibration only): <https://polyhaven.com/a/floor_tiles_06>.

## Tools
- Brutalist `godot-gamedev` skill, walker mode; Remotion scenes (ClaudeComposerAsk, BrutalistHesitantWriter,
  GodotDesignBoard, GodotDevWorkbench, ClaudeVerdictArtifact, ClaudeTitleOutro).
- Narration: Kokoro-82M (`am_onyx`, "Liam"), local, Apache-2.0, $0. No paid generation.
- Godot 4.7.2.stable.official.ed1daf0bf (Forward+, Metal), ffmpeg, Pillow (PT Mono, Lato; ✓ glyph from Arial Unicode).

## Who made the film
Claude Code (Claude Opus 5.5) wrote the beat sheet, script, capture scripts and media tools and rendered the film.
Shriram's work shown in it is labelled as theirs (shaders, predictions, screenshots, mutations); see the repo's SOURCES.md.
