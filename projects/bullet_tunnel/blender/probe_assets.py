# Probe: place candidate library assets in a row and render one lit still + report poly counts. Uses EngineX place_asset().
import bpy, math, time
from mathutils import Vector

CAND = [  # (id, size_m)
    ('ai3d-fishing-trawler-boat-43c178', 9.0),
    ('ai3d-compact-yellow-excavator-29a8ee', 6.0),
    ('veh-jcb-excavator', 8.0),
    ('omni-simready-containers-shipping-01-container_a01', 6.0),
    ('omni-simready-containers-shipping-01-container_b02', 6.0),
    ('metropolitan-skyscraper-1', 60.0),
    ('metropolitan-skyscraper-3', 60.0),
    ('metropolitan-skyscraper-5', 60.0),
    ('terrascape-rock-1', 10.0),
    ('ai3d-cartoon-palm-tree-3fccdd', 8.0),
]
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
rep = []
x = 0.0
for aid, size in CAND:
    t = time.time()
    try:
        root = place_asset(aid, location=(x, 0, 0), size=size, floor=0.0)
        allo = [root] + list(root.children_recursive) if hasattr(root, 'children_recursive') else [root]
        polys = sum(len(o.data.polygons) for o in allo if o.type == 'MESH')
        rep.append(dict(id=aid, ok=True, polys=polys, sec=round(time.time() - t, 1)))
    except Exception as e:
        rep.append(dict(id=aid, ok=False, err=str(e)[:160]))
    x += size * 0.7 + 8
result['report'] = rep
w = bpy.context.scene.world or bpy.data.worlds.new('W'); bpy.context.scene.world = w
w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5, 0.55, 0.65, 1)
bpy.ops.mesh.primitive_plane_add(size=600, location=(x / 2, 0, -0.01))
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(55), 0, math.radians(30))); bpy.context.active_object.data.energy = 4
cam = bpy.data.cameras.new('c'); co = bpy.data.objects.new('c', cam); bpy.context.scene.collection.objects.link(co)
co.location = (x / 2, -x * 0.9, x * 0.25); co.rotation_euler = (math.radians(78), 0, 0); cam.lens = 24; cam.clip_end = 3000
bpy.context.scene.camera = co
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x, sc.render.resolution_y = 1600, 600
sc.render.filepath = out + '/probe.png'
bpy.ops.render.render(write_still=True)
