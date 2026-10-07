extends Control
## Bottom dialogue panel: a view of Story's current line (speaker, text, choices).
## Input never comes here; Controls sends E/Space and W/S to Story.

const StoryData = preload("res://logic/story_data.gd")

var _name: Label
var _text: Label
var _gloss: Label
var _choices: Label

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	position = Vector2(60, 566)
	size = Vector2(1160, 146)
	_name = _label(Vector2(24, 6), 18, Color("ffd36b"))
	_text = _label(Vector2(24, 30), 17, Color.WHITE)          # Tanglish line
	_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_text.size = Vector2(1110, 44)
	_gloss = _label(Vector2(24, 76), 14, Color(0.68, 0.68, 0.72)) # English gloss, smaller and grey
	_gloss.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_gloss.size = Vector2(1110, 36)
	_choices = _label(Vector2(40, 114), 17, Color("9fe7ff"))
	visible = false
	Story.dialogue_line.connect(_on_line)
	Story.dialogue_choice_moved.connect(func(_i: int) -> void: _render_choices())
	Story.dialogue_closed.connect(func(_id: String) -> void: visible = false)

func _on_line(line: Dictionary) -> void:
	visible = true
	_name.text = StoryData.speaker_name(line.get("speaker", ""))
	_text.text = line.get("text", "")
	_gloss.text = line.get("gloss", "")
	_render_choices()
	queue_redraw()

func _render_choices() -> void:
	var rows := PackedStringArray()
	var labels: Array = Story.choice_labels()
	for i in labels.size():
		rows.append(("> " if i == Story.choice_index else "   ") + str(labels[i]))
	_choices.text = "    ".join(rows)

func _label(pos: Vector2, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.position = pos
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(label)
	return label

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), Color(0.05, 0.04, 0.10, 0.88))
	draw_rect(Rect2(Vector2.ZERO, size), Color(1, 0.83, 0.42, 0.6), false, 2.0)
	var hint := "E / Space  >" if Story.current_choices().is_empty() else "W/S choose   E confirm"
	draw_string(ThemeDB.fallback_font, Vector2(size.x - 220, size.y - 12), hint, HORIZONTAL_ALIGNMENT_RIGHT, 200, 14, Color(1, 1, 1, 0.6))
