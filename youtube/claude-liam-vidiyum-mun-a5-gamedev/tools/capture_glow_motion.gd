## SCRIPTED CAPTURE for the A5 film (not played by hand): the real slice, the real driver and shader, with T held
## and released through Input.parse_input_event, recorded frame by frame by Godot's movie maker.
##   godot --path godot --write-movie <out.avi> --fixed-fps 30 --resolution 1920x1080 -s <this file> -- <log.txt>
## Writes one line per frame: frame, T held, LoopState.fast_forward, phase, skip_amount (read from the material).
extends SceneTree

const PLAN := [["release", 20], ["hold", 30], ["release", 30], ["hold", 9], ["release", 24], ["hold", 30], ["release", 24]]
var log_lines := PackedStringArray()
var mat: ShaderMaterial
var ls: Node
var t_down := false
var frame := 0

func _initialize() -> void:
	_run()

func _key(code: Key, pressed: bool) -> void:
	var e := InputEventKey.new()
	e.keycode = code
	e.physical_keycode = code
	e.pressed = pressed
	Input.parse_input_event(e)

func _step(n: int, record := true) -> void:
	for i in n:
		await process_frame
		if record:
			log_lines.append("%d\t%s\t%s\t%d\t%.4f" % [frame, t_down, ls.fast_forward, ls.phase, float(mat.get_shader_parameter(&"skip_amount"))])
			frame += 1

func _run() -> void:
	var slice: Node = load("res://scenes/slice.tscn").instantiate()
	root.add_child(slice)
	ls = root.get_node("LoopState")
	var story := root.get_node("Story")
	mat = (slice.get_node("HUD/StatusBar") as Control).material as ShaderMaterial
	await _step(20, false)
	for i in 30:                                   # close Amma's 8 PM call with real E presses
		if not story.dialogue_active:
			break
		OS.delay_msec(400)
		_key(KEY_E, true)
		await _step(1, false)
		_key(KEY_E, false)
		await _step(2, false)
	log_lines.append("frame\tT_held\tfast_forward\tphase\tskip_amount")
	for seg in PLAN:
		t_down = seg[0] == "hold"
		_key(KEY_T, t_down)
		await _step(seg[1])
	var args := OS.get_cmdline_user_args()
	var f := FileAccess.open(args[0] if args.size() > 0 else "user://glow_motion.txt", FileAccess.WRITE)
	f.store_string("\n".join(log_lines) + "\n")
	f.close()
	quit(0)
