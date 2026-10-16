# build_rock_shrine.py: every execute_blender_code body Claude ran through the Blender MCP
# (mcp-for-blender 2.1.9, Blender 5.2.2 LTS) to build the rock shrine, verbatim and in order,
# including the steps that were later replaced (call 2's small niche), so the history is honest.
# Session: 2026-10-15 ~19:57-20:03 EDT.
#   - Calls 0-2 follow brief revision 2 (Shriram: "option A as it matches the lore").
#   - Shriram then interrupted: "the shrine shouldn't look like a regula rrock, i want it to look like
#     the sea god which i described in my lore ... the rock should have the goddess ibnscribed on it".
#     Claude proposed the 6-shape relief plan (brief revision 3); Shriram: "approved". Calls 1c-8 follow it.
# After each object call Claude also ran get_scene_info (location, size, rotation, scale), and look at
# the end; those are read-only tool calls, not code.


# --- SHRINE call 0: new file for this asset (suv.blend is already saved), metric units, the asset root at the world origin
import bpy, os

for o in list(bpy.data.objects):
    if o.name == "suv" or o.name.startswith("SUV_"):
        bpy.data.objects.remove(o, do_unlink=True)
path = "/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/walker-vidiyum-mun-shriram-a/blender/rock_shrine.blend"
bpy.ops.wm.save_as_mainfile(filepath=path)

scene = bpy.context.scene
us = scene.unit_settings
systems = [i.identifier for i in us.bl_rna.properties["system"].enum_items]
us.system = "METRIC" if "METRIC" in systems else systems[0]
us.scale_length = 1.0
root = bpy.data.objects.new("rock_shrine", None)       # Empty = the asset's origin, centre of the rock's underside
scene.collection.objects.link(root)
root.empty_display_size = 0.4
print("file:", bpy.data.filepath, "| objects:", [o.name for o in bpy.data.objects])


# --- SHRINE call 1: Shrine_Rock, icosphere (subdivisions 2 = 80 triangles) flattened to 1.20 x 1.00 x 0.90 m with a flat base on the floor, rock #6f6a63
import bpy, bmesh

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["rock_shrine"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=(0.0, 0.0, 0.0))
obj = bpy.context.active_object
obj.name = "Shrine_Rock"
obj.data.name = "Shrine_Rock"
obj.scale = (0.60, 0.50, 0.50)                       # half-extents: 1.20 x 1.00 x 1.00 m
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bm = bmesh.new(); bm.from_mesh(obj.data)
for v in bm.verts:
    v.co.z += 0.40                                   # centre at z = 0.40, so the bottom would be at -0.10 ...
    if v.co.z < 0.0:
        v.co.z = 0.0                                 # ... and the part below the sand is pressed flat: a flat base at z = 0
bm.to_mesh(obj.data); bm.free(); obj.data.update()
obj.data.materials.clear()
obj.data.materials.append(flat_material("Shrine_rock", "#6f6a63"))
obj.parent = root
obj.data.calc_loop_triangles()
print(obj.name, "loc", tuple(obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
      "scale", tuple(obj.scale), "tris", len(obj.data.loop_triangles))
# get_scene_info then showed: size 1.14x1.0x0.9, on ground. The X size was 5 % short.


# --- SHRINE call 1b: correction. The icosphere's X extent is 0.951 of its radius, so the rock measured 1.141 m, not 1.20 m. Stretch X to exactly 1.20 and apply.
import bpy
obj = bpy.data.objects["Shrine_Rock"]
xs = [v.co.x for v in obj.data.vertices]
k = 1.20 / (max(xs) - min(xs))
for v in obj.data.vertices:
    v.co.x *= k
obj.data.update()
xs = [v.co.x for v in obj.data.vertices]; ys = [v.co.y for v in obj.data.vertices]; zs = [v.co.z for v in obj.data.vertices]
print("stretch", round(k, 4), "-> size", round(max(xs) - min(xs), 3), round(max(ys) - min(ys), 3), round(max(zs) - min(zs), 3),
      "min z", round(min(zs), 4), "scale", tuple(obj.scale))
# Result: stretch 1.0515 -> size 1.2 1.0 0.9 min z 0.0 scale (1.0, 1.0, 1.0)


# (read-only helper) rock surface heights, to place the niche, lamp and jasmine band on it
import bpy
obj = bpy.data.objects["Shrine_Rock"]
vs = [v.co for v in obj.data.vertices]
top = max(vs, key=lambda c: c.z)
front = max(vs, key=lambda c: c.x)
print("top vertex", tuple(round(a, 3) for a in top), "front vertex", tuple(round(a, 3) for a in front))
for zb in (0.30, 0.45, 0.60, 0.72):
    ring = [c for c in vs if abs(c.z - zb) < 0.09]
    if ring:
        print("z~%.2f  max x %.3f  max y %.3f" % (zb, max(c.x for c in ring), max(c.y for c in ring)))


# --- SHRINE call 2: Shrine_Niche, a dark stone box 0.10 x 0.30 x 0.30 m set into the rock's front face (+X), centre x 0.55, z 0.45, niche #3a3632
# (Replaced by call 2b after Shriram's interruption.)
import bpy

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["rock_shrine"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.55, 0.0, 0.45))
obj = bpy.context.active_object
obj.name = "Shrine_Niche"
obj.data.name = "Shrine_Niche"
obj.scale = (0.10, 0.30, 0.30)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("Shrine_niche", "#3a3632", 0.9))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 3) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SHRINE call 1c: dress the rock's front (+X) into a flat face at x = 0.50 for the goddess panel; colour faces: turmeric around the front, jasmine at the front of the base
import bpy, bmesh

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat

