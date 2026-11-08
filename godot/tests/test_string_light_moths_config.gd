extends "res://tests/harness.gd"
## A6 Effect B configuration read-back (CHANGE-BRIEF §B.3, §B.4).
## Loads res://effects/string_light_moths.tscn and asserts every setting the brief
## names, using the brief's values as the expected values. No rendering, no attractor
## solve — the look is checked by frame strips; this test proves the scene file
## matches §B.3. The effect scene has `use_fixed_seed = false` (preview flips it on).
## Run:  ./scripts/run-test.sh test_string_light_moths_config.gd 60
##
## The scene references res://effects/moth.tres via ext_resource (see §B.3 and the
## note in tools/moth_texture.gd about why the scene loads the .tres, with the .png
## still committed next to it). If either artifact is missing the test writes them
## both via the shared helper before loading the scene.

const SCENE := "res://effects/string_light_moths.tscn"
const MT := preload("res://tools/moth_texture.gd")

const EMITTERS := [
	["MothsWest",   Vector3(8.0,  2.85, -3.4)],
	["MothsMiddle", Vector3(12.0, 2.85, -3.4)],
	["MothsEast",   Vector3(16.0, 2.85, -3.4)],
]
const ATTRACTORS := [
	["AttractorWest",   Vector3(8.0,  2.85, -3.4)],
	["AttractorMiddle", Vector3(12.0, 2.85, -3.4)],
	["AttractorEast",   Vector3(16.0, 2.85, -3.4)],
]

func run() -> bool:
	if not FileAccess.file_exists(MT.OUT_PNG) or not FileAccess.file_exists(MT.OUT_TRES):
		var err := MT.save_all()
		check("bootstrapped %s and %s via tools/moth_texture.gd" % [MT.OUT_PNG, MT.OUT_TRES],
			err == OK, err)
	var ps: PackedScene = load(SCENE)
	check("scene loads: %s" % SCENE, ps != null, ps)
	if ps == null:
		return true
	var root_node: Node = ps.instantiate()
	check("root is Node3D named StringLightMoths",
		root_node is Node3D and root_node.name == "StringLightMoths",
		"%s / %s" % [root_node.get_class(), root_node.name])
	check("root process_mode = PAUSABLE (1)",
		root_node.process_mode == Node.PROCESS_MODE_PAUSABLE, root_node.process_mode)
	check("root has 6 children (3 emitters + 3 attractors)",
		root_node.get_child_count() == 6, root_node.get_child_count())

	for row in EMITTERS:
		var name: String = row[0]
		var want_pos: Vector3 = row[1]
		var cp := root_node.get_node_or_null(name) as GPUParticles3D
		check("%s exists and is GPUParticles3D" % name, cp != null, cp)
		if cp == null:
			continue
		_check_emitter_node(cp, name, want_pos)
		_check_process_material(cp, name)
		_check_draw_pass(cp, name)

	for row in ATTRACTORS:
		var name: String = row[0]
		var want_pos: Vector3 = row[1]
		var at := root_node.get_node_or_null(name) as GPUParticlesAttractorSphere3D
		check("%s exists and is GPUParticlesAttractorSphere3D" % name, at != null, at)
		if at == null:
			continue
		_check_attractor(at, name, want_pos)

	root_node.queue_free()
	await steps(1)
	return true

