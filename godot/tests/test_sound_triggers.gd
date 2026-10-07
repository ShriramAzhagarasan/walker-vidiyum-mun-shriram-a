extends "res://tests/harness.gd"
## Drives two full loops through the real logic layer (keys -> Controls -> Story/LoopState)
## and checks that every sound event fires exactly once per occurrence, even with mashed and
## held E presses. Then repeats the run with Music and SFX muted: the outcome must be identical.
## It also records Hari's state sequence and checks all 10 states appear at the right moments.

const EXPECTED := {"phone_buzz": 2, "clue_saved": 3, "keys_exchanged": 2, "dawn_crash": 1, "safe_dawn": 1}
const ALL_STATES := ["IDLE", "WALK", "TALK", "PHONE", "NOTES", "OVERHEAR", "STARTLED", "KEYS", "WHITEOUT", "RELIEF"]
## Must appear in this order (other states may come between).
const EXPECTED_ORDER := ["PHONE", "IDLE", "WALK", "IDLE", "TALK", "OVERHEAR", "NOTES", "IDLE", "NOTES", "WHITEOUT",
	"STARTLED", "PHONE", "TALK", "KEYS", "NOTES", "IDLE", "RELIEF"]

var seq: Array = []      ## [state, msec] for every hari_state_changed

func run() -> bool:
	story.hari_state_changed.connect(func(state: String) -> void: seq.append([state, Time.get_ticks_msec()]))
	var loud := await scenario(false, "unmuted")
	var muted := await scenario(true, "muted")
	check("mute: same loop_index", loud.loop_index == muted.loop_index, "%s vs %s" % [loud.loop_index, muted.loop_index])
	check("mute: same knowledge", loud.knowledge == muted.knowledge, "%s vs %s" % [loud.knowledge, muted.knowledge])
	check("mute: same per-loop flags", loud.flags == muted.flags, "%s vs %s" % [loud.flags, muted.flags])
	check("mute: same notes", loud.notes == muted.notes, "%s vs %s" % [loud.notes, muted.notes])
	check("mute: end reached both times", loud.ended and muted.ended, "%s / %s" % [loud.ended, muted.ended])
	check("mute: same trigger counts", loud.counts == muted.counts, "%s vs %s" % [loud.counts, muted.counts])
	return true

func counts() -> Dictionary:
	return sound.trigger_counts