obj = bpy.data.objects["Shrine_Rock"]
me = obj.data
for v in me.vertices:
    if v.co.x > 0.50:
        v.co.x = 0.50                                # flat dressed face; the relief in front brings the asset back to x = 0.60
me.update()
me.materials.clear()
me.materials.append(flat_material("Shrine_rock", "#6f6a63"))        # slot 0
me.materials.append(flat_material("Shrine_turmeric", "#d9a21b"))    # slot 1
me.materials.append(flat_material("Shrine_jasmine", "#f2efe6"))     # slot 2
counts = [0, 0, 0]
for p in me.polygons:
    c = p.center
    if c.z < 0.15 and c.x > 0.10:
        p.material_index = 2
    elif c.x > 0.40:
        p.material_index = 1
    else:
        p.material_index = 0
    counts[p.material_index] += 1
xs = [v.co.x for v in me.vertices]
print("rock x range", round(min(xs), 3), round(max(xs), 3), "| faces rock/turmeric/jasmine", counts, "| scale", tuple(obj.scale))
# Result: rock x range -0.6 0.5 | faces rock/turmeric/jasmine [60, 12, 8] | scale (1.0, 1.0, 1.0)


# --- SHRINE call 2b: replace the small niche with Shrine_Panel, a dark recessed stone panel 0.055 x 0.36 x 0.44 m on the dressed face (x 0.50-0.555, z 0.20-0.64), #3a3632
import bpy

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat

old = bpy.data.objects.get("Shrine_Niche")
if old:
    bpy.data.objects.remove(old, do_unlink=True)
root = bpy.data.objects["rock_shrine"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.5275, 0.0, 0.42))
obj = bpy.context.active_object
obj.name = "Shrine_Panel"
obj.data.name = "Shrine_Panel"
obj.scale = (0.055, 0.36, 0.44)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("Shrine_niche", "#3a3632", 0.9))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 4) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SHRINE call 3: Goddess_Robe, an 8-segment cone flattened into a relief: 0.045 deep x 0.24 wide x 0.26 tall, standing on the panel (x 0.555-0.60, z 0.25-0.51), kumkum #b3202a
import bpy

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["rock_shrine"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.12, radius2=0.035, depth=0.26, end_fill_type="NGON",
                                location=(0.5775, 0.0, 0.38))
