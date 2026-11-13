# Chapter 3 plate "The machine" (46.85 s): full TBM (cutterhead, shield, jacks, 8 backup gantries) bored into a soil cutaway
# (same look as the hook cutaway). One continuous camera. Runs after skilllib.py + bt_model.py. args: mode=preview|anim, pct.
import bpy, bmesh, math, random
from mathutils import Vector, Quaternion
FPS = 30
XE = 320.0
TZ, TR, TL = -35.0, 6.55, 0.6
T_END = 46.85
PATH = [
    (0.0, (-95, -55, -25), (-60, 0, -35), 30),
    (3.5, (-55, -40, -33), (-20, 0, -35), 30),
    (6.4, (-6, -30, -33), (6, 0, -35), 28),
    (10.4, (24, -27, -33), (6, 0, -35), 26),
    (17.6, (20, -30, -33), (4, 0, -35), 26),
    (22.0, (-45, -125, -29), (-42, 0, -35), 24),
    (24.4, (-38, -116, -31), (-42, 0, -35), 24),
    (28.6, (16, -26, -33), (0, 0, -35), 30),
    (34.6, (-6, -31, -34), (-4, 0, -36), 30),
    (36.6, (-4, -30, -35), (2, 0, -35), 28),
    (44.0, (17, -23, -33), (6, 0, -36), 26),
    (T_END, (19, -21, -33), (6, 0, -36), 26),
]


def soil(name, c, z0, z1, cut):
    o = Acc(name, strata(mat(name, c, 0.85), tuple(v * 0.55 for v in c), tuple(min(1, v * 1.25) for v in c), 0.12, 3.0, 0.45)); o.box((2 * XE, 300, z0 - z1), (0, 150, (z0 + z1) / 2)); ob = o.build()
    if cut:                                   # bored only behind the face (x < 1.2): the machine is pushing into solid ground
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=TR + TL + 0.3, depth=XE + 1.2, location=(-(XE - 1.2) / 2, 0, TZ), rotation=(0, math.pi / 2, 0))
        cu = bpy.context.active_object
        md = ob.modifiers.new('tun', 'BOOLEAN'); md.object = cu; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
        bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier='tun'); bpy.data.objects.remove(cu, do_unlink=True)
    return ob


