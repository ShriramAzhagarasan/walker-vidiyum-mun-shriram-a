## Shared source of truth for Effect B's moth silhouette (CHANGE-BRIEF §B.3).
## Produces a grayscale+alpha image: two elliptical wings (near-white) and a small
## darker body (gray 0.32), with alpha carving the outline. The particle material
## sets vertex_color_use_as_albedo = true, so the ramp's pale cream multiplies the
## grayscale: wings read as cream, the body stays a muted brown.
## Writes two artifacts:
##   moth.png  — per brief, "the PNG next to the effect"; committed for review.
##   moth.tres — ImageTexture resource the scene actually references via ext_resource.
##   Going through a .tres avoids the headless-vs-editor import step for the PNG:
##   .tres is Godot's native resource format and loads without a reimport pass.
## The committed tool at tools/write_moth_texture.gd calls save_all().
class_name MothTexture
extends RefCounted

const OUT_PNG := "res://effects/moth.png"
const OUT_TRES := "res://effects/moth.tres"
const W := 64
const H := 40                                  ## matches the 0.07 × 0.045 m quad ratio

static func generate() -> Image:
	var img := Image.create(W, H, false, Image.FORMAT_RGBA8)
	for y in H:
		for x in W:
			var nx := (float(x) + 0.5 - W * 0.5) / (W * 0.5)
			var ny := (float(y) + 0.5 - H * 0.5) / (H * 0.5)
			var left_dx := nx + 0.42
			var right_dx := nx - 0.42
			var wy := ny - 0.05                 ## wings sit a touch above the midline
			var left_d := sqrt(left_dx * left_dx * 6.0 + wy * wy * 3.2)
			var right_d := sqrt(right_dx * right_dx * 6.0 + wy * wy * 3.2)
			var wing_mask := clampf(1.0 - minf(left_d, right_d), 0.0, 1.0)
			wing_mask = wing_mask * wing_mask
			var body_d := sqrt(nx * nx * 70.0 + ny * ny * 5.5)
			var body_mask := clampf(1.0 - body_d, 0.0, 1.0)
			var alpha := clampf(wing_mask + body_mask, 0.0, 1.0)
			if alpha <= 0.02:
				img.set_pixel(x, y, Color(0, 0, 0, 0))
				continue
			var body_w := body_mask / (body_mask + wing_mask + 0.0001)
			var gray := lerpf(1.0, 0.32, body_w)
			img.set_pixel(x, y, Color(gray, gray, gray, alpha))
	return img

static func save_png(path := OUT_PNG) -> Error:
	return generate().save_png(ProjectSettings.globalize_path(path))

static func save_tres(path := OUT_TRES) -> Error:
	var tex := ImageTexture.create_from_image(generate())
	tex.resource_path = path
	return ResourceSaver.save(tex, path)

static func save_all() -> Error:
	var e1 := save_png()
	var e2 := save_tres()
	return e1 if e1 != OK else e2
