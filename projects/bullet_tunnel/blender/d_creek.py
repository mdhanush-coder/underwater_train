# Sets A+B in ONE continuous move (lines 6-11, local t=0 = global 14.6 s): creek surface -> aerial -> dive through the water
# -> seabed cutaway with the tunnel -> ghost bullet train -> push to the tunnel mouth -> water-pressure arrows.
# Runs after skilllib.py + bt_model.py. args: mode=preview|anim
import bpy, bmesh, math, random
from mathutils import Vector, Quaternion
FPS = 30
XE = 250.0                 # block half-length along the tunnel (x)
TZ, TR, TL = -35.0, 6.55, 0.6      # tunnel axis depth, inner radius, lining thickness
TY = 2.5                   # track / train centre line, inside the cut half-pipe
T_END = 22.8
PATH = [  # (t s, camera, look-at, lens): one continuous move
    (0.0, (-96, -150, 2.8), (-10, -40, 1.2), 28),
    (4.5, (-40, -92, 3.6), (10, -20, 1.5), 28),
    (5.0, (-36, -96, 6.5), (6, -10, 2.0), 28),
    (7.6, (-10, -210, 92), (0, 60, 0), 30),
    (8.4, (0, -140, 82), (0, -60, 0), 28),
    (9.6, (0, -78, 10), (0, -40, -4), 24),
    (10.3, (0, -70, -14), (0, 0, -30), 22),
    (11.5, (-100, -52, -36), (-70, 0, -35), 22),
    (15.5, (-20, -26, -30), (200, 0, -35), 22),
    (16.9, (40, -22, -31), (200, 0, -35), 22),
    (19.4, (20, -70, -18), (0, 0, -20), 22),
    (21.4, (0, -95, -8), (0, 0, -22), 24),
    (T_END, (0, -100, -8), (0, 0, -22), 24),
]
SUBMERGE = 10.0            # front half (y<0) of the world is hidden here, masked by the murk plane


def water_mat(name, rough=0.06):
    m = mat(name, (0.012, 0.055, 0.07), rough, 0.0)
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 0.09; nz.inputs['Detail'].default_value = 8
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    mp.inputs['Location'].default_value = (0, 0, 0); mp.inputs['Location'].keyframe_insert('default_value', frame=1, index=0)
    mp.inputs['Location'].default_value = (18, 9, 0); mp.inputs['Location'].keyframe_insert('default_value', frame=int(T_END * FPS), index=0)
    mp.inputs['Location'].keyframe_insert('default_value', frame=int(T_END * FPS), index=1)
    return m


