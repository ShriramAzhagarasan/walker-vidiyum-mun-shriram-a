extends SceneTree
## Gameplay capture driver for the gamedev film (isolated harness copy, NOT part of the game source).
##
## Instantiates the REAL res://scenes/slice.tscn and plays loop 1 and loop 2 only through
## keyboard events (Input.parse_input_event with InputEventKey, physical keycodes from
## logic/input_setup.gd): WASD to walk, E to talk/advance, W/S to move the choice cursor,
## P to pause, and the real T key held to fast-forward the night (x8). It OBSERVES positions,
## the clock and the phase to decide when to press keys, but never teleports Hari, sets the
## clock, sets state, or calls any test_* API.
##
## Every input and every observed game event is logged against the rendered frame
## (frame / 30 = capture seconds under --fixed-fps 30) to ../capture/<take>-inputs.jsonl.
## At the end it asserts the run reached the end card with the expected sound-event
## counts and every Hari state seen, prints "CAPTURE OK", and exits 0. Otherwise it prints
## "CAPTURE FAIL: <reason>" and exits 1.
##
##   Godot --path capture-project --script res://capture_driver.gd --resolution 3840x2160 \
##     --write-movie ../capture/run-01.avi --fixed-fps 30 [-- take=run-01] [-- probe=5]
## User args (after --): take=<name> (log name), probe=<seconds> (stop early, exit 0 with PROBE OK),
## allow_missing_sfx (do not require all five SFX files; for probes before the SFX land).

const FPS := 30.0
const EXPECTED := {"phone_buzz": 2, "clue_saved": 3, "keys_exchanged": 2, "dawn_crash": 1, "safe_dawn": 1}
const ALL_STATES := ["IDLE", "WALK", "TALK", "PHONE", "NOTES", "OVERHEAR", "STARTLED", "KEYS", "WHITEOUT", "RELIEF"]
const KEYS := {"left": KEY_A, "right": KEY_D, "up": KEY_W, "down": KEY_S, "interact": KEY_E,
	"ff": KEY_T, "pause": KEY_P, "enter": KEY_ENTER}
const LINE_HOLD := 3.0          ## seconds a dialogue line stays up before E (readable on screen)
const WALK_TOL := 0.22          ## metres

var slice: Node3D
var intro: Node
var ls: Node
var story: Node
var sound: Node
var hari: Node3D
var cam: Camera3D
var frame := 0
var take := "run-01"
var probe_s := -1.0
var allow_missing_sfx := false
var log_file: FileAccess
var held := {}
var sustained := {}                       ## keys held for walking / fast-forward (not taps)
var reasserts := 0
var states_seen := {}
var failed := ""
var expected_events: Array = []          ## [keycode, pressed] pairs the driver itself sent
var foreign_events := 0

## Watches every key/mouse-button event that reaches the game. Anything the driver did not send
## (a real keyboard press, OS key-repeat, a click) fails the take, so the capture is input-only.
class InputMonitor extends Node:
	var driver
	func _ready() -> void:
		process_mode = Node.PROCESS_MODE_ALWAYS
	func _input(event: InputEvent) -> void:
		if event is InputEventKey:
			var pair := [event.physical_keycode, event.pressed]
			var i: int = driver.expected_events.find(pair)
			if i >= 0 and not event.echo:
				driver.expected_events.remove_at(i)
				return
			driver.foreign(event)
		elif event is InputEventMouseButton:
			driver.foreign(event)

func _initialize() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("take="):
			take = a.substr(5)
		elif a.begins_with("probe="):
			probe_s = float(a.substr(6))
		elif a == "allow_missing_sfx":
			allow_missing_sfx = true
	var out_dir := ProjectSettings.globalize_path("res://").path_join("../capture")
	DirAccess.make_dir_recursive_absolute(out_dir)
	log_file = FileAccess.open(out_dir.path_join(take + "-inputs.jsonl"), FileAccess.WRITE)
	ls = root.get_node("LoopState")
	story = root.get_node("Story")
	sound = root.get_node("SoundBank")
	_connect_observers()
	var monitor := InputMonitor.new()
	monitor.driver = self
	root.add_child(monitor)
	# The project's main scene: title screen + intro motion comic, which itself changes to slice.tscn.
	intro = load(ProjectSettings.get_setting("application/run/main_scene")).instantiate()
	root.add_child(intro)
	current_scene = intro
	process_frame.connect(func() -> void: frame += 1)
	_run()

# --- observers (read-only) ------------------------------------------------------

