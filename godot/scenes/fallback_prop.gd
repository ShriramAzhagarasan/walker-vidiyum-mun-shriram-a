extends Node3D
## A flat art quad if art_path exists (width art_width_m, height from the image aspect),
## otherwise placeholder boxes built in code ("suv" or "villa").

const Art3D = preload("res://scenes/art3d.gd")

@export var art_path := ""
@export var art_width_m := 4.6
@export var kind := "suv"
var has_art := false

func _ready() -> void:
	var tex := Art3D.load_texture(art_path)
	has_art = tex != null
	if has_art:
		var quad := MeshInstance3D.new()
		var mesh := QuadMesh.new()
		mesh.size = Vector2(art_width_m, art_width_m * tex.get_height() / tex.get_width())
		quad.mesh = mesh
		quad.position.y = mesh.size.y / 2.0
		quad.material_override = Art3D.cel_material(tex)
		add_child(quad)
		return
	match kind:
		"suv":
			_box(Vector3(4.6, 1.1, 1.9), Vector3(0, 0.75, 0), Art3D.lit_material(Color("2e2d38")))
			_box(Vector3(2.8, 0.6, 1.8), Vector3(-0.3, 1.6, 0), Art3D.lit_material(Color("7d93b8")))
			for x in [-1.5, 1.5]:
				for z in [-0.95, 0.95]:
					_box(Vector3(0.7, 0.7, 0.25), Vector3(x, 0.35, z), Art3D.lit_material(Color("15141a")))
			_box(Vector3(0.05, 0.2, 0.4), Vector3(2.31, 0.95, 0.6), Art3D.lit_material(Color("fff3c4"), 2.0, Color("fff3c4")))
			_box(Vector3(0.05, 0.2, 0.4), Vector3(2.31, 0.95, -0.6), Art3D.lit_material(Color("fff3c4"), 2.0, Color("fff3c4")))
		"villa":
			_box(Vector3(9.0, 6.0, 3.0), Vector3(-4.0, 3.0, 0), Art3D.lit_material(Color("f4f1ea")))
			_box(Vector3(7.0, 4.2, 3.0), Vector3(5.0, 2.1, 0.5), Art3D.lit_material(Color("ece7dd")))
			var glass := Art3D.lit_material(Color("ffd9a0"), 1.6, Color("ffb35c"))
			for i in 4:
				_box(Vector3(1.6, 2.2, 0.05), Vector3(-7.0 + i * 2.2, 1.4, 1.53), glass)
				_box(Vector3(1.6, 1.4, 0.05), Vector3(-7.0 + i * 2.2, 4.4, 1.53), glass)
			for i in 3:
				_box(Vector3(1.8, 2.4, 0.05), Vector3(2.6 + i * 2.4, 1.5, 2.03), glass)

func _box(size: Vector3, pos: Vector3, material: Material) -> void:
	var mi := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	mi.mesh = mesh
	mi.position = pos
	mi.material_override = material
	add_child(mi)
