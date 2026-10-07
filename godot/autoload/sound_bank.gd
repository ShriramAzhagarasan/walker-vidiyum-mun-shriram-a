extends Node
## Listens to LoopState and plays sound. It only reads game state (LoopState clock,
## Story.player_x for the crossfade) and never changes it.
## Missing audio files are silent (no errors); trigger_counts still counts every event.

const SFX_IDS := ["phone_buzz", "clue_saved", "keys_exchanged", "dawn_crash", "safe_dawn"]
const SFX_DIR := "res://assets/audio/sfx/"            ## <id>.ogg or <id>.wav
const PARTY_MUSIC := "res://assets/audio/music/party_loop"   ## .ogg (or .wav)
const GAANA_MUSIC := "res://assets/audio/music/gaana_loop"   ## .ogg (or .wav)
const RAIL_X := 20.0                   ## metres: gaana louder past the railing zone start
const CROSSFADE_FROM := RAIL_X - 2.0
const CROSSFADE_TO := RAIL_X + 1.5
const PARTY_THIN_TO := 0.2             ## party gain at dawn after thinning from 3 AM
const DAWN_FADE_SECONDS := 0.5
const PAUSE_DUCK_DB := -8.0
const SILENT_DB := -60.0

var trigger_counts := {}               ## event id -> times fired (tests read this)
var music_playing := false
var _fade := 1.0
var _fading := false
var _sfx_players := {}
var party: AudioStreamPlayer
var gaana: AudioStreamPlayer

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_ensure_buses()
	reset_counts()
	for id in SFX_IDS:
		var player := AudioStreamPlayer.new()
		player.bus = "SFX"
		player.stream = load_stream(SFX_DIR + id)
		add_child(player)
		_sfx_players[id] = player
	party = _music_player(PARTY_MUSIC)
	gaana = _music_player(GAANA_MUSIC)
	var ls: Node = get_node("/root/LoopState")
	ls.phone_buzz.connect(_play.bind("phone_buzz"))
	ls.clue_saved.connect(func(_id: String) -> void: _play("clue_saved"))
	ls.keys_exchanged.connect(func(_from: String, _to: String) -> void: _play("keys_exchanged"))
	ls.dawn_crash.connect(_on_dawn.bind("dawn_crash"))
	ls.safe_dawn.connect(_on_dawn.bind("safe_dawn"))
	ls.loop_started.connect(func(_index: int) -> void: start_music())
	ls.pause_changed.connect(_on_pause_changed)

func _process(delta: float) -> void:
	if not music_playing:
		return
	if _fading:
		_fade = move_toward(_fade, 0.0, delta / DAWN_FADE_SECONDS)
		if _fade <= 0.0:
			stop_music()
			return
	var ls: Node = get_node("/root/LoopState")
	var t := smoothstep(CROSSFADE_FROM, CROSSFADE_TO, get_node("/root/Story").player_x)
	var thin := remap(clampf(ls.clock_minutes, ls.MUSIC_THIN_START, ls.DAWN_TIME), ls.MUSIC_THIN_START, ls.DAWN_TIME, 1.0, PARTY_THIN_TO)
	party.volume_db = _gain_db(lerpf(1.0, 0.25, t) * thin * _fade)
	gaana.volume_db = _gain_db(lerpf(0.15, 1.0, t) * _fade)

func reset_counts() -> void:
	trigger_counts.clear()
	for id in SFX_IDS:
		trigger_counts[id] = 0

func start_music() -> void:
	_fade = 1.0
	_fading = false
	music_playing = true
	for player in [party, gaana]:
		if player.stream:
			player.play()

func stop_music() -> void:
	music_playing = false
	_fading = false
	for player in [party, gaana]:
		player.stop()

func toggle_bus_mute(bus_name: String) -> void:
	set_bus_muted(bus_name, not is_bus_muted(bus_name))

func set_bus_muted(bus_name: String, muted: bool) -> void:
	AudioServer.set_bus_mute(AudioServer.get_bus_index(bus_name), muted)

func is_bus_muted(bus_name: String) -> bool:
	return AudioServer.is_bus_mute(AudioServer.get_bus_index(bus_name))

## Loads <base>.ogg or <base>.wav if present (imported, or a raw .ogg just dropped in); else null.
static func load_stream(base: String) -> AudioStream:
	for ext in [".ogg", ".wav"]:
		var path: String = base + ext
		if ResourceLoader.exists(path):
			return load(path) as AudioStream
		if ext == ".ogg" and FileAccess.file_exists(path):
			return AudioStreamOggVorbis.load_from_file(path)
	return null

func _play(id: String) -> void:
	trigger_counts[id] = trigger_counts.get(id, 0) + 1
	var player: AudioStreamPlayer = _sfx_players.get(id)
	if player and player.stream:
		player.play()

func _on_dawn(id: String) -> void:
	_play(id)
	if music_playing:
		_fading = true

func _on_pause_changed(paused: bool) -> void:
	var bus := AudioServer.get_bus_index("Music")
	if AudioServer.get_bus_effect_count(bus) > 0:
		AudioServer.set_bus_effect_enabled(bus, 0, paused)
	AudioServer.set_bus_volume_db(bus, PAUSE_DUCK_DB if paused else 0.0)

func _music_player(base: String) -> AudioStreamPlayer:
	var player := AudioStreamPlayer.new()
	player.bus = "Music"
	var stream: Variant = load_stream(base)
	if stream is AudioStreamOggVorbis:
		stream.loop = true
	elif stream is AudioStreamWAV:
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		stream.loop_end = int(stream.get_length() * stream.mix_rate)
	player.stream = stream
	player.volume_db = SILENT_DB
	add_child(player)
	return player

func _gain_db(gain: float) -> float:
	return maxf(linear_to_db(maxf(gain, 0.0001)), SILENT_DB)

## Falls back to creating the buses if default_bus_layout.tres was not loaded.
func _ensure_buses() -> void:
	for bus_name in ["Music", "SFX"]:
		if AudioServer.get_bus_index(bus_name) == -1:
			AudioServer.add_bus()
			var index := AudioServer.bus_count - 1
			AudioServer.set_bus_name(index, bus_name)
			AudioServer.set_bus_send(index, "Master")
			if bus_name == "Music":
				var lowpass := AudioEffectLowPassFilter.new()
				lowpass.cutoff_hz = 900.0
				AudioServer.add_bus_effect(index, lowpass)
				AudioServer.set_bus_effect_enabled(index, 0, false)
