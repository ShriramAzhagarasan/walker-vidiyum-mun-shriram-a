extends Node
## Keyboard -> logic. Polls actions with is_action_just_pressed, so a held key or OS
## key-repeat echo can never fire an action twice. Movement (camera-relative) is read
## by the presentation through move_vector(); everything else goes straight to the logic.

const InputSetup = preload("res://logic/input_setup.gd")

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	InputSetup.ensure_actions()

func _process(_delta: float) -> void:
	var ls: Node = get_node("/root/LoopState")
	var story: Node = get_node("/root/Story")
	var sound: Node = get_node("/root/SoundBank")
	if Input.is_action_just_pressed("quit") and ls.is_ended():
		get_tree().quit()
		return
	if Input.is_action_just_pressed("pause") and not ls.is_ended():
		ls.set_paused(not get_tree().paused)
	if Input.is_action_just_pressed("mute_music"):
		sound.toggle_bus_mute("Music")
	if Input.is_action_just_pressed("mute_sfx"):
		sound.toggle_bus_mute("SFX")
	if get_tree().paused:
		return
	ls.fast_forward = Input.is_action_pressed("fast_forward")
	if ls.is_ended() and Input.is_action_just_pressed("restart"):
		ls.begin_slice()
		return
	if Input.is_action_just_pressed("choice_up"):
		story.move_choice(-1)
	if Input.is_action_just_pressed("choice_down"):
		story.move_choice(1)
	if Input.is_action_just_pressed("interact"):
		story.press_interact()

## WASD / arrows as a 2D vector (x = right, y = down/back), for camera-relative movement.
func move_vector() -> Vector2:
	return Input.get_vector("move_left", "move_right", "move_up", "move_down")
