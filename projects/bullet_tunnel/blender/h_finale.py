# Chapter 7 plate "Finale", Blender part (lines 77-83). Plate frame 1 = chapter time 7.1 s = global 283.005 s; 27.5 s = 825 f.
# One continuous camera: cutaway with two TBMs closing in from each side (77) -> calm wide for the MG map (78-79) -> dive to
# the finished ring tunnel (TBMs/soil swapped out of view at 11.2 s) -> E5-style train streaks past (80) -> camera chases it
# along the coaches (81) -> into a coach: seated passenger, dark window, tunnel lights passing (82) -> out and up through the
# rings, seabed layers and water to a calm sunset surface (83). Runs after skilllib.py + bt_model.py. args: mode, pct.
import bpy, bmesh, math, random
from mathutils import Vector, Quaternion, Matrix

FPS = 30
T_END = 27.5
XE = 1400.0
TZ = -35.0
R_IN, R_OUT, R_BORE = 6.05, 6.55, 6.8            # 13.1 m OD lining, 0.5 m thick, 13.6 m bore
FLOOR = TZ - 3.6                                  # rail top
TOP_INV = FLOOR - 0.44                            # invert concrete top (slab + pads + rail on it)
TY = 2.4                                          # track centre (the +y track of the twin-track tube)
ZC = FLOOR + 2.275                                # train body centre (body 0.9 .. 3.65 m above rail)
HW, HH = 1.675, 1.375                             # body half width / half height (3.35 x 2.75 m section)
V = 88.9                                          # 320 km/h
T_PASS = 12.5                                     # nose passes the line-80 camera (x = -94)
NOSE = 79.25                                      # nose tip ahead of the train centre
T_SWAP = 11.2                                     # TBMs + unbored soil swapped for the finished tunnel (out of view)
STILLS = (1.2, 3.6, 7.2, 11.9, 12.3, 12.9, 16.5, 21.5, 25.6, 27.4)


def F(t): return int(round(t * FPS)) + 1
def ss(a, b, x):
    u = min(1.0, max(0.0, (x - a) / (b - a))); return u * u * (3 - 2 * u)
def X_tr(t): return -94.0 - NOSE + V * (t - T_PASS)


def show_keys(objs, off=(), on=()):
    """hide_render keys: hidden from each t in off, visible again from each t in on."""
    ev = sorted([(t, True) for t in off] + [(t, False) for t in on])
    for o in objs:
        o.hide_render = not ev[0][1] if ev else False; o.keyframe_insert('hide_render', frame=1)
        for t, h in ev:
            o.hide_render = not h; o.keyframe_insert('hide_render', frame=F(t) - 1)
            o.hide_render = h; o.keyframe_insert('hide_render', frame=F(t))


# ---------------------------------------------------------------- ground, lining, track
def soil_layer(name, c, z0, z1, cuts):
    o = Acc(name, noisy(mat(name, c, 0.85), 16.0, 0.55, 0.55)); o.box((2 * XE, 300, z0 - z1), (0, 150, (z0 + z1) / 2)); ob = o.build()
    for x0, x1 in cuts:
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=R_BORE, depth=x1 - x0, location=((x0 + x1) / 2, 0, TZ), rotation=(0, math.pi / 2, 0))
        cu = bpy.context.active_object
        md = ob.modifiers.new('tun', 'BOOLEAN'); md.object = cu; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
        bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier='tun'); bpy.data.objects.remove(cu, do_unlink=True)
    return ob


def arc_solid(bm, r0, r1, a0, a1, x0, x1, step=math.radians(5)):
    n = max(2, int(math.ceil((a1 - a0) / step))); st = []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n; c, s = math.cos(a), math.sin(a)
        st.append([bm.verts.new((x, r * c, TZ + r * s)) for x, r in ((x0, r0), (x0, r1), (x1, r1), (x1, r0))])
    for a, b in zip(st[:-1], st[1:]):
        for i in range(4): bm.faces.new((a[i], a[(i + 1) % 4], b[(i + 1) % 4], b[i]))
    bm.faces.new(st[0][::-1]); bm.faces.new(st[-1])


def ring_pieces(off):
    """9 segments of 37.5 deg + a 22.5 deg key, rotated by off; clipped to the y >= 0 half (-90..90 deg). Seams 2 cm."""
    b = [off + 37.5 * k for k in range(10)] + [off + 360.0]
    g = math.degrees(0.01 / R_IN); out = []
    for k in range(10):
        for sh in (-360.0, 0.0, 360.0):
            lo, hi = b[k] + sh, b[k + 1] + sh
            lo2, hi2 = max(-90.0, lo), min(90.0, hi)
            if hi2 - lo2 > 0.5:
                out.append((lo2 + (g if lo2 == lo else 0), hi2 - (g if hi2 == hi else 0)))
    return out


def lining(name, x0, x1, lm, gm):
    """Segmental lining as a 4 m unit (two rings, staggered keys) arrayed along x."""
    st = 4.0 * math.floor(x0 / 4.0); n = int(round((x1 - st) / 4.0))
    bm = bmesh.new()
    for r, off in ((0, 0.0), (1, 18.75)):
        for a0, a1 in ring_pieces(off):
            arc_solid(bm, R_IN, R_OUT, math.radians(a0), math.radians(a1), st + r * 2.0 + 0.012, st + r * 2.0 + 1.988)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(lm)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    ar = o.modifiers.new('rings', 'ARRAY'); ar.count = n; ar.use_relative_offset = False; ar.use_constant_offset = True
    ar.constant_offset_displace = (4.0, 0, 0)
    bm = bmesh.new(); rr = 6.62; N = 36; vs = []                                # dark grout shell behind the seams
    for k in range(N + 1):
        a = math.radians(-90 + 180 * k / N)
        vs.append((bm.verts.new((st, rr * math.cos(a), TZ + rr * math.sin(a))), bm.verts.new((st + 4 * n, rr * math.cos(a), TZ + rr * math.sin(a)))))
    for (a, b_), (c, d) in zip(vs[:-1], vs[1:]): bm.faces.new((a, b_, d, c))
    me = bpy.data.meshes.new(name + '_grout'); bm.to_mesh(me); bm.free(); me.materials.append(gm)
    g = bpy.data.objects.new(name + '_grout', me); bpy.context.scene.collection.objects.link(g)
    return [o, g]


