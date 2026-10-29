## A5 captures with the real renderer (windowed, never headless), for the human checks in TEST-REPORT.md.
## SCRIPTED captures: uniform values and the clock are set from code, not played by hand.
##   godot --path godot -s res://tools/capture_a5.gd -- <glow|hint|marble|sweep> [out_dir]
## glow:   status bar at skip_amount 0, 0.5, 1.0 and 2.0 (hint_range check), tree paused so nothing moves;
##         prints P1/P2 (CHANGE-BRIEF.md §1.8) as captured, next to the predicted on-screen blend.
## hint:   the hint-experiment quads; prints each band's centre pixel next to the §2.5 prediction.
## marble: the deck at a held 10:00 PM, glow on and glow off (§2.1 lighting).
## sweep:  each marble_dry uniform at its hint_range ends, then back to its default.
extends SceneTree

const P1 := Vector2i(200, 31)      ## battery fill
const P2 := Vector2i(300, 46)      ## bar background
const BAR := Rect2i(14, 12, 300, 38)
const PRED_P1 := {0.0: Color8(255, 255, 255), 0.5: Color8(255, 230, 204), 1.0: Color8(255, 204, 153)}
const PRED_P2 := {0.0: Color8(10, 10, 20), 0.5: Color8(71, 46, 28), 1.0: Color8(133, 82, 36)}
const PRED_HINT := {"A": [64, 128, 192], "B": [137, 188, 225]}

var mode := "glow"
var out_dir := "../evidence/a5"
var scale := 1.0      ## image px per viewport px (HiDPI)

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		mode = args[0]
	if args.size() > 1:
		out_dir = args[1]
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://").path_join(out_dir))
	match mode:
		"glow": _glow()
		"hint": _hint()
		"marble": _marble(false)
		"sweep": _marble(true)
		_:
			push_error("unknown mode " + mode)
			quit(1)

func _wait(frames: int) -> void:
	for i in frames:
		await process_frame

func _shot(name: String) -> Image:
	await _wait(4)
	var img := root.get_viewport().get_texture().get_image()
	scale = img.get_height() / 720.0
	img.save_png(ProjectSettings.globalize_path("res://").path_join(out_dir).path_join(name + ".png"))
	print("shot %s (%dx%d)" % [name, img.get_width(), img.get_height()])
	return img

func _px(img: Image, p: Vector2i) -> Color:
	return img.get_pixel(int(p.x * scale), int(p.y * scale))

func _rgb(c: Color) -> String:
	return "(%d, %d, %d)" % [c.r8, c.g8, c.b8]

func _load_slice() -> Node:
	var slice: Node = load("res://scenes/slice.tscn").instantiate()
	root.add_child(slice)
	var ls := root.get_node("LoopState")
	ls.test_hold_clock = true
	await _wait(30)
	var story := root.get_node("Story")
	var guard := 0
	while story.current_line().size() > 0 and guard < 30:      # close Amma's 8 PM call
		story.press_interact()
		await _wait(14)
		guard += 1
	await _wait(30)
	return slice

func _glow() -> void:
	var slice := await _load_slice()
	var bar := slice.get_node("HUD/StatusBar") as Control
	bar.get_node("NightSkipDriver").set_process(false)
	var mat := bar.material as ShaderMaterial
	paused = true
	bar.visible = false
	var bg := await _shot("glow_background_only")
	bar.visible = true
	var bg2 := _px(bg, P2)
	var bg1 := _px(bg, P1)
	print("scene behind the bar: at P1 %s, at P2 %s" % [_rgb(bg1), _rgb(bg2)])
	var first: Image
	for v in [0.0, 0.5, 1.0, 2.0]:
		mat.set_shader_parameter(&"skip_amount", v)
		var img := await _shot("glow_skip_%s" % str(v).replace(".", "_"))
		if first == null:
			first = img
		var line := "skip_amount %.1f   P1 captured %s   P2 captured %s" % [v, _rgb(_px(img, P1)), _rgb(_px(img, P2))]
		if PRED_P2.has(v):
			# On screen: the bar (alpha 0.6) over the scene; the battery (alpha 0.95) over the bar.
			var p2 := PRED_P2[v].lerp(bg2, 0.4) as Color
			var bar_at_p1 := PRED_P2[v].lerp(bg1, 0.4) as Color
			var p1 := bar_at_p1.lerp(PRED_P1[v], 0.95) as Color
			line += "   | predicted on screen P1 %s P2 %s" % [_rgb(p1), _rgb(p2)]
		print(line)
	# F3: nothing outside the bar's rectangle changes between 0.0 and 2.0.
	var last := root.get_viewport().get_texture().get_image()
	var changed := 0
	for y in range(0, first.get_height(), 2):
		for x in range(0, first.get_width(), 2):
			var p := Vector2i(int(x / scale), int(y / scale))
			if not BAR.has_point(p) and not first.get_pixel(x, y).is_equal_approx(last.get_pixel(x, y)):
				changed += 1
	print("F3 pixels changed outside the status bar between 0.0 and 2.0 (every 2nd px): %d" % changed)
	quit(0)

func _hint() -> void:
	root.add_child(load("res://scenes/hint_experiment.tscn").instantiate())
	await _wait(10)
	var img := await _shot("hint_quads")
	var h := img.get_height()
	var w := img.get_width()
	var unit := h / 3.0      # orthographic camera, size 3 = viewport height in metres
	for row in [["A", 0.7], ["B", -0.7]]:
		var got := []
		for bx in [-1.0, 0.0, 1.0]:
			got.append(img.get_pixel(int(w / 2.0 + bx * unit), int(h / 2.0 - row[1] * unit)).r8)
		print("Quad %s: captured %s   predicted %s" % [row[0], got, PRED_HINT[row[0]]])
	quit(0)

func _marble(sweep: bool) -> void:
	var slice := await _load_slice()
	root.get_node("LoopState").test_advance_to(22 * 60)     # 10:00 PM, held
	await _wait(30)
	var hari: CharacterBody3D = slice.get_node("Hari")
	hari.global_position = Vector3(12.5, 0, 0.6)
	hari.reset_physics_interpolation()
	slice.get_node("CameraRig").call("snap")
	await _wait(60)
	paused = true      # freeze Hari, NPCs and the camera so every frame has the same framing
	var env := (slice.get_node("WorldEnvironment") as WorldEnvironment).environment
	if not sweep:
		await _shot("marble_10pm_glow_on")
		env.glow_enabled = false
		await _shot("marble_10pm_glow_off")
		quit(0)
		return
	env.glow_enabled = false
	var dry: ShaderMaterial = load("res://materials/marble_dry.tres")
	await _shot("sweep_defaults")
	for u in dry.shader.get_shader_uniform_list():
		if u.type != TYPE_FLOAT or u.hint != PROPERTY_HINT_RANGE:
			continue
		var r: PackedStringArray = u.hint_string.split(",")
		var before: Variant = dry.get_shader_parameter(u.name)
		for end in [r[0], r[1]]:
			dry.set_shader_parameter(u.name, float(end))
			await _shot("sweep_%s_%s" % [u.name, end.replace(".", "_")])
		dry.set_shader_parameter(u.name, before)
	await _shot("sweep_back_to_defaults")
	quit(0)
