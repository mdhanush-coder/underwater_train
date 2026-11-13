# Creek environment for Unreal: real terrain (carved creek, tidal mudflats, islands, wooded hills, far-shore city), mangrove forest,
# library trawlers + towers. Flat-colour materials only (glTF), exported as one GLB. Runs after skilllib.py + bt_model.py.
# Blender coords; Unreal = (x, -y, z). Water is NOT here (Unreal plane at z=0).
import bpy, bmesh, math, random
from mathutils import Vector, noise

rng = random.Random(21)
XR, YR, STEP = 2000.0, 1500.0, 10.0
ISLANDS = [(-135, -28, 62), (118, -62, 74), (265, -18, 58), (-300, -150, 90), (30, -330, 110), (520, 60, 70), (-560, 120, 90), (-120, 260, 80), (20, 150, 70), (-345, -75, 85), (405, -115, 95)]


def fbm(x, y, s, o=5):
    return noise.fractal(Vector((x / s, y / s, 0.37)), 0.55, 2.0, o)


def sstep(a, b, v):
    t = max(0.0, min(1.0, (v - a) / (b - a))); return t * t * (3 - 2 * t)


def H(x, y):
    yc = 70.0 * math.sin(x / 520.0)
    c = abs(y - yc); north = y > yc
    if c < 300: h = -7.0 + 1.5 * fbm(x, y, 70)
    elif c < 430: h = -7.0 + 6.75 * sstep(300, 430, c) + 0.6 * fbm(x, y, 40)
    elif c < 620: h = 0.2 + 0.7 * fbm(x, y, 50) + (c - 430) * 0.0012                 # tidal mudflats, partly exposed
    elif north: h = 0.9 + 0.35 * fbm(x, y, 120) + sstep(620, 700, c) * 0.5             # far-shore land, flat (city)
    else: h = 0.5 + (c - 620) * 0.024 + 4.5 * fbm(x, y, 140) * sstep(640, 900, c)      # wooded hills
    for (cx, cy, r) in ISLANDS:
        d = math.hypot(x - cx, y - cy)
        if d < r * 1.6: h += 9.4 * math.exp(-(d / r) ** 2 * 1.5) + 0.5 * fbm(x, y, 16) * math.exp(-(d / r) ** 2)
    return h


def build_terrain(tile=40):
    """Terrain as 400 m tiles (<= 41x41 verts, x2 for the reversed twin = ~3.4k verts each): large single meshes vanished in
    Unreal's glTF import (16-bit index wrap / Nanite drop on >65k-vertex meshes), so nothing here exceeds ~50k."""
    mats = [mat(n, c, 0.95) for n, c in [('seabed', (0.03, 0.026, 0.02)), ('mud', (0.085, 0.066, 0.048)), ('marsh', (0.06, 0.075, 0.035)),
            ('grass', (0.05, 0.095, 0.035)), ('forest_floor', (0.028, 0.065, 0.03)), ('urban', (0.13, 0.125, 0.12))]]
    nx, ny = int(2 * XR / STEP), int(2 * YR / STEP)
    k_ = 0
    for tj in range(0, ny, tile):
        for ti in range(0, nx, tile):
            bm = bmesh.new(); grid = []
            for j in range(tj, min(tj + tile, ny) + 1):
                row = []
                for i in range(ti, min(ti + tile, nx) + 1):
                    x = -XR + i * STEP; y = -YR + j * STEP
                    row.append(bm.verts.new((x, y, H(x, y))))
                grid.append(row)
            for j in range(len(grid) - 1):
                for i in range(len(grid[0]) - 1):
                    f = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
                    h = (grid[j][i].co.z + grid[j + 1][i + 1].co.z) / 2; y = grid[j][i].co.y
                    k = 0 if h < -0.45 else 1 if h < 0.3 else 2 if h < 1.3 else 3 if h < 5.0 else 4
                    if y > 700 and h > 0.5: k = 5
                    f.material_index = k; f.smooth = True
            dup = bmesh.ops.duplicate(bm, geom=list(bm.faces))
            bmesh.ops.reverse_faces(bm, faces=[g for g in dup['geom'] if isinstance(g, bmesh.types.BMFace)])
            me = bpy.data.meshes.new(f'terrain_{k_:03d}'); bm.to_mesh(me); bm.free()
            for m in mats: me.materials.append(m)
            o = bpy.data.objects.new(f'terrain_{k_:03d}', me); bpy.context.scene.collection.objects.link(o); k_ += 1
    return k_


NEAR = {0, 1, 2, 8, 9, 10}   # islands close to the camera path: smoother, denser canopies


