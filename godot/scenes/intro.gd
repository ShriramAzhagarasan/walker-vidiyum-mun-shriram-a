extends Control
## Title screen + intro "motion comic" (Shriram's request, 2026-10-07): generated stills with slow
## camera moves and story captions, then a cut to the game at 8 PM. Presentation only: it never
## touches LoopState; the slice starts its own loop when it loads.
## Enter / E / Space: start, or next panel.  Esc: skip the intro.  M / N mute as in the game.

const ScreenCards = preload("res://ui/screen_cards.gd")
const SLICE := "res://scenes/slice.tscn"
const PANEL_SECONDS := 6.5
const FADE := 0.9
## [image, caption, english-or-empty, camera move: start zoom, end zoom, pan from, pan to (fractions)]
const PANELS := [
	["res://assets/art/intro/intro_1.png", "East Coast Road, Chennai.", "The last night before the beach goes back to the people.", 1.0, 1.12, Vector2(0.5, 0.5), Vector2(0.56, 0.44)],
	["res://assets/art/intro/intro_2.png", "Vastav's father fenced off the sand,", "and the rock the fishermen have always prayed to.", 1.12, 1.0, Vector2(0.45, 0.55), Vector2(0.5, 0.5)],
	["res://assets/art/intro/intro_3.png", "Hari came for one thing: a referral.", "He told Amma he was at Krishna's place, studying.", 1.0, 1.1, Vector2(0.4, 0.5), Vector2(0.55, 0.5)],
	["res://assets/art/intro/intro_4.png", "At dawn, something terrible happens on ECR.", "", 1.0, 1.25, Vector2(0.5, 0.5), Vector2(0.5, 0.5)],
]
const MUSIC := "res://assets/audio/music/gaana_loop.ogg"
const DAWN_SFX := "res://assets/audio/sfx/dawn_crash.ogg"

var _phase := "title"            ## title -> panels -> outro -> (scene change)
var _index := 0
var _t := 0.0
var _textures: Array = []
var _tamil: Font
var _music: AudioStreamPlayer
var _sfx: AudioStreamPlayer
var _leaving := false

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_tamil = ScreenCards.make_tamil_font()
	for p in PANELS:
		_textures.append(load(p[0]) if ResourceLoader.exists(p[0]) else null)
	_music = _player(MUSIC, "Music", -9.0)
	_sfx = _player(DAWN_SFX, "SFX", -4.0)
	if _music.stream is AudioStreamOggVorbis:
		_music.stream.loop = true
	_music.play()

func _player(path: String, bus: String, db: float) -> AudioStreamPlayer:
	var p := AudioStreamPlayer.new()
	p.bus = bus
	p.volume_db = db
	if ResourceLoader.exists(path):
		p.stream = load(path)
	add_child(p)
	return p

func _unhandled_key_input(event: InputEvent) -> void:
	var k := event as InputEventKey
	if k == null or not k.pressed or k.echo:
		return
	if k.keycode == KEY_ESCAPE:
		_go_to_game()
	elif k.keycode in [KEY_ENTER, KEY_KP_ENTER, KEY_SPACE, KEY_E]:
		if _phase == "title":
			_start_panels()
		elif _phase == "panels":
			_next_panel()
		else:
			_go_to_game()

func _start_panels() -> void:
	_phase = "panels"
	_index = 0
	_t = 0.0

func _next_panel() -> void:
	_index += 1
	_t = 0.0
	if _index == 3 and _sfx.stream:                 # the dawn panel: the music cuts, the highway takes over
		_music.stop()
		_sfx.play()
	if _index >= PANELS.size():
		_phase = "outro"
		_music.stop()

func _go_to_game() -> void:
	if _leaving:
		return
	_leaving = true
	get_tree().change_scene_to_file(SLICE)

func _process(delta: float) -> void:
	_t += delta
	if _phase == "panels" and _t >= PANEL_SECONDS:
		_next_panel()
	elif _phase == "outro" and _t >= 3.2:
		_go_to_game()
	queue_redraw()

func _draw() -> void:
	var size_v := get_viewport_rect().size
	draw_rect(Rect2(Vector2.ZERO, size_v), Color.BLACK)
	if _phase == "title":
		_draw_image(_textures[0], 1.04 + 0.02 * sin(_t * 0.3), Vector2(0.5, 0.5), 0.45)
		var pulse := 0.55 + 0.45 * sin(_t * 2.2)
		_center(_tamil, "விடியும் முன்", size_v.y * 0.36, 86, Color(1, 0.92, 0.8))
		_center(_tamil, "VIDIYUM MUN", size_v.y * 0.36 + 70, 34, Color(1, 1, 1, 0.92))
		_center(_tamil, "Before Dawn", size_v.y * 0.36 + 108, 20, Color(0.85, 0.85, 0.95, 0.85))
		_center(_tamil, "Press Enter to begin", size_v.y * 0.78, 20, Color(1, 1, 1, pulse))
		_center(_tamil, "Esc skips the intro  ·  M music  ·  N sound effects", size_v.y * 0.78 + 30, 14, Color(1, 1, 1, 0.55))
	elif _phase == "panels":
		var p: Array = PANELS[_index]
		var k := clampf(_t / PANEL_SECONDS, 0.0, 1.0)
		var alpha := clampf(minf(_t / FADE, (PANEL_SECONDS - _t) / FADE), 0.0, 1.0)
		_draw_image(_textures[_index], lerpf(p[3], p[4], k), p[5].lerp(p[6], k), alpha)
		var ca := clampf((_t - 0.8) / 0.8, 0.0, 1.0) * alpha
		draw_rect(Rect2(0, size_v.y - 130, size_v.x, 130), Color(0, 0, 0, 0.55 * ca))
		_center(_tamil, p[1], size_v.y - 78, 28, Color(1, 1, 1, ca))
		if p[2] != "":
			_center(_tamil, p[2], size_v.y - 40, 20, Color(0.88, 0.88, 0.94, ca))
		_center(_tamil, "Enter: next  ·  Esc: skip", 26, 12, Color(1, 1, 1, 0.35))
	else:
		var a := clampf(_t / 0.8, 0.0, 1.0)
		_center(_tamil, "…and Hari wakes up at 8 PM.", size_v.y * 0.46, 30, Color(1, 1, 1, a))
		_center(_tamil, "Again.", size_v.y * 0.46 + 44, 30, Color(1, 0.85, 0.7, clampf((_t - 1.0) / 0.6, 0.0, 1.0)))

func _draw_image(tex: Texture2D, zoom: float, focus: Vector2, alpha: float) -> void:
	var size_v := get_viewport_rect().size
	if tex == null:
		draw_rect(Rect2(Vector2.ZERO, size_v), Color(0.1, 0.1, 0.2, alpha))
		return
	var tsize := tex.get_size()
	var cover := maxf(size_v.x / tsize.x, size_v.y / tsize.y) * zoom
	var dsize := tsize * cover
	var pos := size_v / 2.0 - (dsize * focus)
	pos.x = clampf(pos.x, size_v.x - dsize.x, 0.0)
	pos.y = clampf(pos.y, size_v.y - dsize.y, 0.0)
	draw_texture_rect(tex, Rect2(pos, dsize), false, Color(1, 1, 1, alpha))

func _center(font: Font, text: String, y: float, size_px: int, color: Color) -> void:
	var w := get_viewport_rect().size.x
	draw_string(font, Vector2(0, y), text, HORIZONTAL_ALIGNMENT_CENTER, w, size_px, color)
