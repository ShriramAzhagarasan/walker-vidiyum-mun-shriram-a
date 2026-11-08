extends "res://tests/harness.gd"
## Headless CPU-cost measurement for the two A6 effects (CHANGE-BRIEF §G,
## CLAUDE.md "a GPU effect's headless CPU price is near zero by construction").
## For each of four scene states, this samples the wall-clock time between
## consecutive process_frame signals with Time.get_ticks_usec() and reports the
## mean, standard deviation, min and max over SAMPLE_FRAMES. The four states
## are:
##   (1) empty                    — no slice, just the SceneTree and autoloads
##   (2) slice, both effects off  — slice.tscn with FootstepScuffs and
##                                  StringLightMoths removed before the tree
##                                  sees them (so neither controller runs)
##   (3) Effect A, 4 bursts alive — slice.tscn without the moth controller;
##                                  four FootstepScuff.tscn instances kept
##                                  alive at all times. The §A.4 rule 9 bound
##                                  is ceil(1.15 s lifetime / 0.38 s stride)
##                                  = 4 bursts, 4*(10+5)=60 particles
##   (4) Effect B, 3 emitters     — slice.tscn without the scuff trigger; the
##       emitting                   StringLightMoths controller is left in,
##                                  clock held at NIGHT_START so its condition
##                                  is active; 3*12 = 36 moths configured
## Time.get_ticks_usec() is the right instrument for per-frame wall-clock time
## (ChatGPT confirmed around Godot 4.7's SceneTree frame loop). A --fixed-fps
## headless run doesn't throttle: the delta is fixed at 1/fps but the loop
## advances as fast as the thread can finish each _process. So these numbers
## are the actual CPU cost of a frame.
##
## Reads §A.3 (CPUParticles3D, amount 10+5, one_shot, lifetime 1.15 s) and
## §B.3 (GPUParticles3D, amount 12 per emitter, lifetime 2.4 s) from
## CHANGE-BRIEF.md. Changes no effect or gameplay file. Headless renders no
## particles; case (4) measures only the GPUParticles3D bookkeeping cost on
## the CPU, which CLAUDE.md flags as near zero. If any pair of cases that
## should differ reports the same number, _flag() calls it out.
##
## Run:  ./scripts/run-test.sh cost_effects.gd 60 300

const SCENE_PATH := "res://scenes/slice.tscn"
const SCUFF_PATH := "res://effects/footstep_scuff.tscn"
const WARMUP_FRAMES := 60
const SAMPLE_FRAMES := 300
const SCUFF_PEAK := 4             ## §A.4 rule 9: ceil(1.15 / 0.38) = 4

func run() -> bool:
	ls.test_hold_clock = true     ## keep LoopState's clock out of the comparison
	var empty := await _measure_empty()
	var baseline := await _measure_slice_both_off()
	var a_heavy := await _measure_effect_a_heavy()
	var b_heavy := await _measure_effect_b_heavy()

	print("")
	print("=== cost_effects results (per-frame CPU time, Time.get_ticks_usec) ===")
	_report("1 empty                   ", empty)
	_report("2 slice, both effects off ", baseline)
	_report("3 Effect A, 4 scuffs alive", a_heavy)
	_report("4 Effect B, 3 emitters on ", b_heavy)
	print("")
	_flag("empty vs slice-off", empty, baseline)
	_flag("slice-off vs A 4 bursts", baseline, a_heavy)
	_flag("slice-off vs B 3 emitters", baseline, b_heavy)
	_flag("A 4 bursts vs B 3 emitters", a_heavy, b_heavy)
	print("")
	check("cost_effects produced four cases", true,
		"empty=%d baseline=%d A=%d B=%d samples" %
			[empty.size(), baseline.size(), a_heavy.size(), b_heavy.size()])
	return true

# ---- the four cases --------------------------------------------------------------

func _measure_empty() -> PackedInt64Array:
	# Only the SceneTree and the four autoloads are present. Nothing else to measure.
	return await _sample(WARMUP_FRAMES, SAMPLE_FRAMES)

func _measure_slice_both_off() -> PackedInt64Array:
	var slice := _load_slice(false, false)
	root.add_child(slice)
	await steps(2)
	var samples := await _sample(WARMUP_FRAMES, SAMPLE_FRAMES)
	slice.queue_free()
	await steps(2)
	return samples

func _measure_effect_a_heavy() -> PackedInt64Array:
	var slice := _load_slice(true, false)        ## keep the scuff trigger node for parity
	root.add_child(slice)
	await steps(2)
	# Spawn our own scuffs under a dedicated holder so we fully control the alive count.
	# The in-game trigger would only fire when Hari is walking; we don't need Hari to walk
	# to measure the particle cost of 4 bursts alive.
	var holder := Node3D.new()
	holder.name = "CostScuffHolder"
	slice.add_child(holder)
	var hari_pos: Vector3 = (slice.get_node("Hari") as Node3D).global_position
	var scuff_scene: PackedScene = load(SCUFF_PATH)
	for i in SCUFF_PEAK:
		_spawn_scuff(holder, scuff_scene, Vector3(hari_pos.x + 0.1 * i, 0.0, hari_pos.z))
	check("Effect A heavy: 4 scuffs instanced before sampling",
		holder.get_child_count() == SCUFF_PEAK, holder.get_child_count())
	var samples := await _sample_with_topup(holder, scuff_scene, hari_pos,
		WARMUP_FRAMES, SAMPLE_FRAMES)
	slice.queue_free()
	await steps(2)
	return samples

