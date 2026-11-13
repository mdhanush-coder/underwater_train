# Chapter 5 plate "Building the ring" (49.09 s, chapter t0 = global 184.818). Runs after skilllib.py + bt_model.py.
# Inside the tail shield: ring erector (rotating ring frame, telescopic arm, vacuum/mechanical gripper), segment feeder,
# 9 + 1 key ring (13.1 m OD, 0.5 m thick, 2 m wide), thrust jacks, advance, cutaway to the annular grout gap, water beads,
# time-lapse of rings, then (black dip 42.30-42.60) a daylight casting yard. One camera. args: mode=preview|anim, pct.
# Animation is a pure function state(t): preview sets it per still, anim keys it every frame (sparse, LINEAR).
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Quaternion
FPS = 30
T_END = 49.09
R_IN, R_OUT, BORE, SH_IN, SH_OUT = 6.05, 6.55, 6.82, 6.62, 6.80
TH = [0, 38, -38, 76, -76, 114, -114, 152, -152, 180]          # placement order: invert, alternate sides, key at the crown
SPAN = [38.0] * 9 + [18.0]
EX_PICK, EX_PLACE, EX_KEY = 1.8, 4.0, 5.2                      # erector axial (machine frame); gripper x = m + ex - 3
RG_F, RG_L = 5.25, 4.45                                         # gripper radius: on the feeder / lifted
Y0 = 3000.0                                                     # casting yard origin (far from the tunnel)
J0, J1, J2, J3 = 42.30, 42.3333, 42.5667, 42.60                # camera relocation inside the black dip
rad = math.radians
XQ = zrot_to((1, 0, 0)); YQ = zrot_to((0, 1, 0))
VR = random.Random(5)                                           # per-segment concrete variant picker

PATH = [
    (0.0, (-11.0, -1.6, -1.2), (6, 0.4, -0.2), 22),
    (3.2, (-10.2, -1.6, -1.15), (6, 0.4, -0.2), 22),
    (7.2, (-7.4, -2.3, -1.7), (3, 0, -1.4), 22),
    (8.4, (-7.5, -3.6, -1.8), (-0.8, 0, -4.3), 26),
    (10.3, (-7.0, -3.4, -1.8), (0.0, 0, -4.2), 26),
    (11.0, (-4.6, 1.4, -1.0), (1, -1.8, -4.0), 24),
    (14.1, (-4.3, 1.6, -1.6), (1, -2.5, -3.8), 24),
    (14.7, (-3.9, 1.8, -2.5), (1.0, -2.9, -3.7), 24),
    (16.9, (-3.8, 1.85, -2.55), (1.0, -2.9, -3.7), 24),
    (18.6, (-9.0, -0.6, -0.6), (2, 0, 0), 16),
    (21.6, (-8.4, -0.6, -0.6), (2, 0, 0.3), 16),
    (23.4, (-6.6, -1.0, -1.5), (2, 0, 2.2), 18),
    (26.7, (-6.1, -1.0, -1.6), (2, 0, 2.4), 18),
    (27.7, (-0.9, -2.3, -1.4), (2.8, 4.8, -1.0), 24),
    (29.5, (-0.8, -2.2, -1.35), (2.7, 4.7, -1.0), 24),
    (31.6, (-7.0, -19.0, 2.5), (3, 0, 0.5), 22),
    (33.6, (-6.6, -18.6, 2.3), (3.2, 0, 0.5), 22),
    (34.6, (0.0, -2.6, 7.0), (-0.3, 0.3, 6.68), 35),
    (36.2, (-0.1, -2.65, 7.0), (-0.4, 0.3, 6.68), 35),
    (37.0, (-2.0, -2.8, 7.3), (-2.6, 0.3, 6.95), 35),
    (39.2, (-2.15, -2.9, 7.3), (-2.6, 0.3, 6.95), 35),
    (J0, (-10, -70, 14), (14, 0, 0), 26),
    (J1, (-10, -70, 14), (14, 0, 0), 26),
    (J2, (-14, Y0 - 38, 15), (60, Y0 + 4, 1), 26),
    (J3, (-14, Y0 - 38, 15), (60, Y0 + 4, 1), 26),
    (T_END, (-5, Y0 - 35, 13.5), (68, Y0 + 6, 1), 26),
]
G = {}                                                          # scene handles
TX = [30.2]                                                     # camera passes through the near lining (set from the path)


