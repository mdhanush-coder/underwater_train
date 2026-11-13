import math, unreal
acts = ex.import_model(inputs['env.glb'])
info = []
for a in acts:
    try:
        o, e = a.get_actor_bounds(False)
        info.append([a.get_actor_label(), a.get_class().get_name(), [round(v / 100) for v in o], [round(v / 100) for v in e]])
    except Exception as ex_:
        info.append([str(a)[:50], 'ERR'])
result['n'] = len(acts)
result['first'] = info[:12]
result['big'] = sorted([i for i in info if len(i) == 4], key=lambda i: -max(i[3]))[:12]
ex.environment('outdoor', sun_elevation=12.0, sun_azimuth=40.0, ground=False)
ex.shape('plane', location=(0, 0, 0.0), scale=(4600, 3600, 1), material=ex.plain_material('w', '#0b2c36', roughness=0.035, two_sided=True), label='Water')
keys = [{'time': 0.0, 'location': [0, 600, 700], 'lookAt': [0, 100, 0]},
        {'time': 1.0, 'location': [-150, 200, 40], 'lookAt': [-140, 70, 1]},
        {'time': 2.0, 'location': [120, 420, 25], 'lookAt': [95, 125, 1]}]
film(acts, keys=keys, duration=2.0, fps=1.5, resolution='720p', lens=28, quality='draft', format='png')
