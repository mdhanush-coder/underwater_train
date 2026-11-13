# Chapter 4 plate "How the water is held back" (54.52 s, chapter t0 = global 130.294): x-ray into the Mixshield chambers
# (excavation chamber between cutterhead and submerged wall, working chamber with the air cushion behind it, pressure
# bulkhead), slurry fill, bentonite macro, pressure balance arrows + gauge, slurry circuit to a surface separation plant,
# pull back to the glowing slurry face. Same soil cutaway as ch3. Runs after skilllib.py + bt_model.py. args: mode, pct.
import bpy, bmesh, math, random
from mathutils import Vector, Quaternion, Matrix
FPS = 30
XE = 320.0
TZ, TR, TL = -35.0, 6.55, 0.6
XS = -130.0                                   # launch shaft on the land side; separation plant beside it
T_END = 54.52
X_CF, X_SW, X_BH, RC = -0.7, -2.9, -5.4, 6.5  # cutterhead back face, submerged wall, pressure bulkhead (x), chamber radius
SW_T, BH_T = 0.25, 0.35
Z_OPEN = TZ - 4.9                             # submerged wall is open below this
L_BACK = TZ + 2.4                             # working-chamber slurry level (air cushion above)
SWC = (-4.13, 0.8)                            # macro swirl centre (x, y) in the working chamber
XQ = Quaternion((0, 1, 0), math.pi / 2)       # local z -> world +x
LATQ = Quaternion((1, 0, 0), -math.pi / 2)    # local z -> world +y
PATH = [
    (0.0, (16, -38, TZ + 5), (0, 0, TZ), 26),                       # 36 x-ray push-in
    (3.3, (2, -30, TZ + 2), (-5, 0, TZ), 30),                 # 37 chamber outline
    (5.9, (1.2, -28, TZ + 2), (-5, 0, TZ), 30),
    (7.2, (-17, -19, TZ + 7), (-3.5, 0, TZ - 0.5), 32),             # 38 walls, rear 3/4
    (9.5, (-16, -18, TZ + 6.5), (-3.5, 0, TZ - 0.5), 32),
    (10.7, (-3, -26, TZ + 1), (-6.5, 0, TZ), 32),                   # 39 fill
    (12.6, (-3.2, -24.5, TZ + 1.2), (-6.5, 0, TZ), 32),
    (13.9, (-3.6, -2.6, TZ + 3.4), (-4.3, 0.6, TZ + 2.5), 40),      # 40 macro powder
    (16.2, (-3.7, -2.3, TZ + 3.3), (-4.3, 0.6, TZ + 2.5), 40),
    (17.0, (-4.0, -1.6, TZ + 3.0), (-4.3, 0.6, TZ + 2.45), 42),     # 41 swirl
    (18.7, (-4.1, -1.4, TZ + 2.95), (-4.3, 0.6, TZ + 2.45), 42),
    (20.9, (7, -24, TZ + 3), (2, 0, TZ), 30),                       # 42 gold arrows
    (24.6, (6, -22, TZ + 2.5), (2, 0, TZ), 30),
    (25.9, (16, -55, TZ + 14), (6, 0, TZ + 12), 30),                # 43 blue from the seabed
    (26.6, (15.5, -54, TZ + 13.5), (6, 0, TZ + 12), 30),
    (28.3, (5, -26, TZ + 3), (0.5, 0, TZ), 28),                     # 44 meet
    (30.0, (4.5, -25, TZ + 3), (0.5, 0, TZ), 28),
    (31.2, (-9.6, -4.8, TZ + 1.4), (-5.6, -2.6, TZ + 0.7), 45),     # 45 gauge
    (34.3, (-9.0, -4.5, TZ + 1.3), (-5.6, -2.6, TZ + 0.7), 45),
    (35.6, (-4.5, -30, TZ + 2), (-4.5, 0, TZ + 0.5), 30),             # 46 air cushion
    (38.0, (-4.8, -29, TZ + 2), (-4.5, 0, TZ + 0.5), 30),
    (39.7, (-20, -14, TZ - 3), (-40, 0, TZ - 4.5), 28),             # 47 follow the brown slurry back
    (41.7, (-112, -14, TZ - 2), (-130, 0, TZ - 3), 28),
    (43.8, (-148, -38, 22), (-172, 20, 5), 30),                     # 48 separation plant
    (45.3, (-152, -37, 21.5), (-172, 20, 5), 30),
    (47.2, (-100, -150, 10), (-95, 0, -15), 24),                    # 49 the loop, wide
    (49.0, (-50, -110, -10), (-60, 0, -22), 24),
    (50.9, (-2, -55, TZ + 6), (-2, 0, TZ), 28),                     # 50 pull back from the glowing face
    (T_END, (10, -75, TZ + 10), (-6, 0, TZ), 26),
]


def F(t): return int(round(t * FPS)) + 1


def K(o, prop, keys):
    for t, v in keys:
        setattr(o, prop, v); o.keyframe_insert(prop, frame=F(t))


def KS(sock, keys):
    for t, v in keys:
        sock.default_value = v; sock.keyframe_insert('default_value', frame=F(t))


def linear(idb):
    for fc in fcurves_of(idb):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'


def bsdf(m): return m.node_tree.nodes['Principled BSDF']


def dithered(m, alpha=1.0):
    try: m.surface_render_method = 'DITHERED'
    except Exception: pass
    bsdf(m).inputs['Alpha'].default_value = alpha
    return m


def mix_rgba(nt):
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
    A = [x for x in mx.inputs if x.name == 'A' and x.type == 'RGBA'][0]; B = [x for x in mx.inputs if x.name == 'B' and x.type == 'RGBA'][0]
    R = [x for x in mx.outputs if x.type == 'RGBA'][0]
    return mx, A, B, R


def value_node(nt, v=0.0):
    n = nt.nodes.new('ShaderNodeValue'); n.outputs[0].default_value = v; return n