def prism(bm, pts, x0, x1):
    v0 = [bm.verts.new((x0, y, z)) for y, z in pts]; v1 = [bm.verts.new((x1, y, z)) for y, z in pts]; n = len(pts)
    bm.faces.new(v0[::-1]); bm.faces.new(v1)
    for i in range(n): bm.faces.new((v0[i], v0[(i + 1) % n], v1[(i + 1) % n], v1[i]))


def dressing(tag, x0, x1, M):
    """Invert, J-slabs, rails + fastenings, walkway, cable trays, wall LED fittings, overhead catenary."""
    L = x1 - x0; xm = (x0 + x1) / 2; objs = []
    bm = bmesh.new(); r = R_IN - 0.01; at = math.asin((TOP_INV - TZ) / r)
    pts = [(0.0, TOP_INV), (0.0, TZ - r)] + [(r * math.cos(a), TZ + r * math.sin(a)) for a in [-math.pi / 2 + (at + math.pi / 2) * k / 16 for k in range(1, 17)]]
    prism(bm, pts, x0, x1); bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    me = bpy.data.meshes.new('invert_' + tag); bm.to_mesh(me); bm.free(); me.materials.append(M['invert'])
    o = bpy.data.objects.new('invert_' + tag, me); bpy.context.scene.collection.objects.link(o); objs.append(o)
    S = Acc('slabs_' + tag, M['slab']); R = Acc('rails_' + tag, M['rail']); K = Acc('fasten_' + tag, M['fasten'])
    W = Acc('walkway_' + tag, M['invert']); C = Acc('trays_' + tag, M['tray']); Lt = Acc('fittings_' + tag, M['led'])
    CA = Acc('catenary_' + tag, M['wire'])
    xs = 5.0 * math.ceil(x0 / 5.0)
    while xs + 5.0 <= x1 + 0.01:
        S.box((4.93, 2.34, 0.24), (xs + 2.5, TY, FLOOR - 0.32)); xs += 5.0
    for s in (-1, 1):
        yr = TY + s * 0.7525
        R.box((L, 0.15, 0.025), (xm, yr, FLOOR - 0.1575)); R.box((L, 0.018, 0.1), (xm, yr, FLOOR - 0.095)); R.box((L, 0.072, 0.045), (xm, yr, FLOOR - 0.0225))
        xk = 0.625 * math.ceil(x0 / 0.625)
        while xk <= x1:
            K.box((0.18, 0.34, 0.06), (xk, yr, FLOOR - 0.18)); xk += 0.625
    W.box((L, 0.75, FLOOR + 0.6 - TOP_INV), (xm, 4.775, (FLOOR + 0.6 + TOP_INV) / 2))
    C.box((L, 0.32, 0.18), (xm, 4.85, FLOOR + 0.69)); C.box((L, 0.25, 0.08), (xm, 5.68, TZ - 1.6)); C.box((L, 0.25, 0.08), (xm, 5.82, TZ - 0.45))
    xf = 8.0 * math.ceil(x0 / 8.0)
    while xf <= x1:
        Lt.box((1.4, 0.08, 0.14), (xf, 5.86, TZ - 1.0)); Lt.box((0.9, 0.08, 0.12), (xf + 4.0, 5.1, TZ + 3.0)); xf += 8.0
    zc_, zm_ = FLOOR + 5.0, FLOOR + 6.1
    CA.cyl(0.014, L, (xm, TY, zc_), zrot_to((1, 0, 0)), 8); CA.cyl(0.012, L, (xm, TY, zm_), zrot_to((1, 0, 0)), 8)
    xd = 5.0 * math.ceil(x0 / 5.0)
    while xd <= x1:
        CA.box((0.012, 0.012, zm_ - zc_), (xd + 2.5, TY, (zc_ + zm_) / 2))
        if int(round(xd)) % 50 == 0:                                              # cantilever bracket every 50 m
            CA.box((0.09, 5.5 - TY + 0.3, 0.09), (xd, (5.5 + TY - 0.3) / 2, zm_ + 0.2)); CA.beam((xd, 5.6, zm_ - 1.2), (xd, TY + 0.6, zm_ + 0.2), 0.07)
            CA.cyl(0.07, 0.5, (xd, TY, zm_ + 0.0), None, 10)
        xd += 5.0
    for A in (S, R, K, W, C, Lt, CA): objs.append(A.build())
    return objs


# ---------------------------------------------------------------- the train (E5-style: long nose, white, teal-green stripe)
def prof(e, n=36):
    P = []
    for i in range(n):
        a = i * math.tau / n; c, s = math.cos(a), math.sin(a)
        P.append((math.copysign(abs(c) ** (2 / e), c), math.copysign(abs(s) ** (2 / e), s)))
    return P


def loft(name, rings, m, n=36):
    bm = bmesh.new(); rv = []
    for x, zc, hw, hh, e in rings:
        rv.append([bm.verts.new((x, px * hw, zc + pz * hh)) for px, pz in prof(e, n)])
    for a, b in zip(rv[:-1], rv[1:]):
        for i in range(n): bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    bm.faces.new(rv[0][::-1]); bm.faces.new(rv[-1])
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    me.materials.append(m)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    return o


def nose_sec(u):
    zb = -HH + 0.3 * u ** 1.6
    zt = HH - 1.75 * ss(0, 0.62, u) - 0.45 * ss(0.62, 1.0, u)
    f = max(0.05, 1 - u ** 7) ** 0.5
    return (zt + zb) / 2, HW * max(0.03, 1 - u ** 2.4) ** 0.5, max(0.04, (zt - zb) / 2 * f), 4.5 - 2.3 * u, zt


def car_layout():
    Ls = [27.0, 25.0, 25.0, 25.0, 25.0, 27.0]; kinds = ['tail', 'mid', 'mid', 'mid', 'mid', 'lead']
    x = -(sum(Ls) + 0.9 * 5) / 2; out = []
    for L_, k in zip(Ls, kinds):
        out.append((x + L_ / 2, L_, k)); x += L_ + 0.9
    return out


