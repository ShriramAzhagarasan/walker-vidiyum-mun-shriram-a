# build_fence_segment.py: the code Claude ran through the Blender MCP (mcp-for-blender 2.1.9, Blender 5.2.2 LTS) to build the
# fence segment, ~20:28-20:31 EDT on 2026-10-15. Shriram chose option A, wooden posts and ropes matching the A2 beach art ("A").
# Each execute_blender_code body was one line running a snippet file saved first, e.g.
#     exec(compile(open(".../fence_1_post.py").read(), "fence_1_post.py", "exec"))
#     build_post("Fence_Post_L", -1.14)
# The snippets follow verbatim, in order. Calls 1-6 also ran the shared helper file (flat_material, replace_with,
# bisect_z, report), which is printed once at the top; it is the same file as in build_rock_shrine.py.

# ---- shrine_r3_common.py
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


# --- FENCE call 0: own file for this asset (suv.blend is saved): clear the SUV, save as fence_segment.blend, metric units, root Empty at the world origin
import bpy
for o in list(bpy.data.objects):
    if o.name == "suv" or o.name.startswith("SUV_"):
        bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath="/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/walker-vidiyum-mun-shriram-a/blender/fence_segment.blend")
us = bpy.context.scene.unit_settings
systems = [i.identifier for i in us.bl_rna.properties["system"].enum_items]
us.system = "METRIC" if "METRIC" in systems else systems[0]
us.scale_length = 1.0
root = bpy.data.objects.new("fence_segment", None)    # origin = centre of the underside; panels tile at x = i * 2.40
bpy.context.scene.collection.objects.link(root)
root.empty_display_size = 0.4
print("file:", bpy.data.filepath, "| objects:", [o.name for o in bpy.data.objects])


# --- FENCE calls 1-2: build_post(name, x): a weathered wooden post, a box 0.12 x 0.12 x 2.10 m standing on the floor, its top
#     tapered to 0.08 m so it reads as a cut timber post; wood #5b4632. Post_L at x -1.14, Post_R at x +1.14 (outer faces at +-1.20).
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))

def build_post(name, x):
    root = bpy.data.objects["fence_segment"]
    obj = replace_with("primitive_cube_add", name, (x, 0.0, 1.05), size=1.0)
    obj.scale = (0.12, 0.12, 2.10)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for v in obj.data.vertices:
        if v.co.z > 0:
            v.co.x *= 0.67; v.co.y *= 0.67               # tapered top
    obj.data.update()
    obj.data.materials.clear()
    obj.data.materials.append(flat_material("Fence_wood", "#5b4632", 0.9))
    obj.parent = root
    report(obj)

build_post("Fence_Post_L", -1.14)   # call 1
build_post("Fence_Post_R", 1.14)    # call 2
# Result each: dims (0.12, 0.12, 2.1) rot 0 scale 1 tris 12


# --- FENCE calls 3-5: build_rope(name, z): a rope strung between the posts, a 6-sided open cylinder 0.03 m thick from x -1.08 to +1.08
#     (inside the posts), cut at the middle and sagging 4 cm there; rope #8c7a5b. Ropes at z 0.60, 1.10, 1.60.
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))

def build_rope(name, z):
    root = bpy.data.objects["fence_segment"]
    obj = replace_with("primitive_cylinder_add", name, (0.0, 0.0, z), vertices=6, radius=0.015, depth=2.16,
                       end_fill_type="NOTHING", rotation=(0.0, math.radians(90), 0.0))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bm = bmesh.new(); bm.from_mesh(obj.data)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector((0, 0, 0)), plane_no=Vector((1, 0, 0)))
    for v in bm.verts:
        if abs(v.co.x) < 1e-4:
            v.co.z -= 0.04                                  # the sag
    bm.to_mesh(obj.data); bm.free(); obj.data.update()
    obj.data.materials.clear()
    obj.data.materials.append(flat_material("Fence_rope", "#8c7a5b", 0.9))
    obj.parent = root
    report(obj)

build_rope("Fence_Rope_Low", 0.60)   # call 3
build_rope("Fence_Rope_Mid", 1.10)   # call 4
build_rope("Fence_Rope_High", 1.60)  # call 5
# Result each: dims (2.16, 0.03, 0.026) rot 0 scale 1 tris 24


# --- FENCE call 6: Fence_Sign, the family's red "private" board, a box 0.50 x 0.03 x 0.30 m hung on the beach side (-Y) at z 1.20-1.50,
#     x 0.30 (off-centre, like a sign someone nailed up). No lettering: text would need a painted texture, which the course rules out. #c0392b
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))
root = bpy.data.objects["fence_segment"]
obj = replace_with("primitive_cube_add", "Fence_Sign", (0.30, -0.045, 1.35), size=1.0)
obj.scale = (0.50, 0.03, 0.30)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("Fence_sign", "#c0392b", 0.6))
obj.parent = root
report(obj)


# --- FENCE call 6b: correction after get_scene_info + look: at z 1.20-1.50 and y -0.06..-0.03 the sign floated between the middle and top ropes, touching nothing.
#     Now tied across the middle rope: z 0.95-1.25, y -0.045..-0.015 (flush with the rope's front), x 0.30. #c0392b
exec(compile(open("/private/tmp/claude-501/-Users-shriramalagarasan-Desktop-NortheasternUniversity-Fall2026-walker-vidiyum-mun-shriram-a/dc44086f-b290-4df3-9577-22f3faebd0de/scratchpad/blender/shrine_r3_common.py").read(), "shrine_r3_common.py", "exec"))
root = bpy.data.objects["fence_segment"]
obj = replace_with("primitive_cube_add", "Fence_Sign", (0.30, -0.03, 1.10), size=1.0)
obj.scale = (0.50, 0.03, 0.30)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
obj.data.materials.clear()
obj.data.materials.append(flat_material("Fence_sign", "#c0392b", 0.6))
obj.parent = root
report(obj)


# --- FENCE call 7 (read-only) + save: whole-asset bounds from vertices, triangles, transforms
import bpy
from mathutils import Vector
root = bpy.data.objects["fence_segment"]
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3); tris = 0
for o in root.children:
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
    print(f"{o.name:16s} rot {tuple(o.rotation_euler)} scale {tuple(o.scale)} tris {len(o.data.loop_triangles)}")
print("asset size X x Y x Z:", tuple(round(v, 3) for v in (hi - lo)), "lowest z:", round(lo.z, 4), "| shapes:", len(root.children), "triangles:", tris)
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)
# Result: all six parts rot 0 scale 1; asset size X x Y x Z: (2.4, 0.12, 2.1) lowest z: 0.0 | shapes: 6 triangles: 108
