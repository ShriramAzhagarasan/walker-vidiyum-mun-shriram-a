extends Control
## Screen-space cards: caption strip, incoming-call card, pause overlay, end card.

const StoryData = preload("res://logic/story_data.gd")
const CAPTION_SECONDS := 3.2            ## per caption line
const PHONE_SECONDS := 2.2
const TAMIL_FONT_NAMES := ["Tamil Sangam MN", "Tamil MN", "Noto Sans Tamil", "Nirmala UI", "Latha"]
const TAMIL_FONT_FILES := ["/System/Library/Fonts/Supplemental/Tamil Sangam MN.ttc", "/System/Library/Fonts/Supplemental/Tamil MN.ttc"]

var caption_queue: Array = []            ## caption lines waiting (Tanglish text + English gloss)
var caption_line := {}
var caption_time := 0.0
var tamil_font: Font
var phone_time := 0.0
var paused := false
var end_alpha := 0.0
var _end_target := 0.0

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	process_mode = Node.PROCESS_MODE_ALWAYS
	tamil_font = make_tamil_font()

## Default UI font with a system Tamil font as fallback (HarfBuzz shapes the Tamil line).
static func make_tamil_font() -> Font:
	var tamil := SystemFont.new()
	tamil.font_names = PackedStringArray(TAMIL_FONT_NAMES)
	var fallbacks: Array[Font] = [tamil]
	for path in TAMIL_FONT_FILES:
		if FileAccess.file_exists(path):
			var file := FontFile.new()
			if file.load_dynamic_font(path) == OK:
				fallbacks.append(file)
	var font := FontVariation.new()
	font.base_font = ThemeDB.fallback_font
	font.fallbacks = fallbacks
	return font

func show_caption(id: String) -> void:
	caption_queue.append_array(StoryData.caption(id))

func show_phone() -> void:
	phone_time = PHONE_SECONDS

func hide_phone() -> void:
	phone_time = 0.0

func set_paused(value: bool) -> void:
	paused = value
	queue_redraw()

func show_end_card(value: bool) -> void:
	_end_target = 1.0 if value else 0.0
	if value:
		caption_queue.clear()                       # nothing from the night may sit on top of the end card
		caption_time = 0.0
	if not value:
		end_alpha = 0.0

func clear() -> void:
	caption_time = 0.0
	caption_queue.clear()
	caption_line = {}
	phone_time = 0.0
	show_end_card(false)
	queue_redraw()

func _process(delta: float) -> void:
	if paused:
		return
	caption_time = maxf(caption_time - delta, 0.0)
	if caption_time <= 0.0 and not caption_queue.is_empty():
		caption_line = caption_queue.pop_front()
		caption_time = CAPTION_SECONDS
	phone_time = maxf(phone_time - delta, 0.0)
	end_alpha = move_toward(end_alpha, _end_target, delta / 1.2)
	queue_redraw()

func _draw() -> void:
	var font := ThemeDB.fallback_font
	var w := size.x
	if phone_time > 0.0:   # visual twin of the phone_buzz sound
		var jitter := Vector2(sin(phone_time * 60.0) * 4.0, 0)
		var card := Rect2(Vector2(w / 2 - 150, 64) + jitter, Vector2(300, 64))
		draw_rect(card, Color(0.08, 0.09, 0.12, 0.92))
		draw_rect(Rect2(card.position + Vector2(14, 12), Vector2(24, 40)), Color("4cc9e0"), false, 3.0)
		draw_string(font, card.position + Vector2(52, 28), "Amma", HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color.WHITE)
		draw_string(font, card.position + Vector2(52, 50), "incoming call...", HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color("9fe7ff"))
	if caption_time > 0.0:
		var a := minf(caption_time * 2.0, 1.0)
		var who := StoryData.speaker_name(caption_line.get("speaker", ""))
		draw_rect(Rect2(w / 2 - 440, 200, 880, 62), Color(0, 0, 0, 0.6 * a))
		draw_string(font, Vector2(w / 2 - 430, 226), who + ": " + str(caption_line.get("text", "")), HORIZONTAL_ALIGNMENT_CENTER, 860, 17, Color(1, 1, 1, a))
		draw_string(font, Vector2(w / 2 - 430, 250), str(caption_line.get("gloss", "")), HORIZONTAL_ALIGNMENT_CENTER, 860, 14, Color(0.75, 0.75, 0.78, a))
	if end_alpha > 0.0:
		var card := StoryData.end_card()
		draw_rect(Rect2(Vector2.ZERO, size), Color(0.12, 0.06, 0.08, 0.8 * end_alpha))
		draw_string(font, Vector2(0, size.y / 2 - 10), str(card.get("title", "")), HORIZONTAL_ALIGNMENT_CENTER, w, 44, Color(1, 0.93, 0.85, end_alpha))
		draw_string(tamil_font, Vector2(0, size.y / 2 + 44), str(card.get("tamil", "")), HORIZONTAL_ALIGNMENT_CENTER, w, 30, Color(1, 0.93, 0.85, 0.9 * end_alpha))
		draw_string(font, Vector2(0, size.y / 2 + 100), str(card.get("hint", "")), HORIZONTAL_ALIGNMENT_CENTER, w, 18, Color(1, 1, 1, 0.7 * end_alpha))
	if paused:
		draw_rect(Rect2(Vector2.ZERO, size), Color(0.02, 0.02, 0.06, 0.65))
		draw_string(font, Vector2(0, size.y / 2 - 30), "PAUSED", HORIZONTAL_ALIGNMENT_CENTER, w, 48, Color.WHITE)
		draw_string(font, Vector2(0, size.y / 2 + 20), "P / Esc  resume      M  music      N  sfx      hold T  fast-forward", HORIZONTAL_ALIGNMENT_CENTER, w, 16, Color(1, 1, 1, 0.75))