def flow_mat(name, c_lo, c_hi, emv, speed, wave=2.5, rough=0.35):
    """Bands travelling along the object's local +Z (each pipe piece is built with +Z = flow direction)."""
    m = mat(name, c_hi, rough, 0.1); nt = m.node_tree; b = bsdf(m); N = nt.nodes.new; L = nt.links.new
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); ph = value_node(nt)
    sub = N('ShaderNodeMath'); sub.operation = 'SUBTRACT'
    mul = N('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = math.tau / wave
    sn = N('ShaderNodeMath'); sn.operation = 'SINE'
    mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -1.0; mr.inputs['From Max'].default_value = 1.0
    mx, A, B, R = mix_rgba(nt); A.default_value = (*c_lo, 1); B.default_value = (*c_hi, 1)
    L(tc.outputs['Object'], sp.inputs['Vector']); L(sp.outputs['Z'], sub.inputs[0]); L(ph.outputs[0], sub.inputs[1])
    L(sub.outputs[0], mul.inputs[0]); L(mul.outputs[0], sn.inputs[0]); L(sn.outputs[0], mr.inputs['Value'])
    L(mr.outputs['Result'], mx.inputs['Factor']); L(R, b.inputs['Base Color']); L(R, b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = emv
    KS(ph.outputs[0], [(0.0, 0.0), (T_END, speed * T_END)]); linear(nt)
    return m


def seg(name, a, b, r, m, segs=20):
    """Cylinder from a to b; origin at a, local +Z along a->b (flow / draw-on direction)."""
    a, b = Vector(a), Vector(b); d = b - a; L = d.length
    bm = bmesh.new(); res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r, radius2=r, depth=L)
    bmesh.ops.translate(bm, vec=(0, 0, L / 2), verts=res['verts'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    for p in me.polygons: p.use_smooth = abs(p.normal.z) < 0.5
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    o.location = a; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    return o


def pipe(name, pts, r, m, fl):
    for i in range(len(pts) - 1):
        seg(f'{name}_{i}', pts[i], pts[i + 1], r, m)
    J = Acc(name + '_fittings', fl)
    for p in pts[1:-1]: J.sphere(r * 1.12, p, sub=2)
    for i in range(len(pts) - 1):
        a, b = Vector(pts[i]), Vector(pts[i + 1]); d = b - a; n = int(d.length // 6)
        for k in range(1, n + 1): J.cyl(r + 0.09, 0.14, a + d * (k / (n + 1)), zrot_to(d), 20)
    J.build(smooth=True)


def arrow(name, a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a; L = d.length; hl = min(L * 0.35, r * 4.5)
    bm = bmesh.new()
    s = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=20, radius1=r, radius2=r, depth=L - hl)
    bmesh.ops.translate(bm, vec=(0, 0, (L - hl) / 2), verts=s['verts'])
    h = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=24, radius1=r * 2.6, radius2=0.0, depth=hl)
    bmesh.ops.translate(bm, vec=(0, 0, L - hl / 2), verts=h['verts'])
    bmesh.ops.remove_doubles(bm, verts=h['verts'], dist=1e-5)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    o.location = a; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.visible_shadow = False
    return o


def prism(name, pts_yz, x0, x1, m):
    bm = bmesh.new(); vs = [bm.verts.new((x0, y, z)) for y, z in pts_yz]
    f = bm.faces.new(vs); r = bmesh.ops.extrude_face_region(bm, geom=[f])
    nv = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(x1 - x0, 0, 0), verts=nv); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    return o


def polar(name, R, rings, segs, zf, m, loc):
    """Disc / mound mesh: z = zf(r, a)."""
    bm = bmesh.new(); c = bm.verts.new((0, 0, zf(0.0, 0.0))); rows = []
    for i in range(1, rings + 1):
        r = R * i / rings
        rows.append([bm.verts.new((r * math.cos(a), r * math.sin(a), zf(r, a))) for a in (math.tau * j / segs for j in range(segs))])
    for j in range(segs): bm.faces.new((c, rows[0][j], rows[0][(j + 1) % segs]))
    for i in range(rings - 1):
        for j in range(segs): bm.faces.new((rows[i][j], rows[i + 1][j], rows[i + 1][(j + 1) % segs], rows[i][(j + 1) % segs]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); o.location = loc
    return o


def half_ring(name, r, depth, m, thick):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=96, radius1=r, radius2=r, depth=depth)
    bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    sol = o.modifiers.new('s', 'SOLIDIFY'); sol.thickness = thick; sol.offset = 0
    return o


def soil(name, m, x0, x1, ztop, zbot, cutters):
    o = Acc(name, m); o.box((x1 - x0, 300, ztop - zbot), ((x0 + x1) / 2, 150, (ztop + zbot) / 2)); ob = o.build()
    for cu, (cz0, cz1) in cutters:
        if cz1 < zbot or cz0 > ztop: continue
        md = ob.modifiers.new('cut', 'BOOLEAN'); md.object = cu; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
        bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier=md.name)
    return ob


def seam_spans(z):
    iv = [(-XE, XE)]; cuts = []
    if TZ - TR - TL - 0.3 <= z <= TZ + TR + TL + 0.3: cuts.append((XS, 1.2))
    if z >= -43.5: cuts.append((XS - 9, XS + 9))
    for c0, c1 in cuts:
        nv = []
        for a, b in iv:
            if c1 <= a or c0 >= b: nv.append((a, b)); continue
            if a < c0: nv.append((a, c0))
            if c1 < b: nv.append((c1, b))
        iv = nv
    return iv


# ---------------------------------------------------------------- ground, tunnel, shaft (ch3 look)
def ground():
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=TR + TL + 0.3, depth=1.2 - XS, location=((XS + 1.2) / 2, 0, TZ), rotation=(0, math.pi / 2, 0))
    bore = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=9.0, depth=50.0, location=(XS, 0, -18.0))
    shaft = bpy.context.active_object
    cutters = [(bore, (TZ - 7.5, TZ + 7.5)), (shaft, (-43.0, 7.0))]
    L = [('seabed_mud', (0.05, 0.04, 0.03), -6, -9), ('soft_clay', (0.34, 0.22, 0.12), -9, -20), ('stiff_clay', (0.52, 0.36, 0.2), -20, -30),
         ('weathered_rock', (0.24, 0.22, 0.2), -30, -46), ('basalt', (0.09, 0.1, 0.13), -46, -90)]
    for nm, c, z0, z1 in L:
        soil(nm, noisy(mat(nm, c, 0.85), 16.0, 0.55, 0.55), -XE, XE, z0, z1, cutters)
    soil('land_fill', noisy(mat('land_fill', (0.27, 0.23, 0.17), 0.9), 10.0, 0.6, 0.5), -XE, -100, 2.0, -6.0, [(shaft, (-43.0, 7.0))])
    for cu in (bore, shaft): bpy.data.objects.remove(cu, do_unlink=True)
    seam = Acc('layer_seams', mat('seam', (0.03, 0.03, 0.035), 0.9))
    for z in (-6, -9, -20, -30, -46):
        for a, b in seam_spans(z): seam.box((b - a, 0.12, 0.35), ((a + b) / 2, -0.04, z))
    seam.build()
    ws = dithered(mat('water_section', (0.02, 0.18, 0.24), 0.3, 0.0, (0.03, 0.22, 0.3), 0.8), 0.6)
    S = Acc('water_section', ws); S.box((XE + 100, 0.1, 6), ((XE - 100) / 2, -0.05, -3)); S.build()
    # segment lining between the shaft eye and the shield tail, ring seams in the shader (as ch3)
    lm = mat('lining', (0.42, 0.41, 0.39), 0.6); nt = lm.node_tree; b = bsdf(lm)
    tc = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'
    wv.inputs['Scale'].default_value = 0.5; wv.wave_profile = 'SAW'
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.5; bp.inputs['Distance'].default_value = 0.15
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    x0 = XS + 9.0; Ln = -14.0 - x0
    lin = half_ring('lining', TR + TL * 0.5, Ln, lm, TL); lin.rotation_euler = (0, math.pi / 2, 0); lin.location = (x0 + Ln / 2, 0, TZ)
    conc = noisy(mat('shaft_concrete', (0.45, 0.44, 0.41), 0.8), 5.0, 0.7, 0.3)
    sw = half_ring('shaft_wall', 8.5, 29.6, conc, 1.0); sw.location = (XS, 0, -27.0 + 14.8)
    Cc = Acc('shaft_slab', conc); Cc.box((18.0, 9.0, 1.0), (XS, 4.5, TZ - 7.95)); Cc.box((20.0, 1.2, 0.8), (XS, 9.6, 2.4))
    for s in (-1, 1): Cc.box((1.2, 10.0, 0.8), (XS + s * 9.6, 5.0, 2.4))
    Cc.build()
    return lin


# ---------------------------------------------------------------- the Mixshield chambers
def ghost_shield():
    gm = noisy(mat('shield_xray', (0.10, 0.17, 0.26), 0.45, 0.4, (0.35, 0.65, 0.9), 0.0), 3.0, 0.7, 0.15); dithered(gm)
    nt = gm.node_tree; b = bsdf(gm); N = nt.nodes.new; Lk = nt.links.new
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.0
    va, ve = value_node(nt, 1.0), value_node(nt, 0.0)
    ad = N('ShaderNodeMath'); ad.operation = 'MULTIPLY_ADD'; ad.use_clamp = True; ad.inputs[1].default_value = 0.45
    em = N('ShaderNodeMath'); em.operation = 'MULTIPLY'
    Lk(lw.outputs['Facing'], pw.inputs[0]); Lk(pw.outputs[0], ad.inputs[0]); Lk(va.outputs[0], ad.inputs[2]); Lk(ad.outputs[0], b.inputs['Alpha'])
    Lk(pw.outputs[0], em.inputs[0]); Lk(ve.outputs[0], em.inputs[1]); Lk(em.outputs[0], b.inputs['Emission Strength'])
    KS(va.outputs[0], [(0.0, 1.0), (0.4, 1.0), (2.6, 0.14), (6.8, 0.14), (7.6, 0.06), (10.2, 0.11)])
    KS(ve.outputs[0], [(0.0, 0.0), (0.4, 0.0), (2.6, 2.2), (7.6, 1.2), (10.2, 1.8)])
    for nm in ('shield', 'shield_detail'):
        o = bpy.data.objects[nm]; me = o.data
        bm = bmesh.new(); bm.from_mesh(me); bm.normal_update()
        caps = [f for f in bm.faces if abs(f.normal.z) > 0.9 and f.calc_area() > 1.0]   # big end discs would wall off the chambers
        bmesh.ops.delete(bm, geom=caps, context='FACES_ONLY'); bm.to_mesh(me); bm.free()
        me.materials.clear(); me.materials.append(gm); o.visible_shadow = False