def sm(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


def win(t, a, b):
    return sm((t - a) / (b - a))


# ---------------------------------------------------------------- geometry
def sector(bm, r0, r1, x0, x1, a0, a1, n, M=None, mi=0):
    """Closed solid annular sector around the X axis; angle a (deg) puts a point at (x, r sin a, -r cos a)."""
    vs = []
    for i in range(n + 1):
        a = rad(a0 + (a1 - a0) * i / n); s, c = math.sin(a), -math.cos(a)
        vs.append([[bm.verts.new((x, r * s, r * c)) for r in (r0, r1)] for x in (x0, x1)])
    F = []
    q = lambda *v: F.append(bm.faces.new(v))
    for i in range(n):
        A, B = vs[i], vs[i + 1]
        q(A[0][0], B[0][0], B[1][0], A[1][0]); q(A[0][1], A[1][1], B[1][1], B[0][1])
        q(A[0][0], A[0][1], B[0][1], B[0][0]); q(A[1][0], B[1][0], B[1][1], A[1][1])
    q(vs[0][0][0], vs[0][1][0], vs[0][1][1], vs[0][0][1]); q(vs[n][0][0], vs[n][0][1], vs[n][1][1], vs[n][1][0])
    if M is not None:
        bmesh.ops.transform(bm, matrix=M, verts=[v for row in vs for p in row for v in p])
    for f in F: f.material_index = mi
    bmesh.ops.recalc_face_normals(bm, faces=F)
    return F


def P(x, r, a):
    return Vector((x, r * math.sin(rad(a)), -r * math.cos(rad(a))))


def mesh_obj(name, bm, mats, parent=None):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    if parent is not None: o.parent = parent
    return o


def split180(a0, a1):
    cuts = [k * 180.0 for k in range(-3, 4) if a0 < k * 180.0 < a1]
    b = [a0] + cuts + [a1]
    return list(zip(b[:-1], b[1:]))


def side_of(a):
    return 'far' if math.sin(rad(a)) > 0 else 'near'


def seg_obj(name, span, mats, clip=None):
    """Hero-grade segment (local: centred on the invert, x in [-1, 1]): concrete, EPDM gasket on all four joint faces,
    bolt pockets on the intrados, grout/lifting socket at the centre. clip=(lo, hi) keeps a part (cutaway twin)."""
    bm = bmesh.new(); h = span / 2
    lo, hi = (-h, h) if clip is None else (max(-h, clip[0]), min(h, clip[1]))
    inside = lambda a: lo <= a <= hi
    n = max(4, int((hi - lo) / 1.6))
    sector(bm, R_IN, R_OUT, -0.994, 0.994, lo, hi, n)
    for sx in (-1, 1):                                                     # circumferential gaskets
        xa, xb = sorted((sx * 0.990, sx * 1.004))
        sector(bm, R_OUT - 0.12, R_OUT - 0.05, xa, xb, max(lo, -h + 0.3), min(hi, h - 0.3), n, mi=1)
    for e, sg in ((-h, -1), (h, 1)):                                       # longitudinal gaskets (real ends only)
        if inside(e):
            a0, a1 = sorted((e - sg * 0.05, e + sg * 0.08))
            sector(bm, R_OUT - 0.12, R_OUT - 0.05, -0.97, 0.97, a0, a1, 1, mi=1)
    for x, a in ((0.86, -h * 0.5), (-0.86, h * 0.5)):                     # bolt pockets on the ring joints (shallow recess)
        if inside(a - 0.7) and inside(a + 0.7):
            sector(bm, R_IN - 0.002, R_IN + 0.02, x - 0.08, x + 0.08, a - 0.7, a + 0.7, 1, mi=2)
    if inside(-1.2) and inside(1.2):                                       # grout hole / lifting socket
        sector(bm, R_IN - 0.006, R_IN + 0.02, -0.11, 0.11, -1.05, 1.05, 2, mi=2)
        sector(bm, R_IN - 0.012, R_IN + 0.02, -0.065, 0.065, -0.62, 0.62, 2, mi=3)
    o = mesh_obj(name, bm, mats)
    bv = o.modifiers.new('bevel', 'BEVEL'); bv.width = 0.012; bv.segments = 2; bv.limit_method = 'ANGLE'; bv.angle_limit = rad(30)
    return o


def ring_into(bms, x0, x1, off, sides=('far', 'near')):
    """Static ring (10 pieces, 1 cm joints) into bms[side] (materials: 0-2 concrete variants, 3 gasket, 4 pocket, 5 plug)."""
    for c, s in zip(TH, SPAN):
        c = c + off; h = s / 2; v = VR.randrange(3)
        for a0, a1 in split180(c - h + 0.06, c + h - 0.06):
            sd = side_of((a0 + a1) / 2)
            if sd in sides:
                sector(bms[sd], R_IN, R_OUT, x0 + 0.006, x1 - 0.006, a0, a1, max(2, int((a1 - a0) / 2.4)), mi=v)
        for x, a in ((0.86, c - h * 0.5), (-0.86, c + h * 0.5)):
            sd = side_of(a)
            if sd in sides and side_of(a - 1) == sd and side_of(a + 1) == sd:
                xm = (x0 + x1) / 2 + x
                sector(bms[sd], R_IN - 0.002, R_IN + 0.02, xm - 0.08, xm + 0.08, a - 0.7, a + 0.7, 1, mi=4)
        sd = side_of(c)
        if sd in sides and side_of(c - 1) == sd and side_of(c + 1) == sd:
            xm = (x0 + x1) / 2
            sector(bms[sd], R_IN - 0.006, R_IN + 0.02, xm - 0.065, xm + 0.065, c - 0.62, c + 0.62, 2, mi=5)


def world_coords(m):
    """Relink every Object texture coordinate to world Position (moving plug + static ground share one texture)."""
    nt = m.node_tree; geo = nt.nodes.new('ShaderNodeNewGeometry')
    for l in list(nt.links):
        if l.from_node.type == 'TEX_COORD':
            to = l.to_socket; nt.links.remove(l); nt.links.new(geo.outputs['Position'], to)
    return m


def build_tunnel():
    sc = bpy.context.scene
    conc_new = noisy(mat('seg_new', (0.56, 0.55, 0.52), 0.82, 0, (1.0, 0.85, 0.6), 0.0), 14.0, 0.72, 0.35)
    conc_old = [noisy(mat(f'lining_concrete{i}', c, 0.85), 11.0, 0.7, 0.35) for i, c in enumerate(((0.47, 0.46, 0.43), (0.50, 0.48, 0.44), (0.44, 0.435, 0.415)))]
    gasket = mat('epdm_gasket', (0.015, 0.015, 0.016), 0.55)
    pocket = mat('bolt_pocket', (0.30, 0.29, 0.27), 0.9)
    plug = mat('grout_plug', (0.16, 0.16, 0.16), 0.5)
    steel_in = noisy(mat('shield_inner', (0.30, 0.32, 0.33), 0.45, 0.6), 3.0, 0.65, 0.12)
    dark = noisy(mat('machine_dark2', (0.10, 0.105, 0.11), 0.5, 0.6), 6.0, 0.6, 0.1)
    yel = noisy(mat('erector_yellow', (0.75, 0.55, 0.08), 0.55, 0.0), 7.0, 0.55, 0.12)   # matte safety-yellow paint, worn
    jcyl = noisy(mat('jack_cylinder', (0.11, 0.115, 0.12), 0.45, 0.5), 5.0, 0.7, 0.08)
    chrome = mat('chrome_rod', (0.78, 0.78, 0.8), 0.15, 1.0)
    rubber = mat('rubber_pad', (0.02, 0.02, 0.02), 0.7)
    bulk_m = noisy(mat('bulkhead_paint', (0.45, 0.46, 0.45), 0.5, 0.4), 4.0, 0.7, 0.1)
    lampm = mat('work_lamp', (1, 0.9, 0.75), 0.4, 0, (1.0, 0.86, 0.62), 4.0)
    NEAR = []
    # ---- old rings behind the tail (45 rings, keys staggered), near/far halves for the cutaway
    bms = {'far': bmesh.new(), 'near': bmesh.new()}
    for j in range(45):
        ring_into(bms, -2.0 * (j + 1), -2.0 * j, 19.0 if j % 2 == 0 else 0.0)
    mesh_obj('lining_far', bms['far'], conc_old + [gasket, pocket, plug])
    NEAR.append(mesh_obj('lining_near', bms['near'], conc_old + [gasket, pocket, plug]))
    # ---- the new ring: 10 animated segments + far-half twins of the two that straddle the cut
    vr = random.Random(3); G['seg_mats'] = [conc_new]
    for o in range(1, 10):
        c = 0.53 + vr.uniform(-0.03, 0.03); G['seg_mats'].append(noisy(mat(f'seg_new{o}', (c + 0.01, c, c - 0.035), 0.82, 0, (1.0, 0.85, 0.6), 0.0), 14.0, 0.72, 0.35))
    G['seg'] = [seg_obj(f'seg_{o}', SPAN[o], [G['seg_mats'][o], gasket, pocket, plug]) for o in range(10)]
    t0 = seg_obj('seg_0_far', SPAN[0], [conc_new, gasket, pocket, plug], clip=(0.0, 99))
    t0.location = (1, 0, 0)
    t9 = seg_obj('seg_9_far', SPAN[9], [G['seg_mats'][9], gasket, pocket, plug], clip=(-99, 0.0))
    t9.location = (1, 0, 0); t9.rotation_euler = (rad(180), 0, 0)
    G['twins'] = [t0, t9]
    # ---- time-lapse rings k = 1..15 (far half only, appear as the tail passes)
    G['tl'] = []
    for k in range(1, 16):
        b = {'far': bmesh.new()}; ring_into(b, 2.0 * k, 2.0 * k + 2, 19.0 if k % 2 else 0.0, sides=('far',))
        G['tl'].append(mesh_obj(f'tl_ring_{k}', b['far'], conc_old + [gasket, pocket, plug]))
    # ---- machine (moves +x by m): tail shield, tail seal, thrust ring, stiffener, bulkhead, jacks, erector beam, lights
    mach = empty('machine'); G['mach'] = mach
    for sd, (a0, a1) in (('far', (0, 180)), ('near', (-180, 0))):
        b = bmesh.new()
        sector(b, SH_IN, SH_OUT, -1.0, 11.4, a0, a1, 64)
        sector(b, 6.2, SH_IN, 7.6, 7.8, a0, a1, 64)                         # stiffener ring
        sector(b, 5.85, SH_IN, 6.6, 6.9, a0, a1, 64)                        # thrust ring (jack heads)
        o1 = mesh_obj('shield_' + sd, b, [steel_in], mach)
        b = bmesh.new(); sector(b, 6.556, 6.615, -1.0, -0.2, a0, a1, 64)   # tail brush seal
        o2 = mesh_obj('tail_seal_' + sd, b, [rubber], mach)
        b = bmesh.new(); sector(b, 0.02, SH_IN, 9.0, 9.4, a0, a1, 64)      # pressure bulkhead
        o3 = mesh_obj('bulkhead_' + sd, b, [bulk_m], mach)
        if sd == 'near': NEAR += [o1, o2, o3]
    BK = Acc('bulkhead_kit', dark); LP = Acc('bulkhead_lamps', lampm)
    BK.cyl(1.0, 2.2, (7.9, 3.0, 2.2), XQ, 32); BK.cyl(1.05, 0.15, (6.8, 3.0, 2.2), XQ, 32)   # man-lock
    for y in (-4.2, 4.2): BK.cyl(0.3, 4.5, (6.75, y, -3.2), XQ, 20)                        # slurry lines
    for a in (60, 120, 200, 250, 300):
        p = P(8.85, 4.2, a); BK.box((0.3, 0.7, 0.9), p)                                     # control boxes
    for a in (35, 90, 145, 215, 270, 325):
        p = P(8.96, 5.3, a); LP.box((0.06, 0.8, 0.3), p, Quaternion((1, 0, 0), rad(a)))
    BK.box((8.0, 1.0, 1.0), (5.0, 0, 0))                                                    # erector support beam
    BK.build(mach); LP.build(mach)
    for sd in ('far', 'near'):                                                              # thrust jacks (14 pairs)
        J = Acc('jack_body_' + sd, jcyl); R = Acc('jack_rods_' + sd, chrome); S = Acc('jack_shoes_' + sd, dark)
        for p in range(14):
            a = (p + 0.5) * 360 / 14
            if side_of(a) != sd: continue
            for d in (-2.6, 2.6):
                q = P(0, 6.25, a + d)
                J.cyl(0.16, 3.0, (5.1, q.y, q.z), XQ, 14); R.cyl(0.085, 1.0, (0.5, q.y, q.z), XQ, 12)
            q = P(0.125, 6.3, a); S.box((0.25, 0.8, 0.42), q, Quaternion((1, 0, 0), rad(a)))
        oj = J.build(mach, True); orod = R.build(None, True); osh = S.build()
        G['rods_' + sd] = orod; G['shoes_' + sd] = osh
        if sd == 'near': NEAR += [oj, orod, osh]
    # ---- erector (rotating ring frame + telescopic arm + gripper), child of the machine
    ere = empty('erector', (EX_PLACE, 0, 0), mach); G['ere'] = ere
    Y = Acc('erector_frame', yel); K = Acc('erector_dark', dark)
    sector(Y.bm, 2.7, 3.3, -0.3, 0.3, -180, 180, 72)
    for i in range(72):
        a = i * 5.0; K.box((0.4, 0.12, 0.12), P(0, 3.36, a), Quaternion((1, 0, 0), rad(a)))
    sector(K.bm, 0.75, 1.05, -0.5, 0.5, -180, 180, 32)
    for a in (45, 135, 225, 315): Y.beam(P(0, 1.05, a), P(0, 2.7, a), 0.3)
    for sy in (-0.55, 0.55):
        Y.box((3.6, 0.35, 0.4), (-1.5, sy, -2.95)); Y.box((0.45, 0.45, 2.3), (-3, sy, -2.75))
        Y.beam((0, sy, -2.3), (-3, sy, -1.7), 0.18)
    Y.box((0.4, 1.55, 0.4), (-3, 0, -1.6))
    K.box((1.0, 2.2, 1.2), (0, 0, 2.3)); K.box((0.6, 0.6, 0.6), P(0.45, 3.0, 90)); K.box((0.6, 0.6, 0.6), P(0.45, 3.0, -90))
    Y.build(ere); K.build(ere)
    tele = empty('erector_tele', (0, 0, 0), ere); G['tele'] = tele
    T = Acc('tele_rods', chrome)
    for sy in (-0.55, 0.55): T.box((0.28, 0.28, 2.85), (-3, sy, -3.025))
    T.build(tele)
    Mg = Matrix.Translation((-3, 0, R_IN - 4.6))
    b = bmesh.new(); sector(b, R_IN - 0.2, R_IN - 0.05, -0.75, 0.75, -9, 9, 12, Mg); mesh_obj('gripper_plate', b, [yel], tele)
    b = bmesh.new(); sector(b, R_IN - 0.05, R_IN - 0.005, -0.65, 0.65, -8, 8, 12, Mg); mesh_obj('vacuum_pad', b, [rubber], tele)
    GB = Acc('gripper_bracket', dark); GB.box((0.6, 1.4, 0.25), (-3, 0, -4.32)); GB.build(tele)
    # ---- segment feeder (rollers on the invert) + backup rails
    FY = Acc('feeder_frame', yel); FR = Acc('feeder_rollers', dark); RL = Acc('backup_rails', chrome)
    for y in (-1.0, 1.0): FY.box((24.7, 0.15, 0.25), (-12.65, y, -5.86))
    for i in range(50): FR.cyl(0.08, 1.85, (-0.5 - i * 0.5, 0, -5.83), YQ, 12)
    for y in (-2.4, 2.4): RL.box((90, 0.16, 0.18), (-45.5, y, -5.46))
    FY.build(); FR.build(); RL.build()
    # ---- cutterhead (reuse the ch3 head, drop the rest of that machine)
    root, head = build_tbm('tbmh', gantries=0)
    keep = {head} | set(head.children_recursive)
    for o in list(root.children_recursive):
        if o not in keep: bpy.data.objects.remove(o, do_unlink=True)
    root.parent = mach; root.location = (12.0, 0, 0); G['head'] = head
    # ---- ground half-block (y >= 0) bored to x = 46, plug ahead of the face, grout, water beads
    gm = world_coords(strata(mat('ground', (0.3, 0.23, 0.16), 0.9), (0.20, 0.16, 0.12), (0.38, 0.30, 0.21), 0.35, 4.0, 0.3))
    A = Acc('ground', gm); A.box((190, 70, 80), (0, 35, 0)); gr = A.build()
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=BORE, depth=142.0, location=(-25.0, 0, 0), rotation=(0, math.pi / 2, 0))
    cu = bpy.context.active_object
    md = gr.modifiers.new('bore', 'BOOLEAN'); md.object = cu; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
    bpy.context.view_layer.objects.active = gr; bpy.ops.object.modifier_apply(modifier='bore'); bpy.data.objects.remove(cu, do_unlink=True)
    b = bmesh.new(); sector(b, 0.02, BORE - 0.005, -1.0, 0.0, 0, 180, 64); pl = mesh_obj('face_plug', b, [gm]); pl.location = (46.0, 0, 0); G['plug'] = pl
    grout = noisy(mat('grout', (0.28, 0.25, 0.2), 0.75), 9.0, 0.75, 0.2)
    gnew = noisy(mat('grout_wet', (0.25, 0.22, 0.175), 0.35), 9.0, 0.75, 0.2)
    b = bmesh.new(); sector(b, 6.556, 6.815, -91.0, -1.0, 0, 180, 64); mesh_obj('grout_old', b, [grout])
    b = bmesh.new(); sector(b, 6.556, 6.815, 0.0, 1.0, 0, 180, 64); gn = mesh_obj('grout_new', b, [gnew]); gn.location = (-1.0, 0, 0); G['grout'] = gn
    wm = mat('water_bead', (0.04, 0.22, 0.42), 0.05, 0, (0.1, 0.45, 0.8), 1.2)
    rng = random.Random(11); G['beads'] = []

    for i in range(16):
        r = rng.uniform(0.035, 0.06)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r, location=(0, -0.03, 9)); bd = bpy.context.active_object
        bd.data.materials.append(wm)
        for pg in bd.data.polygons: pg.use_smooth = True
        ta = rng.uniform(36.3, 37.4)
        G['beads'].append((bd, rng.uniform(-4.0, -1.2), rng.uniform(7.4, 8.4), 6.815 + r * 0.6, ta, ta + rng.uniform(1.2, 1.9)))
    # ---- lights: tunnel lamps + wall strips, shield lamps, bulkhead backlights, hero spot, section fill
    for sd, a in (('far', 115), ('near', -115)):
        b = bmesh.new(); sector(b, 5.97, 6.03, -90.0, -0.6, a - 0.6, a + 0.6, 1)
        o = mesh_obj('wall_strip_' + sd, b, [mat('strip_' + sd, (1, 0.9, 0.7), 0.4, 0, (1.0, 0.86, 0.62), 1.5)])
        if sd == 'near': NEAR.append(o)
    def pl_(loc, e, par=None):
        bpy.ops.object.light_add(type='POINT', location=loc); l = bpy.context.active_object
        l.data.energy = e; l.data.color = (1.0, 0.8, 0.55); l.data.shadow_soft_size = 1.0
        if par: l.parent = par
        return l
    for x in range(-80, -3, 9): pl_((x, 1.5, 4.2), 130)
    for loc in ((7.2, 3.5, 3.0), (7.2, -3.5, 3.0), (7.2, 0, -4.4)): pl_(loc, 260, mach)   # behind the erector: backlight
    G['keep_shadow'] = []
    for loc in ((8.6, 2.2, 1.8), (8.6, -2.2, 1.8), (8.6, 0, -2.5)):
        bpy.ops.object.light_add(type='AREA', location=loc, rotation=(0, math.pi / 2, 0)); l = bpy.context.active_object
        l.data.energy = 500; l.data.size = 1.5; l.data.color = (1.0, 0.85, 0.6); l.parent = mach
        if loc[2] > 0: G['keep_shadow'].append(l)                                      # the two upper backlights are the interior key
    hero_c = Vector((1, -3.02, -3.6)); sp = Vector((3.2, 0.6, 0.8))
    bpy.ops.object.light_add(type='SPOT', location=sp, rotation=(hero_c - sp).to_track_quat('-Z', 'Y').to_euler()); s = bpy.context.active_object
    s.data.energy = 0; s.data.spot_size = rad(40); s.data.spot_blend = 0.5; s.data.color = (1.0, 0.93, 0.82); s.data.shadow_soft_size = 0.6; G['spot'] = s; G['keep_shadow'].append(s)
    fp = Vector((0, -60, 14))
    bpy.ops.object.light_add(type='AREA', location=fp, rotation=(Vector((5, 0, 0)) - fp).to_track_quat('-Z', 'Y').to_euler()); f = bpy.context.active_object
    f.data.energy = 0; f.data.size = 120; f.data.color = (0.85, 0.92, 1.0); G['fill'] = f
    rp = Vector((-6.0, -2.2, 6.75))                                                    # grazing rim on the grout layer
    bpy.ops.object.light_add(type='AREA', location=rp, rotation=(Vector((0, 0.3, 6.7)) - rp).to_track_quat('-Z', 'Y').to_euler()); rl = bpy.context.active_object
    rl.data.energy = 0; rl.data.size = 1.5; rl.data.color = (0.9, 0.95, 1.0); G['rim'] = rl
    G['near'] = NEAR


