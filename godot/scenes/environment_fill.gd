extends Node3D
## Fills the void around the deck (playtest 1 screenshots showed the sky's flat ground colour past
## every edge): a raised stucco plinth under the deck, sand below it out to the beach backdrop, and a
## white compound wall with warm lamps on the gate side. Code-built geometry (Claude), no generated art.

const STUCCO := Color("b8b1a3")             ## night-toned plaster: frames the scene instead of glaring (playtest 3)
const SAND := Color("3b3428")
const WALL_CAP := Color("bdb6a8")
const DECK_MIN := Vector3(-1.8, -3.0, -4.1)      ## the deck and driveway sit on top of this plinth
const DECK_MAX := Vector3(26.1, 0.0, 4.1)

func _ready() -> void:
	# sand: the beach level below the deck, wide enough to meet the beach backdrop and the far horizon
	_box(Vector3(-60, -3.2, -40), Vector3(120, -3.0, 60), SAND, 0.95)
	# plinth: the deck is raised ~3 m above the sand (the beach view looks *down*, as in the story)
	# (top kept below the recessed pool water at y -0.35; thin skirts close the edges up to the floor)
	_box(DECK_MIN, Vector3(DECK_MAX.x, -0.4, DECK_MAX.z), STUCCO, 0.8)
	_box(Vector3(DECK_MIN.x, -0.4, DECK_MAX.z - 0.08), Vector3(DECK_MAX.x, -0.01, DECK_MAX.z), STUCCO, 0.8)
	_box(Vector3(DECK_MIN.x, -0.4, DECK_MIN.z), Vector3(DECK_MAX.x, -0.01, DECK_MIN.z + 0.08), STUCCO, 0.8)
	_box(Vector3(DECK_MAX.x - 0.08, -0.4, DECK_MIN.z), Vector3(DECK_MAX.x, -0.01, DECK_MAX.z), STUCCO, 0.8)
	_box(Vector3(-1.8, -0.02, -4.1), Vector3(0.0, 0.0, 4.1), Color("2a2622"), 0.9)   # paving strip up to the wall
	# compound wall along the gate side (x = -0.6), with a gap for the gate opening near the SUV
	_box(Vector3(-2.0, 0.0, -9.0), Vector3(-1.6, 2.4, -1.6), STUCCO, 0.8)
	_box(Vector3(-2.0, 0.0, 1.6), Vector3(-1.6, 2.4, 4.1), STUCCO, 0.8)
	_box(Vector3(-2.05, 2.4, -9.0), Vector3(-1.55, 2.52, 4.1), WALL_CAP, 0.7)
	# dark metal gate panel in the gap
	_box(Vector3(-1.95, 0.0, -1.6), Vector3(-1.85, 2.0, 1.6), Color("1c1d22"), 0.4)
	# back wall behind the driveway, joining the compound wall to the villa backdrop
	_box(Vector3(-2.0, 0.0, -9.0), Vector3(5.0, 2.4, -8.6), STUCCO, 0.8)
	for z in [-5.0, 3.6]:
		_lamp(Vector3(-1.45, 2.1, z))
	# (box-built palm silhouettes were tried and removed: they read as bars and blobs in the gate shots)

func _crown(pos: Vector3, r: float) -> void:
	var mi := MeshInstance3D.new()
	var s := SphereMesh.new()
	s.radius = r
	s.height = r * 0.9
	mi.mesh = s
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("0f1a12")
	mat.roughness = 1.0
	mi.material_override = mat
	mi.position = pos
	add_child(mi)

func _box(a: Vector3, b: Vector3, color: Color, roughness: float) -> void:
	var mi := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = (b - a).abs()
	mi.mesh = mesh
	mi.position = (a + b) / 2.0
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = roughness
	mi.material_override = mat
	add_child(mi)

func _lamp(pos: Vector3) -> void:
	var bulb := MeshInstance3D.new()
	var s := SphereMesh.new()
	s.radius = 0.09
	s.height = 0.18
	bulb.mesh = s
	var m := StandardMaterial3D.new()
	m.emission_enabled = true
	m.emission = Color("ffc98a")
	m.emission_energy_multiplier = 3.0
	bulb.material_override = m
	bulb.position = pos
	add_child(bulb)
	var light := OmniLight3D.new()
	light.light_color = Color("ffbf80")
	light.light_energy = 0.9
	light.omni_range = 6.0
	light.position = pos + Vector3(0.3, 0, 0)
	add_child(light)
