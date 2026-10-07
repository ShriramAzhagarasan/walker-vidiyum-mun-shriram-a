extends CharacterBody3D
## Hari in 3D: camera-relative walking on the XZ plane, a billboard image per state.
## Reads keys through Controls, reports to the logic only through Story's thin interface
## (player_x, set_moving) and shows Story.hari_state.

const Spec = preload("res://logic/hari_spec.gd")
const Billboard = preload("res://scenes/billboard_art.gd")
const ART_DIR := "res://assets/art/hari/"    ## <state_lower>.png, e.g. idle.png, keys.png

var camera: Camera3D
@onready var sprite: Billboard = $Sprite
@onready var label: Label3D = $StateLabel
@onready var collision: CollisionShape3D = $Collision

func _ready() -> void:
	var capsule := CapsuleShape3D.new()
	capsule.radius = Spec.CAPSULE_RADIUS
	capsule.height = Spec.CAPSULE_HEIGHT
	collision.shape = capsule
	collision.position.y = Spec.CAPSULE_HEIGHT / 2.0      # capsule bottom at the feet
	sprite.height_m = Spec.HEIGHT_M
	Story.hari_state_changed.connect(_show_state)
	_show_state(Story.hari_state)

func _physics_process(_delta: float) -> void:
	var input: Vector2 = Vector2.ZERO if Story.movement_locked() else Controls.move_vector()
	var direction := Vector3.ZERO
	if camera and input != Vector2.ZERO:
		var right := camera.global_basis.x
		var forward := -camera.global_basis.z
		right.y = 0.0
		forward.y = 0.0
		direction = (right.normalized() * input.x + forward.normalized() * -input.y).limit_length(1.0)
		var screen_x := direction.dot(right.normalized())
		if absf(screen_x) > 0.1:
			sprite.flip_h = screen_x < 0.0                  # art faces right; flip when moving screen-left
	velocity = direction * Spec.WALK_SPEED
	move_and_slide()
	position.y = 0.0
	Story.player_x = global_position.x
	Story.set_moving(direction != Vector3.ZERO)

func _show_state(state: String) -> void:
	var key := state.to_lower()
	sprite.set_art(ART_DIR + key + ".png", key)
	label.text = state
	label.visible = not sprite.has_art                       # state label only on placeholders
