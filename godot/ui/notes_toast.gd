extends Control
## Phone-notes card that slides in from the right whenever a clue is saved.

const SHOW_SECONDS := 3.5
const SLIDE_SECONDS := 0.3
const CARD := Vector2(360, 120)

var queue: Array[Dictionary] = []
var current := {}
var shown_count := 0               ## how many cards have appeared (tests read this)
var _t := 0.0

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func push(clue: Dictionary) -> void:
	queue.append(clue)

func _process(delta: float) -> void:
	if current.is_empty():
		if queue.is_empty():
			return
		current = queue.pop_front()
		shown_count += 1
		_t = 0.0
	_t += delta
	if _t > SHOW_SECONDS + 2.0 * SLIDE_SECONDS:
		current = {}
	queue_redraw()

func _draw() -> void:
	if current.is_empty():
		return
	var slide := minf(_t / SLIDE_SECONDS, 1.0) * minf((SHOW_SECONDS + 2.0 * SLIDE_SECONDS - _t) / SLIDE_SECONDS, 1.0)
	var pos := Vector2(size.x - lerpf(-10, CARD.x + 20, clampf(slide, 0, 1)), 70)
	var font := ThemeDB.fallback_font
	draw_rect(Rect2(pos, CARD), Color("fff6d5"))
	draw_rect(Rect2(pos, Vector2(CARD.x, 30)), Color("f5c542"))
	draw_string(font, pos + Vector2(12, 21), "Notes  -  saved", HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color("3b2f12"))
	draw_multiline_string(font, pos + Vector2(12, 56), str(current.get("text", "")), HORIZONTAL_ALIGNMENT_LEFT, CARD.x - 24, 16, 4, Color("1d1b16"))
