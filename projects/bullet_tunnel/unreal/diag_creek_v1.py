# Diagnostic renders for the creek surface (versioned, does not replace creek_surface.py).
# args: test 'A' (static camera, MB off) | 'B' (moving, MB off) | 'C' (moving, MB conservative) | 'D' (moving, production)
# Camera path v2 (Blender coords -> Unreal (x,-y,z)): horizon kept on every key, max 24 m/s, no dive.
import unreal
A = args if isinstance(args, dict) else {}
TEST = A.get('test', 'B')
PATH = [(0.0, (-130, -270, 4.0), (0, 800, 35)), (4.5, (-75, -190, 5.0), (10, 800, 38)), (8.0, (-45, -175, 30.0), (0, 800, 20)),
        (11.5, (-10, -105, 1.6), (0, 800, 25)), (12.5, (-6, -95, 1.2), (0, 800, 25))]
if TEST == 'A':
    PATH = [(0.0, PATH[0][1], PATH[0][2]), (2.0, PATH[0][1], PATH[0][2])]
acts = ex.import_model(inputs['env.glb'])
ex.environment('outdoor', sun_elevation=9.0, sun_azimuth=40.0, ground=False)
ex.shape('plane', location=(0, 0, 0.0), scale=(4600, 3600, 1), material=ex.plain_material('creek_water', '#0b2c36', roughness=0.035, two_sided=True), label='Water')
rep = {}
try:
    fog = ex.spawn(unreal.ExponentialHeightFog, (0, 0, 20), (0, 0, 0))
    c = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
    c.set_editor_property('fog_density', 0.0011); c.set_editor_property('fog_height_falloff', 0.35); c.set_editor_property('start_distance', 120.0)
except Exception as e:
    rep['fog'] = str(e)[:100]
try: ex.post_process(exposure_bias=0.0, bloom=0.3, vignette=0.15)
except Exception as e: rep['pp'] = str(e)[:100]
# motion blur: our own unbound volume at top priority, plus the renderer cvar
mb = {'A': 0.0, 'B': 0.0, 'C': 0.25, 'D': 0.25}[TEST]; mbmax = {'A': 0.0, 'B': 0.0, 'C': 2.0, 'D': 2.0}[TEST]
try:
    v = ex.spawn(unreal.PostProcessVolume, (0, 0, 0), (0, 0, 0))
    v.set_editor_property('unbound', True); v.set_editor_property('priority', 1000.0)
    s = v.get_editor_property('settings')
    s.set_editor_property('override_motion_blur_amount', True); s.set_editor_property('motion_blur_amount', mb)
    s.set_editor_property('override_motion_blur_max', True); s.set_editor_property('motion_blur_max', mbmax)
    v.set_editor_property('settings', s)
    s2 = v.get_editor_property('settings')
    rep['motion_blur_amount'] = s2.get_editor_property('motion_blur_amount'); rep['motion_blur_max'] = s2.get_editor_property('motion_blur_max')
except Exception as e:
    rep['mb_volume'] = str(e)[:140]
try:
    unreal.SystemLibrary.execute_console_command(None, 'r.MotionBlurQuality %d' % (0 if mb == 0 else 4))
    rep['cvar'] = 'r.MotionBlurQuality %d' % (0 if mb == 0 else 4)
except Exception as e:
    rep['cvar'] = str(e)[:100]
keys = [{'time': t, 'location': [c_[0], -c_[1], c_[2]], 'lookAt': [l[0], -l[1], l[2]]} for t, c_, l in PATH]
rep['test'] = TEST; rep['frames'] = int(PATH[-1][0] * 30)
film(acts, keys=keys, duration=PATH[-1][0], fps=30, resolution=A.get('res', '720p'), lens=28,
     quality=A.get('quality', 'draft' if TEST != 'D' else 'standard'), format='mp4')
result.update(rep)
