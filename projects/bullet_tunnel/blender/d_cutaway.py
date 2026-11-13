# Sets A+B in ONE continuous move (lines 6-11, local t=0 = global 14.6 s): creek surface -> aerial -> dive through the water
# -> seabed cutaway with the tunnel -> ghost bullet train -> push to the tunnel mouth -> water-pressure arrows.
# Runs after skilllib.py + bt_model.py. args: mode=preview|anim
import bpy, bmesh, math, random
from mathutils import Vector, Quaternion
FPS = 30
XE = 250.0                 # block half-length along the tunnel (x)
TZ, TR, TL = -35.0, 6.55, 0.6      # tunnel axis depth, inner radius, lining thickness
TY = 2.5                   # track / train centre line, inside the cut half-pipe
T_END = 11.8
PATH = [  # plate 2 (cutaway), t = 0 at the end of line 8; one continuous move, camera under the waterline
    (0.0, (-140, -70, -12), (-80, 0, -34), 22),
    (1.0, (-110, -56, -30), (-70, 0, -35), 22),
    (4.5, (-20, -26, -30), (200, 0, -35), 22),
    (5.9, (40, -22, -31), (200, 0, -35), 22),
    (8.4, (20, -70, -18), (0, 0, -20), 22),
    (10.4, (0, -95, -8), (0, 0, -22), 24),
    (T_END, (0, -100, -8), (0, 0, -22), 24),
]


def ghost_train(length=100.0):
    """Lofted bullet-train body (stadium section, long nose + short tail), translucent glowing 'ghost'."""
    W, H, N = 3.4, 3.7, 28
    prof = []
    for i in range(N):
        a = i * math.tau / N
        c, s = math.cos(a), math.sin(a)
        e = 4.5; px = math.copysign(abs(c) ** (2 / e), c) * W / 2; pz = math.copysign(abs(s) ** (2 / e), s) * H / 2     # superellipse
        prof.append((px, pz))
    nose, tail = 15.0, 7.0
    # build: nose at +x tip. positions from tail to nose
    rings = []
    for k in range(8):                                  # tail taper (x from -L/2 .. -L/2+tail)
        u = k / 7; rings.append((-length / 2 + tail * u, max(0.25, (1 - (1 - u) ** 2) ** 0.5)))
    for k in range(10):                                 # body
        rings.append((-length / 2 + tail + (length - tail - nose) * k / 9, 1.0))
    for k in range(16):                                 # nose
        u = k / 15; rings.append((length / 2 - nose + nose * u, max(0.05, (1 - u ** 2.3) ** 0.5)))
    bm = bmesh.new(); rv = []
    for x, sc_ in rings:
        sz = 1.0 if sc_ >= 1.0 else sc_
        rv.append([bm.verts.new((x, px * sz, pz * (0.55 + 0.45 * sz) + (0.0 if sc_ >= 1.0 else -(1 - sz) * 0.9))) for px, pz in prof])
    for a, b in zip(rv[:-1], rv[1:]):
        for i in range(N):
            j = (i + 1) % N
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(rv[0][::-1]); bm.faces.new(rv[-1])
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces)); bm.normal_update()
    me = bpy.data.meshes.new('train'); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new('ghost_train', me); bpy.context.scene.collection.objects.link(o)
    m = mat('ghost', (0.82, 0.9, 1.0), 0.18, 0.0, (0.4, 0.75, 1.0), 2.2)
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Alpha'].default_value = 0.6
    try: m.surface_render_method = 'DITHERED'
    except Exception: pass
    me.materials.append(m)
    return o


