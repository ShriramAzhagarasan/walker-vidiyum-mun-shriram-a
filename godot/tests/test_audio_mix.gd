extends "res://tests/harness.gd"
## Mix checks after playtest 4 ("pressing n does nothing to the sfx and i cant hear anything"):
## the SFX were masked by the music. Verifies that (1) the music sits under the SFX level,
## (2) an SFX ducks the music while it sounds, (3) a muted SFX bus doesn't duck,
## (4) the N key toggles the SFX bus and M the Music bus, and (5) muting never changes game state.
## It can't prove audibility to a human; the measured capture (TEST-REPORT, section 5) and the playtest do that.

func run() -> bool:
	ls.test_hold_clock = true
	ls.begin_slice()                                   # 8 PM: phone_buzz fires
	await steps(10)
	var now := Time.get_ticks_msec() / 1000.0
	check("music headroom is at least 8 dB under full scale", sound.MUSIC_HEADROOM_DB <= -8.0, sound.MUSIC_HEADROOM_DB)
	check("phone buzz ducks the music (duck window open)", sound._duck_until > now, sound._duck_until - now)
	await steps(20)
	check("music is ducked by >= 6 dB while the buzz sounds", sound._duck_db <= -6.0, sound._duck_db)
	# N toggles the SFX bus, M the Music bus
	var sfx_before: bool = sound.is_bus_muted("SFX")
	key(KEY_N, true); await steps(2); key(KEY_N, false); await steps(2)
	check("N mutes the SFX bus", sound.is_bus_muted("SFX") != sfx_before, sound.is_bus_muted("SFX"))
	var music_before: bool = sound.is_bus_muted("Music")
	key(KEY_M, true); await steps(2); key(KEY_M, false); await steps(2)
	check("M mutes the Music bus", sound.is_bus_muted("Music") != music_before, sound.is_bus_muted("Music"))
	# with SFX muted, a new SFX must not duck the music
	sound._duck_until = 0.0
	var counts_before: int = sound.trigger_counts.get("clue_saved", 0)
	sound._play("clue_saved")
	check("muted SFX still counted (sound never decides state)", sound.trigger_counts.get("clue_saved", 0) == counts_before + 1, sound.trigger_counts)
	check("muted SFX does not duck the music", sound._duck_until == 0.0, sound._duck_until)
	key(KEY_N, true); await steps(2); key(KEY_N, false); await steps(2)
	key(KEY_M, true); await steps(2); key(KEY_M, false); await steps(2)
	check("N and M toggle back (both buses audible)", not sound.is_bus_muted("SFX") and not sound.is_bus_muted("Music"), [sound.is_bus_muted("SFX"), sound.is_bus_muted("Music")])
	return true