def car_rings(cx, L, kind):
    x0, x1 = cx - L / 2, cx + L / 2; NL = 15.0
    b0 = x0 + NL if kind == 'tail' else x0; b1 = x1 - NL if kind == 'lead' else x1
    R = []
    if kind != 'tail': R += [(b0, 0, HW * 0.95, HH * 0.96, 4.5), (b0 + 0.25, 0, HW, HH, 4.5)]
    R += [(b0 + (b1 - b0) * k / 5, 0, HW, HH, 4.5) for k in range(1 if kind != 'tail' else 0, 5 if kind != 'lead' else 6)]
    if kind != 'lead': R += [(b1 - 0.25, 0, HW, HH, 4.5), (b1, 0, HW * 0.95, HH * 0.96, 4.5)]
    nose = []
    for k in range(1, 27):
        u = 1 - (1 - k / 26) ** 1.6; zc, hw, hh, e, _ = nose_sec(u)
        nose.append((u, zc, hw, hh, e))
    if kind == 'lead': R += [(b1 + NL * u, zc, hw, hh, e) for u, zc, hw, hh, e in nose]
    if kind == 'tail': R = [(b0 - NL * u, zc, hw, hh, e) for u, zc, hw, hh, e in reversed(nose)] + R
    return sorted(R, key=lambda r: r[0]), b0, b1


def body_material():
    m = mat('e5_body', (0.82, 0.83, 0.82), 0.22, 0.05); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    try: b.inputs['Coat Weight'].default_value = 0.4
    except Exception: pass
    tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sp.inputs['Vector'])
    def band(z0, z1):
        g = nt.nodes.new('ShaderNodeMath'); g.operation = 'GREATER_THAN'; g.inputs[1].default_value = z0
        l = nt.nodes.new('ShaderNodeMath'); l.operation = 'LESS_THAN'; l.inputs[1].default_value = z1
        m_ = nt.nodes.new('ShaderNodeMath'); m_.operation = 'MULTIPLY'
        nt.links.new(sp.outputs['Z'], g.inputs[0]); nt.links.new(sp.outputs['Z'], l.inputs[0])
        nt.links.new(g.outputs[0], m_.inputs[0]); nt.links.new(l.outputs[0], m_.inputs[1]); return m_
    a1 = band(-0.43, -0.27); a2 = band(-0.53, -0.495)
    mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; nt.links.new(a1.outputs[0], mx.inputs[0]); nt.links.new(a2.outputs[0], mx.inputs[1])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    sA = [x for x in mix.inputs if x.name == 'A' and x.type == 'RGBA'][0]; sB = [x for x in mix.inputs if x.name == 'B' and x.type == 'RGBA'][0]
    sA.default_value = (0.82, 0.83, 0.82, 1); sB.default_value = (0.0, 0.36, 0.30, 1)
    nt.links.new(mx.outputs[0], mix.inputs['Factor']); nt.links.new([x for x in mix.outputs if x.type == 'RGBA'][0], b.inputs['Base Color'])
    m.use_backface_culling = True                     # see out of the shell from inside the coach
    return m


def ell(A, r, loc, scale, rot=None, sub=2):
    res = bmesh.ops.create_icosphere(A.bm, subdivisions=sub, radius=r)
    Rm = rot.to_matrix().to_4x4() if rot else Matrix.Identity(4)
    bmesh.ops.transform(A.bm, matrix=Matrix.Translation(Vector(loc)) @ Rm @ Matrix.Diagonal((*scale, 1.0)), verts=res['verts'])


def skin(obj, arm, bone):
    obj.parent = arm
    vg = obj.vertex_groups.new(name=bone); vg.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
    md = obj.modifiers.new('Armature', 'ARMATURE'); md.object = arm


