# Set C: launch shaft at dawn (lines 1-5, 0-14.5 s). Runs after skilllib.py + bt_model.py in one file. args: mode=preview|anim
import bpy, bmesh, math, random
from mathutils import Vector, Quaternion
FPS = 30
R, DEPTH = 15.0, 56.0
ZC = -DEPTH + 7.3          # TBM axis height (shield radius 6.7 on a 0.6 m cradle)
_OLD_SHOTS = [  # (name, t0, t1, cam_start, look_start, cam_end, look_end, lens)
    ('c1_dawn', 0.0, 2.8, (-80, -34, 2.2), (30, 60, 14), (-70, -26, 3.2), (30, 60, 17), 35),
    ('c2_aerial', 2.8, 5.3, (80, -86, 46), (0, 0, 6), (52, -58, 33), (0, 0, 4), 35),
    ('c3_edge', 5.3, 8.0, (4.0, 2.0, 24), (0, 0.5, -50), (1.5, 1.0, 7), (0, 0.5, -52), 22),
    ('c4_wall', 8.0, 10.1, (R - 3.2, -2, -3), (-R, -3, -12), (R - 3.2, -2, -45), (-R, -3, -54), 22),
    ('c5_floor', 10.1, 14.6, (11.0, -8.6, ZC + 3.0), (-1, 0, ZC), (10.6, -5.2, ZC + 1.6), (-1, 0, ZC), 19),
]


def cyl_obj(name, r, h, loc, m, verts=96, rot=(0, 0, 0), fill='NGON'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot, end_fill_type=fill)
    o = bpy.context.active_object; o.name = name
    o.data.materials.clear(); o.data.materials.append(m)
    return o


def bool_cut(target, r, z=-1.0):
    cut = cyl_obj('cut', r, 12, (0, 0, z), target.data.materials[0])
    md = target.modifiers.new('b', 'BOOLEAN'); md.object = cut; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target; bpy.ops.object.modifier_apply(modifier='b')
    bpy.data.objects.remove(cut, do_unlink=True)


def jcb(x, y, yaw):
    """Library JCB (411 meshes, no textures, no undercarriage): recolour yellow, lift 1 m, add crawler tracks under the turret."""
    root = place_asset('veh-jcb-excavator', location=(x, y, 0), rotation=(0, 0, yaw), size=8.6, floor=1.0)
    bpy.context.view_layer.update()
    ms = [o for o in [root] + list(root.children_recursive) if o.type == 'MESH']
    yel = mat('jcb_yellow', (0.72, 0.45, 0.02), 0.55, 0.1); stl = mat('jcb_steel', (0.30, 0.31, 0.33), 0.4, 0.9)
    for o in ms:
        o.data.materials.clear(); o.data.materials.append(yel if len(o.data.polygons) > 60 else stl)
    big = max(ms, key=lambda o: len(o.data.polygons))
    cs = [big.matrix_world @ Vector(c) for c in big.bound_box]
    cx = sum(c.x for c in cs) / 8; cy = sum(c.y for c in cs) / 8
    T = Acc('jcb_tracks', mat('jcb_track', (0.03, 0.03, 0.035), 0.9)); q = Quaternion((0, 0, 1), yaw)
    for sgn in (-1, 1):
        ox, oy = 1.35 * sgn * math.cos(yaw), 1.35 * sgn * math.sin(yaw)
        T.box((0.95, 4.6, 0.95), (cx + ox, cy + oy, 0.48), q)
    T.box((2.6, 3.6, 0.35), (cx, cy, 1.0), q)
    T.build()


