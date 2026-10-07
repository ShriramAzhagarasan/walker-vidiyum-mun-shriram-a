extends "res://tests/harness.gd"
## Smoke test for the 3D presentation: the scene loads headless, honours the thin interface
## (player_x, nearby_target, movement lock) and keeps Hari's size/collision numbers.
## The game rules themselves are covered by the two logic tests.

const Spec = preload("res://logic/hari_spec.gd")

func run() -> bool:
	ls.test_hold_clock = true
	var slice: Node = load("res://scenes/slice.tscn").instantiate()
	root.add_child(slice)
	await steps(5)
	var hari: CharacterBody3D = slice.get_node("Hari")
	check("scene started loop 1 with Amma's call", ls.loop_index == 1 and story.conversation_id == "amma_call_first", story.conversation_id)
	var x0 := hari.global_position.x
	key(KEY_D, true)
	await steps(20)
	check("movement locked during the call", absf(hari.global_position.x - x0) < 0.001, hari.global_position)
	key(KEY_D, false)
	await finish_dialogue()
	x0 = hari.global_position.x
	key(KEY_D, true)
	await steps(30)
	var speed := Vector2(hari.velocity.x, hari.velocity.z).length()
	key(KEY_D, false)
	await steps(2)
	check("D walks Hari toward +x (camera-relative) at 2.2 m/s", hari.global_position.x > x0 + 0.5 and is_equal_approx(snappedf(speed, 0.01), Spec.WALK_SPEED), "dx=%.2f speed=%.2f" % [hari.global_position.x - x0, speed])
	check("Story.player_x follows Hari", is_equal_approx(story.player_x, hari.global_position.x), "%.2f vs %.2f" % [story.player_x, hari.global_position.x])
	check("Hari WALK then IDLE", story.hari_state == "IDLE", story.hari_state)
	var mani: Node3D = slice.get_node("Manikandan")
	hari.global_position = mani.global_position + Vector3(1.0, 0, 0.6)
	await steps(3)
	check("within 1.6 m of Manikandan -> nearby_target + talk hint", story.nearby_target == "manikandan" and story.can_interact(), story.nearby_target)
	hari.global_position = Vector3(12.5, 0, 2.5)
	await steps(3)
	check("away from NPCs -> no target", story.nearby_target == "", story.nearby_target)
	var capsule := hari.get_node("Collision").shape as CapsuleShape3D
	check("capsule r=0.28 h=1.70, bottom at the feet", is_equal_approx(capsule.radius, Spec.CAPSULE_RADIUS) and is_equal_approx(capsule.height, Spec.CAPSULE_HEIGHT) and is_equal_approx(hari.get_node("Collision").position.y, Spec.CAPSULE_HEIGHT / 2.0), capsule)
	var sprite: Sprite3D = hari.get_node("Sprite")
	check("sprite image height maps to 1.75 m", is_equal_approx(sprite.pixel_size * sprite.texture.get_height(), Spec.HEIGHT_M) and sprite.billboard == BaseMaterial3D.BILLBOARD_FIXED_Y and not sprite.shaded, sprite.pixel_size)
	var idle_tex := sprite.texture
	story.set_hari_state("PHONE")     # synchronous: the next unlocked physics frame sets IDLE/WALK again
	check("state change swaps Hari's image", sprite.texture != idle_tex and hari.get_node("StateLabel").text == "PHONE", hari.get_node("StateLabel").text)
	story.set_hari_state("IDLE")
	var rig: Script = load("res://scenes/camera_rig.gd")
	check("camera presets by zone", rig.zone_weights(2.0).gate == 1.0 and rig.zone_weights(12.0).deck == 1.0 and rig.zone_weights(24.0).railing == 1.0, rig.zone_weights(20.0))
	slice.queue_free()
	await steps(2)
	return true
