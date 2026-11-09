## SCRIPTED CAPTURE for the A6 film (not played by hand): the real slice (real trigger, real moth controller, real
## effect scenes, no fixed seed), with D / P / A pressed and released through Input.parse_input_event, recorded frame
## by frame by Godot's movie maker. Nothing is saved to the project.
##   godot --path godot --write-movie <out.avi> --fixed-fps 30 --resolution 1920x1080 -s <this file> -- <log.txt>
## Writes one line per recorded frame: frame, keys held, paused, Hari x, live FootstepScuff instances, clock minute,
## and how many moth emitters are emitting.
extends SceneTree

# walk right under the string lights, pause mid-walk, unpause, stop, then walk left toward the dark gate and stop
const PLAN := [["idle", 15], ["D", 60], ["P", 1], ["paused", 45], ["P", 1], ["D", 45], ["idle", 40], ["A", 130], ["idle", 45]]
var log_lines := PackedStringArray()
var ls: Node
var slice: Node
var hari: Node3D
var scuffs: Node
var moths: Node
var held := ""
var frame := 0

func _initialize() -> void:
	_run()

func _key(code: Key, pressed: bool) -> void:
	var e := InputEventKey.new()
	e.keycode = code
	e.physical_keycode = code
	e.pressed = pressed
	Input.parse_input_event(e)

func _emitting() -> int:
	var n := 0
	for c in moths.find_children("*", "GPUParticles3D", true, false):
		if (c as GPUParticles3D).emitting:
			n += 1
	return n

func _step(n: int, record := true) -> void:
	for i in n:
		await process_frame
		if record:
			log_lines.append("%d\t%s\t%s\t%.3f\t%d\t%d\t%d" % [frame, held, paused, hari.global_position.x,
				scuffs.get_child_count(), int(ls.clock_minutes), _emitting()])
			frame += 1

func _run() -> void:
	slice = load("res://scenes/slice.tscn").instantiate()
	root.add_child(slice)
	ls = root.get_node("LoopState")
	var story := root.get_node("Story")
	hari = slice.get_node("Hari")
	scuffs = slice.get_node("FootstepScuffs")
	moths = slice.get_node("StringLightMoths")
	await _step(20, false)
	for i in 30:                                   # close Amma's 8 PM call with real E presses
		if not story.dialogue_active:
			break
		OS.delay_msec(400)
		_key(KEY_E, true)
		await _step(1, false)
		_key(KEY_E, false)
		await _step(2, false)
	log_lines.append("frame\tkeys\tpaused\thari_x\tscuffs_alive\tclock_min\tmoth_emitters_on")
	for seg in PLAN:
		match seg[0]:
			"D":
				held = "D"; _key(KEY_D, true); await _step(seg[1]); _key(KEY_D, false); held = ""
			"A":
				held = "A"; _key(KEY_A, true); await _step(seg[1]); _key(KEY_A, false); held = ""
			"P":
				held = "P"; _key(KEY_P, true); await _step(1); _key(KEY_P, false); held = ""
			_:
				await _step(seg[1])
	var args := OS.get_cmdline_user_args()
	var f := FileAccess.open(args[0] if args.size() > 0 else "user://walk_effects.txt", FileAccess.WRITE)
	f.store_string("\n".join(log_lines) + "\n")
	f.close()
	quit(0)
