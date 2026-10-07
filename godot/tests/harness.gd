extends SceneTree
## Shared headless test helpers: frame stepping, key injection, PASS/FAIL bookkeeping.
## Tests drive the logic layer only (LoopState, Story, Controls, SoundBank autoloads);
## no presentation scene is needed. Run:  "$GODOT" --headless --path godot -s res://tests/<file>.gd

var ls: Node          # LoopState: clock, flags, timeline
var story: Node       # Story: dialogue, interaction latch, Hari's state
var sound: Node       # SoundBank: trigger_counts
var checks := 0
var failures := 0

func _initialize() -> void:
	call_deferred("_run_and_report")

func _run_and_report() -> void:
	await process_frame
	ls = root.get_node_or_null("LoopState")
	story = root.get_node_or_null("Story")
	sound = root.get_node_or_null("SoundBank")
	check("autoloads present", ls != null and story != null and sound != null and root.has_node("Controls"), "%s %s %s" % [ls, story, sound])
	# run() returns true only if it reached its end; a script error makes it return null.
	var completed: Variant = false
	if ls and story and sound:
		completed = await run()
	check("test script ran to completion", completed == true, completed)
	print("")
	var verdict := "PASS"
	if failures > 0:
		verdict = "FAIL"
	print("%s: %d checks, %d failed -> %s" % [get_script().resource_path.get_file(), checks, failures, verdict])
	quit(0 if failures == 0 else 1)

func run() -> bool:
	return true

func check(id: String, passed: bool, observed: Variant = "") -> void:
	checks += 1
	if not passed:
		failures += 1
	print("[%s] %s   %s" % ["PASS" if passed else "FAIL", id, str(observed)])

func steps(n: int) -> void:
	for i in n:
		await physics_frame
		await process_frame

func key(code: Key, pressed: bool, echo := false) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	event.echo = echo
	Input.parse_input_event(event)

func tap(code: Key, hold_frames := 1) -> void:
	key(code, true)
	await steps(hold_frames)
	key(code, false)
	await steps(1)

## 10 presses in 20 frames (~0.33 s): faster than any line or cooldown guard.
func mash(code: Key, presses := 10) -> void:
	for i in presses:
		key(code, true)
		await steps(1)
		key(code, false)
		await steps(1)

## Wait (real frames) until cond is true or `seconds` pass. Returns cond's final value.
func wait_until(cond: Callable, seconds: float) -> bool:
	var deadline := Time.get_ticks_msec() + int(seconds * 1000.0)
	while not cond.call() and Time.get_ticks_msec() < deadline:
		await steps(1)
	return cond.call()

## Advance any open dialogue with spaced E taps until it closes, then wait out any brief
## state (NOTES/KEYS/STARTLED) and the talk cooldown.
func finish_dialogue(max_taps := 20) -> void:
	for i in max_taps:
		if not story.dialogue_active:
			break
		await steps(10)     # past the per-line minimum display time
		await tap(KEY_E)
	await wait_until(func() -> bool: return not story.flash_active(), 5.0)
	await steps(30)         # a player takes longer than the 0.35 s talk cooldown to press again

## The presentation's side of the thin interface, stood in for by the test.
func stand_near(target: String, x := 4.5) -> void:
	story.nearby_target = target
	story.player_x = x