def chambers():
    steel = noisy(mat('bulkhead', (0.16, 0.17, 0.18), 0.5, 0.85, (0.35, 0.6, 0.8), 0.0), 4.0, 0.65, 0.15)
    wallm = noisy(mat('submerged_wall', (0.20, 0.21, 0.22), 0.5, 0.85, (0.35, 0.6, 0.8), 0.0), 4.0, 0.65, 0.15)
    for m in (steel, wallm):
        KS(bsdf(m).inputs['Emission Strength'], [(0.0, 0.0), (6.8, 0.0), (7.6, 0.55), (9.9, 0.55), (10.8, 0.12)])
    dark = mat('chamber_dark', (0.05, 0.05, 0.055), 0.5, 0.9)
    hyd = mat('chamber_hyd', (0.6, 0.61, 0.62), 0.25, 1.0)
    paint = noisy(mat('manlock_paint', (0.55, 0.36, 0.05), 0.5, 0.3), 3.0, 0.7, 0.1)
    # submerged wall: circle minus the bottom cap (open below Z_OPEN so slurry passes under it)
    a0 = math.asin((Z_OPEN - TZ) / RC); a1 = math.pi - a0
    pts = [(RC * math.cos(a0 + (a1 - a0) * k / 72), TZ + RC * math.sin(a0 + (a1 - a0) * k / 72)) for k in range(73)]
    prism('submerged_wall', pts, X_SW - SW_T / 2, X_SW + SW_T / 2, wallm)
    B = Acc('bulkhead', steel); B.cyl(RC + 0.1, BH_T, (X_BH, 0, TZ), XQ, 64)
    xr = X_BH - BH_T / 2
    B.cyl(1.3, 0.3, (xr - 0.15, 0, TZ), XQ, 32)                                   # centre boss
    for ang in range(0, 360, 30):
        if ang in (30, 60, 90): continue                                           # manlock side
        a = math.radians(ang); u = Vector((0, math.cos(a), math.sin(a)))
        B.beam(Vector((xr - 0.2, 0, TZ)) + u * 1.3, Vector((xr - 0.2, 0, TZ)) + u * 6.3, 0.22)
    B.build()
    D = Acc('bulkhead_bolts', dark)
    for i in range(40):
        a = i * math.tau / 40; D.cyl(0.06, 0.12, (xr - 0.06, 6.2 * math.cos(a), TZ + 6.2 * math.sin(a)), XQ, 8)
    for s in (-1, 1):                                                              # stone crusher jaws at the chamber invert
        D.box((0.8, 0.45, 1.5), (-2.15, s * 0.85, TZ - 5.45), Quaternion((1, 0, 0), s * 0.25))
    D.build()
    H = Acc('crusher_rams', hyd)
    for s in (-1, 1): H.beam((-2.15, s * 2.4, TZ - 5.0), (-2.15, s * 1.2, TZ - 5.3), 0.16)
    H.build()
    M = Acc('manlock', paint)
    M.cyl(0.95, 2.6, (xr - 1.3, 2.7, TZ + 3.1), XQ, 40); M.cyl(1.05, 0.12, (xr - 0.1, 2.7, TZ + 3.1), XQ, 40)
    M.build(smooth=True)
    D2 = Acc('manlock_door', dark); D2.cyl(0.78, 0.12, (xr - 2.66, 2.7, TZ + 3.1), XQ, 32)
    for dz in (-0.5, 0.5): D2.box((0.15, 0.25, 0.3), (xr - 2.7, 1.95, TZ + 3.1 + dz))
    D2.build()
    pm = mat('chamber_pipe', (0.38, 0.30, 0.22), 0.45, 0.7)
    pipe('feed_in', [(X_BH + BH_T / 2, 1.4, TZ - 4.8), (-4.9, 1.4, TZ - 4.8), (-4.9, -4.2, TZ - 4.8), (-4.9, -4.2, TZ + 4.6), (-1.5, -4.2, TZ + 4.6)], 0.28, pm, dark)
    pipe('suction_in', [(X_BH + BH_T / 2, 0.5, TZ - 4.8), (-3.4, 0.5, TZ - 5.3)], 0.3, pm, dark)
    # glowing chamber outline (edge rings + longitudinal edges of the excavation chamber)
    gl = mat('chamber_glow', (0.6, 0.85, 1.0), 0.4, 0.0, (0.55, 0.85, 1.0), 0.0)
    KS(bsdf(gl).inputs['Emission Strength'], [(0.0, 0.0), (3.5, 0.0), (4.4, 3.4), (6.6, 3.4), (7.4, 2.2), (10.5, 0.9), (13.0, 0.5)])
    for x in (X_CF - 0.05, X_SW + SW_T / 2 + 0.03):
        bpy.ops.mesh.primitive_torus_add(major_radius=RC - 0.05, minor_radius=0.07, major_segments=128, minor_segments=8, location=(x, 0, TZ), rotation=(0, math.pi / 2, 0))
        t = bpy.context.active_object; t.data.materials.append(gl); t.visible_shadow = False
    G = Acc('chamber_edges', gl)
    for k in range(8):
        a = k * math.tau / 8; y, z = (RC - 0.05) * math.cos(a), TZ + (RC - 0.05) * math.sin(a)
        G.beam((X_SW + SW_T / 2 + 0.03, y, z), (X_CF - 0.05, y, z), 0.1)
    G.build().visible_shadow = False
    # slurry volumes: cylinders intersected with rising cutter boxes (fill), air cushion = the remainder of the working chamber
    sl = noisy(mat('slurry', (0.21, 0.20, 0.18), 0.28, 0.0), 5.0, 0.7, 0.15)
    am = dithered(mat('air_cushion', (0.6, 0.85, 1.0), 0.15, 0.0, (0.55, 0.85, 1.0), 0.3), 0.0)
    KS(bsdf(am).inputs['Alpha'], [(0.0, 0.0), (12.4, 0.0), (20.4, 0.0), (21.2, 0.2), (35.3, 0.2),   # off while the macro camera sits inside it
        (35.8, 0.55), (38.7, 0.55), (39.5, 0.2)])
    KS(bsdf(am).inputs['Emission Strength'], [(0.0, 0.3), (35.3, 0.3), (35.8, 1.2), (38.7, 1.2), (39.5, 0.3)])

    inv = dithered(mat('cutter_invisible', (0, 0, 0), 1.0), 0.0)

    def cutter(name, levels, off=0.0):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0)); c = bpy.context.active_object; c.name = name
        c.scale = (20, 20, 30); c.display_type = 'WIRE'
        c.data.materials.append(inv); c.visible_camera = c.visible_shadow = c.visible_diffuse = c.visible_glossy = c.visible_transmission = c.visible_volume_scatter = False   # hide_render would drop it from the render depsgraph and the boolean stops cutting
        K(c, 'location', [(t, (-3.0, 0.0, lv + off - 15.0)) for t, lv in levels])
        return c

    def vol(name, x0, x1, m, cu, op):
        A = Acc(name, m); A.cyl(RC, x1 - x0, ((x0 + x1) / 2, 0, TZ), XQ, 96); o = A.build()
        md = o.modifiers.new('fill', 'BOOLEAN'); md.object = cu; md.operation = op; md.solver = 'EXACT'
        o.visible_shadow = (op == 'INTERSECT')
        return o
    front = [(0.0, TZ - 6.8), (10.45, TZ - 6.8), (12.9, TZ + 6.8)]
    back = [(0.0, TZ - 6.8), (10.6, TZ - 6.8), (12.9, L_BACK), (35.4, L_BACK), (36.3, L_BACK + 1.2), (37.2, L_BACK - 1.0), (38.0, L_BACK + 0.6), (38.7, L_BACK)]
    cf, cb, ca = cutter('cut_front', front), cutter('cut_back', back), cutter('cut_air', back, 0.03)
    xb0, xb1 = X_BH + BH_T / 2 + 0.003, X_SW - SW_T / 2 - 0.003
    vol('slurry_front', X_SW - 0.05, X_CF + 0.1, sl, cf, 'INTERSECT')
    vol('slurry_back', xb0, xb1, sl, cb, 'INTERSECT')
    vol('air_cushion', xb0, xb1, am, ca, 'DIFFERENCE')
    # glowing slurry/air interface line (box tracks the level, width follows the chamber chord)
    ifm = dithered(mat('air_interface', (0.75, 0.95, 1.0), 0.2, 0.0, (0.75, 0.95, 1.0), 0.0), 0.85)
    KS(bsdf(ifm).inputs['Emission Strength'], [(0.0, 0.0), (34.9, 0.0), (35.8, 2.8), (38.7, 2.8), (39.5, 0.0)])
    Ib = Acc('air_interface', ifm); Ib.box((xb1 - xb0, 2.0, 0.14), (0, 0, 0)); ib = Ib.build(); ib.visible_shadow = False
    hw = lambda lv: math.sqrt(max(0.0, RC * RC - (lv - TZ) ** 2)) - 0.02
    K(ib, 'location', [(t, ((xb0 + xb1) / 2, 0, lv + 0.02)) for t, lv in back])
    K(ib, 'scale', [(0.0, (0, 0, 0)), (34.7, (0, 0, 0))] + [(t, (1, hw(lv), 1)) for t, lv in back if t >= 35.4] + [(39.6, (1, hw(L_BACK), 1)), (39.8, (0, 0, 0))])   # only for line 46 (it would cover the macro surface)
    return steel