func scenario(muted: bool, tag: String) -> Dictionary:
	print("--- scenario: %s ---" % tag)
	sound.set_bus_muted("Music", muted)
	sound.set_bus_muted("SFX", muted)
	ls.test_hold_clock = true
	stand_near("", 7.0)
	sound.reset_counts()
	seq.clear()
	ls.begin_slice()
	await steps(2)

	# Loop 1, 8:00 PM: Amma's call.
	check(tag + " L1 phone_buzz on start", counts().phone_buzz == 1, counts())
	check(tag + " L1 Hari PHONE + locked during call", story.hari_state == "PHONE" and story.movement_locked(), story.hari_state)
	await finish_dialogue()
	check(tag + " L1 Hari back to IDLE after call", story.hari_state == "IDLE" and not story.movement_locked(), story.hari_state)

	# The presentation walks Hari over (thin interface: set_moving) -> WALK, then IDLE.
	for i in 10:
		story.set_moving(true)
		await steps(1)
	check(tag + " L1 WALK while moving", story.hari_state == "WALK", story.hari_state)
	story.set_moving(false)

	# Before 1:20 AM: generic polite line, no clue.
	stand_near("manikandan")
	await tap(KEY_E)
	check(tag + " L1 generic line before 1:20, Hari TALK", story.conversation_id == "mani_generic" and story.hari_state == "TALK" and counts().clue_saved == 0, "%s %s" % [story.conversation_id, story.hari_state])
	await finish_dialogue()

	# 1:30 AM: 10 rapid presses at Manikandan -> OVERHEAR while listening, Selvam clue exactly once.
	ls.test_advance_to(25 * 60 + 30)
	check(tag + " L1 Manikandan on the phone 1:20-1:40", ls.manikandan_on_phone(), ls.clock_minutes)
	key(KEY_E, true)
	await steps(1)
	check(tag + " L1 Hari OVERHEAR while the call is open", story.conversation_id == "mani_overhear" and story.hari_state == "OVERHEAR" and counts().clue_saved == 0, story.hari_state)
	key(KEY_E, false)
	await steps(1)
	await mash(KEY_E, 9)
	await wait_until(func() -> bool: return not story.dialogue_active, 2.0)
	check(tag + " L1 call heard -> clue saved once + NOTES", ls.knowledge.KNOW_SELVAM and counts().clue_saved == 1 and story.hari_state == "NOTES", "%s %s" % [counts(), story.hari_state])
	await finish_dialogue()

	# A held press with OS key-repeat echoes: at most one action, no new events.
	key(KEY_E, true)
	for i in 40:
		key(KEY_E, true, true)
		await steps(1)
	key(KEY_E, false)
	await steps(2)
	check(tag + " L1 held E re-triggers nothing", counts().clue_saved == 1 and counts().keys_exchanged == 0, counts())
	await finish_dialogue()

	# 1:40 AM: Advay takes the keys -> keys_exchanged + new KNOW_KEYS clue.
	ls.test_advance_to(ls.ADVAY_TIME)
	check(tag + " L1 Advay took keys (+ NOTES for the new clue)", ls.keys_holder == "advay" and ls.knowledge.KNOW_KEYS and counts().keys_exchanged == 1 and counts().clue_saved == 2 and story.hari_state == "NOTES", "%s %s" % [counts(), story.hari_state])
	check(tag + " L1 Advay present", ls.advay_present(), ls.flags)
	await mash(KEY_E)     # talking to Manikandan now (he's worried) teaches nothing new
	await finish_dialogue()
	check(tag + " L1 talking after Advay re-triggers nothing", counts().clue_saved == 2 and counts().keys_exchanged == 1, counts())
	ls.test_advance_to(ls.FIRE_GLOW_TIME)
	check(tag + " L1 fire glow at 4:45", ls.flags.FIRE_GLOW_DONE, ls.flags)

	# 5:50 AM without KEYS_SAFE: dawn crash once, WHITEOUT, reset to 8 PM loop 2.
	ls.test_advance_to(ls.DAWN_TIME)
	check(tag + " L1 dawn_crash once", counts().dawn_crash == 1 and counts().safe_dawn == 0, counts())
	await mash(KEY_E)
	ls.test_advance_to(ls.NIGHT_END)
	check(tag + " L1 mashing / clock pokes during crash re-trigger nothing", counts().dawn_crash == 1 and not story.dialogue_active, counts())
	var whiteout := await wait_until(func() -> bool: return story.hari_state == "WHITEOUT", story.WHITEOUT_DELAY + 1.0)
	check(tag + " L1 Hari WHITEOUT before reset", whiteout and ls.loop_index == 1, "%s loop=%d" % [story.hari_state, ls.loop_index])
	var reset := await wait_until(func() -> bool: return ls.loop_index == 2, ls.CRASH_RESET_DELAY + 2.0)
	check(tag + " reset to loop 2 at 8:00 PM", reset and is_equal_approx(ls.clock_minutes, ls.NIGHT_START), "loop=%d clock=%.1f" % [ls.loop_index, ls.clock_minutes])

	# Loop 2: startled call, knowledge kept, per-loop flags cleared.
	check(tag + " L2 phone_buzz again", counts().phone_buzz == 2, counts())
	check(tag + " L2 Hari STARTLED first, D8 before Amma", story.hari_state == "STARTLED" and story.conversation_id == "amma_call_repeat" and story.current_line().get("id") == "D8", story.hari_state)
	check(tag + " L2 knowledge kept, KEYS_SAFE reset", ls.knowledge.KNOW_SELVAM and ls.knowledge.KNOW_KEYS and not ls.flags.KEYS_SAFE and ls.keys_holder == "car", "%s %s" % [ls.knowledge, ls.flags])
	stand_near("", 7.0)
	await steps(80)       # read D8 at a normal pace, then go through the call
	await finish_dialogue()

	# 1:00 AM: ask about Selvam -> Manikandan holds the keys.
	ls.test_advance_to(25 * 60)
	stand_near("manikandan")
	await tap(KEY_E)
	await steps(10)
	check(tag + " L2 'Ask about Selvam' offered", story.choice_labels().has("Ask about Selvam"), story.choice_labels())
	await mash(KEY_E)     # first press confirms the highlighted choice, the rest mash through lines
	for i in 20:          # finish D5-D6c at a reading pace
		if not story.dialogue_active:
			break
		await steps(10)
		await tap(KEY_E)
	check(tag + " L2 keys safe after asking, Hari KEYS", ls.flags.KEYS_SAFE and ls.keys_holder == "manikandan" and counts().keys_exchanged == 2 and counts().clue_saved == 3 and story.hari_state == "KEYS", "%s %s" % [counts(), story.hari_state])
	await finish_dialogue()
	await tap(KEY_E)      # talking again re-triggers nothing
	await finish_dialogue()
	check(tag + " L2 talking again re-triggers nothing", counts().keys_exchanged == 2 and counts().clue_saved == 3, counts())

	# 1:40 AM: Manikandan refuses Advay. 5:50 AM: safe dawn, then the end card.
	ls.test_advance_to(ls.ADVAY_TIME)
	check(tag + " L2 Advay refused, keys stay", ls.keys_holder == "manikandan" and counts().keys_exchanged == 2, counts())
	ls.test_advance_to(ls.DAWN_TIME)
	check(tag + " L2 safe_dawn once, no crash", counts().safe_dawn == 1 and counts().dawn_crash == 1, counts())
	check(tag + " L2 Hari RELIEF", story.hari_state == "RELIEF", story.hari_state)
	var ended := await wait_until(func() -> bool: return ls.is_ended(), ls.END_CARD_DELAY + 2.0)
	check(tag + " slice ended", ended, ls.phase)
	check(tag + " music stopped at end", not sound.music_playing, sound.music_playing)

	for id in EXPECTED:
		check("%s exact count %s == %d" % [tag, id, EXPECTED[id]], counts()[id] == EXPECTED[id], counts()[id])
	check(tag + " clue_saved == number of new clues", counts().clue_saved == ls.notes.size(), ls.notes)

	# Hari's state sequence over the whole run.
	var states := seq.map(func(e: Array) -> String: return e[0])
	check(tag + " all 10 Hari states shown", ALL_STATES.all(func(st: String) -> bool: return st in states), ALL_STATES.filter(func(st: String) -> bool: return not st in states))
	check(tag + " state order matches the script", _in_order(states, EXPECTED_ORDER), states)
	for st in ["NOTES", "KEYS"]:
		var d := _durations(st)
		check("%s %s shown ~1.5 s each time" % [tag, st], not d.is_empty() and d.all(func(ms: int) -> bool: return ms >= 1400 and ms <= 1800), d)
	var startled := _durations("STARTLED")
	var after_startled: String = states[states.find("STARTLED") + 1] if "STARTLED" in states else ""
	check(tag + " STARTLED >= ~1.2 s, then PHONE", startled.size() == 1 and startled[0] >= 1150 and after_startled == "PHONE", "%s -> %s" % [startled, after_startled])

	var outcome := {"loop_index": ls.loop_index, "knowledge": ls.knowledge.duplicate(), "flags": ls.flags.duplicate(),
		"notes": ls.notes.duplicate(), "ended": ls.is_ended(), "counts": counts().duplicate()}
	sound.set_bus_muted("Music", false)
	sound.set_bus_muted("SFX", false)
	return outcome

## True if `wanted` appears in `seen` in order (not necessarily adjacent).
func _in_order(seen: Array, wanted: Array) -> bool:
	var i := 0
	for st in seen:
		if i < wanted.size() and st == wanted[i]:
			i += 1
	return i == wanted.size()

## How long (ms) each appearance of `state` lasted in the recorded sequence.
func _durations(state: String) -> Array:
	var out := []
	for i in seq.size() - 1:
		if seq[i][0] == state:
			out.append(seq[i + 1][1] - seq[i][1])
	return out
