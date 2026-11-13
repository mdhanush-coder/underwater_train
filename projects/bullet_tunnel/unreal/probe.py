# Unreal probe: helper docs, water/landscape classes, swamp pack contents. No render.
import unreal
res = {}
res['water_classes'] = [n for n in dir(unreal) if n.startswith('Water')][:50]
res['landscape_classes'] = [n for n in dir(unreal) if n.startswith('Landscape')][:30]
res['fog_sky'] = [n for n in dir(unreal) if any(k in n for k in ('SkyAtmosphere', 'VolumetricCloud', 'ExponentialHeightFog', 'SkyLight', 'DirectionalLight', 'Foliage', 'InstancedStaticMesh'))][:30]
res['ex_methods'] = [n for n in dir(ex) if not n.startswith('_')]
docs = {}
for n in ('environment', 'shape', 'plain_material', 'spawn', 'light', 'camera', 'keyframes_path', 'move_path', 'import_model', 'place', 'spawn_asset', 'find_assets', 'open_world', 'use_pack', 'render_preset'):
    try: docs[n] = (getattr(ex, n).__doc__ or '')[:600]
    except Exception as e: docs[n] = 'ERR ' + str(e)[:80]
res['docs'] = docs
try: res['film_doc'] = (film.__doc__ or '')[:900]
except Exception as e: res['film_doc'] = 'ERR'
found = {}
for w in ('tree', 'palm', 'plant', 'reed', 'grass', 'boat', 'dock', 'pier', 'rock', 'mud', 'house', 'hut', 'water', 'bush', 'root', 'log', 'rope', 'barrel', 'crate', 'lamp', 'sky'):
    try:
        r = ex.find_assets(w, kind='mesh', pack='swamp-village-lighthouse')
        found[w] = [(a['path'].split('/')[-1], a.get('size')) if isinstance(a, dict) else str(a)[:80] for a in list(r)[:6]]
    except Exception as e:
        found[w] = 'ERR ' + str(e)[:100]
res['swamp_found'] = found
result.update(res)