def gauge():
    """Pressure gauge on the rear face of the bulkhead (dial normal -> world -x, dial up -> world +z)."""
    g = empty('gauge', (X_BH - BH_T / 2 - 0.1, -2.6, TZ + 0.7)); g.rotation_mode = 'QUATERNION'
    g.rotation_quaternion = Matrix(((0, 0, -1), (-1, 0, 0), (0, 1, 0))).to_quaternion()
    hs = mat('gauge_housing', (0.06, 0.065, 0.07), 0.35, 1.0); chrome = mat('gauge_bezel', (0.75, 0.76, 0.78), 0.15, 1.0)
    face = mat('gauge_face', (0.86, 0.83, 0.74), 0.5, 0.0, (0.86, 0.83, 0.74), 0.12)
    ink = mat('gauge_ink', (0.03, 0.03, 0.03), 0.5); grn = mat('gauge_green', (0.08, 0.45, 0.14), 0.5)
    amb = mat('gauge_amber', (0.75, 0.45, 0.03), 0.5); red = mat('gauge_red', (0.6, 0.06, 0.04), 0.5)
    A = Acc('gauge_housing', hs); A.cyl(0.52, 0.2, (0, 0, 0), None, 48); A.cyl(0.1, 0.5, (0, -0.62, 0), Quaternion((1, 0, 0), math.pi / 2), 16); A.build(g, True)
    Acc_b = Acc('gauge_bezel', chrome); Acc_b.cyl(0.56, 0.06, (0, 0, 0.08), None, 48)   # top at 0.11, below the dial (was coplanar -> z-fight flicker); Acc_b.build(g, True)
    Fc = Acc('gauge_face', face); Fc.cyl(0.47, 0.02, (0, 0, 0.125), None, 48); Fc.build(g)
    P = lambda a, r: (-math.sin(a) * r, math.cos(a) * r)
    for acc_name, m, ranges in (('gauge_band_g', grn, [(-22, 22)]), ('gauge_band_a', amb, [(22, 60), (-60, -22)]), ('gauge_band_r', red, [(60, 125), (-125, -60)])):
        Bd = Acc(acc_name, m)
        for lo, hi in ranges:
            for d in range(lo, hi, 3):
                a = math.radians(d + 1.5); x, y = P(a, 0.39); Bd.box((0.055, 0.04, 0.012), (x, y, 0.141), Quaternion((0, 0, 1), a))
        Bd.build(g)
    T = Acc('gauge_ticks', ink)
    for d in range(-120, 121, 20):
        a = math.radians(d); x, y = P(a, 0.32); T.box((0.014, 0.075, 0.01), (x, y, 0.142), Quaternion((0, 0, 1), a))
    T.cyl(0.045, 0.03, (0, 0, 0.16), None, 16); T.build(g)
    nd = empty('gauge_needle_pivot', (0, 0, 0.156), g)
    N_ = Acc('gauge_needle', mat('needle', (0.75, 0.05, 0.03), 0.4, 0.0, (0.9, 0.08, 0.04), 0.6)); N_.box((0.02, 0.34, 0.01), (0, 0.13, 0.0)); N_.build(nd)
    gl = dithered(mat('gauge_glass', (0.8, 0.85, 0.9), 0.35, 0.0), 0.12); Gg = Acc('gauge_glass', gl); Gg.cyl(0.48, 0.008, (0, 0, 0.165), None, 48)
    gg = Gg.build(g); gg.visible_shadow = False; gg.hide_render = True    # glass flickered (alpha sorting); a fixed emissive glint replaces it
    Gl = Acc('gauge_glint', mat('gauge_glint', (1, 1, 1), 0.5, 0.0, (1.0, 0.97, 0.9), 2.0)); Gl.cyl(0.035, 0.004, (0.17, 0.2, 0.17), None, 12); Gl.build(g).visible_shadow = False
    nd.rotation_mode = 'XYZ'
    K(nd, 'rotation_euler', [(t, (0, 0, v)) for t, v in ((0.0, 1.95), (30.9, 1.95), (31.7, -0.6), (32.3, 0.32), (32.9, -0.15), (33.4, 0.06), (34.0, 0.0))])