def mangrove_island(cx, cy, r, seed, mud, bark, leaf, front):
    rng = random.Random(seed)
    M = Acc(f'mud{seed}', mud); T = Acc(f'trunk{seed}', bark); Lf = Acc(f'leaf{seed}', leaf)
    M.cyl(r, 0.7, (cx, cy, -0.1), None, 40); M.cyl(r * 0.8, 0.5, (cx, cy, 0.25), None, 32)
    for _ in range(int(r * 0.8)):
        a = rng.uniform(0, math.tau); d = rng.uniform(0, r * 0.82); x, y = cx + math.cos(a) * d, cy + math.sin(a) * d
        h = rng.uniform(4.5, 8.5); tx, ty = x + rng.uniform(-0.7, 0.7), y + rng.uniform(-0.7, 0.7)
        T.beam((x, y, 0.3), (tx, ty, 0.3 + h), 0.38)
        for k in range(5):
            b = k * math.tau / 5 + rng.uniform(-0.3, 0.3)
            T.beam((x, y, 1.9), (x + math.cos(b) * 1.9, y + math.sin(b) * 1.9, 0.15), 0.13)
        for k in range(3):
            Lf.sphere(rng.uniform(1.8, 3.0), (tx + rng.uniform(-1.6, 1.6), ty + rng.uniform(-1.6, 1.6), 0.3 + h + rng.uniform(-0.2, 1.8)), (1, 1, 0.78))
    objs = [M.build(), T.build(), Lf.build(smooth=True)]
    for o in objs:
        for p in o.data.polygons: p.use_smooth = True
    front.extend(objs)


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
    front = []                                                  # objects hidden at SUBMERGE (everything in front of the cut)
    wm = water_mat('creek_water')
    Wf = Acc('water_front', wm); Wf.box((6000, 3000, 0.4), (0, -1500, -0.2)); front.append(Wf.build())
    Wb = Acc('water_back', wm); Wb.box((6000, 3000, 0.4), (0, 1500, -0.2)); Wb.build()
    mud = noisy(mat('mudflat', (0.07, 0.055, 0.04), 0.95), 1.2, 0.5, 0.5)
    bark = mat('mangrove_bark', (0.06, 0.045, 0.035), 0.9)
    leaf = noisy(mat('mangrove_leaf', (0.035, 0.1, 0.035), 0.7), 3.0, 0.45, 0.2)
    for i, (cx, cy, r) in enumerate([(-70, -60, 38), (60, -85, 46), (165, -45, 34), (-170, -110, 52), (20, -190, 60), (150, -170, 40)]):
        mangrove_island(cx, cy, r, 10 + i, mud, bark, leaf, front)
    mangrove_island(-160, 170, 60, 30, mud, bark, leaf, [])      # far bank (stays)
    mangrove_island(180, 220, 70, 31, mud, bark, leaf, [])
    # boats from the library (bobbing)
    rng = random.Random(4)
    for i, (x, y, yaw) in enumerate([(-8, -66, 0.4), (-34, -78, 2.9), (14, -52, 3.9), (-62, -112, 1.2)]):
        try:
            root = place_asset('ai3d-fishing-trawler-boat-43c178', location=(x, y, 0.0), rotation=(0, 0, yaw), size=rng.uniform(12, 15), floor=0.0)
            front.append(root)
            bpy.context.view_layer.update()
            ms = [o for o in [root] + list(root.children_recursive) if o.type == 'MESH']
            cs = [o.matrix_world @ Vector(c) for o in ms for c in o.bound_box]
            dx = max(c.x for c in cs) - min(c.x for c in cs); dy = max(c.y for c in cs) - min(c.y for c in cs); dz = max(c.z for c in cs) - min(c.z for c in cs)
            result.setdefault('boat_dims', []).append([round(dx, 1), round(dy, 1), round(dz, 1)])
            for ch in root.children_recursive: front.append(ch)
            z0 = root.location.z
            for k in range(0, int(T_END * FPS), 45):
                root.location.z = z0 + 0.14 * math.sin(k / 45 * 2.1 + i); root.rotation_euler[0] = math.radians(1.4) * math.sin(k / 45 * 1.7 + i * 2)
                root.keyframe_insert('location', index=2, frame=k + 1); root.keyframe_insert('rotation_euler', index=0, frame=k + 1)
        except Exception as e:
            result.setdefault('warn', []).append(str(e)[:120])
    # skyline on the far shore (+y), real textured towers
    for k in range(20):
        n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10][k % 10]
        try:
            place_asset(f'metropolitan-skyscraper-{n}', location=(-1000 + k * 105 + rng.uniform(-30, 30), rng.uniform(900, 1250), 0), rotation=(0, 0, rng.uniform(0, 6.28)), size=rng.uniform(120, 260), floor=0.0)
        except Exception:
            pass
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
    tr.keyframe_insert('location', frame=int(11.0 * FPS))
    tr.location.x = 330; tr.keyframe_insert('location', frame=int(17.0 * FPS))
    # pressure arrows (blue, 'sea weight') growing down onto the tunnel crown
    am = mat('arrow', (0.1, 0.45, 1.0), 0.3, 0, (0.1, 0.5, 1.0), 4.0)
    ab = am.node_tree.nodes['Principled BSDF']; ab.inputs['Alpha'].default_value = 0.8
    for i, x in enumerate(range(-66, 67, 12)):
        top = Vector((x, -0.6, -8.0)); e = bpy.data.objects.new(f'arrow{i}', None); sc.collection.objects.link(e); e.location = top
        A_ = Acc(f'arrow_mesh{i}', am); A_.cyl(0.55, 14.0, (0, 0, -7.0)); A_.cyl(0.0, 4.0, (0, 0, -16.0), None, 24, 1.4); ao = A_.build(e)
        t0 = 17.4 + i * 0.07
        e.scale = (1, 1, 0.001); e.keyframe_insert('scale', frame=int(t0 * FPS))
        e.scale = (1, 1, 1.0); e.keyframe_insert('scale', frame=int((t0 + 0.7) * FPS))
        for k, tt in enumerate((18.4, 19.0, 19.6, 20.2, 20.8, 21.4, 22.0, 22.6)):
            e.location = top + Vector((0, 0, 0.9 if k % 2 else 0.0)); e.keyframe_insert('location', frame=int(tt * FPS))
    # ---------- hide the front world at SUBMERGE, masked by the murk plane
    for o in front:
        o.hide_render = False; o.keyframe_insert('hide_render', frame=1)
        o.hide_render = True; o.keyframe_insert('hide_render', frame=int(SUBMERGE * FPS))
        for fc in fcurves_of(o):
            if fc.data_path == 'hide_render':
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    # world: dawn sky -> deep teal (mix keyed), sun
    w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    sky = nt.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'SINGLE_SCATTERING'; sky.sun_elevation = math.radians(7); sky.sun_rotation = math.radians(100); sky.sun_disc = False
    mixn = nt.nodes.new('ShaderNodeMixRGB'); mixn.inputs['Color2'].default_value = (0.012, 0.09, 0.12, 1)
    mixn.inputs['Fac'].default_value = 0.0; mixn.inputs['Fac'].keyframe_insert('default_value', frame=int(9.5 * FPS))
    mixn.inputs['Fac'].default_value = 1.0; mixn.inputs['Fac'].keyframe_insert('default_value', frame=int(10.4 * FPS))
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.3; ot = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(sky.outputs['Color'], mixn.inputs['Color1']); nt.links.new(mixn.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], ot.inputs['Surface'])
    bpy.ops.object.light_add(type='SUN', rotation=(math.radians(84), 0, math.radians(280)))
    s = bpy.context.active_object; s.data.energy = 3.2; s.data.color = (1.0, 0.72, 0.5); s.data.angle = math.radians(1.2)