func _check_emitter_node(cp: GPUParticles3D, name: String, want_pos: Vector3) -> void:
	check("%s position = %s" % [name, want_pos],
		cp.transform.origin.is_equal_approx(want_pos), cp.transform.origin)
	check("%s amount = 12" % name, cp.amount == 12, cp.amount)
	check("%s amount_ratio = 1.0" % name,
		is_equal_approx(cp.amount_ratio, 1.0), cp.amount_ratio)
	check("%s one_shot = false" % name, cp.one_shot == false, cp.one_shot)
	check("%s explosiveness = 0.0" % name,
		is_equal_approx(cp.explosiveness, 0.0), cp.explosiveness)
	check("%s randomness = 0.4" % name,
		is_equal_approx(cp.randomness, 0.4), cp.randomness)
	check("%s lifetime = 2.4 s" % name,
		is_equal_approx(cp.lifetime, 2.4), cp.lifetime)
	check("%s preprocess = 2.4 s" % name,
		is_equal_approx(cp.preprocess, 2.4), cp.preprocess)
	check("%s fixed_fps = 30" % name, cp.fixed_fps == 30, cp.fixed_fps)
	check("%s speed_scale = 1.0" % name,
		is_equal_approx(cp.speed_scale, 1.0), cp.speed_scale)
	check("%s use_fixed_seed = false (effect scene; preview flips it)" % name,
		cp.use_fixed_seed == false, cp.use_fixed_seed)
	check("%s local_coords = false (moths fly in world space)" % name,
		cp.local_coords == false, cp.local_coords)
	check("%s trail_enabled = false" % name,
		cp.trail_enabled == false, cp.trail_enabled)
	check("%s process_mode = PAUSABLE (1)" % name,
		cp.process_mode == Node.PROCESS_MODE_PAUSABLE, cp.process_mode)
	check("%s visibility_aabb = AABB((-1.5,-1.1,-1.5),(3,2.2,3))" % name,
		cp.visibility_aabb == AABB(Vector3(-1.5, -1.1, -1.5), Vector3(3.0, 2.2, 3.0)),
		cp.visibility_aabb)

func _check_process_material(cp: GPUParticles3D, name: String) -> void:
	var pm := cp.process_material as ParticleProcessMaterial
	check("%s process_material is ParticleProcessMaterial" % name,
		pm != null, cp.process_material)
	if pm == null:
		return
	# Emission
	check("%s pm.emission_shape = EMISSION_SHAPE_BOX (3)" % name,
		pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_BOX, pm.emission_shape)
	check("%s pm.emission_box_extents = (0.65, 0.30, 0.40)" % name,
		pm.emission_box_extents.is_equal_approx(Vector3(0.65, 0.30, 0.40)),
		pm.emission_box_extents)
	# Process
	check("%s pm.direction = (0, 1, 0)" % name,
		pm.direction.is_equal_approx(Vector3(0, 1, 0)), pm.direction)
	check("%s pm.spread = 85 deg" % name,
		is_equal_approx(pm.spread, 85.0), pm.spread)
	check("%s pm.initial_velocity_min = 0.06" % name,
		is_equal_approx(pm.initial_velocity_min, 0.06), pm.initial_velocity_min)
	check("%s pm.initial_velocity_max = 0.28" % name,
		is_equal_approx(pm.initial_velocity_max, 0.28), pm.initial_velocity_max)
	check("%s pm.gravity = (0, 0, 0)" % name,
		pm.gravity.is_equal_approx(Vector3.ZERO), pm.gravity)
	check("%s pm.damping_min = 0.12" % name,
		is_equal_approx(pm.damping_min, 0.12), pm.damping_min)
	check("%s pm.damping_max = 0.35" % name,
		is_equal_approx(pm.damping_max, 0.35), pm.damping_max)
	check("%s pm.scale_min = 0.7" % name,
		is_equal_approx(pm.scale_min, 0.7), pm.scale_min)
	check("%s pm.scale_max = 1.2" % name,
		is_equal_approx(pm.scale_max, 1.2), pm.scale_max)
	check("%s pm.angle_min = -35 deg" % name,
		is_equal_approx(pm.angle_min, -35.0), pm.angle_min)
	check("%s pm.angle_max = +35 deg" % name,
		is_equal_approx(pm.angle_max, 35.0), pm.angle_max)
	check("%s pm.angular_velocity_min = -110 deg/s" % name,
		is_equal_approx(pm.angular_velocity_min, -110.0), pm.angular_velocity_min)
	check("%s pm.angular_velocity_max = +110 deg/s" % name,
		is_equal_approx(pm.angular_velocity_max, 110.0), pm.angular_velocity_max)
	check("%s pm.hue_variation_min = -0.03" % name,
		is_equal_approx(pm.hue_variation_min, -0.03), pm.hue_variation_min)
	check("%s pm.hue_variation_max = +0.03" % name,
		is_equal_approx(pm.hue_variation_max, 0.03), pm.hue_variation_max)
	check("%s pm.attractor_interaction_enabled = true" % name,
		pm.attractor_interaction_enabled == true, pm.attractor_interaction_enabled)
	# Turbulence
	check("%s pm.turbulence_enabled = true" % name,
		pm.turbulence_enabled == true, pm.turbulence_enabled)
	check("%s pm.turbulence_noise_strength = 0.45" % name,
		is_equal_approx(pm.turbulence_noise_strength, 0.45), pm.turbulence_noise_strength)
	check("%s pm.turbulence_noise_scale = 5.0" % name,
		is_equal_approx(pm.turbulence_noise_scale, 5.0), pm.turbulence_noise_scale)
	check("%s pm.turbulence_noise_speed = (0.15, 0.08, 0.12)" % name,
		pm.turbulence_noise_speed.is_equal_approx(Vector3(0.15, 0.08, 0.12)),
		pm.turbulence_noise_speed)
	check("%s pm.turbulence_noise_speed_random = 0.2" % name,
		is_equal_approx(pm.turbulence_noise_speed_random, 0.2),
		pm.turbulence_noise_speed_random)
	check("%s pm.turbulence_influence_min = 0.12" % name,
		is_equal_approx(pm.turbulence_influence_min, 0.12), pm.turbulence_influence_min)
	check("%s pm.turbulence_influence_max = 0.30" % name,
		is_equal_approx(pm.turbulence_influence_max, 0.30), pm.turbulence_influence_max)
	check("%s pm.turbulence_initial_displacement_min = 0.0" % name,
		is_equal_approx(pm.turbulence_initial_displacement_min, 0.0),
		pm.turbulence_initial_displacement_min)
	check("%s pm.turbulence_initial_displacement_max = 0.06" % name,
		is_equal_approx(pm.turbulence_initial_displacement_max, 0.06),
		pm.turbulence_initial_displacement_max)
	_check_scale_curve(pm, name)
	_check_color_ramp(pm, name)