def macro():
    """Bentonite powder drifting in a light shaft, swirling down into the working-chamber surface (lines 40-41)."""
    rng = random.Random(11)
    pm = mat('bentonite', (0.45, 0.40, 0.33), 0.8, 0.0, (0.6, 0.5, 0.4), 0.15)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0); me = bpy.data.meshes.new('powder'); bm.to_mesh(me); bm.free()
    me.materials.append(pm)
    for i in range(260):
        o = bpy.data.objects.new(f'powder_{i}', me); bpy.context.scene.collection.objects.link(o); o.visible_shadow = False
        r0 = rng.uniform(0.2, 0.92); th0 = rng.uniform(0, math.tau); h0 = rng.uniform(0.35, 2.3); s = rng.uniform(0.004, 0.012)
        ta = rng.uniform(12.6, 16.6); dur = rng.uniform(2.5, 4.0); tb = ta + dur
        for k in range(10):
            u = k / 9; r = r0 * (1 - 0.6 * u); th = th0 + (0.6 * u + 2.2 * u * u) * (1 + 0.5 / r0)
            o.location = (SWC[0] + r * math.cos(th), SWC[1] + r * math.sin(th), L_BACK + 0.02 + h0 * (1 - u ** 2))
            o.keyframe_insert('location', frame=F(ta + u * dur))
        K(o, 'scale', [(ta - 0.04, (0, 0, 0)), (ta + 0.3, (s, s, s)), (tb - 0.2, (s, s, s)), (tb, (0, 0, 0))])
    sw = mat('swirl', (0.07, 0.08, 0.08), 0.08, 0.0)
    KS(bsdf(sw).inputs['Base Color'], [(13.4, (0.07, 0.08, 0.08, 1)), (19.5, (0.20, 0.18, 0.15, 1))])
    KS(bsdf(sw).inputs['Roughness'], [(13.4, 0.08), (19.5, 0.32)])
    zf = lambda r, a: 0.035 * math.sin(3 * a + 10 * r) * (1 - r) ** 0.7 * min(1.0, r * 4) - 0.05 * (1 - r) ** 2
    d = polar('swirl_disc', 1.0, 28, 96, zf, sw, (SWC[0], SWC[1], L_BACK + 0.015))
    K(d, 'scale', [(12.7, (0, 0, 0)), (12.9, (1, 1, 1)), (20.4, (1, 1, 1)), (20.6, (0, 0, 0))])
    K(d, 'rotation_euler', [(12.9, (0, 0, 0)), (20.6, (0, 0, -math.radians(560)))]); linear(d)
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=48, radius1=1.1, radius2=0.06, depth=3.35)
    me2 = bpy.data.meshes.new('light_beam'); bm.to_mesh(me2); bm.free()
    bmat = dithered(mat('light_beam', (0, 0, 0), 1.0, 0.0, (1.0, 0.92, 0.75), 1.0), 0.0); me2.materials.append(bmat)
    KS(bsdf(bmat).inputs['Alpha'], [(12.6, 0.0), (13.4, 0.07), (19.6, 0.07), (20.4, 0.0)])
    bo = bpy.data.objects.new('light_beam', me2); bpy.context.scene.collection.objects.link(bo); bo.location = (SWC[0], SWC[1], L_BACK + 1.7); bo.visible_shadow = False
    bo.hide_render = True                                                   # the haze cone washed the macro out; the spot alone reads better
    bpy.ops.object.light_add(type='SPOT', location=(SWC[0], SWC[1] - 0.3, L_BACK + 3.5)); sp = bpy.context.active_object
    sp.data.spot_size = math.radians(42); sp.data.spot_blend = 0.4; sp.data.color = (1.0, 0.9, 0.72); sp.data.shadow_soft_size = 0.1
    bpy.ops.object.light_add(type='SPOT', location=(SWC[0], SWC[1] + 2.4, L_BACK + 0.45)); rk = bpy.context.active_object   # low raking light skimming the surface from the far side
    rk.rotation_mode = 'QUATERNION'; rk.rotation_quaternion = Vector((0, 2.4, 0.5)).to_track_quat('Z', 'Y')
    rk.data.spot_size = math.radians(55); rk.data.spot_blend = 0.6; rk.data.color = (1.0, 0.82, 0.6); rk.data.shadow_soft_size = 0.1
    for t, e in ((0.0, 0.0), (12.6, 0.0), (13.3, 90.0), (19.7, 90.0), (20.5, 0.0)):
        sp.data.energy = e; sp.data.keyframe_insert('energy', frame=F(t))
        rk.data.energy = e * 0.2; rk.data.keyframe_insert('energy', frame=F(t))


def arrows():
    gm = mat('arrow_gold', (0.96, 0.72, 0.0), 0.4, 0.0, (0.96, 0.72, 0.0), 3.5)
    bm_ = mat('arrow_blue', (0.1, 0.65, 1.0), 0.4, 0.0, (0.1, 0.65, 1.0), 3.5)
    Z = (-4.2, -2.1, 0.0, 2.1, 4.2)
    hide = (0, 0, 0)
    for i, z in enumerate(Z):
        o = arrow(f'gold_{i}', (-2.4, -7.6, TZ + z), (1.75, -7.6, TZ + z), 0.2, gm); d = i * 0.08
        keys = [(0.0, hide), (20.25 + d, hide), (20.3 + d, (0.3, 0.3, 0.02)), (21.1 + d, (1, 1, 0.82)), (27.9, (1, 1, 0.82)), (28.8, (1, 1, 1.0))]
        keys += [(29.6 + 0.8 * k, (1, 1, 0.95 if k % 2 == 0 else 1.0)) for k in range(6)] + [(34.8, (1, 1, 1)), (35.4, hide)]
        K(o, 'scale', keys)
    blue = [((9.5, -7.6, TZ + z), (2.0, -7.6, TZ + z)) for z in Z] + [((x, -7.6, -6.5), (x, -7.6, TZ + 8.6)) for x in (4.5, 8.0, 11.5)]
    for i, (a, b) in enumerate(blue):
        o = arrow(f'blue_{i}', a, b, 0.2, bm_); d = i * 0.06
        keys = [(0.0, hide), (25.7 + d, hide), (25.75 + d, (0.3, 0.3, 0.02)), (26.6 + d, (1, 1, 1))]
        keys += [(29.6 + 0.8 * k, (1, 1, 1.0 if k % 2 == 0 else 0.95)) for k in range(6)] + [(34.8, (1, 1, 1)), (35.4, hide)]
        K(o, 'scale', keys)