def forest():
    bark = mat('mangrove_bark', (0.05, 0.04, 0.032), 0.9)
    la = mat('leaf_a', (0.03, 0.095, 0.03), 0.7); lb = mat('leaf_b', (0.045, 0.12, 0.035), 0.7); lc = mat('leaf_hill', (0.025, 0.07, 0.025), 0.8)
    st = {'i': 0, 'n': 0}
    def fresh():
        i = st['i']; st['i'] += 1
        return Acc(f'mangrove_trunks_{i}', bark), Acc(f'mangrove_leaves_a_{i}', la), Acc(f'mangrove_leaves_b_{i}', lb)
    st['T'], st['A'], st['B'] = fresh(); chunks = []
    def plant(x, y, h, big=1.0, sub=1):
        T, A, B = st['T'], st['A'], st['B']
        ht = rng.uniform(6.0, 11.0) * big; tx, ty = x + rng.uniform(-0.8, 0.8), y + rng.uniform(-0.8, 0.8)
        T.beam((x, y, h), (tx, ty, h + ht), 0.5)
        for k in range(5):
            b = k * math.tau / 5 + rng.uniform(-0.4, 0.4)
            T.beam((x, y, h + 2.4), (x + math.cos(b) * 2.4, y + math.sin(b) * 2.4, h + 0.05), 0.16)
        L = A if rng.random() < 0.55 else B
        for k in range(4 if sub == 1 else 5):
            L.sphere(rng.uniform(2.4, 4.0) if k < 4 else rng.uniform(1.4, 2.0), (tx + rng.uniform(-2.4, 2.4), ty + rng.uniform(-2.4, 2.4), h + ht + rng.uniform(-0.8, 2.6)), (1, 1, 0.72), sub)
        st['n'] += 1
        if st['n'] % 150 == 0:
            chunks.extend([(T, False), (A, True), (B, True)]); st['T'], st['A'], st['B'] = fresh()
    for ii, (cx, cy, r) in enumerate(ISLANDS):                    # dense mangrove walls on every island
        for _ in range(int(r * r / 22)):
            a_ = rng.uniform(0, math.tau); d_ = r * 0.95 * math.sqrt(rng.random()); x, y = cx + math.cos(a_) * d_, cy + math.sin(a_) * d_; h = H(x, y)
            if h > 0.05: plant(x, y, h, 1.0, 2 if ii in NEAR else 1)
    tries = 0
    while st['n'] < 3300 and tries < 30000:                       # tidal flats along both banks
        tries += 1
        x = rng.uniform(-1300, 1300); y = rng.uniform(-700, 760); h = H(x, y)
        if -0.05 < h < 1.6 and fbm(x * 1.3, y * 1.3, 45) > -0.12 and not (abs(y) < 60 and abs(x) < 300): plant(x, y, h)
    C = Acc('hill_forest_0', lc); nc = 0
    for _ in range(2200):
        x = rng.uniform(-1900, 1900); y = rng.uniform(-1450, -640); h = H(x, y)
        if h < 2.0: continue
        C.sphere(rng.uniform(4.0, 7.5), (x, y, h + rng.uniform(2.5, 6)), (1, 1, 0.8), 1); nc += 1
        if nc % 700 == 0: chunks.append((C, True)); C = Acc(f'hill_forest_{nc // 700}', lc)
    chunks.extend([(st['T'], False), (st['A'], True), (st['B'], True), (C, True)])
    for o, sm in chunks: o.build(smooth=sm)
    result['max_verts'] = max(len(ob.data.vertices) for ob in bpy.data.objects if ob.type == 'MESH')
    return st['n']


