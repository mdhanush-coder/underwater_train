import bpy, math
from mathutils import Vector
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
root = place_asset('veh-jcb-excavator', location=(0, 0, 0), size=8.6, floor=0.0)
bpy.context.view_layer.update()
allo = [root] + list(root.children_recursive)
ms = [o for o in allo if o.type == 'MESH']
cs = [o.matrix_world @ Vector(c) for o in ms for c in o.bound_box]
result['dims'] = [round(max(c[i] for c in cs) - min(c[i] for c in cs), 2) for i in range(3)]
result['centre'] = [round((max(c[i] for c in cs) + min(c[i] for c in cs)) / 2, 2) for i in range(3)]
result['meshes'] = [[o.name, len(o.data.polygons), [m.name for m in o.data.materials][:3]] for o in ms][:25]
result['n_meshes'] = len(ms)
# recolour: yellow body, dark tracks/glass/hydraulics
def flat(name, col, rough=0.6, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal; return m
yel = flat('jcb_yellow', (0.72, 0.45, 0.02)); blk = flat('jcb_black', (0.03, 0.03, 0.035)); stl = flat('jcb_steel', (0.35, 0.36, 0.38), 0.4, 0.9)
for o in ms:
    n = o.name.lower()
    m = blk if any(k in n for k in ('track', 'tyre', 'tire', 'wheel', 'glass', 'window', 'seat', 'hose', 'pipe')) else stl if any(k in n for k in ('piston', 'rod', 'pin', 'bolt')) else yel
    o.data.materials.clear(); o.data.materials.append(m)
w = bpy.context.scene.world or bpy.data.worlds.new('W'); bpy.context.scene.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5, 0.55, 0.65, 1)
bpy.ops.mesh.primitive_plane_add(size=40); bpy.ops.object.light_add(type='SUN', rotation=(math.radians(50), 0, math.radians(30))); bpy.context.active_object.data.energy = 3
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); bpy.context.scene.collection.objects.link(cam)
cam.location = (9, -12, 5); bpy.context.scene.camera = cam
d = Vector((0, 0, 1.8)) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x, sc.render.resolution_y = 1000, 640
sc.render.filepath = out + '/jcb.png'; bpy.ops.render.render(write_still=True)
