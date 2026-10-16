extends SceneTree
## Tests the A3 check itself: builds stand-ins from Godot's own BoxMesh (no Blender, no .glb)
## that are correct, then deliberately broken in the ways the brief predicts (A3-F1..F7),
## and confirms check_a3's measurement flags each one. A check that cannot fail proves nothing.
## Run: timeout 120 godot --headless --path godot --script res://tests/check_a3_selftest.gd --fixed-fps 60

const Measure = preload("res://tests/a3_measure.gd")
var checks := 0
var failures := 0

func _initialize() -> void:
	call_deferred("_run")

func _box(parent: Node3D, name: String, size: Vector3, centre: Vector3, colour: Color) -> void:
	var mi := MeshInstance3D.new()
	mi.name = name
	var mesh := BoxMesh.new()
	mesh.size = size
	var mat := StandardMaterial3D.new()
	mat.albedo_color = colour
	mesh.material = mat
	mi.mesh = mesh
	mi.position = centre
	parent.add_child(mi)

## A fence-sized stand-in: two posts, a sign, a rope. Base on y = 0, footprint centred on the origin.
## Colours follow brief revision 3 (wood and rope). With revision 1's steel colours (#8a8f96 posts, #3a3d42 wire)
## this "correct" stand-in failed the colour row after the brief changed, which is the check doing its job.
func _fence() -> Node3D:
	var n := Node3D.new()
	_box(n, "post_a", Vector3(0.12, 2.10, 0.12), Vector3(-1.14, 1.05, 0), Color("#5b4632"))
	_box(n, "post_b", Vector3(0.12, 2.10, 0.12), Vector3(1.14, 1.05, 0), Color("#5b4632"))
	_box(n, "sign", Vector3(0.6, 0.4, 0.04), Vector3(0, 1.2, 0), Color("#c0392b"))
	_box(n, "rope", Vector3(2.40, 0.02, 0.02), Vector3(0, 2.09, 0), Color("#8c7a5b"))
	return n

func _result(node: Node3D, spec: Dictionary, brief: Dictionary) -> Dictionary:
	root.add_child(node)
	await process_frame
	var rows := Measure.evaluate(Measure.measure(node), spec, brief)
	node.queue_free()
	var by := {}
	for r in rows:
		by[r.id] = r.pass
	return by

func expect(case_name: String, by: Dictionary, needle: String, want_pass: bool) -> void:
	var key := ""
	for k in by:
		if needle in k:
			key = k
	checks += 1
	var ok: bool = key != "" and by[key] == want_pass
	if not ok:
		failures += 1
	print("[%s] %s: '%s' %s" % ["PASS" if ok else "FAIL", case_name, needle, "passes" if want_pass else "is caught"])

func _run() -> void:
	var brief: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tests/data/a3_brief.json"))
	var spec: Dictionary = brief.assets.fence_segment
	var good := await _result(_fence(), spec, brief)
	for k in good:
		expect("correct stand-in", good, k, true)
	var n := _fence(); n.position.y = 0.5                    # A3-F3: origin in the middle -> floats
	expect("floating by 0.5 m", await _result(n, spec, brief), "base on the floor", false)
	n = _fence(); n.scale = Vector3(0.1, 0.1, 0.1)           # A3-F2/F4: wrong size, unapplied scale
	var by := await _result(n, spec, brief)
	expect("scaled x0.1", by, "size within", false)
	expect("scaled x0.1", by, "every node scale", false)
	n = _fence(); n.rotation_degrees = Vector3(90, 0, 0)     # A3-F1: lying on its side
	by = await _result(n, spec, brief)
	expect("lying on its side", by, "upright", false)
	expect("lying on its side", by, "root not rotated", false)
	n = _fence()                                              # A3-F6: a colour lost in export
	((n.get_child(2) as MeshInstance3D).mesh.material as StandardMaterial3D).albedo_color = Color.WHITE
	expect("sign colour lost", await _result(n, spec, brief), "colour", false)
	var tight := spec.duplicate(true); tight.max_tris = 40    # A3-F5: over budget (4 boxes = 48 tris)
	expect("over the triangle budget", await _result(_fence(), tight, brief), "triangles", false)
	var suv: Dictionary = brief.assets.suv                    # A3-F7: SUV facing backwards
	var car := Node3D.new()
	_box(car, "chassis", Vector3(4.6, 1.1, 1.9), Vector3(0, 0.55, 0), Color("#2e2d38"))
	_box(car, "cabin", Vector3(2.6, 0.75, 1.8), Vector3(0.6, 1.475, 0), Color("#7d93b8"))   # cabin forward = backwards car
	expect("SUV facing backwards", await _result(car, suv, brief), "front faces +X", false)
	print("\ncheck_a3_selftest.gd: %d checks, %d failed -> %s" % [checks, failures, "PASS" if failures == 0 else "FAIL"])
	quit(0 if failures == 0 else 1)
