extends "res://tests/harness.gd"
## Loop rules: knowledge persists across the reset, per-loop flags reset, KEYS_SAFE prevents
## the crash, and "Ask about Selvam" needs both clues (checked in LoopState and through the
## real key -> Story dialogue path). Logic layer only; no presentation scene.

func run() -> bool:
	ls.test_hold_clock = true

	# --- Loop 1: learn both clues, crash at dawn, reset ---------------------------------
	ls.begin_slice()
	check("fresh slice: loop 1, no knowledge", ls.loop_index == 1 and not ls.knowledge.KNOW_SELVAM and not ls.knowledge.KNOW_KEYS and ls.notes.is_empty(), "%d %s" % [ls.loop_index, ls.knowledge])
	check("8 PM start", is_equal_approx(ls.clock_minutes, ls.NIGHT_START), ls.clock_minutes)
	check("before 1:20 Manikandan is generic", ls.talk_to_manikandan() == "mani_generic", ls.manikandan_topic())
	ls.test_advance_to(25 * 60 + 30)
	check("1:30 loop 1: overhear Selvam (clue saved once the call has been heard)", ls.talk_to_manikandan() == "mani_overhear" and not ls.knowledge.KNOW_SELVAM and ls.finish_overhearing() and ls.knowledge.KNOW_SELVAM, ls.knowledge)
	check("overhearing again teaches nothing new", ls.talk_to_manikandan() == "mani_overheard_again" and not ls.finish_overhearing() and ls.notes.size() == 1, ls.notes)
	check("loop 1: ask unavailable even with Selvam clue", not ls.ask_selvam_available() and not ls.ask_about_selvam(), ls.flags)
	ls.test_advance_to(ls.ADVAY_TIME)
	check("1:40 Advay takes keys, KNOW_KEYS learned", ls.keys_holder == "advay" and ls.knowledge.KNOW_KEYS and not ls.flags.KEYS_SAFE, "%s %s" % [ls.keys_holder, ls.knowledge])
	check("after Advay, Manikandan is worried", ls.manikandan_topic() == "mani_after_advay", ls.manikandan_topic())
	var crashes := [0]
	var safes := [0]
	ls.dawn_crash.connect(func() -> void: crashes[0] += 1)
	ls.safe_dawn.connect(func() -> void: safes[0] += 1)
	ls.test_advance_to(ls.DAWN_TIME)
	check("5:50 without KEYS_SAFE: crash", crashes[0] == 1 and safes[0] == 0 and ls.phase == ls.Phase.CRASH, "crash=%d safe=%d" % [crashes[0], safes[0]])
	ls.test_skip_sequence()
	check("crash resets to 8 PM loop 2", ls.loop_index == 2 and ls.phase == ls.Phase.NIGHT and is_equal_approx(ls.clock_minutes, ls.NIGHT_START), "loop=%d clock=%.0f" % [ls.loop_index, ls.clock_minutes])
	check("knowledge persists across reset", ls.knowledge.KNOW_SELVAM and ls.knowledge.KNOW_KEYS and ls.notes.size() == 2, "%s %s" % [ls.knowledge, ls.notes])
	check("per-loop flags reset", not ls.flags.KEYS_SAFE and not ls.flags.ADVAY_DONE and not ls.flags.FIRE_GLOW_DONE and not ls.flags.DAWN_DONE and ls.keys_holder == "car", "%s %s" % [ls.flags, ls.keys_holder])

	# --- Loop 2: KEYS_SAFE prevents the crash -------------------------------------------
	ls.test_advance_to(25 * 60)
	check("loop 2 with both clues before 1:40: ask available", ls.ask_selvam_available() and ls.manikandan_topic() == "mani_choice", ls.manikandan_topic())
	check("asking sets KEYS_SAFE", ls.ask_about_selvam() and ls.flags.KEYS_SAFE and ls.keys_holder == "manikandan", ls.flags)
	check("cannot ask twice", not ls.ask_about_selvam(), ls.flags)
	ls.test_advance_to(ls.ADVAY_TIME)
	check("1:40 with KEYS_SAFE: Advay refused, keys stay", ls.keys_holder == "manikandan", ls.keys_holder)
	ls.test_advance_to(ls.DAWN_TIME)
	check("KEYS_SAFE prevents the crash", crashes[0] == 1 and safes[0] == 1 and ls.phase == ls.Phase.SAFE_DAWN, "crash=%d safe=%d" % [crashes[0], safes[0]])
	ls.test_skip_sequence()
	check("safe dawn ends the slice", ls.is_ended() and ls.loop_index == 2, ls.phase)
	ls.begin_slice()
	check("R restart: loop 1, knowledge cleared", ls.loop_index == 1 and not ls.knowledge.KNOW_SELVAM and not ls.knowledge.KNOW_KEYS and ls.notes.is_empty(), ls.knowledge)

	# --- "Ask about Selvam" gating ------------------------------------------------------
	var cases := [
		[2, {"KNOW_SELVAM": true, "KNOW_KEYS": false}, 25 * 60, false, "only Selvam clue"],
		[2, {"KNOW_SELVAM": false, "KNOW_KEYS": true}, 25 * 60, false, "only keys clue"],
		[2, {"KNOW_SELVAM": false, "KNOW_KEYS": false}, 25 * 60, false, "no clues"],
		[1, {"KNOW_SELVAM": true, "KNOW_KEYS": true}, 25 * 60, false, "loop 1 even with both"],
		[2, {"KNOW_SELVAM": true, "KNOW_KEYS": true}, ls.ADVAY_TIME + 5, false, "both clues but after 1:40"],
		[2, {"KNOW_SELVAM": true, "KNOW_KEYS": true}, 21 * 60, true, "both clues, loop 2, before 1:40"],
	]
	for c in cases:
		ls.test_setup(c[0], c[1])
		ls.test_advance_to(c[2])
		check("ask gating: %s -> %s" % [c[4], c[3]], ls.ask_selvam_available() == c[3] and (ls.manikandan_topic() == "mani_choice") == c[3], ls.manikandan_topic())

	# Through the real key path (E -> Controls -> Story): the dialogue offers no choice with one
	# clue, and offers "Ask about Selvam" with both.
	ls.test_setup(2, {"KNOW_SELVAM": true, "KNOW_KEYS": false})
	stand_near("", 7.0)
	await finish_dialogue()
	ls.test_advance_to(25 * 60)
	stand_near("manikandan")
	await tap(KEY_E)
	check("dialogue: no 'Ask about Selvam' with one clue", story.dialogue_active and not story.choice_labels().has("Ask about Selvam") and not ls.flags.KEYS_SAFE, "%s %s" % [story.conversation_id, story.choice_labels()])
	await finish_dialogue()
	ls.test_setup(2, {"KNOW_SELVAM": true, "KNOW_KEYS": true})
	stand_near("", 7.0)
	await finish_dialogue()
	ls.test_advance_to(25 * 60)
	stand_near("manikandan")
	await tap(KEY_E)
	check("dialogue: 'Ask about Selvam' shown with both clues", story.choice_labels().has("Ask about Selvam"), story.choice_labels())
	await tap(KEY_S)    # move to "Never mind" and confirm: keys must NOT become safe
	await steps(10)
	await tap(KEY_E)
	check("dialogue: choosing 'Just getting some air' leaves KEYS_SAFE false", not ls.flags.KEYS_SAFE and story.conversation_id == "mani_never_mind", "%s %s" % [story.conversation_id, ls.flags])
	await finish_dialogue()
	stand_near("krishna", 14.0)
	await tap(KEY_E)
	check("krishna ambient line, no flags touched", story.conversation_id == "krishna_ambient" and not ls.flags.KEYS_SAFE, story.conversation_id)
	await finish_dialogue()
	stand_near("", 7.0)
	await tap(KEY_E)
	check("E with nobody near opens nothing", not story.dialogue_active, story.conversation_id)
	# Dialogue data comes from DIALOGUE.md: no placeholders left, Tanglish + English gloss.
	var data: Dictionary = load("res://logic/story_data.gd").data()
	var raw := FileAccess.get_file_as_string("res://data/dialogue.json")
	var ids := []
	for conv in data.conversations.values():
		for line in conv:
			ids.append(line.id)
	for cap in data.captions.values():
		for line in cap:
			ids.append(line.id)
	for clue in data.clues.values():
		ids.append(clue.id)
	var wanted := ["D1a", "D1b", "D1c", "D8", "K1", "D2a", "D2b", "D3", "N1", "D4a", "D4b", "D4c", "N2", "D5", "D6a", "D6b", "D6c", "N3", "D7a", "D7b", "D7c"]
	check("dialogue.json: every DIALOGUE.md id present, no PLACEHOLDER", wanted.all(func(i: String) -> bool: return i in ids) and not raw.contains("PLACEHOLDER"), wanted.filter(func(i: String) -> bool: return not i in ids))
	check("dialogue.json: C1 choice + E1 end card with Tamil line", data.conversations.mani_choice[0].choices[0].label == "Ask about Selvam" and data.end_card.tamil == "\u2026\u0b86\u0ba9\u0bbe\u0bb2\u0bcd \u0baf\u0bbe\u0bb0\u0bcb \u0b95\u0bbe\u0ba3\u0bb5\u0bbf\u0bb2\u0bcd\u0bb2\u0bc8.", data.end_card)
	check("loop 2 opens with D8 (Hari's thought) before Amma's call", data.conversations.amma_call_repeat[0].id == "D8" and data.conversations.amma_call_repeat[1].id == "D1a", data.conversations.amma_call_repeat[0].id)
	return true
