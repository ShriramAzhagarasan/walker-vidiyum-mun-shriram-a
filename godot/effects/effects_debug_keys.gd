extends Node
## A6 debug keys (debug builds only), for pricing the effects on the GPU in a real windowed run (TEST-REPORT A6).
##   F10: vsync on/off, for an FPS comparison only (no project-setting change).
##   F11: both effects off/on. Off hides FootstepScuffs and stops its trigger, and hides StringLightMoths, which
##        stops their emission (the controller's hidden rule, CHANGE-BRIEF B.4 #4). Writes no game state.

const VSYNC_KEY := KEY_F10
const EFFECTS_KEY := KEY_F11

@export var scuffs_path: NodePath
@export var moths_path: NodePath

var _effects_on := true

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS

func _unhandled_input(event: InputEvent) -> void:
	if not OS.is_debug_build() or not (event is InputEventKey) or not event.pressed or event.echo:
		return
	if event.keycode == VSYNC_KEY:
		var off := DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if off else DisplayServer.VSYNC_DISABLED)
		print("F10 vsync ", "on" if off else "off")
	elif event.keycode == EFFECTS_KEY:
		_effects_on = not _effects_on
		var scuffs := get_node(scuffs_path) as Node3D
		scuffs.visible = _effects_on
		scuffs.process_mode = Node.PROCESS_MODE_INHERIT if _effects_on else Node.PROCESS_MODE_DISABLED
		(get_node(moths_path) as Node3D).visible = _effects_on
		print("F11 effects ", "on" if _effects_on else "off")