# ---------------------------------------------------------------- casting yard (y ~ 3000)
def gantry(name, x0, yc, span=25.0, h=14.0):
    yel = noisy(mat(name + '_paint', (0.75, 0.55, 0.08), 0.55, 0.0), 3.0, 0.75, 0.1); dk = mat(name + '_dk', (0.05, 0.05, 0.055), 0.55, 0.7)
    root = empty(name, (x0, yc, 0)); A = Acc(name + '_y', yel); B = Acc(name + '_d', dk)
    for sy in (-1, 1):
        for sx in (-1, 1): A.box((0.9, 0.9, h), (sx * 4, sy * span / 2, h / 2 + 0.9))
        A.box((10, 1.2, 1.2), (0, sy * span / 2, h + 1.4)); B.box((10.5, 1.0, 0.9), (0, sy * span / 2, 0.45))
        for sx in (-4.5, -3.5, 3.5, 4.5): B.cyl(0.45, 0.5, (sx, sy * span / 2, 0.45), YQ, 16)
        A.beam((-4, sy * span / 2, 2.0), (4, sy * span / 2, h), 0.35)
    for sx in (-1.6, 1.6): A.box((1.0, span + 1.5, 1.6), (sx, 0, h + 2.4))
    A.build(root); B.build(root)
    tr = empty(name + '_trolley', (0, -4.0, 0), root)
    C = Acc(name + '_trolley_m', dk); C.box((4.2, 3.0, 1.6), (0, 0, h + 4.0))
    zl = 4.5
    for sx in (-0.6, 0.6):
        for sy in (-0.4, 0.4): C.beam((sx, sy, h + 3.2), (sx, sy, zl + 0.5 + 0.3), 0.05)
    C.box((2.2, 3.0, 0.3), (0, 0, zl + 0.5 + 0.15)); C.build(tr)
    b = bmesh.new(); sector(b, R_IN, R_OUT, -1, 1, -19, 19, 10, Matrix.Translation((0, 0, zl + R_OUT)))
    mesh_obj(name + '_load', b, [G['yard_mats'][0]], tr)
    return root, tr


