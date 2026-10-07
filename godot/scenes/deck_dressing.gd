extends Node3D
## Builds the simple-box set dressing: railing, pool walls, string-light poles, bulbs and lights.
## Layout numbers (metres) are constants here; the floor and water are textured nodes in the scene.

const Art3D = preload("res://scenes/art3d.gd")
const DECK_LENGTH := 26.0
const DECK_HALF_DEPTH := 4.0
const RAILING_START_X := 20.0
const POOL := Rect2(9.0, -3.2, 7.0, 2.4)      ## x, z, size x, size z (the recess)
const POOL_DEPTH := 0.6
const LIGHT_XS := [6.0, 10.0, 14.0, 18.0]      ## string-light poles along the back of the deck
const LIGHT_Z := -3.6
const STRING_LIGHT_COLOR := Color(1.0, 0.66, 0.36)   ## ~2700 K

func _ready() -> void:
	var rail := Art3D.lit_material(Color("d8cbb5"))
	# railing along the +x end and along +z for the railing zone
	_box(Vector3(0.08, 0.08, DECK_HALF_DEPTH * 2), Vector3(DECK_LENGTH, 1.05, 0), rail)
	_box(Vector3(DECK_LENGTH - RAILING_START_X, 0.08, 0.08), Vector3((DECK_LENGTH + RAILING_START_X) / 2.0, 1.05, DECK_HALF_DEPTH), rail)
	for i in 9:
		_box(Vector3(0.06, 1.05, 0.06), Vector3(DECK_LENGTH, 0.52, -DECK_HALF_DEPTH + i * 1.0), rail)
	for i in 7:
		_box(Vector3(0.06, 1.05, 0.06), Vector3(RAILING_START_X + i * 1.0, 0.52, DECK_HALF_DEPTH), rail)
	# pool walls (the floor has a hole over POOL; water sits below)
	var tile := Art3D.lit_material(Color("8fd3e0"))
	var c := POOL.get_center()
	_box(Vector3(POOL.size.x, POOL_DEPTH, 0.05), Vector3(c.x, -POOL_DEPTH / 2, POOL.position.y), tile)
	_box(Vector3(POOL.size.x, POOL_DEPTH, 0.05), Vector3(c.x, -POOL_DEPTH / 2, POOL.end.y), tile)
	_box(Vector3(0.05, POOL_DEPTH, POOL.size.y), Vector3(POOL.position.x, -POOL_DEPTH / 2, c.y), tile)
	_box(Vector3(0.05, POOL_DEPTH, POOL.size.y), Vector3(POOL.end.x, -POOL_DEPTH / 2, c.y), tile)
	# string lights: poles, a sagging row of emissive bulbs, and a warm OmniLight3D per span
	var pole := Art3D.lit_material(Color("2b2530"))
	var bulb := Art3D.lit_material(Color("ffd36b"), 4.0, Color("ffc46b"))
	for i in LIGHT_XS.size():
		var x: float = LIGHT_XS[i]
		_box(Vector3(0.08, 3.2, 0.08), Vector3(x, 1.6, LIGHT_Z), pole)
		if i + 1 < LIGHT_XS.size():
			var next: float = LIGHT_XS[i + 1]
			for s in range(1, 8):
				var t := s / 8.0
				_sphere(0.06, Vector3(lerpf(x, next, t), 3.1 - sin(t * PI) * 0.45, LIGHT_Z + 0.05), bulb)
			var light := OmniLight3D.new()
			light.light_color = STRING_LIGHT_COLOR
			light.light_energy = 2.8
			light.omni_range = 7.0
			light.position = Vector3((x + next) / 2.0, 2.7, LIGHT_Z + 1.2)
			add_child(light)

func _box(size: Vector3, pos: Vector3, material: Material) -> void:
	var mi := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	mi.mesh = mesh
	mi.position = pos
	mi.material_override = material
	add_child(mi)

func _sphere(radius: float, pos: Vector3, material: Material) -> void:
	var mi := MeshInstance3D.new()
	var mesh := SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius * 2.0
	mesh.radial_segments = 8
	mesh.rings = 4
	mi.mesh = mesh
	mi.position = pos
	mi.material_override = material
	add_child(mi)
