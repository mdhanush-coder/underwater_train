# Unreal: creek surface plate (local 0-10.3 s of lines 6-8): terrain GLB from Blender + sky/sun + water + haze + one camera path.
# args: mode 'flip' (draft PNG flipbook) or 'final'; keys use Blender coords (x, y, z): converted to Unreal (x, -y, z).
import math, unreal
A = args if isinstance(args, dict) else {}
PATH = A.get('path') or [
    (0.0, (-96, -150, 2.8), (-10, -40, 1.2)), (4.5, (-40, -92, 3.6), (10, -20, 1.5)), (5.0, (-36, -96, 6.5), (6, -10, 2.0)),
    (7.6, (-10, -210, 92), (0, 60, 0)), (8.4, (0, -140, 82), (0, -60, 0)), (9.6, (0, -78, 10), (0, -40, -4)), (10.3, (0, -70, -14), (0, 0, -30))]
SUN_AZ = float(A.get('sun_az', 40.0)); SUN_EL = float(A.get('sun_el', 7.0))
acts = ex.import_model(inputs['env.glb'])
ex.environment('outdoor', sun_elevation=SUN_EL, sun_azimuth=SUN_AZ, ground=False)
water = ex.plain_material('creek_water', '#0b2c36', roughness=0.035, two_sided=True)
ex.shape('plane', location=(0, 0, 0.0), scale=(4600, 3600, 1), material=water, label='Water')
warn = []
try:
    fog = ex.spawn(unreal.ExponentialHeightFog, (0, 0, 20), (0, 0, 0))
    c = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
    c.set_editor_property('fog_density', 0.0011)
    c.set_editor_property('fog_height_falloff', 0.35)
    for nm in ('fog_inscattering_luminance', 'inscattering_color', 'fog_inscattering_color'):
        try:
            c.set_editor_property(nm, unreal.LinearColor(0.95, 0.72, 0.5, 1.0)); break
        except Exception as e2:
            warn.append(nm + ' x')
    c.set_editor_property('start_distance', 120.0)
    c.set_editor_property('volumetric_fog', True)
except Exception as e:
    warn.append('fog ' + str(e)[:120])
try: ex.post_process(exposure_bias=A.get('ev', 0.0), bloom=0.5, vignette=0.2)
except Exception as e: warn.append('pp ' + str(e)[:100])
keys = [{'time': t, 'location': [c[0], -c[1], c[2]], 'lookAt': [l[0], -l[1], l[2]]} for t, c, l in PATH]
mode = A.get('mode', 'flip')
if mode == 'flip':
    film(acts, keys=keys, duration=PATH[-1][0], fps=float(A.get('fps', 1.25)), resolution='720p', lens=28, quality='draft', format='png')
else:
    film(acts, keys=keys, duration=PATH[-1][0], fps=30, resolution=A.get('res', '540p' if False else '720p'), lens=28, quality=A.get('quality', 'standard'), format='mp4')
result['warn'] = warn