def build_yard():
    hard = noisy(mat('hardstand', (0.40, 0.39, 0.36), 0.85), 0.35, 0.7, 0.2)
    A = Acc('yard_ground', hard); A.box((1600, 1600, 0.2), (300, Y0, -0.1)); A.build()
    mats = [noisy(mat(f'yard_conc{i}', c, 0.85), 9.0, 0.7, 0.35) for i, c in enumerate(((0.58, 0.57, 0.54), (0.52, 0.51, 0.48), (0.62, 0.60, 0.56)))]
    G['yard_mats'] = mats
    bms = [bmesh.new() for _ in mats]
    tim = Acc('battens', noisy(mat('timber', (0.32, 0.21, 0.11), 0.8), 6.0, 0.6, 0.3))
    rng = random.Random(7)
    for j in range(-3, 9):
        yr = Y0 + j * 6.5
        for i in range(110):
            x = i * 2.8; nl = rng.choice((4, 5, 5, 6)); v = rng.randrange(3)
            for L in range(nl):
                z = 0.25 + L * 0.64
                sector(bms[v], R_IN, R_OUT, x - 1, x + 1, -19, 19, 6, Matrix.Translation((x, yr, z + R_OUT)))
                for sy in (-1.3, 1.3):
                    if L == 0: tim.box((2.1, 0.15, 0.38), (x, yr + sy, 0.19))
                    else: tim.box((2.1, 0.12, 0.12), (x, yr + sy, z + 0.07))
    for i, b in enumerate(bms): mesh_obj(f'yard_segments_{i}', b, [mats[i]])
    tim.build()
    S = Acc('casting_shed', noisy(mat('shed', (0.35, 0.37, 0.38), 0.5, 0.6), 2.0, 0.7, 0.1))
    S.box((60, 90, 14), (350, Y0 + 20, 7)); S.box((62, 92, 1.0), (350, Y0 + 20, 14.5)); S.build()
    G['gan'] = gantry('gantry_a', 30.0, Y0 - 9.75)
    gantry('gantry_b', 150.0, Y0 + 29.25)
    w = bpy.context.scene.world or bpy.data.worlds.new('W'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    sky = nt.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'SINGLE_SCATTERING'; sky.sun_elevation = rad(30); sky.sun_rotation = rad(110); sky.sun_disc = False
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.03; ot = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(sky.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], ot.inputs['Surface'])
    G['bg'] = bg
    bpy.ops.object.light_add(type='SUN', rotation=(rad(60), 0, rad(200))); s = bpy.context.active_object
    s.data.energy = 0; s.data.color = (1.0, 0.93, 0.82); s.data.angle = rad(1.0); G['sun'] = s; G['keep_shadow'].append(s)