func _connect_observers() -> void:
	ls.loop_started.connect(func(i: int) -> void: _log("loop_started", {"loop": i}))
	ls.phone_buzz.connect(func() -> void: _log("sfx_event", {"id": "phone_buzz"}))
	ls.clue_saved.connect(func(id: String) -> void: _log("sfx_event", {"id": "clue_saved", "clue": id}))
	ls.keys_exchanged.connect(func(f: String, t: String) -> void: _log("sfx_event", {"id": "keys_exchanged", "from": f, "to": t}))
	ls.advay_arrived.connect(func(took: bool) -> void: _log("advay_arrived", {"took_keys": took}))
	ls.fire_glow.connect(func() -> void: _log("fire_glow", {}))
	ls.dawn_crash.connect(func() -> void: _log("sfx_event", {"id": "dawn_crash"}))
	ls.safe_dawn.connect(func() -> void: _log("sfx_event", {"id": "safe_dawn"}))
	ls.slice_ended.connect(func() -> void: _log("slice_ended", {}))
	ls.pause_changed.connect(func(p: bool) -> void: _log("pause_changed", {"paused": p}))
	story.hari_state_changed.connect(_on_state)
	story.dialogue_line.connect(_on_line)
	story.dialogue_closed.connect(func(id: String) -> void: _log("dialogue_closed", {"conversation": id}))

func _on_state(st: String) -> void:
	states_seen[st] = true
	_log("hari_state", {"state": st, "flip_h": hari.get_node("Sprite").flip_h if hari else false})

func _on_line(line: Dictionary) -> void:
	_log("dialogue_line", {"conversation": story.conversation_id, "line": line.get("id", ""), "speaker": line.get("speaker", "")})

func _clock_text() -> String:
	var total := int(ls.clock_minutes)
	var hour := (total / 60) % 24
	var h12 := hour % 12
	if h12 == 0:
		h12 = 12
	return "%d:%02d %s" % [h12, total % 60, "AM" if hour < 12 else "PM"]

func _log(kind: String, data: Dictionary) -> void:
	var row := {"frame": frame, "t": snappedf(frame / FPS, 0.001), "event": kind, "clock": _clock_text(),
		"loop": ls.loop_index, "x": snappedf(hari.global_position.x, 0.01) if hari else 0.0,
		"z": snappedf(hari.global_position.z, 0.01) if hari else 0.0}
	row.merge(data)
	log_file.store_line(JSON.stringify(row))
	log_file.flush()

# --- keyboard -----------------------------------------------------------------------

func _key(name: String, pressed: bool, sustain := true) -> void:
	if held.get(name, false) == pressed:
		return
	held[name] = pressed
	sustained[name] = pressed and sustain
	var e := InputEventKey.new()
	e.physical_keycode = KEYS[name]
	e.keycode = KEYS[name]
	e.pressed = pressed
	expected_events.append([KEYS[name], pressed])
	Input.parse_input_event(e)
	_log("input", {"key": OS.get_keycode_string(KEYS[name]), "pressed": pressed})

func _tap(name: String) -> void:
	_key(name, true, false)
	await _frames(3)
	_key(name, false)
	await _frames(1)

func _release_moves() -> void:
	for k in ["left", "right", "up", "down"]:
		_key(k, false)

func _frames(n: int) -> void:
	for i in n:
		await process_frame
		_reassert()
		_check_probe()

## If the OS window loses focus, Godot releases every pressed key (Input.release_pressed_events).
## A key the driver is still holding (walking, T) is then pressed again, and the re-press is logged.
func _reassert() -> void:
	for name in sustained:
		if sustained[name] and not Input.is_physical_key_pressed(KEYS[name]):
			var e := InputEventKey.new()
			e.physical_keycode = KEYS[name]
			e.keycode = KEYS[name]
			e.pressed = true
			expected_events.append([KEYS[name], true])
			Input.parse_input_event(e)
			reasserts += 1
			_log("input_reassert", {"key": OS.get_keycode_string(KEYS[name]), "pressed": true})

func _secs(s: float) -> void:
	await _frames(int(round(s * FPS)))

func _check_probe() -> void:
	if probe_s > 0.0 and frame >= int(probe_s * FPS):
		_log("probe_end", {})
		print("PROBE OK frames=%d" % frame)
		quit(0)

func _until(cond: Callable, timeout_s: float, what: String) -> bool:
	var limit := frame + int(timeout_s * FPS)
	while not cond.call():
		if frame > limit:
			_fail("timed out waiting for " + what)
			return false
		await _frames(1)
	return true

