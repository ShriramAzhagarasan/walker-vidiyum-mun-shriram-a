extends "res://tests/harness.gd"
## A5 night-skip glow (CHANGE-BRIEF.md §1.3–1.5). Loads the real slice, drives the state only through real
## key presses (T to fast-forward, P to pause, E to close Amma's call), and samples skip_amount every frame
## from a node with a high process_priority, so it reads after every other _process() in the frame.
## Durations are game time: the sum of the frames' process deltas, as the driver sees them.
## Run at 30, 60 and 144:  ./scripts/run-test.sh test_night_skip.gd <fps>
## Headless draws nothing: this proves parsing, the uniform contract and the driven values, never the look.

const SHADER_PATH := "res://shaders/night_skip.gdshader"
const MATERIAL_PATH := "res://materials/night_skip.tres"
const FADE_IN := 0.25
const FADE_OUT := 0.5
## Name -> [Variant type from get_shader_uniform_list(), type in the source, hint in the source, default in the source]
const UNIFORMS := {
	"skip_amount": [TYPE_FLOAT, "float", "hint_range(0.0, 1.0)", "0.0"],
	"skip_tint": [TYPE_COLOR, "vec4", "source_color", "vec4(1.0, 0.6, 0.2, 1.0)"],
	"tint_strength": [TYPE_FLOAT, "float", "hint_range(0.0, 1.0)", "0.5"],
}

class Sampler extends Node:
	var material: ShaderMaterial
	var loop_state: Node
	var samples: Array = []      ## per frame: {v, state, dt, paused, phase}

	func _ready() -> void:
		process_priority = 1000
		process_mode = Node.PROCESS_MODE_ALWAYS

	func _process(delta: float) -> void:
		samples.append({
			"v": float(material.get_shader_parameter(&"skip_amount")),
			"state": loop_state.fast_forward and loop_state.phase == loop_state.Phase.NIGHT,
			"dt": delta,
			"paused": get_tree().paused,
			"phase": loop_state.phase,
		})

var sampler: Sampler
var frame_s := 0.0      ## one frame period at time_scale 1 (1 / --fixed-fps)

func run() -> bool:
	check_source_and_uniforms()
	var slice: Node = load("res://scenes/slice.tscn").instantiate()
	root.add_child(slice)
	await steps(3)
	var bar := slice.get_node("HUD/StatusBar") as Control
	check_material_wiring(slice, bar)
	sampler = Sampler.new()
	sampler.material = bar.material as ShaderMaterial
	sampler.loop_state = ls
	root.add_child(sampler)
	await steps(5)
	frame_s = sampler.samples[-1].dt
	print("frame period: %.5f s (%.1f fps)" % [frame_s, 1.0 / frame_s])
	check("R1 0.0 before T", is_zero_approx(sampler.samples[-1].v), sampler.samples[-1].v)

	await rule_fade_in_out()
	await rule_retrigger_continue()
	await rule_release_mid_fade_in()
	await rule_time_scale()
	await rule_pause_freezes()
	await rule_other_phase()
	slice.queue_free()
	await steps(2)
	return true

# --- static contract: the shader text and its uniform list -------------------------------------------

func check_source_and_uniforms() -> void:
	var source := FileAccess.get_file_as_string(SHADER_PATH)
	check("shader source readable", source != "", SHADER_PATH)
	var re := RegEx.create_from_string("uniform\\s+(\\w+)\\s+(\\w+)\\s*:\\s*([^=;]+?)\\s*=\\s*([^;]+?)\\s*;")
	var declared := {}
	for m in re.search_all(source):
		declared[m.get_string(2)] = [m.get_string(1), m.get_string(3), m.get_string(4)]
	for uname in UNIFORMS:
		var want: Array = UNIFORMS[uname]
		check("source: %s %s : %s = %s" % [want[1], uname, want[2], want[3]],
			declared.get(uname, []) == [want[1], want[2], want[3]], declared.get(uname, "missing"))
	check("source: canvas_item, no sampler uniforms",
		source.contains("shader_type canvas_item;") and not source.contains("sampler2D"), source.get_slice("\n", 0))

	var shader: Shader = load(SHADER_PATH)
	var listed := {}
	for u in shader.get_shader_uniform_list():
		listed[u.name] = u.type
	check("uniform list has exactly 3 uniforms (empty means the shader failed to parse)", listed.size() == 3, listed)
	for uname in UNIFORMS:
		check("uniform list: %s is %s" % [uname, type_string(UNIFORMS[uname][0])],
			listed.get(uname, -1) == UNIFORMS[uname][0], type_string(listed.get(uname, TYPE_NIL)))

