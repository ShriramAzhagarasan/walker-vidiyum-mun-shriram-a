extends "res://tests/harness.gd"
## A6 Effect A configuration read-back (CHANGE-BRIEF §A.3, §A.4).
## Loads res://effects/footstep_scuff.tscn and asserts every setting the brief names, using the
## brief's values as the expected values. No rendering, no triggering — the look is checked by
## frame strips; this test proves the scene file matches §A.3.
## Run:  ./scripts/run-test.sh test_footstep_scuff_config.gd 60

const SCENE := "res://effects/footstep_scuff.tscn"

const EPS := 1.0e-5

func run() -> bool:
	var ps: PackedScene = load(SCENE)
	check("scene loads: %s" % SCENE, ps != null, ps)
	if ps == null:
		return true
	var root_node: Node = ps.instantiate()
	check("root is Node3D named FootstepScuff",
		root_node is Node3D and root_node.name == "FootstepScuff",
		"%s / %s" % [root_node.get_class(), root_node.name])
	check("root process_mode = PAUSABLE (1)",
		root_node.process_mode == Node.PROCESS_MODE_PAUSABLE, root_node.process_mode)
	check("root has exactly two children (SoftDust, FineGrit)",
		root_node.get_child_count() == 2, root_node.get_child_count())

	var soft: CPUParticles3D = root_node.get_node_or_null("SoftDust")
	var grit: CPUParticles3D = root_node.get_node_or_null("FineGrit")
	check("SoftDust exists and is CPUParticles3D", soft != null, soft)
	check("FineGrit exists and is CPUParticles3D", grit != null, grit)
	if soft == null or grit == null:
		root_node.queue_free()
		return true

	_check_emitter(soft, "SoftDust", {
		"amount": 10, "lifetime": 1.15, "one_shot": true, "explosiveness": 1.0,
		"box": Vector3(0.08, 0.01, 0.05),
		"spread": 80.0, "vmin": 0.25, "vmax": 0.65,
		"gravity_y": -0.9, "dmin": 1.5, "dmax": 2.5,
		"smin": 0.8, "smax": 1.2,
		"avmin": -40.0, "avmax": 40.0,
		"quad_size": Vector2(0.12, 0.12),
	})
	_check_emitter(grit, "FineGrit", {
		"amount": 5, "lifetime": 1.15, "one_shot": true, "explosiveness": 1.0,
		"box": Vector3(0.06, 0.01, 0.04),
		"spread": 85.0, "vmin": 0.35, "vmax": 0.80,
		"gravity_y": -1.8, "dmin": 1.0, "dmax": 2.0,
		"smin": 0.7, "smax": 1.3,
		"avmin": -60.0, "avmax": 60.0,
		"quad_size": Vector2(0.035, 0.035),
	})

	# SoftDust size curve: 0.6 → 1.3 at 25% → 1.0 at 50% → 0.4 at end; max_value must clear 1.3 (§A.3 note).
	_check_scale_curve(soft, "SoftDust", [
		Vector2(0.0, 0.6), Vector2(0.25, 1.3), Vector2(0.5, 1.0), Vector2(1.0, 0.4),
	], 1.3)
	# FineGrit size curve: 1.0 → 0.9 at 50% → 0.2 at end.
	_check_scale_curve(grit, "FineGrit", [
		Vector2(0.0, 1.0), Vector2(0.5, 0.9), Vector2(1.0, 0.2),
	], 1.0)

	# SoftDust colour ramp (colour, alpha) from §A.3, alpha at 50 %/70 % from brief revision 2 (tuning r1).
	_check_color_ramp(soft, "SoftDust", [
		[0.0,  Color8(0xD9, 0xC5, 0xA4), 0.55],
		[0.2,  Color8(0xE2, 0xD1, 0xB5), 0.45],
		[0.5,  Color8(0xE5, 0xD8, 0xC5), 0.30],
		[0.7,  Color8(0xE5, 0xD8, 0xC5), 0.15],
		[1.0,  Color8(0xE5, 0xD8, 0xC5), 0.00],
	])
	_check_color_ramp(grit, "FineGrit", [
		[0.0,  Color8(0x80, 0x64, 0x48), 0.85],
		[0.3,  Color8(0xA1, 0x83, 0x5B), 0.65],
		[0.65, Color8(0xB8, 0x9A, 0x71), 0.15],
		[1.0,  Color8(0xB8, 0x9A, 0x71), 0.00],
	])

	root_node.queue_free()
	await steps(1)
	return true