def build_train():
    sc = bpy.context.scene; cars = car_layout()
    bpy.ops.object.armature_add(location=(0, TY, ZC)); arm = bpy.context.active_object; arm.name = 'train'
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones; eb.remove(eb[0])
    for i, (cx, L, k) in enumerate(cars):
        b = eb.new(f'car{i}'); b.head = (cx, 0, 0); b.tail = (cx, 1, 0)
    bpy.ops.object.mode_set(mode='OBJECT')
    body = body_material()
    glass = mat('e5_glass', (0.015, 0.02, 0.025), 0.06, 0.3, (1.0, 0.86, 0.62), 0.12)
    dark = mat('e5_dark', (0.03, 0.03, 0.035), 0.6, 0.3); under = noisy(mat('e5_under', (0.16, 0.16, 0.17), 0.6, 0.5), 3.0, 0.7, 0.1)
    steel = mat('e5_steel', (0.45, 0.45, 0.47), 0.3, 1.0); canopy = mat('e5_canopy', (0.01, 0.012, 0.015), 0.05, 0.2)
    lamp = mat('e5_headlight', (1, 1, 1), 0.2, 0, (1.0, 0.95, 0.85), 3.5)
    gang = mat('e5_gangway', (0.05, 0.05, 0.055), 0.8)
    for i, (cx, L, kind) in enumerate(cars):
        rings, b0, b1 = car_rings(cx, L, kind)
        skin(loft(f'car{i}_body', rings, body), arm, f'car{i}')
        Wn = Acc(f'car{i}_windows', glass); D = Acc(f'car{i}_doors', dark); U = Acc(f'car{i}_under', under); Bg = Acc(f'car{i}_bogies', steel)
        if kind == 'mid': wx = [cx + 9.0 - k * 1.04 for k in range(19)]
        elif kind == 'lead': wx = [b1 - 1.3 - k * 1.04 for k in range(9)]
        else: wx = [b0 + 1.3 + k * 1.04 for k in range(9)]
        for x in wx:
            for s in (-1, 1): Wn.box((0.75, 0.04, 0.62), (x, s * (HW - 0.005), 0.125))
        dxs = {'mid': (cx - 11.3, cx + 11.3), 'lead': (cx - 12.2,), 'tail': (cx + 12.2,)}[kind]
        for dx in dxs:                                                            # door outlines + door window
            for s in (-1, 1):
                y = s * (HW + 0.004)
                for a, bb in (((dx - 0.5, -1.25), (dx - 0.5, 0.75)), ((dx + 0.5, -1.25), (dx + 0.5, 0.75)), ((dx - 0.5, 0.75), (dx + 0.5, 0.75))):
                    D.box((abs(bb[0] - a[0]) + 0.03, 0.02, abs(bb[1] - a[1]) + 0.03), ((a[0] + bb[0]) / 2, y, (a[1] + bb[1]) / 2))
                Wn.box((0.32, 0.04, 0.5), (dx, s * (HW - 0.005), 0.2))
        bx = (cx - 8.75, cx + 8.75) if kind == 'mid' else ((cx - 9.75, cx + 4.0) if kind == 'lead' else (cx - 4.0, cx + 9.75))
        for bxx in bx:                                                            # bogies: frame, 4 wheels, axles, dampers
            Bg.box((3.2, 2.1, 0.3), (bxx, 0, -1.62))
            for ax in (-1.25, 1.25):
                for s in (-1, 1): Bg.cyl(0.43, 0.14, (bxx + ax, s * 0.75, -1.845), zrot_to((0, 1, 0)), 24)
                Bg.cyl(0.08, 1.7, (bxx + ax, 0, -1.845), zrot_to((0, 1, 0)), 10)
            for s in (-1, 1): Bg.beam((bxx - 0.9, s * 1.05, -1.55), (bxx + 0.9, s * 1.05, -1.3), 0.12)
        segs = [b0 + (0.6 if kind != 'tail' else 3.0)] + [v for bxx in bx for v in (bxx - 1.95, bxx + 1.95)] + [b1 - (0.6 if kind != 'lead' else 3.0)]
        for a, bb in zip(segs[0::2], segs[1::2]):                                 # skirts + underfloor boxes between bogies
            if bb - a > 0.3:
                U.box((bb - a, 2.9, 0.42), ((a + bb) / 2, 0, -1.58))
                for s in (-1, 1): U.box((bb - a, 0.05, 0.45), ((a + bb) / 2, s * (HW - 0.06), -1.56))
        if kind in ('lead', 'tail'):                                              # cab canopy blister + headlights on the nose
            sg = 1 if kind == 'lead' else -1; root_x = b1 if kind == 'lead' else b0
            zt3 = nose_sec(0.3)[4]; slope = (nose_sec(0.32)[4] - nose_sec(0.28)[4]) / (0.04 * 15.0)
            Cn = Acc(f'car{i}_canopy', canopy)
            ell(Cn, 1.0, (root_x + sg * 4.6, 0, zt3 - 0.02), (2.5, 0.88, 0.40), Quaternion((0, 1, 0), sg * math.atan(-slope)), 3)
            skin(Cn.build(), arm, f'car{i}')
            Hl = Acc(f'car{i}_lights', lamp)
            zc, hw, hh, e, _ = nose_sec(0.8)
            for s in (-1, 1): ell(Hl, 0.11, (root_x + sg * 12.0, s * hw * 0.96, zc + hh * 0.1), (2.4, 0.8, 0.7))
            skin(Hl.build(), arm, f'car{i}')
        for A in (Wn, D, U, Bg): skin(A.build(), arm, f'car{i}')
        if i < len(cars) - 1:
            e1 = cx + L / 2; skin(loft(f'gang{i}', [(e1 - 0.1, 0, HW * 0.86, HH * 0.9, 4.0), (e1 + 1.0, 0, HW * 0.86, HH * 0.9, 4.0)], gang, 28), arm, f'car{i}')
    cx3 = cars[3][0]; P = Acc('pantograph', steel); x = cx3 + 6.0                 # single-arm pantograph on car 3
    P.box((1.8, 1.3, 0.14), (x, 0, HH + 0.08)); P.beam((x - 0.6, 0, HH + 0.15), (x + 0.5, 0, 2.15), 0.07); P.beam((x + 0.5, 0, 2.15), (x - 0.4, 0, 2.66), 0.05)
    P.box((0.22, 1.9, 0.06), (x - 0.4, 0, 2.70))
    for s in (-1, 1): P.cyl(0.07, 0.3, (x + s * 0.6, s * 0.4, HH + 0.25), None, 10)
    skin(P.build(), arm, 'car3')
    pb = arm.pose.bones
    for b in pb: b.rotation_mode = 'XYZ'
    for i in range(len(cars)):                                                    # articulated sway (car 2 = the interior car, held)
        if i == 2: continue
        for k in range(0, F(T_END) + 6, 6):
            ph = k / 6.0 * 0.9 + i * 1.3
            pb[f'car{i}'].location = (0, 0, 0.01 * math.sin(ph * 1.7)); pb[f'car{i}'].rotation_euler = (0.0014 * math.sin(ph), 0, 0.0018 * math.sin(ph * 0.8 + i))
            pb[f'car{i}'].keyframe_insert('location', index=2, frame=k + 1); pb[f'car{i}'].keyframe_insert('rotation_euler', frame=k + 1)
    for fc in fcurves_of(arm):
        for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'
    return arm, cars


