extends RefCounted
## Reads every dialogue line, caption and clue text from res://data/dialogue.json.

const PATH := "res://data/dialogue.json"
static var _data: Dictionary = {}

static func data() -> Dictionary:
	if _data.is_empty():
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(PATH))
		_data = parsed if parsed is Dictionary else {}
	return _data

static func conversation(id: String) -> Array:
	return data().get("conversations", {}).get(id, [])

static func speaker_name(id: String) -> String:
	return data().get("speakers", {}).get(id, id.capitalize())

static func clue(id: String) -> Dictionary:
	return data().get("clues", {}).get(id, {"text": id})

## A caption is a list of lines shown as subtitles wherever Hari is (e.g. Advay at the car).
static func caption(id: String) -> Array:
	return data().get("captions", {}).get(id, [])

static func end_card() -> Dictionary:
	return data().get("end_card", {"title": "...but someone is missing.", "hint": "R restart / Esc quit"})
