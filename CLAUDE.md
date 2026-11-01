# CLAUDE.md

## Project context

- **Engine:** Godot 4.7.2.stable.official, macOS (`README.md:4`; feature `"4.7"` at `godot/project.godot:16`).
- **Renderer:** Forward+ (`godot/project.godot:38`). **Main scene:** `res://scenes/intro.tscn` (`project.godot:15`);
  the A5 effects live in the gameplay scene `res://scenes/slice.tscn` (root `Slice`, a `Node3D`).

### Part 1 shaded object (phone status bar)

- *(Updated 2026-11-01 for A5.)* Drawn by `HUD/StatusBar`, a `Control` with `res://ui/status_bar.gd`
  (`godot/scenes/slice.tscn:274`), material `materials/night_skip.tres`. The bar is `status_bar.gd:32-39`
  (background `:32`, clock `:33`, signal `:34-35`, battery `:36-38`, "loop N" `:39`).
- Its child `NightSkipDriver` (`slice.tscn:283`, `godot/ui/night_skip_driver.gd`) sets `skip_amount`. `HUD/HUD`
  (`hud.gd`) still draws ">> x8" (`hud.gd:31`), the mute icons and the talk hint.

### Game state that drives the night-skip shader

- `LoopState.fast_forward` (`godot/autoload/loop_state.gd:43`; autoload at `project.godot:20`; used by the clock at
  `loop_state.gd:58-59`), combined with `phase == Phase.NIGHT` (enum `loop_state.gd:18`).
- Written every frame from the `fast_forward` action by `Controls` (`godot/autoload/controls.gd:27`), which stops
  updating it while paused (`controls.gd:25-26`).

### Part 2 textured shader (deck floors)

- *(Updated 2026-11-01 for A5.)* `MeshInstance3D` nodes under `Slice/Deck` in `godot/scenes/slice.tscn`.
  - **Dry marble** (`material_override = marble_dry.tres`): `FloorWest` (`:99`), `FloorEast` (`:104`), `FloorFront` (`:114`).
  - **Wet marble** (`marble_wet.tres`): `FloorBack` (`:109`).
  - Both materials use `godot/shaders/deck_marble.gdshader` and replace the old `textured_surface.gd` StandardMaterial3D.

### Tests (all through `scripts/run-test.sh`)

`scripts/run-test.sh <file.gd> <fps>` runs
`godot --headless --path godot --script res://tests/<file> --fixed-fps <fps>`
with a 120 s timeout, tees to `logs/<name>_<fps>fps.log`, and exits 1 on
`SHADER ERROR` or `SCRIPT ERROR` (`scripts/run-test.sh:1-9`).

Current A2/A3 tests in `godot/tests/`, with the baseline counts (commit `18cdc12`, `logs/`):

```bash
scripts/run-test.sh test_assets_present.gd 60   # 70/70 PASS
scripts/run-test.sh test_audio_mix.gd 60        # 10/10 PASS
scripts/run-test.sh test_sound_triggers.gd 60   # 53/86 FAIL under --fixed-fps (86/86 unpinned)
scripts/run-test.sh test_loop_logic.gd 60       # 4/36 FAIL under --fixed-fps (36/36 unpinned)
scripts/run-test.sh test_slice_smoke.gd 60      # 4/13 FAIL under --fixed-fps (13/13 unpinned)
scripts/run-test.sh check_a3_assets.gd 60       # 31/31 PASS
scripts/run-test.sh check_a3_selftest.gd 60     # 17/17 PASS
```
`harness.gd` is the shared base class, and `a3_measure.gd` and `capture_a3.gd` are helpers: none of them is a test.

### Headless facts (confirmed on this machine)
- `godot` on PATH is a symlink, `/opt/homebrew/bin/godot` → `~/Downloads/Godot.app/Contents/MacOS/Godot`
  (4.7.2.stable.official.ed1daf0bf). The README's `/Applications` path is wrong for this machine.
- `timeout` is GNU coreutils at `/opt/homebrew/bin/timeout`. Exit status 124 means the test hung.
- `--fixed-fps` runs headless faster than real time. Code that measures wall-clock time (`Story._now()`,
  `godot/autoload/story.gd:203`) breaks under it, which is why three baseline tests fail only through the wrapper.
  New A5 code and tests must use frame `delta`, never `Time.get_ticks_msec()`.
- A headless run uses a dummy renderer that draws nothing. It can show that a shader parses (`SHADER ERROR`
  lines, `get_shader_uniform_list()`), but **not** how anything looks, and it doesn't report uniform defaults
  (read them from the `.gdshader` text). Never add `--rendering-driver`. Every visual rule ends in a human check.

New A5 tests (`CHANGE-BRIEF.md` §1.7, §2.6) run through the same wrapper: the driver test at 30, 60 and 144.

## Current change

@CHANGE-BRIEF.md

## Ownership

Files in `godot/shaders/` are hand-written by Shriram. An agent must
never create, edit, or rewrite any `.gdshader` file (including both A5
shaders and the hint-experiment shader) or the one `COLOR` line inside
`fragment()`. Agent sessions must leave `git diff --stat godot/shaders/`
empty. The hand-computed pixel predictions, hint-experiment predictions,
colour line, and Part 3 short answers inside `CHANGE-BRIEF.md` are also
Shriram's and are not rewritten by an agent.

## Out of scope

The A5 change must not touch:

- Movement, input mapping, or `Controls` (`godot/autoload/controls.gd`).
- `LoopState` logic, timings, or the night clock rate
  (`godot/autoload/loop_state.gd`), and `Story` logic
  (`godot/autoload/story.gd`). Presentation code may read `LoopState`;
  it never writes it.
- Any existing test under `godot/tests/` or its expectations.
- Any other HUD element — mute icons, talk hint, toasts, dialogue,
  white-out, screen cards — or any 3D object other than the four deck
  floor planes named above.
- The known A2 wall-clock limitation in `Story._now()`
  (`godot/autoload/story.gd:203`) stays as-is.
- `godot/project.godot` renderer, display, and autoload settings.
- Source model and texture files (`godot/assets/models/*.glb`, `godot/assets/art/`, downloaded texture PNGs).
  Their `.import` settings may change only as `CHANGE-BRIEF.md` §2.2 specifies.
- `scripts/run-test.sh`: diff it in every review.

## Unconfirmed

- No `AGENTS.md` exists at the repository root.
- *(Updated 2026-11-01.)* The A5 files now exist. New tests: `test_night_skip.gd` (30/60/144: 33/33),
  `test_materials.gd` (156/156), `normal_map_check.gd` (11/11); results in TEST-REPORT.md "Assignment 5".
- Opening the editor rewrites `project.godot`, `default_bus_layout.tres` and the scenes. Restore them with git after
  every editor session (TEST-REPORT A5.8).
