# Probe v2: Reallusion Worker without its studio backdrop, scaled from the body mesh, three arm-pose axis tests side by side.
import bpy, math
from mathutils import Vector, Euler
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
rep = {}
roots = []
for k in range(3):
    root = place_asset('omni-characters-Worker', location=(k * 1.6 - 1.6, 0, 0), size=1.8, floor=0.0)
    bpy.context.view_layer.update()
    allo = [root] + list(root.children_recursive)
    for o in allo:
        if o.type == 'MESH' and o.name.lower().startswith('background'):
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.context.view_layer.update()
    allo = [root] + list(root.children_recursive)
    body = [o for o in allo if o.type == 'MESH' and 'Body' in o.name]
    cs = [o.matrix_world @ Vector(c) for o in body for c in o.bound_box]
    dims = [max(c[i] for c in cs) - min(c[i] for c in cs) for i in range(3)]
    if k == 0: rep['body_dims_before'] = [round(d, 2) for d in dims]
    hi = max(range(3), key=lambda i: dims[i])
    rep.setdefault('tall_axis', []).append(hi)
    roots.append((root, allo, body))
# normalise: tallest body axis -> height 1.78 m, then stand up on z=0
for k, (root, allo, body) in enumerate(roots):
    cs = [o.matrix_world @ Vector(c) for o in body for c in o.bound_box]
    dims = [max(c[i] for c in cs) - min(c[i] for c in cs) for i in range(3)]
    f = 1.78 / max(dims)
    root.scale = tuple(s * f for s in root.scale)
    bpy.context.view_layer.update()
    cs = [o.matrix_world @ Vector(c) for o in body for c in o.bound_box]
    root.location.z -= min(c.z for c in cs)
    rep.setdefault('height_after', []).append(round(max(c.z for c in cs) - min(c.z for c in cs), 2))
    arm = [o for o in allo if o.type == 'ARMATURE'][0]
    for nm in ('L_Upperarm', 'R_Upperarm'):
        pb = arm.pose.bones.get(nm)
        if pb:
            pb.rotation_mode = 'XYZ'
            e = [0, 0, 0]; e[k] = math.radians(55 if nm.startswith('L') else -55)
            pb.rotation_euler = tuple(e)
    rep.setdefault('bones_arm', [b.name for b in arm.data.bones if 'Upperarm' in b.name or 'Forearm' in b.name][:6])
result.update(rep)
w = bpy.context.scene.world or bpy.data.worlds.new('W'); bpy.context.scene.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5, 0.55, 0.65, 1)
bpy.ops.mesh.primitive_plane_add(size=30); bpy.ops.object.light_add(type='SUN', rotation=(math.radians(50), 0, math.radians(30))); bpy.context.active_object.data.energy = 4
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); bpy.context.scene.collection.objects.link(cam)
cam.location = (0, -6.2, 1.1); cam.rotation_euler = (math.radians(88), 0, 0); bpy.context.scene.camera = cam
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x, sc.render.resolution_y = 1200, 700
sc.render.filepath = out + '/worker2.png'; bpy.ops.render.render(write_still=True)