def slurry_face():
    fm = dithered(mat('slurry_face', (0.42, 0.40, 0.36), 0.3, 0.0, (0.95, 0.82, 0.55), 0.0))
    nt = fm.node_tree; b = bsdf(fm); N = nt.nodes.new; Lk = nt.links.new
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); mr = N('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = 0.0; mr.inputs['From Max'].default_value = 1.2; mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
    vis, em = value_node(nt, 0.0), value_node(nt, 0.0)
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; me_ = N('ShaderNodeMath'); me_.operation = 'MULTIPLY'
    Lk(tc.outputs['Object'], sp.inputs['Vector']); Lk(sp.outputs['X'], mr.inputs['Value']); Lk(mr.outputs['Result'], mu.inputs[0]); Lk(vis.outputs[0], mu.inputs[1])
    Lk(mu.outputs[0], b.inputs['Alpha']); Lk(mr.outputs['Result'], me_.inputs[0]); Lk(em.outputs[0], me_.inputs[1]); Lk(me_.outputs[0], b.inputs['Emission Strength'])
    KS(vis.outputs[0], [(0.0, 0.0), (12.6, 0.0), (13.5, 1.0)])
    KS(em.outputs[0], [(0.0, 0.0), (12.6, 0.0), (13.5, 0.6), (49.6, 0.6), (50.6, 3.2)])
    bm = bmesh.new(); vs = [bm.verts.new(v) for v in ((0, 0, -7.4), (1.2, 0, -7.4), (1.2, 0, 7.4), (0, 0, 7.4))]; bm.faces.new(vs)
    me = bpy.data.meshes.new('slurry_face_band'); bm.to_mesh(me); bm.free(); me.materials.append(fm)
    o = bpy.data.objects.new('slurry_face_band', me); bpy.context.scene.collection.objects.link(o); o.location = (1.2, -0.03, TZ); o.visible_shadow = False
    pts = [(7.3 * math.cos(a), 7.3 * math.sin(a)) for a in (math.pi * (k / 48 - 0.5) for k in range(49))]
    hd = prism('slurry_face_disc', pts, 1.12, 1.18, fm); hd.location = (0, 0, 0); hd.visible_shadow = False
    for v in hd.data.vertices: v.co.z += TZ
    bpy.ops.object.light_add(type='POINT', location=(2.6, -3.0, TZ)); l = bpy.context.active_object
    l.data.color = (1.0, 0.85, 0.6); l.data.shadow_soft_size = 1.5
    for t, e in ((0.0, 0.0), (49.6, 0.0), (50.6, 4000.0)):
        l.data.energy = e; l.data.keyframe_insert('energy', frame=F(t))


# ---------------------------------------------------------------- slurry circuit + separation plant
def circuit():
    dm = flow_mat('slurry_discharge', (0.14, 0.07, 0.03), (0.50, 0.27, 0.10), 0.25, 6.0)
    KS(bsdf(dm).inputs['Emission Strength'], [(0.0, 0.25), (38.8, 0.25), (39.6, 1.4), (43.0, 1.4), (44.0, 0.4)])
    fm = flow_mat('slurry_feed', (0.33, 0.32, 0.30), (0.60, 0.58, 0.53), 0.15, 6.0)
    KS(bsdf(fm).inputs['Emission Strength'], [(0.0, 0.15), (46.3, 0.15), (46.9, 1.0), (49.8, 1.0), (50.6, 0.2)])
    fl = mat('pipe_flange', (0.10, 0.10, 0.11), 0.45, 0.9)
    PX, PY = -170.0, 18.0
    dis = [(-5.6, 0.5, TZ - 4.8), (XS + 1.5, 0.5, TZ - 4.8), (XS + 1.5, 0.5, 4.0), (XS + 1.5, 5.0, 4.0), (PX, 5.0, 4.0), (PX, 5.0, 14.0), (PX, PY - 1.0, 14.0)]
    fed = [(-187.0, 10.0, 4.5), (-183.0, 10.0, 4.5), (-183.0, 3.0, 4.5), (XS - 1.5, 3.0, 4.5), (XS - 1.5, 1.4, 4.5), (XS - 1.5, 1.4, TZ - 4.8), (-5.6, 1.4, TZ - 4.8)]
    pipe('discharge', dis, 0.32, dm, fl); pipe('feed', fed, 0.30, fm, fl)
    return dm, fm, dis, fed


def plant():
    GZ = 2.0; PX, PY = -170.0, 18.0
    conc = noisy(mat('pad_concrete', (0.36, 0.35, 0.33), 0.85), 6.0, 0.7, 0.2)
    stl = noisy(mat('plant_steel', (0.26, 0.29, 0.31), 0.5, 0.7), 4.0, 0.7, 0.1)
    blue = noisy(mat('plant_blue', (0.04, 0.14, 0.30), 0.45, 0.3), 3.0, 0.75, 0.1)
    orng = noisy(mat('cyclone_orange', (0.60, 0.22, 0.03), 0.45, 0.2), 3.0, 0.75, 0.1)
    tnk = noisy(mat('plant_tank', (0.60, 0.60, 0.57), 0.45, 0.2), 2.0, 0.8, 0.1)
    ylw = mat('plant_rail', (0.60, 0.42, 0.02), 0.5, 0.2)
    grt = noisy(mat('plant_grating', (0.2, 0.2, 0.2), 0.7, 0.7), 30.0, 0.5, 0.4)
    dk = mat('plant_dark', (0.04, 0.045, 0.05), 0.5, 0.8)
    lampm = mat('plant_lamp', (1, 0.9, 0.7), 0.4, 0, (1.0, 0.86, 0.62), 4.0)
    winm = mat('plant_window', (0.2, 0.3, 0.35), 0.1, 0, (0.55, 0.8, 1.0), 2.5)
    C, S, Bl, O, T, Y, G, D, Lp, W = [Acc(n, m) for n, m in (('plant_pad', conc), ('plant_frame', stl), ('plant_blue', blue), ('cyclones', orng), ('plant_tanks', tnk),
                                                            ('plant_rails', ylw), ('plant_grating', grt), ('plant_dark', dk), ('plant_lamps', lampm), ('plant_windows', winm))]
    C.box((60, 40, 0.3), (-172, 22, GZ + 0.15))
    # cyclone tower: 4 columns, ring beams at 6 and 12 m, X bracing, grating deck, handrails, stair
    for sx in (-1, 1):
        for sy in (-1, 1): S.box((0.4, 0.4, 13.6), (PX + sx * 3.5, PY + sy * 3.5, GZ + 6.8))
    for z in (6.0, 12.0):
        for s in (-1, 1): S.box((7.4, 0.35, 0.45), (PX, PY + s * 3.5, z)); S.box((0.35, 7.4, 0.45), (PX + s * 3.5, PY, z))
    for s in (-1, 1):
        for za, zb in ((GZ + 0.3, 6.0), (6.0, 12.0)):
            S.beam((PX - 3.5, PY + s * 3.5, za), (PX + 3.5, PY + s * 3.5, zb), 0.18); S.beam((PX + 3.5, PY + s * 3.5, za), (PX - 3.5, PY + s * 3.5, zb), 0.18)
    G.box((7.6, 7.6, 0.08), (PX, PY, 12.25))
    cs = [Vector((PX - 3.8, PY - 3.8, 0)), Vector((PX + 3.8, PY - 3.8, 0)), Vector((PX + 3.8, PY + 3.8, 0)), Vector((PX - 3.8, PY + 3.8, 0))]
    for i in range(4):
        a, b = cs[i], cs[(i + 1) % 4]
        for k in range(7):
            p = a + (b - a) * (k / 6); Y.box((0.06, 0.06, 1.1), (p.x, p.y, 12.85))
        for h in (12.85, 13.4): Y.beam((a.x, a.y, h), (b.x, b.y, h), 0.06)
    for k in range(14):                                                          # stair to the screen deck
        S.box((1.0, 0.3, 0.06), (PX - 4.4, PY - 3.0 + k * 0.42, GZ + 0.3 + k * 0.28))
    for e in (-0.5, 0.5): S.beam((PX - 4.4 + e, PY - 3.2, GZ), (PX - 4.4 + e, PY + 2.8, 6.0), 0.12)
    # 8 hydrocyclones round a distributor drum, overflow launder ring
    Bl.cyl(0.9, 1.2, (PX, PY, 13.6), None, 32)
    for i in range(8):
        a = (i + 0.5) * math.tau / 8; cx, cy = PX + 2.1 * math.cos(a), PY + 2.1 * math.sin(a)
        O.cyl(0.45, 1.1, (cx, cy, 12.85), None, 24); O.cyl(0.1, 2.4, (cx, cy, 11.1), None, 24, r2=0.45)
        D.cyl(0.12, 0.35, (cx, cy, 9.75), None, 12); S.cyl(0.14, 1.3, (cx, cy, 14.05), None, 12)
        S.beam((PX + 0.8 * math.cos(a), PY + 0.8 * math.sin(a), 13.6), (cx - 0.4 * math.cos(a), cy - 0.4 * math.sin(a), 13.1), 0.22)
    for k in range(32):
        a = k * math.tau / 32; S.box((0.48, 0.55, 0.4), (PX + 2.1 * math.cos(a), PY + 2.1 * math.sin(a), 14.75), Quaternion((0, 0, 1), a))
    # two vibrating screens under the cyclones (+x end low), sump tank, chute to the conveyor
    q = Quaternion((0, 1, 0), math.radians(10))
    for s in (-1, 1):
        yc = PY + s * 1.7
        G.box((5.6, 2.8, 0.12), (PX, yc, 7.0), q)
        for e in (-1, 1): Bl.box((5.8, 0.12, 0.9), (PX, yc + e * 1.45, 7.25), q)
        Bl.cyl(0.3, 3.0, (PX - 0.6, yc, 7.9), LATQ, 16); D.box((0.9, 0.6, 0.7), (PX - 0.6, yc + s * 1.9, 7.9))
        for e in (-1, 1): D.cyl(0.18, 0.5, (PX + e * 2.2, yc + 1.2 * s, 6.35), None, 12)          # spring mounts
    Bl.box((6.6, 6.6, 3.2), (PX, PY, GZ + 1.6))
    D.box((1.4, 3.2, 0.12), (PX + 3.2, PY, 6.0), Quaternion((0, 1, 0), math.radians(35)))
    # 3 slurry tanks with agitators, rails, ladders, pumps
    for ty in (10.0, 20.0, 30.0):
        tx = -190.0
        T.cyl(3.2, 7.0, (tx, ty, GZ + 3.5), None, 48); D.cyl(3.3, 0.25, (tx, ty, GZ + 7.0), None, 48); D.cyl(3.25, 0.2, (tx, ty, GZ + 0.3), None, 48)
        S.beam((tx - 3.0, ty, GZ + 7.25), (tx + 3.0, ty, GZ + 7.25), 0.3); Bl.box((1.0, 1.0, 1.2), (tx, ty, GZ + 7.95)); Bl.cyl(0.35, 0.8, (tx, ty, GZ + 8.9), None, 16)
        for j in range(16):
            a = j * math.tau / 16; b = (j + 1) * math.tau / 16
            Y.box((0.06, 0.06, 1.1), (tx + 3.1 * math.cos(a), ty + 3.1 * math.sin(a), GZ + 7.7))
            Y.beam((tx + 3.1 * math.cos(a), ty + 3.1 * math.sin(a), GZ + 8.25), (tx + 3.1 * math.cos(b), ty + 3.1 * math.sin(b), GZ + 8.25), 0.06)
        for e in (-0.25, 0.25): Y.beam((tx + e, ty - 3.3, GZ), (tx + e, ty - 3.3, GZ + 8.3), 0.06)
        for k in range(22): Y.box((0.5, 0.04, 0.04), (tx, ty - 3.3, GZ + 0.35 + k * 0.36))
        D.box((2.6, 1.3, 0.3), (tx + 5.2, ty, GZ + 0.45)); Bl.cyl(0.55, 0.6, (tx + 4.6, ty, GZ + 1.2), LATQ, 24)
        Bl.cyl(0.42, 1.3, (tx + 5.7, ty, GZ + 1.15), XQ, 24); S.beam((tx + 3.1, ty, GZ + 0.9), (tx + 4.2, ty, GZ + 1.2), 0.3)
    # control container, light masts, pipe supports
    Bl.box((6.0, 2.5, 2.6), (-158.0, 9.0, GZ + 1.6)); W.box((2.0, 0.05, 0.8), (-158.6, 7.73, GZ + 2.0)); W.box((1.2, 0.05, 0.8), (-155.6, 7.73, GZ + 2.0))
    for mx, my in ((-197.0, 4.0), (-146.0, 40.0)):
        S.beam((mx, my, GZ), (mx, my, GZ + 16), 0.3); Lp.box((1.8, 0.3, 0.6), (mx, my, GZ + 16.4))
    for x in range(-182, -128, 6):
        if abs(x - XS) > 9.5: S.box((0.25, 0.25, 2.2), (x, 3.0, GZ + 1.1))
    for x in range(-168, -128, 6):
        if abs(x - XS) > 9.5: S.box((0.25, 0.25, 1.7), (x, 5.0, GZ + 0.85))
    for A in (C, S, Bl, O, Y, G, D, Lp, W): A.build()
    T.build()
    # conveyor from under the screens up to the spoil heap; moving belt; clods ride up and drop
    S0, E0 = Vector((-166.0, PY, 5.4)), Vector((-151.0, 30.0, 10.8)); d = E0 - S0; Ln = d.length; dn = d.normalized()
    side = dn.cross(Vector((0, 0, 1))).normalized(); up = side.cross(dn)
    CV = Acc('conveyor_frame', stl); RL = Acc('conveyor_rollers', dk)
    for e in (-1, 1): CV.beam(S0 + side * e * 0.85, E0 + side * e * 0.85, 0.25)
    n = int(Ln / 1.2)
    for k in range(n + 1): RL.cyl(0.1, 1.5, S0 + d * (k / n) + up * 0.05, zrot_to(side), 10)
    for k in range(1, 4):
        p = S0 + d * (k / 4)
        for e in (-1, 1): CV.beam(p + side * e * 0.85, Vector((p.x + side.x * e * 0.85, p.y + side.y * e * 0.85, GZ + 0.3)), 0.2)
    CV.build(); RL.build()
    belt = flow_mat('belt_rubber', (0.02, 0.02, 0.02), (0.08, 0.08, 0.08), 0.0, 2.0, wave=0.6, rough=0.8)
    bm = bmesh.new(); r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, Ln / 2)) @ Matrix.Diagonal((1.4, 0.08, Ln, 1.0)), verts=r['verts'])
    me = bpy.data.meshes.new('conveyor_belt'); bm.to_mesh(me); bm.free(); me.materials.append(belt)
    bo = bpy.data.objects.new('conveyor_belt', me); bpy.context.scene.collection.objects.link(bo)
    bo.location = S0 + up * 0.2; bo.rotation_mode = 'QUATERNION'; bo.rotation_quaternion = d.to_track_quat('Z', 'Y')
    clay = noisy(mat('spoil_clay', (0.30, 0.20, 0.11), 0.75), 3.0, 0.6, 0.6)
    HC = Vector((-150.0, 31.0, GZ))
    rng = random.Random(3)
    polar('spoil_heap', 6.5, 14, 48, lambda r, a: 6.0 * max(0.0, 1 - r / 6.5) ** 1.1 + (0.25 * math.sin(5 * a + r) * min(1.0, r) if r > 0 else 0), clay, HC)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
    for v in bm.verts: v.co *= rng.uniform(0.75, 1.2)
    cm = bpy.data.meshes.new('clod'); bm.to_mesh(cm); bm.free(); cm.materials.append(clay)
    for i in range(26):
        o = bpy.data.objects.new(f'clod_{i}', cm); bpy.context.scene.collection.objects.link(o)
        s = rng.uniform(0.22, 0.42); o.rotation_euler = [rng.uniform(0, 6.28) for _ in range(3)]
        ts = 38.0 + i * 0.5; p0 = S0 + up * 0.45; p1 = E0 + up * 0.45 + dn * 0.6
        rr = rng.uniform(0, 3.0); aa = rng.uniform(0, math.tau)
        land = Vector((HC.x + rr * math.cos(aa), HC.y + rr * math.sin(aa), GZ + 6.0 * (1 - rr / 6.5) ** 1.1 + s * 0.6))
        o.scale = (0, 0, 0); o.keyframe_insert('scale', frame=F(ts - 0.05))
        o.scale = (s, s * 0.8, s * 0.7); o.keyframe_insert('scale', frame=F(ts))
        keys = [(ts - 0.05, p0), (ts, p0), (ts + 2.8, p1)]
        for f in (0.33, 0.66, 1.0):
            q_ = p1.lerp(land, f); q_.z = p1.z + (land.z - p1.z) * f * f; keys.append((ts + 2.8 + 0.5 * f, q_))
        K(o, 'location', keys); linear(o)