## Walk to (x, z) on the deck with WASD, choosing keys from the camera's current basis
## (movement in hari.gd is camera-relative). Observes position only.
func _walk_to(x: float, z: float, what: String) -> void:
	var target := Vector2(x, z)
	var best := INF
	var stuck := 0
	_log("walk_start", {"to": [x, z], "what": what})
	while true:
		var p := Vector2(hari.global_position.x, hari.global_position.z)
		var d := target - p
		if d.length() < WALK_TOL:
			break
		if d.length() < best - 0.02:
			best = d.length()
			stuck = 0
		else:
			stuck += 1
			if stuck > int(4.0 * FPS):
				_release_moves()
				_fail("stuck walking to " + what)
				return
		var r := Vector2(cam.global_basis.x.x, cam.global_basis.x.z).normalized()
		var f := Vector2(-cam.global_basis.z.x, -cam.global_basis.z.z).normalized()
		var dn := d.normalized()
		var ix := dn.dot(r)
		var iy := -dn.dot(f)
		_key("right", ix > 0.38)
		_key("left", ix < -0.38)
		_key("down", iy > 0.38)
		_key("up", iy < -0.38)
		await _frames(1)
	_release_moves()
	_log("walk_end", {"what": what})

## Advance every line of the open conversation with E, holding each line on screen.
func _read_dialogue(hold: float) -> void:
	var guard := 0
	while story.dialogue_active and guard < 12:
		await _secs(hold)
		var before: int = story.line_index
		var conv: String = story.conversation_id
		await _tap("interact")
		await _frames(2)
		if story.dialogue_active and story.line_index == before and story.conversation_id == conv:
			_fail("E did not advance " + conv)
			return
		guard += 1

func foreign(event: InputEvent) -> void:
	foreign_events += 1
	_log("foreign_input", {"event": event.as_text()})
	_fail("foreign input reached the game: " + event.as_text())

func _fail(reason: String) -> void:
	if failed == "":
		failed = reason
		_log("fail", {"reason": reason})
		_finish()                         # stop the take now: a failed route is not footage

# --- the route ------------------------------------------------------------------------