# ---------------------------------------------------------------- motion (pure functions of t)
W = [(0.0, EX_PLACE, 120, RG_L), (3.7, EX_PLACE, 120, RG_L), (6.9, EX_PICK, 0, RG_L), (7.6, EX_PICK, 0, RG_F),
     (8.1, EX_PICK, 0, RG_F), (9.0, EX_PICK, 0, RG_L), (10.4, EX_PLACE, 0, RG_L), (10.7, EX_PLACE, 0, RG_L),
     (14.1, EX_PLACE, -40, RG_L), (17.0, EX_PLACE, -40, RG_L), (17.5, EX_PLACE, 0, RG_L), (17.85, EX_PLACE, 0, R_IN)]
GRAB, REL = {0: 7.6}, {0: 17.85}
_c, _D = 17.85, 0.66
for _o in range(1, 9):                                     # time-lapse pace: 0.66 s per segment
    W += [(_c + 0.10 * _D, EX_PLACE, TH[_o - 1], RG_L), (_c + 0.42 * _D, EX_PICK, 0, RG_L), (_c + 0.50 * _D, EX_PICK, 0, RG_F),
          (_c + 0.58 * _D, EX_PICK, 0, RG_L), (_c + 0.88 * _D, EX_PLACE, TH[_o], RG_L), (_c + _D, EX_PLACE, TH[_o], R_IN)]
    GRAB[_o], REL[_o] = _c + 0.50 * _D, _c + _D; _c += _D