def loop_arrow():
    lm = dithered(mat('loop_arrow', (0.9, 0.86, 0.75), 0.4, 0.0, (0.95, 0.9, 0.75), 3.0))
    KS(bsdf(lm).inputs['Alpha'], [(49.9, 1.0), (50.7, 0.0)])
    LOOP = [(-186, -3, 8), (XS - 3, -3, 8), (XS - 3, -3, TZ + 1), (XS + 12, -9.5, TZ + 1), (-4, -9.5, TZ + 1), (1.0, -8.0, TZ + 1)]
    V = [Vector(p) for p in LOOP]; lens_ = [(V[i + 1] - V[i]).length for i in range(len(V) - 1)]; tot = sum(lens_)
    t0, t1 = 46.5, 49.3; tc = t0; times = [t0]
    for i in range(len(V) - 1):
        dt = (t1 - t0) * lens_[i] / tot
        o = seg(f'loop_{i}', V[i], V[i + 1], 0.7, lm, 16); o.visible_shadow = False
        K(o, 'scale', [(0.0, (0, 0, 0)), (tc - 0.04, (0, 0, 0)), (tc, (1, 1, 0.001)), (tc + dt, (1, 1, 1))]); linear(o)
        tc += dt; times.append(tc)
    bm = bmesh.new(); r = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=24, radius1=1.9, radius2=0.0, depth=3.6)
    bmesh.ops.translate(bm, vec=(0, 0, 1.8), verts=r['verts']); bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-5)
    me = bpy.data.meshes.new('loop_head'); bm.to_mesh(me); bm.free(); me.materials.append(lm)
    h = bpy.data.objects.new('loop_head', me); bpy.context.scene.collection.objects.link(h); h.rotation_mode = 'QUATERNION'; h.visible_shadow = False
    dirs = [(V[i + 1] - V[i]).to_track_quat('Z', 'Y') for i in range(len(V) - 1)]
    K(h, 'scale', [(0.0, (0, 0, 0)), (t0 - 0.04, (0, 0, 0)), (t0, (1, 1, 1))])
    K(h, 'location', [(t, V[i]) for i, t in enumerate(times)])
    qk = [(t0, dirs[0])]
    for i in range(1, len(dirs)): qk += [(times[i] - 0.04, dirs[i - 1]), (times[i] + 0.04, dirs[i])]
    K(h, 'rotation_quaternion', qk); linear(h)
    return h


