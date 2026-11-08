# CLAUDE.md

## Project context

**Engine:** Godot 4.7.2.stable.official.ed1daf0bf, macOS (feature `"4.7"` at
`godot/project.godot:16`; `README.md:6`). **Renderer:** Forward+ (`project.godot:38`).
**Main scene:** `res://scenes/intro.tscn` (`project.godot:15`). Both A6 effects live in the
gameplay scene `res://scenes/slice.tscn` (root `Slice`, `Node3D` at `slice.tscn:78`).

**Effect A — Sand scuff on footsteps.** Two `CPUParticles3D` emitters (SoftDust, FineGrit)
under a `FootstepScuff` root, instanced per footfall. CPU, because the scuff only needs
gravity, damping, colour, and scale, and `CPUParticles3D` here has no `amount_ratio`,
turbulence, or attractor (CHANGE-BRIEF §0). Trigger owner: Hari, a `CharacterBody3D`
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

`harness.gd` is the shared base class; `a3_measure.gd`/`capture_a3.gd` are helpers, not
tests. New A6 tests (CHANGE-BRIEF §D) run through the same wrapper and must use frame
`delta`, never `Time.get_ticks_msec()`.

### Headless facts
`godot` on PATH: `/opt/homebrew/bin/godot` → `~/Downloads/Godot.app/Contents/MacOS/Godot`
(README's `/Applications` path is wrong here). `timeout` is GNU coreutils at
`/opt/homebrew/bin/timeout` (exit 124 = hung). Headless uses a dummy renderer:
`GPUParticles3D` isn't GPU-simulated. It can read `can_process()`, `emitting`, `visible`,
`amount`, `lifetime`, curves, materials — never the rendered picture; every visual rule
ends in a human check. Never add `--rendering-driver`.

## Current change

@CHANGE-BRIEF.md

## Ownership

Files in `godot/shaders/` are hand-written by Shriram. An agent must never create, edit, or
rewrite any `.gdshader` file (both A5 shaders and the hint-experiment shader) or the one
`COLOR` line in `fragment()`. Agent sessions leave `git diff --stat godot/shaders/` empty.
The A5 pixel predictions, hint-experiment predictions, colour line, and Part 3 short
answers in `CHANGE-BRIEF.md` are also Shriram's and aren't rewritten.

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

## Out of scope

The A6 change must not touch: Hari's movement, the 0.38 s footstep interval, collision, or
input (`godot/scenes/hari.gd`, `godot/autoload/controls.gd`, `godot/logic/input_setup.gd`,
`godot/logic/hari_spec.gd`); `LoopState` (`godot/autoload/loop_state.gd`) or `Story`
(`godot/autoload/story.gd`) logic, phases, or the night clock rate — read-only; any A5
shader (`godot/shaders/`) or A5 material (`godot/materials/marble_{dry,wet}.tres`,
`night_skip.tres`); `godot/scenes/deck_dressing.gd`, string-light positions, bulbs, or the
warm `OmniLight3D` — read-only for the moths; any existing test in `godot/tests/` or its
expectations; `scripts/run-test.sh` (diff in every review); the known A2 wall-clock
limitation in `Story._now()` (`story.gd:203`); any HUD element, dialogue, toast, white-out,
or 3D object other than the new effect scenes and the small trigger script that
instantiates Effect A; `godot/project.godot` renderer, display, physics, and autoload settings.

## Unconfirmed

- No `AGENTS.md` at the repository root. `godot/effects/` does not exist yet; it will be
  created when Effect A or B is first built.
- The A5 editor-rewrite caveat (`project.godot`, `default_bus_layout.tres`, scenes) is
  assumed to still apply to A6 editor sessions; restore with git after each session
  (TEST-REPORT A5.8).
- CHANGE-BRIEF §B.3 plans moth emitters at x = 8, 12, 16, between the pole x-values
  (6, 10, 14, 18) from `deck_dressing.gd:11`, not on the bulbs; the brief flags this for a
  re-check before building.
