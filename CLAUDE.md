# CLAUDE.md

## Project context

- **Engine:** Godot 4.7.2.stable.official, macOS (`README.md:4`;
  `godot/project.godot:16` lists feature `"4.7"`).
- **Renderer:** Forward+ (`godot/project.godot:38`).
- **Main scene:** `res://scenes/intro.tscn` (`godot/project.godot:15`).
  The gameplay scene the A5 effects live in is `res://scenes/slice.tscn`
  (loaded from the intro; root node `Slice` is a `Node3D`).

### Part 1 shaded object (phone status bar)

- Drawn today by `HUD/HUD`, a `Control` with script `res://ui/hud.gd`,
  inside the `HUD` `CanvasLayer` of the slice
  (`godot/scenes/slice.tscn:278-287`).
- The status bar itself is the `draw_rect` / `draw_string` calls in
  `HUD._draw()` at `godot/ui/hud.gd:38-49` (bar background `:42`, clock
  text `:43`, signal bars `:44-45`, battery `:46-48`, "loop N" `:49`).
  `HUD._process()` (`hud.gd:25-36`) polls state and uses
  `LoopState.fast_forward and LoopState.phase == LoopState.Phase.NIGHT`
  at `hud.gd:26` for ">> x8" (`hud.gd:50-51`).
- Per `CHANGE-BRIEF.md` §1.2, the status bar moves into its own Control
  node for A5 so only that node gets the shader material.

### Game state that drives the night-skip shader

- Owned by `res://autoload/loop_state.gd` (autoloaded as `LoopState`,
  `godot/project.godot:20`). The state is `LoopState.fast_forward`
  (declared `loop_state.gd:43`, consumed by the clock tick `:58-59`)
  combined with `LoopState.phase == LoopState.Phase.NIGHT` (enum
  `loop_state.gd:18`).
- `LoopState.fast_forward` is written every frame from the
  `fast_forward` input action by `Controls` at
  `godot/autoload/controls.gd:27`. `Controls` stops updating it while
  paused (`controls.gd:25-26`).

### Part 2 textured shader (deck floors)

- 3D objects: `MeshInstance3D` nodes under `Slice/Deck` in
  `godot/scenes/slice.tscn`:
  - **Dry marble:** `FloorWest` (`slice.tscn:100-105`), `FloorEast`
    (`:107-113`), `FloorFront` (`:121-127`).
  - **Wet marble:** `FloorBack` (`:114-120`).
- Today each has `res://scenes/textured_surface.gd` attached, which
  builds a `StandardMaterial3D` in code at
  `godot/scenes/textured_surface.gd:18-39` from
  `res://assets/art/env/marble.png` and assigns it as
  `material_override` (`textured_surface.gd:39`).
- Per `CHANGE-BRIEF.md` §2.1, §2.4, A5 replaces this with
  `godot/materials/marble_dry.tres` (FloorWest/East/Front) and
  `godot/materials/marble_wet.tres` (FloorBack), both backed by
  `godot/shaders/deck_marble.gdshader`.

### Tests (all through `scripts/run-test.sh`)

`scripts/run-test.sh <file.gd> <fps>` runs
`godot --headless --path godot --script res://tests/<file> --fixed-fps <fps>`
with a 120 s timeout, tees to `logs/<name>_<fps>fps.log`, and exits 1 on
`SHADER ERROR` or `SCRIPT ERROR` (`scripts/run-test.sh:1-9`).

Current A2/A3 tests in `godot/tests/`:

```bash
scripts/run-test.sh test_assets_present.gd 60
scripts/run-test.sh test_audio_mix.gd 60
scripts/run-test.sh test_sound_triggers.gd 60
scripts/run-test.sh test_loop_logic.gd 60
scripts/run-test.sh test_slice_smoke.gd 60
```

The new A5 tests specified in `CHANGE-BRIEF.md` §1.7 and §2.6 (e.g. for
`skip_amount` at 30/60/144 fps, uniform-list assertions, material/import
assertions) run through the same wrapper with the matching fps argument.

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

## Unconfirmed

- No `AGENTS.md` exists at the repository root.
- The A5 shaders (`godot/shaders/night_skip.gdshader`,
  `deck_marble.gdshader`, `hint_experiment.gdshader`), materials
  (`godot/materials/marble_dry.tres`, `marble_wet.tres`), textures under
  `godot/assets/textures/marble_01/`, and the generator
  `godot/tools/write_hint_strip.gd` are specified in `CHANGE-BRIEF.md`
  but do not exist yet. The new A5 test scripts named in §1.7 and §2.6
  do not exist yet either; only the five A2/A3 tests above are present.