def build():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    # ---------- the cutaway block (y >= 0)
    clay = strata(mat('clay', (0.18, 0.14, 0.11), 0.9), (0.20, 0.12, 0.06), (0.46, 0.30, 0.17), 0.35, 2.5, 0.08)
    rock = strata(mat('rock', (0.11, 0.11, 0.115), 0.85), (0.05, 0.055, 0.07), (0.17, 0.18, 0.2), 0.22, 3.0, 0.12)
    mudl = noisy(mat('seabed_mud', (0.045, 0.035, 0.025), 0.9), 1.5, 0.5, 0.15)
    A1 = Acc('seabed_mud', mudl); A1.box((2 * XE, 300, 3), (0, 150, -7.5)); A1.build()
    clay_o = Acc('clay_layer', clay); clay_o.box((2 * XE, 300, 19), (0, 150, -18.5)); co = clay_o.build()
    rock_o = Acc('rock_layer', rock); rock_o.box((2 * XE, 300, 62), (0, 150, -59)); ro = rock_o.build()
    for ob in (co, ro):
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=TR + TL, depth=2 * XE + 40, location=(0, 0, TZ), rotation=(0, math.pi / 2, 0))
        cut = bpy.context.active_object
        md = ob.modifiers.new('tun', 'BOOLEAN'); md.object = cut; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
        bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier='tun')
        bpy.data.objects.remove(cut, do_unlink=True)
    # water section on the slice face (gradient teal) + lining half-pipe + track + lights + end plug
    ws = mat('water_section', (0.02, 0.16, 0.2), 0.3); wb = ws.node_tree.nodes['Principled BSDF']
    wb.inputs['Alpha'].default_value = 0.55; wb.inputs['Emission Color'].default_value = (0.02, 0.2, 0.26, 1); wb.inputs['Emission Strength'].default_value = 0.7
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
    lm = mat('lining', (0.34, 0.335, 0.32), 0.65)
    nt = lm.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'
    wv.inputs['Scale'].default_value = 0.5; wv.inputs['Distortion'].default_value = 0.0; wv.wave_profile = 'SAW'
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.6; bp.inputs['Distance'].default_value = 0.2
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    me.materials.append(lm)
    steel = mat('rail_steel', (0.45, 0.46, 0.48), 0.3, 1.0); conc = noisy(mat('slab', (0.28, 0.275, 0.26), 0.8), 4.0, 0.6, 0.2)
    Tk = Acc('track_slab', conc); Tk.box((2 * XE, 5.4, 0.7), (0, 2.75, TZ - 3.6 - 0.35)); Tk.build()
    R_ = Acc('rails', steel)
    for s_ in (-1, 1): R_.box((2 * XE, 0.16, 0.2), (0, TY + s_ * 0.7175, TZ - 3.6 + 0.1))
    R_.build()
    Lt = Acc('tunnel_lights', mat('strip', (1, 0.9, 0.7), 0.4, 0, (1.0, 0.88, 0.65), 5.0))
    Lt.box((2 * XE, 0.35, 0.18), (0, 3.7, TZ + 4.9)); Lt.box((2 * XE, 0.35, 0.18), (0, 5.8, TZ - 0.3)); Lt.build()
    Pl = Acc('end_plug', mat('plug', (0.0, 0.0, 0.0), 1.0)); Pl.cyl(TR, 0.4, (XE - 8, 0, TZ), Quaternion((0, 1, 0), math.pi / 2), 64); Pl.build()
    for x in range(-240, 241, 60):
        bpy.ops.object.light_add(type='POINT', location=(x, 1.5, TZ + 2.0)); l = bpy.context.active_object
        l.data.energy = 2200; l.data.color = (1.0, 0.86, 0.62); l.data.shadow_soft_size = 2.0
    bpy.ops.object.light_add(type='AREA', location=(0, -60, -20), rotation=(math.radians(90), 0, 0)); f = bpy.context.active_object
    f.data.energy = 250000; f.data.size = 220; f.data.color = (0.75, 0.9, 1.0)
    # train
    tr = ghost_train(100.0); tr.location = (-260, TY, TZ - 3.6 + 0.15 + 1.85)
    tr.keyframe_insert('location', frame=1)
    tr.location.x = 330; tr.keyframe_insert('location', frame=int(6.0 * FPS))
    # pressure arrows (blue, 'sea weight') growing down onto the tunnel crown
    am = mat('arrow', (0.1, 0.45, 1.0), 0.3, 0, (0.1, 0.5, 1.0), 4.0)
    ab = am.node_tree.nodes['Principled BSDF']; ab.inputs['Alpha'].default_value = 0.8
    for i, x in enumerate(range(-66, 67, 12)):
        top = Vector((x, -0.6, -8.0)); e = bpy.data.objects.new(f'arrow{i}', None); sc.collection.objects.link(e); e.location = top
        A_ = Acc(f'arrow_mesh{i}', am); A_.cyl(0.55, 14.0, (0, 0, -7.0)); A_.cyl(0.0, 4.0, (0, 0, -16.0), None, 24, 1.4); ao = A_.build(e)
        t0 = 6.4 + i * 0.07
        e.scale = (1, 1, 0.001); e.keyframe_insert('scale', frame=int(t0 * FPS))
        e.scale = (1, 1, 1.0); e.keyframe_insert('scale', frame=int((t0 + 0.7) * FPS))
        for k, tt in enumerate((7.4, 8.0, 8.6, 9.2, 9.8, 10.4, 11.0, 11.6)):
            e.location = top + Vector((0, 0, 0.9 if k % 2 else 0.0)); e.keyframe_insert('location', frame=int(tt * FPS))
    w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Color'].default_value = (0.012, 0.09, 0.12, 1); bg.inputs['Strength'].default_value = 0.8
    ot = nt.nodes.new('ShaderNodeOutputWorld'); nt.links.new(bg.outputs['Background'], ot.inputs['Surface'])


def run(args):
    build()
    sc = bpy.context.scene
    tot = int(T_END * FPS); sc.frame_start, sc.frame_end, sc.render.fps = 1, tot, FPS
    cam, tg = path_camera(PATH, FPS)
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 32
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 50
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    if args.get('mode', 'preview') == 'preview':
        for t in args.get('times', (0.4, 1.6, 2.6, 3.6, 5.2, 7.2, 9.4, 11.2)):
            sc.frame_set(int(t * FPS) + 1); sc.render.filepath = f'{out}/d_{t:04.1f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        video_output(sc, out + '/set_cutaway.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
