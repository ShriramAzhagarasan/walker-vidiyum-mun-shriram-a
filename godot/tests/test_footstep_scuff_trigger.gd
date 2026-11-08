extends "res://tests/harness.gd"
## A6 Effect A state test (CHANGE-BRIEF §A.4 rules 8, 9 and the "level unloaded" half of rule 10).
## Drives res://scenes/slice.tscn through real keys: D for walk, E to close Amma's call
## (Story._now() gates E on wall-clock, so each tap is preceded by OS.delay_msec(400) as
## test_night_skip.gd does), P for pause. Watches FootstepScuffs' child count to see when the
## trigger instances the scene. The "Hari freed while the level persists" half of rule 10 is not
## probed here because slice.gd._process and camera_rig.gd dereference hari every frame and
## crash the running scene the moment Hari is queue_freed; the trigger's own guard
## (`is_instance_valid(_hari)` in `_process`) is visible in the trigger source. The "entire
## level unloaded" half is exercised by the final slice.queue_free(). Headless does not render
## particles; this proves the trigger's rules, not the look (CHANGE-BRIEF §D).
## Run:  ./scripts/run-test.sh test_footstep_scuff_trigger.gd 60

const SCENE := "res://scenes/slice.tscn"
const FLOOR_TOL := 0.01
const XZ_TOL := 0.08      ## one 60-fps frame of walking at 2.2 m/s plus a little slack

func run() -> bool:
	ls.test_hold_clock = true
	var slice: Node = load(SCENE).instantiate()
	root.add_child(slice)
	await steps(1)

	var trigger: Node3D = slice.get_node_or_null("FootstepScuffs")
	check("FootstepScuffs container present in slice.tscn", trigger != null, trigger)
	if trigger == null:
		slice.queue_free()
		await steps(1)
		return true

	# Rule 8: must not fire on scene load.
	check("no scuff at scene load (frame 1, before any input)",
		trigger.get_child_count() == 0, trigger.get_child_count())

	var hari: CharacterBody3D = slice.get_node("Hari")

	# Rule 8: must not fire while movement is blocked by dialogue (Amma's call is open on load).
	check("Amma's call is active on load", story.dialogue_active, story.conversation_id)
	check("movement is locked on load", story.movement_locked(), story.movement_locked())
	var before_locked := trigger.get_child_count()
	key(KEY_D, true)
	await steps(30)
	key(KEY_D, false)
	await steps(2)
	check("no scuff while dialogue locks movement (D held 30 frames)",
		trigger.get_child_count() == before_locked and story.dialogue_active,
		"%d children, dialogue=%s" % [trigger.get_child_count(), story.dialogue_active])

	# Close Amma's call with real E presses (same pattern as test_night_skip.gd rule_other_phase).
	for i in 30:
		if not story.dialogue_active:
			break
		OS.delay_msec(400)
		await tap(KEY_E)
		await steps(2)
	check("Amma's call closed through real E presses",
		not story.dialogue_active, story.conversation_id)

	# Rule 8: must not fire while standing still.
	var idle_before := trigger.get_child_count()
	await steps(60)
	check("no scuff while standing still (60 frames idle after dialogue)",
		trigger.get_child_count() == idle_before,
		"%d (was %d)" % [trigger.get_child_count(), idle_before])

	# Rule 8: fires on every actual footfall during WALK, at Hari's floor projection.
	var walk_start := trigger.get_child_count()
	var walk_start_x := hari.global_position.x
	var fires: Array = []
	var seen := walk_start
	# Exact count (Claude's review): every scuff that enters the container, against the contacts in Hari's walked distance.
	var entered := [0]
	trigger.child_entered_tree.connect(func(_n: Node) -> void: entered[0] += 1)
	var travel_start := float(hari.get("_travel"))
	key(KEY_D, true)
	for i in 180:
		await steps(1)
		var n := trigger.get_child_count()
		while seen < n:
			var inst := trigger.get_child(seen) as Node3D
			fires.append({"inst": inst, "x": inst.global_position.x,
				"y": inst.global_position.y, "z": inst.global_position.z,
				"hari_x": hari.global_position.x, "hari_z": hari.global_position.z})
			seen += 1
		if fires.size() >= 3:
			break
	var contacts := _contacts(float(hari.get("_travel"))) - _contacts(travel_start)
	check("exactly one scuff per footfall (rule 8, never otherwise)",
		entered[0] == contacts and contacts >= 3,
		"%d scuffs for %d contacts in %.2f m walked" % [entered[0], contacts, float(hari.get("_travel")) - travel_start])
	key(KEY_D, false)
	await steps(2)
	check("walking fired >= 3 scuffs (rule 8: once per footfall)",
		fires.size() >= 3,
		"%d fires in %.2f m of walk" % [fires.size(), hari.global_position.x - walk_start_x])

	if fires.size() >= 1:
		var f0: Dictionary = fires[0]
		check("fire 0 Y = 0 (floor projection, rule 8)",
			absf(f0["y"]) <= FLOOR_TOL, f0["y"])
		check("fire 0 XZ within %.2f m of Hari (rule 8: Hari's world position)" % XZ_TOL,
			absf(f0["x"] - f0["hari_x"]) <= XZ_TOL and absf(f0["z"] - f0["hari_z"]) <= XZ_TOL,
			"fire(%.3f,%.3f) vs hari(%.3f,%.3f)"
				% [f0["x"], f0["z"], f0["hari_x"], f0["hari_z"]])

	# Rule 9: two contacts within one lifetime (1.15 s) produce overlapping instances.
	if fires.size() >= 2:
		var inst0: Node3D = fires[0]["inst"]
		var inst1: Node3D = fires[1]["inst"]
		check("fires 0 and 1 are distinct instances (new per footfall, not reset)",
			inst0 != inst1, "%s vs %s" % [inst0, inst1])
		check("fire 0 still alive when fire 1 arrives (overlap, not replaced)",
			is_instance_valid(inst0) and is_instance_valid(inst1),
			"inst0=%s inst1=%s" % [is_instance_valid(inst0), is_instance_valid(inst1)])

	# Rule 8: paused tree -> no new scuffs even with D held.
	var paused_before := trigger.get_child_count()
	await tap(KEY_P)
	await steps(2)
	check("P paused the tree", paused, paused)
	key(KEY_D, true)
	await steps(30)
	key(KEY_D, false)
	check("no new scuffs while paused (30 frames with D held)",
		trigger.get_child_count() == paused_before and paused,
		"%d (was %d)" % [trigger.get_child_count(), paused_before])
	await tap(KEY_P)
	await steps(2)
	check("P unpaused the tree", not paused, paused)

	# Rule 10 (level unloaded): freeing the slice frees the trigger's container and its scuff
	# children together, with no stray references.
	slice.queue_free()
	await steps(2)
	check("slice (and FootstepScuffs with it) freed cleanly",
		not is_instance_valid(trigger), trigger)
	return true

## Footfalls up to `travel` metres: contact at _travel / STRIDE_M = 2k + 0.5 (hari.gd:74-75).
func _contacts(travel: float) -> int:
	return int(floor((travel - 0.21) / 0.84))
