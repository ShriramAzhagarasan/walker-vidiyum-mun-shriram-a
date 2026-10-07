extends RefCounted
## Keyboard bindings, registered in code so tests and the game share them.

const ACTIONS := {
	"move_left": [KEY_A, KEY_LEFT],
	"move_right": [KEY_D, KEY_RIGHT],
	"move_up": [KEY_W, KEY_UP],
	"move_down": [KEY_S, KEY_DOWN],
	"interact": [KEY_E, KEY_SPACE],
	"choice_up": [KEY_W, KEY_UP],
	"choice_down": [KEY_S, KEY_DOWN],
	"fast_forward": [KEY_T],
	"pause": [KEY_ESCAPE, KEY_P],
	"quit": [KEY_ESCAPE],
	"restart": [KEY_R],
	"mute_music": [KEY_M],
	"mute_sfx": [KEY_N],
}

static func ensure_actions() -> void:
	for action in ACTIONS:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action)
		for key in ACTIONS[action]:
			var event := InputEventKey.new()
			event.physical_keycode = key
			InputMap.action_add_event(action, event)
