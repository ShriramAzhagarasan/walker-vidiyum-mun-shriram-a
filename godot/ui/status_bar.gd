extends Control
## Hari's phone status bar (top-left): clock, signal bars, battery, loop number.
## Its own node so the night-skip material (A5) tints only this bar, not the rest of the HUD.
## Polls the logic each frame (runs while paused, like the HUD).

var clock_minutes := 1200.0
var loop_index := 1

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
	if int(LoopState.clock_minutes) == int(clock_minutes) and LoopState.loop_index == loop_index:
		return
	clock_minutes = LoopState.clock_minutes
	loop_index = LoopState.loop_index
	queue_redraw()

func _draw() -> void:
	var font := ThemeDB.fallback_font
	var white := Color(1, 1, 1, 0.95)
	draw_rect(Rect2(14, 12, 300, 38), Color(0.04, 0.04, 0.08, 0.6))
	draw_string(font, Vector2(26, 40), format_clock(clock_minutes), HORIZONTAL_ALIGNMENT_LEFT, -1, 22, white)
	for i in 4:   # signal bars
		draw_rect(Rect2(150 + i * 7, 38 - i * 4, 5, 4 + i * 4), white)
	draw_rect(Rect2(190, 24, 30, 15), white, false, 2.0)   # battery
	draw_rect(Rect2(193, 27, 14, 9), white)
	draw_rect(Rect2(220, 28, 3, 7), white)
	draw_string(font, Vector2(236, 37), "loop %d" % loop_index, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color(1, 1, 1, 0.6))
