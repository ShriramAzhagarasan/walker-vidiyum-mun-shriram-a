extends Node3D
## Effect A trigger (CHANGE-BRIEF §A.4 rules 8-10). Instances res://effects/footstep_scuff.tscn
## under self at Hari's floor projection on every contact crossing detected from hari._travel,
## while Story.hari_state == "WALK" and not Story.movement_locked(). Pause is handled by
## PROCESS_MODE_PAUSABLE on the container and the scuff scene. Each instance is freed after the
## scene's 1.15 s lifetime by a pausable SceneTree timer. Writes no game state.

const SCUFF_SCENE := preload("res://effects/footstep_scuff.tscn")
const STRIDE_M := 0.42                 ## matches hari.gd:11
const LIFETIME_S := 1.15               ## matches footstep_scuff.tscn SoftDust/FineGrit lifetime
const _HALF_STRIDE := 0.5 * STRIDE_M
const _DOUBLE_STRIDE := 2.0 * STRIDE_M

@export var hari_path: NodePath

var _hari: CharacterBody3D
var _last_contact := -1

func _ready() -> void:
	_hari = get_node_or_null(hari_path) as CharacterBody3D
	_last_contact = _contact_index(_travel())

func _process(_delta: float) -> void:
	if not is_instance_valid(_hari):
		return
	if Story.hari_state != "WALK" or Story.movement_locked():
		_last_contact = _contact_index(_travel())
		return
	var now := _contact_index(_travel())
	while now > _last_contact:
		_last_contact += 1
		_fire_at(_hari.global_position)

func _travel() -> float:
	return float(_hari.get("_travel")) if is_instance_valid(_hari) else 0.0

func _contact_index(travel: float) -> int:
	return int(floor((travel - _HALF_STRIDE) / _DOUBLE_STRIDE))

func _fire_at(pos: Vector3) -> void:
	var scuff := SCUFF_SCENE.instantiate() as Node3D
	add_child(scuff)
	scuff.global_position = Vector3(pos.x, 0.0, pos.z)
	(scuff.get_node("SoftDust") as CPUParticles3D).emitting = true
	(scuff.get_node("FineGrit") as CPUParticles3D).emitting = true
	get_tree().create_timer(LIFETIME_S, false).timeout.connect(scuff.queue_free)
