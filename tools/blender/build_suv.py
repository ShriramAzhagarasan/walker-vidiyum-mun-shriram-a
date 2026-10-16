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