def interior(arm, cx):
    """Coach interior for car 2 (2+3 seating, window openings on both walls, ceiling light strips), train-local coords."""
    fz = -1.075; wall = noisy(mat('int_wall', (0.6, 0.58, 0.54), 0.6), 3.0, 0.9, 0.05)
    seatm = noisy(mat('int_seat', (0.06, 0.13, 0.32), 0.85), 40.0, 0.7, 0.3); floor_m = noisy(mat('int_floor', (0.12, 0.11, 0.10), 0.8), 20.0, 0.7, 0.2)
    grey = mat('int_grey', (0.12, 0.12, 0.13), 0.5, 0.4); strip = mat('int_strip', (1, 1, 1), 0.3, 0, (1.0, 0.95, 0.85), 2.5)
    Wl, St, Fl, Gr, Ls = Acc('int_walls', wall), Acc('int_seats', seatm), Acc('int_floor', floor_m), Acc('int_trim', grey), Acc('int_strips', strip)
    gz = mat('int_glass', (0.01, 0.012, 0.015), 0.04, 0.0); gz.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.55
    try: gz.surface_render_method = 'BLENDED'
    except Exception: pass
    Gz = Acc('int_panes', gz)
    xa, xb_ = cx - 11.3, cx + 11.3; L = xb_ - xa; xm = (xa + xb_) / 2
    Fl.box((L, 3.0, 0.05), (xm, 0, fz - 0.025)); Wl.box((L, 3.0, 0.05), (xm, 0, 1.08))
    for s in (-1, 1): Ls.box((L - 1.0, 0.18, 0.02), (xm, s * 0.55, 1.05))
    wx = [cx + 9.0 - k * 1.04 for k in range(19)]
    for s in (-1, 1):
        y = s * 1.5
        Wl.box((L, 0.04, -0.2 - fz), (xm, y, (fz - 0.2) / 2)); Wl.box((L, 0.04, 1.08 - 0.45), (xm, y, (1.08 + 0.45) / 2))
        edges = [xa] + [v for x in sorted(wx) for v in (x - 0.375, x + 0.375)] + [xb_]
        for a, b in zip(edges[0::2], edges[1::2]):
            if b - a > 0.01: Wl.box((b - a, 0.04, 0.65), ((a + b) / 2, y, 0.125))
        Gr.box((L, 0.36, 0.03), (xm, s * 1.3, 0.62))                             # luggage racks
        for x in wx: Gz.box((0.75, 0.01, 0.65), (x, s * 1.53, 0.125))                # tinted panes: a dark window
    Wl.box((0.05, 3.0, 2.15), (xa, 0, (fz + 1.08) / 2)); Gr.box((0.06, 0.9, 1.9), (xa + 0.02, 0.2, fz + 0.95))
    seats = []
    for k in range(18):
        xb = cx + 8.75 - k * 1.04
        for yc in (0.70, 1.18, -0.30, -0.76, -1.22):
            St.box((0.5, 0.44, 0.13), (xb + 0.30, yc, fz + 0.40))
            St.box((0.1, 0.44, 0.72), (xb + 0.08, yc, fz + 0.86), Quaternion((0, 1, 0), math.radians(-12)))
            St.box((0.1, 0.30, 0.18), (xb - 0.0, yc, fz + 1.30), Quaternion((0, 1, 0), math.radians(-12)))
            Gr.box((0.3, 0.36, 0.33), (xb + 0.3, yc, fz + 0.17))
            seats.append((xb, yc))
        for yc in (0.46, 1.42, -0.06, -1.46): Gr.box((0.45, 0.05, 0.06), (xb + 0.28, yc, fz + 0.64))
    for A in (Wl, St, Fl, Gr, Ls, Gz): A.build(arm)
    ld = bpy.data.lights.new('coach_light', 'AREA'); ld.shape = 'RECTANGLE'; ld.size = L - 1.0; ld.size_y = 2.2
    ld.energy = 320; ld.color = (1.0, 0.93, 0.82)
    lo = bpy.data.objects.new('coach_light', ld); bpy.context.scene.collection.objects.link(lo); lo.parent = arm; lo.location = (xm, 0, 1.0)
    return fz


# ---------------------------------------------------------------- seated passenger (library Worker via rigged_worker)
def bend(arm, pbone, child, want, ang):
    base = list(pbone.rotation_euler); bpy.context.view_layer.update(); p0 = arm.matrix_world @ child.head; best = (-1e9, base)
    for ax in range(3):
        for sg in (1, -1):
            e = base[:]; e[ax] += sg * ang; pbone.rotation_euler = e; bpy.context.view_layer.update()
            sc_ = ((arm.matrix_world @ child.head) - p0).dot(want)
            if sc_ > best[0]: best = (sc_, e[:])
    pbone.rotation_euler = best[1]; bpy.context.view_layer.update()
    return best


def passenger(train, cx, fz):
    rep = {}
    xb = cx + 8.75; yc = 1.18                                                     # first row, window seat on the +y side
    floor_w = ZC + fz
    root = rigged_worker(xb + 0.3, TY + yc, floor_w, math.pi / 2, seed=3, fps=FPS, frames=F(T_END))
    meshes = [o for o in [root] + list(root.children_recursive) if o.type == 'MESH']
    rep['meshes'] = [o.name for o in meshes][:20]
    for o in meshes:                                                              # passenger clothes, no site gear
        n = o.name.lower(); col = None
        if 'cap' in n or 'helmet' in n or 'glove' in n: o.hide_render = True; continue
        if 'jacket' in n or 'vest' in n: col = (0.05, 0.06, 0.08)
        elif 'pant' in n: col = (0.13, 0.13, 0.14)
        elif 'scrub' in n or 'shirt' in n: col = (0.48, 0.56, 0.66)
        if col: o.data.materials.clear(); o.data.materials.append(mat('pax_' + n, col, 0.75))
    parm = [o for o in root.children_recursive if o.type == 'ARMATURE'][0]
    parm.animation_data_clear()
    pb = parm.pose.bones
    def find(side, key):
        c = [b for b in pb if key in b.name.lower() and (b.name.lower().startswith(side + '_') or ('_' + side + '_') in b.name.lower()) and 'twist' not in b.name.lower()]
        return min(c, key=lambda b: len(b.name)) if c else None
    fwd, up = Vector((1, 0, 0)), Vector((0, 0, 1))
    for side in ('l', 'r'):
        th, ca, ft = find(side, 'thigh'), find(side, 'calf'), find(side, 'foot')
        ua, fa, hd = find(side, 'upperarm'), find(side, 'forearm'), find(side, 'hand')
        rep[side] = [b.name if b else None for b in (th, ca, ft, ua, fa, hd)]
        if th and ca: bend(parm, th, ca, fwd, math.radians(84))
        if ca and ft: bend(parm, ca, ft, -up, math.radians(82))
        inward = Vector((0, -1 if side == 'l' else 1, 0))
        if ua and fa: bend(parm, ua, fa, -up, math.radians(14)); bend(parm, ua, fa, fwd, math.radians(18))
        if fa and hd: bend(parm, fa, hd, fwd + inward * 1.2, math.radians(55))
    bpy.context.view_layer.update()
    th = [b for b in (find('l', 'thigh'), find('r', 'thigh')) if b]
    if th:
        hip = sum((parm.matrix_world @ b.head for b in th), Vector()) / len(th)
        root.location += Vector((xb + 0.25, TY + yc, floor_w + 0.57)) - hip
        bpy.context.view_layer.update()
    ft = [b for b in (find('l', 'foot'), find('r', 'foot')) if b]
    if ft: rep['foot_above_floor'] = round(min((parm.matrix_world @ b.head).z for b in ft) - floor_w, 3)
    hb = pb.get('Head')
    sp = pb.get('Spine01')
    for k in range(0, F(T_END) + 15, 15):                                         # calm idle: breathing + a slow look to the window
        t = k / FPS
        if sp: sp.rotation_euler = (0.012 * math.sin(t * math.tau / 4.2), 0, 0); sp.keyframe_insert('rotation_euler', frame=k + 1)
        if hb: hb.rotation_euler = (0, 0.28 + 0.05 * math.sin(t * math.tau / 9.0), 0); hb.keyframe_insert('rotation_euler', frame=k + 1)
    bpy.context.view_layer.update()
    head = parm.matrix_world @ hb.head if hb else Vector((xb + 0.25, TY + yc, floor_w + 1.2))
    root.parent = train; root.matrix_parent_inverse = train.matrix_world.inverted()
    return head, parm, rep


