# Chapter 6 plate "The rock section (NATM)" (42.0 s, chapter t0 = global 233.903). Horseshoe drill-and-blast tunnel in wet
# basalt (12.6 m excavated). Face A: 3-boom jumbo drills, charges, blast, shotcrete robot, rock bolts. Adit (side tunnel)
# junction. Plan cutaway (roof hidden while the camera is above it) showing three lit faces A, B, C. Final blast at B,
# breakthrough into C (6 m pillar). One continuous camera. Runs after skilllib.py + bt_model.py. args: mode=preview|anim, pct.
import bpy, bmesh, math, random
from mathutils import Vector, Quaternion
FPS = 30
T_END = 42.0
F = lambda t: int(round(t * FPS)) + 1
ZC = 7.0                         # plan-section height of the cutaway
R, ZS, WB = 6.3, 4.6, 5.6        # main tunnel: crown radius / spring line / invert half-width
RA, ZSA, WBA = 4.2, 3.6, 3.8     # adit
XA0, XA1 = -60.0, -63.0          # face A before / after the blast
XB, XCF, XCE, YAE = 60.0, 66.0, 240.0, 200.0
T_BLA, T_BLB = 17.3, 38.7        # blasts
PATH = [
    (0.0, (-54.5, 4.4, 2.4), (-60.3, -2.2, 5.2), 30),
    (7.6, (-55.6, 3.9, 2.9), (-60.3, -2.2, 5.2), 30),
    (8.8, (-39.5, 1.6, 5.6), (-60.0, -1.2, 5.0), 24),
    (11.4, (-40.8, 1.5, 5.4), (-60.0, -1.2, 5.0), 24),
    (12.2, (-44.0, 4.6, 2.6), (-58.5, -1.0, 4.6), 30),
    (14.6, (-44.4, 4.5, 2.7), (-58.5, -1.0, 4.6), 30),
    (15.4, (-44.0, 3.4, 5.4), (-60.0, -2.0, 4.6), 26),
    (19.2, (-43.6, 3.4, 5.4), (-60.0, -2.0, 4.6), 26),
    (20.0, (-45.5, -4.3, 2.8), (-58.0, 1.2, 7.5), 26),
    (23.2, (-46.2, -4.2, 2.9), (-58.0, 1.2, 7.5), 26),
    (23.9, (-50.5, -1.5, 3.4), (-56.0, 3.5, 8.5), 28),
    (26.9, (-50.9, -1.4, 3.4), (-56.0, 3.5, 8.5), 28),
    (27.6, (-30.0, -4.6, 6.0), (-4.0, 4.0, 4.0), 26),
    (28.4, (-14.0, -4.0, 4.4), (0.4, 11.0, 3.2), 26),
    (31.9, (-13.2, -4.1, 4.3), (0.4, 11.0, 3.2), 26),
    (33.3, (2.0, -80.0, 80.0), (2.0, 2.0, 0.0), 24),
    (35.0, (4.0, -77.0, 77.0), (3.0, 2.0, 0.0), 24),
    (35.9, (38.0, -4.0, 15.0), (58.0, 0.0, 4.5), 26),
    (36.8, (44.0, -2.5, 4.6), (60.0, 1.4, 4.8), 28),
    (T_END, (46.2, -2.2, 4.7), (60.0, 1.6, 4.9), 28),
]
HIDE_MATS = []                   # materials of everything above the cutaway plane (alpha-keyed while the camera is above)


# ---------------------------------------------------------------- profiles
def resample(pts, step):
    P = [Vector(p) for p in pts] + [Vector(pts[0])]
    L = [0.0]
    for i in range(1, len(P)): L.append(L[-1] + (P[i] - P[i - 1]).length)
    n = max(8, int(round(L[-1] / step))); out = []; j = 0
    for k in range(n):
        s = L[-1] * k / n
        while L[j + 1] < s: j += 1
        f = (s - L[j]) / max(1e-9, L[j + 1] - L[j]); p = P[j].lerp(P[j + 1], f); out.append((p.x, p.y))
    return out