func check_material_wiring(slice: Node, bar: Control) -> void:
	var mat := bar.material as ShaderMaterial
	check("R8 StatusBar has the night-skip ShaderMaterial", mat != null and mat.resource_path == MATERIAL_PATH, mat)
	check("R8 that material uses the hand-written shader", mat != null and mat.shader != null and mat.shader.resource_path == SHADER_PATH, mat.shader if mat else null)
	var others := []
	for path in ["HUD/HUD", "HUD/NotesToast", "HUD/Dialogue", "HUD/Whiteout", "HUD/ScreenCards"]:
		var n := slice.get_node_or_null(path) as CanvasItem
		if n == null or n.material != null or n.use_parent_material:
			others.append(path)
	check("F3 no other HUD node carries a material (mute icons and talk hint stay untinted)", others.is_empty(), others)

# --- driven rules ----------------------------------------------------------------------------------

## Game time from samples[from] until the value first equals target (inclusive), or -1 if it never does.
func time_to(from: int, target: float) -> float:
	var t := 0.0
	for i in range(from, sampler.samples.size()):
		t += sampler.samples[i].dt
		if is_equal_approx(sampler.samples[i].v, target):
			return t
	return -1.0

## Index of the first sample at or after `from` whose state equals `state`.
func flip(from: int, state: bool) -> int:
	for i in range(from, sampler.samples.size()):
		if sampler.samples[i].state == state:
			return i
	return -1

func wait_value(cond: Callable, max_frames := 600) -> void:
	for i in max_frames:
		if cond.call(sampler.samples[-1].v):
			return
		await steps(1)

func within_frame(measured: float, expected: float, frame: float) -> bool:
	return measured >= 0.0 and absf(measured - expected) <= frame + 1e-4

func rule_fade_in_out() -> void:
	var start := sampler.samples.size()
	key(KEY_T, true)
	await wait_value(func(v: float) -> bool: return is_equal_approx(v, 1.0))
	await steps(10)
	var on := flip(start, true)
	var t_in := time_to(on, 1.0)
	check("R1 R2 R3 fade-in 0.0 -> 1.0 in 0.25 s ± one frame", within_frame(t_in, FADE_IN, frame_s), "%.4f s game time" % t_in)
	check("R1 holds 1.0 while T is held", is_equal_approx(sampler.samples[-1].v, 1.0), sampler.samples[-1].v)
	var release := sampler.samples.size()
	key(KEY_T, false)
	await wait_value(func(v: float) -> bool: return is_zero_approx(v))
	await steps(10)
	var off := flip(release, false)
	var t_out := time_to(off, 0.0)
	check("R1 R2 R3 fade-out 1.0 -> 0.0 in 0.5 s ± one frame", within_frame(t_out, FADE_OUT, frame_s), "%.4f s game time" % t_out)

func rule_retrigger_continue() -> void:
	key(KEY_T, true)
	await wait_value(func(v: float) -> bool: return is_equal_approx(v, 1.0))
	var release := sampler.samples.size()
	key(KEY_T, false)
	await wait_value(func(v: float) -> bool: return v <= 0.6)
	var repress := sampler.samples.size()
	key(KEY_T, true)
	await wait_value(func(v: float) -> bool: return is_equal_approx(v, 1.0))
	await steps(5)
	var on := flip(repress, true)
	var before: float = sampler.samples[on - 1].v
	var at: float = sampler.samples[on].v
	var step_in: float = sampler.samples[on].dt / FADE_IN
	check("R4 re-press mid-fade-out continues from the current value (no drop to 0)", at > before and before > 0.3, "%.4f -> %.4f" % [before, at])
	check("R4 turns around at the fade-in rate", absf((at - before) - step_in) < 1e-4, "step %.5f, expected %.5f" % [at - before, step_in])
	var biggest_drop := 0.0
	for i in range(flip(release, false) + 1, sampler.samples.size()):
		biggest_drop = maxf(biggest_drop, sampler.samples[i - 1].v - sampler.samples[i].v)
	check("R4 no frame drops more than one fade-out step", biggest_drop <= frame_s / FADE_OUT + 1e-4, "largest drop %.5f" % biggest_drop)
	var t_back := time_to(on, 1.0)
	check("R4 back to 1.0 in (1 - v) × 0.25 s ± one frame", within_frame(t_back, (1.0 - before) * FADE_IN, frame_s), "%.4f s from v=%.3f" % [t_back, before])
	key(KEY_T, false)
	await wait_value(func(v: float) -> bool: return is_zero_approx(v))
	await steps(5)

