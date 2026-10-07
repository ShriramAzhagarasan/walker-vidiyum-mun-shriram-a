## Scripted-state screenshots of the running slice (windowed, real renderer), used for TEST-REPORT
## comparisons (storyboard vs slice, character sheet vs in-engine). These are SCRIPTED captures:
## the clock and Hari's position are set via the test API, not played by hand.
##   Godot --path godot -s res://tools/capture_shots.gd -- [out_dir]
extends SceneTree

var out_dir := "../evidence/shots"
var slice: Node3D

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		out_dir = args[0]
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://").path_join(out_dir))
	slice = load("res://scenes/slice.tscn").instantiate()
	root.add_child(slice)
	_run()

func _wait(frames: int) -> void:
	for i in frames:
		await process_frame

func _shot(name: String) -> void:
	await _wait(3)
	var img := root.get_viewport().get_texture().get_image()
	var path := ProjectSettings.globalize_path("res://").path_join(out_dir).path_join(name + ".png")
	img.save_png(path)
	print("shot ", name)

func _place(x: float, z: float = 0.0, face_left := false) -> void:
	var hari: CharacterBody3D = slice.get_node("Hari")
	hari.global_position = Vector3(x, 0, z)
	hari.get_node("Sprite").flip_h = face_left
	slice.get_node("CameraRig").call("snap")
	await _wait(40)

func _close_dialogue() -> void:
	var story := root.get_node("Story")
	var guard := 0
	while story.current_line().size() > 0 and guard < 30:
		story.press_interact()
		await _wait(14)
		guard += 1

func _run() -> void:
	var ls := root.get_node("LoopState")
	var story := root.get_node("Story")
	ls.test_hold_clock = true
	await _wait(30)
	# Panel 2: 8 PM, Amma's call (PHONE + phone card + dialogue)
	await _wait(40)
	await _shot("p02_amma_call")
	await _close_dialogue()
	await _wait(100)
	# State gallery on the deck, facing right then left (character sheet vs engine)
	var hari_node: Node = slice.get_node("Hari")
	hari_node.set_physics_process(false)                   # stop the idle/walk auto-state while posing for the gallery
	for st in ["IDLE", "WALK", "TALK", "PHONE", "NOTES", "OVERHEAR", "STARTLED", "KEYS", "WHITEOUT", "RELIEF"]:
		await _place(11.0)
		story.set_hari_state(st)
		await _shot("state_%s_right" % st.to_lower())
		await _place(11.0, 0.0, true)
		await _shot("state_%s_left" % st.to_lower())
	story.set_hari_state("IDLE")
	hari_node.set_physics_process(true)
	# Panel 3: walking up to Manikandan at the SUV (gate framing)
	await _place(4.2, 0.6, true)
	story.set_hari_state("WALK")
	await _shot("p03_gate_walk")
	story.set_hari_state("IDLE")
	await _place(3.7, 0.6, true)
	story.start_conversation("mani_generic")
	await _wait(10)
	await _shot("p03_talk_manikandan")
	await _close_dialogue()
	# Panel 4: overhearing at 1:25 AM, then the clue card
	ls.test_advance_to(25 * 60 + 25)
	await _place(3.7, 0.6, true)
	story.start_conversation("mani_overhear")
	await _wait(10)
	await _shot("p04_overhear")
	await _close_dialogue()
	await _wait(20)
	await _shot("p04_clue_saved")
	await _wait(120)
	# Panel 5: 1:40 AM, Advay takes the keys
	await _place(5.5, 0.4, true)
	ls.test_advance_to(25 * 60 + 40)
	await _wait(30)
	await _shot("p05_keys_taken")
	await _wait(200)
	# Fire glow at 4:45 from the railing
	ls.test_advance_to(28 * 60 + 50)
	await _place(22.5, 1.0)
	await _wait(60)
	await _shot("railing_fire_445am")
	# Panel 6: dawn failure
	await _place(12.0)
	ls.test_advance_to(29 * 60 + 50)
	await _wait(50)
	await _shot("p06_dawn_crash")
	await _wait(80)
	await _shot("p06_whiteout")
	ls.test_skip_sequence()
	await _wait(30)
	# Panel 7: loop 2 start
	await _shot("p07_loop2_wake")
	await _close_dialogue()
	await _wait(60)
	# Panel 8: ask about Selvam -> keys stay
	await _place(3.7, 0.6, true)
	story.start_conversation("mani_choice")
	await _wait(10)
	await _shot("p08_choice")
	story.move_choice(0)
	await _close_dialogue()
	await _wait(10)
	await _shot("p08_keys_stay")
	await _wait(200)
	# Panel 9: safe dawn at the railing, then end card
	await _place(22.5, 1.0)
	ls.test_advance_to(29 * 60 + 50)
	await _wait(60)
	await _shot("p09_safe_dawn")
	ls.test_skip_sequence()
	await _wait(120)
	await _shot("p09_end_card")
	quit(0)