func _check_scale_curve(pm: ParticleProcessMaterial, name: String) -> void:
	# ParticleProcessMaterial wraps the Curve in a CurveTexture.
	var tex := pm.scale_curve as CurveTexture
	check("%s pm.scale_curve is CurveTexture" % name, tex != null, pm.scale_curve)
	if tex == null:
		return
	var c := tex.curve as Curve
	check("%s pm.scale_curve.curve is Curve" % name, c != null, tex.curve)
	if c == null:
		return
	var want: Array[Vector2] = [
		Vector2(0.0, 0.7), Vector2(0.15, 1.0), Vector2(0.75, 1.0), Vector2(1.0, 0.6),
	]
	check("%s scale_curve has %d points" % [name, want.size()],
		c.get_point_count() == want.size(), c.get_point_count())
	for i in want.size():
		var w: Vector2 = want[i]
		var g := c.get_point_position(i)
		check("%s scale_curve[%d] = (life %.2f, scale %.2f)" % [name, i, w.x, w.y],
			g.is_equal_approx(w), g)

func _check_color_ramp(pm: ParticleProcessMaterial, name: String) -> void:
	# ParticleProcessMaterial wraps the Gradient in a GradientTexture1D.
	var tex := pm.color_ramp as GradientTexture1D
	check("%s pm.color_ramp is GradientTexture1D" % name, tex != null, pm.color_ramp)
	if tex == null:
		return
	var g := tex.gradient as Gradient
	check("%s pm.color_ramp.gradient is Gradient" % name, g != null, tex.gradient)
	if g == null:
		return
	# §B.3: stops at 0%/15%/70%/100%; colours and alpha from the brief.
	var want := [
		# Colours from brief revision 4 (tuning B r2, dark umber); alphas from §B.3.
		[0.00, Color8(0x3B, 0x2F, 0x25), 0.0],
		[0.15, Color8(0x4A, 0x3B, 0x2E), 0.8],
		[0.70, Color8(0x4A, 0x3B, 0x2E), 0.7],
		[1.00, Color8(0x3B, 0x2F, 0x25), 0.0],
	]
	check("%s color_ramp has %d stops" % [name, want.size()],
		g.get_point_count() == want.size(), g.get_point_count())
	for i in want.size():
		var row: Array = want[i]
		var want_t: float = row[0]
		var want_c: Color = row[1]
		var want_a: float = row[2]
		var got_t := g.get_offset(i)
		var got_c := g.get_color(i)
		check("%s color_ramp[%d] offset = %.2f" % [name, i, want_t],
			is_equal_approx(got_t, want_t), got_t)
		check("%s color_ramp[%d] rgb within 1/255 of %s" % [name, i, _hex6(want_c)],
			_rgb_close(got_c, want_c), got_c)
		check("%s color_ramp[%d] alpha = %.2f" % [name, i, want_a],
			is_equal_approx(got_c.a, want_a), got_c.a)