def city():
    cols = [(0.22, 0.20, 0.18), (0.34, 0.28, 0.22), (0.16, 0.19, 0.24), (0.38, 0.33, 0.30), (0.20, 0.24, 0.30), (0.30, 0.22, 0.18), (0.14, 0.15, 0.17), (0.42, 0.40, 0.36)]
    accs = [Acc(f'lowrise{i}', mat(f'lowrise{i}', c, 0.8)) for i, c in enumerate(cols)]
    Wn = Acc('city_windows', mat('city_window', (1.0, 0.85, 0.6), 0.3, 0.0, (1.0, 0.8, 0.5), 0.9))
    for _ in range(1000):
        x = rng.uniform(-1900, 1900); y = rng.uniform(690, 1450); h = H(x, y)
        w, d_, ht = rng.uniform(22, 55), rng.uniform(22, 55), rng.uniform(14, 75) * (0.5 + 0.5 * max(0.0, 1 - abs(x) / 1600))
        accs[rng.randrange(len(accs))].box((w, d_, ht), (x, y, h + ht / 2))
        if y < 1100 and rng.random() < 0.65:                      # lit window bands on the face toward the creek (-y)
            for lv in range(int(ht // 6)):
                if rng.random() < 0.7: Wn.box((w * 0.82, 0.25, 1.1), (x, y - d_ / 2 - 0.12, h + 4 + lv * 6))
    for A in accs: A.build()
    Wn.build()


def fishing_boat(x, y, yaw, hull_col, trim_col, name):
    """Thane-creek style wooden fishing boat: long narrow hull with raised bow, stern cabin, flat roof, mast + pennant."""
    L, W, D = 11.0, 2.7, 1.25
    bm = bmesh.new(); rings = []
    for k in range(13):
        u = k / 12.0; hw = max(0.05, W / 2 * (1 - (2 * u - 1) ** 2) ** 0.5 if 0 < u < 1 else 0.05); zt = D + 1.6 * u ** 3.2; kd = 0.55 * (1 - abs(2 * u - 1) ** 2.2)
        pts = [(-hw, zt), (-hw * 0.93, zt - 0.55 * D), (-hw * 0.62, -kd * 0.78), (0.0, -kd), (hw * 0.62, -kd * 0.78), (hw * 0.93, zt - 0.55 * D), (hw, zt)]
        rings.append([bm.verts.new(((u - 0.5) * L, py, pz)) for py, pz in pts])
    for a_, b_ in zip(rings[:-1], rings[1:]):
        for i in range(7): bm.faces.new((a_[i], a_[(i + 1) % 7], b_[(i + 1) % 7], b_[i]))
    bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    me = bpy.data.meshes.new(name + '_hull'); bm.to_mesh(me); bm.free()
    hull = bpy.data.objects.new(name + '_hull', me); bpy.context.scene.collection.objects.link(hull)
    me.materials.append(mat(name + '_paint', hull_col, 0.55))
    for p in me.polygons: p.use_smooth = True
    W_ = Acc(name + '_white', mat(name + '_cabin', (0.55, 0.53, 0.48), 0.7)); K = Acc(name + '_dark', mat(name + '_dark', trim_col, 0.6))
    W_.box((2.6, 1.9, 1.7), (-2.6, 0, D + 0.85)); K.box((3.0, 2.3, 0.14), (-2.6, 0, D + 1.78))             # cabin + roof
    K.beam((0.6, 0, D), (0.6, 0, D + 4.6), 0.12); K.box((1.0, 0.04, 0.6), (1.1, 0, D + 4.1))               # mast + pennant
    K.box((1.6, 0.9, 0.05), (2.8, 0, D + 0.25))                                                              # fish hatch
    for o in (W_, K):
        ob = o.build(); ob.parent = hull
    hull.location = (x, y, 0.15); hull.rotation_euler = (0, 0, yaw)
    return hull


def library():
    for i, (x, y, yaw) in enumerate([(-18, -42, 0.3), (14, -58, -0.45), (46, -30, 0.9), (-52, -66, -0.2), (74, -78, 0.5), (-86, -34, 1.3)]):
        hc = [(0.07, 0.15, 0.32), (0.34, 0.07, 0.05), (0.52, 0.5, 0.45), (0.07, 0.2, 0.3), (0.3, 0.1, 0.05), (0.1, 0.25, 0.22)][i]
        fishing_boat(x, y, yaw, hc, (0.05, 0.05, 0.06), f'boat{i}')
    for k in range(12):
        n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 3][k]
        x = -1000 + k * 175 + rng.uniform(-40, 40); y = rng.uniform(720, 1000); h = H(x, y)
        try:
            root = place_asset(f'metropolitan-skyscraper-{n}', location=(x, y, h), rotation=(0, 0, rng.uniform(0, 6.28)), size=rng.uniform(120, 230), floor=h)
            root.name = f'tower{k}'
        except Exception as e:
            result.setdefault('warn', []).append(str(e)[:100])


for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
if (args or {}).get('mode') == 'diag':
    import statistics
    hs = [H(x, y) for x in range(-1500, 1501, 25) for y in range(-900, 901, 25)]
    result['h_min_max'] = [round(min(hs), 2), round(max(hs), 2)]
    result['frac_above_0'] = round(sum(h > 0 for h in hs) / len(hs), 3)
    result['islands'] = [[cx, cy, round(H(cx, cy), 2)] for cx, cy, r in ISLANDS]
    result['fbm_range'] = [round(min(fbm(x, y, 70) for x in range(-1500, 1500, 37) for y in range(-900, 900, 37)), 2), round(max(fbm(x, y, 70) for x in range(-1500, 1500, 37) for y in range(-900, 900, 37)), 2)]
    build_terrain()
    bpy.ops.mesh.primitive_plane_add(size=6000, location=(0, 0, 0)); wpl = bpy.context.active_object
    wm = bpy.data.materials.new('w'); wm.use_nodes = True; wm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.02, 0.15, 0.3, 1); wpl.data.materials.append(wm)
    cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); bpy.context.scene.collection.objects.link(cam)
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 3400; cam.location = (0, 0, 800); cam.data.clip_end = 5000
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type='SUN'); bpy.context.active_object.data.energy = 3
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x, sc.render.resolution_y = 1200, 700
    sc.render.filepath = out + '/top.png'; bpy.ops.render.render(write_still=True)
else:
    build_terrain()
    result['mangroves'] = forest()
    city()
    library()
    bpy.ops.export_scene.gltf(filepath=out + '/creek_env.glb', export_format='GLB', export_apply=True, export_cameras=False, export_lights=False)
    result['objects'] = len(bpy.data.objects)