func rule_release_mid_fade_in() -> void:
	key(KEY_T, true)
	await wait_value(func(v: float) -> bool: return v >= 0.6)
	var release := sampler.samples.size()
	key(KEY_T, false)
	await wait_value(func(v: float) -> bool: return is_zero_approx(v))
	await steps(5)
	var off := flip(release, false)
	var peak: float = sampler.samples[off - 1].v
	var t_down := time_to(off, 0.0)
	check("R5 T released mid-fade-in turns around from the current value", sampler.samples[off].v < peak and peak < 1.0, "peak %.3f" % peak)
	check("R5 falls to 0 in v × 0.5 s ± one frame", within_frame(t_down, peak * FADE_OUT, frame_s), "%.4f s from v=%.3f (expected %.4f)" % [t_down, peak, peak * FADE_OUT])

func rule_time_scale() -> void:
	Engine.time_scale = 0.5
	await steps(2)
	var start := sampler.samples.size()
	key(KEY_T, true)
	await wait_value(func(v: float) -> bool: return is_equal_approx(v, 1.0))
	await steps(3)
	var on := flip(start, true)
	var frames := 0
	for i in range(on, sampler.samples.size()):
		frames += 1
		if is_equal_approx(sampler.samples[i].v, 1.0):
			break
	var game_t := time_to(on, 1.0)
	var real_t := frames * frame_s
	check("R6 time_scale 0.5: fade-in is still 0.25 s of scaled game time", within_frame(game_t, FADE_IN, frame_s * 0.5), "%.4f s" % game_t)
	check("R6 time_scale 0.5: fade-in takes 0.5 s of real frames ± one frame", within_frame(real_t, FADE_IN / 0.5, frame_s), "%d frames = %.4f s" % [frames, real_t])
	key(KEY_T, false)
	await wait_value(func(v: float) -> bool: return is_zero_approx(v), 1200)
	Engine.time_scale = 1.0
	await steps(3)

func rule_pause_freezes() -> void:
	key(KEY_T, true)
	await wait_value(func(v: float) -> bool: return v >= 0.4)
	await tap(KEY_P)                     # real pause key; T is still held
	await steps(2)
	var frozen_from := sampler.samples.size()
	await steps(30)
	var values := {}
	var all_paused := true
	for i in range(frozen_from, sampler.samples.size()):
		values[snappedf(sampler.samples[i].v, 1e-6)] = true
		all_paused = all_paused and sampler.samples[i].paused
	check("R7 tree is paused by the P key", all_paused, all_paused)
	check("R7 value frozen while paused (30 frames, one value)", values.size() == 1, values.keys())
	await tap(KEY_P)
	await wait_value(func(v: float) -> bool: return is_equal_approx(v, 1.0))
	check("R7 resumes after unpause and reaches 1.0", is_equal_approx(sampler.samples[-1].v, 1.0) and not paused, sampler.samples[-1].v)
	key(KEY_T, false)
	await wait_value(func(v: float) -> bool: return is_zero_approx(v))
	await steps(3)

## Hold T through the whole night: the dawn crash ends Phase.NIGHT, so the glow must fade out with T still held.
## Amma's call keeps the clock still, so close it first. Story._now() gates E presses on wall-clock time
## (the known A2 limitation), so wait real time between presses, as a player would.
func rule_other_phase() -> void:
	for i in 30:
		if not story.dialogue_active:
			break
		OS.delay_msec(400)
		await tap(KEY_E)
		await steps(2)
	check("Amma's call closed through real E presses", not story.dialogue_active, story.conversation_id)
	key(KEY_T, true)
	var deadline := 40000
	while ls.phase == ls.Phase.NIGHT and deadline > 0:
		if story.dialogue_active:
			OS.delay_msec(400)
			await tap(KEY_E)
		await steps(1)
		deadline -= 1
	check("reached the dawn crash with T held (real clock, ×8)", ls.phase == ls.Phase.CRASH, "phase %d, clock %.1f" % [ls.phase, ls.clock_minutes])
	var start := sampler.samples.size() - 1
	await steps(int(ceil((FADE_OUT + 0.1) / frame_s)))
	var in_crash := true
	for i in range(start, sampler.samples.size()):
		in_crash = in_crash and sampler.samples[i].phase == ls.Phase.CRASH
	check("R9 still in the crash phase with T held", in_crash and Input.is_key_pressed(KEY_T), in_crash)
	check("R9 glow faded to 0 outside Phase.NIGHT within 0.5 s", is_zero_approx(sampler.samples[-1].v), "%.3f" % sampler.samples[-1].v)
	key(KEY_T, false)
	await steps(2)