# ---------------------------------------------------------------- lights, world, camera
def lights():
    lamps = []
    Lt = Acc('tunnel_lights', mat('strip', (1, 0.9, 0.7), 0.4, 0, (1.0, 0.88, 0.65), 3.0))
    x0 = XS + 9.0; Ln = -14.0 - x0
    Lt.box((Ln, 0.35, 0.18), (x0 + Ln / 2, 3.7, TZ + 4.9)); Lt.box((Ln, 0.35, 0.18), (x0 + Ln / 2, 5.8, TZ - 0.3)); Lt.build()
    for x in range(-120, 1, 18):
        bpy.ops.object.light_add(type='POINT', location=(x, -2.0, TZ + 3.5)); l = bpy.context.active_object
        l.data.energy = 1800; l.data.color = (1.0, 0.82, 0.55); l.data.shadow_soft_size = 2.0; l.data.use_shadow = False; lamps.append(l)
    bpy.ops.object.light_add(type='AREA', location=(0, -80, -25), rotation=(math.radians(90), 0, 0)); f = bpy.context.active_object
    f.data.energy = 140000; f.data.size = 240; f.data.color = (0.8, 0.92, 1.0); f.data.use_shadow = False; lamps.append(f)
    for l in lamps:                                                               # line 38: the chamber isolated, the rest dims
        e0 = l.data.energy
        for t, k in ((6.8, 1.0), (7.6, 0.45), (9.8, 0.45), (10.6, 1.0)):
            l.data.energy = e0 * k; l.data.keyframe_insert('energy', frame=F(t))

    def aim(kind, loc, target, energy, size, col):
        bpy.ops.object.light_add(type=kind, location=loc); l = bpy.context.active_object
        l.rotation_mode = 'QUATERNION'; l.rotation_quaternion = (Vector(loc) - Vector(target)).to_track_quat('Z', 'Y')
        l.data.energy = energy; l.data.color = col
        if kind == 'AREA': l.data.size = size
        else: l.data.shadow_soft_size = size; l.data.use_shadow = False      # small fill (gauge): no cast shadow
        return l
    ck = aim('AREA', (-3, -14, TZ + 4), (-3, 0, TZ), 900, 8, (1.0, 0.95, 0.88))
    for t, e in ((0.0, 900), (12.7, 900), (13.4, 110), (19.8, 110), (20.7, 900)):      # macro: dark chamber, light only from the beam + raking lamp
        ck.data.energy = e; ck.data.keyframe_insert('energy', frame=F(t))           # chamber key through the x-ray skin
    aim('POINT', (-7.0, -4.6, TZ + 3.2), (-5.6, -2.6, TZ + 0.7), 50, 0.6, (1.0, 0.9, 0.75))   # gauge
    aim('AREA', (-150, -45, 55), (-170, 20, 5), 30000, 70, (1.0, 0.93, 0.82))         # separation plant


def world():
    sc = bpy.context.scene
    w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    tcw = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = -0.6; mr.inputs['From Max'].default_value = 0.7
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.004, 0.03, 0.045, 1); cr.color_ramp.elements[1].color = (0.03, 0.2, 0.26, 1)
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.9; ot = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(tcw.outputs['Generated'], sep.inputs['Vector']); nt.links.new(sep.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], ot.inputs['Surface'])


def build():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    ground()
    tbm, head = build_tbm('tbm', gantries=8)
    tbm.location = (0, 0, TZ)
    K(head, 'rotation_euler', [(0.0, (0, 0, 0)), (T_END, (0, 0, math.radians(200)))]); linear(head)
    ghost_shield(); chambers(); gauge(); macro(); arrows(); slurry_face(); circuit(); plant()
    head_arrow = loop_arrow(); lights(); world()
    return head_arrow


def run(args):
    from bpy_extras.object_utils import world_to_camera_view
    loop_head = build()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, int(T_END * FPS), FPS
    cam, tg = path_camera(PATH, FPS)
    sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 64
    # anti-flicker: big shadow pool (dropped virtual-shadow tiles flickered), stable shadow sampling, no jitter
    for k, v in (('shadow_pool_size', '4096'), ('shadow_resolution_scale', 1.0), ('shadow_ray_count', 2), ('shadow_step_count', 8)):
        if hasattr(sc.eevee, k):
            try: setattr(sc.eevee, k, v)
            except Exception: pass
    for o in sc.objects:
        if o.type == 'LIGHT':
            if hasattr(o.data, 'use_shadow_jitter'): o.data.use_shadow_jitter = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, int(args.get('pct', 50))
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.1
    A = [(36, 'chamber', (-1.85, -6.4, TZ), 2.6), (37, 'chamber_outline', (-1.75, -4.6, TZ + 4.6), 5.0),
         (38, 'submerged_wall', (-2.9, -3.5, TZ + 3.0), 8.6), (38, 'bulkhead', (-5.4, -3.5, TZ + 3.0), 8.6),
         (39, 'slurry', (-1.85, -5.0, TZ - 2.0), 12.2), (40, 'powder', (SWC[0], SWC[1], L_BACK + 0.5), 15.0),
         (41, 'swirl', (SWC[0], SWC[1], L_BACK), 18.5), (42, 'gold_arrows', (0.0, -7.6, TZ + 4.2), 22.5),
         (43, 'blue_arrows', (8.0, -7.6, TZ + 14.0), 26.8), (44, 'meet', (1.9, -7.6, TZ), 29.5),
         (45, 'gauge', (X_BH - BH_T / 2 - 0.2, -2.6, TZ + 0.7), 33.5), (46, 'air_cushion', (-4.1, -4.0, TZ + 4.5), 36.6),
         (47, 'discharge_pipe', (-100.0, 0.5, TZ - 4.8), 41.0), (48, 'cyclones', (-170.0, 18.0, 13.0), 45.0),
         (48, 'spoil_heap', (-150.0, 31.0, 6.0), 45.0), (49, 'loop_arrow_head', None, 48.0), (50, 'slurry_face', (1.6, 0.0, TZ), 53.0)]
    an = []
    for ln, name, p, t in A:
        sc.frame_set(F(t))
        if p is None: p = loop_head.matrix_world.translation.copy()
        v = world_to_camera_view(sc, cam, Vector(p)); an.append([ln, name, round(t, 2), round(v.x, 3), round(1 - v.y, 3)])
    result['anchors'] = an
    if args.get('mode') == 'track':
        result['track'] = track_screen(cam, {
            'chamber': (lambda: Vector((-1.85, -5.0, TZ + 2.5)), 4.5, 12.5),
            'air_cushion': (lambda: Vector((-4.1, -4.0, TZ + 4.5)), 33.0, 41.0),
            'cyclones': (lambda: Vector((-170.0, 18.0, 13.0)), 41.0, 48.5)}, FPS); return
    if args.get('mode', 'preview') == 'preview':
        for t in args.get('times', (2.6, 5.0, 8.6, 12.2, 15.0, 18.5, 22.5, 26.8, 29.5, 33.5, 36.6, 41.0, 45.0, 48.0, 53.0)):
            sc.frame_set(F(t)); sc.render.filepath = f'{out}/t_{t:06.3f}.png'
            bpy.ops.render.render(write_still=True)
    if args.get('mode') == 'anim':
        video_output(sc, out + '/ch4_slurry.mp4')
        bpy.ops.render.render(animation=True)
    result['ok'] = True


run(args)
