# CLAUDE.md

## Project context

**Engine:** Godot 4.7.2.stable.official.ed1daf0bf, macOS (feature `"4.7"` at
`godot/project.godot:16`; `README.md:6`). **Renderer:** Forward+ (`project.godot:38`).
**Main scene:** `res://scenes/intro.tscn` (`project.godot:15`). Both A6 effects live in the
gameplay scene `res://scenes/slice.tscn` (root `Slice`, `Node3D` at `slice.tscn:78`).

**Effect A — Sand scuff on footsteps.** Two `CPUParticles3D` emitters (SoftDust, FineGrit)
under a `FootstepScuff` root, one instance per footfall (overlap, CHANGE-BRIEF §A.3-A.4). Trigger owner: Hari, a `CharacterBody3D`
(`slice.tscn:236`, `godot/scenes/hari.gd`). Walked distance in `hari.gd:11,69,72`
(`STRIDE_M = 0.42`, `_travel += speed * delta`); foot contact at `_travel / STRIDE_M` = 2k + 0.5
(`hari.gd:74-75`), ~0.38 s at `WALK_SPEED = 2.2` (`godot/logic/hari_spec.gd:4,7`).
**No footstep signal exists today** — the trigger must detect contact crossings itself.
Gate on `Story.hari_state == "WALK"` (`godot/autoload/story.gd:25,60`) and
`Story.movement_locked()` (respected at `hari.gd:43`); pause = tree pause set by `Controls`
on `pause` (`godot/autoload/controls.gd:19-20`; `godot/logic/input_setup.gd:13`).

**Effect B — Moths around the string lights.** Three `GPUParticles3D` emitters using a
`ParticleProcessMaterial`, each paired with a `GPUParticlesAttractorSphere3D`. Chosen for
`turbulence_*` and attractor interaction, which `CPUParticles3D` lacks here (CHANGE-BRIEF §0).
String lights (poles, bulbs, warm `OmniLight3D` per span) are built by
`godot/scenes/deck_dressing.gd:11-13,42-46`, attached from `slice.tscn:91`. Condition owner:
`LoopState.phase == Phase.NIGHT` (enum `godot/autoload/loop_state.gd:18`) and
`LoopState.clock_minutes < 1740` (sky-lighten threshold `godot/scenes/slice.gd:28`; clock
written at `loop_state.gd:59`). **No signal fires at minute 1740** — the controller must
poll each frame. Pause = tree pause.

### Tests (all through `scripts/run-test.sh`)

`scripts/run-test.sh <file.gd> <fps|realtime> [timeout-seconds]` runs
`godot --headless --path godot --script res://tests/<file>`, adds `--fixed-fps <fps>` when
`$2` is numeric and omits it when `$2` is `realtime`; tees to `logs/<name>_<fps|realtime>.log`
and exits 1 on `SHADER ERROR`/`SCRIPT ERROR` (`scripts/run-test.sh:1-14`; default timeout 120 s).
Baseline in `logs/a6-baseline/SUMMARY.txt`. The three wall-clock A2 tests need `realtime`;
the rest pass at any fps.

```bash
scripts/run-test.sh test_assets_present.gd 60        # A2  70/70
scripts/run-test.sh test_audio_mix.gd 60             # A2  10/10
scripts/run-test.sh test_sound_triggers.gd realtime  # A2  86/86 wall-clock (53/86 at --fixed-fps 60)
scripts/run-test.sh test_loop_logic.gd realtime      # A2  36/36 wall-clock (4/36  at --fixed-fps 60)
scripts/run-test.sh test_slice_smoke.gd realtime     # A2  13/13 wall-clock (4/13  at --fixed-fps 60)
scripts/run-test.sh check_a3_assets.gd 60            # A3  31/31
scripts/run-test.sh check_a3_selftest.gd 60          # A3  17/17
scripts/run-test.sh test_night_skip.gd 30            # A5  33/33 (also at 60 and 144)
scripts/run-test.sh test_materials.gd 60             # A5  156/156
scripts/run-test.sh normal_map_check.gd 60           # A5  11/11
```

`harness.gd` is the base class; `a3_measure.gd`/`capture_a3.gd` are helpers. New A6 tests
(CHANGE-BRIEF §D) use the same wrapper and frame `delta`, never `Time.get_ticks_msec()`.

