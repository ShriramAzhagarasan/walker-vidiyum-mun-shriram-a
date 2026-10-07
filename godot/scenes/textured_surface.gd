extends MeshInstance3D
## A floor/water/backdrop surface: uses art_path if present, else a fallback.
## Fallback is a generated placeholder image (placeholder_kind) or a plain colour.

const Art3D = preload("res://scenes/art3d.gd")

@export var art_path := ""
@export var placeholder_kind := ""       ## "" = plain fallback_color
@export var fallback_color := Color.WHITE
@export var uv_tiles := Vector2.ONE      ## texture repeats (marble tiles)
@export var unshaded := false            ## backdrops: unshaded, tinted by the clock instead
@export var transparent := false
@export var emission := 0.0
@export var draw_after := 0              ## render_priority: overlays draw over the backdrop behind them
var material: StandardMaterial3D
var has_art := false

func _ready() -> void:
	var tex := Art3D.load_texture(art_path)
	has_art = tex != null
	if not has_art and placeholder_kind != "":
		tex = ImageTexture.create_from_image(Art3D.placeholder(placeholder_kind))
	material = StandardMaterial3D.new()
	material.albedo_color = Color.WHITE if tex else fallback_color
	material.albedo_texture = tex
	material.uv1_scale = Vector3(uv_tiles.x, uv_tiles.y, 1)
	if unshaded:
		material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	if transparent:
		material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		material.cull_mode = BaseMaterial3D.CULL_DISABLED
	if emission > 0.0:
		material.emission_enabled = true
		material.emission = fallback_color
		material.emission_energy_multiplier = emission
		if tex:
			material.emission_texture = tex
	material.render_priority = draw_after
	material_override = material

## Clock tint for unshaded backdrops; alpha for overlays that fade in.
func set_tint(color: Color) -> void:
	if material:
		material.albedo_color = color
