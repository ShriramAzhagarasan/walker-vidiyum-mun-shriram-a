extends Node
## Dialogue flow, interaction latch and Hari's current state: logic only, no scene nodes.
##
## Thin interface with whatever presentation is loaded (3D now, could be 2D):
##   presentation -> Story : player_x (metres along the deck), nearby_target ("" / "manikandan" /
##                           "krishna"), set_moving(bool) every physics frame.
##   Story -> presentation : hari_state + hari_state_changed, movement_locked(), dialogue signals.
## Keys reach Story through Controls (press_interact / move_choice), never from the scene.

signal hari_state_changed(state: String)
signal dialogue_line(line: Dictionary)        ## a new line is up (choices included)
signal dialogue_choice_moved(index: int)
signal dialogue_closed(conversation_id: String)

const StoryData = preload("res://logic/story_data.gd")
const STATES := ["IDLE", "WALK", "TALK", "PHONE", "NOTES", "OVERHEAR", "STARTLED", "KEYS", "WHITEOUT", "RELIEF"]
const FLASH_SECONDS := {"NOTES": 1.5, "STARTLED": 1.2, "KEYS": 1.5}   ## brief states, queued over the base state
const INTERACTABLES := ["manikandan", "krishna"]
const INTERACT_COOLDOWN := 0.35     ## s after a dialogue closes before E can open another one
const MIN_LINE_SECONDS := 0.15      ## a line stays up at least this long, so mashing can't skip it unseen
const WHITEOUT_DELAY := 1.4         ## s from dawn_crash (headlights) to Hari's WHITEOUT image

var player_x := 0.0
var nearby_target := ""
var hari_state := "IDLE"                 ## what is shown: the front flash if any, else the base state
var _base_state := "IDLE"
var _flashes: Array = []                 ## queue of [state, seconds left]
var dialogue_active := false
var conversation_id := ""
var lines: Array = []
var line_index := 0
var choice_index := 0
var _line_shown_at := 0.0
var _closed_at := -10.0
var _whiteout_in := -1.0

func _ready() -> void:
	var ls: Node = _ls()
	ls.loop_started.connect(_on_loop_started)
	ls.clue_saved.connect(func(_id: String) -> void: flash_state("NOTES"))
	ls.keys_exchanged.connect(_on_keys_exchanged)
	ls.dawn_crash.connect(_on_dawn_crash)
	ls.safe_dawn.connect(_on_safe_dawn)

func _process(delta: float) -> void:
	if _whiteout_in >= 0.0:
		_whiteout_in -= delta
		if _whiteout_in < 0.0:
			set_hari_state("WHITEOUT")
	if not _flashes.is_empty():
		_flashes[0][1] -= delta
		if _flashes[0][1] <= 0.0:
			_flashes.pop_front()
			_refresh_state()

# --- presentation -> logic --------------------------------------------------------

func set_moving(moving: bool) -> void:
	if not movement_locked():
		set_hari_state("WALK" if moving else "IDLE")

func movement_locked() -> bool:
	return dialogue_active or flash_active() or _ls().phase != _ls().Phase.NIGHT

func can_interact() -> bool:
	return nearby_target in INTERACTABLES and not movement_locked()

func flash_active() -> bool:
	return not _flashes.is_empty()

## Show a brief state (NOTES / STARTLED / KEYS) for its FLASH_SECONDS, after any already queued.
func flash_state(state: String) -> void:
	_flashes.append([state, FLASH_SECONDS[state]])
	_refresh_state()

# --- keys (via Controls) ----------------------------------------------------------

## One fresh E/Space press. Advances an open dialogue, or opens a talk with the nearby NPC.
func press_interact() -> void:
	if dialogue_active:
		_advance()
		return
	if not can_interact() or _now() - _closed_at < INTERACT_COOLDOWN:
		return
	match nearby_target:
		"manikandan":
			var topic: String = _ls().talk_to_manikandan()
			if topic != "":
				start_conversation(topic)
		"krishna":
			start_conversation("krishna_ambient_repeat" if _ls().loop_index >= 2 else "krishna_ambient")

func move_choice(step: int) -> void:
	var choices := current_choices()
	if choices.is_empty():
		return
	choice_index = posmod(choice_index + step, choices.size())
	dialogue_choice_moved.emit(choice_index)

# --- dialogue ---------------------------------------------------------------------

func start_conversation(id: String) -> void:
	lines = StoryData.conversation(id)
	if lines.is_empty():
		return
	conversation_id = id
	line_index = 0
	dialogue_active = true
	_ls().talking = true
	_show_line()

func current_line() -> Dictionary:
	return lines[line_index] if dialogue_active and line_index < lines.size() else {}

func current_choices() -> Array:
	return current_line().get("choices", [])

func choice_labels() -> Array:
	return current_choices().map(func(c: Dictionary) -> String: return c.get("label", ""))

## Sets the base state (held states); a running flash still shows on top until it ends.
func set_hari_state(state: String) -> void:
	if state in STATES:
		_base_state = state
		_refresh_state()

func _refresh_state() -> void:
	var shown: String = _flashes[0][0] if not _flashes.is_empty() else _base_state
	if shown != hari_state:
		hari_state = shown
		hari_state_changed.emit(shown)

func _advance() -> void:
	if _now() - _line_shown_at < MIN_LINE_SECONDS:
		return
	var choices := current_choices()
	if not choices.is_empty():
		var action: String = choices[choice_index].get("action", "")
		if action == "ask_selvam" and _ls().ask_selvam_available():
			start_conversation("mani_ask_selvam")
		else:
			start_conversation("mani_never_mind")
		return
	line_index += 1
	if line_index >= lines.size():
		_close(true)
	else:
		_show_line()

func _show_line() -> void:
	choice_index = 0
	_line_shown_at = _now()
	var line := current_line()
	set_hari_state(line.get("hari_state", "TALK"))
	dialogue_line.emit(line)

func _close(normal_end: bool) -> void:
	if not dialogue_active:
		return
	dialogue_active = false
	_ls().talking = false
	lines = []
	_closed_at = _now()
	if normal_end and _ls().phase == _ls().Phase.NIGHT:
		# Outcomes land when the conversation has been heard to the end (flashes queue first,
		# so IDLE only shows once they finish).
		if conversation_id == "mani_overhear":
			_ls().finish_overhearing()           # -> clue_saved -> NOTES
		elif conversation_id == "mani_ask_selvam":
			_ls().ask_about_selvam()             # -> keys_exchanged -> KEYS, then clue_saved -> NOTES
		set_hari_state("IDLE")
	dialogue_closed.emit(conversation_id)

# --- LoopState events -------------------------------------------------------------

func _on_loop_started(index: int) -> void:
	_whiteout_in = -1.0
	_flashes.clear()
	_close(false)
	if index >= 2:
		flash_state("STARTLED")                  # the wake-up: at least ~1.2 s before PHONE shows
	set_hari_state("IDLE")
	start_conversation("amma_call_repeat" if index >= 2 else "amma_call_first")

func _on_keys_exchanged(_from: String, to: String) -> void:
	if to == "manikandan":
		flash_state("KEYS")

func _on_dawn_crash() -> void:
	_flashes.clear()
	_close(false)
	_refresh_state()
	_whiteout_in = WHITEOUT_DELAY

func _on_safe_dawn() -> void:
	_flashes.clear()
	_close(false)
	set_hari_state("RELIEF")

func _ls() -> Node:
	return get_node("/root/LoopState")

func _now() -> float:
	return Time.get_ticks_msec() / 1000.0
