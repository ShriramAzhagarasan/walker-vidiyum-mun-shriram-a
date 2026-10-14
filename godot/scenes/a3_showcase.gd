extends Node3D
## A3 asset showcase: the three Blender assets side by side at game scale on a floor, with one
## light, a camera, and Hari's real 1.75 m billboard for scale. Each asset sits at its slot's
## origin on y = 0, so a wrong origin shows as floating or sinking.
##
## Human look check (TEST-REPORT): drag or arrow keys = orbit (including from behind and from
## below), scroll or +/- = zoom, 1 / 2 / 3 = focus SUV / shrine / fence, 0 = all three,
## H = toggle Hari, L = toggle labels. Missing .glb files show a labelled grey box.

const Brief := "res://tests/data/a3_brief.json"
const ORDER := ["rock_shrine", "suv", "fence_segment"]
const SLOT_X := {"rock_shrine": -4.2, "suv": 0.0, "fence_segment": 4.6}

@onready var cam: Camera3D = $Camera3D
var focus := Vector3(0, 0.9, 0)
var yaw := deg_to_rad(-28.0)
var pitch := deg_to_rad(16.0)
var dist := 13.0
var dragging := false
var labels: Array[Label3D] = []

func _ready() -> void:
	var brief: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(Brief))
	for id in ORDER:
		var spec: Dictionary = brief.assets[id]
		var slot := Node3D.new()
		slot.name = "Slot_" + id
		slot.position = Vector3(SLOT_X[id], 0, 0)
		add_child(slot)
		var asset: Node3D = null
		if ResourceLoader.exists(spec.glb):
			asset = (load(spec.glb) as PackedScene).instantiate()
		else:
			asset = _placeholder(Vector3(spec.size_xyz[0], spec.size_xyz[1], spec.size_xyz[2]))
		asset.name = id
		slot.add_child(asset)
		var label := Label3D.new()
		label.text = "%s\nbrief %.2f × %.2f × %.2f m" % [id, spec.size_xyz[0], spec.size_xyz[2], spec.size_xyz[1]]
		label.position = Vector3(0, spec.size_xyz[1] + 0.45, 0)
		label.pixel_size = 0.004
		label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		label.modulate = Color("f2efe7")
		label.outline_size = 8
		slot.add_child(label)
		labels.append(label)
	_update_camera()

## Grey stand-in so the scene still opens before export; clearly labelled, never shipped as the asset.
func _placeholder(size: Vector3) -> Node3D:
	var n := Node3D.new()
	var mi := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	mi.mesh = mesh
	mi.position.y = size.y / 2.0
	var m := StandardMaterial3D.new()
	m.albedo_color = Color(0.5, 0.5, 0.5, 0.5)
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mi.material_override = m
	n.add_child(mi)
	var tag := Label3D.new()
	tag.text = "MISSING .glb (placeholder)"
	tag.position.y = size.y / 2.0
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color("ff6b6b")
	n.add_child(tag)
	return n

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		var mb := event as InputEventMouseButton
		if mb.button_index == MOUSE_BUTTON_LEFT:
			dragging = mb.pressed
		elif mb.button_index == MOUSE_BUTTON_WHEEL_UP and mb.pressed:
			dist = maxf(2.0, dist * 0.9)
		elif mb.button_index == MOUSE_BUTTON_WHEEL_DOWN and mb.pressed:
			dist = minf(40.0, dist * 1.1)
	elif event is InputEventMouseMotion and dragging:
		var mm := event as InputEventMouseMotion
		yaw -= mm.relative.x * 0.006
		pitch = clampf(pitch + mm.relative.y * 0.006, deg_to_rad(-80), deg_to_rad(85))
	elif event is InputEventPanGesture:                      # macOS two-finger trackpad
		var pg := event as InputEventPanGesture
		yaw -= pg.delta.x * 0.05
		pitch = clampf(pitch + pg.delta.y * 0.05, deg_to_rad(-80), deg_to_rad(85))
	elif event is InputEventKey and event.pressed and not event.echo:
		match (event as InputEventKey).keycode:
			KEY_1: _focus("suv", 7.5)
			KEY_2: _focus("rock_shrine", 4.0)
			KEY_3: _focus("fence_segment", 5.0)
			KEY_0: focus = Vector3(0, 0.9, 0); dist = 13.0
			KEY_H: $HariReference.visible = not $HariReference.visible
			KEY_L:
				for l in labels: l.visible = not l.visible
			KEY_EQUAL, KEY_KP_ADD: dist = maxf(2.0, dist * 0.9)
			KEY_MINUS, KEY_KP_SUBTRACT: dist = minf(40.0, dist * 1.1)
	_update_camera()

func _process(delta: float) -> void:
	var turn := Input.get_axis("ui_left", "ui_right")
	var tilt := Input.get_axis("ui_down", "ui_up")
	if turn != 0.0 or tilt != 0.0:
		yaw -= turn * delta * 1.4
		pitch = clampf(pitch + tilt * delta * 1.0, deg_to_rad(-80), deg_to_rad(85))
		_update_camera()

func _focus(id: String, d: float) -> void:
	focus = Vector3(SLOT_X[id], 0.8, 0)
	dist = d

func _update_camera() -> void:
	var offset := Vector3(sin(yaw) * cos(pitch), sin(pitch), cos(yaw) * cos(pitch)) * dist
	cam.position = focus + offset
	cam.look_at(focus, Vector3.UP)