def murk(cam):
    mm = mat('murk', (0.02, 0.2, 0.26), 0.5, 0, (0.02, 0.22, 0.3), 1.2)
    b = mm.node_tree.nodes['Principled BSDF']
    try: mm.surface_render_method = 'BLENDED'
    except Exception: pass
    for t, a in ((9.4, 0.0), (9.85, 0.92), (10.2, 0.92), (10.9, 0.0)):
        b.inputs['Alpha'].default_value = a; b.inputs['Alpha'].keyframe_insert('default_value', frame=int(t * FPS) + 1)
    bpy.ops.mesh.primitive_plane_add(size=1.0); p = bpy.context.active_object; p.name = 'murk'
    p.scale = (2.6, 1.5, 1); p.parent = cam; p.location = (0, 0, -0.6); p.data.materials.append(mm)
    p.hide_render = False


def run(args):
    build()
    sc = bpy.context.scene
    tot = int(T_END * FPS); sc.frame_start, sc.frame_end, sc.render.fps = 1, tot, FPS
    cam, tg = path_camera(PATH, FPS)
    murk(cam)
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 32
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 50
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    if args.get('mode', 'preview') == 'preview':
        for t in args.get('times', (0.8, 2.8, 4.3, 12.0, 12.8, 13.8, 15.0, 19.0)):
            sc.frame_set(int(t * FPS) + 1); sc.render.filepath = f'{out}/d_{t:04.1f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        video_output(sc, out + '/set_ab_lowres.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