W += [(_c + 0.25, EX_PLACE, TH[8], RG_L), (_c + 0.85, EX_PICK, 0, RG_L), (_c + 1.05, EX_PICK, 0, RG_F), (_c + 1.3, EX_PICK, 0, RG_L),
      (_c + 2.0, EX_KEY, 180, RG_L), (_c + 2.3, EX_KEY, 180, R_IN), (_c + 3.0, EX_PLACE, 180, R_IN)]
GRAB[9], REL[9] = _c + 1.05, _c + 3.0
T_LOCK = REL[9]
W += [(T_LOCK + 0.45, EX_PLACE, 180, R_IN), (T_LOCK + 1.25, EX_PLACE, 180, RG_L), (T_END, EX_PLACE, 180, RG_L)]
SHIFT = [GRAB[0] + 1.4] + [GRAB[j] + 0.06 for j in range(1, 10)]


def E(t):
    if t <= W[0][0]: return W[0][1:]
    for a, b in zip(W[:-1], W[1:]):
        if t <= b[0]:
            u = sm((t - a[0]) / max(1e-6, b[0] - a[0]))
            return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
    return W[-1][1:]


def M_of(t):
    return 2.0 * win(t, 31.4, 33.6) + 30.0 * win(t, 39.6, 42.3)


def seg_pose(o, t, m):
    if t >= REL[o]: return 1.0, TH[o], R_IN
    if t >= GRAB[o]:
        ex, th, rg = E(t); return m + ex - 3.0, th, rg
    q = o - sum(win(t, SHIFT[j], SHIFT[j] + 0.4) for j in range(o))
    return -1.2 - 2.2 * q, 0.0, RG_F