obj = bpy.context.active_object
obj.name = "Goddess_Robe"
obj.data.name = "Goddess_Robe"
obj.scale = (0.1875, 1.0, 1.0)                       # 0.24 m across -> 0.045 m deep: a relief, not a statue
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("Goddess_kumkum", "#b3202a", 0.7))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 4) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SHRINE call 4: Goddess_Head, an icosphere (subdivisions 1, 20 triangles) flattened to 0.045 x 0.12 x 0.12 m, above the robe (centre x 0.5775, z 0.565), turmeric #d9a21b
import bpy

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["rock_shrine"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.06, location=(0.5775, 0.0, 0.565))
obj = bpy.context.active_object
obj.name = "Goddess_Head"
obj.data.name = "Goddess_Head"
obj.scale = (0.375, 1.0, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("Shrine_turmeric", "#d9a21b"))
obj.parent = root
print(obj.name, "loc", tuple(round(v, 4) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SHRINE call 5: Shrine_Lamp, an 8-segment brass cylinder 0.12 m wide x 0.12 m tall, on the rock's top (base sunk to z 0.86 so it meets the sloping top), brass #c9a24a
import bpy

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat

root = bpy.data.objects["rock_shrine"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=0.12, end_fill_type="NGON", location=(0.0, 0.0, 0.92))
obj = bpy.context.active_object
obj.name = "Shrine_Lamp"
obj.data.name = "Shrine_Lamp"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
mat = flat_material("Shrine_brass", "#c9a24a", 0.35)
next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Metallic"].default_value = 0.8
obj.data.materials.append(mat)
obj.parent = root
print(obj.name, "loc", tuple(round(v, 4) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SHRINE call 6: Shrine_Flame, an 8-segment cone 0.07 m wide x 0.12 m tall on the lamp (z 0.98-1.10), flame #ffb347 with a soft glow
import bpy

def flat_material(name, hex_colour, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True
    h = hex_colour.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*lin, 1.0)
    return mat, bsdf, lin

root = bpy.data.objects["rock_shrine"]
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.035, radius2=0.0, depth=0.12, end_fill_type="NGON", location=(0.0, 0.0, 1.04))
obj = bpy.context.active_object
obj.name = "Shrine_Flame"
obj.data.name = "Shrine_Flame"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
mat, bsdf, lin = flat_material("Shrine_flame", "#ffb347", 0.5)
if "Emission Color" in bsdf.inputs:
    bsdf.inputs["Emission Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Emission Strength"].default_value = 2.0
obj.data.materials.append(mat)
obj.parent = root
print(obj.name, "loc", tuple(round(v, 4) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions), "scale", tuple(obj.scale))


# --- SHRINE call 7 (read-only): whole-asset bounds, triangles, transforms
import bpy
from mathutils import Vector
root = bpy.data.objects["rock_shrine"]
deps = bpy.context.evaluated_depsgraph_get()
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3); tris = 0
for o in root.children:
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    me = o.evaluated_get(deps).to_mesh(); me.calc_loop_triangles(); tris += len(me.loop_triangles); o.evaluated_get(deps).to_mesh_clear()
    print(f"{o.name:14s} rot {tuple(round(v, 4) for v in o.rotation_euler)} scale {tuple(o.scale)} mats {[m.name for m in o.data.materials]}")
print("asset size X x Y x Z:", tuple(round(v, 3) for v in (hi - lo)), "x range", round(lo.x, 3), round(hi.x, 3), "lowest z:", round(lo.z, 4))
print("shapes:", len(root.children), "triangles:", tris)
# Result: all six parts rot (0,0,0) scale (1,1,1); asset size X x Y x Z: (1.2, 1.0, 1.1) x range -0.6 0.6 lowest z: 0.0; shapes: 6 triangles: 182


# --- SHRINE call 8: save the source file
import bpy
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)


# =====================================================================================================
# BUILD 3 (brief revision 3), ~20:22-20:27 EDT. Shriram inspected build 2 and asked: "the flame on top doesn't
# resemble a flame at all, rather it just looks like a sharp triangleon top, it should have a lamp holder and the
# top should have an orange flame which keeps burning and the size of it need not be way too big as vastav's dad
# would burn it every night or would get someone to burn it for him so wherever it's kept needs to be accessible,
# also for the devi, instead of jsut shapes could we not do something to make her resemble more on the rock?
# implement al of this" (then: "no go ahead").
# Each execute_blender_code body was one line running a snippet file saved first:
#     exec(compile(open(".../shrine_r3_<n>.py").read(), "shrine_r3_<n>.py", "exec"))
# The snippets, and the helper file they all run first, follow verbatim. (Call 4 made two objects, the holder
# and the flame, in one call.)
# =====================================================================================================

# ---- shrine_r3_common.py (run at the top of calls 1-4)
import bpy, bmesh, math
from mathutils import Vector

def flat_material(name, hex_colour, roughness=0.8, metallic=0.0, emission=0.0):
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

def replace_with(kind, name, location, **kw):
    """Remove the old part of this name and add a fresh primitive in its place."""
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    bpy.ops.object.select_all(action="DESELECT")
    getattr(bpy.ops.mesh, kind)(location=location, **kw)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    return obj

def bisect_z(bm, z_local):
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector((0, 0, z_local)), plane_no=Vector((0, 0, 1)))