func _check_emitter(cp: CPUParticles3D, name: String, want: Dictionary) -> void:
	check("%s emission_shape = EMISSION_SHAPE_BOX (3)" % name,
		cp.emission_shape == CPUParticles3D.EMISSION_SHAPE_BOX, cp.emission_shape)
	check("%s amount = %d" % [name, want["amount"]], cp.amount == want["amount"], cp.amount)
	check("%s lifetime = %.2fs" % [name, want["lifetime"]],
		is_equal_approx(cp.lifetime, want["lifetime"]), cp.lifetime)
	check("%s one_shot = %s" % [name, want["one_shot"]], cp.one_shot == want["one_shot"], cp.one_shot)
	check("%s explosiveness = %.2f" % [name, want["explosiveness"]],
		is_equal_approx(cp.explosiveness, want["explosiveness"]), cp.explosiveness)
	check("%s emitting = false (initial)" % name, cp.emitting == false, cp.emitting)
	check("%s emission_box_extents = %s" % [name, want["box"]],
		cp.emission_box_extents.is_equal_approx(want["box"]), cp.emission_box_extents)

	check("%s direction = (0, 1, 0)" % name,
		cp.direction.is_equal_approx(Vector3(0, 1, 0)), cp.direction)
	check("%s spread = %.0f deg" % [name, want["spread"]],
		is_equal_approx(cp.spread, want["spread"]), cp.spread)
	check("%s initial_velocity_min = %.2f m/s" % [name, want["vmin"]],
		is_equal_approx(cp.initial_velocity_min, want["vmin"]), cp.initial_velocity_min)
	check("%s initial_velocity_max = %.2f m/s" % [name, want["vmax"]],
		is_equal_approx(cp.initial_velocity_max, want["vmax"]), cp.initial_velocity_max)
	check("%s gravity = (0, %.2f, 0)" % [name, want["gravity_y"]],
		cp.gravity.is_equal_approx(Vector3(0, want["gravity_y"], 0)), cp.gravity)
	check("%s damping_min = %.2f" % [name, want["dmin"]],
		is_equal_approx(cp.damping_min, want["dmin"]), cp.damping_min)
	check("%s damping_max = %.2f" % [name, want["dmax"]],
		is_equal_approx(cp.damping_max, want["dmax"]), cp.damping_max)
	check("%s scale_amount_min = %.2f" % [name, want["smin"]],
		is_equal_approx(cp.scale_amount_min, want["smin"]), cp.scale_amount_min)
	check("%s scale_amount_max = %.2f" % [name, want["smax"]],
		is_equal_approx(cp.scale_amount_max, want["smax"]), cp.scale_amount_max)
	check("%s hue_variation_min = -0.02" % name,
		is_equal_approx(cp.hue_variation_min, -0.02), cp.hue_variation_min)
	check("%s hue_variation_max = +0.02" % name,
		is_equal_approx(cp.hue_variation_max, 0.02), cp.hue_variation_max)
	check("%s angle_min = 0 deg" % name,
		is_equal_approx(cp.angle_min, 0.0), cp.angle_min)
	check("%s angle_max = 360 deg" % name,
		is_equal_approx(cp.angle_max, 360.0), cp.angle_max)
	check("%s angular_velocity_min = %.0f deg/s" % [name, want["avmin"]],
		is_equal_approx(cp.angular_velocity_min, want["avmin"]), cp.angular_velocity_min)
	check("%s angular_velocity_max = %.0f deg/s" % [name, want["avmax"]],
		is_equal_approx(cp.angular_velocity_max, want["avmax"]), cp.angular_velocity_max)

	# Draw
	var mesh := cp.mesh as QuadMesh
	check("%s mesh is QuadMesh" % name, mesh != null, cp.mesh)
	if mesh != null:
		check("%s quad size = %s m" % [name, want["quad_size"]],
			mesh.size.is_equal_approx(want["quad_size"]), mesh.size)
		var mat := mesh.material as StandardMaterial3D
		check("%s material is StandardMaterial3D" % name, mat != null, mesh.material)
		if mat != null:
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
			check("%s material.albedo_texture is a procedural GradientTexture2D" % name,
				mat.albedo_texture != null and mat.albedo_texture is GradientTexture2D, mat.albedo_texture)

	# Node settings
	check("%s local_coords = false (dust stays at footprint)" % name,
		cp.local_coords == false, cp.local_coords)
	check("%s preprocess = 0.0 s" % name, is_equal_approx(cp.preprocess, 0.0), cp.preprocess)
	check("%s speed_scale = 1.0" % name, is_equal_approx(cp.speed_scale, 1.0), cp.speed_scale)
	check("%s visibility_aabb = AABB((-0.6,-0.1,-0.6),(1.2,0.6,1.2))" % name,
		cp.visibility_aabb == AABB(Vector3(-0.6, -0.1, -0.6), Vector3(1.2, 0.6, 1.2)),
		cp.visibility_aabb)
	check("%s process_mode = PAUSABLE (1)" % name,
		cp.process_mode == Node.PROCESS_MODE_PAUSABLE, cp.process_mode)
	# Emitter 0.03 m above the root so the root sits on the floor at Hari's feet.
	check("%s transform.origin = (0, 0.03, 0)" % name,
		cp.transform.origin.is_equal_approx(Vector3(0, 0.03, 0)), cp.transform.origin)