func _check_draw_pass(cp: GPUParticles3D, name: String) -> void:
	var mesh := cp.draw_pass_1 as QuadMesh
	check("%s draw_pass_1 is QuadMesh" % name, mesh != null, cp.draw_pass_1)
	if mesh == null:
		return
	check("%s quad size = (0.21, 0.135) m (brief revision 3, tuning B r1; was 0.07 x 0.045)" % name,
		mesh.size.is_equal_approx(Vector2(0.21, 0.135)), mesh.size)
	var mat := mesh.material as StandardMaterial3D
	check("%s mesh.material is StandardMaterial3D" % name, mat != null, mesh.material)
	if mat == null:
		return
	check("%s material.transparency = ALPHA (1)" % name,
		mat.transparency == BaseMaterial3D.TRANSPARENCY_ALPHA, mat.transparency)
	check("%s material.blend_mode = MIX (0)" % name,
		mat.blend_mode == BaseMaterial3D.BLEND_MODE_MIX, mat.blend_mode)
	check("%s material.shading_mode = UNSHADED (0)" % name,
		mat.shading_mode == BaseMaterial3D.SHADING_MODE_UNSHADED, mat.shading_mode)
	check("%s material.billboard_mode = BILLBOARD_PARTICLES (3)" % name,
		mat.billboard_mode == BaseMaterial3D.BILLBOARD_PARTICLES, mat.billboard_mode)
	check("%s material.vertex_color_use_as_albedo = true" % name,
		mat.vertex_color_use_as_albedo == true, mat.vertex_color_use_as_albedo)
	check("%s material.albedo_texture = res://effects/moth.tres" % name,
		mat.albedo_texture != null and mat.albedo_texture.resource_path == "res://effects/moth.tres",
		mat.albedo_texture)

func _check_attractor(at: GPUParticlesAttractorSphere3D, name: String, want_pos: Vector3) -> void:
	check("%s position = %s" % [name, want_pos],
		at.transform.origin.is_equal_approx(want_pos), at.transform.origin)
	check("%s radius = 1.0" % name, is_equal_approx(at.radius, 1.0), at.radius)
	check("%s strength = 0.30" % name,
		is_equal_approx(at.strength, 0.30), at.strength)
	check("%s attenuation = 1.0" % name,
		is_equal_approx(at.attenuation, 1.0), at.attenuation)
	check("%s directionality = 0.0" % name,
		is_equal_approx(at.directionality, 0.0), at.directionality)
	check("%s cull_mask = 4294967295 (all layers; won't affect Effect A CPU particles)" % name,
		at.cull_mask == 4294967295, at.cull_mask)

func _rgb_close(a: Color, b: Color) -> bool:
	var tol := 0.5 / 255.0
	return absf(a.r - b.r) <= tol and absf(a.g - b.g) <= tol and absf(a.b - b.b) <= tol

func _hex6(c: Color) -> String:
	return "#%02X%02X%02X" % [int(round(c.r * 255.0)), int(round(c.g * 255.0)), int(round(c.b * 255.0))]
