extends Node3D
## A6 Effect B controller (CHANGE-BRIEF §B.4 rules 1-5). Instantiates
## res://effects/string_light_moths.tscn as its only child and toggles each
## GPUParticles3D.emitting as the condition
##     LoopState.phase == NIGHT and LoopState.clock_minutes < 1740
## and self.visible change. On the inactive->active edge, and on the
## hidden->visible edge while active, calls restart() so preprocess repopulates
## the group (rule 4). When the condition ends, emitting goes false immediately;
## the controller then waits one emitter lifetime (2.4 s) of pausable game time
## and hides the group (rule 2). Writes no game state; never touches amount or
## amount_ratio; never constructs a ParticleProcessMaterial. Pause: this node
## and the three emitters are PROCESS_MODE_PAUSABLE (effect scene).

const EFFECT_SCENE := preload("res://effects/string_light_moths.tscn")
const LIFETIME_S := 2.4           ## matches string_light_moths.tscn emitter lifetime
const DAWN_MINUTE := 1740.0       ## matches slice.gd:28 and CHANGE-BRIEF §B.1

var _emitters: Array[GPUParticles3D] = []
var _was_active := false
var _was_visible := true
var _fade_remaining := 0.0

func _ready() -> void:
	var effect: Node3D = EFFECT_SCENE.instantiate()
	add_child(effect)
	for c in effect.get_children():
		if c is GPUParticles3D:
			_emitters.append(c)
	_was_active = _condition_active()
	_was_visible = visible
	for e in _emitters:
		e.emitting = _was_active and _was_visible

func _process(delta: float) -> void:
	var active := _condition_active()
	var vis := visible
	var active_edge := active and not _was_active
	var show_edge := active and vis and not _was_visible
	if active_edge and not vis:
		visible = true
		vis = true
	if active_edge or show_edge:
		for e in _emitters:
			e.restart()
		_fade_remaining = 0.0
	for e in _emitters:
		e.emitting = active and vis
	if _was_active and not active:
		_fade_remaining = LIFETIME_S
	elif not active and _fade_remaining > 0.0:
		_fade_remaining = maxf(_fade_remaining - delta, 0.0)
		if _fade_remaining == 0.0 and vis:
			visible = false
			vis = false
	_was_active = active
	_was_visible = vis

func _condition_active() -> bool:
	return LoopState.phase == LoopState.Phase.NIGHT and LoopState.clock_minutes < DAWN_MINUTE