# ---------------------------------------------------------------- world: ch3 teal under the water, sunset once we surface
def world():
    sc = bpy.context.scene; w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    N = nt.nodes.new; Lk = nt.links.new
    tc = N('ShaderNodeTexCoord'); nv = N('ShaderNodeVectorMath'); nv.operation = 'NORMALIZE'; Lk(tc.outputs['Generated'], nv.inputs[0])
    sep = N('ShaderNodeSeparateXYZ'); Lk(nv.outputs['Vector'], sep.inputs['Vector'])
    mA = N('ShaderNodeMapRange'); mA.inputs['From Min'].default_value = -0.6; mA.inputs['From Max'].default_value = 0.7; Lk(sep.outputs['Z'], mA.inputs['Value'])
    cA = N('ShaderNodeValToRGB'); cA.color_ramp.elements[0].color = (0.004, 0.03, 0.045, 1); cA.color_ramp.elements[1].color = (0.03, 0.2, 0.26, 1)
    Lk(mA.outputs['Result'], cA.inputs['Fac'])
    mB = N('ShaderNodeMapRange'); mB.inputs['From Min'].default_value = -1.0; mB.inputs['From Max'].default_value = 1.0; Lk(sep.outputs['Z'], mB.inputs['Value'])
    cB = N('ShaderNodeValToRGB'); el = cB.color_ramp.elements
    el[0].position = 0.0; el[0].color = (0.003, 0.02, 0.03, 1); el[1].position = 1.0; el[1].color = (0.025, 0.05, 0.14, 1)
    for p, c in ((0.495, (0.03, 0.08, 0.1)), (0.5, (1.0, 0.42, 0.12)), (0.515, (0.85, 0.36, 0.2)), (0.56, (0.32, 0.2, 0.3)), (0.7, (0.08, 0.1, 0.22))):
        e = el.new(p); e.color = (*c, 1)
    Lk(mB.outputs['Result'], cB.inputs['Fac'])
    S = Vector((0.1, 1.0, 0.035)).normalized()
    dot = N('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'; dot.inputs[1].default_value = S; Lk(nv.outputs['Vector'], dot.inputs[0])
    gl = N('ShaderNodeMapRange'); gl.inputs['From Min'].default_value = 0.94; gl.inputs['From Max'].default_value = 1.0; Lk(dot.outputs['Value'], gl.inputs['Value'])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 3.0; Lk(gl.outputs['Result'], pw.inputs[0])
    dk = N('ShaderNodeMath'); dk.operation = 'GREATER_THAN'; dk.inputs[1].default_value = 0.9994; Lk(dot.outputs['Value'], dk.inputs[0])
    def mix(blend, fac_src, a_src, b_val):
        m = N('ShaderNodeMix'); m.data_type = 'RGBA'; m.blend_type = blend
        sA = [x for x in m.inputs if x.name == 'A' and x.type == 'RGBA'][0]; sB = [x for x in m.inputs if x.name == 'B' and x.type == 'RGBA'][0]
        Lk(a_src, sA)
        if isinstance(b_val, tuple): sB.default_value = (*b_val, 1)
        else: Lk(b_val, sB)
        if fac_src is not None: Lk(fac_src, m.inputs['Factor'])
        return m, [x for x in m.outputs if x.type == 'RGBA'][0]
    _, g1 = mix('ADD', pw.outputs[0], cB.outputs['Color'], (1.0, 0.5, 0.18))
    _, g2 = mix('ADD', dk.outputs[0], g1, (1.0, 0.8, 0.5))
    mAB, out_ = mix('MIX', None, cA.outputs['Color'], g2)
    bg = N('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.9; ot = N('ShaderNodeOutputWorld')
    Lk(out_, bg.inputs['Color']); Lk(bg.outputs['Background'], ot.inputs['Surface'])
    fs = mAB.inputs['Factor']; idx = list(mAB.inputs).index(fs); dp = f'nodes["{mAB.name}"].inputs[{idx}].default_value'
    fs.default_value = 0.0; nt.keyframe_insert(data_path=dp, frame=F(25.7))
    fs.default_value = 1.0; nt.keyframe_insert(data_path=dp, frame=F(26.5))
    bg.inputs['Strength'].default_value = 0.9
    result['world_fcurves'] = [(fc.data_path, [round(k.co[1], 3) for k in fc.keyframe_points]) for fc in fcurves_of(nt)]


def water():
    ws = mat('water_section', (0.02, 0.16, 0.2), 0.3, 0.0); nt = ws.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sp.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -6.0; mr.inputs['From Max'].default_value = 0.0; nt.links.new(sp.outputs['Z'], mr.inputs['Value'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.006, 0.05, 0.065, 1); cr.color_ramp.elements[1].color = (0.04, 0.24, 0.28, 1)
    nt.links.new(mr.outputs['Result'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color']); nt.links.new(cr.outputs['Color'], b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = 0.7
    S = Acc('water_section', ws); S.box((2 * XE, 300, 5.97), (0, 150, -6 + 5.97 / 2)); S.build()
    wm = mat('water_surface', (0.008, 0.03, 0.04), 0.1, 0.0); nt = wm.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'
    nz.inputs['Scale'].default_value = 0.6; nz.inputs['Detail'].default_value = 8
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.45; bp.inputs['Distance'].default_value = 0.3
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector']); nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    wi = nz.inputs['W']; wi.default_value = 0.0; wi.keyframe_insert('default_value', frame=1); wi.default_value = 2.0; wi.keyframe_insert('default_value', frame=F(T_END))
    bm = bmesh.new(); v = [bm.verts.new(p) for p in ((-3000, 0, 0), (3000, 0, 0), (3000, 3000, 0), (-3000, 3000, 0))]; bm.faces.new(v)
    me = bpy.data.meshes.new('water_surface'); bm.to_mesh(me); bm.free(); me.materials.append(wm)
    o = bpy.data.objects.new('water_surface', me); bpy.context.scene.collection.objects.link(o)


# ---------------------------------------------------------------- scene
def build():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    L = [('seabed_mud', (0.05, 0.04, 0.03), -6, -9, False), ('soft_clay', (0.34, 0.22, 0.12), -9, -20, False), ('stiff_clay', (0.52, 0.36, 0.2), -20, -30, True),
         ('weathered_rock', (0.24, 0.22, 0.2), -30, -46, True), ('basalt', (0.09, 0.1, 0.13), -46, -90, False)]
    seam = Acc('layer_seams', mat('seam', (0.03, 0.03, 0.035), 0.9)); part, full = [], []
    for nm, c, z0, z1, cut in L:
        if cut:
            part.append(soil_layer(nm + '_bored', c, z0, z1, [(-XE - 20, -14.2), (14.2, XE + 20)]))
            full.append(soil_layer(nm + '_done', c, z0, z1, [(-XE - 20, XE + 20)]))
        else: soil_layer(nm, c, z0, z1, [])
        seam.box((2 * XE, 0.12, 0.35), (0, -0.04, z0))
    seam.build(); water()
    lm = noisy(mat('lining', (0.47, 0.46, 0.43), 0.8), 2.5, 0.75, 0.15); gm = mat('grout', (0.035, 0.035, 0.04), 0.9)
    M = {'invert': noisy(mat('invert', (0.36, 0.35, 0.33), 0.85), 3.0, 0.7, 0.2), 'slab': noisy(mat('slab', (0.42, 0.41, 0.39), 0.75), 4.0, 0.7, 0.2),
         'rail': mat('rail', (0.5, 0.5, 0.52), 0.25, 1.0), 'fasten': mat('fasten', (0.08, 0.08, 0.09), 0.5, 0.6), 'tray': mat('tray', (0.2, 0.2, 0.21), 0.5, 0.7),
         'led': mat('led', (1, 1, 1), 0.3, 0, (1.0, 0.9, 0.75), 4.0), 'wire': mat('wire', (0.35, 0.2, 0.1), 0.35, 1.0)}
    mid = lining('lining_mid', -32, 32, lm, gm) + dressing('mid', -60, 60, M)
    lining('lining_w', -XE, -32, lm, gm); lining('lining_e', 32, XE, lm, gm); dressing('w', -XE, -60, M); dressing('e', 60, XE, M)
    tbms = []
    for nm, x0, x1, rot in (('tbmA', -16.2, -15.0, (0, math.pi / 2, 0)), ('tbmB', 16.2, 15.0, (0, math.pi / 2, math.pi))):
        root, head = build_tbm(nm, gantries=2); root.rotation_euler = rot
        for t, x in ((0.0, x0), (T_SWAP, x1)):
            root.location = (x, 0, TZ); root.keyframe_insert('location', frame=F(t))
        for t, a in ((0.0, 0.0), (T_SWAP, 110.0)):
            head.rotation_euler = (0, 0, math.radians(a)); head.keyframe_insert('rotation_euler', frame=F(t))
        for fc in fcurves_of(head):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'                # constant cutterhead rpm (intended)
        tbms.append(root)
        for xl in (x0 * 1.4, x0 * 2.6):                                           # work lamps on the open (section) side
            bpy.ops.object.light_add(type='POINT', location=(xl, -2.0, TZ + 3.5)); l = bpy.context.active_object
            l.data.energy = 1800; l.data.color = (1.0, 0.82, 0.55); l.data.shadow_soft_size = 2.0
    tb_objs = [o for r in tbms for o in [r] + list(r.children_recursive)]
    show_keys(tb_objs + part, off=(T_SWAP,)); show_keys(mid + full, on=(T_SWAP,))
    for x in range(int(-XE) + 20, int(XE), 40):
        bpy.ops.object.light_add(type='POINT', location=(x, 4.0, TZ + 3.0)); l = bpy.context.active_object
        l.data.energy = 900; l.data.color = (1.0, 0.86, 0.62); l.data.shadow_soft_size = 1.5
    bpy.ops.object.light_add(type='AREA', location=(0, -80, -25), rotation=(math.radians(90), 0, 0)); fill = bpy.context.active_object
    fill.data.energy = 160000; fill.data.size = 260; fill.data.color = (0.8, 0.92, 1.0)
    train, cars = build_train()
    cx2 = cars[2][0]; fz = interior(train, cx2)
    head, parm, rep = passenger(train, cx2, fz)
    show_keys([bpy.data.objects['car2_windows']], off=(19.3,), on=(24.75,))
    for t in (0.0, T_END):
        train.location.x = X_tr(t); train.keyframe_insert('location', index=0, frame=F(t))
    for fc in fcurves_of(train):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'                    # constant 320 km/h (intended)
    world()                                                                        # after place_asset (it touched the world strength)
    return tbms, train, cars, head, parm, fill, rep


# ---------------------------------------------------------------- one continuous camera
def interp(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t <= t1:
            s = ss(t0, t1, t); return tuple(x + (y - x) * s for x, y in zip(a, b))
    return keys[-1][1]


def camera_path(head):
    hx, hy, hz = head.x, head.y, head.z
    W1 = [(0.0, (0, -82, -31, 0, 0, -34.5, 26)), (2.1, (0, -86, -30, 0, 0, -34, 26)), (3.9, (0, -112, -22, 0, 0, -27, 24)),
          (8.7, (4, -118, -21, 2, 0, -27, 24)), (11.0, (-92, -11, -36, -125, 3, -37, 24)), (12.6, (-94, -11.5, -36, -125, 3, -37, 24))]
    r0 = -94 - X_tr(12.6); l0 = -125 - X_tr(12.6)
    inside = (hx + 1.45, TY + 0.2, hz + 0.05, hx, hy + 0.05, hz - 0.12, 32)
    T = [(12.6, (r0, -11.5, -36, l0, 3, -37, 24)), (14.4, (24, -4.5, -36.0, 50, 2.4, -36.4, 26)), (19.0, (-6, -3.2, -35.9, 14, 2.4, -36.2, 26)),
         (19.75, (hx + 1.75, TY + 0.12, hz + 0.08, hx, hy + 0.05, hz - 0.12, 30)), (23.9, inside), (24.3, inside),
         (24.9, (hx - 1.0, -5.5, ZC + 0.8, hx + 3.0, TY, ZC + 0.2, 26))]
    xs = X_tr(25.1) + hx - 1.0

    def W2(t):
        s = ss(24.6, T_END, t)
        c = Vector((xs + 6 * s, -5.5 + 1.5 * s - 16 * math.sin(math.pi * s), (ZC + 0.8) + (4.0 - ZC - 0.8) * s))
        k = s ** 3
        l = Vector((c.x + 4 + 20 * math.sin(math.pi * s) + 32 * k, 2.4 + 397.6 * k, (c.z - 1) + (1.5 - (c.z - 1)) * k))
        return (*c, *l, 24 + 2 * s)

    def P(t):
        a = interp(W1, t); tr = interp(T, t); X = X_tr(t)
        b = (tr[0] + X, tr[1], tr[2], tr[3] + X, tr[4], tr[5], tr[6])
        w1 = ss(12.6, 14.4, t); p = tuple(x + (y - x) * w1 for x, y in zip(a, b))
        w2 = ss(24.6, 25.6, t); c = W2(t)
        return tuple(x + (y - x) * w2 for x, y in zip(p, c))
    return P


def build_camera(P, fill):
    sc = bpy.context.scene
    cam = make_camera('Cam', focal=24, clip=(0.1, 6000.0)); tg = bpy.data.objects.new('Cam_t', None); sc.collection.objects.link(tg)
    tc = cam.constraints.new('TRACK_TO'); tc.target = tg; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
    for f in range(1, F(T_END) + 2):                                              # sampled smooth path, one key per frame
        p = P((f - 1) / FPS)
        cam.location = p[:3]; cam.keyframe_insert('location', frame=f)
        tg.location = p[3:6]; tg.keyframe_insert('location', frame=f)
        cam.data.lens = p[6]; cam.data.keyframe_insert('lens', frame=f)
        fill.location.x = p[0]; fill.keyframe_insert('location', index=0, frame=f)
    for ob in (cam, tg, cam.data, fill):
        for fc in fcurves_of(ob):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'                # dense samples of an eased path (intended)
    sc.camera = cam
    return cam


def anchors(cam, pts):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; outd = {}
    for name, (fn, ts) in pts.items():
        outd[name] = []
        for t in ts:
            sc.frame_set(F(t)); p = fn(); v = world_to_camera_view(sc, cam, p)
            outd[name].append([round(t, 2), round(v.x, 3), round(1 - v.y, 3), round(v.z, 1)])
    return outd


def run(args):
    tbms, train, cars, head, parm, fill, rep = build()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, F(T_END) - 1, FPS
    cam = build_camera(camera_path(head), fill)
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 32
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, int(args.get('pct', 50))
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5      # constant, never keyed
    E = sc.eevee                                                                 # anti-flicker: no shadow-pool overflow, stable blur
    for k, v in (('motion_blur_max', 128), ('motion_blur_steps', 2), ('motion_blur_position', 'CENTER'), ('taa_render_samples', 64),
                 ('shadow_pool_size', '4096'), ('shadow_resolution_scale', 1.0), ('shadow_ray_count', 2), ('shadow_step_count', 8)):
        if hasattr(E, k):
            try: setattr(E, k, v)
            except Exception: pass
    for o in bpy.data.objects:                                                   # shadows only on the two key lights
        if o.type == 'LIGHT':
            if hasattr(o.data, 'use_shadow_jitter'): o.data.use_shadow_jitter = False
            o.data.use_shadow = o.name in ('coach_light', 'Area')
    hb = parm.pose.bones.get('Head')
    hw_ = lambda: parm.matrix_world @ hb.head if hb else head
    x2 = cars[2][0]; x3 = cars[3][0]
    result['passenger'] = rep
    result['worlds'] = [(w.name, [round(n.inputs['Strength'].default_value, 2) for n in w.node_tree.nodes if n.type == 'BACKGROUND']) for w in bpy.data.worlds if w.use_nodes]
    result['anchors'] = anchors(cam, {
        'tbmA_face': (lambda: tbms[0].matrix_world.translation + Vector((1.5, -3.0, 0)), (1.2, 3.6, 7.2)),
        'tbmB_face': (lambda: tbms[1].matrix_world.translation + Vector((-1.5, -3.0, 0)), (1.2, 3.6, 7.2)),
        'tbmA_tail_check': (lambda: Vector((-49.0, -6.0, TZ)), (10.6, 11.2, 11.9)),
        'tbmB_tail_check': (lambda: Vector((49.0, -6.0, TZ)), (10.6, 11.2, 11.9)),
        'train_nose': (lambda: Vector((train.location.x + NOSE - 3.0, TY - 1.2, ZC)), (11.9, 12.9)),
        'coaches': (lambda: Vector((train.location.x + x3, TY - HW, ZC)), (14.4, 16.5, 19.0)),
        'passenger_head': (hw_, (19.75, 21.5, 23.9)),
        'window': (lambda: Vector((train.location.x + head.x + 0.4, TY + 1.5, ZC + 0.12)), (21.5,)),
        'surface': (lambda: Vector((cam.matrix_world.translation.x + 40, 400, 0.5)), (27.4,)),
    })
    if args.get('mode', 'preview') == 'preview':
        for t in STILLS:
            sc.frame_set(F(t)); sc.render.filepath = f'{out}/t_{t:04.1f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'frames':                                             # flicker check: consecutive frames + mean luminance
        lum = {}
        for t0 in args.get('around', (12.0, 20.0)):
            for f in range(F(t0) - 4, F(t0) + 4):
                sc.frame_set(f); sc.render.filepath = f'{out}/f_{f:04d}.png'; bpy.ops.render.render(write_still=True)
                im = bpy.data.images.load(sc.render.filepath); px = im.pixels[:]; n = len(px) // 4
                lum[f] = round(sum(0.2126 * px[4 * i] + 0.7152 * px[4 * i + 1] + 0.0722 * px[4 * i + 2] for i in range(0, n, 7)) / (n / 7) * 255, 2)
                bpy.data.images.remove(im)
        result['lum'] = lum
    if args.get('mode') == 'anim':
        video_output(sc, out + '/ch7_finale.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


try:
    run(args)
except Exception:                                   # report instead of failing the job (failed runs pause the engine)
    import traceback; result['ok'] = False; result['error'] = traceback.format_exc()[-3000:]
