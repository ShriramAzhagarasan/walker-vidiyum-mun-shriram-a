# build_suv.py: every execute_blender_code body Claude ran through the Blender MCP
# (mcp-for-blender 2.1.9, Blender 5.2.2 LTS) to build the SUV, verbatim and in order.
# Session: 2026-10-15 ~19:50 EDT, Shriram approved the plan ("approved") before call 0.
# After each object call, Claude also ran get_scene_info (location, size, rotation, scale, ground)
# and, at the end, look (angles: front, right, three_quarter, below). Those are read-only tool
# calls, not code, so they are not copied here; their results are in TEST-REPORT.md.
# The file is also runnable as a script-route fallback:
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_suv.py
# (headless, the default cube/camera/light of factory startup are left in the scene; the export step removes nothing.)


# --- SUV call 0: scene units + the asset root (origin = centre of the underside, at the world origin)
import bpy

scene = bpy.context.scene
us = scene.unit_settings
systems = [i.identifier for i in us.bl_rna.properties["system"].enum_items]
us.system = "METRIC" if "METRIC" in systems else systems[0]
us.scale_length = 1.0
lengths = [i.identifier for i in us.bl_rna.properties["length_unit"].enum_items]
if "METERS" in lengths:
    us.length_unit = "METERS"

root = bpy.data.objects.get("suv")
if root is None:
    root = bpy.data.objects.new("suv", None)          # an Empty: no geometry, just the origin
    scene.collection.objects.link(root)
root.empty_display_size = 0.5
root.location = (0.0, 0.0, 0.0)
root.rotation_euler = (0.0, 0.0, 0.0)
root.scale = (1.0, 1.0, 1.0)
print("units:", us.system, us.length_unit, "scale_length", us.scale_length)
print("root:", root.name, tuple(root.location), "type", root.type)


# --- SUV call 1: SUV_Chassis, a box 4.60 x 1.80 x 0.75 m, from z 0.35 to 1.10, body #2e2d38
import bpy

