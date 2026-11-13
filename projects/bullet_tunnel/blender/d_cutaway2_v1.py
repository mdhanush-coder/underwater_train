# Plate 2 (cutaway), v2: distinct soil layers, tunnel half-pipe, RIGGED articulated ghost train (armature: root + 4 car bones,
# meshes skinned by vertex groups, root drives travel, car bones add lag/sway), pressure arrows, camera tracking square-on.
# Runs after skilllib.py + bt_model.py. args: mode=preview|anim. t=0 is the end of narration line 8.
import bpy, bmesh, math
from mathutils import Vector, Quaternion
FPS = 30
XE = 250.0
TZ, TR, TL = -35.0, 6.55, 0.6
TY = 2.5
T_END = 11.8
FLOOR = TZ - 3.6                      # track floor level
ZC = FLOOR + 0.15 + 1.85              # train centre height
PATH = [
    (0.0, (-200, -70, -15), (-160, 0, -34), 24),
    (0.8, (-165, -27, -34), (-150, 0, -35), 24),
    (5.0, (175, -27, -34), (190, 0, -35), 24),
    (5.9, (205, -24, -34), (320, 0, -35), 22),
    (8.4, (60, -80, -20), (0, 0, -20), 22),
    (10.4, (0, -110, -8), (0, 0, -22), 24),
    (T_END, (0, -115, -8), (0, 0, -22), 24),
]
CAR_X = [-39.0, -13.0, 13.0, 39.0]    # car centres relative to the train centre; car length 25 m, 0.9 m gaps
CAR_L = 24.8


def car_mesh(name, cx, kind):
    """One car lofted from superellipse sections; kind: 'lead' (long nose at +x), 'tail' (taper at -x), 'mid'."""
    W, H, N = 3.4, 3.7, 28
    prof = []
    for i in range(N):
        a = i * math.tau / N; c, s = math.cos(a), math.sin(a); e = 4.5
        prof.append((math.copysign(abs(c) ** (2 / e), c) * W / 2, math.copysign(abs(s) ** (2 / e), s) * H / 2))
    L = CAR_L; rings = []                                # (x relative to car centre, scale)
    n0, n1 = (0.0, 0.0)
    if kind == 'lead': n1 = 13.0
    if kind == 'tail': n0 = 7.0
    for k in range(7 if n0 else 1):
        u = k / 6.0 if n0 else 1.0; rings.append((-L / 2 + n0 * u, max(0.3, (1 - (1 - u) ** 2) ** 0.5) if n0 else 1.0))
    nbody = 6
    for k in range(nbody): rings.append((-L / 2 + n0 + (L - n0 - n1) * (k + 1) / nbody, 1.0))
    if n1:
        for k in range(14):
            u = (k + 1) / 14.0; rings.append((L / 2 - n1 + n1 * u, max(0.06, (1 - u ** 2.3) ** 0.5)))
    bm = bmesh.new(); rv = []
    for x, sc_ in rings:
        sz = min(1.0, sc_)
        rv.append([bm.verts.new((cx + x, px * sz, pz * (0.55 + 0.45 * sz) + (0 if sz >= 1.0 else -(1 - sz) * 0.9))) for px, pz in prof])
    for a, b in zip(rv[:-1], rv[1:]):
        for i in range(N): bm.faces.new((a[i], a[(i + 1) % N], b[(i + 1) % N], b[i]))
    bm.faces.new(rv[0][::-1]); bm.faces.new(rv[-1])
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    return o


def skin(obj, arm, bone):
    obj.parent = arm
    vg = obj.vertex_groups.new(name=bone); vg.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
    md = obj.modifiers.new('Armature', 'ARMATURE'); md.object = arm


