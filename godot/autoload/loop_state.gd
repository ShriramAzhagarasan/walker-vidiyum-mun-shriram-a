extends Node
## Game logic for the night: clock, loop counter, knowledge, per-loop flags and the timeline.
## Knows nothing about audio or about the 2D/3D presentation: those only listen to these signals
## and read the queries below. Story (dialogue/interaction) and Controls (keys) sit beside it.
## Every timeline event is latched by a per-loop flag, so it fires exactly once per loop.

signal loop_started(loop_index: int)
signal phone_buzz
signal clue_saved(clue_id: String)
signal keys_exchanged(from_holder: String, to_holder: String)
signal advay_arrived(took_keys: bool)
signal fire_glow
signal dawn_crash
signal safe_dawn
signal slice_ended
signal pause_changed(paused: bool)

enum Phase { NIGHT, CRASH, SAFE_DAWN, ENDED }

# Clock values are minutes after midnight of the party day, so 1:30 AM = 25 * 60 + 30.
const NIGHT_START := 20 * 60              ## 8:00 PM
const NIGHT_END := 29 * 60 + 55           ## 5:55 AM
const NIGHT_REAL_SECONDS := 180.0         ## real seconds for the whole night at 1x
const FAST_FORWARD := 8.0                 ## hold T
const MINUTES_PER_SECOND := (NIGHT_END - NIGHT_START) / NIGHT_REAL_SECONDS
const OVERHEAR_START := 25 * 60 + 20      ## 1:20 AM, Manikandan calls Selvam
const ADVAY_TIME := 25 * 60 + 40          ## 1:40 AM, Advay comes for the keys
const MUSIC_THIN_START := 27 * 60         ## 3:00 AM, party music starts thinning
const FIRE_GLOW_TIME := 28 * 60 + 45      ## 4:45 AM
const DAWN_TIME := 29 * 60 + 50           ## 5:50 AM
const CRASH_RESET_DELAY := 4.0            ## real seconds from dawn_crash to the 8 PM reset
const END_CARD_DELAY := 3.0               ## real seconds from safe_dawn to the end card
const KNOWLEDGE := ["KNOW_SELVAM", "KNOW_KEYS"]

var loop_index := 1
var knowledge := {}                       ## persists across loops
var notes: Array[String] = []             ## phone notes (clue ids), persist across loops
var flags := {}                           ## reset every loop
var clock_minutes := float(NIGHT_START)
var phase := Phase.NIGHT
var keys_holder := "car"                  ## car / manikandan / advay
var talking := false                      ## set by Story while a dialogue is open: freezes the clock
var fast_forward := false                 ## set by Controls while T is held
var running := false
var test_hold_clock := false              ## test-only: stop the clock from moving by itself
var _sequence_time := 0.0

func _ready() -> void:
	_clear_knowledge()
	_reset_loop_flags()

func _process(delta: float) -> void:
	if not running:
		return
	match phase:
		Phase.NIGHT:
			if not talking and not test_hold_clock:
				var speed: float = FAST_FORWARD if fast_forward else 1.0
				_set_clock(clock_minutes + delta * MINUTES_PER_SECOND * speed)
		Phase.CRASH:
			_sequence_time += delta
			if _sequence_time >= CRASH_RESET_DELAY:
				start_loop(loop_index + 1)
		Phase.SAFE_DAWN:
			clock_minutes = minf(clock_minutes + delta * MINUTES_PER_SECOND, NIGHT_END)
			_sequence_time += delta
			if _sequence_time >= END_CARD_DELAY:
				phase = Phase.ENDED
				slice_ended.emit()

# --- loop control ---------------------------------------------------------------

## Fresh slice: loop 1 with all knowledge cleared (used at launch and by R on the end card).
func begin_slice() -> void:
	_clear_knowledge()
	start_loop(1)

func start_loop(index: int) -> void:
	loop_index = index
	_reset_loop_flags()
	clock_minutes = NIGHT_START
	phase = Phase.NIGHT
	keys_holder = "car"
	talking = false
	_sequence_time = 0.0
	running = true
	loop_started.emit(loop_index)
	phone_buzz.emit()

func set_paused(paused: bool) -> void:
	get_tree().paused = paused
	pause_changed.emit(paused)

func is_ended() -> bool:
	return phase == Phase.ENDED

