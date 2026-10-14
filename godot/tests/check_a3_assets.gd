extends SceneTree
## A3 headless asset check: loads each .glb named in tests/data/a3_brief.json, places it at
## the origin on the floor, and compares what arrived with the brief (size, upright, node
## scale, base height, origin, triangles, shape count, colours, SUV front).
## Run (Module 3 form):
##   timeout 120 godot --headless --path godot --script res://tests/check_a3_assets.gd --fixed-fps 60
## Exit 0 only if every check passes. A pass proves the numbers arrived as measured; it does
## not prove the asset looks right, reads as what it is, or suits the game. That is human work.

const Measure = preload("res://tests/a3_measure.gd")
const BRIEF := "res://tests/data/a3_brief.json"

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var brief: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BRIEF))
	var checks := 0
	var failures := 0
	var report := {"engine": Engine.get_version_info().string, "brief": BRIEF, "assets": {}}
	print("A3 asset check · %s · brief %s" % [Engine.get_version_info().string, BRIEF])
	for id in brief.assets:
		var spec: Dictionary = brief.assets[id]
		print("\n== %s  (%s)" % [id, spec.glb])
		var rows := []
		if not ResourceLoader.exists(spec.glb):
			rows = [{"id": "imported .glb exists", "pass": false, "observed": "missing; run --import after exporting"}]
		else:
			var packed := load(spec.glb) as PackedScene
			var node: Node3D = packed.instantiate() if packed else null
			if node == null:
				rows = [{"id": "imported .glb instantiates as Node3D", "pass": false, "observed": str(packed)}]
			else:
				root.add_child(node)            # at the origin, on the floor (y = 0)
				await process_frame
				var m := Measure.measure(node)
				rows = [{"id": "imported .glb instantiates", "pass": true, "observed": "%d mesh nodes" % m.meshes}]
				rows.append_array(Measure.evaluate(m, spec, brief))
				report.assets[id] = {"size": [m.size.x, m.size.y, m.size.z], "min_y": m.min.y, "tris": m.tris, "meshes": m.meshes}
				node.queue_free()
		for r in rows:
			checks += 1
			if not r.pass:
				failures += 1
			print("[%s] %s   %s" % ["PASS" if r.pass else "FAIL", r.id, r.observed])
		report.assets[id] = report.assets.get(id, {})
		report.assets[id]["rows"] = rows
	report.checks = checks
	report.failures = failures
	var out := ProjectSettings.globalize_path("res://../evidence/a3")
	DirAccess.make_dir_recursive_absolute(out)
	var f := FileAccess.open(out + "/check-a3-%d.json" % int(Time.get_unix_time_from_system()), FileAccess.WRITE)
	f.store_string(JSON.stringify(report, "  "))
	f.close()
	print("\ncheck_a3_assets.gd: %d checks, %d failed -> %s" % [checks, failures, "PASS" if failures == 0 else "FAIL"])
	quit(0 if failures == 0 else 1)
