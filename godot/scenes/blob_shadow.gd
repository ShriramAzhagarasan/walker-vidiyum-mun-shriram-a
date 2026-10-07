extends MeshInstance3D
## Soft elliptical contact shadow on the floor under a billboard character, so sprites don't look pasted on.

@export var size := Vector2(0.95, 0.42)
@export var strength := 0.55

func _ready() -> void:
	var g := Gradient.new()
	g.set_color(0, Color(0, 0, 0, strength))
	g.set_color(1, Color(0, 0, 0, 0))
	var tex := GradientTexture2D.new()
	tex.gradient = g
	tex.fill = GradientTexture2D.FILL_RADIAL
	tex.fill_from = Vector2(0.5, 0.5)
	tex.fill_to = Vector2(0.5, 0.0)
	tex.width = 128
	tex.height = 128
	var quad := PlaneMesh.new()
	quad.size = size
	mesh = quad
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_texture = tex
	mat.disable_receive_shadows = true
	material_override = mat
	cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	position.y = 0.015