def flat_material(name, hex_colour):
    """Flat Principled BSDF colour. Blender stores linear values; the hex is sRGB."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    mat.diffuse_color = (*lin, 1.0)                    # so Solid view shows the same colour
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.725))
obj = bpy.context.active_object
obj.name = "SUV_Chassis"
obj.data.name = "SUV_Chassis"
obj.scale = (4.60, 1.80, 0.75)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("SUV_body", "#2e2d38"))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location),
      "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SUV call 2: SUV_Cabin, a box 2.70 x 1.70 x 0.75 m, from z 1.10 to 1.85, set back to x = -0.75 (front is +X), glass #7d93b8
import bpy

def flat_material(name, hex_colour):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.75, 0.0, 1.475))
obj = bpy.context.active_object
obj.name = "SUV_Cabin"
obj.data.name = "SUV_Cabin"
obj.scale = (2.70, 1.70, 0.75)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("SUV_glass", "#7d93b8"))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location),
      "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SUV call 3: SUV_Wheel_FL, a 12-segment cylinder, 0.76 m diameter x 0.25 m wide, axle along Y, at x +1.40, y +0.825, touching the floor, tyre #15141a
import bpy, math

def flat_material(name, hex_colour):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.38, depth=0.25, end_fill_type="NGON",
                                    location=(1.40, 0.825, 0.38), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = "SUV_Wheel_FL"
obj.data.name = "SUV_Wheel_FL"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("SUV_tyre", "#15141a"))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale))


# --- SUV call 4: SUV_Wheel_FR, same wheel at x +1.40, y -0.825
import bpy, math

def flat_material(name, hex_colour):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.38, depth=0.25, end_fill_type="NGON",
                                    location=(1.40, -0.825, 0.38), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = "SUV_Wheel_FR"
obj.data.name = "SUV_Wheel_FR"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("SUV_tyre", "#15141a"))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale))


# --- SUV call 5: SUV_Wheel_RL, same wheel at x -1.40, y +0.825
import bpy, math

def flat_material(name, hex_colour):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.38, depth=0.25, end_fill_type="NGON",
                                    location=(-1.40, 0.825, 0.38), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = "SUV_Wheel_RL"
obj.data.name = "SUV_Wheel_RL"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("SUV_tyre", "#15141a"))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale))


# --- SUV call 6: SUV_Wheel_RR, same wheel at x -1.40, y -0.825
import bpy, math

def flat_material(name, hex_colour):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.38, depth=0.25, end_fill_type="NGON",
                                    location=(-1.40, -0.825, 0.38), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = "SUV_Wheel_RR"
obj.data.name = "SUV_Wheel_RR"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("SUV_tyre", "#15141a"))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale))


# --- SUV call 7 (read-only): whole-asset bounds, triangle count, transforms
import bpy
from mathutils import Vector

root = bpy.data.objects["suv"]
deps = bpy.context.evaluated_depsgraph_get()
lo = Vector((1e9, 1e9, 1e9)); hi = Vector((-1e9, -1e9, -1e9)); tris = 0
for o in root.children:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    me = o.evaluated_get(deps).to_mesh()
    me.calc_loop_triangles()
    tris += len(me.loop_triangles)
    o.evaluated_get(deps).to_mesh_clear()
    print(f"{o.name:14s} rot {tuple(round(v, 4) for v in o.rotation_euler)} scale {tuple(o.scale)} mat {[m.name for m in o.data.materials]}")
size = hi - lo
print("asset size X x Y x Z:", tuple(round(v, 3) for v in size), "lowest z:", round(lo.z, 4))
print("shapes:", len(root.children), "triangles:", tris)
# Result: SUV_Cabin/Chassis/Wheel_FL/FR/RL/RR all rot (0,0,0) scale (1,1,1);
#         asset size X x Y x Z: (4.6, 1.9, 1.85) lowest z: 0.0; shapes: 6 triangles: 200


# --- SUV call 8: save the source file
import bpy, os
path = "/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/walker-vidiyum-mun-shriram-a/blender/suv.blend"
os.makedirs(os.path.dirname(path), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=path)
print("saved", bpy.data.filepath)


# =====================================================================================================
# BUILD 2 (brief revision 2). Shriram inspected build 1 in Blender: "the suv in this blender should
# resemble a modern mercedes or a bmw suv, the one on blender looks pretty basic, rework on that
# accordingly this is not what i asked for". Build 1 is committed (18b3c9c). Claude proposed the build-2
# plan; Shriram: "approved". Run in the session after the shrine, ~20:03-20:06 EDT. Build 2 replaces
# build 1 in blender/suv.blend; running this whole file headless would build both, so run from here down.
# =====================================================================================================

# --- SUV r2 call 0: back to the SUV's own file. rock_shrine.blend is saved; clear its objects and save over suv.blend (build 1 is kept in git, commit 18b3c9c)
import bpy

for o in list(bpy.data.objects):
    if o.name == "rock_shrine" or o.name.startswith(("Shrine_", "Goddess_")):
        bpy.data.objects.remove(o, do_unlink=True)
path = "/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/walker-vidiyum-mun-shriram-a/blender/suv.blend"
bpy.ops.wm.save_as_mainfile(filepath=path)
scene = bpy.context.scene
us = scene.unit_settings
systems = [i.identifier for i in us.bl_rna.properties["system"].enum_items]
us.system = "METRIC" if "METRIC" in systems else systems[0]
us.scale_length = 1.0
root = bpy.data.objects.new("suv", None)              # Empty = the asset's origin, centre of the underside
scene.collection.objects.link(root)
root.empty_display_size = 0.5
print("file:", bpy.data.filepath, "| objects:", [o.name for o in bpy.data.objects])


# --- SUV r2 call 1: SUV_Body, a box 4.60 x 1.84 m (z 0.30-1.05), shaped: bonnet slopes to 0.90 at the nose, nose and tail raised to 0.40;
#     cuts at z 0.80 / 0.92 and y +-0.45 make faces for a full-width front light bar, a black grille and a full-width red tail-light bar
import bpy, bmesh
from mathutils import Vector

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*lin, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.675))
obj = bpy.context.active_object
obj.name = "SUV_Body"
obj.data.name = "SUV_Body"
obj.scale = (4.60, 1.84, 0.75)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bm = bmesh.new(); bm.from_mesh(obj.data)
for v in bm.verts:                                    # local z = world z - 0.675
    wz = v.co.z + 0.675
    if v.co.x > 0 and wz > 1.0:  v.co.z = 0.90 - 0.675   # bonnet line down to the nose
    if wz < 0.35:                v.co.z = 0.40 - 0.675 if abs(v.co.x) > 2.0 else v.co.z
for z in (0.80, 0.92):
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector((0, 0, z - 0.675)), plane_no=Vector((0, 0, 1)))
for y in (-0.45, 0.45):
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector((0, y, 0)), plane_no=Vector((0, 1, 0)))
bm.to_mesh(obj.data); bm.free(); obj.data.update()

me = obj.data
me.materials.clear()
for m in (flat_material("SUV_body", "#333738", 0.35, 0.5),           # 0
          flat_material("SUV_grille", "#0e0f12", 0.5),                # 1
          flat_material("SUV_headlight", "#f4f1e6", 0.2, 0.0, 3.0),   # 2
          flat_material("SUV_taillight", "#b3121b", 0.3, 0.0, 1.5)):  # 3
    me.materials.append(m)
for p in me.polygons:
    c = p.center; n = p.normal; wz = c.z + 0.675
    if n.x > 0.7:
        p.material_index = 2 if wz > 0.80 else (1 if abs(c.y) < 0.45 else 0)
    elif n.x < -0.7:
        p.material_index = 3 if 0.80 < wz < 0.92 else 0
    else:
        p.material_index = 0
obj.parent = root
me.calc_loop_triangles()
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "scale", tuple(obj.scale), "faces", len(me.polygons), "tris", len(me.loop_triangles),
      "faces per material", [sum(1 for p in me.polygons if p.material_index == i) for i in range(4)])
# Result: dims (4.6, 1.84, 0.75) faces 30 tris 60. get_scene_info: size 4.6x1.84x0.65, floating 0.4.
# Claude's mistake, noted: a cube has only corner vertices, so "raise the nose and tail" raised the whole
# underside to z 0.40 (body 0.40-1.05). Kept: the 0.78 m wheels fill the gap.


# --- SUV r2 call 2: SUV_Cabin (the glasshouse), a box from x -2.20 to 1.10, z 0.95-1.70, width 1.76; top pulled in for a raked windscreen (front top to x 0.30),
#     a sloped rear (rear top to x -1.95) and tumblehome (top width 1.48). Roof face body-coloured, the rest tinted glass
import bpy, bmesh

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*lin, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
cx, cz = -0.55, 1.325
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, 0.0, cz))
obj = bpy.context.active_object
obj.name = "SUV_Cabin"
obj.data.name = "SUV_Cabin"
obj.scale = (3.30, 1.76, 0.75)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
for v in obj.data.vertices:                           # local coordinates around (cx, 0, cz)
    if v.co.z > 0:                                    # top four corners
        v.co.x = (0.30 - cx) if v.co.x > 0 else (-1.95 - cx)
        v.co.y = 0.74 if v.co.y > 0 else -0.74
obj.data.update()
me = obj.data
me.materials.clear()
me.materials.append(flat_material("SUV_glass", "#1f2633", 0.12))           # 0
me.materials.append(flat_material("SUV_body", "#333738", 0.35, 0.5))       # 1, already made in call 1
for p in me.polygons:
    p.material_index = 1 if p.normal.z > 0.9 else 0
obj.parent = root
xs = [v.co.x + cx for v in me.vertices]
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "scale", tuple(obj.scale), "x range", round(min(xs), 2), round(max(xs), 2),
      "vertex-centre x", round(sum(xs) / len(xs), 3))


# --- SUV r2 call 3: SUV_Wheel_FL, a 12-segment cylinder 0.78 m diameter x 0.26 m wide at x +1.40, y +0.82 (outer face at y +0.95), touching the floor;
#     the outer cap is inset into a tyre sidewall ring and a silver wheel face
import bpy, bmesh, math

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    mat.diffuse_color = (*lin, 1.0)
    return mat

name, x, y = "SUV_Wheel_FL", 1.40, 0.82
root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.39, depth=0.26, end_fill_type="NGON",
                                    location=(x, y, 0.39), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = name
obj.data.name = name
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bm = bmesh.new(); bm.from_mesh(obj.data)
outer = [f for f in bm.faces if len(f.verts) == 12 and (f.normal.y > 0.9 if y > 0 else f.normal.y < -0.9)]
res = bmesh.ops.inset_individual(bm, faces=outer, thickness=0.09, depth=0.0)
for f in bm.faces:
    f.material_index = 0
for f in outer:
    f.material_index = 1                               # the inner disc after the inset = the wheel face
bm.to_mesh(obj.data); bm.free(); obj.data.update()
obj.data.materials.clear()
obj.data.materials.append(flat_material("SUV_tyre", "#15141a", 0.8))
obj.data.materials.append(flat_material("SUV_wheel_face", "#b8bcc4", 0.3, 0.8))
obj.parent = root
obj.data.calc_loop_triangles()
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale), "tris", len(obj.data.loop_triangles))
# look at the wheel showed no silver face: the material index set in bmesh did not survive. Fixed in 3b.


# --- SUV r2 call 3b: fix. After the inset, the 12-sided inner disc is the face to colour; assign it by shape and normal (the first try left every face as tyre)
import bpy
obj = bpy.data.objects["SUV_Wheel_FL"]
me = obj.data
side = 1 if obj.location.y > 0 else -1
before = [p.material_index for p in me.polygons]
for p in me.polygons:
    p.material_index = 1 if (len(p.vertices) == 12 and p.normal.y * side > 0.9) else 0
me.update()
print("before", sorted(set(before)), "after: faces per material", [sum(1 for p in me.polygons if p.material_index == i) for i in range(2)],
      "| 12-gons:", [(round(p.normal.y, 2), round(p.area, 3)) for p in me.polygons if len(p.vertices) == 12])
# Result: before [0] after: faces per material [25, 1] | 12-gons: [(-1.0, 0.456), (1.0, 0.27)]


# --- SUV r2 call 4: SUV_Wheel_FR at x +1.40, y -0.82 (same wheel; the wheel face is assigned after the inset, as fixed in call 3b)
import bpy, bmesh, math

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    mat.diffuse_color = (*lin, 1.0)
    return mat

name, x, y = "SUV_Wheel_FR", 1.40, -0.82
root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.39, depth=0.26, end_fill_type="NGON",
                                    location=(x, y, 0.39), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = name
obj.data.name = name
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
side = 1 if y > 0 else -1
bm = bmesh.new(); bm.from_mesh(obj.data)
outer = [f for f in bm.faces if len(f.verts) == 12 and f.normal.y * side > 0.9]
bmesh.ops.inset_individual(bm, faces=outer, thickness=0.09, depth=0.0)
bm.to_mesh(obj.data); bm.free()
me = obj.data
me.materials.clear()
me.materials.append(flat_material("SUV_tyre", "#15141a", 0.8))
me.materials.append(flat_material("SUV_wheel_face", "#b8bcc4", 0.3, 0.8))
for p in me.polygons:
    p.material_index = 1 if (len(p.vertices) == 12 and p.normal.y * side > 0.9) else 0
me.update()
obj.parent = root
me.calc_loop_triangles()
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale), "tris", len(me.loop_triangles),
      "wheel-face faces", sum(1 for p in me.polygons if p.material_index == 1))


# --- SUV r2 call 5: SUV_Wheel_RL at x -1.40, y +0.82
import bpy, bmesh, math

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    mat.diffuse_color = (*lin, 1.0)
    return mat

name, x, y = "SUV_Wheel_RL", -1.40, 0.82
root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.39, depth=0.26, end_fill_type="NGON",
                                    location=(x, y, 0.39), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = name
obj.data.name = name
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
side = 1 if y > 0 else -1
bm = bmesh.new(); bm.from_mesh(obj.data)
outer = [f for f in bm.faces if len(f.verts) == 12 and f.normal.y * side > 0.9]
bmesh.ops.inset_individual(bm, faces=outer, thickness=0.09, depth=0.0)
bm.to_mesh(obj.data); bm.free()
me = obj.data
me.materials.clear()
me.materials.append(flat_material("SUV_tyre", "#15141a", 0.8))
me.materials.append(flat_material("SUV_wheel_face", "#b8bcc4", 0.3, 0.8))
for p in me.polygons:
    p.material_index = 1 if (len(p.vertices) == 12 and p.normal.y * side > 0.9) else 0
me.update()
obj.parent = root
me.calc_loop_triangles()
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale), "tris", len(me.loop_triangles),
      "wheel-face faces", sum(1 for p in me.polygons if p.material_index == 1))


# --- SUV r2 call 6: SUV_Wheel_RR at x -1.40, y -0.82
import bpy, bmesh, math

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    mat.diffuse_color = (*lin, 1.0)
    return mat

name, x, y = "SUV_Wheel_RR", -1.40, -0.82
root = bpy.data.objects["suv"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.39, depth=0.26, end_fill_type="NGON",
                                    location=(x, y, 0.39), rotation=(math.radians(90), 0.0, 0.0))
obj = bpy.context.active_object
obj.name = name
obj.data.name = name
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
side = 1 if y > 0 else -1
bm = bmesh.new(); bm.from_mesh(obj.data)
outer = [f for f in bm.faces if len(f.verts) == 12 and f.normal.y * side > 0.9]
bmesh.ops.inset_individual(bm, faces=outer, thickness=0.09, depth=0.0)
bm.to_mesh(obj.data); bm.free()
me = obj.data
me.materials.clear()
me.materials.append(flat_material("SUV_tyre", "#15141a", 0.8))
me.materials.append(flat_material("SUV_wheel_face", "#b8bcc4", 0.3, 0.8))
for p in me.polygons:
    p.material_index = 1 if (len(p.vertices) == 12 and p.normal.y * side > 0.9) else 0
me.update()
obj.parent = root
me.calc_loop_triangles()
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale), "tris", len(me.loop_triangles),
      "wheel-face faces", sum(1 for p in me.polygons if p.material_index == 1))


# --- SUV r2 call 7 (read-only): whole-asset bounds from vertices, triangles, transforms
import bpy
from mathutils import Vector
root = bpy.data.objects["suv"]
deps = bpy.context.evaluated_depsgraph_get()
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3); tris = 0
for o in root.children:
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    me = o.evaluated_get(deps).to_mesh(); me.calc_loop_triangles(); tris += len(me.loop_triangles); o.evaluated_get(deps).to_mesh_clear()
    print(f"{o.name:14s} rot {tuple(round(v, 4) for v in o.rotation_euler)} scale {tuple(o.scale)} mats {[m.name for m in o.data.materials]}")
print("asset size X x Y x Z:", tuple(round(v, 3) for v in (hi - lo)), "lowest z:", round(lo.z, 4))
print("shapes:", len(root.children), "triangles:", tris)
# Result: all six parts rot (0,0,0) scale (1,1,1); asset size X x Y x Z: (4.6, 1.9, 1.7) lowest z: 0.0; shapes: 6 triangles: 344


# --- SUV r2 call 8: save the source file
import bpy
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)


# =====================================================================================================
# BUILD 3 (brief revision 3), ~20:12-20:21 EDT. Shriram inspected build 2 and asked:
# "there should be a front glass and doors and windows separating sections so it should have 4 doors and
# one openable boot which would give it the look of a suv, the front of the car needs to have a grille,
# indivudal headlights, fog lamps, and the boot of the car should have a boot opener and a exhaust
# implement al of this". Build 3 rebuilds the body, cabin and wheels (still 6 basic shapes).
# From here on each execute_blender_code body was one line that ran a snippet file saved first:
#     exec(compile(open(".../suv_r3_<n>.py").read(), "suv_r3_<n>.py", "exec"))
# (plus a build_wheel(...) line for the wheels). The snippet files follow verbatim.
# =====================================================================================================

# --- SUV r3 call 1: rebuild SUV_Body for Shriram's detail list. Box 4.60 x 1.84 m, z 0.45-1.12 (taller body, visible ground clearance),
#     a nearly flat bonnet (1.05 at the nose). Face cuts + flat materials, no extra shapes:
#     front: two separate headlights, a grille, two fog lamps in a dark lower bumper;
#     rear: full-width tail-light bar, tailgate handle, dark bumper with a recessed exhaust;
#     sides: three thin seams = front door, rear door (4 doors with the other side).
import bpy, bmesh
from mathutils import Vector

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*lin, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = (*lin, 1.0)
    return mat

Z0 = 0.785                                            # body centre height; local z = world z - Z0
def W(z): return z - Z0

def cut(bm, faces, co, no):
    if not faces:
        return
    edges = list({e for f in faces for e in f.edges})
    verts = list({v for f in faces for v in f.verts})
    bmesh.ops.bisect_plane(bm, geom=faces + edges + verts, plane_co=co, plane_no=no)

def C(f): return f.calc_center_median()
def front(bm): return [f for f in bm.faces if f.normal.x > 0.9]
def rear(bm):  return [f for f in bm.faces if f.normal.x < -0.9]
def sides(bm): return [f for f in bm.faces if abs(f.normal.y) > 0.9]

root = bpy.data.objects["suv"]
old = bpy.data.objects.get("SUV_Body")
if old:
    bpy.data.objects.remove(old, do_unlink=True)
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, Z0))
obj = bpy.context.active_object
obj.name = "SUV_Body"
obj.data.name = "SUV_Body"
obj.scale = (4.60, 1.84, 0.67)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

me = obj.data
me.materials.clear()
SLOTS = [("SUV_body", "#333738", 0.35, 0.5, 0.0), ("SUV_grille", "#0e0f12", 0.5, 0.0, 0.0),
         ("SUV_headlight", "#f4f1e6", 0.2, 0.0, 3.0), ("SUV_taillight", "#b3121b", 0.3, 0.0, 1.5),
         ("SUV_foglamp", "#fff1c4", 0.2, 0.0, 1.0), ("SUV_bumper", "#1c1d20", 0.7, 0.0, 0.0),
         ("SUV_seam", "#121315", 0.8, 0.0, 0.0), ("SUV_chrome", "#b8bcc4", 0.25, 0.9, 0.0),
         ("SUV_exhaust", "#050506", 0.9, 0.0, 0.0)]
for s in SLOTS:
    me.materials.append(flat_material(*s))
BODY, GRILLE, HEAD, TAIL, FOG, BUMPER, SEAM, CHROME, EXHAUST = range(9)

bm = bmesh.new(); bm.from_mesh(me)
for v in bm.verts:
    if v.co.x > 0 and v.co.z > 0:
        v.co.z = W(1.05)                              # bonnet: 7 cm drop to the nose, nearly flat like a modern SUV
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))

# front: rows at 0.60 / 0.88, columns at +-0.40; fog-lamp cells at |y| 0.62-0.80 in the lowest row
cut(bm, front(bm), Vector((0, 0, W(0.88))), Z)
cut(bm, front(bm), Vector((0, 0.40, 0)), Y); cut(bm, front(bm), Vector((0, -0.40, 0)), Y)
cut(bm, [f for f in front(bm) if abs(C(f).y) > 0.40 and C(f).z < W(0.88)], Vector((0, 0, W(0.60))), Z)
for y in (0.62, 0.80, -0.62, -0.80):
    cut(bm, [f for f in front(bm) if C(f).z < W(0.60) and abs(C(f).y) > 0.40], Vector((0, y, 0)), Y)
heads = [f for f in front(bm) if C(f).z > W(0.88) and abs(C(f).y) > 0.40]
grille = [f for f in front(bm) if C(f).z < W(0.88) and abs(C(f).y) < 0.40]
fogs = [f for f in front(bm) if C(f).z < W(0.60) and 0.62 < abs(C(f).y) < 0.80]
front_low = [f for f in front(bm) if C(f).z < W(0.60) and f not in fogs]
bmesh.ops.inset_individual(bm, faces=heads, thickness=0.035, depth=0.0)
bmesh.ops.inset_individual(bm, faces=grille, thickness=0.05, depth=0.0)
bmesh.ops.inset_individual(bm, faces=fogs, thickness=0.03, depth=0.0)

# rear: rows at 0.62 / 0.80 / 0.92; tailgate handle cell |y| < 0.10 in the 0.62-0.80 row; exhaust cell y -0.72..-0.50 in the bumper row
for z in (0.62, 0.80, 0.92):
    cut(bm, rear(bm), Vector((0, 0, W(z))), Z)
for y in (0.10, -0.10):
    cut(bm, [f for f in rear(bm) if W(0.62) < C(f).z < W(0.80)], Vector((0, y, 0)), Y)
for y in (-0.50, -0.72):
    cut(bm, [f for f in rear(bm) if C(f).z < W(0.62)], Vector((0, y, 0)), Y)
handle = [f for f in rear(bm) if W(0.62) < C(f).z < W(0.80) and abs(C(f).y) < 0.10]
exhaust = [f for f in rear(bm) if C(f).z < W(0.62) and -0.72 < C(f).y < -0.50]
tail = [f for f in rear(bm) if W(0.80) < C(f).z < W(0.92)]
bmesh.ops.inset_individual(bm, faces=handle, thickness=0.025, depth=0.0)
bmesh.ops.inset_individual(bm, faces=exhaust, thickness=0.03, depth=-0.04)   # recessed opening
rear_low = [f for f in rear(bm) if C(f).z < W(0.62) and f not in exhaust]

# sides: thin seams (2 cm) at x 1.10 (front edge of the front door), 0.00 (between the doors), -1.10 (rear edge of the rear door)
for x in (1.09, 1.11, -0.01, 0.01, -1.11, -1.09):
    cut(bm, sides(bm), Vector((x, 0, 0)), X)
seams = [f for f in sides(bm) if any(a < C(f).x < b for a, b in ((1.09, 1.11), (-0.01, 0.01), (-1.11, -1.09)))]

for f in bm.faces:
    c = C(f)
    f.material_index = BODY
    if c.x > 2.25 and c.z < W(0.60):                  # front lower bumper, including the fog lamps' surrounds
        f.material_index = BUMPER
    if c.x < -2.25 and c.z < W(0.62):                 # rear bumper; the exhaust recess walls are dark
        f.material_index = EXHAUST if -0.72 < c.y < -0.50 else BUMPER
for group, idx in ((heads, HEAD), (grille, GRILLE), (fogs, FOG),
                   (tail, TAIL), (handle, CHROME), (exhaust, EXHAUST), (seams, SEAM)):
    for f in group:
        if f.is_valid:
            f.material_index = idx
bm.to_mesh(me); bm.free(); me.update()
obj.parent = root
me.calc_loop_triangles()
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "scale", tuple(obj.scale), "faces", len(me.polygons), "tris", len(me.loop_triangles))
print("faces per material", {SLOTS[i][0]: sum(1 for p in me.polygons if p.material_index == i) for i in range(len(SLOTS))})
# Result: dims (4.6, 1.84, 0.67) scale (1,1,1) faces 66 tris 188; faces per material: body 31, grille 1, headlight 2, taillight 1,
#         foglamp 2, bumper 17, seam 6, chrome 1, exhaust 5


# --- SUV r3 call 2: rebuild SUV_Cabin (glasshouse) on the taller body: x -2.20..1.10 at the base (z 1.05), roof z 1.70 (x -1.95..0.30),
#     sides lean in (1.76 -> 1.48 wide). Windscreen = front face, rear window = back face. B pillar (x -0.05..0.05) and
#     C pillar (x -1.16..-1.04) cut into each side so the front-door, rear-door and quarter windows read separately.
#     Roof and pillars body-coloured, windows tinted glass.
import bpy, bmesh
from mathutils import Vector

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*lin, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
old = bpy.data.objects.get("SUV_Cabin")
if old:
    bpy.data.objects.remove(old, do_unlink=True)
cx, cz = -0.55, 1.375
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, 0.0, cz))
obj = bpy.context.active_object
obj.name = "SUV_Cabin"
obj.data.name = "SUV_Cabin"
obj.scale = (3.30, 1.76, 0.65)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
me = obj.data
me.materials.clear()
me.materials.append(flat_material("SUV_glass", "#1f2633", 0.12))            # 0
me.materials.append(flat_material("SUV_body", "#333738", 0.35, 0.5))        # 1

bm = bmesh.new(); bm.from_mesh(me)
for v in bm.verts:                                     # local coordinates around (cx, 0, cz)
    if v.co.z > 0:
        v.co.x = (0.30 - cx) if v.co.x > 0 else (-1.95 - cx)
        v.co.y = 0.74 if v.co.y > 0 else -0.74
bm.normal_update()
pillars = ((-0.05, 0.05), (-1.16, -1.04))
for x in (a for p in pillars for a in p):
    side = [f for f in bm.faces if abs(f.normal.y) > 0.8]
    edges = list({e for f in side for e in f.edges}); verts = list({v for f in side for v in f.verts})
    bmesh.ops.bisect_plane(bm, geom=side + edges + verts, plane_co=Vector((x - cx, 0, 0)), plane_no=Vector((1, 0, 0)))
for f in bm.faces:
    c = f.calc_center_median()
    is_roof = f.normal.z > 0.9
    is_pillar = abs(f.normal.y) > 0.8 and any(a < c.x + cx < b for a, b in pillars)
    f.material_index = 1 if (is_roof or is_pillar) else 0
bm.to_mesh(me); bm.free(); me.update()
obj.parent = root
me.calc_loop_triangles()
xs = [v.co.x + cx for v in me.vertices]
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "scale", tuple(obj.scale), "tris", len(me.loop_triangles), "vertex-centre x", round(sum(xs) / len(xs), 3),
      "| glass/body faces", [sum(1 for p in me.polygons if p.material_index == i) for i in range(2)])
# Result: dims (3.3, 1.76, 0.65) scale (1,1,1) tris 44, vertex-centre x -0.596 (behind the middle: front is +X)


# --- SUV r3 calls 3-6: build_wheel(name, x, y) rebuilds one wheel at 10 segments (was 12) so the detailed SUV stays under the
#     course's 500 triangles: 0.78 m diameter x 0.26 m wide, axle along Y, touching the floor, outer cap inset into a tyre
#     sidewall and a silver wheel face (assigned after the inset, as fixed in r2 call 3b). Each call ran this file, then
#     build_wheel(...) for one wheel: FL (1.40, 0.82), FR (1.40, -0.82), RL (-1.40, 0.82), RR (-1.40, -0.82).
import bpy, bmesh, math

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    mat.diffuse_color = (*lin, 1.0)
    return mat

def build_wheel(name, x, y, segments=10):
    root = bpy.data.objects["suv"]
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.mesh.primitive_cylinder_add(vertices=segments, radius=0.39, depth=0.26, end_fill_type="NGON",
                                        location=(x, y, 0.39), rotation=(math.radians(90), 0.0, 0.0))
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    side = 1 if y > 0 else -1
    me = obj.data
    me.materials.clear()
    me.materials.append(flat_material("SUV_tyre", "#15141a", 0.8))
    me.materials.append(flat_material("SUV_wheel_face", "#b8bcc4", 0.3, 0.8))
    bm = bmesh.new(); bm.from_mesh(me)
    outer = [f for f in bm.faces if len(f.verts) == segments and f.normal.y * side > 0.9]
    bmesh.ops.inset_individual(bm, faces=outer, thickness=0.09, depth=0.0)
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.material_index = 1 if (len(p.vertices) == segments and p.normal.y * side > 0.9) else 0
    me.update()
    obj.parent = root
    me.calc_loop_triangles()
    print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
          "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale),
          "tris", len(me.loop_triangles), "wheel-face faces", sum(1 for p in me.polygons if p.material_index == 1))

# The four calls (each also re-ran the file above first):
build_wheel("SUV_Wheel_FL", 1.40, 0.82)
build_wheel("SUV_Wheel_FR", 1.40, -0.82)
build_wheel("SUV_Wheel_RL", -1.40, 0.82)
build_wheel("SUV_Wheel_RR", -1.40, -0.82)
# Result each: dims (0.742, 0.26, 0.78) rot (0,0,0) scale (1,1,1) tris 56, one silver wheel face. (A 10-sided wheel is 0.742 m
# across its flats in X and 0.78 m vertex-to-vertex in Z; it touches the floor at a vertex.)


# --- SUV r3 call 7 (read-only) + call 8 (save): whole-asset bounds from vertices, triangles, transforms; then save suv.blend
import bpy
from mathutils import Vector
root = bpy.data.objects["suv"]
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3); tris = 0
for o in root.children:
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
    print(f"{o.name:14s} rot {tuple(round(v, 4) for v in o.rotation_euler)} scale {tuple(o.scale)} tris {len(o.data.loop_triangles)}")
print("asset size X x Y x Z:", tuple(round(v, 3) for v in (hi - lo)), "lowest z:", round(lo.z, 4), "| shapes:", len(root.children), "triangles:", tris)
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)
# Result: body 188, cabin 44, wheels 4 x 56; asset size X x Y x Z: (4.6, 1.9, 1.7) lowest z: 0.0 | shapes: 6 triangles: 456


# =====================================================================================================
# BUILD 4 (doors), ~20:25-20:27 EDT. Shriram, looking at the side of build 3 in Blender: "the sides of the suv
# doesn't look good and proper, it is not equal sized,a dn that doesn;t look like a speartion, fix that".
# Claude's diagnosis: 2 cm dark-grey seams on a dark body, front door 1.10 m vs a windscreen base at 1.10 and a
# C pillar off the seam, so the windows did not line up with the doors. Fix: equal 1.05 m doors, 3.5 cm near-black
# seams, pillars centred on the seams. Wheels unchanged from build 3.
# =====================================================================================================

# --- SUV r4 call 0: open the SUV's own file (rock_shrine.blend was saved first)
import bpy
bpy.ops.wm.open_mainfile(filepath="/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/walker-vidiyum-mun-shriram-a/blender/suv.blend")
print("opened", bpy.data.filepath, [o.name for o in bpy.data.objects])

# calls 1 and 2 were exec() lines running these snippet files:
# --- SUV r4 call 1: SUV_Body again, door seams fixed after Shriram's look: "the sides of the suv doesn't look good and proper, it is not equal sized,a dn that doesn;t look like a speartion, fix that".
#     Two equal 1.05 m doors (seams centred at x +1.05, 0.00, -1.05, lined up with the A, B and C pillars), seams 3.5 cm wide and near-black #060607.
#     Everything else as in r3 call 1:
#     a nearly flat bonnet (1.05 at the nose). Face cuts + flat materials, no extra shapes:
#     front: two separate headlights, a grille, two fog lamps in a dark lower bumper;
#     rear: full-width tail-light bar, tailgate handle, dark bumper with a recessed exhaust;
#     sides: three thin seams = front door, rear door (4 doors with the other side).
import bpy, bmesh
from mathutils import Vector

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*lin, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = (*lin, 1.0)
    return mat

Z0 = 0.785                                            # body centre height; local z = world z - Z0
def W(z): return z - Z0

def cut(bm, faces, co, no):
    if not faces:
        return
    edges = list({e for f in faces for e in f.edges})
    verts = list({v for f in faces for v in f.verts})
    bmesh.ops.bisect_plane(bm, geom=faces + edges + verts, plane_co=co, plane_no=no)

def C(f): return f.calc_center_median()
def front(bm): return [f for f in bm.faces if f.normal.x > 0.9]
def rear(bm):  return [f for f in bm.faces if f.normal.x < -0.9]
def sides(bm): return [f for f in bm.faces if abs(f.normal.y) > 0.9]

root = bpy.data.objects["suv"]
old = bpy.data.objects.get("SUV_Body")
if old:
    bpy.data.objects.remove(old, do_unlink=True)
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, Z0))
obj = bpy.context.active_object
obj.name = "SUV_Body"
obj.data.name = "SUV_Body"
obj.scale = (4.60, 1.84, 0.67)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

me = obj.data
me.materials.clear()
SLOTS = [("SUV_body", "#333738", 0.35, 0.5, 0.0), ("SUV_grille", "#0e0f12", 0.5, 0.0, 0.0),
         ("SUV_headlight", "#f4f1e6", 0.2, 0.0, 3.0), ("SUV_taillight", "#b3121b", 0.3, 0.0, 1.5),
         ("SUV_foglamp", "#fff1c4", 0.2, 0.0, 1.0), ("SUV_bumper", "#1c1d20", 0.7, 0.0, 0.0),
         ("SUV_seam", "#060607", 0.9, 0.0, 0.0), ("SUV_chrome", "#b8bcc4", 0.25, 0.9, 0.0),
         ("SUV_exhaust", "#050506", 0.9, 0.0, 0.0)]
for s in SLOTS:
    me.materials.append(flat_material(*s))
BODY, GRILLE, HEAD, TAIL, FOG, BUMPER, SEAM, CHROME, EXHAUST = range(9)

bm = bmesh.new(); bm.from_mesh(me)
for v in bm.verts:
    if v.co.x > 0 and v.co.z > 0:
        v.co.z = W(1.05)                              # bonnet: 7 cm drop to the nose, nearly flat like a modern SUV
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))

# front: rows at 0.60 / 0.88, columns at +-0.40; fog-lamp cells at |y| 0.62-0.80 in the lowest row
cut(bm, front(bm), Vector((0, 0, W(0.88))), Z)
cut(bm, front(bm), Vector((0, 0.40, 0)), Y); cut(bm, front(bm), Vector((0, -0.40, 0)), Y)
cut(bm, [f for f in front(bm) if abs(C(f).y) > 0.40 and C(f).z < W(0.88)], Vector((0, 0, W(0.60))), Z)
for y in (0.62, 0.80, -0.62, -0.80):
    cut(bm, [f for f in front(bm) if C(f).z < W(0.60) and abs(C(f).y) > 0.40], Vector((0, y, 0)), Y)
heads = [f for f in front(bm) if C(f).z > W(0.88) and abs(C(f).y) > 0.40]
grille = [f for f in front(bm) if C(f).z < W(0.88) and abs(C(f).y) < 0.40]
fogs = [f for f in front(bm) if C(f).z < W(0.60) and 0.62 < abs(C(f).y) < 0.80]
front_low = [f for f in front(bm) if C(f).z < W(0.60) and f not in fogs]
bmesh.ops.inset_individual(bm, faces=heads, thickness=0.035, depth=0.0)
bmesh.ops.inset_individual(bm, faces=grille, thickness=0.05, depth=0.0)
bmesh.ops.inset_individual(bm, faces=fogs, thickness=0.03, depth=0.0)

# rear: rows at 0.62 / 0.80 / 0.92; tailgate handle cell |y| < 0.10 in the 0.62-0.80 row; exhaust cell y -0.72..-0.50 in the bumper row
for z in (0.62, 0.80, 0.92):
    cut(bm, rear(bm), Vector((0, 0, W(z))), Z)
for y in (0.10, -0.10):
    cut(bm, [f for f in rear(bm) if W(0.62) < C(f).z < W(0.80)], Vector((0, y, 0)), Y)
for y in (-0.50, -0.72):
    cut(bm, [f for f in rear(bm) if C(f).z < W(0.62)], Vector((0, y, 0)), Y)
handle = [f for f in rear(bm) if W(0.62) < C(f).z < W(0.80) and abs(C(f).y) < 0.10]
exhaust = [f for f in rear(bm) if C(f).z < W(0.62) and -0.72 < C(f).y < -0.50]
tail = [f for f in rear(bm) if W(0.80) < C(f).z < W(0.92)]
bmesh.ops.inset_individual(bm, faces=handle, thickness=0.025, depth=0.0)
bmesh.ops.inset_individual(bm, faces=exhaust, thickness=0.03, depth=-0.04)   # recessed opening
rear_low = [f for f in rear(bm) if C(f).z < W(0.62) and f not in exhaust]

# sides: thin seams (2 cm) at x 1.10 (front edge of the front door), 0.00 (between the doors), -1.10 (rear edge of the rear door)
SEAMS = ((1.0325, 1.0675), (-0.0175, 0.0175), (-1.0675, -1.0325))
for x in (a for s in SEAMS for a in s):
    cut(bm, sides(bm), Vector((x, 0, 0)), X)
seams = [f for f in sides(bm) if any(a < C(f).x < b for a, b in SEAMS)]

for f in bm.faces:
    c = C(f)
    f.material_index = BODY
    if c.x > 2.25 and c.z < W(0.60):                  # front lower bumper, including the fog lamps' surrounds
        f.material_index = BUMPER
    if c.x < -2.25 and c.z < W(0.62):                 # rear bumper; the exhaust recess walls are dark
        f.material_index = EXHAUST if -0.72 < c.y < -0.50 else BUMPER
for group, idx in ((heads, HEAD), (grille, GRILLE), (fogs, FOG),
                   (tail, TAIL), (handle, CHROME), (exhaust, EXHAUST), (seams, SEAM)):
    for f in group:
        if f.is_valid:
            f.material_index = idx
bm.to_mesh(me); bm.free(); me.update()
obj.parent = root
me.calc_loop_triangles()
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "scale", tuple(obj.scale), "faces", len(me.polygons), "tris", len(me.loop_triangles))
print("faces per material", {SLOTS[i][0]: sum(1 for p in me.polygons if p.material_index == i) for i in range(len(SLOTS))})
# Result: dims (4.6, 1.84, 0.67) scale (1,1,1) tris 188


# --- SUV r4 call 2: SUV_Cabin again, lined up with the r4 doors: windscreen base (A pillar) at x 1.05 (roof front 0.25), B pillar x -0.05..0.05
#     over the middle seam, C pillar x -1.11..-0.99 over the rear seam. Otherwise as r3 call 2:
#     sides lean in (1.76 -> 1.48 wide). Windscreen = front face, rear window = back face. B pillar (x -0.05..0.05) and
#     C pillar (x -1.16..-1.04) cut into each side so the front-door, rear-door and quarter windows read separately.
#     Roof and pillars body-coloured, windows tinted glass.
import bpy, bmesh
from mathutils import Vector

def flat_material(name, hex_colour, roughness=0.6, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*lin, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["suv"]
old = bpy.data.objects.get("SUV_Cabin")
if old:
    bpy.data.objects.remove(old, do_unlink=True)
cx, cz = -0.575, 1.375
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, 0.0, cz))
obj = bpy.context.active_object
obj.name = "SUV_Cabin"
obj.data.name = "SUV_Cabin"
obj.scale = (3.25, 1.76, 0.65)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
me = obj.data
me.materials.clear()
me.materials.append(flat_material("SUV_glass", "#1f2633", 0.12))            # 0
me.materials.append(flat_material("SUV_body", "#333738", 0.35, 0.5))        # 1

bm = bmesh.new(); bm.from_mesh(me)
for v in bm.verts:                                     # local coordinates around (cx, 0, cz)
    if v.co.z > 0:
        v.co.x = (0.25 - cx) if v.co.x > 0 else (-1.95 - cx)
        v.co.y = 0.74 if v.co.y > 0 else -0.74
bm.normal_update()
pillars = ((-0.05, 0.05), (-1.11, -0.99))
for x in (a for p in pillars for a in p):
    side = [f for f in bm.faces if abs(f.normal.y) > 0.8]
    edges = list({e for f in side for e in f.edges}); verts = list({v for f in side for v in f.verts})
    bmesh.ops.bisect_plane(bm, geom=side + edges + verts, plane_co=Vector((x - cx, 0, 0)), plane_no=Vector((1, 0, 0)))
for f in bm.faces:
    c = f.calc_center_median()
    is_roof = f.normal.z > 0.9
    is_pillar = abs(f.normal.y) > 0.8 and any(a < c.x + cx < b for a, b in pillars)
    f.material_index = 1 if (is_roof or is_pillar) else 0
bm.to_mesh(me); bm.free(); me.update()
obj.parent = root
me.calc_loop_triangles()
xs = [v.co.x + cx for v in me.vertices]
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "scale", tuple(obj.scale), "tris", len(me.loop_triangles), "vertex-centre x", round(sum(xs) / len(xs), 3),
      "| glass/body faces", [sum(1 for p in me.polygons if p.material_index == i) for i in range(2)])
# Result: dims (3.25, 1.76, 0.65) scale (1,1,1) tris 44, vertex-centre x -0.588


# --- SUV r4 call 3 (read-only) + save
import bpy
from mathutils import Vector
root = bpy.data.objects["suv"]
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3); tris = 0
for o in root.children:
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
seam_x = sorted({round((o.matrix_world @ p.center).x, 3) for o in [bpy.data.objects["SUV_Body"]] for p in o.data.polygons if o.data.materials[p.material_index].name == "SUV_seam"})
print("asset size X x Y x Z:", tuple(round(v, 3) for v in (hi - lo)), "lowest z:", round(lo.z, 4), "| shapes:", len(root.children), "triangles:", tris, "| seam centres x:", seam_x)
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)
# Result: asset size X x Y x Z: (4.6, 1.9, 1.7) lowest z: 0.0 | shapes: 6 triangles: 456 | seam centres x: [-1.05, 0.0, 1.05]
