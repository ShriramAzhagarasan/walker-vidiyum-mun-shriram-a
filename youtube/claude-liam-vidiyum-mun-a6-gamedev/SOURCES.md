# Sources and provenance

Game source shown: git `52fa183`, the last commit touching godot/ or scripts/ (`git log -1 --format=%h -- godot scripts`,
recorded in `evidence/source-revision.txt`); godot/ content snapshot in beat_sheet.json `metadata.game.build_id`.
The working tree had uncommitted editor rewrites of `godot/project.godot` and `godot/default_bus_layout.tres` before
this film started; the film did not touch them (diff hash identical before and after the captures:
`_qc/pre-capture-gitdiff.txt`).

## Engine evidence
| File | Label in film | How it was made |
|---|---|---|
| `captures/footstep_scuff/r*/`, `captures/string_light_moths/r*/` | FIXTURE, captured by Shriram | preview scenes in `godot/previews/` over the real level, Movie Maker 30 fps (TUNING.md) |
| `evidence/strip_*.png` | FIXTURE strips | `tools/make_media.py`: the real frames above, cropped and enlarged with LANCZOS, file numbers printed under each tile |
| `capture/walk_effects.avi` | SCRIPTED CAPTURE | `tools/capture_walk_effects.gd` (this film): real slice, D/P/A via `Input.parse_input_event`, Movie Maker 30 fps, windowed, no `--rendering-driver`; per-frame log `evidence/walk_effects_frames.txt` |
| `capture/moths_r3_preview.avi`, `capture/scuff_retrigger_dark.avi` | FIXTURE, captured for this film | `tools/run_captures.sh`: the repo's preview scenes, Movie Maker 30 fps, `--quit-after` (the scuff capture is not used in the cut) |
| `evidence/a6/**` | SHRIRAM'S OWN SCREENSHOT / CLAUDE'S ZOOM | Shriram's screenshots of the running preview / game / editor; `claude-*` images are Claude's zooms and texture renders made during tuning |
| `evidence/terminal_*.png`, `evidence/table_*.png` | HEADLESS / verbatim | `tools/make_media.py`: lines copied verbatim from `logs/` and rows from TUNING.md / TEST-REPORT.md, located by anchor |

## Who did what (A6)
- **Shriram:** chose both effects and the retrigger rule (from options Claude laid out); wrote CHANGE-BRIEF.md Parts A–H
  with ChatGPT's help on wording/structure and the Part G price predictions (SOURCES.md, Assignment 6); approved every
  tuning change; captured every strip; ran both mutations; gave every verdict and play check; generated and saved
  `particles_generated.gdshader` in the editor.
- **Claude Code** (scoped `claude -p` agent sessions, `prompts/a6/`, and an interactive session): brief §0, CLAUDE.md
  revision, effect scenes, previews, trigger and controller, tests, cost script, debug keys, strip readings and
  proposed changes. **This film** (scripts in `tools/`, narration text, the shader annotation in B21) is Claude's.
- **Textures:** all procedural (GradientTexture2D in `footstep_scuff.tscn`; the moth drawn by `godot/tools/moth_texture.gd`).
  No external art. **Voice:** Kokoro-82M `am_onyx` ("Liam"), local, $0.
