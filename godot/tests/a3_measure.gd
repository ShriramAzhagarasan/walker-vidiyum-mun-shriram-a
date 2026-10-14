extends RefCounted
## A3 asset measurement, shared by check_a3_assets.gd (the real .glb files) and
## check_a3_selftest.gd (deliberately broken stand-ins that prove the checks can fail).
##
## Everything is measured from MESH VERTICES in world space, never from a collider:
## Module 3's floor check stopped on the object's own collider and proved nothing.
## What this cannot show: whether an asset looks right, reads as what it is, or suits
## the game's lighting and style. Those are Shriram's human checks (TEST-REPORT).

## Walk every MeshInstance3D under `node`, after it is in the tree (global transforms valid).
static func measure(node: Node3D) -> Dictionary:
	var lo := Vector3(INF, INF, INF)
	var hi := Vector3(-INF, -INF, -INF)
	var tris := 0
	var meshes := 0
	var surfaces := 0
	var colours: Array[Color] = []
	var parts := {}                      # lower-case node name -> world-space vertex centre
	var scales := {}                     # node path -> scale, for every Node3D (root included)
	for n in _all(node):
		if n is Node3D:
			scales[str(node.get_path_to(n))] = (n as Node3D).scale
		if not (n is MeshInstance3D) or (n as MeshInstance3D).mesh == null:
			continue
		var mi := n as MeshInstance3D
		meshes += 1
		var p_lo := Vector3(INF, INF, INF)
		var p_hi := Vector3(-INF, -INF, -INF)
		for s in mi.mesh.get_surface_count():
			surfaces += 1
			var arrays := mi.mesh.surface_get_arrays(s)
			var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
			var idx = arrays[Mesh.ARRAY_INDEX]
			tris += (idx.size() if idx != null and idx.size() > 0 else verts.size()) / 3
			for v in verts:
				var w := mi.global_transform * v
				lo = lo.min(w); hi = hi.max(w)
				p_lo = p_lo.min(w); p_hi = p_hi.max(w)
			var mat := mi.get_active_material(s)
			if mat is BaseMaterial3D:
				colours.append((mat as BaseMaterial3D).albedo_color)
		parts[mi.name.to_lower()] = (p_lo + p_hi) / 2.0
	var size := hi - lo if meshes > 0 else Vector3.ZERO
	return {"size": size, "min": lo, "max": hi, "tris": tris, "meshes": meshes, "surfaces": surfaces,
			"colours": colours, "parts": parts, "scales": scales, "root_basis_identity": node.basis.is_equal_approx(Basis.IDENTITY)}

## Compare a measurement with one asset's entry in a3_brief.json. Returns [{id, pass, observed}].
static func evaluate(m: Dictionary, spec: Dictionary, brief: Dictionary) -> Array:
	var out := []
	var want := Vector3(spec.size_xyz[0], spec.size_xyz[1], spec.size_xyz[2])
	var tol: float = brief.tolerance_size_fraction
	var size: Vector3 = m.size
	var axis_ok := []
	for i in 3:
		axis_ok.append(absf(size[i] - want[i]) <= want[i] * tol)
	out.append({"id": "size within ±%d %% of brief (x, y=up, z)" % int(tol * 100),
		"pass": axis_ok[0] and axis_ok[1] and axis_ok[2],
		"observed": "%.3f × %.3f × %.3f m vs brief %.2f × %.2f × %.2f" % [size.x, size.y, size.z, want.x, want.y, want.z]})
	# Upright: Godot's Y must carry the briefed HEIGHT. An asset on its side swaps Y with X or Z.
	out.append({"id": "upright: Godot Y extent = briefed height", "pass": axis_ok[1],
		"observed": "y extent %.3f m (brief height %.2f m)" % [size.y, want.y]})
	var bad_scales := []
	for path in m.scales:
		if not (m.scales[path] as Vector3).is_equal_approx(Vector3.ONE):
			bad_scales.append("%s=%s" % [path, m.scales[path]])
	out.append({"id": "every node scale = (1, 1, 1)", "pass": bad_scales.is_empty(),
		"observed": "all 1,1,1 (%d nodes)" % m.scales.size() if bad_scales.is_empty() else ", ".join(bad_scales)})
	out.append({"id": "root not rotated", "pass": m.root_basis_identity, "observed": "basis identity" if m.root_basis_identity else "rotated root"})
	var ftol: float = brief.floor_tolerance_m
	var min_y: float = (m.min as Vector3).y
	out.append({"id": "base on the floor: lowest mesh vertex y = 0 ± %.2f m (vertices, not a collider)" % ftol,
		"pass": absf(min_y) <= ftol, "observed": "lowest vertex y = %+.4f m%s" % [min_y, "  (floats)" if min_y > ftol else ("  (sinks)" if min_y < -ftol else "")]})
	var centre_xz := Vector2(((m.min as Vector3).x + (m.max as Vector3).x) / 2.0, ((m.min as Vector3).z + (m.max as Vector3).z) / 2.0)
	out.append({"id": "origin under the footprint centre (±10 % of each footprint side)",
		"pass": absf(centre_xz.x) <= want.x * 0.10 and absf(centre_xz.y) <= want.z * 0.10,
		"observed": "footprint centre at x=%+.3f, z=%+.3f m" % [centre_xz.x, centre_xz.y]})
	out.append({"id": "triangles ≤ %d" % int(spec.max_tris), "pass": m.tris <= int(spec.max_tris), "observed": "%d triangles" % m.tris})
	out.append({"id": "mesh parts ≤ %d basic shapes" % int(spec.max_shapes), "pass": m.meshes >= 1 and m.meshes <= int(spec.max_shapes),
		"observed": "%d mesh nodes, %d surfaces (joined objects would hide shape count)" % [m.meshes, m.surfaces]})
	var ctol: float = brief.colour_tolerance
	var missing := []
	for name in spec.colours:
		var target := Color(spec.colours[name])
		var hit := false
		for c in m.colours:
			if absf(c.r - target.r) <= ctol and absf(c.g - target.g) <= ctol and absf(c.b - target.b) <= ctol:
				hit = true
				break
		if not hit:
			missing.append("%s %s" % [name, spec.colours[name]])
	var seen := []
	for c in m.colours:
		seen.append("#" + c.to_html(false))
	out.append({"id": "every briefed colour arrives (albedo within ±%.2f)" % ctol, "pass": missing.is_empty(),
		"observed": ("all %d found" % spec.colours.size() if missing.is_empty() else "missing: " + ", ".join(missing)) + "; seen " + ", ".join(seen)})
	if spec.has("front_check"):
		var part: String = spec.front_check.part
		var found := ""
		for p in m.parts:
			if part in p:
				found = p
		var ok := found != "" and (m.parts[found] as Vector3).x < 0.0
		out.append({"id": "front faces +X: '%s' centre behind the middle (x < 0)" % part, "pass": ok,
			"observed": ("%s centre x = %+.3f m" % [found, (m.parts[found] as Vector3).x]) if found != "" else "no mesh named *%s*" % part})
	return out

static func _all(n: Node) -> Array:
	var out := [n]
	for c in n.get_children():
		out.append_array(_all(c))
	return out