## Presentation queries (pure).
func manikandan_on_phone() -> bool:
	return phase == Phase.NIGHT and clock_minutes >= OVERHEAR_START and clock_minutes < ADVAY_TIME

func advay_present() -> bool:
	return flags.ADVAY_DONE and phase != Phase.CRASH

# --- interactions ---------------------------------------------------------------

## Which conversation Manikandan offers right now. Pure query; changes nothing.
func manikandan_topic() -> String:
	if phase != Phase.NIGHT:
		return ""
	if flags.KEYS_SAFE:
		return "mani_keys_safe"
	if keys_holder == "advay":
		return "mani_after_advay"
	if ask_selvam_available():
		return "mani_choice"
	if clock_minutes >= OVERHEAR_START and clock_minutes < ADVAY_TIME:
		return "mani_overheard_again" if knowledge.KNOW_SELVAM else "mani_overhear"
	return "mani_generic"

## Hari talks to Manikandan. Returns the conversation id (changes nothing by itself).
func talk_to_manikandan() -> String:
	return manikandan_topic()

## Hari has listened to the whole Selvam call (Story calls this when mani_overhear closes).
## Saves the clue once; returns true if it was new.
func finish_overhearing() -> bool:
	return phase == Phase.NIGHT and _learn("KNOW_SELVAM")

func ask_selvam_available() -> bool:
	return phase == Phase.NIGHT and loop_index >= 2 and knowledge.KNOW_SELVAM and knowledge.KNOW_KEYS \
		and clock_minutes < ADVAY_TIME and not flags.KEYS_SAFE

## The "Ask about Selvam" choice. Manikandan agrees to hold the keys. Returns false if not allowed.
func ask_about_selvam() -> bool:
	if not ask_selvam_available():
		return false
	flags.KEYS_SAFE = true
	var from := keys_holder
	keys_holder = "manikandan"
	keys_exchanged.emit(from, keys_holder)
	_save_note("KEYS_WITH_MANI")
	return true

# --- test-only API ----------------------------------------------------------------

## Jump the clock forward to `minutes` and run every timeline event on the way, in order.
func test_advance_to(minutes: float) -> void:
	if phase == Phase.NIGHT:
		_set_clock(maxf(minutes, clock_minutes))

## Finish the running dawn sequence now instead of waiting for its real-time delay.
func test_skip_sequence() -> void:
	_sequence_time = 1000.0
	_process(0.0)

func test_setup(index: int, known: Dictionary) -> void:
	_clear_knowledge()
	for id in known:
		knowledge[id] = known[id]
	start_loop(index)

# --- internals --------------------------------------------------------------------

func _set_clock(minutes: float) -> void:
	clock_minutes = minf(minutes, NIGHT_END)
	if clock_minutes >= ADVAY_TIME and not flags.ADVAY_DONE:
		flags.ADVAY_DONE = true
		_advay_arrives()
	if clock_minutes >= FIRE_GLOW_TIME and not flags.FIRE_GLOW_DONE:
		flags.FIRE_GLOW_DONE = true
		fire_glow.emit()
	if clock_minutes >= DAWN_TIME and not flags.DAWN_DONE:
		flags.DAWN_DONE = true
		clock_minutes = DAWN_TIME
		_dawn()

func _advay_arrives() -> void:
	if flags.KEYS_SAFE:
		advay_arrived.emit(false)
		return
	var from := keys_holder
	keys_holder = "advay"
	advay_arrived.emit(true)
	keys_exchanged.emit(from, keys_holder)
	_learn("KNOW_KEYS")

func _dawn() -> void:
	_sequence_time = 0.0
	if flags.KEYS_SAFE:
		phase = Phase.SAFE_DAWN
		safe_dawn.emit()
	else:
		phase = Phase.CRASH
		dawn_crash.emit()

func _learn(id: String) -> bool:
	if knowledge.get(id, false):
		return false
	knowledge[id] = true
	_save_note(id)
	return true

func _save_note(id: String) -> void:
	if id in notes:
		return
	notes.append(id)
	clue_saved.emit(id)

func _clear_knowledge() -> void:
	knowledge.clear()
	for id in KNOWLEDGE:
		knowledge[id] = false
	notes.clear()

func _reset_loop_flags() -> void:
	flags = {"KEYS_SAFE": false, "ADVAY_DONE": false, "FIRE_GLOW_DONE": false, "DAWN_DONE": false}
