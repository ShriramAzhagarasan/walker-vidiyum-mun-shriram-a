extends Control
## Fast-forward label (top-left, under the phone status bar), Music/SFX mute indicators (top-right)
## and the "E — Talk" hint. The status bar itself is ui/status_bar.gd (its own node since A5).
## Polls the logic each frame (runs while paused so mute toggles show).

var fast_forward := false
var music_muted := false
var sfx_muted := false
var talk_hint := false

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	process_mode = Node.PROCESS_MODE_ALWAYS

func _process(_delta: float) -> void:
	var state := [LoopState.fast_forward and LoopState.phase == LoopState.Phase.NIGHT,
		SoundBank.is_bus_muted("Music"), SoundBank.is_bus_muted("SFX"), Story.can_interact()]
	if state == [fast_forward, music_muted, sfx_muted, talk_hint]:
		return
	fast_forward = state[0]
	music_muted = state[1]
	sfx_muted = state[2]
	talk_hint = state[3]
	queue_redraw()

func _draw() -> void:
	var font := ThemeDB.fallback_font
	var white := Color(1, 1, 1, 0.95)
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
