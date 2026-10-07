## Scripted stills of the title and intro panels (for TEST-REPORT / film evidence).
extends SceneTree
func _initialize() -> void:
	var intro: Control = load("res://scenes/intro.tscn").instantiate()
	root.add_child(intro)
	_run(intro)
func _shot(n: String) -> void:
	for i in 3: await process_frame
	root.get_viewport().get_texture().get_image().save_png(ProjectSettings.globalize_path("res://").path_join("../evidence/shots/" + n + ".png"))
	print("shot ", n)
func _run(intro: Control) -> void:
	for i in 90: await process_frame
	await _shot("intro_title")
	intro.call("_start_panels")
	for p in 4:
		for i in 150: await process_frame
		await _shot("intro_panel_%d" % (p + 1))
		intro.call("_next_panel")
	for i in 70: await process_frame
	await _shot("intro_outro")
	quit(0)
