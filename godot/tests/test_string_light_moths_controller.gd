extends "res://tests/harness.gd"
## A6 Effect B state test (CHANGE-BRIEF §B.4 rules 1-5). Loads res://scenes/slice.tscn
## and drives the condition the same way the running game does: real P pauses,
## moths.visible toggles, and real T held through the harness pushes clock_minutes
## past 1740 through LoopState._process (the same path the game uses). Amma's call
## is closed with spaced real E taps first (Story._now() gates E on wall-clock,
## same mechanism as test_night_skip.gd). The effect scene owns amount (12) and
## amount_ratio (1.0); the controller only toggles emitting and visible, and the
## test asserts amount and amount_ratio are unchanged across the whole run.
## Headless draws nothing: this proves the controller's rules, never the look
## (CHANGE-BRIEF §D).
## Run:  ./scripts/run-test.sh test_string_light_moths_controller.gd 60

const SCENE := "res://scenes/slice.tscn"
const LIFETIME_S := 2.4
const DAWN_MINUTE := 1740.0

func run() -> bool:
	ls.test_hold_clock = true
	var slice: Node = load(SCENE).instantiate()
	root.add_child(slice)
	await steps(2)

	var moths: Node3D = slice.get_node_or_null("StringLightMoths") as Node3D
	check("StringLightMoths container present in slice.tscn", moths != null, moths)
	if moths == null:
		slice.queue_free()
		await steps(1)
		return true

	var emitters: Array[GPUParticles3D] = []
	_gather(moths, emitters)
	check("3 GPUParticles3D under the controller", emitters.size() == 3, emitters.size())
	if emitters.size() != 3:
		slice.queue_free()
		await steps(1)
		return true

	# --- Rule 1 + 5: active at scene load (phase NIGHT, clock 1200 < 1740) ---------
	check("rule 1: phase == NIGHT at load", ls.phase == ls.Phase.NIGHT, ls.phase)
	check("rule 1: clock_minutes < 1740 at load",
		ls.clock_minutes < DAWN_MINUTE, ls.clock_minutes)
	check("rule 1 + 5: controller visible at load", moths.visible, moths.visible)
	for e in emitters:
		check("rule 1 + 5: %s.emitting == true at load" % e.name, e.emitting, e.emitting)
		check("rule 1 + 5: %s.amount == 12 (scene value, not touched)" % e.name,
			e.amount == 12, e.amount)
		check("rule 1 + 5: %s.amount_ratio == 1.0 (scene value, not touched)" % e.name,
			is_equal_approx(e.amount_ratio, 1.0), e.amount_ratio)

	# --- Rule 3: pause freezes (real P key, PROCESS_MODE_PAUSABLE on emitters) -----
	var pre_pause := _snapshot(emitters)
	await tap(KEY_P)
	await steps(2)
	check("rule 3: real P paused the tree", paused, paused)
	for e in emitters:
		check("rule 3: %s.can_process() == false while paused" % e.name,
			not e.can_process(), e.can_process())
	await steps(30)
	var during_pause := _snapshot(emitters)
	check("rule 3: emitter state byte-equal across 30 paused frames",
		during_pause == pre_pause, "pre=%s during=%s" % [pre_pause, during_pause])
	await tap(KEY_P)
	await steps(2)
	check("rule 3: real P unpaused the tree", not paused, paused)
	for e in emitters:
		check("rule 3: %s.emitting still true after unpause" % e.name, e.emitting, e.emitting)

	# --- Rule 4: hide stops emission; show while active restarts (preprocess) ------
	moths.visible = false
	await steps(2)
	for e in emitters:
		check("rule 4 (hide): %s.emitting == false while hidden" % e.name,
			not e.emitting, e.emitting)
		check("rule 4 (hide): %s.amount == 12 unchanged" % e.name, e.amount == 12, e.amount)
		check("rule 4 (hide): %s.amount_ratio == 1.0 unchanged" % e.name,
			is_equal_approx(e.amount_ratio, 1.0), e.amount_ratio)
	moths.visible = true
	await steps(2)
	for e in emitters:
		check("rule 4 (show, active): %s.emitting == true again" % e.name,
			e.emitting, e.emitting)

	# --- Rule 2: real T held past clock 1740, after real E closes Amma's call ------
	# Story._now() gates E on wall-clock; spaced delay_msec(400) matches
	# test_night_skip.gd rule_other_phase.
	ls.test_hold_clock = false
	for i in 30:
		if not story.dialogue_active:
			break
		OS.delay_msec(400)
		await tap(KEY_E)
		await steps(2)
	check("Amma's call closed through real E presses",
		not story.dialogue_active, story.conversation_id)

	key(KEY_T, true)
	var deadline := 10000
	while ls.clock_minutes < DAWN_MINUTE and deadline > 0:
		if story.dialogue_active:
			OS.delay_msec(400)
			await tap(KEY_E)
		await steps(1)
		deadline -= 1
	key(KEY_T, false)
	check("rule 2: clock_minutes reached 1740 under real T (fast-forward)",
		ls.clock_minutes >= DAWN_MINUTE,
		"clock=%.2f, phase=%d" % [ls.clock_minutes, ls.phase])
	check("rule 2: phase still NIGHT at the 1740 cutoff (dawn phase is 1790)",
		ls.phase == ls.Phase.NIGHT, ls.phase)
	# Freeze the clock at >= 1740 so condition stays inactive through the fade wait;
	# dawn at 1790 would otherwise flip phase to CRASH mid-fade.
	ls.test_hold_clock = true
	await steps(2)
	for e in emitters:
		check("rule 2: %s.emitting == false after clock >= 1740" % e.name,
			not e.emitting, e.emitting)
		check("rule 2: %s.amount == 12 still (no mutation)" % e.name,
			e.amount == 12, e.amount)
		check("rule 2: %s.amount_ratio == 1.0 still (no mutation)" % e.name,
			is_equal_approx(e.amount_ratio, 1.0), e.amount_ratio)
	check("rule 2: container still visible immediately after cutoff (2.4 s fade in flight)",
		moths.visible, moths.visible)

	# Rule 2: container hides after one emitter lifetime (2.4 s) of pausable game time.
	var hid: bool = await wait_until(func() -> bool: return not moths.visible, 5.0)
	check("rule 2: controller hid the group after the 2.4 s lifetime (game time, pausable)",
		hid, "visible=%s, _fade_remaining=%s" % [moths.visible, moths.get("_fade_remaining")])
	for e in emitters:
		check("rule 2: %s.emitting still false after the fade" % e.name,
			not e.emitting, e.emitting)
		check("rule 2: %s.amount == 12 still (no mutation across the whole run)" % e.name,
			e.amount == 12, e.amount)
		check("rule 2: %s.amount_ratio == 1.0 still (no mutation across the whole run)" % e.name,
			is_equal_approx(e.amount_ratio, 1.0), e.amount_ratio)

	# --- Rule 4: show while inactive stays off -------------------------------------
	moths.visible = true
	await steps(2)
	for e in emitters:
		check("rule 4 (show, inactive): %s.emitting == false (clock still >= 1740)" % e.name,
			not e.emitting, e.emitting)

	slice.queue_free()
	await steps(2)
	return true

func _gather(n: Node, out: Array[GPUParticles3D]) -> void:
	for c in n.get_children():
		if c is GPUParticles3D:
			out.append(c)
		_gather(c, out)

func _snapshot(emitters: Array[GPUParticles3D]) -> Array:
	var rows := []
	for e in emitters:
		rows.append([e.emitting, e.amount, e.amount_ratio, e.visible])
	return rows