def report(obj):
    obj.data.calc_loop_triangles()
    print(obj.name, "loc", tuple(round(v, 4) for v in obj.location), "dims", tuple(round(v, 3) for v in obj.dimensions),
          "rot", tuple(round(math.degrees(v), 1) for v in obj.rotation_euler), "scale", tuple(obj.scale),
          "tris", len(obj.data.loop_triangles))


# --- SHRINE r3 call 0: open the shrine's own file (suv.blend was saved first)
import bpy
bpy.ops.wm.open_mainfile(filepath="/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/walker-vidiyum-mun-shriram-a/blender/rock_shrine.blend")
print("opened", bpy.data.filepath, [o.name for o in bpy.data.objects])


# --- SHRINE r3 call 1: Shrine_Panel becomes an arched niche (a pointed top, like a temple niche) with a sea-blue wave band at its foot,
#     so the goddess stands on the sea. Same box, x 0.50-0.555, y +-0.18, z 0.20-0.64, peak raised to 0.72. Stone #3a3632, sea #2b6f8e
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))
root = bpy.data.objects["rock_shrine"]
obj = replace_with("primitive_cube_add", "Shrine_Panel", (0.5275, 0.0, 0.42), size=1.0)
obj.scale = (0.055, 0.36, 0.44)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
me = obj.data
me.materials.clear()
me.materials.append(flat_material("Shrine_niche", "#3a3632", 0.9))     # 0
me.materials.append(flat_material("Shrine_sea", "#2b6f8e", 0.5))       # 1
bm = bmesh.new(); bm.from_mesh(me)
geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector((0, 0, 0)), plane_no=Vector((0, 1, 0)))
for v in bm.verts:
    if abs(v.co.y) < 1e-5 and v.co.z > 0:
        v.co.z += 0.08                                  # the arch's peak, 0.72 m
front = [f for f in bm.faces if f.normal.x > 0.9]
edges = list({e for f in front for e in f.edges}); verts = list({v for f in front for v in f.verts})
bmesh.ops.bisect_plane(bm, geom=front + edges + verts, plane_co=Vector((0, 0, 0.27 - 0.42)), plane_no=Vector((0, 0, 1)))
for f in bm.faces:
    f.material_index = 1 if (f.normal.x > 0.9 and f.calc_center_median().z < 0.27 - 0.42) else 0
bm.to_mesh(me); bm.free(); me.update()
obj.parent = root
report(obj)


# --- SHRINE r3 call 2: Goddess_Robe rebuilt as a figure in relief: an 8-sided cylinder with rings at 0.40 / 0.415 / 0.47 shaped into a
#     flared saree skirt (0.22 wide at 0.27), a waist (0.09 at 0.40), shoulders (0.15 at 0.47) and a neck (0.056 at 0.505); 0.044 deep.
#     A gold band at the waist (0.40-0.415): Manimekala means "jewelled girdle". Kumkum #b3202a, gold #c9a24a
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))
root = bpy.data.objects["rock_shrine"]
CZ = 0.3875                                             # z 0.27-0.505
obj = replace_with("primitive_cylinder_add", "Goddess_Robe", (0.5775, 0.0, CZ), vertices=8, radius=0.1, depth=0.235, end_fill_type="NGON")
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
me = obj.data
me.materials.clear()
me.materials.append(flat_material("Goddess_kumkum", "#b3202a", 0.7))  # 0
me.materials.append(flat_material("Shrine_brass", "#c9a24a", 0.35, 0.8))  # 1 gold girdle
bm = bmesh.new(); bm.from_mesh(me)
for z in (0.40, 0.415, 0.47):
    bisect_z(bm, z - CZ)
profile = {0.27: 0.11, 0.40: 0.045, 0.415: 0.047, 0.47: 0.075, 0.505: 0.028}   # world z -> half-width in Y
for v in bm.verts:
    zw = round(v.co.z + CZ, 3)
    r = profile[min(profile, key=lambda k: abs(k - zw))]
    a = math.atan2(v.co.y, v.co.x)
    v.co.x = math.cos(a) * r * 0.2                     # flattened: a relief 0.044 m deep at the hem
    v.co.y = math.sin(a) * r
