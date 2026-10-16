extends SceneTree
## Saves screenshots of the A3 showcase scene (windowed run, not headless, so it really renders):
##   ~/Downloads/Godot.app/Contents/MacOS/Godot --path godot --script res://tests/capture_a3.gd --resolution 1600x900
## Writes evidence/a3/godot-<view>.png. These are engine screenshots for TEST-REPORT and the film; the human look check
## (orbiting each asset by hand, including behind and below) is still Shriram's.

const VIEWS := [
	# name, focus, distance, yaw (deg), pitch (deg)
	["overview", Vector3(0, 0.9, 0), 13.0, -28.0, 16.0],
	["suv-front", Vector3(0, 0.8, 0), 7.5, 55.0, 12.0],
	["suv-rear", Vector3(0, 0.8, 0), 7.5, -125.0, 12.0],
	["suv-below", Vector3(0, 0.8, 0), 7.0, 20.0, -18.0],
	["shrine-front", Vector3(-4.2, 0.45, 0), 3.0, -12.0, 8.0],
	["shrine-back", Vector3(-4.2, 0.45, 0), 3.0, 160.0, 20.0],
	["fence-front", Vector3(4.6, 1.0, 0), 4.6, -5.0, 6.0],
	["fence-side", Vector3(4.6, 1.0, 0), 4.6, 70.0, 15.0],
]

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var scene: Node3D = (load("res://scenes/a3_showcase.tscn") as PackedScene).instantiate()
	root.add_child(scene)
	var out := ProjectSettings.globalize_path("res://../evidence/a3")
	DirAccess.make_dir_recursive_absolute(out)
	for v in VIEWS:
		scene.focus = v[1]
		scene.dist = v[2]
		scene.yaw = deg_to_rad(v[3])
		scene.pitch = deg_to_rad(v[4])
		scene._update_camera()
		for i in 8:
			await process_frame
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		img.save_png(out + "/godot-%s.png" % v[0])
		print("saved godot-%s.png" % v[0])
	quit(0)