func _run() -> void:
	await _frames(2)                          # autoload _ready() has run by now
	var present := {}
	for id in sound.SFX_IDS:
		present[id] = sound._sfx_players[id].stream != null
	_log("setup", {"engine": Engine.get_version_info().string, "renderer": ProjectSettings.get_setting("rendering/renderer/rendering_method"),
		"sfx_streams_present": present, "music_present": [sound.party.stream != null, sound.gaana.stream != null],
		"probe_s": probe_s, "main_scene": ProjectSettings.get_setting("application/run/main_scene")})
	_log("route", {"step": "title screen, then Enter once; the intro panels run on their own timers"})
	await _secs(3.0)
	await _tap("enter")
	await _until(func() -> bool: return current_scene != null and current_scene.name == "Slice", 60.0, "intro -> slice")
	if failed != "":
		return
	slice = current_scene                     # slice._ready() has called LoopState.begin_slice()
	hari = slice.get_node("Hari")
	cam = slice.get_node("CameraRig/Camera")
	_log("scene", {"scene": "slice"})
	_log("route", {"step": "loop 1: Amma's 8 PM call"})
	await _read_dialogue(LINE_HOLD)
	await _secs(1.0)

	_log("route", {"step": "loop 1: walk the deck to Krishna and talk"})
	await _walk_to(14.3, 1.0, "Krishna")
	await _secs(0.8)
	await _tap("interact")
	await _read_dialogue(3.5)
	await _secs(0.5)

	_log("route", {"step": "loop 1: railing, music crossfade, pause and resume"})
	await _walk_to(22.6, 1.6, "railing")
	await _secs(3.0)
	await _tap("pause")
	await _secs(2.5)
	await _tap("pause")
	await _secs(1.0)

	_log("route", {"step": "loop 1: hold T, walk back to Manikandan at the SUV, wait for 1:21 AM"})
	_key("ff", true)
	await _walk_to(5.4, 0.5, "Manikandan")
	if failed != "":
		_finish()
		return
	await _until(func() -> bool: return ls.clock_minutes >= 25 * 60 + 21, 30.0, "1:21 AM")
	_key("ff", false)
	if ls.clock_minutes >= ls.ADVAY_TIME:
		_fail("fast-forward overshot 1:40 AM")
		_finish()
		return
	await _secs(1.2)
	_log("route", {"step": "loop 1: overhear the Selvam call"})
	await _tap("interact")
	if story.conversation_id != "mani_overhear":
		_fail("expected mani_overhear, got " + story.conversation_id)
		_finish()
		return
	await _read_dialogue(5.5)

	_log("route", {"step": "loop 1: wait at 1x for 1:40 AM, Advay takes the keys"})
	await _until(func() -> bool: return ls.clock_minutes >= ls.ADVAY_TIME, 20.0, "1:40 AM")
	await _secs(10.5)

	_log("route", {"step": "loop 1: hold T to 5:44 AM on the deck, then dawn at 1x"})
	_key("ff", true)
	await _walk_to(11.0, 1.0, "mid deck")
	await _until(func() -> bool: return ls.clock_minutes >= 29 * 60 + 44, 30.0, "5:44 AM")
	_key("ff", false)
	await _until(func() -> bool: return ls.phase == ls.Phase.CRASH, 10.0, "dawn crash")
	await _until(func() -> bool: return ls.loop_index == 2, 8.0, "loop 2")
	if failed != "":
		_finish()
		return

	_log("route", {"step": "loop 2: wake-up and the repeat call"})
	await _frames(1)
	await _read_dialogue(2.4)
	await _secs(1.0)

	_log("route", {"step": "loop 2: walk to Manikandan, choose Ask about Selvam"})
	await _walk_to(5.4, 0.5, "Manikandan")
	await _secs(0.6)
	await _tap("interact")
	if story.conversation_id != "mani_choice":
		_fail("expected mani_choice, got " + story.conversation_id)
		_finish()
		return
	await _secs(2.5)
	await _tap("down")
	await _secs(1.2)
	await _tap("up")
	await _secs(1.5)
	if story.choice_index != 0:
		_fail("choice cursor not on Ask about Selvam")
		_finish()
		return
	await _tap("interact")
	await _frames(2)
	if story.conversation_id != "mani_ask_selvam":
		_fail("expected mani_ask_selvam, got " + story.conversation_id)
		_finish()
		return
	await _read_dialogue(3.2)
	await _secs(4.0)

	_log("route", {"step": "loop 2: hold T to 1:35 AM, then 1:40 at 1x (Advay refused)"})
	_key("ff", true)
	await _until(func() -> bool: return ls.clock_minutes >= 25 * 60 + 35, 30.0, "1:35 AM")
	_key("ff", false)
	await _until(func() -> bool: return ls.clock_minutes >= ls.ADVAY_TIME, 10.0, "1:40 AM")
	await _secs(7.5)

	_log("route", {"step": "loop 2: hold T, walk to the railing, dawn at 1x"})
	_key("ff", true)
	await _walk_to(22.6, 1.6, "railing")
	await _until(func() -> bool: return ls.clock_minutes >= 29 * 60 + 44, 30.0, "5:44 AM")
	_key("ff", false)
	await _until(func() -> bool: return ls.phase == ls.Phase.SAFE_DAWN, 10.0, "safe dawn")
	await _until(func() -> bool: return ls.is_ended(), 8.0, "end card")
	await _secs(4.0)
	_finish()

var _finished := false

func _finish() -> void:
	if _finished:
		return
	_finished = true
	for k in held.keys():
		_key(k, false)
	var counts: Dictionary = sound.trigger_counts.duplicate()
	var missing_states := ALL_STATES.filter(func(s: String) -> bool: return not states_seen.has(s))
	if failed == "":
		if counts != EXPECTED:
			_fail("sound counts %s != expected %s" % [counts, EXPECTED])
		elif not missing_states.is_empty():
			_fail("Hari states never shown: %s" % [missing_states])
		elif not ls.is_ended() or ls.loop_index != 2:
			_fail("end card not reached in loop 2")
	if failed == "" and not allow_missing_sfx:
		for id in sound.SFX_IDS:
			if sound._sfx_players[id].stream == null:
				_fail("SFX file missing: " + id)
	_log("summary", {"counts": counts, "states_seen": states_seen.keys(), "ended": ls.is_ended(), "failed": failed,
		"foreign_events": foreign_events, "reasserts": reasserts, "unmatched_driver_events": expected_events.size()})
	if failed == "":
		print("CAPTURE OK frames=%d seconds=%.2f counts=%s" % [frame, frame / FPS, counts])
		quit(0)
	else:
		print("CAPTURE FAIL: " + failed)
		quit(1)
