# CLAUDE.md

## Project context

- **Engine:** Godot 4.7.2.stable.official, macOS (`README.md:4`; feature `"4.7"` at `godot/project.godot:16`).
- **Renderer:** Forward+ (`godot/project.godot:38`). **Main scene:** `res://scenes/intro.tscn` (`project.godot:15`);
  the A5 effects live in the gameplay scene `res://scenes/slice.tscn` (root `Slice`, a `Node3D`).

### Part 1 shaded object (phone status bar)

- Drawn today by `HUD/HUD`, a `Control` with `res://ui/hud.gd`, inside the `HUD` `CanvasLayer`
  (`godot/scenes/slice.tscn:278-287`). The bar is the `draw_rect`/`draw_string` calls in `HUD._draw()`
  (`godot/ui/hud.gd:38-49`: background `:42`, clock `:43`, signal `:44-45`, battery `:46-48`, "loop N" `:49`).
- `HUD._process()` (`hud.gd:25-36`) shows ">> x8" (`hud.gd:50-51`) on
  `LoopState.fast_forward and LoopState.phase == LoopState.Phase.NIGHT` (`hud.gd:26`).
- The status bar moves into its own Control node for A5 (`CHANGE-BRIEF.md` §1.2).

### Game state that drives the night-skip shader

- `LoopState.fast_forward` (`godot/autoload/loop_state.gd:43`; autoload at `project.godot:20`; used by the clock at
  `loop_state.gd:58-59`), combined with `phase == Phase.NIGHT` (enum `loop_state.gd:18`).
- Written every frame from the `fast_forward` action by `Controls` (`godot/autoload/controls.gd:27`), which stops
  updating it while paused (`controls.gd:25-26`).

### Part 2 textured shader (deck floors)

- `MeshInstance3D` nodes under `Slice/Deck` in `godot/scenes/slice.tscn`. **Dry marble:** `FloorWest` (`:94`),
  `FloorEast` (`:102`), `FloorFront` (`:118`). **Wet marble:** `FloorBack` (`:110`).
- Today each uses `res://scenes/textured_surface.gd`, which builds a `StandardMaterial3D` in code from
  `res://assets/art/env/marble.png` (`textured_surface.gd:18-39`) and sets it as `material_override` (`:39`).
- A5 replaces this with `godot/materials/marble_dry.tres` (West/East/Front) and `marble_wet.tres` (Back), both on
  `godot/shaders/deck_marble.gdshader` (`CHANGE-BRIEF.md` §2.1, §2.4).

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
- Everything A5 adds (the three shaders, the materials, the textures, `write_hint_strip.gd`, the new tests) is specified
  in `CHANGE-BRIEF.md` but doesn't exist yet. Only the seven A2/A3 tests above are present.