for f in bm.faces:
    zc = f.calc_center_median().z + CZ
    f.material_index = 1 if (abs(f.normal.z) < 0.9 and 0.40 < zc < 0.415) else 0
bm.to_mesh(me); bm.free(); me.update()
obj.parent = root
report(obj)


# --- SHRINE r3 call 3: Goddess_Head rebuilt with a pointed crown (kireedam): icosphere subdivisions 1, 0.12 m, flattened to 0.045 deep,
#     top vertex raised 0.045 m; the crown faces gold, the face turmeric #d9a21b
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))
root = bpy.data.objects["rock_shrine"]
obj = replace_with("primitive_ico_sphere_add", "Goddess_Head", (0.5775, 0.0, 0.565), subdivisions=1, radius=0.06)
obj.scale = (0.375, 1.0, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
me = obj.data
me.materials.clear()
me.materials.append(flat_material("Shrine_turmeric", "#d9a21b"))          # 0 face
me.materials.append(flat_material("Shrine_brass", "#c9a24a", 0.35, 0.8))  # 1 crown
top = max(me.vertices, key=lambda v: v.co.z)
top.co.z += 0.045
for p in me.polygons:
    p.material_index = 1 if top.index in p.vertices else 0
me.update()
obj.parent = root
report(obj)


# --- SHRINE r3 call 4: the lamp moves off the top of the rock to the front, on the sand beside the goddess (x 0.52, y 0.30), where
#     whoever lights it each night can reach it. Shrine_Lamp = a brass holder from one 8-sided cylinder: a 0.09 m foot, a 0.032 m stem
#     at 0.08 and a 0.11 m bowl at 0.14 (a small kuthu-vilakku shape). Shrine_Flame = a teardrop on the bowl: icosphere subdivisions 1,
#     stretched 1.5x upward with its tip pulled up 0.045 m, glowing orange #ff8c1a. The model can't animate (course rule); in Godot its light can flicker.
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))
root = bpy.data.objects["rock_shrine"]
LX, LY, CZ = 0.52, 0.30, 0.07
lamp = replace_with("primitive_cylinder_add", "Shrine_Lamp", (LX, LY, CZ), vertices=8, radius=0.04, depth=0.14, end_fill_type="NGON")
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bm = bmesh.new(); bm.from_mesh(lamp.data)
bisect_z(bm, 0.08 - CZ)
profile = {0.0: 0.045, 0.08: 0.016, 0.14: 0.055}
for v in bm.verts:
    zw = v.co.z + CZ
    r = profile[min(profile, key=lambda k: abs(k - zw))]
    a = math.atan2(v.co.y, v.co.x)
    v.co.x = math.cos(a) * r
    v.co.y = math.sin(a) * r
bm.to_mesh(lamp.data); bm.free(); lamp.data.update()
lamp.data.materials.clear()
lamp.data.materials.append(flat_material("Shrine_brass", "#c9a24a", 0.35, 0.8))
lamp.parent = root
report(lamp)

flame = replace_with("primitive_ico_sphere_add", "Shrine_Flame", (LX, LY, 0.18), subdivisions=1, radius=0.028)
flame.scale = (1.0, 1.0, 1.5)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
tip = max(flame.data.vertices, key=lambda v: v.co.z)
tip.co.z += 0.045
flame.data.update()
flame.data.materials.clear()
flame.data.materials.append(flat_material("Shrine_flame", "#ff8c1a", 0.5, 0.0, 4.0))
flame.parent = root
report(flame)


# Results (get_scene_info / measured from vertices): Panel 0.055 x 0.36 x 0.52 (z 0.20-0.72, arch peak), 26 tris; Robe 0.044 x 0.22 x 0.235,
# 76 tris; Head 0.04 x 0.10 x 0.165 with crown (z 0.505-0.67), 20 tris; Lamp holder 0.11 x 0.11 x 0.14 on the floor, 44 tris;
# Flame 0.05 x 0.05 x 0.13 (z 0.138-0.267), 20 tris. Whole asset: 1.20 x 1.00 x 0.90 m, lowest z 0.0, 6 shapes, 266 triangles,
# all rotations 0 and scales 1. Then: bpy.ops.wm.save_mainfile()
