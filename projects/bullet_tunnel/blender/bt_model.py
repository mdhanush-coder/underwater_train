# Shared bullet-tunnel models (runs after skilllib.py). Real counts from NHSRCL/NBM&CW: cutterhead 13.6 m, 84 disc cutters,
# 124 scrapers, 16 bucket lips; Mixshield; ~96 m long. Everything is built with bmesh accumulators (one object per material).
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Quaternion


def mat(name, col, rough=0.6, metal=0.0, em=None, emv=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if em:
        b.inputs['Emission Color'].default_value = (*em, 1); b.inputs['Emission Strength'].default_value = emv
    return m


def noisy(m, scale=6.0, dark=0.55, bump=0.3):
    """Add object-space noise variation to a material's base colour + bump (breaks the flat CG look)."""
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    base = Vector(b.inputs['Base Color'].default_value[:3])
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 8; nz.inputs['Roughness'].default_value = 0.65
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    sA = [x for x in mix.inputs if x.name == 'A' and x.type == 'RGBA'][0]; sB = [x for x in mix.inputs if x.name == 'B' and x.type == 'RGBA'][0]
    sA.default_value = (*(base * dark), 1); sB.default_value = (*base, 1)
    sR = [x for x in mix.outputs if x.type == 'RGBA'][0]
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector']); nt.links.new(nz.outputs['Fac'], mix.inputs['Factor'])
    nt.links.new(sR, b.inputs['Base Color'])
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


class Acc:
    """Accumulates boxes / cylinders / beams into one mesh object."""
    def __init__(self, name, m):
        self.bm = bmesh.new(); self.name = name; self.m = m

    @staticmethod
    def _M(loc, rot, scale=(1, 1, 1)):
        R = rot.to_matrix().to_4x4() if rot is not None else Matrix.Identity(4)
        return Matrix.Translation(Vector(loc)) @ R @ Matrix.Diagonal((*scale, 1.0))

    def box(self, size, loc, rot=None):
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        bmesh.ops.transform(self.bm, matrix=self._M(loc, rot, size), verts=r['verts'])

    def cyl(self, r, h, loc, rot=None, segs=24, r2=None):
        r_ = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r, radius2=(r if r2 is None else r2), depth=h)
        bmesh.ops.transform(self.bm, matrix=self._M(loc, rot), verts=r_['verts'])

    def beam(self, a, b, w, w2=None):
        a, b = Vector(a), Vector(b); d = b - a
        self.box((w, w if w2 is None else w2, d.length), (a + b) / 2, d.to_track_quat('Z', 'Y'))

    def lattice(self, a, b, w, chord=0.2, brace=0.1, step=2.0):
        a, b = Vector(a), Vector(b); d = b - a; q = d.to_track_quat('Z', 'Y')
        ex, ey = q @ Vector((1, 0, 0)), q @ Vector((0, 1, 0))
        cs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        P = lambda i, u: a + d * u + ex * cs[i][0] * w / 2 + ey * cs[i][1] * w / 2
        for i in range(4): self.beam(P(i, 0), P(i, 1), chord)
        n = max(1, int(d.length / step))
        for k in range(n):
            u0, u1 = k / n, (k + 1) / n
            for i in range(4):
                j = (i + 1) % 4
                self.beam(P(i, u0), P(j, u1), brace) if k % 2 == 0 else self.beam(P(j, u0), P(i, u1), brace)
                self.beam(P(i, u0), P(j, u0), brace)

    def build(self, parent=None, smooth=False):
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        me.materials.append(self.m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        o = bpy.data.objects.new(self.name, me); bpy.context.scene.collection.objects.link(o)
        if parent is not None: o.parent = parent
        return o


def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.location = loc
    if parent is not None: e.parent = parent
    return e


def zrot_to(v):
    return Vector((0, 0, 1)).rotation_difference(Vector(v).normalized())


# ---------------------------------------------------------------- TBM (local frame: +Z = digging direction, face at z ~ +0.9)
def build_tbm(name='tbm', gantries=2, hollow=False):
    root = empty(name)
    head = empty(name + '_head', parent=root)
    steel = mat('head_steel', (0.09, 0.09, 0.10), 0.55, 1.0)
    disc_m = mat('disc_steel', (0.55, 0.56, 0.58), 0.28, 1.0)
    hard = mat('hardfacing', (0.34, 0.19, 0.04), 0.5, 0.9)       # worn orange hard-faced scrapers
    paint = noisy(mat('shield_paint', (0.10, 0.17, 0.26), 0.5, 0.4), 3.0, 0.7, 0.15)
    dark = mat('machine_dark', (0.05, 0.055, 0.06), 0.5, 1.0)
    yellow = mat('safety_yellow', (0.55, 0.38, 0.02), 0.5, 0.2)
    hyd = mat('hydraulic', (0.60, 0.61, 0.62), 0.25, 1.0)
    RR = 6.8
    A = Acc('cutter_frame', steel); D = Acc('disc_cutters', disc_m); S = Acc('scrapers', hard); BL = Acc('bucket_lips', hard)
    A.cyl(1.7, 1.5, (0, 0, 0.1), segs=32)                                    # hub
    for i in range(6):                                                         # 6 spokes
        a = i * math.pi / 3; ux, uy = math.cos(a), math.sin(a)
        A.box((RR - 1.2, 1.9, 1.3), (ux * (RR + 1.2) / 2, uy * (RR + 1.2) / 2, 0.0), Quaternion((0, 0, 1), a))
        k = 0
        for side in (-1, 1):                                                   # 2 rows x 7 discs = 14 per spoke = 84
            for j in range(7):
                r = 2.3 + j * 0.62
                px, py = ux * r - uy * side * 0.6, uy * r + ux * side * 0.6
                t = Vector((-uy, ux, 0))                                        # disc axis = tangent (disc rolls radially)
                q = zrot_to(t)
                A.box((0.55, 0.40, 0.50), (px, py, 0.82), Quaternion((0, 0, 1), a))   # housing
                D.cyl(0.26, 0.15, (px, py, 1.12), q, 20)                        # the disc
                k += 1
        for side in (-1, 1):                                                   # 2 edges x 10 scrapers = 20 per spoke (120) ...
            for j in range(10):
                r = 1.9 + j * 0.46
                S.box((0.36, 0.16, 0.30), (ux * r - uy * side * 1.0, uy * r + ux * side * 1.0, 0.85), Quaternion((0, 0, 1), a))
    for j in range(4):                                                         # ... + 4 at the hub = 124
        a = j * math.pi / 2 + 0.4
        S.box((0.36, 0.16, 0.30), (math.cos(a) * 1.2, math.sin(a) * 1.2, 0.95), Quaternion((0, 0, 1), a))
    for i in range(48):                                                        # rim ring
        a = i * math.tau / 48
        A.box((0.8, 0.5 * 1.0 + 0.2, 1.5), (math.cos(a) * (RR - 0.1), math.sin(a) * (RR - 0.1), 0.1), Quaternion((0, 0, 1), a + math.pi / 2) if False else Quaternion((0, 0, 1), a))
    for i in range(16):                                                        # 16 bucket lips on the rim
        a = (i + 0.5) * math.tau / 16
        BL.box((0.9, 0.5, 0.6), (math.cos(a) * (RR - 0.05), math.sin(a) * (RR - 0.05), 0.9), Quaternion((0, 0, 1), a))
    for o in (A.build(head), D.build(head, True), S.build(head), BL.build(head)):
        pass
    # shield skin (open tube if hollow), articulation jacks, tail skin
    SH = Acc('shield', paint)
    segs = 64
    SH.cyl(6.70, 7.0, (0, 0, -4.4), segs=segs)
    SH.cyl(6.62, 5.5, (0, 0, -11.9), segs=segs)
    sh = SH.build(root, True)
    if hollow:
        for ob in (sh,):
            ob.modifiers.new('sol', 'SOLIDIFY').thickness = -0.35
    J = Acc('articulation_jacks', hyd)
    for i in range(24):
        a = i * math.tau / 24
        J.cyl(0.17, 3.2, (math.cos(a) * 6.2, math.sin(a) * 6.2, -8.9), None, 12)
    J.build(root, True)
    # shield detail: plate seams, articulation gap, tail seal, grout ports, wear grime
    SD = Acc('shield_detail', dark)
    for z in (-1.2, -3.6, -6.0, -10.0, -12.6):
        SD.cyl(6.76, 0.12, (0, 0, z), segs=64)
    SD.cyl(6.66, 1.4, (0, 0, -8.55), segs=64)                                    # articulation joint (closes the shield gap)
    SD.cyl(6.68, 0.5, (0, 0, -14.45), segs=64)                                    # tail brush seal
    for i in range(16):
        a = i * math.tau / 16
        SD.cyl(0.14, 0.2, (math.cos(a) * 6.73, math.sin(a) * 6.73, -13.6), zrot_to((math.cos(a), math.sin(a), 0)), 10)
        SD.box((0.1, 0.1, 12.0), (math.cos(a) * 6.71, math.sin(a) * 6.71, -7.4), Quaternion((0, 0, 1), a))   # weld seams
    SD.build(root)
    # backup gantries (local frame: up = -x, lateral = y, along = z). Multi-deck lattice frames on rails, with plant.
    frame = noisy(mat('gantry_frame', (0.16, 0.17, 0.16), 0.55, 0.6), 4.0, 0.6, 0.2)
    grate = noisy(mat('gantry_grating', (0.22, 0.22, 0.21), 0.7, 0.7), 30.0, 0.5, 0.4)
    cab = noisy(mat('cabinet', (0.42, 0.44, 0.45), 0.45, 0.3), 3.0, 0.75, 0.1)
    tank = noisy(mat('tank_white', (0.62, 0.62, 0.58), 0.4, 0.2), 2.0, 0.8, 0.1)
    pipe_o = mat('slurry_pipe', (0.45, 0.18, 0.04), 0.45, 0.6)
    duct_m = noisy(mat('vent_duct', (0.55, 0.36, 0.04), 0.8), 2.0, 0.7, 0.3)
    lamp_m = mat('gantry_lamp', (1, 0.9, 0.7), 0.4, 0, (1.0, 0.85, 0.6), 6.0)
    win_m = mat('cabin_window', (0.2, 0.3, 0.35), 0.1, 0, (0.55, 0.8, 1.0), 2.5)
    G, Y, Gr, C, T, P, Du, Lp, W = (Acc('gantries', frame), Acc('gantry_rails', yellow), Acc('gantry_grating', grate), Acc('gantry_cabinets', cab),
                                    Acc('gantry_tanks', tank), Acc('gantry_pipes', pipe_o), Acc('vent_duct', duct_m), Acc('gantry_lamps', lamp_m), Acc('cabin_windows', win_m))
    L3 = lambda lat, up, al: (-up, lat, al)
    S3 = lambda sl, su, sa: (su, sl, sa)
    def bx(acc, size, c): acc.box(S3(*size), L3(*c))
    def bm_(acc, p, q, w): acc.beam(L3(*p), L3(*q), w)
    AX = Quaternion((0, 0, 1), 0)                     # cylinder along 'along' (local z) needs no rotation
    LATQ = zrot_to((0, 1, 0))                          # cylinder along lateral
    FLOOR, D1, D2, TOP, HW = -4.5, -1.4, 1.8, 3.6, 4.3
    z_start = -15.0
    zend = z_start - gantries * 9.0
    for g in range(gantries):
        z1 = z_start - g * 9.0; z2 = z1 - 8.6; zm = (z1 + z2) / 2
        for zc in (z1 - 0.3, zm, z2 + 0.3):                                       # portal columns + top beam + bogies
            for s in (-1, 1):
                bx(G, (0.36, TOP - FLOOR, 0.36), (s * HW, (TOP + FLOOR) / 2, zc))
                bx(G, (0.5, 0.5, 1.2), (s * HW, FLOOR + 0.1, zc)); P.cyl(0.32, 0.3, L3(s * (HW - 0.45), FLOOR - 0.2, zc), LATQ, 16)
            bx(G, (2 * HW + 0.4, 0.4, 0.4), (0, TOP, zc))
        for s in (-1, 1):                                                         # side bracing (X between columns)
            for za, zb in ((z1 - 0.3, zm), (zm, z2 + 0.3)):
                bm_(G, (s * HW, D1, za), (s * HW, D2, zb), 0.16); bm_(G, (s * HW, D2, za), (s * HW, D1, zb), 0.16)
                bm_(G, (s * HW, FLOOR + 0.5, za), (s * HW, D1, zb), 0.16)
        for up in (D1, D2):                                                       # two decks: stringers, cross beams, grating
            for s in (-1, 1): bx(G, (0.3, 0.45, 8.6), (s * (HW - 0.1), up - 0.25, zm))
            for k in range(5): bx(G, (2 * HW, 0.25, 0.2), (0, up - 0.25, z1 - 0.3 - k * 2.0))
            bx(Gr, (2 * HW + 0.6, 0.06, 8.6), (0, up, zm))
            for s in (-1, 1):                                                     # yellow railings on both deck edges
                ys = s * (HW + 0.3)
                for k in range(7): bx(Y, (0.07, 1.1, 0.07), (ys, up + 0.55, z1 - 0.1 - k * 1.4))
                bx(Y, (0.07, 0.07, 8.6), (ys, up + 1.1, zm)); bx(Y, (0.06, 0.06, 8.6), (ys, up + 0.55, zm)); bx(Y, (0.04, 0.18, 8.6), (ys, up + 0.09, zm))
            for k in range(3): bx(Lp, (0.5, 0.08, 0.25), (-2.0 + k * 2.0, up - 0.52, zm + 2.5))
        kind = g % 4                                                              # plant on the decks
        if kind == 0:                                                             # control cabin + transformer
            bx(C, (3.2, 2.4, 4.0), (-1.4, D1 + 1.2, zm)); bx(W, (0.05, 0.8, 2.8), (-3.02, D1 + 1.5, zm))
            bx(C, (2.4, 2.0, 2.2), (2.0, D2 + 1.0, zm - 1.5))
            for k in range(8): bx(G, (2.2, 1.6, 0.06), (2.0, D2 + 1.0, zm + 0.6 + k * 0.3))   # transformer fins
        elif kind == 1:                                                           # hydraulic power packs
            for k in range(3):
                bx(C, (2.0, 1.6, 2.2), (-2.0, D1 + 0.8, z1 - 1.6 - k * 2.6)); P.cyl(0.32, 0.9, L3(-2.0, D1 + 1.9, z1 - 1.6 - k * 2.6), zrot_to((-1, 0, 0)), 16)
            bx(C, (1.8, 2.2, 6.0), (2.2, D2 + 1.1, zm))
        elif kind == 2:                                                           # grout / bentonite tanks
            for k in range(2):
                T.cyl(1.05, 3.6, L3(-1.8, D1 + 1.15, zm + (k - 0.5) * 4.0), AX, 28)
                T.cyl(0.9, 2.2, L3(1.8, D2 + 1.0, zm + (k - 0.5) * 4.0), zrot_to((-1, 0, 0)), 28)
        else:                                                                     # cable and hose reels
            for k, (lat, r) in enumerate(((-1.8, 1.5), (1.6, 1.2))):
                T.cyl(r, 0.25, L3(lat, D1 + r + 0.1, zm - 1.6), AX, 32); T.cyl(r, 0.25, L3(lat, D1 + r + 0.1, zm + 1.6), AX, 32)
                C.cyl(r * 0.7, 3.0, L3(lat, D1 + r + 0.1, zm), AX, 32)
            bx(C, (3.6, 1.8, 3.0), (0, D2 + 0.9, zm))
    for lat, up, r in ((3.3, -3.9, 0.32), (2.5, -3.9, 0.32)):                     # slurry feed + discharge lines, flanges every 6 m
        P.cyl(r, -zend + 2 - 12, L3(lat, up, (zend - 12 + 2) / 2 - 1), AX, 20)
        for zz in range(-14, int(zend), -6): P.cyl(r + 0.1, 0.12, L3(lat, up, zz), AX, 20)
    Du.cyl(0.65, -zend - 13, L3(0, TOP + 1.3, (zend - 13) / 2 - 6.5 + 6.5), AX, 28)  # ventilation duct with rings
    for zz in range(-14, int(zend), -2): Du.cyl(0.69, 0.12, L3(0, TOP + 1.3, zz), AX, 28)
    for acc in (G, Y, Gr, C, P, Lp, W): acc.build(root)
    T.build(root, True); Du.build(root, True)
    root.rotation_euler = (0, math.pi / 2, 0)                                   # +Z -> +X
    return root, head


# ---------------------------------------------------------------- site dressing
def tower_crane(name, base, height=52.0, jib=38.0, yaw=0.0):
    ye = mat('crane_paint', (0.52, 0.34, 0.03), 0.55, 0.3)
    wh = mat('crane_white', (0.62, 0.62, 0.60), 0.6, 0.2)
    A = Acc(name + '_mast', ye); B = Acc(name + '_dark', mat(name + 'k', (0.06, 0.06, 0.065), 0.55, 0.8))
    bx, by, bz = base
    A.lattice((bx, by, bz), (bx, by, bz + height), 2.2, 0.25, 0.12, 2.2)
    cy_ = Vector((math.cos(yaw), math.sin(yaw), 0))
    top = Vector((bx, by, bz + height))
    A.lattice(top + Vector((0, 0, 3.4)), top + Vector((0, 0, 3.4)) + cy_ * jib, 1.6, 0.18, 0.09, 2.0)
    A.beam(top + Vector((0, 0, 2.5)), top + Vector((0, 0, 2.5)) - cy_ * 12, 1.2)                     # counter-jib
    B.box((3.0, 3.0, 2.2), top - cy_ * 10 + Vector((0, 0, 1.6)))                                      # counterweights
    B.box((2.4, 2.4, 2.6), top + Vector((0, 0, 1.2)))                                                # cab
    hook_x = top + cy_ * (jib * 0.62)
    B.beam(hook_x + Vector((0, 0, 3.0)), hook_x - Vector((0, 0, 14.0)), 0.07)
    B.box((0.7, 0.7, 0.9), hook_x - Vector((0, 0, 14.5)))
    A.build(); B.build()


def crawler_crane(name, loc, yaw=0.0, boom_to=None):
    ye = mat(name + 'y', (0.50, 0.32, 0.03), 0.55, 0.3); dk = mat(name + 'd', (0.05, 0.05, 0.055), 0.6, 0.7)
    A = Acc(name + '_body', ye); B = Acc(name + '_tracks', dk)
    R = Quaternion((0, 0, 1), yaw); L = Vector(loc)
    def P(v): return L + R @ Vector(v)
    for s in (-1, 1): B.box((14.0, 2.6, 2.4), P((0, s * 4.2, 1.2)), R)
    A.box((9.0, 7.0, 3.0), P((0, 0, 3.6)), R); A.box((3.0, 3.0, 2.8), P((3.4, 3.0, 6.0)), R)
    B.box((6.0, 5.5, 3.5), P((-4.8, 0, 6.2)), R)
    tip = Vector(boom_to) if boom_to else P((38, 0, 62))
    A.lattice(P((2.0, 0, 6.5)), tip, 2.4, 0.22, 0.1, 2.5)
    B.beam(tip, tip - Vector((0, 0, 40)), 0.07)
    A.build(); B.build()


def containers(rng_seed, area, n):
    rng = random.Random(rng_seed)
    cols = [(0.35, 0.08, 0.05), (0.08, 0.17, 0.30), (0.55, 0.55, 0.52), (0.12, 0.30, 0.18), (0.45, 0.30, 0.06)]
    accs = [Acc(f'cont{i}', noisy(mat(f'cm{i}', c, 0.7, 0.3), 12.0, 0.6, 0.1)) for i, c in enumerate(cols)]
    for k in range(n):
        x = rng.uniform(area[0], area[1]); y = rng.uniform(area[2], area[3]); a = rng.choice([0, math.pi / 2])
        accs[rng.randrange(len(cols))].box((6.0, 2.5, 2.6), (x, y, 1.3), Quaternion((0, 0, 1), a))
    for A in accs: A.build()


def light_mast(base, h=14.0):
    d = mat('mast', (0.1, 0.1, 0.1), 0.6, 0.8); l = mat('flood', (1, 0.9, 0.7), 0.3, 0, (1, 0.85, 0.6), 40.0)
    A = Acc('mast', d); B = Acc('flood', l)
    bx, by, bz = base
    A.beam((bx, by, bz), (bx, by, bz + h), 0.35)
    for s in (-1, 0, 1): B.box((0.9, 0.12, 0.55), (bx + s * 1.1, by, bz + h + 0.5))
    A.build(); B.build()


# ---------------------------------------------------------------- shared helpers added for the creek scene
def _sphere(self, r, loc, scale=(1, 1, 1), sub=1):
    res = bmesh.ops.create_icosphere(self.bm, subdivisions=sub, radius=r)
    bmesh.ops.transform(self.bm, matrix=self._M(loc, None, scale), verts=res['verts'])


Acc.sphere = _sphere


def strata(m, c1, c2, scale=0.5, distort=5.0, bump=0.25):
    """Layered ground: Wave bands along Z + noise, colour ramp c1..c2 (sedimentary look)."""
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave')
    wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.inputs['Scale'].default_value = scale
    wv.inputs['Distortion'].default_value = distort; wv.inputs['Detail'].default_value = 4
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.8; nz.inputs['Detail'].default_value = 10
    mx = nt.nodes.new('ShaderNodeMixRGB'); mx.blend_type = 'MULTIPLY'; mx.inputs['Fac'].default_value = 0.6
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*c1, 1); cr.color_ramp.elements[1].color = (*c2, 1)
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(wv.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], mx.inputs['Color1'])
    nt.links.new(nz.outputs['Fac'], mx.inputs['Color2']); nt.links.new(mx.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def path_camera(PATH, fps, name='Cam'):
    """ONE continuous camera: PATH = [(t_s, cam_xyz, look_xyz, lens)]; Bezier auto-clamped, TRACK_TO target empty."""
    sc = bpy.context.scene
    cam = make_camera(name, focal=30, fstop=8.0, clip=(0.1, 6000.0))
    tg = bpy.data.objects.new(name + '_t', None); sc.collection.objects.link(tg)
    tc = cam.constraints.new('TRACK_TO'); tc.target = tg; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
    cam.data.dof.use_dof = False
    for t, c, l, lens in PATH:
        f = int(round(t * fps)) + 1
        cam.location = Vector(c); cam.keyframe_insert('location', frame=f)
        tg.location = Vector(l); tg.keyframe_insert('location', frame=f)
        cam.data.lens = lens; cam.data.keyframe_insert('lens', frame=f)
    sc.camera = cam
    for ob in (cam, tg, cam.data):
        for fc in fcurves_of(ob):
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    return cam, tg


# ---------------------------------------------------------------- rigged crew (library Reallusion Worker, 101-bone armature)
def rigged_worker(x, y, z, yaw, seed=0, fps=30, frames=480):
    """Place the library Worker (rigged), drop its studio backdrop, recolour to site gear, pose arms down (local-Z rotation on the
    upper arms) and key a gentle idle (spine breathing, head turn, forearm gesture). Returns the root."""
    rg = random.Random(seed)
    root = place_asset('omni-characters-Worker', location=(x, y, z), rotation=(0, 0, yaw), size=1.8, floor=z)
    bpy.context.view_layer.update()
    for o in [root] + list(root.children_recursive):
        if o.type == 'MESH' and o.name.lower().startswith('background'):
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.context.view_layer.update()
    body = [o for o in [root] + list(root.children_recursive) if o.type == 'MESH' and 'Body' in o.name]
    cs = [o.matrix_world @ Vector(c) for o in body for c in o.bound_box]
    dims = [max(c[i] for c in cs) - min(c[i] for c in cs) for i in range(3)]
    f = 1.78 / max(dims)                                      # size= was measured with the studio backdrop in it: renormalise from the body mesh
    root.scale = tuple(sc_ * f for sc_ in root.scale)
    bpy.context.view_layer.update()
    cs = [o.matrix_world @ Vector(c) for o in body for c in o.bound_box]
    root.location.z += z - min(c.z for c in cs)
    bpy.context.view_layer.update()
    cols = {'cap': (0.75, 0.55, 0.02), 'jacket': (0.8, 0.28, 0.02), 'pant': (0.05, 0.08, 0.16), 'shoe': (0.03, 0.03, 0.035), 'scrub': (0.18, 0.2, 0.22)}
    skin = rg.choice([(0.30, 0.18, 0.11), (0.38, 0.24, 0.15), (0.24, 0.14, 0.09)])
    for o in [root] + list(root.children_recursive):
        if o.type != 'MESH': continue
        n = o.name.lower(); c = None
        if 'cap' in n or 'helmet' in n: c = cols['cap']
        elif 'jacket' in n: c = cols['jacket']
        elif 'pant' in n: c = cols['pant']
        elif 'shoe' in n: c = cols['shoe']
        elif 'scrub' in n or 'shirt' in n: c = cols['scrub']
        elif 'body' in n: c = skin
        if c is None: continue
        o.data.materials.clear(); o.data.materials.append(mat(f'wk_{n}_{seed}', c, 0.7))
    arm = [o for o in root.children_recursive if o.type == 'ARMATURE'][0]
    pb = arm.pose.bones
    for b in pb: b.rotation_mode = 'XYZ'
    for nm, sgn in (('L_Upperarm', -1), ('R_Upperarm', 1)):
        if nm in pb: pb[nm].rotation_euler = (0, 0, math.radians(62 * sgn))
    for nm, sgn in (('L_Forearm', -1), ('R_Forearm', 1)):
        if nm in pb: pb[nm].rotation_euler = (0, 0, math.radians(14 * sgn))
    ph = rg.uniform(0, 6.28)
    for k in range(0, frames, 15):
        t = k / fps
        for nm, ax, amp, per in (('Spine01', 0, 0.012, 3.2), ('Head', 2, 0.18, 6.5), ('R_Forearm', 2, 0.20, 4.1), ('L_Forearm', 2, 0.10, 5.3)):
            if nm in pb:
                e = list(pb[nm].rotation_euler)
                base = e[2] if ax == 2 and 'Forearm' in nm else 0.0
                if nm == 'R_Forearm': base = math.radians(14)
                if nm == 'L_Forearm': base = math.radians(-14)
                e[ax] = base + amp * math.sin(t * math.tau / per + ph)
                pb[nm].rotation_euler = tuple(e); pb[nm].keyframe_insert('rotation_euler', frame=k + 1)
    for nm in ('L_Upperarm', 'R_Upperarm'):
        if nm in pb: pb[nm].keyframe_insert('rotation_euler', frame=1)
    for fc in fcurves_of(arm):
        for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'
    return root
