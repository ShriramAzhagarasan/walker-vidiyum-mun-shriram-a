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
