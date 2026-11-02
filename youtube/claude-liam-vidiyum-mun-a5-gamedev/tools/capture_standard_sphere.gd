## SCRIPTED CAPTURE for the A5 film: Shriram's scratch scene (scenes/scratch_standard.tscn, a sphere whose material is
## the ShaderMaterial converted from a StandardMaterial3D, i.e. shaders/standard_generated.gdshader) rendered by the
## real renderer. The scene has no camera or light of its own, so this script adds a camera, one light and a plain
## environment at runtime; nothing is saved back to the project.
##   godot --path godot -s <this file> -- <out.png>
extends SceneTree

func _initialize() -> void:
	_run()

func _run() -> void:
	var scene: Node3D = load("res://scenes/scratch_standard.tscn").instantiate()
	root.add_child(scene)
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR
	env.environment.background_color = Color(0.11, 0.11, 0.13)
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.environment.ambient_light_color = Color(0.35, 0.35, 0.4)
	scene.add_child(env)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-35, 40, 0)
	sun.light_energy = 1.3
	scene.add_child(sun)
	var cam := Camera3D.new()
	cam.position = Vector3(0, 0.15, 2.4)
	cam.fov = 40
	scene.add_child(cam)
	cam.current = true
	var mi := scene.get_node("MeshInstance3D") as MeshInstance3D
	var mat := mi.material_override as ShaderMaterial
	print("material: ", mat, " shader: ", mat.shader.resource_path if mat else "none")
	for i in 20:
		await process_frame
	var img := root.get_viewport().get_texture().get_image()
	var args := OS.get_cmdline_user_args()
	img.save_png(args[0])
	print("saved ", args[0], " ", img.get_size())
	quit(0)