def build():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    earth = noisy(mat('earth', (0.075, 0.058, 0.043), 0.95), 0.35, 0.45, 0.5)
    conc = noisy(mat('concrete', (0.22, 0.215, 0.20), 0.85), 3.0, 0.65, 0.35)
    wet = noisy(mat('wet_concrete', (0.12, 0.12, 0.125), 0.45), 2.2, 0.55, 0.4)
    g = cyl_obj('ground', 420, 3, (0, 0, -1.5), earth); bool_cut(g, R)
    pad = cyl_obj('pad', R + 22, 0.25, (0, 0, 0.0), conc); bool_cut(pad, R)
    Rd = Acc('road', noisy(mat('asphalt', (0.05, 0.05, 0.052), 0.8), 1.5, 0.6, 0.3))
    Rd.box((300, 9, 0.12), (0, -60, 0.02)); Rd.box((9, 200, 0.12), (-48, 0, 0.02)); Rd.build()
    Cl = Acc('collar', conc)
    for i in range(96):
        a = i * math.tau / 96
        Cl.box((1.3, 1.2, 1.4), ((R + 0.65) * math.cos(a), (R + 0.65) * math.sin(a), 0.6), Quaternion((0, 0, 1), a + math.pi / 2))
    Cl.build()
    wall = cyl_obj('wall', R, DEPTH, (0, 0, -DEPTH / 2), wet, fill='NOTHING')
    bpy.context.view_layer.objects.active = wall
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.flip_normals(); bpy.ops.object.mode_set(mode='OBJECT')
    W = Acc('wall_detail', conc); P = Acc('wall_pipes', mat('wall_pipe', (0.05, 0.055, 0.06), 0.5, 1.0))
    L_ = Acc('lamps', mat('lamp', (1, 0.8, 0.45), 0.4, 0, (1.0, 0.78, 0.4), 40.0))
    for z in range(-2, -int(DEPTH), -4):
        for i in range(96):
            a = i * math.tau / 96
            W.box((1.0, 0.45, 0.45), ((R - 0.2) * math.cos(a), (R - 0.2) * math.sin(a), z), Quaternion((0, 0, 1), a + math.pi / 2))
    for i in range(32):
        a = i * math.tau / 32
        W.box((0.25, 0.35, DEPTH), ((R - 0.15) * math.cos(a), (R - 0.15) * math.sin(a), -DEPTH / 2), Quaternion((0, 0, 1), a))
    for j in range(3):
        a = math.radians(205 + j * 11)
        P.cyl(0.34, DEPTH, ((R - 0.7) * math.cos(a), (R - 0.7) * math.sin(a), -DEPTH / 2), None, 16)
    for k, z in enumerate(range(-6, -int(DEPTH), -7)):
        for j in range(3):
            a = math.radians(30 + j * 120 + k * 19)
            L_.box((0.7, 0.25, 0.25), ((R - 0.7) * math.cos(a), (R - 0.7) * math.sin(a), z), Quaternion((0, 0, 1), a))
    W.build(); P.build(); L_.build()
    cyl_obj('floor', R, 1.4, (0, 0, -DEPTH - 0.7), conc)
    tbm, head = build_tbm('tbm', gantries=1)
    tbm.location = (-3.5, 0, ZC)
    cr = Acc('cradle', mat('cradle', (0.05, 0.05, 0.055), 0.6, 0.8))
    for x in (-12, -7, -2, 2): cr.box((1.2, 11.0, 0.9), (x, 0, -DEPTH + 0.45))
    cr.build()
    crawler_crane('crawler', (R + 22, -14, 0), yaw=math.radians(200), boom_to=(4.5, 0, 24))
    tower_crane('tcA', (-44, -34, 0), 56, 42, math.radians(35))
    tower_crane('tcB', (46, 40, 0), 52, 38, math.radians(215))
    containers(11, (-95, -30, 10, 75), 24); containers(21, (45, 115, -70, -22), 14); containers(31, (45, 105, 28, 85), 12)
    Bar = Acc('barriers', mat('barrier', (0.55, 0.53, 0.5), 0.8))
    for i in range(70):
        if i % 9 in (0, 1): continue
        a = i * math.tau / 70
        Bar.box((3.0, 0.8, 1.0), ((R + 26) * math.cos(a), (R + 26) * math.sin(a), 0.5), Quaternion((0, 0, 1), a + math.pi / 2))
    Bar.build()
    Pp = Acc('pipe_stack', mat('hdpe', (0.04, 0.04, 0.045), 0.5))
    for row, n in enumerate((6, 5, 4, 3)):
        for k in range(n):
            Pp.cyl(0.45, 12.0, (-30 + 0.95 * k + 0.47 * row, 40 + 0.0, 0.5 + 0.8 * row), Quaternion((0, 1, 0), math.pi / 2) if False else Quaternion((1, 0, 0), math.pi / 2), 16)
    Pp.build()
    for p in ((R + 6, 20), (-R - 6, -22), (24, -24), (-26, 24)): light_mast((p[0], p[1], 0))
    crew = [(R + 7, 6, 0, 2.9), (R + 8.2, 4.4, 0, 3.6), (R + 6.5, -9, 0, 1.7), (-R - 8, 8, 0, 0.4), (-R - 9.5, 6.5, 0, 5.6), (26, -3, 0, 3.1),
            (7.5, -9.8, -DEPTH, 2.2), (9.2, -8.4, -DEPTH, 3.9)]          # last two: on the shaft floor beside the cutterhead (scale)
    for i, (wx, wy, wz, yw) in enumerate(crew):
        try:
            rigged_worker(wx, wy, wz, yw, seed=i, fps=FPS, frames=int(PATH[-1][0] * FPS) + 5)
        except Exception as e_:
            result.setdefault('warn', []).append('worker %d %s' % (i, str(e_)[:80]))
    rng = random.Random(7)
    for k in range(14):                                   # Video Copilot Metropolitan towers, far + hazy
        n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10][k % 10]
        x = -260 + k * 38 + rng.uniform(-12, 12); y = rng.uniform(260, 420)
        try:
            place_asset(f'metropolitan-skyscraper-{n}', location=(x, y, 0), rotation=(0, 0, rng.uniform(0, 6.28)), size=rng.uniform(70, 150), floor=0.0)
        except Exception:
            pass
    for (x, y, a_) in ((R + 10, 14, 2.4), (-26, -21, 0.6), (28, -31, 4.0)):
        try:
            jcb(x, y, a_)
        except Exception as e_:
            result.setdefault('warn', []).append('jcb ' + str(e_)[:90])
    w = bpy.context.scene.world or bpy.data.worlds.new('W'); bpy.context.scene.world = w
    w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    sky = nt.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'SINGLE_SCATTERING'; sky.sun_elevation = math.radians(7); sky.sun_rotation = math.radians(100); sky.sun_disc = False
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.3
    ot = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(sky.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], ot.inputs['Surface'])
    bpy.ops.object.light_add(type='SUN', rotation=(math.radians(84), 0, math.radians(280)))
    s = bpy.context.active_object; s.data.energy = 3.0; s.data.color = (1.0, 0.72, 0.5); s.data.angle = math.radians(1.2)
    for z in (-12, -26, -40, -52):
        bpy.ops.object.light_add(type='POINT', location=(R - 2.0, 0, z)); l = bpy.context.active_object
        l.data.energy = 3000; l.data.color = (1.0, 0.82, 0.55)
    bpy.ops.object.light_add(type='AREA', location=(-2, -9, -DEPTH + 18)); a = bpy.context.active_object
    a.data.energy = 6000; a.data.size = 10; a.data.color = (1.0, 0.88, 0.65); a.rotation_euler = (math.radians(25), 0, 0)
    bpy.ops.object.light_add(type='SPOT', location=(-2, 0, -26), rotation=(0, 0, 0)); f = bpy.context.active_object
    f.data.energy = 60000; f.data.spot_size = math.radians(42); f.data.spot_blend = 0.9; f.data.color = (1.0, 0.9, 0.72); f.data.shadow_soft_size = 3
    return head