def expo(t):
    if t < 41.95: return 0.1
    if t < 42.6: return 0.1 - 8.1 * win(t, 41.95, 42.30)
    return -8.0 + 8.1 * win(t, 42.6, 42.95)


KEY = {'on': False, 'f': 1}; LAST = {}; IDS = set()


def put(owner, attr, val):
    if isinstance(val, (tuple, list, Vector)): val = tuple(round(float(v), 5) for v in val)
    elif isinstance(val, float): val = round(val, 5)
    setattr(owner, attr, val)
    if not KEY['on']: return
    f = KEY['f']; k = (owner.as_pointer(), attr); lf = LAST.get(k)
    if lf is None or lf[1] != val:
        if lf is not None and lf[0] < f - 1:                   # anchor the hold before a change
            setattr(owner, attr, lf[1]); owner.keyframe_insert(attr, frame=f - 1); setattr(owner, attr, val)
        owner.keyframe_insert(attr, frame=f); LAST[k] = (f, val); IDS.add(owner.id_data)


def state(t):
    m = M_of(t); out_ = t >= TX[0]
    put(G['mach'], 'location', (m, 0, 0))
    ex, th, rg = E(t)
    put(G['ere'], 'location', (ex, 0, 0)); put(G['ere'], 'rotation_euler', (rad(th), 0, 0)); put(G['tele'], 'location', (0, 0, -(rg - 4.6)))
    for o, s in enumerate(G['seg']):
        x, a, r = seg_pose(o, t, m)
        loc = Vector((x, 0, 0)) + Matrix.Rotation(rad(a), 3, 'X') @ Vector((0, 0, R_IN - r))
        put(s, 'location', loc); put(s, 'rotation_euler', (rad(a), 0, 0))
        put(s, 'hide_render', bool(out_ and o in (0, 2, 4, 6, 8, 9)))
    for tw in G['twins']: put(tw, 'hide_render', not out_)
    for o in G['near']: put(o, 'hide_render', bool(out_))
    put(G['fill'].data, 'energy', 22000.0 if out_ else 0.0)
    put(G['rim'].data, 'energy', 250.0 * win(t, 33.8, 34.6) * (1 - win(t, 39.2, 39.8)))
    if m <= 2.0:
        xs = 3.2 - 1.2 * win(t, 27.6, 28.6)
    else:
        K = max([0] + [k for k in range(1, 16) if m >= 2 * k + 0.3]); xs = 2.0 * K + 2.0
    for sd in ('far', 'near'):
        put(G['shoes_' + sd], 'location', (xs, 0, 0))
        put(G['rods_' + sd], 'location', (xs + 0.25, 0, 0)); put(G['rods_' + sd], 'scale', (max(0.05, m + 3.6 - xs - 0.25), 1, 1))
    for k, rg_ in enumerate(G['tl'], 1): put(rg_, 'hide_render', not (m >= 2 * k + 0.3))
    put(G['grout'], 'scale', (max(0.001, 2.0 * win(t, 34.5, 36.0) + max(0.0, m - 2.0)), 1, 1))
    put(G['plug'], 'scale', (max(0.001, 46.0 - (m + 13.4)), 1, 1))
    for bd, x, z0, zs, ta, tb in G['beads']:
        u = sm((t - ta) / (tb - ta)); g = sm((t - ta) / 0.3); fl = 1.0 - 0.35 * sm((t - tb + 0.2) / 0.4)
        put(bd, 'hide_render', t < ta); put(bd, 'location', (x, -0.03, z0 + (zs - z0) * (1 - (1 - u) ** 2)))
        put(bd, 'scale', (max(0.01, g), max(0.01, g), max(0.01, g * fl)))
    put(G['head'], 'rotation_euler', (0, 0, rad(12.0 * t + 15.0 * max(0.0, m - 2.0))))
    put(G['spot'].data, 'energy', 800.0 * win(t, 10.4, 11.0) * (1 - win(t, 17.0, 17.6)))
    fl = max(0.0, 1.0 - abs(t - (T_LOCK + 0.18)) / 0.3)
    for sm_ in G['seg_mats']: put(sm_.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], 'default_value', 0.8 * fl)
    yard = t >= 42.45
    put(G['sun'].data, 'energy', 1.7 if yard else 0.0); put(G['bg'].inputs['Strength'], 'default_value', 0.12 if yard else 0.03)
    put(bpy.context.scene.view_settings, 'exposure', expo(t))
    gr, tr = G['gan']
    put(gr, 'location', (30.0 + 10.0 * win(t, 42.6, T_END), Y0 - 9.75, 0)); put(tr, 'location', (0, -4.0 + 7.0 * win(t, 43.5, 48.5), 0))


