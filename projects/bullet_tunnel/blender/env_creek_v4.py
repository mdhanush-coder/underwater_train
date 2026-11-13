# Creek environment for Unreal: real terrain (carved creek, tidal mudflats, islands, wooded hills, far-shore city), mangrove forest,
# library trawlers + towers. Flat-colour materials only (glTF), exported as one GLB. Runs after skilllib.py + bt_model.py.
# Blender coords; Unreal = (x, -y, z). Water is NOT here (Unreal plane at z=0).
import bpy, bmesh, math, random
from mathutils import Vector, noise

rng = random.Random(21)
XR, YR, STEP = 2000.0, 1500.0, 10.0
ISLANDS = [(-140, -70, 55), (95, -125, 62), (235, -55, 48), (-310, -210, 90), (40, -320, 110), (520, 60, 70), (-560, 120, 90), (-120, 230, 80)]


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
        if d < r * 1.6: h += 8.7 * math.exp(-(d / r) ** 2 * 1.7) + 0.5 * fbm(x, y, 16) * math.exp(-(d / r) ** 2)
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


def forest():
    bark = mat('mangrove_bark', (0.05, 0.04, 0.032), 0.9)
    la = mat('leaf_a', (0.03, 0.095, 0.03), 0.7); lb = mat('leaf_b', (0.045, 0.12, 0.035), 0.7); lc = mat('leaf_hill', (0.025, 0.07, 0.025), 0.8)
    chunks = []
    def fresh(i):
        return Acc(f'mangrove_trunks_{i}', bark), Acc(f'mangrove_leaves_a_{i}', la), Acc(f'mangrove_leaves_b_{i}', lb)
    T, A, B = fresh(0); C = Acc('hill_forest_0', lc); n = 0; nc = 0
    for _ in range(40000):
        x = rng.uniform(-1500, 1500); y = rng.uniform(-900, 900); h = H(x, y)
        if not (-0.05 < h < 1.6) or fbm(x * 1.3, y * 1.3, 45) < -0.12: continue
        if abs(y) < 120 and abs(x) < 300: continue
        ht = rng.uniform(4.5, 9.0); tx, ty = x + rng.uniform(-0.7, 0.7), y + rng.uniform(-0.7, 0.7)
        T.beam((x, y, h), (tx, ty, h + ht), 0.4)
        for k in range(4):
            b = k * math.tau / 4 + rng.uniform(-0.4, 0.4)
            T.beam((x, y, h + 1.9), (x + math.cos(b) * 1.9, y + math.sin(b) * 1.9, h + 0.05), 0.14)
        L = A if rng.random() < 0.55 else B
        for k in range(3):
            L.sphere(rng.uniform(1.9, 3.1), (tx + rng.uniform(-1.7, 1.7), ty + rng.uniform(-1.7, 1.7), h + ht + rng.uniform(-0.3, 1.9)), (1, 1, 0.78))
        n += 1
        if n % 250 == 0:
            chunks += [(T, False), (A, True), (B, True)]; T, A, B = fresh(n // 250)
        if n >= 2800: break
    for _ in range(4500):
        x = rng.uniform(-1900, 1900); y = rng.uniform(-1450, -640); h = H(x, y)
        if h < 2.0: continue
        C.sphere(rng.uniform(4.0, 7.5), (x, y, h + rng.uniform(2.5, 6)), (1, 1, 0.8), 1)
        nc += 1
        if nc % 900 == 0:
            chunks.append((C, True)); C = Acc(f'hill_forest_{nc // 900}', lc)
    chunks += [(T, False), (A, True), (B, True), (C, True)]
    for o, sm in chunks:
        o.build(smooth=sm)
    result['max_verts'] = max(len(ob.data.vertices) for ob in bpy.data.objects if ob.type == 'MESH')
    return n


def city():
    cols = [(0.20, 0.19, 0.18), (0.28, 0.25, 0.21), (0.16, 0.17, 0.19), (0.30, 0.27, 0.26), (0.22, 0.21, 0.24)]
    accs = [Acc(f'lowrise{i}', mat(f'lowrise{i}', c, 0.85)) for i, c in enumerate(cols)]
    for _ in range(1400):
        x = rng.uniform(-1900, 1900); y = rng.uniform(690, 1450); h = H(x, y)
        w, d_, ht = rng.uniform(22, 55), rng.uniform(22, 55), rng.uniform(14, 75) * (0.5 + 0.5 * max(0.0, 1 - abs(x) / 1600))
        accs[rng.randrange(len(accs))].box((w, d_, ht), (x, y, h + ht / 2))
    for A in accs: A.build()


def library():
    boats = [(-8, -66, 0.4), (-34, -78, 2.9), (14, -52, 3.9), (-62, -112, 1.2)]
    for i, (x, y, yaw) in enumerate(boats):
        try:
            root = place_asset('ai3d-fishing-trawler-boat-43c178', location=(x, y, 0.0), rotation=(0, 0, yaw), size=rng.uniform(12, 15), floor=0.0)
            root.name = f'boat{i}'
        except Exception as e:
            result.setdefault('warn', []).append(str(e)[:100])
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
