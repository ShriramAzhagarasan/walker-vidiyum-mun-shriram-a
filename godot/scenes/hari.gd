extends CharacterBody3D
## Hari in 3D: camera-relative walking on the XZ plane, a billboard image per state.
## Reads keys through Controls, reports to the logic only through Story's thin interface
## (player_x, set_moving) and shows Story.hari_state.

const Spec = preload("res://logic/hari_spec.gd")
const Billboard = preload("res://scenes/billboard_art.gd")
const ART_DIR := "res://assets/art/hari/"    ## <state_lower>.png, e.g. idle.png, keys.png
const ACCEL := 9.0                           ## m/s^2: ~0.25 s to full walking speed
const DECEL := 14.0                          ## m/s^2: settles in ~0.15 s
const STRIDE_M := 0.42                       ## distance per walk frame (feet don't slide)
const BOB_M := 0.035                         ## step bob height at full speed
const BREATH_HZ := 0.28                      ## idle breathing
const BREATH_AMOUNT := 0.007
const TURN_SECONDS := 0.14                   ## squash when facing flips

var _walk_frames: Array[String] = []
var _travel := 0.0
var _time := 0.0
var _turn := 0.0
var _facing_left := false

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
	for i in range(1, 9):                                    # optional walk cycle: walk_1.png, walk_2.png, ...
		if ResourceLoader.exists(ART_DIR + "walk_%d.png" % i):
			_walk_frames.append(ART_DIR + "walk_%d.png" % i)
	add_child(preload("res://scenes/blob_shadow.gd").new())
	Story.hari_state_changed.connect(_show_state)
	_show_state(Story.hari_state)

func _physics_process(delta: float) -> void:
	var input: Vector2 = Vector2.ZERO if Story.movement_locked() else Controls.move_vector()
	var direction := Vector3.ZERO
	if camera and input != Vector2.ZERO:
		var right := camera.global_basis.x
		var forward := -camera.global_basis.z
		right.y = 0.0
		forward.y = 0.0
		direction = (right.normalized() * input.x + forward.normalized() * -input.y).limit_length(1.0)
		var screen_x := direction.dot(right.normalized())
		if absf(screen_x) > 0.1 and (screen_x < 0.0) != _facing_left:
			_facing_left = screen_x < 0.0                    # art faces right; flip when moving screen-left
			_turn = TURN_SECONDS
	var target_v := direction * Spec.WALK_SPEED
	var rate := ACCEL if target_v.length() > 0.01 else DECEL
	var hv := Vector3(velocity.x, 0.0, velocity.z).move_toward(target_v, rate * delta)
	velocity = Vector3(hv.x, 0.0, hv.z)
	move_and_slide()
	position.y = 0.0
	Story.player_x = global_position.x
	Story.set_moving(direction != Vector3.ZERO)

## Presentation-only motion: walk frames by distance, step bob, idle breathing, turn squash.
func _process(delta: float) -> void:
	_time += delta
	var speed := Vector2(velocity.x, velocity.z).length()
	var k := clampf(speed / Spec.WALK_SPEED, 0.0, 1.0)
	_travel += speed * delta
	var walking := Story.hari_state == "WALK"
	if walking and _walk_frames.size() > 1:
		var frame := int(_travel / STRIDE_M) % _walk_frames.size()
		sprite.set_art(_walk_frames[frame], "walk")
	# low on contact frames (even), high on passing frames (odd): a step, not a float
	var bob := (1.0 - cos(PI * (_travel / STRIDE_M - 0.5))) * 0.5 * BOB_M * k if walking else 0.0
	sprite.position.y = sprite.height_m / 2.0 + bob
	var breath := 1.0 + (sin(_time * TAU * BREATH_HZ) * BREATH_AMOUNT if not walking else 0.0)
	_turn = maxf(_turn - delta, 0.0)
	var squash := 1.0 - 0.55 * sin(PI * (1.0 - _turn / TURN_SECONDS)) if _turn > 0.0 else 1.0
	sprite.flip_h = _facing_left
	sprite.scale = Vector3(squash, breath, 1.0)

func _show_state(state: String) -> void:
	var key := state.to_lower()
	if key == "walk" and _walk_frames.size() > 1:
		sprite.set_art(_walk_frames[int(_travel / STRIDE_M) % _walk_frames.size()], key)
	else:
		sprite.set_art(ART_DIR + key + ".png", key)
	label.text = state
	label.visible = not sprite.has_art                       # state label only on placeholders