func _check_scale_curve(cp: CPUParticles3D, name: String, want_points: Array, want_max: float) -> void:
	var c := cp.scale_amount_curve as Curve
	check("%s scale_amount_curve set" % name, c != null, c)
	if c == null:
		return
	check("%s scale_amount_curve.max_value >= %.2f (so peak isn't clipped, §A.3 note)"
			% [name, want_max],
		c.max_value + EPS >= want_max, c.max_value)
	check("%s scale_amount_curve has %d points" % [name, want_points.size()],
		c.get_point_count() == want_points.size(), c.get_point_count())
	for i in want_points.size():
		var want: Vector2 = want_points[i]
		var got := Vector2(c.get_point_position(i).x, c.get_point_position(i).y)
		check("%s scale_amount_curve[%d] = (life %.2f, scale %.2f)"
				% [name, i, want.x, want.y],
			got.is_equal_approx(want), got)

func _check_color_ramp(cp: CPUParticles3D, name: String, want: Array) -> void:
	var g := cp.color_ramp as Gradient
	check("%s color_ramp set" % name, g != null, g)
	if g == null:
		return
	check("%s color_ramp has %d stops" % [name, want.size()],
		g.get_point_count() == want.size(), g.get_point_count())
	for i in want.size():
		var row: Array = want[i]
		var want_t: float = row[0]
		var want_c: Color = row[1]
		var want_a: float = row[2]
		var got_t: float = g.get_offset(i)
		var got_c: Color = g.get_color(i)
		check("%s color_ramp[%d] offset = %.2f" % [name, i, want_t],
			is_equal_approx(got_t, want_t), got_t)
		# Colour and alpha both live in the Gradient's Color values (CPUParticles3D has no alpha_curve in 4.7.2).
		check("%s color_ramp[%d] rgb within 1/255 of %s" % [name, i, _hex6(want_c)],
			_rgb_close(got_c, want_c), got_c)
		check("%s color_ramp[%d] alpha = %.2f" % [name, i, want_a],
			is_equal_approx(got_c.a, want_a), got_c.a)

func _rgb_close(a: Color, b: Color) -> bool:
	# One 8-bit step = 1/255 ≈ 0.00392. Allow half a step.
	var tol := 0.5 / 255.0
	return absf(a.r - b.r) <= tol and absf(a.g - b.g) <= tol and absf(a.b - b.b) <= tol

func _hex6(c: Color) -> String:
	return "#%02X%02X%02X" % [int(round(c.r * 255.0)), int(round(c.g * 255.0)), int(round(c.b * 255.0))]