def _q(a, c, b, t): return (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t * t * b


def profile(Rr, zs, wb, step):
    """Horseshoe: semicircular crown + slightly bowed walls down to a flat invert. Closed loop of (lateral, z)."""
    pts = [(wb * i / 20, 0.0) for i in range(20)]
    a, c, b = Vector((wb, 0)), Vector((Rr - 0.02, zs * 0.45)), Vector((Rr, zs))
    pts += [tuple(_q(a, c, b, i / 30)) for i in range(30)]
    pts += [(Rr * math.cos(math.pi * i / 80), zs + Rr * math.sin(math.pi * i / 80)) for i in range(80)]
    a, c, b = Vector((-Rr, zs)), Vector((-Rr + 0.02, zs * 0.45)), Vector((-wb, 0))
    pts += [tuple(_q(a, c, b, i / 30)) for i in range(30)]
    pts += [(-wb + wb * i / 20, 0.0) for i in range(20)]
    return resample(pts, step)


def hw_fn(Rr, zs, wb):
    a, c, b = Vector((wb, 0)), Vector((Rr - 0.02, zs * 0.45)), Vector((Rr, zs))
    tab = [_q(a, c, b, i / 200) for i in range(201)]
    def hw(z):
        if z >= zs: return math.sqrt(max(0.0, Rr * Rr - (z - zs) ** 2))
        if z <= 0: return wb
        for i in range(200):
            if tab[i + 1].y >= z:
                f = (z - tab[i].y) / max(1e-9, tab[i + 1].y - tab[i].y); return tab[i].x + (tab[i + 1].x - tab[i].x) * f
        return Rr
    return hw


hwM, hwA = hw_fn(R, ZS, WB), hw_fn(RA, ZSA, WBA)


def inside_main(y, z, off):
    if z < off: return False
    if z <= ZS: return abs(y) < hwM(z) - off
    return y * y + (z - ZS) ** 2 < (R - off) ** 2


def rings(zones):
    out = []
    for a, b, st in zones:
        n = max(1, int(round((b - a) / st)))
        out += [a + (b - a) * k / n for k in range(n)]
    return out + [zones[-1][1]]


def tube(bm, prof, rr, place, keep, inner):
    m = len(prof); rows = [[bm.verts.new(place(s, u, v)) for (u, v) in prof] for s in rr]
    for i in range(len(rr) - 1):
        A, B = rows[i], rows[i + 1]
        for j in range(m):
            q = (A[j], A[(j + 1) % m], B[(j + 1) % m], B[j])
            c = (q[0].co + q[1].co + q[2].co + q[3].co) * 0.25
            if not keep(c): continue
            f = bm.faces.new(q); f.normal_update()
            if f.normal.dot(inner(c) - c) < 0: f.normal_flip()
            f.material_index = 1 if c.z > ZC else 0


def finish(bm, name, mats):
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    me.shade_smooth()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    return o


def tex(name, kind, size, **kw):
    t = bpy.data.textures.new(name, kind); t.noise_scale = size
    for k, v in kw.items(): setattr(t, k, v)
    return t


def disp(ob, t, strength, vg=None):
    m = ob.modifiers.new(t.name, 'DISPLACE'); m.texture = t; m.texture_coords = 'GLOBAL'; m.strength = strength; m.mid_level = 0.5
    m.direction = 'NORMAL'
    if vg: m.vertex_group = vg


# ---------------------------------------------------------------- materials
def rock_mat(name, shot=False, cull=True, hide=False):
    """Wet basalt: noise colour + voronoi fracture lines + wet (coat, low roughness) patches. shot=True adds the shotcrete
    mask (grey where x > T, T keyed; never in the fresh rock 52 < x < 74 at the B/C faces) and a muddy wet invert."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes.new; Lk = nt.links.new
    b = nt.nodes['Principled BSDF']
    def mr(v, a, bb, c=0.0, d=1.0):
        n = N('ShaderNodeMapRange'); n.inputs['From Min'].default_value = a; n.inputs['From Max'].default_value = bb
        n.inputs['To Min'].default_value = c; n.inputs['To Max'].default_value = d; Lk(v, n.inputs['Value']); return n.outputs['Result']
    def mth(op, x, y):
        n = N('ShaderNodeMath'); n.operation = op
        if isinstance(x, (int, float)): n.inputs[0].default_value = x
        else: Lk(x, n.inputs[0])
        if isinstance(y, (int, float)): n.inputs[1].default_value = y
        else: Lk(y, n.inputs[1])
        return n.outputs[0]
    def mix(fac, a, bb, rgba=True):
        n = N('ShaderNodeMix'); n.data_type = 'RGBA' if rgba else 'FLOAT'; t = 'RGBA' if rgba else 'VALUE'
        sA = [x for x in n.inputs if x.name == 'A' and x.type == t][0]; sB = [x for x in n.inputs if x.name == 'B' and x.type == t][0]
        Lk(fac, n.inputs['Factor'])
        for s, v in ((sA, a), (sB, bb)):
            if isinstance(v, (tuple, list)): s.default_value = (*v, 1) if rgba else v
            elif isinstance(v, (int, float)): s.default_value = v
            else: Lk(v, s)
        return [x for x in n.outputs if x.type == t][0]
    tc = N('ShaderNodeTexCoord')
    n1 = N('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 0.9; n1.inputs['Detail'].default_value = 12; n1.inputs['Roughness'].default_value = 0.62
    vo = N('ShaderNodeTexVoronoi'); vo.feature = 'DISTANCE_TO_EDGE'; vo.inputs['Scale'].default_value = 1.4
    n2 = N('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 0.35; n2.inputs['Detail'].default_value = 3
    for n in (n1, vo, n2): Lk(tc.outputs['Object'], n.inputs['Vector'])
    cr = N('ShaderNodeValToRGB'); e = cr.color_ramp.elements
    e[0].position, e[0].color = 0.3, (0.042, 0.041, 0.04, 1); e[1].position, e[1].color = 0.75, (0.085, 0.081, 0.075, 1)
    Lk(n1.outputs['Fac'], cr.inputs['Fac'])
    crack = mr(vo.outputs['Distance'], 0.0, 0.03, 0.82, 1.0)
    mul = N('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1.0
    Lk(cr.outputs['Color'], [x for x in mul.inputs if x.name == 'A' and x.type == 'RGBA'][0]); Lk(crack, [x for x in mul.inputs if x.name == 'B' and x.type == 'RGBA'][0])
    rockc = [x for x in mul.outputs if x.type == 'RGBA'][0]
    wet = mr(n2.outputs['Fac'], 0.42, 0.62)
    rough = mr(wet, 0.0, 1.0, 0.7, 0.45)
    coat = mth('MULTIPLY', wet, 0.0)
    col, rgh = rockc, rough
    nf = N('ShaderNodeTexNoise'); nf.inputs['Scale'].default_value = 14.0; nf.inputs['Detail'].default_value = 6; Lk(tc.outputs['Object'], nf.inputs['Vector'])
    nl = N('ShaderNodeTexNoise'); nl.inputs['Scale'].default_value = 0.12; Lk(tc.outputs['Object'], nl.inputs['Vector'])
    lv = N('ShaderNodeMix'); lv.data_type = 'RGBA'; lv.blend_type = 'MULTIPLY'; Lk(mr(nl.outputs['Fac'], 0.35, 0.65), lv.inputs['Factor'])
    Lk(rockc, [x for x in lv.inputs if x.name == 'A' and x.type == 'RGBA'][0]); [x for x in lv.inputs if x.name == 'B' and x.type == 'RGBA'][0].default_value = (0.86, 0.82, 0.76, 1)
    rockc = [x for x in lv.outputs if x.type == 'RGBA'][0]; col = rockc
    bmp = mth('ADD', mth('ADD', n1.outputs['Fac'], mth('MULTIPLY', crack, 0.15)), mth('MULTIPLY', nf.outputs['Fac'], 0.35))
    if shot:
        sep = N('ShaderNodeSeparateXYZ'); Lk(tc.outputs['Object'], sep.inputs[0])
        tv = N('ShaderNodeValue'); tv.name = 'T'; tv.outputs[0].default_value = -49.0
        d = mth('ADD', mth('SUBTRACT', sep.outputs['X'], tv.outputs[0]), mth('MULTIPLY', mth('SUBTRACT', n1.outputs['Fac'], 0.5), 1.6))
        s1 = mr(d, -0.2, 0.2)
        inB = mth('MULTIPLY', mr(sep.outputs['X'], 52.0, 53.0), mr(sep.outputs['X'], 73.0, 74.0, 1.0, 0.0))
        fl = mr(sep.outputs['Z'], 0.45, 0.2)
        sh = mth('MULTIPLY', mth('MULTIPLY', s1, mth('SUBTRACT', 1.0, inB)), mth('SUBTRACT', 1.0, fl))
        n3 = N('ShaderNodeTexNoise'); n3.inputs['Scale'].default_value = 5.0; n3.inputs['Detail'].default_value = 8; Lk(tc.outputs['Object'], n3.inputs['Vector'])
        sc = N('ShaderNodeValToRGB'); e = sc.color_ramp.elements
        e[0].color = (0.17, 0.17, 0.165, 1); e[1].color = (0.33, 0.325, 0.31, 1); Lk(n3.outputs['Fac'], sc.inputs['Fac'])
        col = mix(sh, rockc, sc.outputs['Color'])
        col = mix(fl, col, mix(wet, (0.075, 0.064, 0.052), (0.035, 0.03, 0.025)))
        rgh = mix(sh, rough, 0.85, False); rgh = mix(fl, rgh, mr(wet, 0.0, 1.0, 0.5, 0.06), False)
        coat = mth('MULTIPLY', coat, mth('SUBTRACT', 1.0, sh))
        bmp = mix(sh, bmp, mth('MULTIPLY', n3.outputs['Fac'], 0.5), False)
    Lk(col, b.inputs['Base Color']); Lk(rgh, b.inputs['Roughness'])
    try: Lk(coat, b.inputs['Coat Weight']); b.inputs['Coat Roughness'].default_value = 0.05
    except Exception: pass
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.6; bp.inputs['Distance'].default_value = 0.08
    Lk(bmp, bp.inputs['Height']); Lk(bp.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Specular IOR Level'].default_value = 0.3
    m.use_backface_culling = cull
    if hide: HIDE_MATS.append(m)
    return m


def hid(m):
    HIDE_MATS.append(m); return m


def puff_mat(name, col, dens, radial=True):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); pv = N('ShaderNodeVolumePrincipled'); tc = N('ShaderNodeTexCoord')
    ln = N('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; Lk(tc.outputs['Object'], ln.inputs[0])
    r1 = N('ShaderNodeMapRange'); r1.inputs['From Min'].default_value = 1.0; r1.inputs['From Max'].default_value = 0.25; Lk(ln.outputs['Value'], r1.inputs['Value'])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 5; Lk(tc.outputs['Object'], nz.inputs['Vector'])
    r2 = N('ShaderNodeMapRange'); r2.inputs['From Min'].default_value = 0.3; r2.inputs['From Max'].default_value = 0.68; Lk(nz.outputs['Fac'], r2.inputs['Value'])
    a = N('ShaderNodeMath'); a.operation = 'MULTIPLY'; Lk(r2.outputs['Result'], a.inputs[1])
    if radial: Lk(r1.outputs['Result'], a.inputs[0])
    else: a.inputs[0].default_value = 1.0
    if not radial: r2.inputs['From Min'].default_value = 0.05; r2.inputs['From Max'].default_value = 0.55; r2.inputs['To Min'].default_value = 0.35
    c = N('ShaderNodeMath'); c.operation = 'MULTIPLY'; c.name = 'D'; Lk(a.outputs[0], c.inputs[0]); c.inputs[1].default_value = dens
    Lk(c.outputs[0], pv.inputs['Density']); pv.inputs['Color'].default_value = (*col, 1); pv.inputs['Anisotropy'].default_value = 0.45
    Lk(pv.outputs['Volume'], out.inputs['Volume'])
    return m


def sphere_mesh(name, sub, jitter, seed):
    rng = random.Random(seed); bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0)
    if jitter:
        for v in bm.verts: v.co *= rng.uniform(1 - jitter, 1 + jitter)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if not jitter:
        for p in me.polygons: p.use_smooth = True
    return me


def link(name, me):
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); return o


def key_vis(ob, t_on=None, t_off=None):
    """Visibility switch (constant by nature): hidden before t_on, hidden from t_off."""
    if t_on is not None:
        ob.hide_render = True; ob.keyframe_insert('hide_render', frame=1); ob.keyframe_insert('hide_render', frame=F(t_on) - 1)
        ob.hide_render = False; ob.keyframe_insert('hide_render', frame=F(t_on))
    if t_off is not None:
        ob.hide_render = False; ob.keyframe_insert('hide_render', frame=F(t_off) - 1)
        ob.hide_render = True; ob.keyframe_insert('hide_render', frame=F(t_off))
    if t_on is None and t_off is None: return
    ob.hide_render = (t_on is not None)


def aim(ob, d):
    ob.rotation_euler = Vector(d).to_track_quat('-Z', 'Y').to_euler()


def spot(name, loc, target, energy, size_deg, soft, col=(1.0, 0.86, 0.68), parent=None):
    ld = bpy.data.lights.new(name, 'SPOT'); ld.energy = energy; ld.spot_size = math.radians(size_deg); ld.spot_blend = 0.25
    ld.shadow_soft_size = soft; ld.color = col
    o = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(o); o.location = loc
    if parent is not None: o.parent = parent
    aim(o, Vector(target) - Vector(loc)); return o


def point(name, loc, energy, col=(1.0, 0.84, 0.62), soft=0.3):
    ld = bpy.data.lights.new(name, 'POINT'); ld.energy = energy; ld.color = col; ld.shadow_soft_size = soft
    if name.startswith('lamp'): ld.volume_factor = 0.0                  # no glow balls in the dust
    o = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(o); o.location = loc; return o


def key_energy(l, keys):
    for t, e in keys:
        l.data.energy = e; l.data.keyframe_insert('energy', frame=F(t))


# ---------------------------------------------------------------- machines
def jumbo(name, loc):
    """3-boom face drilling jumbo (Epiroc-yellow carrier). Local frame: front (booms) at x=0 drilling toward -x.
    Booms = STRETCH_TO to tip empties; each tip carries a feed rail with a drill rod (child 'drill', advance on -x)."""
    yel = noisy(mat(name + '_yel', (0.66, 0.44, 0.03), 0.62, 0.0), 4.0, 0.75, 0.12)
    alu = noisy(mat(name + '_alu', (0.72, 0.73, 0.75), 0.38, 1.0), 9.0, 0.85, 0.05)
    dk = mat(name + '_dk', (0.035, 0.036, 0.04), 0.5, 0.7); st = mat(name + '_st', (0.55, 0.56, 0.58), 0.28, 1.0)
    ty = noisy(mat(name + '_tyre', (0.025, 0.025, 0.027), 0.85), 20.0, 0.7, 0.4)
    gl = mat(name + '_gl', (0.03, 0.04, 0.05), 0.05, 0.0); lp = mat(name + '_lamp', (1, 1, 1), 0.3, 0, (1.0, 0.92, 0.8), 4.0)
    hs = mat(name + '_hose', (0.02, 0.02, 0.02), 0.6)
    root = empty(name, loc)
    B, K, T, G, L, H = (Acc(name + '_body', yel), Acc(name + '_dark', dk), Acc(name + '_tyres', ty), Acc(name + '_glass', gl),
                        Acc(name + '_lamps', lp), Acc(name + '_hoses', hs))
    B.box((11.0, 2.5, 0.9), (6.5, 0, 1.35)); B.box((3.4, 2.5, 1.5), (10.4, 0, 2.55)); K.box((0.25, 2.2, 1.0), (12.2, 0, 2.5))
    for k in range(6): K.box((3.0, 0.04, 0.9), (10.4, -1.0 + k * 0.4, 3.31))                       # engine louvres
    B.box((2.6, 1.4, 0.25), (4.8, 0.5, 1.95)); B.box((2.8, 1.7, 0.15), (4.8, 0.5, 4.0))              # cab floor / FOPS roof
    for cx, cy in ((3.6, 1.25), (6.0, 1.25), (3.6, -0.25), (6.0, -0.25)): K.box((0.12, 0.12, 2.0), (cx, cy, 3.0))
    G.box((0.04, 1.3, 1.3), (3.6, 0.5, 3.0)); G.box((2.2, 0.04, 1.1), (4.8, 1.26, 3.0)); G.box((2.2, 0.04, 1.1), (4.8, -0.26, 3.0)); G.box((0.04, 1.3, 1.1), (6.0, 0.5, 3.0))
    K.box((0.6, 0.6, 0.9), (4.9, 0.6, 2.5)); K.box((0.4, 0.8, 0.5), (4.1, 0.6, 2.6))                  # seat, console
    B.box((1.8, 2.5, 1.5), (0.9, 0, 2.05)); K.box((0.7, 3.0, 0.5), (0.4, 0, 1.0))                    # turret, front beam
    for s in (-1, 1): K.box((0.35, 0.35, 1.2), (0.4, s * 1.45, 0.55)); K.box((0.6, 0.6, 0.08), (0.4, s * 1.45, 0.04))
    for wx in (2.4, 9.8):
        for s in (-1, 1):
            T.cyl(0.8, 0.62, (wx, s * 1.35, 0.8), zrot_to((0, 1, 0)), 32); K.cyl(0.42, 0.64, (wx, s * 1.35, 0.8), zrot_to((0, 1, 0)), 16)
    T.cyl(0.65, 1.8, (12.9, 0, 2.7), zrot_to((0, 1, 0)), 28); K.cyl(0.25, 1.9, (12.9, 0, 2.7), zrot_to((0, 1, 0)), 12)  # cable reel
    for s in (-1, 1): L.box((0.06, 0.35, 0.2), (3.5, s * 0.7 + 0.5, 4.15)); L.box((0.06, 0.3, 0.18), (-0.02, s * 0.9, 2.7))
    for k in range(5): H.beam((1.6, -0.9 + k * 0.45, 2.8), (4.0, -0.9 + k * 0.4, 4.1), 0.07)
    for a in (B, K, T, G, L, H): a.build(root)
    tips, drills = [], []
    for k, by in enumerate((-1.0, 0.0, 1.0)):
        base = Vector((0.15, by, 2.8 if k == 1 else 2.35))
        park = Vector((-4.6, by * 1.6, 3.0 + (0.8 if k == 1 else 0.0)))
        tip = empty(f'{name}_tip{k}', park, root); L0 = (park - base).length
        A = Acc(f'{name}_boom{k}', yel)                                       # telescopic boom: outer + inner round tubes
        A.cyl(0.21, L0 * 0.62, (0, L0 * 0.31, 0), zrot_to((0, 1, 0)), 24); A.cyl(0.15, L0 * 0.5, (0, L0 * 0.72, 0), zrot_to((0, 1, 0)), 20)
        A.cyl(0.24, 0.12, (0, L0 * 0.62, 0), zrot_to((0, 1, 0)), 24); A.box((0.6, 0.7, 0.62), (0, 0.2, 0)); A.cyl(0.2, 0.75, (0, 0.2, 0), zrot_to((1, 0, 0)), 20)
        Hc = Acc(f'{name}_boomcyl{k}', st)                                     # lift cylinder + chrome rod
        Hc.cyl(0.09, L0 * 0.45, (0, L0 * 0.3, -0.32), zrot_to((0, 1, 0)), 14); Hc.cyl(0.05, L0 * 0.35, (0, L0 * 0.68, -0.27), zrot_to((0, 1, 0)), 10)
        Hh = Acc(f'{name}_boomhose{k}', mat(f'{name}_hz{k}', (0.02, 0.02, 0.02), 0.6))
        for hx in (-0.12, 0.0, 0.12): Hh.cyl(0.025, L0 * 0.95, (hx, L0 * 0.5, 0.25), zrot_to((0, 1, 0)), 8)
        for acc in (A, Hc, Hh):
            o = acc.build(root); o.location = base
            c = o.constraints.new('STRETCH_TO'); c.target = tip; c.rest_length = L0; c.volume = 'NO_VOLUME'
        Fd = Acc(f'{name}_feed{k}', alu)                                      # aluminium feed beam with a top slot
        Fd.box((5.8, 0.26, 0.05), (-0.9, 0, -0.1)); Fd.box((5.8, 0.07, 0.24), (-0.9, 0.095, 0)); Fd.box((5.8, 0.07, 0.24), (-0.9, -0.095, 0))
        for fx in (-3.4, -1.8, -0.2, 1.4): Fd.box((0.08, 0.3, 0.28), (fx, 0, 0))
        Fs = Acc(f'{name}_head{k}', st)                                       # boom head: rotator + cradle + front centraliser
        Fs.cyl(0.26, 0.35, (0.3, 0, -0.42), zrot_to((1, 0, 0)), 24); Fs.box((0.7, 0.42, 0.22), (0.3, 0, -0.22))
        Fs.cyl(0.16, 0.18, (-3.75, 0, 0.25), zrot_to((1, 0, 0)), 20); Fs.box((0.2, 0.34, 0.18), (-3.75, 0, 0.05))
        Fd.build(tip); Fs.build(tip)
        Dr = Acc(f'{name}_drill{k}', st); Dr.cyl(0.02, 5.2, (-1.3, 0, 0.25), zrot_to((1, 0, 0)), 10)
        for cx in (-2.6, 0.1): Dr.cyl(0.035, 0.18, (cx, 0, 0.25), zrot_to((1, 0, 0)), 10)
        dr = Dr.build(tip)
        Hm = Acc(f'{name}_hammer{k}', dk)                                     # drifter: body + motor + slide shoe in the slot
        Hm.box((0.95, 0.3, 0.3), (1.6, 0, 0.27)); Hm.cyl(0.13, 0.4, (2.2, 0, 0.27), zrot_to((1, 0, 0)), 16); Hm.box((0.9, 0.12, 0.12), (1.6, 0, 0.08))
        Hm.build(dr)
        tips.append(tip); drills.append(dr)
    for s in (-1, 1):
        spot(f'{name}_sp{s}', (-0.3, s * 1.0, 4.0), (-12, s * 0.6, 2.0), 3500, 70, 0.12, parent=root)
    return root, tips, drills


def drill_cycle(root_loc, tip, dr, k, holes, t_park_out, t_park_in, park, gap=4.2, adv=-1.6):
    """Move tip from park to each hole, advance the rod, withdraw; back to park. holes: [(t0, world (hx, hy, hz))]."""
    rl = Vector(root_loc)
    tip.location = park; tip.keyframe_insert('location', frame=1); tip.keyframe_insert('location', frame=F(t_park_out))
    dr.location.x = 0.0; dr.keyframe_insert('location', index=0, frame=1)
    for t0, h in holes:
        hp = Vector((h[0] + gap, h[1], h[2] - 0.25)) - rl
        tip.location = hp + Vector((0.7, 0, 0)); tip.keyframe_insert('location', frame=F(t0 - 0.35))
        tip.location = hp; tip.keyframe_insert('location', frame=F(t0))
        dr.location.x = 0.0; dr.keyframe_insert('location', index=0, frame=F(t0 + 0.05))
        dr.location.x = adv; dr.keyframe_insert('location', index=0, frame=F(t0 + 0.7))
        dr.location.x = 0.0; dr.keyframe_insert('location', index=0, frame=F(t0 + 0.9))
        tip.location = hp + Vector((0.7, 0, 0)); tip.keyframe_insert('location', frame=F(t0 + 1.05))
    tip.location = park; tip.keyframe_insert('location', frame=F(t_park_in))


def spraymec(name, loc):
    """Shotcrete robot: carrier + pump + long boom (STRETCH_TO a nozzle empty), nozzle head tracks the wall target, spray cone
    (volume) stretched to the target."""
    org = noisy(mat(name + '_org', (0.62, 0.17, 0.03), 0.6, 0.0), 4.0, 0.75, 0.12)
    gr = noisy(mat(name + '_grey', (0.36, 0.37, 0.38), 0.5, 0.4), 6.0, 0.6, 0.15)
    dk = mat(name + '_dk', (0.035, 0.036, 0.04), 0.5, 0.7); st = mat(name + '_st', (0.55, 0.56, 0.58), 0.3, 1.0)
    ty = noisy(mat(name + '_tyre', (0.025, 0.025, 0.027), 0.85), 20.0, 0.7, 0.4); gl = mat(name + '_gl', (0.03, 0.04, 0.05), 0.05)
    lp = mat(name + '_lamp', (1, 1, 1), 0.3, 0, (1.0, 0.92, 0.8), 4.0)
    root = empty(name, loc)
    O, Gr, K, T, G, L = (Acc(name + '_body', org), Acc(name + '_pump', gr), Acc(name + '_dark', dk), Acc(name + '_tyres', ty),
                         Acc(name + '_glass', gl), Acc(name + '_lamps', lp))
    O.box((9.6, 2.4, 0.9), (5.2, 0, 1.3)); O.box((2.0, 1.15, 1.7), (1.6, 0.6, 2.6)); G.box((0.04, 1.0, 0.9), (0.58, 0.6, 2.9))
    Gr.box((3.6, 2.3, 1.7), (6.4, 0, 2.6)); Gr.box((1.7, 2.1, 1.1), (8.9, 0, 2.3)); Gr.cyl(0.55, 2.0, (4.0, -0.6, 2.3), zrot_to((1, 0, 0)), 24)
    O.box((1.3, 1.3, 1.0), (0.7, -0.5, 2.25))
    for wx in (2.0, 8.2):
        for s in (-1, 1):
            T.cyl(0.72, 0.55, (wx, s * 1.3, 0.72), zrot_to((0, 1, 0)), 28); K.cyl(0.38, 0.57, (wx, s * 1.3, 0.72), zrot_to((0, 1, 0)), 16)
    L.box((0.05, 0.3, 0.18), (0.55, 0.9, 3.3)); L.box((0.05, 0.3, 0.18), (0.55, 0.3, 3.3))
    for a in (O, Gr, K, T, G, L): a.build(root)
    base = Vector((0.7, -0.5, 2.8)); park = Vector((-3.2, -0.5, 3.3))
    noz = empty(name + '_noz', park, root); L0 = (park - base).length
    A = Acc(name + '_boom', org)                                             # three telescopic round sections
    A.cyl(0.24, L0 * 0.45, (0, L0 * 0.225, 0), zrot_to((0, 1, 0)), 24); A.cyl(0.18, L0 * 0.4, (0, L0 * 0.58, 0), zrot_to((0, 1, 0)), 20)
    A.cyl(0.13, L0 * 0.25, (0, L0 * 0.86, 0), zrot_to((0, 1, 0)), 18); A.cyl(0.27, 0.12, (0, L0 * 0.45, 0), zrot_to((0, 1, 0)), 24); A.cyl(0.21, 0.1, (0, L0 * 0.78, 0), zrot_to((0, 1, 0)), 20)
    A.box((0.7, 0.8, 0.7), (0, 0.2, 0)); A.cyl(0.22, 0.85, (0, 0.2, 0), zrot_to((1, 0, 0)), 20)
    Hs = Acc(name + '_boomhose', dk); Hs.cyl(0.07, L0 * 0.98, (0.3, L0 * 0.5, 0.22), zrot_to((0, 1, 0)), 12)
    for hy in range(1, 8): Hs.cyl(0.1, 0.06, (0.3, L0 * hy / 8, 0.22), zrot_to((0, 1, 0)), 12)
    for acc in (A, Hs):
        o = acc.build(root); o.location = base
        c = o.constraints.new('STRETCH_TO'); c.target = noz; c.rest_length = L0; c.volume = 'NO_VOLUME'
    tgt = empty(name + '_target', (-60, 0, 9))
    Nh = Acc(name + '_nozzle', st); Nh.cyl(0.11, 0.7, (0, 0.2, 0), zrot_to((0, 1, 0)), 16); Nh.box((0.35, 0.35, 0.35), (0, -0.1, 0))
    nh = Nh.build(noz); c = nh.constraints.new('DAMPED_TRACK'); c.target = tgt; c.track_axis = 'TRACK_Y'
    bm = bmesh.new(); Lc = 4.4
    r_ = bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.06, radius2=1.0, depth=Lc)
    bmesh.ops.translate(bm, vec=(0, 0, Lc / 2), verts=r_['verts'])
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Quaternion((1, 0, 0), -math.pi / 2).to_matrix(), verts=r_['verts'])
    me = bpy.data.meshes.new(name + '_spray'); bm.to_mesh(me); bm.free()
    me.materials.append(puff_mat(name + '_spraymat', (0.62, 0.62, 0.6), 10.0, radial=False))
    cone = link(name + '_spray', me); cone.parent = nh                     # rides the nozzle head (tracks the wall target)
    spot(name + '_sp', (0.3, 0.0, 3.6), (-12, 0, 5.0), 2500, 70, 0.15, parent=root)
    return root, noz, tgt, cone, park


def dumper(name, loc):
    """Articulated dump truck, front facing -y."""
    ye = noisy(mat(name + '_y', (0.6, 0.4, 0.03), 0.45, 0.25), 4.0, 0.7, 0.12); dk = mat(name + '_d', (0.035, 0.036, 0.04), 0.5, 0.7)
    ty = noisy(mat(name + '_t', (0.025, 0.025, 0.027), 0.85), 20.0, 0.7, 0.4); lp = mat(name + '_l', (1, 1, 1), 0.3, 0, (1.0, 0.95, 0.85), 4.0)
    mud = noisy(mat(name + '_m', (0.07, 0.065, 0.06), 0.9), 8.0, 0.6, 0.4)
    root = empty(name, loc)
    Y, K, T, L, M = Acc(name + '_body', ye), Acc(name + '_dark', dk), Acc(name + '_tyres', ty), Acc(name + '_lamps', lp), Acc(name + '_muck', mud)
    Y.box((2.6, 2.6, 1.6), (0, 1.5, 1.9)); Y.box((1.9, 1.7, 1.5), (-0.2, 1.4, 3.4)); K.box((1.5, 0.05, 0.9), (-0.2, 0.54, 3.5))
    Y.box((3.0, 5.6, 0.3), (0, 6.2, 1.9)); Y.box((0.2, 5.6, 1.6), (-1.4, 6.2, 2.8)); Y.box((0.2, 5.6, 1.6), (1.4, 6.2, 2.8)); Y.box((3.0, 0.3, 1.9), (0, 3.4, 3.0))
    M.box((2.6, 5.0, 0.9), (0, 6.3, 3.3)); M.sphere(1.3, (0, 6.4, 3.6), (1.0, 1.9, 0.5), 2)
    for wy in (1.4, 5.3, 7.6):
        for s in (-1, 1): T.cyl(0.85, 0.7, (s * 1.35, wy, 0.85), zrot_to((1, 0, 0)), 28); K.cyl(0.45, 0.72, (s * 1.35, wy, 0.85), zrot_to((1, 0, 0)), 14)
    for s in (-1, 1): L.box((0.35, 0.06, 0.22), (s * 0.9, 0.18, 2.3))
    for a in (Y, K, T, L, M): a.build(root, True if a is M else False)
    spot(name + '_sp', (0, 0.0, 2.4), (0, -20, 0.0), 3000, 60, 0.1, (1.0, 0.95, 0.88), root)
    return root


# ---------------------------------------------------------------- face details
def face_holes(cap, xref, sgn):
    """Drill pattern (perimeter + grid) ray-cast onto the displaced face. Returns [(hx, hy, hz)]."""
    bpy.context.scene.frame_set(1); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for (u, v) in profile(R, ZS, WB, 0.8):
        if v < 0.05: continue
        c = Vector((0, max(min(v, ZS), 0.6))); p = Vector((u, v)); p = p + (c - p).normalized() * 0.5; pts.append((p.x, p.y))
    pts += [(u, 0.55) for u in [-4.8 + 0.8 * i for i in range(13)]]          # lifters
    for r_, zz in enumerate([1.6 + 1.05 * i for i in range(9)]):
        for yy in [-5.4 + 1.1 * i + (0.55 if r_ % 2 else 0) for i in range(11)]:
            if inside_main(yy, zz, 1.0): pts.append((yy, zz))
    out = []
    for y, z in pts:
        hit, loc, nor, idx = cap.ray_cast(Vector((xref + 8 * sgn, y, z)), Vector((-sgn, 0, 0)), depsgraph=dg)
        if hit: out.append((loc.x, y, z))
    return out


def hole_disc(acc, h, sgn):
    acc.cyl(0.055, 0.14, (h[0] - 0.03 * sgn, h[1], h[2]), zrot_to((1, 0, 0)), 12)


def wire(acc_c, acc_w, h, sgn, rng):
    x, y, z = h; dy = rng.uniform(-0.25, 0.25); dz = rng.uniform(0.5, 1.2)
    acc_c.cyl(0.042, 0.12, (x + 0.05 * sgn, y, z), zrot_to((1, 0, 0)), 10)
    p0 = Vector((x + 0.08 * sgn, y, z)); p1 = p0 + Vector((0.22 * sgn, dy * 0.4, -0.12)); p2 = p1 + Vector((0.12 * sgn, dy, -dz))
    acc_w.beam(p0, p1, 0.026); acc_w.beam(p1, p2, 0.026)


def chunks(name, m, n, x0, dirx, t0, seed, ylim=5.0):
    rng = random.Random(seed); meshes = [sphere_mesh(f'{name}_me{i}', 1, 0.35, seed + i) for i in range(5)]
    for me in meshes: me.materials.append(m)
    for i in range(n):
        ob = link(f'{name}{i}', meshes[i % 5]); s = rng.uniform(0.14, 0.45)
        ob.scale = (s * rng.uniform(0.8, 1.4), s, s * rng.uniform(0.6, 1.0))
        p = Vector((x0 + 0.4 * dirx, rng.uniform(-4.0, 4.0), rng.uniform(0.8, 8.5)))
        v = Vector((dirx * rng.uniform(5, 15), rng.uniform(-2.0, 2.0), rng.uniform(-1, 4)))
        rot = Vector([rng.uniform(0, 6.28) for _ in range(3)]); w = Vector([rng.uniform(-9, 9) for _ in range(3)])
        key_vis(ob, t_on=t0)
        t, dt = 0.0, 2.0 / FPS
        while t < 2.6:
            ob.location = p; ob.rotation_euler = rot
            ob.keyframe_insert('location', frame=F(t0 + t)); ob.keyframe_insert('rotation_euler', frame=F(t0 + t))
            v.z -= 9.8 * dt; p = p + v * dt; rot = rot + w * dt
            if p.z < s * 0.6:
                p.z = s * 0.6; v = Vector((v.x * 0.35, v.y * 0.35, -v.z * 0.2)); w *= 0.4
                if abs(v.z) < 0.6: v.z = 0.0
            if abs(p.y) > ylim: p.y = math.copysign(ylim, p.y); v.y = -v.y * 0.3
            t += dt
        for fc in fcurves_of(ob):
            for kp in fc.keyframe_points:
                if fc.data_path != 'hide_render': kp.interpolation = 'LINEAR'          # ballistic samples (intended)


def puffs(name, m, n, seed, t0, x0, dirx, reach, smax, dens_keys):
    rng = random.Random(seed); me = sphere_mesh(name + '_me', 3, 0.0, seed)
    for i in range(n):
        ob = link(f'{name}{i}', me)
        mi = m.copy(); ob.data = me.copy(); ob.data.materials.append(mi); D = mi.node_tree.nodes['D'].inputs[1]; d0 = D.default_value
        p0 = Vector((x0 + 0.5 * dirx, rng.uniform(-3, 3), rng.uniform(1.5, 7.5)))
        p1 = Vector((x0 + dirx * rng.uniform(0.25, 1.0) * reach, rng.uniform(-4.2, 4.2), rng.uniform(1.8, 7.0)))
        s1 = rng.uniform(0.6, 1.0) * smax; dl = rng.uniform(0.0, 0.25)
        ob.location = p0; ob.scale = (0.4, 0.4, 0.4); ob.keyframe_insert('location', frame=F(t0 + dl)); ob.keyframe_insert('scale', frame=F(t0 + dl))
        ob.location = p0.lerp(p1, 0.55); ob.scale = (0.7 * s1, 0.6 * s1, 0.55 * s1); ob.keyframe_insert('location', frame=F(t0 + 0.35 + dl)); ob.keyframe_insert('scale', frame=F(t0 + 0.35 + dl))
        ob.location = p1; ob.scale = (s1, s1 * 0.85, s1 * 0.75); ob.keyframe_insert('location', frame=F(t0 + 1.6 + dl)); ob.keyframe_insert('scale', frame=F(t0 + 1.6 + dl))
        ob.location = p1 + Vector((dirx * 1.5, 0, -0.6)); ob.scale = (s1 * 1.2, s1, s1 * 0.85)
        ob.keyframe_insert('location', frame=F(dens_keys[-1][0])); ob.keyframe_insert('scale', frame=F(dens_keys[-1][0]))
        for t, d in [(0.0, 0.0), (t0 + dl - 0.05, 0.0)] + [(tt + (dl if j == 0 else 0), dd) for j, (tt, dd) in enumerate(dens_keys)]:
            D.default_value = d * d0; D.keyframe_insert('default_value', frame=max(1, F(t)))


def flash(name, loc, t0, light_e):
    l = point(name + '_l', loc, 0.0, (1.0, 0.7, 0.4), 1.5)
    key_energy(l, ((0, 0), (t0 - 0.04, 0), (t0, light_e), (t0 + 0.15, light_e * 0.4), (t0 + 0.45, 0)))


# ---------------------------------------------------------------- the set
def build():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    rng = random.Random(6)
    # ---- shells: main (A..B), tunnel C, adit, one mesh; roof faces (z > ZC) use the hideable material
    shell_lo = rock_mat('shell_rock', shot=True); shell_hi = rock_mat('shell_rock_roof', shot=True, hide=True)
    pM, pA = profile(R, ZS, WB, 0.2), profile(RA, ZSA, WBA, 0.2)
    bm = bmesh.new()
    inM = lambda c: Vector((c.x, 0, max(min(c.z, ZS), 1.0)))
    keepM = lambda c: not (c.y > 0 and c.z > 0.15 and c.z < ZSA + RA and abs(c.x) < hwA(c.z) - 0.02)
    tube(bm, pM, rings([(-64.0, -36, 0.2), (-36, -6, 0.4), (-6, 6, 0.2), (6, 40, 0.4), (40, 61.0, 0.2)]), lambda s, u, v: Vector((s, u, v)), keepM, inM)
    tube(bm, pM, rings([(65.0, 90, 0.2), (90, XCE + 2, 0.6)]), lambda s, u, v: Vector((s, u, v)), lambda c: True, inM)
    tube(bm, pA, rings([(4.5, 30, 0.2), (30, YAE + 2, 0.6)]), lambda s, u, v: Vector((u, s, v)), lambda c: c.y > hwM(c.z),
         lambda c: Vector((0, c.y, max(min(c.z, ZSA), 1.0))))
    shell = finish(bm, 'shell', [shell_lo, shell_hi])
    vg = shell.vertex_groups.new(name='wall')
    vg.add([v.index for v in shell.data.vertices if v.co.z > 0.05], 1.0, 'REPLACE'); vg.add([v.index for v in shell.data.vertices if v.co.z <= 0.05], 0.3, 'REPLACE')
    t_cl = tex('rk_clouds', 'CLOUDS', 1.6, noise_depth=4); t_vo = tex('rk_cells', 'VORONOI', 0.7, weight_1=-1.0, weight_2=1.0)
    disp(shell, t_cl, 0.55, 'wall'); disp(shell, t_vo, 0.05, 'wall')
    # ---- faces (caps): A (moves at the blast), B, C; + holed versions of B/C and the breakthrough bore
    cap_lo = rock_mat('face_rock'); cap_hi = rock_mat('face_rock_roof', hide=True)
    t_cl2 = tex('fc_clouds', 'CLOUDS', 1.6, noise_depth=5); t_vo2 = tex('fc_cells', 'VORONOI', 0.55, weight_1=-1.0, weight_2=1.0); t_fn = tex('fc_fine', 'CLOUDS', 0.35, noise_depth=3)
    hole_r = lambda a: 3.3 + 0.45 * math.sin(3 * a + 1.0) + 0.3 * math.sin(5 * a + 2.2) + 0.2 * math.sin(8 * a)

    def cap(name, x0, sgn, step, hole=False):
        bm = bmesh.new(); y0, z0 = -7.4, -0.5; ny, nz = int(14.8 / step), int(12.4 / step); V = {}
        def ok(y, z):
            if z <= ZS: return abs(y) <= hwM(max(z, 0)) + 0.9
            return y * y + (z - ZS) ** 2 <= (R + 0.9) ** 2
        def gv(i, k):
            if (i, k) not in V: V[(i, k)] = bm.verts.new((x0, y0 + i * step, z0 + k * step))
            return V[(i, k)]
        for i in range(ny):
            for k in range(nz):
                yc, zc = y0 + (i + 0.5) * step, z0 + (k + 0.5) * step
                if not ok(yc, zc): continue
                if hole and yc * yc + (zc - 4.2) ** 2 < hole_r(math.atan2(zc - 4.2, yc)) ** 2: continue
                f = bm.faces.new((gv(i, k), gv(i + 1, k), gv(i + 1, k + 1), gv(i, k + 1)))
                if sgn < 0: f.normal_flip()
                f.material_index = 1 if zc > ZC else 0
        o = finish(bm, name, [cap_lo, cap_hi]); vgn = None
        if hole:                                    # damp the big x-displacement at the hole rim (no stretched streaks)
            vgn = 'rim'; g = o.vertex_groups.new(name=vgn)
            for v in o.data.vertices:
                y, z = v.co.y, v.co.z; d = math.sqrt(y * y + (z - 4.2) ** 2) - hole_r(math.atan2(z - 4.2, y))
                g.add([v.index], max(0.15, min(1.0, d / 1.2)), 'REPLACE')
        disp(o, t_cl2, 1.0, vgn); disp(o, t_fn, 0.25); disp(o, t_vo2, 0.04); return o
    capA = cap('face_A', XA0, 1, 0.07); capB = cap('face_B', XB, -1, 0.1); capC = cap('face_C', XCF, 1, 0.12)
    capBh = cap('face_B_open', XB, -1, 0.1, True); capCh = cap('face_C_open', XCF, 1, 0.12, True)
    bm = bmesh.new()
    pH = resample([(hole_r(a) * math.cos(a), 4.2 + hole_r(a) * math.sin(a)) for a in [i * math.tau / 160 for i in range(160)]], 0.15)
    tube(bm, pH, rings([(XB - 0.6, XCF + 0.6, 0.1)]), lambda s, u, v: Vector((s, u, v)), lambda c: True, lambda c: Vector((c.x, 0, 4.2)))
    bore = finish(bm, 'breakthrough_bore', [cap_lo, cap_lo]); bore.data.shade_flat(); disp(bore, t_cl, 0.35); disp(bore, t_vo2, 0.35); disp(bore, t_fn, 0.2)
    for o in (capBh, capCh, bore): key_vis(o, t_on=T_BLB + 0.25)
    for o in (capB, capC): key_vis(o, t_off=T_BLB + 0.25)
    capA.keyframe_insert('location', index=0, frame=F(T_BLA + 0.1))
    capA.location.x = XA1 - XA0; capA.keyframe_insert('location', index=0, frame=F(T_BLA + 0.15))
    # ---- plan-section slab (top at ZC) with the tunnel bands open
    pl = rock_mat('section_rock', cull=False)
    S = Acc('section', pl); wM, wA = hwM(ZC) - 0.4, hwA(ZC) - 0.3; X0, X1, Y0, Y1 = -240.0, 340.0, -170.0, 260.0
    def slab(xa, xb, ya, yb): S.box((xb - xa, yb - ya, 0.3), ((xa + xb) / 2, (ya + yb) / 2, ZC - 0.15))
    slab(X0, X1, Y0, -wM); slab(X0, -wA, wM, Y1); slab(wA, X1, wM, Y1); slab(-wA, wA, YAE, Y1)
    slab(X0, XA1, -wM, wM); slab(XB, XCF, -wM, wM); slab(XCE, X1, -wM, wM)
    S.build()
    # ---- lattice girders behind face A (exposed steel arches), roof part hideable
    gs = noisy(mat('girder', (0.22, 0.13, 0.08), 0.55, 0.8), 12.0, 0.6, 0.2)
    Glo, Ghi = Acc('girders', gs), Acc('girders_roof', hid(noisy(mat('girder_roof', (0.22, 0.13, 0.08), 0.55, 0.8), 12.0, 0.6, 0.2)))
    gp = [(u, v) for (u, v) in profile(R, ZS, WB, 0.45) if v > 0.05]
    def gpt(x, u, v, off, dx):
        c = Vector((0, max(min(v, ZS), 0.0))); p = Vector((u, v)); q = p + (c - p).normalized() * off
        return Vector((x + dx, q.x, q.y))
    for gx in [-58.6 + 2.0 * i for i in range(5)]:
        ia = [gpt(gx, u, v, 0.55, -0.11) for u, v in gp]; ib = [gpt(gx, u, v, 0.55, 0.11) for u, v in gp]; ou = [gpt(gx, u, v, 0.32, 0.0) for u, v in gp]
        def bm_(a, b, w): (Ghi if (a.z + b.z) / 2 > ZC else Glo).beam(a, b, w)
        for i in range(len(gp) - 1):
            bm_(ia[i], ia[i + 1], 0.045); bm_(ib[i], ib[i + 1], 0.045); bm_(ou[i], ou[i + 1], 0.05)
            bm_(ia[i], ou[i + 1], 0.022); bm_(ib[i], ou[i + 1], 0.022); bm_(ia[i], ib[i], 0.02)
    Glo.build(); Ghi.build()
    # ---- services: vent duct at the crown (hideable), pipes on the wall, wall light strips, junction collar
    Du = Acc('vent_duct', hid(noisy(mat('duct', (0.62, 0.42, 0.04), 0.8), 2.0, 0.75, 0.3)))
    for xa, xb in ((-47.0, 58.0), (70.0, XCE)):
        Du.cyl(0.75, xb - xa, ((xa + xb) / 2, 2.6, 9.4), zrot_to((1, 0, 0)), 28)
        for xx in range(int(xa), int(xb), 3): Du.cyl(0.79, 0.1, (xx, 2.6, 9.4), zrot_to((1, 0, 0)), 28)
    Du.build(None, True)
    Pp = Acc('pipes', mat('pipe', (0.4, 0.41, 0.42), 0.35, 1.0)); yp = -(hwM(1.0) - 0.3)
    for xa, xb in ((-56.0, 59.0), (68.0, XCE)):
        Pp.cyl(0.09, xb - xa, ((xa + xb) / 2, yp, 1.0), zrot_to((1, 0, 0)), 12); Pp.cyl(0.14, xb - xa, ((xa + xb) / 2, yp + 0.05, 1.45), zrot_to((1, 0, 0)), 14)
        for xx in range(int(xa), int(xb), 4): Pp.box((0.08, 0.35, 0.7), (xx, yp - 0.05, 1.2))
    Pp.build(None, True)
    Ls = Acc('strip_lights', mat('strip', (1, 0.95, 0.85), 0.4, 0, (1.0, 0.9, 0.72), 3.0)); ys = hwM(5.6) - 0.3
    for s in (-1, 1):
        for xa, xb in (((-46.0, -4.5), (4.5, 58.0)) if s > 0 else ((-46.0, 58.0),)) + ((70.0, XCE),):
            Ls.box((xb - xa, 0.12, 0.1), ((xa + xb) / 2, s * ys, 5.6))
        Ls.box((0.12, YAE - 9.0, 0.1), (s * (hwA(4.5) - 0.3), (YAE + 9.0) / 2, 4.5))
    Ls.build()
    col_lo = noisy(mat('collar', (0.3, 0.3, 0.29), 0.85), 5.0, 0.7, 0.3)
    Cl, Ch = Acc('adit_collar', col_lo), Acc('adit_collar_roof', hid(noisy(mat('collar_roof', (0.3, 0.3, 0.29), 0.85), 5.0, 0.7, 0.3)))
    cp = [(u, v) for (u, v) in profile(RA, ZSA, WBA, 0.3) if v > 0.05]
    for i in range(len(cp) - 1):
        a = Vector((cp[i][0], hwM(cp[i][1]), cp[i][1])); b = Vector((cp[i + 1][0], hwM(cp[i + 1][1]), cp[i + 1][1]))
        (Ch if (a.z + b.z) / 2 > ZC else Cl).beam(a, b, 0.55, 0.95)
    Cl.build(); Ch.build()
    portal = mat('daylight', (1, 1, 1), 0.5, 0, (1.0, 0.96, 0.88), 4.0); Pt = Acc('portals', portal)
    Pt.box((0.2, 12.4, 10.8), (XCE + 1.2, 0, 5.4)); Pt.box((8.2, 0.2, 7.8), (0, YAE + 1.2, 3.9)); Pt.build()
    # ---- machines
    jA, tipsA, drA = jumbo('jumboA', (-40.0, -2.6, 0.0))
    jA.keyframe_insert('location', index=0, frame=1); jA.keyframe_insert('location', index=0, frame=F(9.5))
    jA.location.x = -48.0; jA.keyframe_insert('location', index=0, frame=F(11.5)); jA.keyframe_insert('location', index=0, frame=F(14.9))
    jA.location.x = -34.0; jA.keyframe_insert('location', index=0, frame=F(16.9))
    jC, tipsC, drC = jumbo('jumboC', (77.5, 2.4, 0.0))
    sm, noz, tgt, cone, spark = spraymec('spraymec', (-36.0, 3.0, 0.0))
    for t, x in ((0.0, -36.0), (18.0, -36.0), (19.7, -49.0), (23.3, -49.0), (25.0, -38.0)):
        sm.location.x = x; sm.keyframe_insert('location', index=0, frame=F(t))
    dmp = dumper('dumper', (0.0, 70.0, 0.0))
    for t, y in ((0.0, 70.0), (27.0, 70.0), (31.8, 16.0)):
        dmp.location.y = y; dmp.keyframe_insert('location', index=1, frame=F(t))
    # ---- face A: drill pattern, 6 holes drilled live, charges + wires loaded 15.0-16.8, blast
    hm = mat('hole', (0.004, 0.004, 0.005), 0.9)
    hA = face_holes(capA, XA0, 1)
    want = [[(-3.5, 3.0), (-2.6, 1.6)], [(-0.5, 7.6), (0.6, 6.5)], [(2.4, 3.6), (3.4, 2.2)]]
    live = [[min(hA, key=lambda h: (h[1] - y) ** 2 + (h[2] - z) ** 2) for (y, z) in w] for w in want]
    flat = [h for w in live for h in w]
    H0 = Acc('holes_A', hm)
    for h in hA:
        if h not in flat: hole_disc(H0, h, 1)
    hob = H0.build(); key_vis(hob, t_off=T_BLA + 0.1)
    dust_m = puff_mat('dust', (0.42, 0.39, 0.34), 0.6); dustB_m = puff_mat('dustB', (0.5, 0.47, 0.42), 0.4); fine_m = puff_mat('drill_dust', (0.5, 0.48, 0.44), 2.5)
    fme = sphere_mesh('drill_puff', 2, 0.0, 3)
    for k in range(3):
        hs = [(11.8 + 0.15 * k + 1.45 * j, live[k][j]) for j in range(2)]
        drill_cycle((-48.0, -2.6, 0.0), tipsA[k], drA[k], k, hs, 11.4, 14.85, tipsA[k].location.copy())
        for t0, h in hs:
            Hn = Acc(f'hole_new{k}_{t0:.1f}', hm); hole_disc(Hn, h, 1); o = Hn.build(); key_vis(o, t_on=t0 + 0.85, t_off=T_BLA + 0.1)
            pf = link(f'dpuff{k}_{t0:.1f}', fme.copy()); pf.location = (h[0] + 0.5, h[1], h[2]); pf.scale = (0.5, 0.5, 0.5)
            fm = fine_m.copy(); pf.data.materials.append(fm); D = fm.node_tree.nodes['D'].inputs[1]; d0 = D.default_value
            for tt, d, s_ in ((0, 0, 0.3), (t0 + 0.05, 0, 0.3), (t0 + 0.3, 1, 0.6), (t0 + 0.8, 0.8, 0.9), (t0 + 1.6, 0, 1.3)):
                D.default_value = d * d0; D.keyframe_insert('default_value', frame=max(1, F(tt))); pf.scale = (s_, s_, s_); pf.keyframe_insert('scale', frame=max(1, F(tt)))
    cm = mat('charge', (0.45, 0.06, 0.03), 0.5); wm = [mat('det_or', (0.8, 0.25, 0.02), 0.45), mat('det_ye', (0.75, 0.6, 0.03), 0.45)]
    order = sorted(hA, key=lambda h: (-round(h[2] / 1.0), h[1])); n = len(order)
    for i, h in enumerate(order):
        Cc, Cw = Acc(f'charge{i}', cm), Acc(f'wire{i}', wm[i % 2]); wire(Cc, Cw, (h[0] - h[0], 0, 0), 1, rng)
        for a in (Cc, Cw):
            o = a.build(); o.location = h; t0 = 15.0 + 1.8 * i / n
            o.scale = (0.01, 0.01, 0.01); o.keyframe_insert('scale', frame=1); o.keyframe_insert('scale', frame=F(t0))
            o.scale = (1, 1, 1); o.keyframe_insert('scale', frame=F(t0 + 0.15)); key_vis(o, t_off=T_BLA + 0.1)
    flash('flashA', (XA0 + 1.0, 0, 4.6), T_BLA, 1.2e5)
    puffs('dustA', dust_m, 16, 11, T_BLA, XA0, 1, 22.0, 4.8, [(T_BLA + 0.1, 1.0), (T_BLA + 1.5, 0.85), (19.2, 0.35), (20.2, 0.0)])
    chunks('chunkA', cap_lo, 36, XA0, 1, T_BLA, 21)
    heap = link('muck_A', sphere_mesh('muck_me', 4, 0.12, 9)); heap.data.materials.append(cap_lo)
    heap.location = (XA1 + 5.5, 0, -0.5); heap.scale = (6.0, 5.0, 1.5); key_vis(heap, t_on=T_BLA + 0.2)
    # ---- shotcrete 19.9-23.0 (mask threshold T, nozzle sweeps the crown), cone on only while spraying
    Tn = shell_lo.node_tree.nodes['T']; Tn2 = shell_hi.node_tree.nodes['T']
    for n_ in (Tn, Tn2):
        for t, v in ((0.0, -49.0), (19.9, -49.0), (23.0, -64.0)):
            n_.outputs[0].default_value = v; n_.outputs[0].keyframe_insert('default_value', frame=F(t))
    smr = Vector((-49.0, 3.0, 0.0))
    noz.location = spark; noz.keyframe_insert('location', frame=1); noz.keyframe_insert('location', frame=F(19.3))
    for i in range(12):
        t = 19.9 + i * (3.1 / 11); x = -49.5 + (-63.5 + 49.5) * i / 11; th = math.radians(28 if i % 2 == 0 else 152)
        p = Vector((x, 6.0 * math.cos(th), ZS + 6.0 * math.sin(th)))
        tgt.location = p; tgt.keyframe_insert('location', frame=F(t))
        nz_ = p + (Vector((x + 2.0, 0.8, ZS + 0.5)) - p).normalized() * 4.6
        noz.location = nz_ - smr; noz.keyframe_insert('location', frame=F(t))
    noz.location = spark; noz.keyframe_insert('location', frame=F(23.8))
    key_vis(cone, t_on=19.9, t_off=23.05)
    # ---- rock bolts 23.8-26.6: rods pushed into the fresh lined rock, plates seat in a staggered pattern
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    rod_m = mat('bolt_rod', (0.35, 0.33, 0.3), 0.4, 1.0); pl_m = mat('bolt_plate', (0.75, 0.74, 0.7), 0.3, 1.0)
    bi = 0
    for r_, bx in enumerate((-51.5, -53.7, -55.9, -58.1)):
        for th in [30 + 20 * j + (10 if r_ % 2 else 0) for j in range(7)]:
            if th > 150: continue
            d = Vector((0, math.cos(math.radians(th)), math.sin(math.radians(th))))
            hit, loc, nor, idx = shell.ray_cast(Vector((bx, 0, ZS)), d, depsgraph=dg)
            if not hit: continue
            nrm = -d; q = zrot_to(nrm); t0 = 23.8 + 0.105 * bi; bi += 1
            Rd = Acc(f'bolt{bi}', rod_m); Rd.cyl(0.03, 3.0, (0, 0, -1.5), None, 10); Rd.cyl(0.045, 0.12, (0, 0, 0.06), None, 8)
            ro = Rd.build(); ro.rotation_euler = q.to_euler()
            ro.location = loc + nrm * 2.9; key_vis(ro, t_on=t0); ro.keyframe_insert('location', frame=F(t0))
            ro.location = loc + nrm * 0.06; ro.keyframe_insert('location', frame=F(t0 + 0.35))
            Pl = Acc(f'plate{bi}', pl_m); Pl.box((0.32, 0.32, 0.025), (0, 0, 0)); Pl.box((0.1, 0.1, 0.08), (0, 0, 0.05))
            po = Pl.build(); po.rotation_euler = q.to_euler(); po.location = loc + nrm * 0.05
            po.scale = (0.01, 0.01, 0.01); po.keyframe_insert('scale', frame=1); po.keyframe_insert('scale', frame=F(t0 + 0.3))
            po.scale = (1, 1, 1); po.keyframe_insert('scale', frame=F(t0 + 0.42))
    # ---- jumbo C drilling face C (29-35 s), face B charged and waiting
    for k in range(3):
        hs = [(29.6 + 0.2 * k + 1.5 * j, (XCF + 0.4, 1.4 + (k - 1) * 1.1 + j * 0.3, 1.6 + 1.3 * j + 0.4 * k)) for j in range(4)]
        drill_cycle((77.5, 2.4, 0.0), tipsC[k], drC[k], k, hs, 29.0, 36.5, tipsC[k].location.copy(), gap=4.6, adv=-2.0)
    hB = face_holes(capB, XB, -1); HB, CB, WB_ = Acc('holes_B', hm), Acc('charges_B', cm), Acc('wires_B', wm[0])
    for h in hB: hole_disc(HB, h, -1); wire(CB, WB_, h, -1, rng)
    for a in (HB, CB, WB_): key_vis(a.build(), t_off=T_BLB + 0.05)
    flash('flashB', (XB - 1.0, 0, 4.6), T_BLB, 1.2e5)
    puffs('dustB', dustB_m, 20, 12, T_BLB, XB, -1, 24.0, 5.5, [(T_BLB + 0.1, 1.2), (T_BLB + 1.3, 1.0), (40.8, 0.45), (T_END, 0.3)])
    chunks('chunkB', cap_lo, 30, XB, -1, T_BLB, 31)
    # ---- lights
    for x in range(-44, 58, 12): point(f'lamp_m{x}', (x, 2.5 if (x // 12) % 2 else -2.5, 6.3), 700)
    for x in range(72, int(XCE), 16): point(f'lamp_c{x}', (x, -2.5, 6.3), 700)
    for y in range(14, int(YAE), 16): point(f'lamp_a{y}', (0, y, 5.4), 600)
    E = 4500
    sA = spot('face_A_key', (-48.0, -4.6, 8.0), (-61.0, 0.4, 4.2), E, 55, 0.03, (1.0, 0.9, 0.78))
    sB = spot('face_B_key', (48.0, -4.6, 8.0), (60.0, 0.0, 4.5), E, 55, 0.05, (1.0, 0.9, 0.78))
    sC = spot('face_C_key', (78.0, -4.4, 8.0), (66.0, 0.0, 4.5), E, 55, 0.05, (1.0, 0.9, 0.78))
    key_energy(sA, ((0, E), (26.6, E), (27.6, 0.1 * E), (32.5, 0.1 * E), (32.9, E)))
    for s_ in (sB, sC): key_energy(s_, ((0, 0.08 * E), (32.5, 0.08 * E), (32.9, E)))
    fill = point('face_A_fill', (-52.0, 4.2, 2.5), 400, (0.75, 0.85, 1.0), 1.0)
    bt = spot('breakthrough', (82.0, -2.8, 5.5), (55.0, 0.0, 4.2), 0.0, 55, 0.3, (1.0, 0.8, 0.55))
    key_energy(bt, ((0, 0), (T_BLB + 1.1, 0), (40.2, 1.0e5), (T_END, 1.15e5)))
    glow = spot('breakthrough_glow', (68.5, 0.0, 4.2), (50.0, 0.0, 3.5), 0.0, 90, 2.0, (1.0, 0.9, 0.75))
    key_energy(glow, ((0, 0), (T_BLB + 1.1, 0), (40.4, 1.5e3), (T_END, 1.8e3)))
    bpy.ops.object.light_add(type='AREA', location=(13, -10, 95)); top = bpy.context.active_object
    top.data.size = 260; top.data.color = (0.75, 0.82, 0.95); key_energy(top, ((0, 0), (31.6, 0), (32.6, 2.5e5), (35.4, 2.5e5), (36.2, 0)))
    w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Color'].default_value = (0.004, 0.005, 0.006, 1); bg.inputs['Strength'].default_value = 1.0
    nt.links.new(bg.outputs['Background'], nt.nodes.new('ShaderNodeOutputWorld').inputs['Surface'])
    return dict(capA=capA, tipsA=tipsA, tgt=tgt, jA=jA)


def key_roof(cam):
    """Alpha 1 -> 0 on every above-the-section material while the camera is above the roof (plan cutaway)."""
    cz = [fc for fc in fcurves_of(cam) if fc.data_path == 'location' and fc.array_index == 2][0]
    hf = next(f for f in range(F(30), F(37)) if cz.evaluate(f) > 11.5)
    sf = next(f for f in range(hf, F(40)) if cz.evaluate(f) < 11.5)
    for m in HIDE_MATS:
        a = m.node_tree.nodes['Principled BSDF'].inputs['Alpha']
        for f, v in ((1, 1.0), (hf - 1, 1.0), (hf, 0.0), (sf - 1, 0.0), (sf, 1.0)):
            a.default_value = v; a.keyframe_insert('default_value', frame=f)
        for fc in fcurves_of(m.node_tree):
            if fc.data_path.startswith('nodes["Principled BSDF"]'):
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'               # visibility switch (intended)
    return round((hf - 1) / FPS, 2), round((sf - 1) / FPS, 2)


def anchors(cam, pts, times):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; outd = {}
    for name, (fn, ts) in pts.items():
        outd[name] = []
        for t in ts:
            sc.frame_set(F(t)); p = fn()
            v = world_to_camera_view(sc, cam, p); outd[name].append([round(t, 2), round(v.x, 3), round(1 - v.y, 3), round(v.z, 1)])
    return outd


def run(args):
    d = build()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, int(T_END * FPS), FPS
    cam, tg = path_camera(PATH, FPS)
    result['roof_hidden'] = key_roof(cam)
    sc.render.engine = 'BLENDER_EEVEE'
    ee = sc.eevee
    for k, v in (('taa_render_samples', 32), ('use_volumetric_shadows', True), ('volumetric_tile_size', '4'), ('use_raytracing', True),
                 ('volumetric_end', 180.0)):
        try: setattr(ee, k, v)
        except Exception as e: result.setdefault('warn', []).append(f'{k}: {e}')
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, int(args.get('pct', 50))
    # anti-flicker (EEVEE virtual shadow maps): big pool, steady shadows, no jitter, shadows only where they matter
    for k, v in (('shadow_pool_size', str(args.get('pool', '2048'))), ('shadow_resolution_scale', 1.0), ('taa_render_samples', 64),
                 ('shadow_ray_count', 2), ('shadow_step_count', 8)):
        if hasattr(ee, k):
            try: setattr(ee, k, v)
            except Exception as e: result.setdefault('warn', []).append(f'{k}: {e}')
    for l in bpy.data.lights:
        if hasattr(l, 'use_shadow_jitter'): l.use_shadow_jitter = False
        if l.name.startswith(('lamp_', 'face_A_fill', 'Area')) or l.type == 'AREA': l.use_shadow = False
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = float(args.get('exp', 0.1))
    tA, tgtS = d['tipsA'], d['tgt']
    if args.get('mode') == 'track':
        result['track'] = track_screen(cam, {'bolts': (lambda: Vector((-55.9, 3.1, 9.6)), 21.5, 29.0)}, FPS); return
    result['anchors'] = anchors(cam, {
        'face_A': (lambda: Vector((XA0 + 0.4, 0, 5.0)), [1.3, 5.6]),
        'girders': (lambda: Vector((-54.0, 3.6, 9.2)), [9.8, 11.0]),
        'jumbo_booms': (lambda: tA[0].matrix_world.translation, [12.5, 13.6]),
        'blast_face': (lambda: Vector((XA0, 0, 4.5)), [16.0, 17.6]),
        'spray': (lambda: tgtS.matrix_world.translation, [20.5, 21.5, 22.5]),
        'bolts': (lambda: Vector((-55.9, 3.1, 9.6)), [25.0, 26.5]),
        'adit': (lambda: Vector((0.0, 7.0, 4.0)), [29.0, 31.0]),
        'face_A_wide': (lambda: Vector((XA1, 0, 3.0)), [33.8, 34.8]),
        'face_B_wide': (lambda: Vector((XB, 0, 3.0)), [33.8, 34.8]),
        'face_C_wide': (lambda: Vector((XCF, 0, 3.0)), [33.8, 34.8]),
        'face_B': (lambda: Vector((XB, 0, 4.5)), [37.5, 38.6]),
        'breakthrough': (lambda: Vector((XB, 0, 4.2)), [40.5, 41.5]),
    }, None)
    if args.get('mode', 'preview') == 'preview':
        for t in args.get('times', (1.3, 5.6, 9.8, 13.2, 16.4, 17.6, 21.4, 25.3, 29.8, 33.8, 39.2, 41.0)):
            sc.frame_set(F(t)); sc.render.filepath = f'{out}/t_{t:04.1f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        video_output(sc, out + '/ch6_natm.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