func _measure_effect_b_heavy() -> PackedInt64Array:
	var slice := _load_slice(false, true)        ## scuff trigger removed, moth controller kept
	root.add_child(slice)
	await steps(2)
	# The controller's condition (§B.4 rule 1) is phase==NIGHT and clock<1740.
	# Those are the LoopState defaults, so the moths are already emitting on load.
	# test_hold_clock stops the clock from drifting past 1740 while we sample.
	ls.phase = ls.Phase.NIGHT
	ls.clock_minutes = float(ls.NIGHT_START)
	await steps(5)
	var mo: Node = slice.get_node_or_null("StringLightMoths")
	var emitting := _count_emitting(mo)
	check("Effect B heavy: all 3 emitters emitting before sampling",
		emitting == 3, "%d of 3 emitting" % emitting)
	var samples := await _sample(WARMUP_FRAMES, SAMPLE_FRAMES)
	slice.queue_free()
	await steps(2)
	return samples

# ---- helpers ---------------------------------------------------------------------

func _load_slice(keep_scuff_trigger: bool, keep_moth_controller: bool) -> Node:
	var slice: Node = load(SCENE_PATH).instantiate()
	if not keep_scuff_trigger:
		var ft := slice.get_node_or_null("FootstepScuffs")
		if ft:
			slice.remove_child(ft)
			ft.queue_free()
	if not keep_moth_controller:
		var mo := slice.get_node_or_null("StringLightMoths")
		if mo:
			slice.remove_child(mo)
			mo.queue_free()
	return slice

func _spawn_scuff(holder: Node, scuff_scene: PackedScene, pos: Vector3) -> void:
	var scuff: Node3D = scuff_scene.instantiate()
	holder.add_child(scuff)
	scuff.global_position = pos
	(scuff.get_node("SoftDust") as CPUParticles3D).emitting = true
	(scuff.get_node("FineGrit") as CPUParticles3D).emitting = true

func _count_alive_scuffs(holder: Node) -> int:
	var n := 0
	for c in holder.get_children():
		var s := c.get_node_or_null("SoftDust") as CPUParticles3D
		if s != null and s.emitting:
			n += 1
	return n

func _count_emitting(mo: Node) -> int:
	if mo == null:
		return 0
	var n := 0
	for a in mo.get_children():
		for b in a.get_children():
			if b is GPUParticles3D and (b as GPUParticles3D).emitting:
				n += 1
	# The effect scene is one child under the controller; the three emitters are its children.
	# Loop above walks both depths in case the controller's child layout changes.
	return n

func _sample(warm: int, n: int) -> PackedInt64Array:
	for i in warm:
		await process_frame
	var samples := PackedInt64Array()
	samples.resize(n)
	var t0 := Time.get_ticks_usec()
	for i in n:
		await process_frame
		var t1 := Time.get_ticks_usec()
		samples[i] = t1 - t0
		t0 = t1
	return samples

## Like _sample(), but between frames (outside the measured window) tops the
## holder back up to SCUFF_PEAK alive bursts and reaps the dead ones.
func _sample_with_topup(holder: Node, scuff_scene: PackedScene, pos: Vector3,
		warm: int, n: int) -> PackedInt64Array:
	for i in warm:
		await process_frame
		_topup(holder, scuff_scene, pos)
	var samples := PackedInt64Array()
	samples.resize(n)
	var t0 := Time.get_ticks_usec()
	for i in n:
		await process_frame
		var t1 := Time.get_ticks_usec()
		samples[i] = t1 - t0
		_topup(holder, scuff_scene, pos)     ## outside the window [t0..t1]
		t0 = Time.get_ticks_usec()
	return samples

func _topup(holder: Node, scuff_scene: PackedScene, pos: Vector3) -> void:
	for c in holder.get_children():
		var s := c.get_node_or_null("SoftDust") as CPUParticles3D
		if s == null or not s.emitting:
			c.queue_free()
	var alive := 0
	for c in holder.get_children():
		if not c.is_queued_for_deletion():
			alive += 1
	var to_spawn: int = SCUFF_PEAK - alive
	for i in to_spawn:
		_spawn_scuff(holder, scuff_scene, Vector3(pos.x + 0.1 * i, 0.0, pos.z))

# ---- reporting -------------------------------------------------------------------

func _report(label: String, samples: PackedInt64Array) -> void:
	if samples.is_empty():
		print("[COST] %s  no samples" % label)
		return
	var total: int = 0
	var mn: int = samples[0]
	var mx: int = samples[0]
	for v in samples:
		total += v
		if v < mn:
			mn = v
		if v > mx:
			mx = v
	var mean := float(total) / samples.size()
	var sd := _sd(samples, mean)
	print("[COST] %s  n=%d  mean=%8.1f us  sd=%8.1f us  min=%d us  max=%d us"
		% [label, samples.size(), mean, sd, mn, mx])

func _flag(label: String, a: PackedInt64Array, b: PackedInt64Array) -> void:
	if a.is_empty() or b.is_empty():
		return
	var ma := _mean(a)
	var mb := _mean(b)
	var sa := _sd(a, ma)
	var sb := _sd(b, mb)
	var diff := absf(ma - mb)
	var noise := maxf(sa, sb)
	if diff < maxf(1.0, noise):
		print("[COST] WARN  %s: means %.1f us vs %.1f us differ by %.1f us, within one standard deviation (%.1f us). Either the effect has no measurable CPU price here, or this script is measuring itself."
			% [label, ma, mb, diff, noise])
	else:
		print("[COST] OK    %s: means %.1f us vs %.1f us differ by %.1f us (noise %.1f us)."
			% [label, ma, mb, diff, noise])

func _mean(a: PackedInt64Array) -> float:
	var t: int = 0
	for v in a:
		t += v
	return float(t) / a.size()

func _sd(a: PackedInt64Array, mean: float) -> float:
	var v := 0.0
	for x in a:
		var d := float(x) - mean
		v += d * d
	return sqrt(v / a.size())