def build():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    L = [('seabed_mud', (0.05, 0.04, 0.03), -6, -9, False), ('soft_clay', (0.34, 0.22, 0.12), -9, -20, False), ('stiff_clay', (0.52, 0.36, 0.2), -20, -30, True),
         ('weathered_rock', (0.24, 0.22, 0.2), -30, -46, True), ('basalt', (0.09, 0.1, 0.13), -46, -90, False)]
    seam = Acc('layer_seams', mat('seam', (0.03, 0.03, 0.035), 0.9))
    for nm, c, z0, z1, cut in L:
        soil(nm, c, z0, z1, cut); seam.box((2 * XE, 0.12, 0.35), (0, -0.04, z0))
    seam.build()
    ws = mat('water_section', (0.02, 0.18, 0.24), 0.3, 0.0, (0.03, 0.22, 0.3), 0.8); ws.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.6
    try: ws.surface_render_method = 'DITHERED'
    except Exception: pass
    S = Acc('water_section', ws); S.box((2 * XE, 0.1, 6), (0, -0.05, -3)); S.build()
    # segment lining only behind the tail (x < -14), half-pipe y >= 0 with ring seams
    bm = bmesh.new()
    res = bmesh.ops.create_cone(bm, cap_ends=False, segments=96, radius1=TR + TL * 0.5, radius2=TR + TL * 0.5, depth=XE - 14)
    bmesh.ops.transform(bm, matrix=Quaternion((0, 1, 0), math.pi / 2).to_matrix().to_4x4(), verts=res['verts'])
    bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True)
    me = bpy.data.meshes.new('lining'); bm.to_mesh(me); bm.free()
    lin = bpy.data.objects.new('lining', me); sc.collection.objects.link(lin); lin.location = (-(XE + 14) / 2, 0, TZ)
    for p in me.polygons: p.use_smooth = True
    sol = lin.modifiers.new('s', 'SOLIDIFY'); sol.thickness = TL; sol.offset = 0
    lm = mat('lining', (0.42, 0.41, 0.39), 0.6); nt = lm.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'
    wv.inputs['Scale'].default_value = 0.5; wv.wave_profile = 'SAW'
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.5; bp.inputs['Distance'].default_value = 0.15
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    me.materials.append(lm)
    # the machine: real counts (84 discs / 124 scrapers / 16 bucket lips), 8 backup gantries -> ~96 m
    tbm, head = build_tbm('tbm', gantries=8)
    tbm.location = (0, 0, TZ)
    for t, x in ((0.0, -1.2), (T_END, 0.4)):                 # slow advance under the jacks
        tbm.location.x = x; tbm.keyframe_insert('location', index=0, frame=int(t * FPS) + 1)
    for t, ang in ((0.0, 0.0), (T_END, 300.0)):             # cutterhead turns (constant rpm is intended)
        head.rotation_euler = (0, 0, math.radians(ang)); head.keyframe_insert('rotation_euler', frame=int(t * FPS) + 1)
    for fc in fcurves_of(head):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    jk = bpy.data.objects.get('articulation_jacks')
    if jk:                                                     # jacks extend while the machine is pushed (29-35 s)
        jk.scale = (1, 1, 1); jk.keyframe_insert('scale', frame=int(29.0 * FPS))
        jk.scale = (1, 1, 1.25); jk.keyframe_insert('scale', frame=int(34.6 * FPS))
    # lights: warm tunnel strips + work lamps, a teal fill on the cut face; the "problem" beat dims them (35-37 s)
    Lt = Acc('tunnel_lights', mat('strip', (1, 0.9, 0.7), 0.4, 0, (1.0, 0.88, 0.65), 3.0))
    Lt.box((XE, 0.35, 0.18), (-(XE + 14) / 2, 3.7, TZ + 4.9)); Lt.box((XE, 0.35, 0.18), (-(XE + 14) / 2, 5.8, TZ - 0.3)); Lt.build()
    lamps = []
    for x in range(-120, 1, 18):
        bpy.ops.object.light_add(type='POINT', location=(x, -2.0, TZ + 3.5)); l = bpy.context.active_object
        l.data.energy = 1800; l.data.color = (1.0, 0.82, 0.55); l.data.shadow_soft_size = 2.0; lamps.append(l)
    bpy.ops.object.light_add(type='AREA', location=(0, -80, -25), rotation=(math.radians(90), 0, 0)); f = bpy.context.active_object
    f.data.energy = 140000; f.data.size = 240; f.data.color = (0.8, 0.92, 1.0); lamps.append(f)
    for l in lamps:
        e0 = l.data.energy
        for t, k in ((34.8, 1.0), (36.2, 0.35), (44.6, 0.35), (45.6, 0.8)):
            l.data.energy = e0 * k; l.data.keyframe_insert('energy', frame=int(t * FPS) + 1)
    # soft face slumping toward the machine (44.7-46.8 s)
    rng = random.Random(5); clay = noisy(mat('slump', (0.36, 0.24, 0.13), 0.9), 9.0, 0.6, 0.5)
    for i in range(26):
        y = rng.uniform(-3.5, -0.3); z = TZ + rng.uniform(-4, 5.5); x = 2.0 + rng.uniform(0, 0.8)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rng.uniform(0.25, 0.7), location=(x, y, z)); ch = bpy.context.active_object
        for v in ch.data.vertices: v.co *= rng.uniform(0.7, 1.25)                       # irregular clods, not balls
        ch.scale = (rng.uniform(0.8, 1.4), rng.uniform(0.6, 1.1), rng.uniform(0.5, 0.9)); ch.rotation_euler = [rng.uniform(0, 6.28) for _ in range(3)]
        ch.data.materials.append(clay); ch.hide_render = True; ch.keyframe_insert('hide_render', frame=int(44.6 * FPS))
        ch.hide_render = False; ch.keyframe_insert('hide_render', frame=int(44.7 * FPS))
        ch.keyframe_insert('location', frame=int(44.7 * FPS))
        ch.location = (x - rng.uniform(0.5, 1.6), y - rng.uniform(0.0, 1.0), z - rng.uniform(1.5, 4.0)); ch.keyframe_insert('location', frame=int(T_END * FPS))
    w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    tcw = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = -0.6; mr.inputs['From Max'].default_value = 0.7
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.004, 0.03, 0.045, 1); cr.color_ramp.elements[1].color = (0.03, 0.2, 0.26, 1)
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.9; ot = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(tcw.outputs['Generated'], sep.inputs['Vector']); nt.links.new(sep.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], ot.inputs['Surface'])
    return head


def anchors(cam, pts, times):
    """Screen positions (0-1, y from top) of named world points at given times, for the overlay leaders."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; outd = {}
    for name, fn in pts.items():
        outd[name] = []
        for t in times:
            sc.frame_set(int(t * FPS) + 1); p = fn()
            v = world_to_camera_view(sc, cam, p); outd[name].append([round(t, 2), round(v.x, 4), round(1 - v.y, 4)])
    return outd


def run(args):
    head = build()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, int(T_END * FPS), FPS
    cam, tg = path_camera(PATH, FPS)
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 32
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, int(args.get('pct', 50))
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    tbm = bpy.data.objects['tbm']
    result['anchors'] = anchors(cam, {
        'cutterhead': lambda: head.matrix_world.translation + Vector((1.0, -4.0, 0)),
        'discs': lambda: head.matrix_world.translation + Vector((1.2, -2.5, 3.0)),
        'tail': lambda: tbm.matrix_world.translation + Vector((-80, -6.7, 2)),
        'jacks': lambda: tbm.matrix_world.translation + Vector((-8.9, -6.4, 1.0)),
        'face': lambda: tbm.matrix_world.translation + Vector((2.2, -2.0, 0)),
    }, [7.0, 11.0, 14.0, 18.0, 23.0, 26.0, 30.0, 33.0, 40.0, 45.0])
    if args.get('mode', 'preview') == 'preview':
        for t in (0.5, 4.5, 8.0, 12.0, 19.0, 23.0, 26.5, 32.0, 36.0, 45.5):
            sc.frame_set(int(t * FPS) + 1); sc.render.filepath = f'{out}/t_{t:04.1f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        video_output(sc, out + '/ch3_tbm.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