### Headless facts
`godot` on PATH: `/opt/homebrew/bin/godot` → `~/Downloads/Godot.app/Contents/MacOS/Godot`
(README's `/Applications` path is wrong here). `timeout` is GNU coreutils at
`/opt/homebrew/bin/timeout` (exit 124 = hung). Never add `--rendering-driver`.
- A headless run uses a dummy renderer: it draws no particles and runs no GPU particle
  process. Node state (emitting, one_shot, amount_ratio, visibility, instance counts) is
  observable; the look is not. *(Confirmed 2026-11-08: empty video adapter name;
  `GPUParticles3D.capture_aabb()` stays zero-size after 30 emitting frames.)*
- A GPU effect's headless CPU price is near zero by construction.
- Frame strips come from a windowed Movie Maker run, which I start.

## Current change

@CHANGE-BRIEF.md

## Ownership

Files in `godot/shaders/` are hand-written by Shriram. An agent must never create, edit, or
rewrite any `.gdshader` file (both A5 shaders and the hint-experiment shader) or the one
`COLOR` line in `fragment()`. Agent sessions leave `git diff --stat godot/shaders/` empty.
Shriram's A6 brief text (Parts A–H), every prediction, every verdict and the process-shader
notes are Shriram's and aren't rewritten. `godot/shaders/particles_generated.gdshader` (Step 6)
is saved by Shriram from the editor; no agent creates or edits it.

**A6 particle effects** — every per-emitter setting (emission, process, draw, turbulence,
attractor) lives in scene files under `godot/effects/` (`.tscn` + the `.tres` they
reference), **not** in code. Scripts in `godot/effects/` may trigger, position, show, hide,
pause, and free those instances, and may read `LoopState`/`Story`, but must not construct
`ParticleProcessMaterial`, curves, or ramps programmatically — the values from CHANGE-BRIEF
§A.3 and §B.3 belong in the scene.

## Godot 4 names

Use Godot 4 names for 4.7.2, not Godot 3 names. If I'm unsure a property or enum exists
here, I say so instead of guessing.

- **`ParticleProcessMaterial`** (not `ParticlesMaterial`). Ranges are min/max pairs:
  `initial_velocity_min/_max`, `scale_min/_max`, `damping_min/_max`, `hue_variation_min/_max`.
  Setting the Godot 3 scalar `initial_velocity`/`scale` leaves the pair at 0 and the scene
  still loads silently (CHANGE-BRIEF §0). `scale_random` doesn't exist here.
- **`GPUParticles3D`** (`amount_ratio`, `use_fixed_seed`, `seed`, `preprocess`,
  `visibility_aabb`, `trail_enabled`, `sub_emitter`) vs **`CPUParticles3D`** (no
  `amount_ratio`, turbulence, or attractor). Attractor: **`GPUParticlesAttractorSphere3D`**
  (`radius`, `strength`, `attenuation`, `directionality`).
- **`StandardMaterial3D`**: `vertex_color_use_as_albedo`, `transparency`, `blend_mode`,
  `billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES` (= 3).
- **`Curve`** clamps points to `min_value..max_value` (default 0..1): a 1.3 point needs
  `max_value >= 1.3` (checked 2026-11-08).

## Out of scope

The A6 change must not touch: Hari's movement, the 0.38 s footstep interval, collision or input
(`hari.gd`, `controls.gd`, `input_setup.gd`, `hari_spec.gd`); `LoopState`/`Story` logic, phases or
clock rate (read-only); A5 shaders and materials; the string lights in `deck_dressing.gd` (read-only);
existing tests and their expectations; `scripts/run-test.sh` (diff it in every review);
`Story._now()` (`story.gd:203`); any HUD element or 3D object other than the new effect scenes
and their trigger/controller scripts; `project.godot` renderer, display, physics and autoloads.

## Unconfirmed

- No `AGENTS.md` at the repository root. `godot/effects/` doesn't exist until the first build.
- Editor sessions rewrite `project.godot`, `default_bus_layout.tres` and scenes; restore
  with git after each (TEST-REPORT A5.8). Assumed to still hold for A6.
- Whether a hidden `GPUParticles3D` keeps simulating in 4.7.2 is unconfirmed; B.4 stops
  emission explicitly when hidden, so tests assert `emitting`/`visible`, not GPU state.
