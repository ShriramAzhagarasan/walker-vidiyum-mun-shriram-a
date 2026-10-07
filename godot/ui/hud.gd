extends Control
## Phone-status-bar clock (top-left), Music/SFX mute indicators (top-right) and the
## "E — Talk" hint. Polls the logic each frame (runs while paused so mute toggles show).

var clock_minutes := 1200.0
var loop_index := 1
var fast_forward := false
var music_muted := false
var sfx_muted := false
var talk_hint := false

static func format_clock(minutes: float) -> String:
	var total := int(minutes)
	var hour := (total / 60) % 24
	var h12 := hour % 12
	if h12 == 0:
		h12 = 12
	return "%d:%02d %s" % [h12, total % 60, "AM" if hour < 12 else "PM"]

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	process_mode = Node.PROCESS_MODE_ALWAYS

func _process(_delta: float) -> void:
	var state := [int(LoopState.clock_minutes), LoopState.loop_index, LoopState.fast_forward and LoopState.phase == LoopState.Phase.NIGHT,
		SoundBank.is_bus_muted("Music"), SoundBank.is_bus_muted("SFX"), Story.can_interact()]
	if state == [int(clock_minutes), loop_index, fast_forward, music_muted, sfx_muted, talk_hint]:
		return
	clock_minutes = LoopState.clock_minutes
	loop_index = state[1]
	fast_forward = state[2]
	music_muted = state[3]
	sfx_muted = state[4]
	talk_hint = state[5]
	queue_redraw()

func _draw() -> void:
	var font := ThemeDB.fallback_font
	var white := Color(1, 1, 1, 0.95)
	# status bar
	draw_rect(Rect2(14, 12, 300, 38), Color(0.04, 0.04, 0.08, 0.6))
	draw_string(font, Vector2(26, 40), format_clock(clock_minutes), HORIZONTAL_ALIGNMENT_LEFT, -1, 22, white)
	for i in 4:   # signal bars
		draw_rect(Rect2(150 + i * 7, 38 - i * 4, 5, 4 + i * 4), white)
	draw_rect(Rect2(190, 24, 30, 15), white, false, 2.0)   # battery
	draw_rect(Rect2(193, 27, 14, 9), white)
	draw_rect(Rect2(220, 28, 3, 7), white)
	draw_string(font, Vector2(236, 37), "loop %d" % loop_index, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color(1, 1, 1, 0.6))
	if fast_forward:
		draw_string(font, Vector2(26, 72), ">> x8", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color("ffd36b"))
	if talk_hint:
		draw_rect(Rect2(size.x / 2 - 70, 520, 140, 36), Color(0, 0, 0, 0.6))
		draw_string(font, Vector2(size.x / 2 - 70, 545), "E \u2014 Talk", HORIZONTAL_ALIGNMENT_CENTER, 140, 18, white)
	# mute indicators: a drawn eighth note for Music, "SFX" text; crossed out when muted
	var w := size.x
	var music_col := Color(1, 1, 1, 0.35) if music_muted else white
	draw_circle(Vector2(w - 128, 38), 6.0, music_col)
	draw_line(Vector2(w - 123, 38), Vector2(w - 123, 18), music_col, 2.5)
	draw_line(Vector2(w - 123, 18), Vector2(w - 114, 25), music_col, 2.5)
	if music_muted:
		draw_line(Vector2(w - 140, 44), Vector2(w - 108, 14), Color("e5484d"), 3.0)
	var sfx_col := Color(1, 1, 1, 0.35) if sfx_muted else white
	draw_string(font, Vector2(w - 92, 37), "SFX", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, sfx_col)
	if sfx_muted:
		draw_line(Vector2(w - 96, 42), Vector2(w - 48, 18), Color("e5484d"), 3.0)