def anchors(cam, pts):
    """{name: (fn, times)} -> screen positions (0-1, y from top) at those times."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; outd = {}
    for name, (fn, times) in pts.items():
        outd[name] = []
        for t in times:
            sc.frame_set(int(round(t * FPS)) + 1); state(t); bpy.context.view_layer.update()
            v = world_to_camera_view(sc, cam, fn()); outd[name].append([round(t, 2), round(v.x, 4), round(1 - v.y, 4)])
    return outd


def run(args):
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    build_tunnel(); build_yard()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, int(round(T_END * FPS)), FPS
    cam, tg = path_camera(PATH, FPS)
    jf = {int(round(t * FPS)) + 1 for t in (J0, J1, J2)}               # hold-then-jump keys around the black dip
    for ob in (cam, tg, cam.data):
        for fc in fcurves_of(ob):
            for kp in fc.keyframe_points:
                if int(round(kp.co.x)) in jf: kp.interpolation = 'CONSTANT'
    for f in range(int(29.4 * FPS), int(32.0 * FPS)):                    # cutaway switch = camera inside the lining wall
        sc.frame_set(f)
        if cam.matrix_world.translation.y < -(R_IN + R_OUT) / 2:
            TX[0] = (f - 1) / FPS; break
    sc.render.engine = 'BLENDER_EEVEE'; ee = sc.eevee; ee.taa_render_samples = 64
    for k, v in (('shadow_pool_size', '2048'), ('shadow_resolution_scale', 1.0), ('shadow_ray_count', 2), ('shadow_step_count', 8)):
        if hasattr(ee, k):
            try: setattr(ee, k, v)
            except Exception as e: result.setdefault('eevee_warn', []).append(f'{k}: {e}')
    keep = {o.data.name for o in G['keep_shadow']}                     # stable shadows: only the key lights cast them
    for l in bpy.data.lights:
        l.use_shadow = l.name in keep
        if hasattr(l, 'use_shadow_jitter'): l.use_shadow_jitter = False
    result['shadow_lights'] = sorted(keep)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, int(args.get('pct', 50))
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    s0, ere, mach = G['seg'][0], G['ere'], G['mach']
    Ls = lambda o, v: o.matrix_world @ Vector(v)
    result['tx'] = TX[0]
    if args.get('mode') == 'track':
        result['track'] = track_screen(cam, {
            'erector_arm': (lambda: Ls(ere, (-3, 0, -3.0)), 2.0, 10.0),
            'segment': (lambda: Ls(s0, (0, 0, -6.3)), 8.5, 16.5),
            'grout_new': (lambda: Vector((0, 0, 6.69)), 32.5, 38.5)}, FPS, pre=state); return
    result['anchors'] = anchors(cam, {
        'erector_arm': (lambda: Ls(ere, (-3, 0, -3.0)), [1.8, 5.5]),
        'segment': (lambda: Ls(s0, (0, 0, -6.3)), [9.0, 12.5, 15.8]),
        'seg_w0_inner': (lambda: Ls(s0, P(-1, R_IN, 19)), [15.8]),
        'seg_w1_inner': (lambda: Ls(s0, P(1, R_IN, 19)), [15.8]),
        'seg_t_outer': (lambda: Ls(s0, P(1, R_OUT, 19)), [15.8]),
        'ring_crown': (lambda: Vector((1, 0, 6.3)), [20.0, 26.3]),
        'ring_side': (lambda: Vector((1, 6.3, 0)), [20.0]),
        'key': (lambda: Ls(G['seg'][9], (0, 0, -6.3)), [25.8, 26.3]),
        'jack_shoe': (lambda: Vector((G['shoes_far'].location.x + 0.1, 6.3, 0)), [28.8]),
        'shield': (lambda: Ls(mach, (5, 0, 6.8)), [32.8]),
        'tail': (lambda: Ls(mach, (-1, 0, 6.7)), [32.8]),
        'grout_new': (lambda: Vector((0, 0, 6.69)), [35.6]),
        'grout_line': (lambda: Vector((-3, 0, 6.82)), [38.3]),
        'tube': (lambda: Vector((15, 0, 0)), [41.5]),
        'stacks': (lambda: Vector((20, Y0, 2)), [46.0]),
        'gantry': (lambda: Ls(G['gan'][0], (0, 0, 16)), [46.0]),
    })
    if args.get('mode', 'preview') == 'preview':
        for t in ([(f - 1) / FPS for f in args['frames']] if args.get('frames') else args.get('times', (1.8, 5.5, 8.8, 12.5, 15.8, 20.0, 25.8, 26.3, 28.8, 32.8, 35.6, 38.3, 41.5, 46.0))):
            sc.frame_set(int(round(t * FPS)) + 1); state(t)
            fr = int(round(t * FPS)) + 1
            sc.render.filepath = f'{out}/t_{t:04.1f}.png' if not args.get('frames') else f'{out}/f_{fr:04d}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        KEY['on'] = True
        for f in range(sc.frame_start, sc.frame_end + 1):
            KEY['f'] = f; state((f - 1) / FPS)
        for idb in IDS:
            for fc in fcurves_of(idb):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
        KEY['on'] = False
        video_output(sc, out + '/ch5_rings.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