def rigged_train():
    sc = bpy.context.scene
    bpy.ops.object.armature_add(location=(0, TY, ZC)); arm = bpy.context.active_object; arm.name = 'train_rig'
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones; r = eb[0]; r.name = 'root'; r.head = (0, 0, 0); r.tail = (0, 1, 0)
    for i, cx in enumerate(CAR_X):
        b = eb.new(f'car{i}'); b.head = (cx, 0, 0); b.tail = (cx, 1, 0); b.parent = r
    bpy.ops.object.mode_set(mode='OBJECT')
    ghost = mat('ghost', (0.55, 0.66, 0.8), 0.22, 0.0, (0.35, 0.6, 0.9), 0.45)
    ghost.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.5
    try: ghost.surface_render_method = 'DITHERED'
    except Exception: pass
    win = mat('train_windows', (1.0, 0.9, 0.7), 0.3, 0.0, (1.0, 0.85, 0.6), 1.4)
    stripe = mat('train_stripe', (0.1, 0.6, 1.0), 0.3, 0.0, (0.1, 0.6, 1.0), 1.6)
    dark = mat('gangway', (0.02, 0.02, 0.025), 0.7)
    for i, cx in enumerate(CAR_X):
        kind = 'lead' if i == 3 else 'tail' if i == 0 else 'mid'
        car = car_mesh(f'car{i}_body', cx, kind); car.data.materials.append(ghost); skin(car, arm, f'car{i}')
        W_ = Acc(f'car{i}_windows', win); S_ = Acc(f'car{i}_stripe', stripe)
        x0, x1 = cx - CAR_L / 2 + (8 if kind == 'tail' else 2.5), cx + CAR_L / 2 - (14 if kind == 'lead' else 2.5)
        for k in range(int((x1 - x0) // 2.6)):
            xx = x0 + 1.3 + k * 2.6; W_.box((1.7, 0.06, 0.8), (xx, -1.74, 0.55)); W_.box((1.7, 0.06, 0.8), (xx, 1.74, 0.55))
        S_.box((x1 - x0, 0.06, 0.28), ((x0 + x1) / 2, -1.75, -0.3)); S_.box((x1 - x0, 0.06, 0.28), ((x0 + x1) / 2, 1.75, -0.3))
        for ob_, nm in ((W_.build(), 'w'), (S_.build(), 's')): skin(ob_, arm, f'car{i}')
        if i < 3:
            G = Acc(f'gang{i}', dark); G.box((1.1, 3.0, 3.1), (cx + CAR_L / 2 + 0.45, 0, 0)); skin(G.build(), arm, f'car{i}')
    # animation: root travels, car bones lag and sway (articulated feel); Bezier everywhere
    pb = arm.pose.bones
    for b in pb: b.rotation_mode = 'XYZ'
    for t, x in ((0.0, -260.0), (0.8, -200.0), (5.0, 140.0), (6.6, 300.0)):
        pb['root'].location = (x, 0, 0); pb['root'].keyframe_insert('location', frame=int(t * FPS) + 1)
    for i in range(4):
        for k in range(0, int(T_END * FPS), 6):
            ph = k / 6.0 * 0.9 + i * 1.3
            pb[f'car{i}'].location = (0, 0, 0.012 * math.sin(ph * 1.7)); pb[f'car{i}'].rotation_euler = (0.0016 * math.sin(ph), 0, 0.0022 * math.sin(ph * 0.8 + i))
            pb[f'car{i}'].keyframe_insert('location', index=2, frame=k + 1); pb[f'car{i}'].keyframe_insert('rotation_euler', frame=k + 1)
    for fc in fcurves_of(arm):
        for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'
    for ob in [o for o in bpy.data.objects if o.parent == arm]:      # the train is swallowed by the dark end cap (nose reaches x~240 at ~5.5 s)
        ob.hide_render = False; ob.keyframe_insert('hide_render', frame=1)
        ob.hide_render = True; ob.keyframe_insert('hide_render', frame=int(5.55 * FPS))
        for fc in fcurves_of(ob):
            if fc.data_path == 'hide_render':
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    return arm


def box_layer(name, mat_, z0, z1):
    o = Acc(name, mat_); o.box((2 * XE, 300, z0 - z1), (0, 150, (z0 + z1) / 2)); return o.build()


def build():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    L = [('seabed_mud', (0.05, 0.04, 0.03), -6, -9, False), ('soft_clay', (0.34, 0.22, 0.12), -9, -20, False), ('stiff_clay', (0.52, 0.36, 0.2), -20, -30, True),
         ('weathered_rock', (0.24, 0.22, 0.2), -30, -46, True), ('basalt', (0.09, 0.1, 0.13), -46, -90, False)]
    seam = Acc('layer_seams', mat('seam', (0.03, 0.03, 0.035), 0.9))
    for nm, c, z0, z1, cut_ in L:
        ob = box_layer(nm, noisy(mat(nm, c, 0.9), 2.2, 0.72, 0.18), z0, z1)
        if cut_:
            bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=TR + TL, depth=2 * XE + 40, location=(0, 0, TZ), rotation=(0, math.pi / 2, 0))
            cut = bpy.context.active_object
            md = ob.modifiers.new('tun', 'BOOLEAN'); md.object = cut; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
            bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier='tun'); bpy.data.objects.remove(cut, do_unlink=True)
        seam.box((2 * XE, 0.12, 0.35), (0, -0.04, z0))
    seam.build()
    ws = mat('water_section', (0.02, 0.18, 0.24), 0.3, 0.0, (0.03, 0.22, 0.3), 0.8); ws.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.6
    try: ws.surface_render_method = 'DITHERED'
    except Exception: pass
    S = Acc('water_section', ws); S.box((2 * XE, 0.1, 6), (0, -0.05, -3)); S.build()
    bm = bmesh.new()
    res = bmesh.ops.create_cone(bm, cap_ends=False, segments=96, radius1=TR + TL * 0.5, radius2=TR + TL * 0.5, depth=2 * XE)
    bmesh.ops.transform(bm, matrix=Quaternion((0, 1, 0), math.pi / 2).to_matrix().to_4x4(), verts=res['verts'])
    bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True)
    me = bpy.data.meshes.new('lining'); bm.to_mesh(me); bm.free()
    lin = bpy.data.objects.new('lining', me); sc.collection.objects.link(lin); lin.location = (0, 0, TZ)
    for p in me.polygons: p.use_smooth = True
    sol = lin.modifiers.new('s', 'SOLIDIFY'); sol.thickness = TL; sol.offset = 0
    lm = mat('lining', (0.42, 0.41, 0.39), 0.6); nt = lm.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'
    wv.inputs['Scale'].default_value = 0.5; wv.inputs['Distortion'].default_value = 0.0; wv.wave_profile = 'SAW'
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.5; bp.inputs['Distance'].default_value = 0.15
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    me.materials.append(lm)
    steel = mat('rail_steel', (0.5, 0.5, 0.52), 0.3, 1.0); conc = noisy(mat('slab', (0.3, 0.29, 0.27), 0.8), 4.0, 0.6, 0.2)
    Tk = Acc('track_slab', conc); Tk.box((2 * XE, 5.4, 0.7), (0, 2.75, FLOOR - 0.35)); Tk.build()
    R_ = Acc('rails', steel)
    for s_ in (-1, 1): R_.box((2 * XE, 0.16, 0.2), (0, TY + s_ * 0.7175, FLOOR + 0.1))
    R_.build()
    Lt = Acc('tunnel_lights', mat('strip', (1, 0.9, 0.7), 0.4, 0, (1.0, 0.88, 0.65), 3.0))
    Lt.box((2 * XE, 0.35, 0.18), (0, 3.7, TZ + 4.9)); Lt.box((2 * XE, 0.35, 0.18), (0, 5.8, TZ - 0.3)); Lt.build()
    pm = bpy.data.meshes.new('end_plug'); pbm = bmesh.new()
    pv = [pbm.verts.new((XE - 8, TR * math.sin(math.pi * k / 48), TZ + TR * math.cos(math.pi * k / 48))) for k in range(49)]
    pbm.faces.new(pv); pbm.to_mesh(pm); pbm.free(); pm.materials.append(mat('plug', (0.0, 0.0, 0.0), 1.0))
    po = bpy.data.objects.new('end_plug', pm); sc.collection.objects.link(po)
    for x in range(-240, 241, 40):
        bpy.ops.object.light_add(type='POINT', location=(x, 1.8, TZ + 2.5)); l = bpy.context.active_object
        l.data.energy = 1100; l.data.color = (1.0, 0.86, 0.62); l.data.shadow_soft_size = 2.5
    bpy.ops.object.light_add(type='AREA', location=(0, -80, -25), rotation=(math.radians(90), 0, 0)); f = bpy.context.active_object
    f.data.energy = 160000; f.data.size = 260; f.data.color = (0.8, 0.92, 1.0)
    rigged_train()
    am = mat('arrow', (0.1, 0.45, 1.0), 0.3, 0, (0.1, 0.5, 1.0), 3.5); am.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.85
    for i, x in enumerate(range(-66, 67, 12)):
        top = Vector((x, -0.6, -8.0)); e = bpy.data.objects.new(f'arrow{i}', None); sc.collection.objects.link(e); e.location = top
        A_ = Acc(f'arrow_mesh{i}', am); A_.cyl(0.55, 14.0, (0, 0, -7.0)); A_.cyl(0.0, 4.0, (0, 0, -16.0), None, 24, 1.4); A_.build(e)
        t0 = 6.4 + i * 0.07
        e.scale = (1, 1, 0.001); e.keyframe_insert('scale', frame=int(t0 * FPS))
        e.scale = (1, 1, 1.0); e.keyframe_insert('scale', frame=int((t0 + 0.7) * FPS))
        for k, tt in enumerate((7.4, 8.0, 8.6, 9.2, 9.8, 10.4, 11.0, 11.6)):
            e.location = top + Vector((0, 0, 0.9 if k % 2 else 0.0)); e.keyframe_insert('location', frame=int(tt * FPS))
    w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    tcw = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = -0.6; mr.inputs['From Max'].default_value = 0.7
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.004, 0.03, 0.045, 1); cr.color_ramp.elements[1].color = (0.03, 0.2, 0.26, 1)
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.9; ot = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(tcw.outputs['Generated'], sep.inputs['Vector']); nt.links.new(sep.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], ot.inputs['Surface'])


def run(args):
    build()
    sc = bpy.context.scene
    tot = int(T_END * FPS); sc.frame_start, sc.frame_end, sc.render.fps = 1, tot, FPS
    cam, tg = path_camera(PATH, FPS)
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 32
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, int(args.get('pct', 50))
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    if args.get('mode', 'preview') == 'preview':
        for t in (0.3, 1.5, 3.0, 4.6, 5.6, 7.0, 9.4, 11.2):
            sc.frame_set(int(t * FPS) + 1); sc.render.filepath = f'{out}/d_{t:04.1f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        video_output(sc, out + '/set_cutaway.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