PATH = [  # (t s, camera, look-at, lens): ONE continuous move, no cuts
    (0.0, (-84, -42, 2.6), (18, 34, 16), 32),
    (2.8, (-48, -72, 20), (0, 0, 8), 28),
    (5.3, (34, -62, 36), (0, 0, 2), 26),
    (6.1, (11, -10, 24), (0, 0, -18), 24),
    (8.0, (6.5, -5, -14), (-1, 0, -48), 22),
    (10.1, (11.0, -8.0, -41), (0, 0, -52), 20),
    (11.6, (11.0, -8.6, ZC + 3.0), (-1, 0, ZC), 20),
    (14.6, (10.0, -5.5, ZC + 1.6), (-1, 0, ZC), 20),
    (15.6, (9.6, -5.0, ZC + 1.5), (-1, 0, ZC), 20),
]


def cameras(head):
    sc = bpy.context.scene
    tot = int(PATH[-1][0] * FPS)
    sc.frame_start, sc.frame_end, sc.render.fps = 1, tot, FPS
    cam = make_camera('Cam', focal=30, fstop=8.0, clip=(0.1, 3000.0))
    tg = bpy.data.objects.new('Cam_t', None); sc.collection.objects.link(tg)
    tc = cam.constraints.new('TRACK_TO'); tc.target = tg; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
    cam.data.dof.use_dof = False
    for t, c, l, lens in PATH:
        f = int(t * FPS) + 1
        cam.location = Vector(c); cam.keyframe_insert('location', frame=f)
        tg.location = Vector(l); tg.keyframe_insert('location', frame=f)
        cam.data.lens = lens; cam.data.keyframe_insert('lens', frame=f)
    sc.camera = cam
    for ob in (cam, tg):                                # smooth, no linear segments
        for fc in fcurves_of(ob):
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    # head: starts turning with the line "machine ... ghoomne lagti hai" (~11.4 s), eases in
    for t, ang in ((11.2, 0.0), (12.4, 6.0), (15.6, 70.0)):
        head.rotation_euler = (0, 0, math.radians(ang)); head.keyframe_insert('rotation_euler', frame=int(t * FPS) + 1)
    # dawn fade-in from black over the first 0.9 s
    sc.view_settings.exposure = -8.0; sc.view_settings.keyframe_insert('exposure', frame=1)
    sc.view_settings.exposure = 0.1; sc.view_settings.keyframe_insert('exposure', frame=28)


def run(args):
    head = build(); cameras(head)
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 32
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, int(args.get('pct', 50))
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    if args.get('mode', 'preview') == 'preview':
        for t in (3.4, 4.4, 5.4, 6.0):
            sc.frame_set(int(t * FPS)); sc.render.filepath = f'{out}/c_{t:04.1f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        video_output(sc, out + '/set_c_lowres.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
