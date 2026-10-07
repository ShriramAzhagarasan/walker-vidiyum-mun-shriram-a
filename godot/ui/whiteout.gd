extends Control
## Full-screen white-out (dawn crash) and a brief headlight flash: the visual twins of dawn_crash.

var white := 0.0
var flash := 0.0
var _crash_tween: Tween

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func play_crash(flash_seconds: float, white_seconds: float) -> void:
	_crash_tween = create_tween()
	_crash_tween.tween_method(_animate.bind("flash"), 0.0, 1.0, flash_seconds * 0.5)
	_crash_tween.tween_method(_animate.bind("flash"), 1.0, 0.0, flash_seconds * 0.5)
	_crash_tween.tween_method(_animate.bind("white"), 0.0, 1.0, white_seconds)

func clear_white(seconds: float) -> void:
	if _crash_tween and _crash_tween.is_valid():
		_crash_tween.kill()                                # a reset must win over a crash fade still running
	flash = 0.0
	if white > 0.0:
		create_tween().tween_method(_animate.bind("white"), white, 0.0, seconds)

func _animate(value: float, which: String) -> void:
	set(which, value)
	queue_redraw()

func _draw() -> void:
	if flash > 0.0:
		draw_rect(Rect2(Vector2.ZERO, size), Color(1, 0.97, 0.8, 0.35 * flash))
	if white > 0.0:
		draw_rect(Rect2(Vector2.ZERO, size), Color(1, 1, 1, white))
