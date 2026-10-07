extends Sprite3D
## Character/prop billboard: loads art_path if present, else a generated placeholder image.
## The image height always maps to height_m (pixel_size = height_m / texture height),
## with the feet at the parent's origin (y = 0).

const Art3D = preload("res://scenes/art3d.gd")

@export var art_path := ""
@export var height_m := 1.75
@export var placeholder_kind := ""
@export var variant := ""
@export var billboard_y := true          ## fixed-Y billboard (characters); false = flat quad facing +z
var has_art := false

func _ready() -> void:
	shaded = false                       # unshaded: cel art keeps its colours
	alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	no_depth_test = false
	double_sided = true
	billboard = BaseMaterial3D.BILLBOARD_FIXED_Y if billboard_y else BaseMaterial3D.BILLBOARD_DISABLED
	refresh()

func set_art(path: String, new_variant: String = variant) -> void:
	if path == art_path and new_variant == variant and texture:
		return
	art_path = path
	variant = new_variant
	refresh()

func refresh() -> void:
	var tex := Art3D.load_texture(art_path)
	has_art = tex != null
	texture = tex if has_art else ImageTexture.create_from_image(Art3D.placeholder(placeholder_kind, variant))
	pixel_size = height_m / float(texture.get_height())
	centered = true
	position.y = height_m / 2.0
